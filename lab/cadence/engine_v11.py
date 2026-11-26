#!/usr/bin/env python3
"""OBM engine v1.1: a curated operating environment around an agent with full autonomy. Task-agnostic.

v1.1 keeps v1's loop (ground-truth measures, process behavior charts, pulse and audit reviews, diagnosis, redesign, all
run by the system in fresh contexts) and changes what reaches the agent and who decides the task-specific parts:

  * The designer owns everything task-specific (R12). It reads the task's brief, the human's requirements and
    swarm/system_interface.md (written here from the adapter), and writes swarm/system.json: the measures to chart, the
    signals that pull a review early, what counts as an opportunity, the exemplar and the cadence. This engine and the
    harness hold nothing about any one task; the task supplies only an adapter.
  * Guidance, never orders (R1). The guidance library (swarm/guidance/G-NNN.md) holds advice, guidelines and examples
    of what good looks like, each with its evidence and a revisit point. Nothing the system gives the agent assigns,
    requires, forbids, blocks or caps an action.
  * Every period the agent gets one compact hand-off (R2, R3, R8): capacity used in the period that just ended, the
    opportunities open at its end and now, the guidance that fits what is open, and anything new. It is information.
  * Reviews and diagnoses change the environment, not the agent (R4, R7): they propose guidance as files in
    swarm/guidance/proposed/, and a fact check against recorded ground truth decides whether each enters the library.
  * The agent's own policies and beliefs are fact-checked and shown back to it, never adopted as rules (R5).
  * Reviews are also triggered by what the agent does (R6): a period ended with capacity unused while opportunities
    were open, repeated early ends, a statement refuted by the ground truth. A slow scheduled review is the backstop.
  * Behavior and cost are measured and shown as information, never as targets or limits (R9, R11).
  * Every role is a prompt in and records out, run by a configurable command on any model (R10).

usage:
  engine_v11.py <config.json>              PostToolUse on the period-ending tool (reads the hook's JSON on stdin)
  engine_v11.py <config.json> --pre        PreToolUse on the same tool: notes the state as the period ends
  engine_v11.py <config.json> --interface  writes swarm/system_interface.md for the designer, before the run
Config keys (all task-agnostic): workspace, log, adapter ("module:Class"), adapter_args, model, role_models
({pulse, audit, diagnosis, redesign, check}: model), runner (optional command template, a list with {prompt}, {model},
{budget}, {turns}), hook_event, budgets ({role: USD}), review_timeout_s.
"""
import importlib, json, operator, re, shlex, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import charts

OPS = {"==": operator.eq, "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge, "!=": operator.ne}
DEFAULT_CADENCE = {"pulse_every": 5, "audit_every": 50, "min_periods_between_redesigns": 20, "check_every": 5,
                   "event_min_gap": 3, "early_end_unused_share": 0.5, "repeated_early_ends": 3, "repeated_window": 5,
                   "not_before": 3}
# Files the system or the management roles write. Everything else in the workspace was written by the working agent.
SYSTEM_PATHS = ("swarm/metrics_system.md", "swarm/charts.md", "swarm/handoff.md", "swarm/system_interface.md",
                "swarm/requirements.md", "swarm/spec.md", "swarm/system.json", "swarm/ground_truth/", "swarm/audits/",
                "swarm/checks/", "swarm/guidance/", "swarm/history/")
BEHAVIOR = ("capacity_used_share", "opportunities_open_at_end", "agent_context_k")

def plain(s):
    """Markdown emphasis removed, so marker lines parse however a role formats them."""
    return re.sub(r"[*_`]+", "", s)

def adapter_of(cfg):
    mod, cls = cfg["adapter"].split(":")
    return getattr(importlib.import_module(mod), cls)(**cfg.get("adapter_args", {}))

# ---------- the design (written by the designer) ----------

def resolve(name, names):
    """A name as the designer wrote it, matched to one the adapter reports: exact, or the same ignoring case and any
    bracketed note ("worker time" for "worker time (minutes a day)"). None when there is no single match."""
    if not isinstance(name, str):
        return None
    if name in names:
        return name
    norm = lambda x: re.sub(r"\s*\([^)]*\)", "", x).strip().lower()
    c = [n for n in names if norm(n) == norm(name)]
    return c[0] if len(c) == 1 else None

def load_design(sw, spec):
    """swarm/system.json, checked against what the adapter exposes. Returns (design, problems). Bad entries are dropped,
    never guessed; a missing file falls back to charting every declared measure with no signals or opportunities."""
    problems, d = [], {}
    p = sw / "system.json"
    if p.exists():
        try:
            d = json.loads(p.read_text())
        except Exception as e:
            problems.append(f"swarm/system.json is not valid JSON ({e}); using the defaults")
            d = {}
    else:
        problems.append("swarm/system.json is missing; using the defaults")
    meas = spec.get("measures", {}); res = list(spec.get("resources", []))
    def fix(obj, key, names):  # match a near-miss name to the reported one, and say so
        r = resolve(obj.get(key), names)
        if r and r != obj.get(key):
            problems.append(f"'{obj.get(key)}' read as '{r}'"); obj[key] = r
    for c in d.get("charts") or []:
        if isinstance(c, dict): fix(c, "from" if "from" in c else "name", list(meas))
    for s in d.get("signals") or []:
        if isinstance(s, dict): fix(s, "measure", list(meas))
    for o in d.get("opportunities") or []:
        for c in (o.get("when") or []) if isinstance(o, dict) else []:
            if isinstance(c, dict): fix(c, "resource" if "resource" in c else "measure", res if "resource" in c else list(meas))
    if isinstance(d.get("exemplar"), dict): fix(d["exemplar"], "measure", list(meas))
    out = {"cadence": {**DEFAULT_CADENCE, **{k: v for k, v in (d.get("cadence") or {}).items() if k in DEFAULT_CADENCE and isinstance(v, (int, float))}}}
    ch = []
    for c in d.get("charts") or [{"name": m, "better": v.get("better", "up")} for m, v in meas.items()]:
        if not isinstance(c, dict) or c.get("from", c.get("name")) not in meas:
            problems.append(f"chart {c} names no measure the adapter reports; dropped"); continue
        ch.append({"name": c["name"], "from": c.get("from", c["name"]), "better": c.get("better", meas[c.get("from", c["name"])].get("better", "up")),
                   **({"diff": int(c["diff"])} if c.get("diff") else {})})
    out["charts"] = ch
    sig = []
    for s in d.get("signals") or []:
        if isinstance(s, dict) and s.get("measure") in meas and s.get("op") in OPS and isinstance(s.get("value"), (int, float)):
            sig.append(s)
        else:
            problems.append(f"signal {s} is not {{measure, op, value}} on a reported measure; dropped")
    out["signals"] = sig
    opp = []
    for o in d.get("opportunities") or []:
        conds = o.get("when") if isinstance(o, dict) else None
        ok = isinstance(conds, list) and conds and all(
            (c.get("measure") in meas and c.get("op") in OPS and isinstance(c.get("value"), (int, float))) or
            (c.get("resource") in res and any(isinstance(c.get(k), (int, float)) for k in ("unused_at_least", "unused_share_at_least")))
            for c in conds if isinstance(c, dict)) and all(isinstance(c, dict) for c in conds)
        if ok and o.get("id") and o.get("label"):
            opp.append(o)
        else:
            problems.append(f"opportunity {o} needs id, label and 'when' conditions on reported measures or resources; dropped")
    out["opportunities"] = opp
    ex = d.get("exemplar")
    if ex and isinstance(ex, dict) and ex.get("measure") in meas and isinstance(ex.get("points"), dict) and len(ex["points"]) >= 2:
        out["exemplar"] = ex
    elif ex:
        problems.append("exemplar needs {measure, points: {period: value} (two or more), origin, source}; dropped")
    out["charts_opts"] = {k: d.get("charts_opts", {}).get(k, v) for k, v in {"not_before": 3, "min_points": 8, "baseline_points": 20}.items()}
    return out, problems

def open_opportunities(design, reading, skip_resource=None):
    """Opportunities whose every condition holds in this reading, with the amount open. At the start of a period the
    agent's own capacity is all still ahead, so opportunities on it (skip_resource) are judged only as a period ends."""
    m, r = reading.get("measures", {}), reading.get("resources", {})
    found = []
    for o in design["opportunities"]:
        if skip_resource and any(c.get("resource") == skip_resource for c in o["when"]):
            continue
        amount, ok = None, True
        for c in o["when"]:
            if "measure" in c:
                v = m.get(c["measure"])
                ok = v is not None and OPS[c["op"]](v, c["value"])
                amount = v if amount is None else amount
            else:
                x = r.get(c["resource"]) or {}
                used, avail = x.get("used"), x.get("available")
                if used is None or not avail:
                    ok = False
                else:
                    unused = avail - used
                    ok = unused >= c.get("unused_at_least", float("-inf")) and unused / avail >= c.get("unused_share_at_least", float("-inf")) and unused > 0
                    amount = round(unused, 2) if amount is None else amount
            if not ok:
                break
        if ok:
            found.append({"id": o["id"], "label": o["label"], "amount": amount})
    return found

def write_interface(cfg):
    """What the designer can build on: the adapter's measures, resources and capacity, and the formats it writes."""
    ws = Path(cfg["workspace"]); sw = ws / "swarm"; sw.mkdir(parents=True, exist_ok=True)
    spec = adapter_of(cfg).spec()
    unit = spec.get("unit", "period")
    lines = [f"# System interface (written by the system; do not edit)", "",
             f"The work runs in {unit}s, {spec.get('horizon', '?')} in all. At the end of every {unit} the system reads the task's own state "
             "(ground truth, never an agent's report), charts it, and hands the working agent a short note. You decide, in "
             "swarm/system.json, what it charts, what pulls a review early, what counts as an opportunity, and the exemplar.", "",
             "## Measures the system reads every " + unit, "", "| measure | kind | better |", "| --- | --- | --- |"]
    lines += [f"| {k} | {v.get('kind', '')} | {v.get('better', '')} |" for k, v in spec.get("measures", {}).items()]
    lines += ["", "## Resources (used and available, every " + unit + ")", ""]
    lines += [f"- `{x}`" + ("  (the working agent's own capacity)" if x == spec.get("capacity") else "") + (f": {spec.get('resource_sources', {}).get(x)}" if spec.get('resource_sources', {}).get(x) else "")
              for x in spec.get("resources", [])]
    g = spec.get("goal") or {}
    if g:
        lines += ["", "## Goal as the task states it", "", f"{g.get('type', '')} {spec.get('top', '')}" + (f"; best known: {g['value']} ({g.get('source', '')})" if g.get("value") else "")]
    lines += ["", "## swarm/system.json", "", "```json", json.dumps({
        "charts": [{"name": "<a measure above, or a new name>", "from": "<measure>", "diff": "<optional: change over this many periods>", "better": "up|down"}],
        "signals": [{"measure": "<measure>", "op": "== | < | <= | > | >= | !=", "value": 0, "periods": 2, "not_before": 8, "label": "<why this matters>"}],
        "opportunities": [{"id": "O1", "label": "<what is open, in the task's own words>", "when": [
            {"resource": "<resource>", "unused_at_least": 1}, {"resource": "<resource>", "unused_share_at_least": 0.3},
            {"measure": "<measure>", "op": ">", "value": 0}]}],
        "exemplar": {"measure": "<measure>", "points": {"0": 0, "<period>": 0}, "origin": 0, "source": "<where it comes from>"},
        "cadence": {k: v for k, v in DEFAULT_CADENCE.items()}}, indent=1), "```", "",
        "Use measure and resource names exactly as listed above. Every condition in an opportunity's `when` must hold for it to show as open. Opportunities are information: the system "
        "never ranks, assigns or requires them. Cadence keys you leave out keep the defaults shown.", "",
        "## A guidance entry (swarm/guidance/G-NNN.md; later ones go to swarm/guidance/proposed/)", "", "```markdown",
        "# <short title>", "Applies when: always | <opportunity ids, comma-separated>", "What good looks like: <advice, a guideline or an example>",
        "Why: <the reason and the evidence>", "Source: <brief | review or diagnosis id>", f"Revisit: {unit} <N>", "```", "",
        "A proposal may add `Revises: G-NNN` or `Retires: G-NNN`. Guidance is never an instruction: it never requires, forbids or caps an action."]
    (sw / "system_interface.md").write_text("\n".join(lines) + "\n")

# ---------- the guidance library ----------

FIELDS = ("Applies when", "What good looks like", "Why", "Source", "Revisit", "Revises", "Retires", "Fact check")

def parse_entry(text):
    t = plain(text); e = {"title": ""}
    for line in t.splitlines():
        s = line.strip()
        if s.startswith("#") and not e["title"]:
            e["title"] = s.lstrip("# ").strip()
        for f in FIELDS:
            if s.lower().startswith(f.lower() + ":"):
                e[f] = s.split(":", 1)[1].strip()
    e["applies"] = [x.strip() for x in re.split(r"[,;]", e.get("Applies when", "always")) if x.strip()] or ["always"]
    mm = re.search(r"(\d+)", e.get("Revisit", ""))
    e["revisit"] = int(mm.group(1)) if mm else None
    return e

def library(sw):
    g = sw / "guidance"
    return {f.stem: parse_entry(f.read_text()) for f in sorted(g.glob("G-*.md"))} if g.exists() else {}

def write_library_index(sw, lib, unit):
    rows = [f"# Guidance library (index written by the system; entries are advice, never instructions)", "",
            "| id | title | applies when | source | fact check | revisit |", "| --- | --- | --- | --- | --- | --- |"]
    rows += [f"| {k} | {e['title']} | {', '.join(e['applies'])} | {e.get('Source', '')} | {e.get('Fact check', '')} | {e.get('Revisit', '')} |" for k, e in lib.items()]
    (sw / "guidance" / "index.md").write_text("\n".join(rows) + "\n")

def next_gid(sw):
    n = [int(f.stem[2:]) for f in (sw / "guidance").glob("G-*.md") if f.stem[2:].isdigit()]
    n += [int(f.stem[2:]) for f in (sw / "guidance" / "retired").glob("G-*.md") if f.stem[2:].isdigit()] if (sw / "guidance" / "retired").exists() else []
    return f"G-{(max(n) if n else 0) + 1:03d}"

def admit(sw, prop, verdict, check_id, reason, period, unit):
    """A fact-checked proposal: accepted or untestable enters the library (or revises or retires an entry); refuted is kept with its reason."""
    g = sw / "guidance"; text = prop.read_text(); e = parse_entry(text)
    stamp = f"\nFact check: {check_id} {verdict} at {unit} {period}" + (f" ({reason})" if reason else "") + "\n"
    if verdict == "refuted":
        (g / "refuted").mkdir(exist_ok=True); (g / "refuted" / prop.name).write_text(text + stamp); prop.unlink(); return None
    mm = re.search(r"G-\d+", e.get("Retires") or e.get("Revises") or "")
    target = mm.group(0) if mm and (g / f"{mm.group(0)}.md").exists() else None
    if target:
        (sw / "history").mkdir(exist_ok=True)
        old = g / f"{target}.md"; (sw / "history" / f"{target}.before-{prop.stem}.md").write_text(old.read_text())
        if e.get("Retires"):
            (g / "retired").mkdir(exist_ok=True); old.rename(g / "retired" / old.name); prop.unlink(); return f"retired {target}"
        old.write_text(text + stamp); prop.unlink(); return f"revised {target}"
    gid = next_gid(sw); (g / f"{gid}.md").write_text(text + stamp); prop.unlink(); return f"added {gid}"

# ---------- the working agent's own files ----------

def agent_files(ws):
    out = {}
    for f in ws.rglob("*"):
        if f.is_file():
            rel = str(f.relative_to(ws))
            if not rel.startswith(SYSTEM_PATHS) and not rel.startswith("."):
                st = f.stat(); out[rel] = [st.st_mtime, st.st_size]
    return out

def agent_context_k(hook):
    """The working agent's context at this period end, in thousands of tokens, from its own transcript (cost, R11)."""
    tp = hook.get("transcript_path")
    if not tp or not Path(tp).exists():
        return None
    try:
        with open(tp, "rb") as f:
            f.seek(0, 2); n = f.tell(); f.seek(max(0, n - 400_000)); tail = f.read().decode("utf-8", "ignore").splitlines()
        for line in reversed(tail):
            if '"usage"' in line:
                u = (json.loads(line).get("message") or {}).get("usage") or {}
                t = (u.get("input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0)
                if t:
                    return round(t / 1000, 1)
    except Exception:
        return None
    return None

# ---------- roles ----------

def runner_cmd(cfg, prompt, model, budget, turns):
    tpl = cfg.get("runner")
    if tpl:
        return [str(x).format(prompt=prompt, model=model, budget=budget, turns=turns) for x in tpl]
    return ["claude", "-p", prompt, "--model", model, "--output-format", "json", "--max-turns", str(turns),
            "--tools", "Read,Write,Edit,Glob,Grep,Skill", "--allowedTools", "Read,Write,Edit,Glob,Grep,Skill", "--strict-mcp-config",
            "--permission-mode", "acceptEdits", "--max-budget-usd", str(budget), "--no-session-persistence"]

# ---------- the period end ----------

def pre(cfg):
    """PreToolUse on the period-ending tool: the state as the agent ends its period, before the task advances."""
    sys.stdin.read()
    ws = Path(cfg["workspace"]); log_p = Path(cfg["log"]); mem_p = log_p.with_suffix(".mem.json")
    ad = adapter_of(cfg)
    if hasattr(ad, "on_period_end"):
        ad.on_period_end()
    reading = ad.read()
    if reading is None:
        print("{}"); return
    design, _ = load_design(ws / "swarm", ad.spec())
    mem = json.loads(mem_p.read_text()) if mem_p.exists() else {}
    mem["at_end"] = {"period": reading["period"], "open": open_opportunities(design, reading)}
    mem_p.write_text(json.dumps(mem)); print("{}")

def post(cfg):
    raw = sys.stdin.read()
    try: hook = json.loads(raw) if raw.strip() else {}
    except Exception: hook = {}
    ws = Path(cfg["workspace"]); sw = ws / "swarm"; sw.mkdir(parents=True, exist_ok=True); log_p = Path(cfg["log"])
    ad = adapter_of(cfg); spec = ad.spec(); unit = spec.get("unit", "period"); horizon = spec.get("horizon", "?")
    reading = ad.read()
    if reading is None:
        return
    period, over, measures = reading["period"], reading["over"], dict(reading["measures"])
    mem_p = log_p.with_suffix(".mem.json")
    mem = json.loads(mem_p.read_text()) if mem_p.exists() else {}
    for k, v in {"last_period": -1, "last_audit": 0, "last_pulse": 0, "last_check": 0, "n_audit": 0, "n_pulse": 0, "n_check": 0,
                 "history": [], "pending": [], "early_ends": [], "role_cost": {}, "files": None, "revisited": [], "events": []}.items():
        mem.setdefault(k, v)
    if period <= mem["last_period"]:
        return
    first = mem["last_period"] < 0
    mem["last_period"] = period
    log = log_p.open("a")
    def event(**kw):
        log.write(json.dumps({"t": time.time(), "period": period, **kw}) + "\n")

    design, problems = load_design(sw, spec)
    if first:
        event(event="design_loaded", problems=problems, charts=[c["name"] for c in design["charts"]],
              opportunities=[o["id"] for o in design["opportunities"]], signals=len(design["signals"]))
    cad = design["cadence"]

    # 1. Behavior and cost, as information (R9, R11).
    cap = spec.get("capacity"); r = (reading.get("resources") or {}).get(cap) or {}
    used_share = round(r["used"] / r["available"], 3) if r.get("used") is not None and r.get("available") else None
    at_end = (mem.get("at_end") or {}).get("open", []) if (mem.get("at_end") or {}).get("period") == period - 1 else []
    beh = {"capacity_used_share": used_share, "opportunities_open_at_end": len(at_end), "agent_context_k": agent_context_k(hook)}
    measures.update(beh)
    mem["history"] = (mem["history"] + [measures])[-60:]

    # 2. Ground truth on file: measures every period, and the state snapshots the fact checks use.
    met = sw / "metrics_system.md"
    if first or not mem.get("columns"):
        mem["columns"] = list(measures)
        met.write_text(f"# Ground-truth measures (written by the system every {unit}; do not edit)\n\nThe last three columns describe the "
                       "working agent's behavior and cost. They are information, never targets or limits.\n\n| "
                       f"{unit} | " + " | ".join(mem["columns"]) + " |\n| --- |" + " --- |" * len(mem["columns"]) + "\n")
    with met.open("a") as f:
        f.write(f"| {period} | " + " | ".join(str(measures.get(c)) for c in mem["columns"]) + " |\n")
    if hasattr(ad, "snapshot"):
        gt = sw / "ground_truth"; gt.mkdir(exist_ok=True)
        snap = ad.snapshot(); (gt / "latest.md").write_text(f"# State at {unit} {period} (ground truth)\n\n{snap}")
        (gt / f"{unit}-{period:04d}.md").write_text(snap)
        for old in sorted(gt.glob(f"{unit}-*.md"))[:-30]:
            old.unlink()

    # 3. Charts: the designer's measures, then behavior (shown, never used to trigger a redesign).
    ccfg = {"charts": {**design["charts_opts"], "measures": design["charts"] + [{"name": b, "better": "up"} for b in BEHAVIOR[:1]]},
            "exemplar": design.get("exemplar")}
    md, bad = charts.update(ccfg, mem, period, measures, unit)
    bad = [b for b in bad if not b.startswith(BEHAVIOR)]
    cost = mem["role_cost"]
    md += ("\n## Behavior and cost (information only; never a target or a limit)\n\n"
           f"- Capacity used in the last {unit}: " + (f"{used_share:.0%}" if used_share is not None else "not reported") + "\n"
           f"- Opportunities open when the last {unit} ended: {len(at_end)}" + (" (" + ", ".join(f"{o['id']} {o['label']}" for o in at_end) + ")" if at_end else "") + "\n"
           f"- Working agent's context: " + (f"{beh['agent_context_k']}k tokens" if beh["agent_context_k"] is not None else "not available") + "\n"
           f"- Management roles' cost so far: " + (", ".join(f"{k} ${v:.2f}" for k, v in cost.items()) or "none yet") + "\n")
    (sw / "charts.md").write_text(md)
    event(event="measure", chart_signals=bad, capacity_used_share=used_share, open_at_end=len(at_end), context_k=beh["agent_context_k"])

    # 4. Execution events (R6).
    events = []
    if used_share is not None and period >= cad["not_before"]:
        early = (1 - used_share) >= cad["early_end_unused_share"] and len(at_end) > 0
        mem["early_ends"] = (mem["early_ends"] + [period if early else None])[-int(cad["repeated_window"]):]
        n_early = sum(1 for x in mem["early_ends"] if x is not None)
        if n_early >= cad["repeated_early_ends"]:
            events.append(f"the period ended early in {n_early} of the last {len(mem['early_ends'])} {unit}s with opportunities open")
        elif early:
            events.append(f"{unit} {period - 1} ended with {1 - used_share:.0%} of capacity unused and these open: " + "; ".join(o["label"] for o in at_end))
    fired = None
    for s in design["signals"]:
        if period < s.get("not_before", 0):
            continue
        last = [h.get(s["measure"]) for h in mem["history"][-int(s.get("periods", 1)):]]
        if len(last) == int(s.get("periods", 1)) and all(v is not None and OPS[s["op"]](v, s["value"]) for v in last):
            fired = s.get("label", f"{s['measure']} {s['op']} {s['value']}"); break
    if not fired and bad:
        fired = "chart signal, wrong direction: " + "; ".join(bad)

    budgets = cfg.get("budgets", {}); model = cfg.get("model", "claude-haiku-5-5"); roles = cfg.get("role_models", {})
    jobs = log_p.with_suffix(".jobs"); jobs.mkdir(exist_ok=True)
    new_jobs, notes = [], []

    def spawn(jid, kind, prompt, turns, extra):
        out = jobs / f"{jid}.json"; m = roles.get(kind, model); b = budgets.get(kind, 1.0)
        shell = " ".join(shlex.quote(c) for c in runner_cmd(cfg, prompt, m, b, turns)) + f" > {shlex.quote(str(out) + '.tmp')} 2>/dev/null; mv {shlex.quote(str(out) + '.tmp')} {shlex.quote(str(out))}"
        subprocess.Popen(["sh", "-c", shell], cwd=ws, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        new_jobs.append({"id": jid, "kind": kind, "period": period, "started": time.time(), "out": str(out), **extra})
        event(event="started", id=jid, kind=kind, model=m, trigger=extra.get("trigger"))

    def record(jid, r):
        f = sw / ("checks" if jid.startswith("C-") else "audits") / f"{jid}.md"
        return f.read_text() if f.exists() else (r.get("result") or "")

    def first_part(text, n=700):
        body = "\n".join(l for l in text.splitlines() if not l.startswith("#")).strip()
        return (body[:n] + " ...") if len(body) > n else body

    # 5. Deliver finished jobs.
    still = []
    lib_before = set(library(sw))
    for j in mem["pending"]:
        out = Path(j["out"])
        if not out.exists():
            if time.time() - j["started"] > cfg.get("review_timeout_s", 1200):
                event(event="timeout", id=j["id"], kind=j["kind"])
            else:
                still.append(j)
            continue
        try: r = json.loads(out.read_text())
        except Exception: r = {}
        c = r.get("total_cost_usd") or 0; cost[j["kind"]] = round(cost.get(j["kind"], 0) + c, 4)
        rec = record(j["id"], r)
        event(event=j["kind"], id=j["id"], started=j["period"], delivered=period, trigger=j.get("trigger"), event_period=j.get("event_period"),
              lag=(period - j["event_period"]) if j.get("event_period") is not None else None, cost=c, turns=r.get("num_turns"), record=bool(rec))
        if not rec:
            event(event="no_record", id=j["id"]); continue
        if j["kind"] == "check":
            changes, stated = [], []
            for line in plain(rec).splitlines():
                s = line.strip().lstrip("-• ").strip()
                parts = {p.split(":", 1)[0].strip().lower(): p.split(":", 1)[1].strip() for p in s.split("|") if ":" in p}
                v = (parts.get("verdict") or "").split()[0:1]; v = v[0].lower().strip(".,") if v else ""
                if "proposal" in parts and v in ("accepted", "untestable", "refuted"):
                    prop = (ws / parts["proposal"]) if not Path(parts["proposal"]).is_absolute() else Path(parts["proposal"])
                    if not prop.exists():
                        prop = sw / "guidance" / "proposed" / Path(parts["proposal"]).name
                    if prop.exists() and prop.parent.name == "proposed":
                        did = admit(sw, prop, v, j["id"], parts.get("reason", ""), period, unit)
                        changes.append(did or f"refuted {prop.stem}: {parts.get('reason', '')[:120]}")
                elif "statement" in parts and v in ("supported", "refuted", "untestable"):
                    stated.append((parts["statement"], parts.get("file", ""), v, parts.get("evidence", "")))
            pol = sw / "checks" / "policies.md"
            if not pol.exists():
                pol.write_text("# The working agent's own policies and beliefs, fact-checked against the ground truth (written by the system)\n\n"
                               "They stay the agent's own notes: a check never turns one into a rule.\n\n| checked at | statement | file | verdict | evidence |\n| --- | --- | --- | --- | --- |\n")
            with pol.open("a") as f:
                for st, fl, v, ev in stated:
                    f.write(f"| {unit} {period} | {st} | {fl} | {v} | {ev} |\n")
            if changes:
                notes.append(f"Fact check {j['id']} on proposed guidance: " + "; ".join(changes) + ".")
            for st, fl, v, ev in stated:
                if v != "untestable":
                    notes.append(f"Fact check of your note {st} ({fl}): {v}. {ev}")
                if v == "refuted":
                    events.append(f"a statement in {fl} does not match the ground truth ({st[:80]})")
            continue
        if j["kind"] == "redesign":
            design, problems = load_design(sw, spec)
            event(event="design_loaded", after=j["id"], problems=problems, charts=[c["name"] for c in design["charts"]],
                  opportunities=[o["id"] for o in design["opportunities"]])
            charts.new_phase(mem, j["id"], period); mem["last_adopted"] = period
            notes.append(f"The designer changed the environment after diagnosis {j['after']} (swarm/audits/{j['id']}.md): {first_part(rec, 500)}")
            continue
        if j["kind"] == "diagnosis":
            notes.append(f"Diagnosis {j['id']} (swarm/audits/{j['id']}.md), for your information: {first_part(rec, 500)}")
            rid = "R-" + j["id"][2:]
            spawn(rid, "redesign",
                  f"Use the obm-swarm-designer skill in REDESIGN mode, invoked by the system at {unit} {period} of {horizon}. Diagnosis "
                  f"{j['id']} (swarm/audits/{j['id']}.md) says what is going wrong and why. Read it, swarm/charts.md, swarm/spec.md, "
                  f"swarm/system.json, swarm/system_interface.md and the guidance library (swarm/guidance/index.md). You change the "
                  f"environment, never the agent: what the system charts and counts as an opportunity (swarm/system.json; copy the old "
                  f"version to swarm/history/ first), the spec, or the guidance, which you propose as files in swarm/guidance/proposed/ "
                  f"for the system's fact check. Guidance is advice, guidelines or examples of what good looks like: never write one that "
                  f"requires, forbids or caps an action. Never lower the goal. Make the smallest change that addresses the cause, and "
                  f"state a prediction the charts can test. Write the record to swarm/audits/{rid}.md, starting with a one-paragraph "
                  f"summary and ending with a line 'Environment change: <what changed>'. Reply in under 150 words.",
                  25, {"after": j["id"]})
            continue
        label = "Full audit" if j["kind"] == "audit" else "Pulse review"
        notes.append(f"{label} {j['id']} (as of {unit} {j['period']}; swarm/audits/{j['id']}.md), for your information: {first_part(rec)}")
        mem["revisited"] = sorted(set(mem["revisited"]) | set(j.get("revisit", [])))
        if "diagnosis needed: yes" in plain(rec).lower():
            busy = any(p["kind"] in ("diagnosis", "redesign") and not Path(p["out"]).exists() for p in mem["pending"]) or \
                   any(p["kind"] in ("diagnosis", "redesign") for p in new_jobs)
            since = max(mem.get("last_diagnosis", -10**6), mem.get("last_adopted", -10**6))
            if not busy and period - since >= cad["min_periods_between_redesigns"]:
                mem["last_diagnosis"] = period; did = f"D-{j['id']}"
                spawn(did, "diagnosis",
                      f"Use the obm-swarm-diagnostician skill, invoked by the system because review {j['id']} (swarm/audits/{j['id']}.md) "
                      f"says a diagnosis is needed, at {unit} {period} of {horizon}. Charts: swarm/charts.md (limits computed by the system, "
                      f"and the agent's behavior and cost); measures for every {unit}: swarm/metrics_system.md; recent state: swarm/ground_truth/; "
                      f"the design: swarm/spec.md and swarm/system.json; the guidance library: swarm/guidance/. Walk the tree from the top "
                      f"measure down to what moved, then find why, looking first in what the environment gives the agent. Do not change "
                      f"anything: the designer redesigns from your diagnosis. Write swarm/audits/{did}.md, starting with a one-paragraph "
                      f"summary, and reply with it in under 200 words.", 20, {"after": j["id"]})
            else:
                event(event="diagnosis_deferred", after=j["id"])
    mem["pending"] = still + new_jobs; new_jobs = []
    lib = library(sw)
    if lib or (sw / "guidance").exists():
        (sw / "guidance").mkdir(exist_ok=True); write_library_index(sw, lib, unit)
    added = [k for k in lib if k not in lib_before]

    # 6. Start a review if one is due (one pulse or audit at a time).
    if events:
        mem["events"] = (mem["events"] + [{"period": period, "what": e} for e in events])[-50:]
        event(event="execution_event", what=events)
    reviewing = any(p["kind"] in ("pulse", "audit") for p in mem["pending"])
    last_rev = max(mem["last_audit"], mem["last_pulse"])
    due_rev = [k for k, e in lib.items() if e["revisit"] is not None and e["revisit"] <= period and f"{k}@{e['revisit']}" not in mem["revisited"]]
    kind = None
    if period - mem["last_audit"] >= cad["audit_every"] or (fired and period - last_rev >= cad["event_min_gap"]):
        kind, why = "audit", (f"because a signal fired: {fired}" if fired else "on its schedule")
    elif events and period - last_rev >= cad["event_min_gap"]:
        kind, why = "pulse", "because of what the agent did: " + "; ".join(events)
    elif period - last_rev >= cad["pulse_every"]:
        kind, why = "pulse", "on its schedule"
    if kind and not over and not reviewing and period >= cad["not_before"]:
        (sw / "audits").mkdir(exist_ok=True)
        if kind == "audit":
            mem["n_audit"] += 1; mem["last_audit"] = period; aid = f"A-{mem['n_audit']:03d}"
        else:
            mem["n_pulse"] += 1; mem["last_pulse"] = period; aid = f"P-{mem['n_pulse']:03d}"
        common = (f"at {unit} {period} of {horizon}. You cannot act on the work. Read swarm/handoff.md (what the agent was last "
                  f"given), swarm/charts.md (limits computed by the system, the agent's behavior and cost), swarm/spec.md, the guidance "
                  f"library (swarm/guidance/index.md), swarm/checks/policies.md and the agent's own recent notes. Measures and state "
                  f"come from the system (swarm/metrics_system.md, swarm/ground_truth/), never from an agent. You change the environment, "
                  f"never the agent: you never tell the agent what to do. If guidance would help, propose it as files in "
                  f"swarm/guidance/proposed/ (format in swarm/system_interface.md): advice, guidelines or examples of what good looks "
                  f"like, never a requirement, prohibition or cap; the system fact-checks each before it enters the library. Give "
                  f"about one keep-doing for every four problems. "
                  + (f"Guidance due for revisit: {', '.join(due_rev)}; propose a revision or retirement if the evidence says so. " if due_rev else ""))
        tail = ("Start the record with a one-paragraph summary of what you found. End it with a line 'Environment change: <the "
                "proposals you wrote, or none>' and then a last line exactly 'Diagnosis needed: yes' or 'Diagnosis needed: no'.")
        if kind == "audit":
            prompt = (f"Use the obm-swarm-auditor skill for a FULL AUDIT, invoked by the system ({why}). This is audit {aid}, {common}Judge "
                      f"the outcome first: are the goal's main measures moving toward it, is capacity in use, is anything declining? Is the "
                      f"direction right, and did each redesign's prediction appear on the charts? Does the guidance still fit the evidence? "
                      f"Write swarm/audits/{aid}.md. {tail}")
            spawn(aid, "audit", prompt, 30, {"trigger": fired or "scheduled", "event_period": period if fired else None, "revisit": [f"{k}@{lib[k]['revisit']}" for k in due_rev]})
        else:
            prompt = (f"Use the obm-swarm-auditor skill for a PULSE REVIEW, invoked by the system {why}. This is pulse {aid}, {common}"
                      f"Answer: which measures show a signal and which only routine variation; what the agent did with its capacity and "
                      f"the opportunities open, and why that might be (look at what the environment gave it); what is heading the wrong "
                      f"way. Write swarm/audits/{aid}.md in under 300 words. A pulse asks for a diagnosis when a chart signals a change "
                      f"in the wrong direction, when a redesign's prediction has not appeared by its date, or when the gap to the exemplar "
                      f"is large and nothing has improved for 30 {unit}s. {tail}")
            spawn(aid, "pulse", prompt, 14, {"trigger": "event" if events else "scheduled", "event_period": period if events else None, "revisit": [f"{k}@{lib[k]['revisit']}" for k in due_rev]})
        mem["pending"] += new_jobs; new_jobs = []

    # 7. Fact checks: proposed guidance, and the agent's own written policies and beliefs (R4, R5).
    props = sorted(str(p.relative_to(ws)) for p in (sw / "guidance" / "proposed").glob("*.md")) if (sw / "guidance" / "proposed").exists() else []
    now_files = agent_files(ws); prev = mem["files"] or {}
    changed = sorted(k for k, v in now_files.items() if prev.get(k) != v)
    checking = any(p["kind"] == "check" for p in mem["pending"])
    if not over and not checking and (props or (changed and period - mem["last_check"] >= cad["check_every"] and mem["files"] is not None)):
        mem["n_check"] += 1; mem["last_check"] = period; cid = f"C-{mem['n_check']:03d}"; (sw / "checks").mkdir(exist_ok=True)
        spawn(cid, "check",
              f"Use the obm-swarm-checker skill in FACT CHECK mode, invoked by the system at {unit} {period} of {horizon}. This is "
              f"check {cid}. Ground truth: swarm/metrics_system.md (every {unit}'s measures) and swarm/ground_truth/ (state snapshots "
              f"for recent {unit}s). Never use an agent's report as evidence.\n"
              + (f"Proposed guidance to check: {', '.join(props)}. For each, check every factual claim in it against the ground truth, "
                 f"and check that it is advice: one that requires, forbids or caps an action is refuted with reason 'not advice'. "
                 f"Verdict: accepted (its facts hold), untestable (advice with no factual claim to check), or refuted (say which claim "
                 f"is false).\n" if props else "")
              + (f"Files the working agent changed since the last check: {', '.join(changed[:20])}. Find each policy it set itself or "
                 f"belief it states about the task or its results (not plans or to-do items) and check its factual basis. Verdict: "
                 f"supported, refuted or untestable. Quote at most 8 statements, the ones that most shape what it does.\n" if changed and mem["files"] is not None else "")
              + f"Write swarm/checks/{cid}.md with one line per item, exactly in these forms:\n"
                f"Proposal: <path> | Verdict: <accepted|untestable|refuted> | Reason: <one line>\n"
                f"Statement: \"<quote>\" | File: <path> | Verdict: <supported|refuted|untestable> | Evidence: <the numbers, with {unit}s>\n"
                f"Keep it under 400 words. Reply 'done'.", 16, {})
        mem["pending"] += new_jobs; new_jobs = []
    mem["files"] = now_files

    # 8. The hand-off (R2, R3, R8): one compact note of information and advice, every period.
    open_now = open_opportunities(design, reading, skip_resource=cap)
    fit = [k for k, e in lib.items() if any(a in {o["id"] for o in open_now + at_end} for a in e["applies"])]
    always = [k for k, e in lib.items() if "always" in [a.lower() for a in e["applies"]]]
    shown = set(mem.get("shown_guidance", []))
    lines = [f"SYSTEM ({unit} {period} of {horizon}): information and advice for you to use as you see fit. You decide what to do."]
    if used_share is not None:
        lines.append(f"Last {unit}: you used {used_share:.0%} of your capacity ({cap})." + (
            " Open when it ended: " + "; ".join(f"{o['id']} {o['label']}" + (f" ({o['amount']})" if o["amount"] is not None else "") for o in at_end) + "." if at_end else ""))
    if open_now:
        lines.append("Open now: " + "; ".join(f"{o['id']} {o['label']}" + (f" ({o['amount']})" if o["amount"] is not None else "") for o in open_now) + ".")
    fit = sorted(fit, key=lambda k: (k not in added, k not in shown, k))  # new and unseen first; at most five per note
    more = len(fit) - 5; fit = fit[:5]
    for k in fit + [k for k in always if (k not in shown or k in added) and k not in fit]:
        e = lib[k]; first_time = k not in shown or k in added
        lines.append(f"Guidance {k}, {e['title']}" + (f": {e.get('What good looks like', '')}" if first_time else " (swarm/guidance/" + k + ".md)"))
        shown.add(k)
    if more > 0:
        lines.append(f"{more} more guidance entries fit what is open (swarm/guidance/index.md).")
    mem["shown_guidance"] = sorted(shown)
    if bad:
        lines.append("Charts: " + "; ".join(bad) + " (swarm/charts.md).")
    lines += notes
    if first:
        lines.append(f"The designer's work system is in swarm/spec.md and the guidance library in swarm/guidance/. Each {unit} this note "
                     "is also kept in swarm/handoff.md.")
    text = "\n".join(lines)
    (sw / "handoff.md").write_text(f"# Hand-off at {unit} {period} (written by the system every {unit})\n\n" + text.replace("\n", "\n\n") + "\n")
    mem_p.write_text(json.dumps(mem)); log.close()
    if not over:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": cfg.get("hook_event", "PostToolUse"), "additionalContext": text}}))

def main():
    cfg = json.loads(Path(sys.argv[1]).read_text())
    if "--interface" in sys.argv:
        write_interface(cfg)
    elif "--pre" in sys.argv:
        pre(cfg)
    else:
        post(cfg)

if __name__ == "__main__":
    main()
