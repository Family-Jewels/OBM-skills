"""OBM cadence engine, version 4: risk management and improvement as two separate branches. Task-agnostic.

Called by engine.py when the config has "version": 4. What changes from v3 (see the v4 design doc):
- Two branches, each with its own triggers, queue, change lane and budget, so neither can starve the other.
  Risk branch (keep the floor): risk monitor (auditor, RISK PULSE), checker (claim samples), diagnostician, controls owner.
    It changes swarm/controls.md only. Triggers: risk events, on a change of state (a guardrail newly crossed, a chart
    signal newly in the wrong direction, a measure gone missing, a misreport, the work newly off its planned capacity
    split), plus a routine sweep every `risk_sweep_every` points.
  Improvement branch (raise the ceiling): Strategist, designer (AIM UPDATE right after each strategy; METHOD CHANGE from
    batched requests). It changes swarm/aims.md, swarm/spec.md and method rules. Triggers: every `strategy_every` points,
    and early when the top measure newly falls below its floor or its celeration newly turns flat or wrong.
  The full audit (third line) is independent of both. The worker reads one assembled file, swarm/instructions.md:
  controls first (bounds), then aims and methods (what to push within them).
- Mechanics are code: a request ledger with merging of repeats, required dispositions, and escalation to the human
  (ledger.py); a fact register and a pursuit measure from the harness's own log of actions (facts.py); triggers on
  changes of state; every change job takes all open requests for its branch in one batch.
- A task profile sets the configuration, with bounds (profile.py). The Organizer reviews the system's health at each
  quarter and may change one setting within its bounds; every change is logged and escalated.
"""
import hashlib, importlib, json, re, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import charts, progress, facts, profile
from ledger import Ledger, parse_requests
from engine_v2 import load_spec, preflight
try:  # change verification by the system (lab/longrun/verify.py); the engine runs without it
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "longrun"))
    import verify
    if not all(hasattr(verify, f) for f in ("register", "update", "markdown", "parse")):
        verify = None  # some other module by that name
except Exception:
    verify = None

ROLE_OF = {"pulse": "risk monitor", "check": "checker", "diagnosis": "diagnostician", "controls": "controls owner",
           "strategist": "Strategist", "aims": "designer (aim update)", "method": "designer (method change)",
           "audit": "auditor (full audit)", "organizer": "Organizer"}
BRANCH = {"pulse": "risk", "check": "risk", "diagnosis": "risk", "controls": "risk", "strategist": "improvement",
          "aims": "improvement", "method": "improvement", "audit": "audit", "organizer": "organization"}

def fhash(paths):
    h = hashlib.sha256()
    for f in paths:
        for g in ([f] if f.is_file() else sorted(f.glob("*")) if f.is_dir() else []):
            if g.is_file():
                h.update(g.name.encode()); h.update(g.read_bytes())
    return h.hexdigest()[:16]

REQ_HOWTO = ("If you need something from another role, end your record with a '## Requests' section, one line each: "
             "'- to: <controls|designer|strategist|human> | key: <short-slug> | <the ask>'. First check the Requests table in "
             "swarm/charts.md: if your ask is already open, reuse its key (the system merges repeats and escalates those asked 3 "
             "times). Never ask for a fact the Facts table already measures. A fact you can support from ground truth but the "
             "system cannot measure goes in a '## Facts' section: '- <fact> | source: <where in the ground truth>'.")

def main(cfg, cfg_path=None):
    ws = Path(cfg["workspace"]); log_p = Path(cfg["log"])
    mod, cls = cfg["adapter"].split(":")
    adapter = getattr(importlib.import_module(mod), cls)(**cfg.get("adapter_args", {}))
    reading = adapter.read()
    if reading is None:
        return
    spec = load_spec(cfg, adapter); unit = spec["unit"]; horizon = spec["horizon"]
    period, over, measures = reading["period"], reading["over"], reading["measures"]
    t = reading.get("clock", period)
    resources = reading.get("resources") or {}
    mem_p = log_p.with_suffix(".mem.json")
    mem = json.loads(mem_p.read_text()) if mem_p.exists() else {"last_period": -1, "history": [], "pending": [], "n": {}}
    if period <= mem["last_period"]:
        return
    first = mem["last_period"] < 0
    mem["last_period"] = period
    mem["history"] = (mem["history"] + [measures])[-50:]
    sw = ws / "swarm"; sw.mkdir(parents=True, exist_ok=True); (sw / "audits").mkdir(exist_ok=True)
    log = log_p.open("a")
    def ev(_event, **kw):
        log.write(json.dumps({"t": time.time(), "period": period, "event": _event, **kw}) + "\n")
    handoff = []
    escal = []
    win = mem.setdefault("window", progress.derive_window(horizon, spec.get("cycle", 1), spec.get("clock", "period")))
    W = win["w"]
    if first:
        probs = preflight(spec, reading)
        if not spec.get("profile"):
            probs.append("no task profile (work_shape, feedback_lag, reversible): defaults used (operation, lag of one point, irreversible)")
        prof, conf, bounds = profile.derive(spec, W)
        mem.update({"profile": prof, "config": conf, "bounds": bounds})
        ev("preflight", problems=probs, window=win, profile=prof, config=conf)
        if probs:
            handoff.append("adapter preflight found: " + "; ".join(probs) + ". The system measures what it can.")
            escal.append(("preflight", "; ".join(probs)))
    C = mem["config"]
    met = sw / "metrics_system.md"
    if not met.exists():
        met.write_text(f"# Ground-truth measures (written by the system every {unit}; do not edit)\n\n| {unit} | " + " | ".join(measures)
                       + " |\n| --- |" + " --- |" * len(measures) + "\n")
    with met.open("a") as f:
        f.write(f"| {period} | " + " | ".join(str(v) for v in measures.values()) + " |\n")
    cfg.setdefault("charts", {})["own_best_window"] = W
    cmd_md, chart_bad = charts.update(cfg, mem, period, measures, unit)
    prog_md, events = progress.update(mem, spec, t, measures, resources)
    new_point = any(e["kind"] == "new_point" for e in events)
    newest = mem["progress"]["last_point"]
    point = (newest or 0) + 1  # 1-based label of the latest completed point

    # Facts and pursuit, from the harness's log of every action.
    actions = facts.load_actions(cfg.get("action_log"))
    cs = facts.costs(actions, (spec.get("action_clock") or {}).get("start"))
    reg = facts.register(cs, period, W)
    aims_text = (sw / "aims.md").read_text() if (sw / "aims.md").exists() else ""
    split = facts.parse_split(aims_text)
    prow = facts.pursuit(split, cs, period, W)

    # Risk events, on a change of state only.
    risk_now = []
    gr = sorted(e["label"] for e in events if e["kind"] == "guardrail")
    for g in gr:
        if g not in mem.get("gr_prev", []):
            risk_now.append(("guardrail", g))
    mem["gr_prev"] = gr
    bad = sorted(set(chart_bad or []))
    for b in bad:
        if b not in mem.get("bad_prev", []):
            risk_now.append(("chart signal", b))
    mem["bad_prev"] = bad
    had = mem.setdefault("seen_measures", [])
    missing = sorted(k for k in had if measures.get(k) is None)
    for k in missing:
        if k not in mem.get("missing_prev", []):
            risk_now.append(("measure missing", k))
    mem["missing_prev"] = missing
    mem["seen_measures"] = sorted(set(had) | {k for k, v in measures.items() if v is not None})
    if new_point and split:
        off = facts.off_plan(prow)
        for o in off:
            if o not in mem.get("off_prev", []):
                risk_now.append(("off plan", f"capacity on '{o}' missed its planned share by more than 25 points over the last point"))
        mem["off_prev"] = off
    if gr:
        new_gr = [g for k, g in risk_now if k == "guardrail"]
        if new_gr:
            handoff.append("; ".join(new_gr) + ". Restore the guardrail before anything else; the risk monitor has been called.")
    for e in events:
        if e["kind"] == "aim_raised":
            handoff.append(f"the aim for {spec['top']} was met on 2 of the last 3 points, so it has been raised: {e['label']}.")
            ev("aim_raised", label=e["label"])
    mem.setdefault("risk_events", []).extend([{"kind": k, "label": l, "period": period} for k, l in risk_now])
    for k, l in risk_now:
        ev("risk_event", kind=k, label=l)

    # Improvement triggers, on a change of state only.
    imp_kinds = sorted({e["kind"] for e in events if e["kind"] in ("below_floor", "flat_or_wrong")})
    imp_new = []
    if new_point:
        imp_new = [e["label"] for e in events if e["kind"] in imp_kinds and e["kind"] not in mem.get("imp_prev", [])]
        mem["imp_prev"] = imp_kinds

    L = Ledger(mem)
    charted = [m["name"] for m in cfg.get("charts", {}).get("measures", [])]
    series_of = lambda name: mem.get("charts", {}).get("series", {}).get(name, [])
    def sys_request(key, text):
        for req, how in L.file("system", [{"to": "designer", "key": key, "text": text[:400]}], point, period):
            ev("request_" + how, id=req["id"], to=req["to"], key=req["key"], asked=req["asked"])
    budgets = cfg.get("budgets", {}); model = cfg.get("model", "claude-haiku-5-5")
    jobs = log_p.with_suffix(".jobs"); jobs.mkdir(exist_ok=True)
    where = f"{unit} {period} of {horizon}"
    cap = spec.get("capacity") or "capacity"
    charts_note = ("swarm/charts.md (written by the system: level charts, celeration, the top measure's floor and aim lines, resources, "
                   "guardrails, the Facts measured from every action, planned vs actual capacity split, and the Requests ledger)")

    def busy(*kinds):
        return any(j["kind"] in kinds for j in mem["pending"])

    def nid(prefix):
        mem["n"][prefix] = mem["n"].get(prefix, 0) + 1
        return f"{prefix}-{mem['n'][prefix]:03d}"

    def spawn(jid, kind, prompt, budget, turns, extra=None):
        extra = extra or {}
        out = jobs / f"{jid}.json"
        cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json", "--max-turns", str(turns),
               "--tools", "Read,Write,Edit,Glob,Grep,Skill", "--allowedTools", "Read,Write,Edit,Glob,Grep,Skill", "--strict-mcp-config",
               "--permission-mode", "acceptEdits", "--max-budget-usd", str(budget), "--no-session-persistence"]
        shell = " ".join("'" + c.replace("'", "'\\''") + "'" for c in cmd) + f" > '{out}.tmp' 2>/dev/null; mv '{out}.tmp' '{out}'"
        if cfg.get("dry_run"):
            dry(jid, kind, extra)
            out.write_text(json.dumps({"result": f"dry run {jid}", "total_cost_usd": 0}))
        else:
            subprocess.Popen(["sh", "-c", shell], cwd=ws, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        mem["pending"].append({"id": jid, "kind": kind, "period": period, "point": point, "started": time.time(), "out": str(out), **extra})
        ev("started", id=jid, kind=kind, branch=BRANCH[kind], trigger=extra.get("trigger"))

    def dry(jid, kind, extra):
        """Tests and replay: write the record a role would write, from cfg['dry'] templates (no model call)."""
        d = cfg.get("dry", {})
        rec = d.get(kind, "")
        if isinstance(rec, list):  # one record per job of this kind, in order (the last repeats)
            i = mem.setdefault("dry_i", {}).get(kind, 0); mem["dry_i"][kind] = i + 1
            rec = rec[min(i, len(rec) - 1)]
        if kind == "aims":
            (sw / "aims.md").write_text(d.get("aims_md", f"# Aims ({jid})\n\n## Capacity split\n- 100% all: x\n"))
        if kind == "controls":
            with (sw / "controls.md").open("a") as fh: fh.write(f"\n- control from {jid}\n")
        if kind == "method":
            with (sw / "spec.md").open("a") as fh: fh.write(f"\nmethod change {jid}\n")
        if kind == "organizer":
            rec = d.get("organizer", "Config change: none")
        if extra.get("reqs"):
            disp = d.get("disposition", "done")
            rec += "\n\n## Dispositions\n" + "\n".join(f"- {r}: {disp} | dry run" for r in extra["reqs"])
        (sw / "audits" / f"{jid}.md").write_text(rec.replace("{id}", jid))

    common = (f"at {where} of the work the swarm in swarm/ is doing. The ground-truth measures (swarm/metrics_system.md) and "
              f"{charts_note} are written by the system, never by an agent; an agent's own log is never a measure.")
    disp_howto = ("Answer every request handed to you in a '## Dispositions' section, one line each: '- REQ-NNN: done | <what you "
                  "changed>' or '- REQ-NNN: declined | <why, e.g. the Facts table shows it is fixed by the environment>' or "
                  "'- REQ-NNN: deferred | <what you are waiting for>'. A request you do not answer goes back to open.")

    def pulse_prompt(pid, trig):
        return (f"Use the obm-swarm-auditor skill for a RISK PULSE ({pid}), invoked by the system ({trig}), {common} Your question is "
                f"only: is anything broken, false, or about to cross a line? Not whether the work could be better: the improvement branch "
                f"owns that. Read swarm/charts.md, swarm/instructions.md and the last lines of the worker's log. A fault is: a guardrail at "
                f"risk or crossed; a level chart signal in the wrong direction; a measure missing; the worker's log claiming what the "
                f"ground truth does not show; the worker not following swarm/instructions.md (the Pursuit table shows the capacity split). "
                f"A point below the floor or a flat celeration is NOT a fault. Write swarm/audits/{pid}.md in under 200 words: what you "
                f"checked and found; if the worker's own work needs correcting now (an error, not a new rule), a '## Corrections' section "
                f"with at most four items plus one keep-doing item (what is safe and working); then the line 'Fault: yes' or 'Fault: no', "
                f"and with yes a line 'Fault key: <short-slug>' (reuse the key of an earlier fault if it is the same problem). {REQ_HOWTO}")

    def diag_prompt(did, fq):
        lst = ", ".join(f"{f['key']} (from {f['from']}, swarm/audits/{f['from']}.md)" for f in fq)
        return (f"Use the obm-swarm-diagnostician skill ({did}), invoked by the system because the risk branch found these faults: {lst}. "
                f"{common} For each, find what moved and what maintains it, cause in the environment first (information, resources, "
                f"incentives, the facts in the Facts table), then the worker. Do not write a fix or change anything: the controls owner "
                f"acts on your diagnosis. Write swarm/audits/{did}.md in under 250 words. {REQ_HOWTO}")

    def controls_prompt(cid, reqs):
        return (f"Use the obm-swarm-controls skill ({cid}), invoked by the system {common} These requests are yours, all at once:\n{reqs}\n"
                f"Change swarm/controls.md, the risk branch's only output: limits, checks and things the worker must not do. Make the "
                f"fewest, smallest controls that close the faults. Every control names the risk it guards and a review point "
                f"('Review at point N'), and never stops the core work or sets aims. Copy the old controls.md to swarm/history/ first. "
                f"Write swarm/audits/{cid}.md: what you changed and why. {disp_howto} {REQ_HOWTO}")

    def check_prompt(kid):
        return (f"Use the obm-swarm-checker skill for a CLAIM SAMPLE ({kid}), invoked by the system {common} Pick three concrete "
                f"claims from the last point of the worker's log (an amount, a count, an action done) and verify each against ground "
                f"truth: swarm/metrics_system.md, the Facts table and any system snapshot. Write swarm/audits/{kid}.md: each claim, the "
                f"evidence, verified or not; then the line 'Misreport: yes' or 'Misreport: no'. {REQ_HOWTO}")

    def strat_prompt(sid, why, reqs):
        return (f"Use the obm-swarm-strategist skill ({sid}), invoked by the system ({why}), {common} Read swarm/aims.md, the driver "
                f"tree in swarm/spec.md and your earlier records swarm/audits/S-*.md. The Pursuit table shows whether the last aims were "
                f"pursued: use it, do not re-judge it. Find the constraint now, starting with the worker's own {cap}, using the Facts "
                f"table for what each action costs. Set a stretch aim for each priority driver (at most three) for the next point and the "
                f"capacity split. The human's goal is fixed. Write swarm/audits/{sid}.md in under 250 words; the designer turns it into "
                f"aims at once. A change to how the work is done goes in your Requests to the designer, once, with a key."
                + (f"\nRequests addressed to you:\n{reqs}\n{disp_howto}" if reqs else "") + f" {REQ_HOWTO}")

    def aims_prompt(sid):
        return (f"Use the obm-swarm-designer skill in AIM UPDATE mode (A{sid}), invoked by the system right after the Strategist's "
                f"redirect {sid} (swarm/audits/{sid}.md), {common} Rewrite swarm/aims.md now, short enough for the worker to read every "
                f"{unit}: the constraint, the aim for each priority driver for the next point, and a section exactly '## Capacity split' "
                f"with one line per share: '- <percent>% <label>: <action names>' using the action names in the Facts table (the system "
                f"measures the actual split from them). Copy the old aims.md to swarm/history/ first. Do not change swarm/spec.md, the "
                f"rules or swarm/controls.md. If the redirect needs a change to how the work is done, put it in your Requests to the "
                f"designer. Write swarm/audits/A{sid}.md briefly. {REQ_HOWTO}")

    def method_prompt(mid, reqs):
        return (f"Use the obm-swarm-designer skill in METHOD CHANGE mode ({mid}), invoked by the system {common} These requests are "
                f"yours, all at once:\n{reqs}\nMake the smallest change to how the work is done (swarm/spec.md, swarm/rules/) that answers "
                f"them; a new measure the system cannot take goes in your Requests to the human. Do not touch swarm/controls.md (the risk "
                f"branch's) or lower the goal. End the record with one line exactly 'Prediction: <measure> <up|down> within <N> points', "
                f"naming one measure the system charts ({', '.join(charted) or 'see swarm/charts.md'}): the system judges it from the "
                f"charts by the protocol's signal rule, counted from the {unit} your change is adopted, and hands a miss back to you. "
                f"Copy changed files to swarm/history/ first. Write swarm/audits/{mid}.md. {disp_howto} {REQ_HOWTO}")

    def audit_prompt(aid, q, n):
        return (f"Use the obm-swarm-auditor skill for a FULL AUDIT, invoked by the system at {q} of {n} of the horizon, {common} You are "
                f"the third line, independent of both branches. Judge: the outcome against the floor and aim lines; whether the risk "
                f"branch's controls are earning their cost or over-controlling; whether the improvement branch's changes did what they "
                f"predicted; whether requests are being answered (the Requests table); honesty of the records; cost. Write "
                f"swarm/audits/{aid}.md with findings first, at most five items, about one keep-doing to "
                f"four fixes, then 'Fault: yes' or 'Fault: no' (with 'Fault key:'). {REQ_HOWTO}")

    def organizer_prompt(oid):
        return (f"Use the obm-swarm-organizer skill, invoked by the system {common} Read the System health section of swarm/charts.md, the "
                f"Requests table and swarm/escalations.md. Judge whether the management system itself is working: requests answered "
                f"quickly, aims reaching the worker fast, roles doing useful work, cost in proportion. You may propose at most one "
                f"change to one setting, within its bounds, as a line exactly 'Config change: <setting> = <value>' with the reason, or "
                f"'Config change: none'. You never touch the goal, guardrails, measures, controls or aims. Write swarm/audits/{oid}.md in under 200 words.")

    # 1. Deliver anything finished.
    still = []
    for j in mem["pending"]:
        out = Path(j["out"])
        if not out.exists():
            if time.time() - j["started"] > cfg.get("review_timeout_s", 1500):
                ev("review_timeout", id=j["id"], kind=j["kind"])
                if j.get("reqs"):
                    L.answer(j["id"], "", point)
            else:
                still.append(j)
            continue
        try: r = json.loads(out.read_text())
        except Exception: r = {}
        mem.setdefault("cost", {}).setdefault(j["kind"], 0.0)
        mem["cost"][j["kind"]] += r.get("total_cost_usd") or 0
        ev(j["kind"], id=j["id"], branch=BRANCH[j["kind"]], started_period=j["period"], cost=r.get("total_cost_usd"), turns=r.get("num_turns"))
        rec_f = sw / "audits" / f"{j['id']}.md"
        rec = rec_f.read_text() if rec_f.exists() else (r.get("result") or "")
        for req, how in L.file(j["id"], parse_requests(rec), point, period):
            ev("request_" + how, id=req["id"], to=req["to"], key=req["key"], asked=req["asked"])
        for fct in facts.parse_proposed(rec):
            mem.setdefault("proposed_facts", []).append({**fct, "from": j["id"]})
        if j.get("reqs"):
            answered = L.answer(j["id"], rec, point)
            for rid, st in answered:
                ev("request_" + st, id=rid, by=j["id"])
            if verify is not None and j["kind"] == "method":  # a restated prediction for an earlier change
                for r in L.reqs:
                    if r["id"] in {a for a, s in answered if s == "done"} and r["key"].startswith("prediction-"):
                        old = next((p for p in mem.get("predictions", []) if p.get("problem") and p["id"].lower() == r["key"][11:]), None)
                        pr, prob = verify.parse(rec, charted)
                        if old and pr:
                            old.pop("problem"); old.update(pr); old["detectable"] = verify.detectable(series_of(pr["measure"]), old["adopted"])
                            ev("prediction_restated", id=old["id"], by=j["id"])
        k = j["kind"]
        if k == "pulse" or k == "audit" or k == "check":
            fault = re.search(r"^\s*Fault\s*:\s*yes\b(.*)$", rec, re.M | re.I)
            mis = re.search(r"^\s*Misreport\s*:\s*yes\b", rec, re.M | re.I)
            if fault or mis:
                key = re.search(r"^\s*Fault key\s*:\s*([\w-]+)", rec, re.M | re.I)
                key = (key.group(1).lower() if key else ("misreport" if mis and not fault else f"fault-{j['id'].lower()}"))
                fq = mem.setdefault("fault_queue", [])
                fq[:] = [f for f in fq if f["key"] != key] + [{"key": key, "from": j["id"]}]  # the latest evidence replaces older
                ev("fault", key=key, by=j["id"])
            corr = re.search(r"^#+\s*Corrections.*?$(.*?)(?=^#+\s|\Z)", rec, re.M | re.S | re.I)
            if corr and corr.group(1).strip():
                handoff.append(f"{ROLE_OF[k]} {j['id']} (swarm/audits/{j['id']}.md) found faults in the work itself. Correct them this {unit} "
                               f"and log what you did:\n{corr.group(1).strip()[:1500]}")
            if k == "audit":
                handoff.append(f"full audit {j['id']} is in swarm/audits/{j['id']}.md.")
        elif k == "diagnosis":
            L.file(j["id"], [{"to": "controls", "key": j.get("fault_key", "fault"), "text": f"Act on diagnosis {j['id']} (swarm/audits/{j['id']}.md)."}],
                   point, period)
        elif k == "controls":
            h = fhash([sw / "controls.md"])
            if h != mem.get("controls_hash"):
                mem["controls_hash"] = h; mem["last_control_point"] = newest
                mem.setdefault("changes", []).append({"branch": "risk", "id": j["id"], "period": period})
                ev("adopted", id=j["id"], branch="risk")
        elif k == "strategist":
            mem["strategy_delivered"] = period
            aid = "A" + j["id"]
            spawn(aid, "aims", aims_prompt(j["id"]), budgets.get("aims", 0.8), 15, {"after": j["id"]})
        elif k == "aims":
            if mem.get("strategy_delivered") is not None:
                mem.setdefault("aim_latency", []).append(period - mem["strategy_delivered"])
            handoff.append(f"new aims from the designer (after {j.get('after')}): work to them from now. They are in swarm/instructions.md.")
        elif k == "method":
            h = fhash([sw / "spec.md", sw / "rules"])
            if h != mem.get("design_hash"):
                charts.new_phase(mem, j["id"], period); progress.new_phase(mem)
                mem["design_hash"] = h; mem["last_method_point"] = newest
                mem.setdefault("changes", []).append({"branch": "improvement", "id": j["id"], "period": period})
                ev("adopted", id=j["id"], branch="improvement")
                handoff.append(f"the designer changed how the work is done ({j['id']}, swarm/audits/{j['id']}.md). Re-read swarm/spec.md and swarm/rules/.")
                if verify is not None:
                    prob = verify.register(mem, j["id"], rec, charted, period, series_of)
                    ev("prediction_problem" if prob else "prediction_registered", id=j["id"], problem=prob)
                    if prob:
                        sys_request(f"prediction-{j['id'].lower()}", f"{j['id']} was adopted, but the system cannot judge it: {prob}")
        elif k == "organizer":
            m = re.search(r"^\s*Config change\s*:\s*([\w_]+)\s*=\s*(\S+)", rec, re.M | re.I)
            if m:
                ok, v = profile.validate(m.group(1), m.group(2), C, mem["bounds"])
                if ok:
                    old = C[m.group(1)]; C[m.group(1)] = v
                    mem.setdefault("changes", []).append({"branch": "organization", "id": j["id"], "period": period})
                    ev("config_change", key=m.group(1), old=old, new=v, by=j["id"])
                    escal.append(("config change", f"{j['id']} set {m.group(1)} from {old} to {v} (swarm/audits/{j['id']}.md)"))
                else:
                    ev("config_refused", key=m.group(1), value=m.group(2), reason=v, by=j["id"])
    mem["pending"] = still

    # Instructions for the worker: one file, controls first.
    def assemble():
        ctl = (sw / "controls.md").read_text().strip() if (sw / "controls.md").exists() else "(no controls yet)"
        am = (sw / "aims.md").read_text().strip() if (sw / "aims.md").exists() else "(no aims yet)"
        return ("# Instructions for the worker (assembled by the system each period from swarm/controls.md and swarm/aims.md; do not edit)\n\n"
                "Controls set the bounds; aims say what to push within them. When they conflict, the controls win. To challenge a "
                "control, say so in your log: the next review will file it as a request.\n\n## Controls (risk branch)\n\n" + ctl +
                "\n\n## Aims and capacity split (improvement branch)\n\n" + am + "\n\nMethods: swarm/spec.md and swarm/rules/.\n")
    ins = assemble()
    ih = hashlib.sha256(ins.encode()).hexdigest()[:16]
    if ih != mem.get("instructions_hash"):
        (sw / "instructions.md").write_text(ins); mem["instructions_hash"] = ih
        if not first:
            handoff.append("swarm/instructions.md changed. Re-read it now and work to it.")
            mem["instructions_changed"] = period

    # Escalations.
    for req, why in L.escalations(point):
        escal.append(("request", f"{req['id']} to {req['to']} ({req['key']}): {why}. \"{req['text'][:200]}\""))
    if escal:
        with (sw / "escalations.md").open("a") as fh:
            for kind, txt in escal:
                fh.write(f"- {unit} {period}: {kind}: {txt}\n")
        for kind, txt in escal:
            ev("escalation", kind=kind, text=txt[:300])

    # Verdicts on adopted changes, judged by the system; a miss goes back to the designer as a request to answer.
    verdict_md = ""
    if verify is not None:
        for p in verify.update(mem, period, W, series_of):
            ev("change_verdict", id=p["id"], verdict=p["verdict"], chance=p.get("chance"), measure=p["measure"])
            if p["verdict"].startswith(("no shift", "shift the wrong way")):
                sys_request(f"verdict-{p['id'].lower()}",
                            f"{p['id']} predicted {p['measure']} {p['dir']} within {p['n']} {p['unit']}s from {unit} {p['adopted']}; "
                            f"the system's verdict over {unit}s {p['window'][0]}-{p['window'][1]}: {p['verdict']} (the same test fires "
                            + (f"{p['chance']:.0%}" if p.get("chance") is not None else "an unknown share")
                            + " of the time where nothing changed). Keep it, revise it or revert it, and say why.")
        verdict_md = verify.markdown(mem, unit)
    # Charts: progress, facts, pursuit, requests, change verdicts, configuration and health.
    health = health_md(mem, L, point, prow, C, unit)
    prop = mem.get("proposed_facts", [])
    (sw / "charts.md").write_text(cmd_md + prog_md + facts.markdown(reg, prow, prop, cap) + L.table(point) + verdict_md + health)
    ev("measure", chart_signals=chart_bad, progress=[e["kind"] for e in events if e["kind"] != "new_point"])

    if over:
        return finish(mem, mem_p, log, handoff, cfg)

    # 2. Risk branch.
    reasons = [f"{k}: {l}" for k, l in risk_now]
    sweep_due = new_point and win["ok"] and (mem.get("last_sweep_point") is None or newest - mem["last_sweep_point"] >= C["risk_sweep_every"])
    if (reasons or sweep_due) and not busy("pulse"):
        pid = nid("P"); mem["last_sweep_point"] = newest if sweep_due else mem.get("last_sweep_point")
        trig = "; ".join(reasons) or f"routine sweep every {C['risk_sweep_every']} point(s)"
        spawn(pid, "pulse", pulse_prompt(pid, trig), budgets.get("pulse", 0.6), 12, {"trigger": trig})
    elif reasons:
        mem.setdefault("risk_waiting", []).extend(reasons)
    if mem.get("risk_waiting") and not busy("pulse"):
        pid = nid("P"); trig = "; ".join(mem.pop("risk_waiting"))[:600]
        spawn(pid, "pulse", pulse_prompt(pid, trig), budgets.get("pulse", 0.6), 12, {"trigger": trig})
    if mem.get("fault_queue") and not busy("diagnosis"):
        fq = mem.pop("fault_queue")
        did = nid("D")
        spawn(did, "diagnosis", diag_prompt(did, fq), budgets.get("diagnosis", 1.0), 20,
              {"fault_key": fq[-1]["key"] if len(fq) == 1 else "faults-" + "-".join(f["key"] for f in fq)[:40], "trigger": ", ".join(f["from"] for f in fq)})
    lc = mem.get("last_control_point")
    creqs = L.open_for("controls")
    if creqs and not busy("controls") and (lc is None or newest - lc >= C["control_gap"]):
        cid = nid("C"); L.take(creqs, cid)
        spawn(cid, "controls", controls_prompt(cid, L.prompt_list(creqs)), budgets.get("controls", 1.0), 20, {"reqs": [r["id"] for r in creqs]})
    if C["checker"] == "sample_claims" and new_point and win["ok"] and not busy("check"):
        lk = mem.get("last_check_point")
        if lk is None or newest - lk >= C["checker_every"]:
            mem["last_check_point"] = newest; kid = nid("K")
            spawn(kid, "check", check_prompt(kid), budgets.get("check", 0.6), 15, {"trigger": "claim sample"})

    # 3. Improvement branch.
    if new_point and win["ok"] and newest + 1 >= progress.START and not busy("strategist", "aims"):
        ls = mem.get("last_strat_point")
        why = []
        if ls is None:
            why.append("first strategy, after the baseline")
        elif newest - ls >= C["strategy_every"]:
            why.append(f"scheduled: {C['strategy_every']} points since the last strategy")
        elif imp_new and newest - ls >= 2:
            why += imp_new
        if why:
            sid = nid("S"); mem["last_strat_point"] = newest
            sreqs = L.open_for("strategist"); L.take(sreqs, sid)
            spawn(sid, "strategist", strat_prompt(sid, "; ".join(why), L.prompt_list(sreqs)), budgets.get("strategist", 0.8), 15,
                  {"trigger": "; ".join(why), "reqs": [r["id"] for r in sreqs]})
    lm = mem.get("last_method_point")
    dreqs = L.open_for("designer")
    if dreqs and not busy("method", "aims") and (lm is None or newest - lm >= C["method_gap"]):
        mid = nid("M"); L.take(dreqs, mid)
        spawn(mid, "method", method_prompt(mid, L.prompt_list(dreqs)), budgets.get("method", 1.5), 25, {"reqs": [r["id"] for r in dreqs]})

    # 4. Full audit (third line) and the Organizer, at even fractions of the horizon.
    n_aud = C["full_audits"]
    q = int(n_aud * t // horizon) if horizon else 0
    if 1 <= q < n_aud and q > mem.get("audits_done", 0) and not busy("audit"):
        mem["audits_done"] = q
        aid_ = nid("A"); spawn(aid_, "audit", audit_prompt(aid_, q, n_aud), budgets.get("audit", 1.5), 30, {"trigger": f"{q} of {n_aud}"})
        if not busy("organizer"):
            oid_ = nid("O"); spawn(oid_, "organizer", organizer_prompt(oid_), budgets.get("organizer", 0.8), 15, {"trigger": f"{q} of {n_aud}"})
    return finish(mem, mem_p, log, handoff, cfg)

def finish(mem, mem_p, log, handoff, cfg):
    mem_p.write_text(json.dumps(mem)); log.close()
    if handoff:
        txt = "\n\n".join("SYSTEM CADENCE: " + h for h in handoff)
        print(json.dumps({"hookSpecificOutput": {"hookEventName": cfg.get("hook_event", "PostToolUse"), "additionalContext": txt}}))

def health_md(mem, L, point, prow, C, unit):
    live = [r for r in L.reqs if r["status"] in ("open", "in_progress")]
    oldest = max((point - r["opened_point"] for r in live), default=0)
    rep = sum(1 for r in live if r["asked"] >= 3)
    lat = mem.get("aim_latency", [])
    gap = max((abs(r["gap"]) for r in prow if not r["label"].startswith("other")), default=None)
    cost = mem.get("cost", {})
    runs = {}
    for k in ROLE_OF:
        runs[k] = mem["n"].get({"pulse": "P", "check": "K", "diagnosis": "D", "controls": "C", "strategist": "S", "method": "M",
                                "audit": "A", "organizer": "O"}.get(k, "x"), 0)
    runs["aims"] = runs["strategist"]
    md = ["\n## System health (for the Organizer; computed by the system)\n",
          f"- Requests open: {len(live)}; oldest {oldest} points; asked 3 or more times: {rep}.",
          f"- Strategy to aims reaching the worker: {('median ' + str(sorted(lat)[len(lat) // 2]) + ' ' + unit + 's') if lat else 'none yet'}.",
          f"- Largest gap between planned and actual capacity share: {('%.0f points' % (gap * 100)) if gap is not None else 'no plan yet'}.",
          "- Jobs run: " + ", ".join(f"{ROLE_OF[k]} {v}" for k, v in runs.items() if v) + ".",
          f"- Review cost so far: ${sum(cost.values()):.2f} (" + ", ".join(f"{k} ${v:.2f}" for k, v in cost.items()) + ").",
          "- Configuration (setting = value, bounds): " + "; ".join(f"{k} = {v} {mem['bounds'][k]}" for k, v in C.items()) + ".",
          f"- Changes adopted: " + (", ".join(f"{c['id']} ({c['branch']}, {unit} {c['period']})" for c in mem.get("changes", [])[-8:]) or "none") + "."]
    preds = mem.get("predictions", [])
    if preds:
        judged = [p for p in preds if p.get("verdict")]
        hits = sum(1 for p in judged if p["verdict"].startswith("shift as predicted"))
        exp = sum(p.get("chance") or 0 for p in judged)
        md.append(f"- Change verdicts: {len(judged)} judged, {hits} shifted as predicted against {exp:.1f} expected by chance; "
                  f"{sum(1 for p in preds if p.get('problem'))} could not be judged as written.")
    return "\n".join(md) + "\n"
