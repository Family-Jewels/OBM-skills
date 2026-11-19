"""OBM cadence engine, version 2: the safety half (v1) plus the improvement half. Task-agnostic.

Called by engine.py when the config has "version": 2. What changes from v1:
- Timing comes from the task, not from fixed periods. The adapter's spec() states the horizon, the natural cycle and the
  clock; progress.derive_window turns them into a point window, and every interval is counted in points:
  a pulse every point (every second point after three quiet pulses), redesigns at least 3 points after the last adoption,
  an opportunity review every 3 points without one, full audits at each quarter of the horizon.
- Progress measures (progress.py): celeration per measure, a floor line and a stretch aim for the top measure, resources
  in use and idle, guardrails, experiments judged on the system's data.
- An opportunity review (the diagnostician's opportunity mode) runs on a schedule and when the top measure falls below
  its floor line or its celeration is flat or going the wrong way, even when every level chart is stable. The designer
  redesigns from it as from a diagnosis.
- Reviews give about one keep-doing item to four fixes, with at least one keep-doing.
v2 supports the skills prompts only; the plain (no-skills) arm stays on v1.
"""
import importlib, json, re, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import charts, progress
import experiments as X

GAP_POINTS = 3

def load_spec(cfg, adapter):
    spec = adapter.spec() if hasattr(adapter, "spec") else {}
    spec.update(cfg.get("spec", {}))
    spec.setdefault("unit", cfg.get("unit", "period")); spec.setdefault("horizon", cfg.get("horizon"))
    return spec

def preflight(spec, reading):
    """Checks the adapter before the run, on its first reading. Returns a list of problems (empty = ready)."""
    p = []
    m = reading.get("measures", {})
    if not spec.get("horizon"):
        p.append("no horizon")
    if spec.get("top") not in spec.get("measures", {}):
        p.append("the top measure is not among the measures")
    g = spec.get("goal", {})
    if not (g.get("value") and g.get("value") > 0):
        p.append("no goal value or ceiling: the floor and aim lines cannot be drawn")
    for name, d in spec.get("measures", {}).items():
        v = m.get(d.get("from", name))
        if v is None:
            continue  # some measures only exist once there is data (e.g. the first purchase)
        if not isinstance(v, (int, float)):
            p.append(f"measure {name} gives no number")
        elif v < 0:
            p.append(f"measure {name} is negative ({v}): celeration needs a positive flow or level")
    for rname, r in (reading.get("resources") or {}).items():
        if not r.get("available") or r["available"] <= 0:
            p.append(f"resource {rname} reports no available amount")
    for gd in spec.get("guardrails", []):
        if gd.get("min") is None and gd.get("max") is None:
            p.append(f"guardrail {gd.get('label')} has no side")
    if not progress.derive_window(spec["horizon"], spec.get("cycle", 1), spec.get("clock", "period"))["ok"]:
        p.append("horizon too short for celeration; level charts only")
    return p

def design_hash(sw):
    import hashlib
    h = hashlib.sha256()
    for f in [sw / "spec.md"] + sorted((sw / "rules").glob("*")) if (sw / "rules").exists() else [sw / "spec.md"]:
        if f.is_file():
            h.update(f.name.encode()); h.update(f.read_bytes())
    return h.hexdigest()[:16]

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
    mem = json.loads(mem_p.read_text()) if mem_p.exists() else {"last_period": -1, "n_audit": 0, "n_pulse": 0, "n_opp": 0,
                                                                "history": [], "pending": [], "quarters_done": 0}
    if period <= mem["last_period"]:
        return
    first = mem["last_period"] < 0
    mem["last_period"] = period
    mem["history"] = (mem["history"] + [measures])[-50:]
    sw = ws / "swarm"; sw.mkdir(parents=True, exist_ok=True)
    log = log_p.open("a")
    handoff = ""
    if first:
        probs = preflight(spec, reading)
        win = progress.derive_window(horizon, spec.get("cycle", 1), spec.get("clock", "period"))
        log.write(json.dumps({"t": time.time(), "period": period, "event": "preflight", "problems": probs, "window": win}) + "\n")
        if probs:
            handoff += "SYSTEM CADENCE: adapter preflight found: " + "; ".join(probs) + ". The system measures what it can."
    met = sw / "metrics_system.md"
    if not mem.get("owns_metrics"):
        if met.exists():
            met.rename(sw / "metrics_designed_by_agent.md")
        mem["owns_metrics"] = True
    if not met.exists():
        met.write_text(f"# Ground-truth measures (written by the system every {unit}; do not edit)\n\n| {unit} | " + " | ".join(measures)
                       + " |\n| --- |" + " --- |" * len(measures) + "\n")
    with met.open("a") as f:
        f.write(f"| {period} | " + " | ".join(str(v) for v in measures.values()) + " |\n")
    win = mem.setdefault("window", progress.derive_window(horizon, spec.get("cycle", 1), spec.get("clock", "period")))
    W = win["w"]
    cfg.setdefault("charts", {})["own_best_window"] = W
    cmd_md, chart_bad = charts.update(cfg, mem, period, measures, unit)
    prog_md, events = progress.update(mem, spec, t, measures, resources)
    X.record_units(mem, t, reading.get("units"))
    if hasattr(adapter, "snapshot"):  # ground truth of what the swarm controls, for the checker's fidelity checks
        snap = sw / "snapshots"; snap.mkdir(exist_ok=True)
        (snap / f"{period:05d}.md").write_text(f"# Snapshot at {unit} {period} (written by the system from ground truth; do not edit)\n\n" + adapter.snapshot())
        for old in sorted(snap.glob("*.md"))[:-(3 * W + 2)]:
            old.unlink()
    exp_md, exp_acts = X.step(mem, spec, sw, t, mem["progress"]["last_point"], True, W)
    unit_md = ""
    if mem.get("units"):
        ums = list(mem["units"]); ids = sorted({u for m in ums for u in mem["units"][m]})
        unit_md = ("\n## Units (for experiment slices; latest point, median per " + unit + ")\n\n| unit | " + " | ".join(ums) + " |\n| --- |"
                   + " --- |" * len(ums) + "\n")
        for u in ids:
            vals = []
            for m in ums:
                pts = progress.points(mem["units"][m].get(u, []), W, "flow", now=t)
                vals.append(str(round(pts[-1][1], 2)) if pts else "—")
            unit_md += f"| {u} | " + " | ".join(vals) + " |\n"
    (sw / "charts.md").write_text(cmd_md + prog_md + unit_md + exp_md)
    log.write(json.dumps({"t": time.time(), "period": period, "event": "measure", "chart_signals": chart_bad,
                          "progress": [e["kind"] for e in events if e["kind"] != "new_point"]}) + "\n")

    new_point = any(e["kind"] == "new_point" for e in events)
    newest = mem["progress"]["last_point"]
    gr_now = sorted(e["label"] for e in events if e["kind"] == "guardrail")
    if gr_now and gr_now != mem.get("guardrails_reported"):
        handoff += ("\n\nSYSTEM CADENCE: " + "; ".join(gr_now) + ". Revert any experiment that may have caused it, and restore the "
                    "guardrail before anything else.")
        mem["flag_since_pulse"] = True
        log.write(json.dumps({"t": time.time(), "period": period, "event": "guardrail", "labels": gr_now}) + "\n")
    mem["guardrails_reported"] = gr_now
    for e in events:
        if e["kind"] == "aim_raised":
            handoff += f"\n\nSYSTEM CADENCE: the aim for {spec['top']} was met on 2 of the last 3 points, so it has been raised: {e['label']}."
            log.write(json.dumps({"t": time.time(), "period": period, "event": "aim_raised", "label": e["label"]}) + "\n")
    if chart_bad:
        mem["flag_since_pulse"] = True

    budgets = cfg.get("budgets", {}); model = cfg.get("model", "claude-haiku-5-5")
    jobs = log_p.with_suffix(".jobs"); jobs.mkdir(exist_ok=True)
    new_jobs = []

    def spawn(jid, kind, prompt, budget, turns, extra):
        out = jobs / f"{jid}.json"
        cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json", "--max-turns", str(turns),
               "--tools", "Read,Write,Edit,Glob,Grep,Skill", "--allowedTools", "Read,Write,Edit,Glob,Grep,Skill", "--strict-mcp-config",
               "--permission-mode", "acceptEdits", "--max-budget-usd", str(budget), "--no-session-persistence"]
        shell = " ".join("'" + c.replace("'", "'\\''") + "'" for c in cmd) + f" > '{out}.tmp' 2>/dev/null; mv '{out}.tmp' '{out}'"
        if cfg.get("dry_run"):  # replay and tests: no model call; the job "finishes" at once with a neutral report
            out.write_text(json.dumps({"result": f"dry run {jid}. Diagnosis needed: {cfg.get('dry_run_diagnosis', 'no')}\nFidelity: pass\n"
                                                 f"Verdict: {cfg.get('dry_run_verdict', 'keep')}", "total_cost_usd": 0}))
            if kind == "redesign":  # alternate between changing the design and setting up an experiment
                mem["dry_n"] = mem.get("dry_n", 0) + 1
                if mem["dry_n"] % 2:
                    with (sw / "spec.md").open("a") as fh: fh.write(f"\nchange {jid}\n")
                else:
                    (sw / "experiments").mkdir(exist_ok=True)
                    ids = sorted({u for m in mem.get("units", {}).values() for u in m})
                    (sw / "experiments" / f"E-{mem['dry_n']:03d}.md").write_text(
                        f"Driver: {next(iter(spec.get('unit_measures', {})), spec['top'])}\nSlice: {ids[0] if ids else 'all'}\nControl: rest\n"
                        f"Start: {period + 1}\nEnd: {period + GAP_POINTS * W}\nApplied: {period + 1}\n")
        else:
            subprocess.Popen(["sh", "-c", shell], cwd=ws, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        new_jobs.append({"id": jid, "kind": kind, "period": period, "started": time.time(), "out": str(out), **extra})
        log.write(json.dumps({"t": time.time(), "period": period, "event": "started", "id": jid, "kind": kind, "trigger": extra.get("trigger")}) + "\n")

    def redesign_ok():
        busy = any(p.get("kind") in ("diagnosis", "redesign", "opportunity") for p in mem["pending"] + new_jobs)
        la = mem.get("last_adopted_point")
        return not busy and (la is None or newest - la >= GAP_POINTS)

    where = f"{unit} {period} of {horizon}"
    measure_names = ", ".join(list(spec.get("unit_measures", {})) + list(spec.get("measures", {})))
    charts_note = ("swarm/charts.md (written by the system: level charts with limits from the data; Progress: celeration per measure, the "
                   "top measure's floor and aim lines, own best; Resources in use and idle; Guardrails; Experiments)")

    def spawn_redesign(src_id, src_kind):
        rid = "R-" + src_id[2:] if src_kind == "diagnosis" else "R-" + src_id
        what = (f"Diagnosis {src_id} (swarm/audits/{src_id}.md) says what is going wrong and why." if src_kind == "diagnosis" else
                f"Opportunity review {src_id} (swarm/audits/{src_id}.md) names where the most room is: the constraint, idle resources, "
                f"what worked best, and candidate experiments.")
        spawn(rid, "redesign",
              f"Use the obm-swarm-designer skill in REDESIGN mode, invoked by the system at {where} of the work the swarm in swarm/ is doing. "
              f"{what} Read {charts_note} and the driver tree in swarm/spec.md. First ask whether the direction is right, then make the "
              f"smallest design change that addresses it: fix the cause, elevate the constraint, put an idle resource to work, scale up what "
              f"works, or set up up to two experiments inside the spec's experiment budget. Write each experiment to swarm/experiments/E-NNN.md "
              f"with lines 'Driver:' (exactly one of the measures the system records: {measure_names}), 'Slice:' (the units it touches, "
              f"from the Units table in swarm/charts.md, or 'all'), 'Control: rest', 'Change:', 'Prediction:', 'Guardrail:', "
              f"'Start: <{unit} number>' and 'End: <{unit} number>', lasting at least {GAP_POINTS} points ({GAP_POINTS * W} {unit}s). "
              f"Prefer a slice with the rest as control, judged on a per-unit driver ({", ".join(spec.get("unit_measures", {})) or "none in this task"}); a whole-system driver can only be judged on the whole system; experiments whose slices overlap run one after another. Change exactly one lever on the slice and leave the core work going on as usual on slice and control alike: never freeze restocking or other core work on a slice. You do not decide "
              f"keep or revert: the system measures, and the auditor rules. The goal and the aim are the human's: never lower them. State a prediction "
              f"in the record: which measure should shift, which way, by which {unit}. Never change anything in a way that stops the core "
              f"work. Before changing swarm/spec.md or a rule file, copy the old version to swarm/history/ with its version number; keep the "
              f"current version at its usual path. Then write the redesign record to swarm/audits/{rid}.md. Reply with the change in under 150 words.",
              budgets.get("redesign", 1.5), 25, {"after": src_id})

    # 0. Experiments: notes, fidelity checks (checker) and verdicts (auditor), all called by the system.
    for act in exp_acts:
        if act[0] == "note":
            handoff += "\n\nSYSTEM CADENCE: " + act[1]; mem["flag_since_pulse"] = True
            log.write(json.dumps({"t": time.time(), "period": period, "event": "experiment_note", "text": act[1][:200]}) + "\n")
        elif act[0] == "fidelity":
            e = act[1]; fid = f"F-{e['id']}-{mem['exp'][e['id']]['fails'] + 1}"
            (sw / "audits").mkdir(exist_ok=True)
            spawn(fid, "fidelity", f"Use the obm-swarm-checker skill for an EXPERIMENT FIDELITY CHECK, invoked by the system at {where}. "
                  f"Experiment {e['id']} (swarm/experiments/{e['id']}.md) is due to start. Verify from ground truth, never from the "
                  f"orchestrator's notes, that its Change was made as written and on its Slice only. The system's snapshots of what the "
                  f"swarm controls are in swarm/snapshots/ (one per {unit}, written from ground truth): compare the latest with the one "
                  f"before the experiment's Start. Check that units outside the slice did not get the change, and that no other "
                  f"running experiment touches this slice. Those three are the only pass criteria. Timing is not one: the clock starts "
                  f"when this check passes, so a change made after the planned Start is fine. Ordinary core work going on alike on slice "
                  f"and control (restocking, new products, orders) is not a violation, and record-keeping, cost claims and other "
                  f"pre-conditions in the file are notes, not criteria: the system measures cost and enforces guardrails itself. Write swarm/audits/{fid}.md: what you compared, any mismatch, then a last "
                  f"line exactly 'Fidelity: pass' or 'Fidelity: fail'.", budgets.get("pulse", 0.6), 15, {"exp": e["id"]})
        elif act[0] == "verdict":
            e, c = act[1], act[2]; vid = f"V-{e['id']}"
            eff = f"{c['effect']:.3f}" if c["effect"] else "none"
            env = f"x{c['envelope']:.2f}" if c["envelope"] else "none"
            spawn(vid, "verdict", f"Use the obm-swarm-auditor skill for an EXPERIMENT VERDICT, invoked by the system at {where}. Experiment "
                  f"{e['id']} (swarm/experiments/{e['id']}.md) has ended. The system's comparison on its driver ({c['how']}): "
                  f"{c['before_n']} points before, {c['after_n']} during; effect {eff} (1.0 = no change; better is {c['better']}); "
                  f"envelope of the earlier bounce {env}; the system reads this as: {c['reading']}. Judge it against the experiment's "
                  f"prediction and guardrail, using the system's data, not the orchestrator's notes. Keep only an effect beyond the "
                  f"bounce in the right direction; revert one in the wrong direction or one that crossed a guardrail; call an effect "
                  f"inside the bounce too small to read and say whether a larger or longer test is worth it. Write swarm/audits/{vid}.md "
                  f"briefly, ending with a line exactly 'Verdict: keep', 'Verdict: revert' or 'Verdict: too small to read'.",
                  budgets.get("pulse", 0.6), 12, {"exp": e["id"]})
    mem["pending"] += new_jobs; new_jobs = []

    # 1. Deliver anything finished.
    still = []
    for j in mem["pending"]:
        out = Path(j["out"])
        if not out.exists():
            if time.time() - j["started"] > cfg.get("review_timeout_s", 1200):
                log.write(json.dumps({"t": time.time(), "period": period, "event": "review_timeout", "id": j["id"]}) + "\n")
            else:
                still.append(j)
            continue
        try: r = json.loads(out.read_text())
        except Exception: r = {}
        log.write(json.dumps({"t": time.time(), "period": j["period"], "delivered": period, "event": j["kind"], "id": j["id"],
                              "trigger": j.get("trigger"), "cost": r.get("total_cost_usd"), "turns": r.get("num_turns")}) + "\n")
        rec_f = sw / "audits" / f"{j['id']}.md"
        rec = rec_f.read_text() if rec_f.exists() else (r.get("result") or "(no record)")
        if j["kind"] == "redesign":
            h = design_hash(sw)
            if h != mem.get("design_hash"):  # a new phase only when the design itself changed, not when only experiments were set up
                charts.new_phase(mem, j["id"], period); progress.new_phase(mem)
                mem["last_adopted_point"] = newest
            mem["design_hash"] = h; mem["flag_since_pulse"] = True
            handoff += (f"\n\nSYSTEM CADENCE: the designer redesigned the work system after {j['after']} (swarm/audits/{j['id']}.md). "
                        f"Adopt it from now on: re-read swarm/spec.md, swarm/rules/ and swarm/experiments/.\n\n{rec[-2000:]}")
            continue
        if j["kind"] == "fidelity":
            ok, state = X.fidelity_result(mem, j["exp"], rec, period, W)
            if ok:
                handoff += (f"\n\nSYSTEM CADENCE: the checker confirmed experiment {j['exp']} was made as written ({j['id']}). Its clock "
                            f"starts now and ends at {unit} {mem['exp'][j['exp']]['end_t']}. Leave the slice as it is until the verdict.")
            else:
                handoff += (f"\n\nSYSTEM CADENCE: the checker found experiment {j['exp']} was not made as written ({j['id']}); "
                            + ("it is void after three failed checks." if state == "void" else "fix it on the slice only; it will be checked again.")
                            + f"\n\n{rec[-1200:]}")
            log.write(json.dumps({"t": time.time(), "period": period, "event": "fidelity_" + ("pass" if ok else "fail"), "exp": j["exp"]}) + "\n")
            continue
        if j["kind"] == "verdict":
            v = X.verdict_result(mem, j["exp"], rec)
            ef = sw / "experiments" / f"{j['exp']}.md"
            if ef.exists():
                with ef.open("a") as fh:
                    fh.write(f"\n\n## Verdict (by the auditor in swarm/audits/{j['id']}.md; written by the system): {v}\n")
            handoff += (f"\n\nSYSTEM CADENCE: the auditor's verdict on experiment {j['exp']} is '{v}' ({j['id']}). Apply it this {unit}: "
                        f"{'keep the change, and extend it where the spec allows' if v == 'keep' else 'undo the change on its slice' if v == 'revert' else 'leave it as it stands until the designer decides'}.\n\n{rec[-800:]}")
            log.write(json.dumps({"t": time.time(), "period": period, "event": "experiment_verdict", "exp": j["exp"], "verdict": v}) + "\n")
            mem["flag_since_pulse"] = True
            continue
        if j["kind"] in ("diagnosis", "opportunity"):
            label = "diagnosis" if j["kind"] == "diagnosis" else "opportunity review"
            handoff += f"\n\nSYSTEM CADENCE: {label} {j['id']} (swarm/audits/{j['id']}.md); the designer is now redesigning from it.\n\n{rec[-1200:]}"
            spawn_redesign(j["id"], j["kind"])
            continue
        label = "full audit" if j["kind"] == "audit" else "pulse review"
        handoff += (f"\n\nSYSTEM CADENCE: {label} {j['id']} reviewed the work as of {unit} {j['period']} (swarm/audits/{j['id']}.md). "
                    f"Act on it this {unit}: do the fixes and keep doing what it says works. Log what you did.\n\n{rec[-3500:]}")
        wants = "diagnosis needed: yes" in rec.lower()
        if j["kind"] == "pulse":
            mem["quiet_pulses"] = 0 if (wants or j.get("flagged")) else mem.get("quiet_pulses", 0) + 1
        if wants:
            if redesign_ok():
                did = f"D-{j['id']}"
                spawn(did, "diagnosis",
                      f"Use the obm-swarm-diagnostician skill, invoked by the system because {label} {j['id']} (swarm/audits/{j['id']}.md) says a "
                      f"diagnosis is needed, at {where}. Read {charts_note} and the driver tree in swarm/spec.md. Walk the tree from the top measure "
                      f"down to the driver that moved, then find why; ask too whether any resource sits idle while a driver is short. Do not write a "
                      f"fix or change anything: the designer will redesign from your diagnosis. Write swarm/audits/{did}.md and reply with it in under 200 words.",
                      budgets.get("diagnosis", 1.0), 20, {"after": j["id"], "trigger": label})
                handoff += "\n\nSYSTEM CADENCE: a diagnosis of this finding has started; it and the redesign will be handed to you when ready."
            else:
                handoff += (f"\n\nSYSTEM CADENCE: no redesign now: one is in progress or was adopted less than {GAP_POINTS} points "
                            f"({GAP_POINTS * W} {unit}s) ago, so its effect cannot be judged yet. Use the review's items instead.")
                log.write(json.dumps({"t": time.time(), "period": period, "event": "diagnosis_deferred", "after": j["id"]}) + "\n")
    mem["pending"] = still + new_jobs; new_jobs = []

    if over:
        handoff = handoff.strip()
        mem_p.write_text(json.dumps(mem)); log.close()
        if handoff:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": cfg.get("hook_event", "PostToolUse"), "additionalContext": handoff}}))
        return

    # 2. Opportunity review: on the progress rules, or every 3 points without one.
    if "design_hash" not in mem:
        mem["design_hash"] = design_hash(sw)
    running = [k for k, v in mem.get("exp", {}).items() if v.get("state") in ("queued", "fidelity", "running", "verdict")]
    lo0 = mem.get("last_opp_point", mem.get("first_point"))
    overdue = lo0 is not None and newest - lo0 >= 2 * GAP_POINTS  # experiments may not hold off the review for ever
    if new_point and win["ok"] and running and not overdue:
        log.write(json.dumps({"t": time.time(), "period": period, "event": "opportunity_waits", "running": running}) + "\n")
    if new_point and win["ok"] and (not running or overdue):  # while an experiment runs, its end is usually the next decision point
        reasons = [e["label"] for e in events if e["kind"] in ("below_floor", "flat_or_wrong")]
        lo = mem.get("last_opp_point")
        if lo is None:
            lo = mem.setdefault("first_point", newest)
        if newest - lo >= GAP_POINTS:
            reasons.append(f"scheduled: {GAP_POINTS} points without an opportunity review")
        if reasons or mem.get("opp_wanted"):
            why = "; ".join(reasons) or mem.get("opp_wanted")
            if redesign_ok() and newest >= progress.START:
                mem["n_opp"] += 1; oid = f"O-{mem['n_opp']:03d}"; mem["last_opp_point"] = newest; mem["opp_wanted"] = None
                (sw / "audits").mkdir(exist_ok=True)
                spawn(oid, "opportunity",
                      f"Use the obm-swarm-diagnostician skill in OPPORTUNITY mode, invoked by the system ({why}), at {where} of the work the "
                      f"swarm in swarm/ is doing. Nothing may be broken: the question is where the most room for improvement is. Read {charts_note}, "
                      f"the driver tree in swarm/spec.md, swarm/experiments/ and earlier records in swarm/audits/. Rank the drivers by gap x leverage, "
                      f"find the constraint, list idle resources and what one more unit put to work would likely return, study the own-best stretch "
                      f"(what was different then), and name up to two candidate experiments, each with its driver, predicted shift and guardrail. "
                      f"Do not write a fix or change anything: the designer will redesign from your findings. Write swarm/audits/{oid}.md and reply "
                      f"with it in under 200 words.", budgets.get("diagnosis", 1.0), 20, {"trigger": why})
            else:
                mem["opp_wanted"] = why
    mem["pending"] += new_jobs; new_jobs = []

    # 3. Pulse every point (every second point after three quiet pulses), full audit at each quarter of the horizon.
    q = int(4 * t // horizon) if horizon else 0
    full_due = 1 <= q <= 3 and q > mem.get("quarters_done", 0)
    lp = mem.get("last_pulse_point")
    step = 2 if mem.get("quiet_pulses", 0) >= 3 else 1
    pulse_due = new_point and (lp is None or newest - lp >= step) and win["ok"]
    lr = mem.get("last_review_period", -10**6)
    early = bool(chart_bad) and step == 2 and period - lr >= max(1, W // 2)  # with weekly pulses, a signal waits for the next one
    if not win["ok"]:
        pulse_due = period - lr >= cfg.get("pulse_every", 5)
    busy_kinds = {j["kind"] for j in mem["pending"]}
    if full_due and "audit" in busy_kinds:
        full_due = False
    if not full_due and "pulse" in busy_kinds:
        pulse_due = early = False
    if full_due or pulse_due or early:
        (sw / "audits").mkdir(exist_ok=True)
        common = (f"at {where} of the work the swarm in swarm/ is doing. You cannot act on the work itself; review the records. The "
                  f"ground-truth measures (swarm/metrics_system.md) and {charts_note} are written by the system, never by an agent.")
        items = ("then at most five items for the orchestrator, about one keep-doing (what works and should be done more) to four fixes, "
                 "with at least one keep-doing; never a pause of its core work")
        mem["last_review_period"] = period
        if full_due:  # a due pulse is not lost: it runs at the next period, beside the audit
            mem["quarters_done"] = q; mem["n_audit"] += 1; aid = f"A-{mem['n_audit']:03d}"
            spawn(aid, "audit", f"Use the obm-swarm-auditor skill for a FULL AUDIT, invoked by the system at quarter {q} of the horizon. This is "
                  f"audit {aid}, {common} Judge the outcome first: is the top measure above its floor line, how far from its aim, and is its "
                  f"celeration near its own best? Is capacity in use, or are resources idle? Is anything declining? Is the direction right: does "
                  f"the driver tree in swarm/spec.md add up to the goal, and are its drivers the ones that move it? Do the system's measures still "
                  f"track the goal, or has the work started serving the measures? Did each redesign's predicted shift appear by its date? Judge "
                  f"each experiment in swarm/experiments/ against its prediction: a missed prediction is information, an unrun one is a finding. "
                  f"Did anything lower the goal or an aim? Then whether earlier findings were acted on, then whether the records are current. "
                  f"Write swarm/audits/{aid}.md: findings first, {items}, then a last line exactly 'Diagnosis needed: yes' or 'Diagnosis needed: no'.",
                  budgets.get("audit", 1.5), 30, {"trigger": f"quarter {q}"})
        else:
            mem["n_pulse"] += 1; aid = f"P-{mem['n_pulse']:03d}"
            if pulse_due:
                mem["last_pulse_point"] = newest
            flagged = bool(mem.get("flag_since_pulse")); mem["flag_since_pulse"] = False
            spawn(aid, "pulse", f"Use the obm-swarm-auditor skill for a PULSE REVIEW, invoked by the system "
                  f"{'because a level chart signalled a change in the wrong direction' if early and not pulse_due else 'on its schedule'}. "
                  f"This is pulse {aid}, {common} Read only swarm/charts.md, the driver tree in swarm/spec.md, swarm/experiments/ and the last "
                  f"lines of the orchestrator's log. Answer: which measures show a signal and which only routine variation (never react to routine "
                  f"variation); is the top measure above its floor line and how far from its aim; which driver's celeration is flattest for its "
                  f"leverage; is any resource idle; what is working best, and is the swarm doing more of it. Write swarm/audits/{aid}.md in under "
                  f"250 words: the answers, {items}, then a last line exactly 'Diagnosis needed: yes' or 'Diagnosis needed: no'. Answer 'yes' only "
                  f"when a level chart signals a change in the wrong direction or a redesign's predicted shift has not appeared by its date. A flat "
                  f"celeration or a point below the floor line goes to the system's opportunity review, not to a diagnosis.",
                  budgets.get("pulse", 0.6), 12, {"trigger": "chart signal" if early and not pulse_due else "scheduled", "flagged": flagged})
        mem["pending"] += new_jobs
    handoff = handoff.strip()
    mem_p.write_text(json.dumps(mem)); log.close()
    if handoff:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": cfg.get("hook_event", "PostToolUse"), "additionalContext": handoff}}))
