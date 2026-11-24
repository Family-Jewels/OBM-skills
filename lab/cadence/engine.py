#!/usr/bin/env python3
"""OBM cadence engine: the system, not the agents, invokes the roles on a schedule. Task-agnostic.

Run it as a hook that fires once per period of the work (for example, a PostToolUse hook on the tool that ends a period,
or a scheduler). Each time it runs:
  1. Measurement (no model): asks the task's adapter for this period's ground-truth measures, appends them to
     swarm/metrics_system.md, and rewrites swarm/charts.md: process behavior charts with limits computed from the data,
     their signals, and the gap to an exemplar (charts.py).
  2. Pulse review every `pulse_every` periods: a short auditor review of the numbers, ending in at most three pivots.
  3. Full audit every `audit_every` periods, or at once when a chart signals a change in the wrong direction or an
     alarm rule fires.
  4. Diagnosis when a pulse or audit ends with "Diagnosis needed: yes": what is going wrong and why, no fix.
  5. Redesign: the designer reads the diagnosis and reworks the spec, KPIs or rules (spaced so each change can be judged).
  6. Hand-off: reviews run in the background while the work continues; their findings and any redesign go back to
     the orchestrator at the first period after they finish, as additional context on the hook's event.

usage: engine.py <config.json>      (reads the hook's JSON on stdin and ignores it)
Config keys: workspace, log, adapter ("module.path:Class"), adapter_args, unit ("day", "cycle", ...), horizon,
pulse_every (default 5), audit_every (default 50), min_periods_between_redesigns (default 20: a change must have time
to show its effect), signals ([{measure, op, value, periods, label, not_before, min_gap}]), model, hook_event (default
PostToolUse), budgets ({pulse, audit, diagnosis, redesign} in USD), charts ({measures: [{name, from, diff, better}],
not_before, min_points, baseline_points}), exemplar ({measure, points: {period: value}, origin, source}).
"""
import importlib, json, operator, subprocess, sys, time
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import charts
from pathlib import Path

OPS = {"==": operator.eq, "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge, "!=": operator.ne}

def main():
    sys.stdin.read()
    cfg = json.loads(Path(sys.argv[1]).read_text())
    if cfg.get("version", 1) >= 2 and cfg.get("prompts") != "plain":  # v2: the improvement half (engine_v2.py); v1 below is unchanged
        import engine_v2
        return engine_v2.main(cfg)
    ws = Path(cfg["workspace"]); log_p = Path(cfg["log"]); unit = cfg.get("unit", "period")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    mod, cls = cfg["adapter"].split(":")
    reading = getattr(importlib.import_module(mod), cls)(**cfg.get("adapter_args", {})).read()
    if reading is None:
        return
    period, over, measures = reading["period"], reading["over"], reading["measures"]
    mem_p = log_p.with_suffix(".mem.json")
    mem = json.loads(mem_p.read_text()) if mem_p.exists() else {"last_period": -1, "last_audit": 0, "last_pulse": 0, "n_audit": 0, "n_pulse": 0, "history": []}
    if period <= mem["last_period"]:
        return
    mem["last_period"] = period
    mem["history"] = (mem["history"] + [measures])[-50:]
    sw = ws / "swarm"; sw.mkdir(parents=True, exist_ok=True)
    met = sw / "metrics_system.md"
    if not mem.get("owns_metrics"):
        if met.exists():  # an agent wrote it; the system's file has one writer, the system
            met.rename(sw / "metrics_designed_by_agent.md")
        mem["owns_metrics"] = True
    if not met.exists():
        met.write_text(f"# Ground-truth measures (written by the system every {unit}; do not edit)\n\n| {unit} | " + " | ".join(measures)
                       + " |\n| --- |" + " --- |" * len(measures) + "\n")
    with met.open("a") as f:
        f.write(f"| {period} | " + " | ".join(str(v) for v in measures.values()) + " |\n")
    cmd_md, chart_bad = charts.update(cfg, mem, period, measures, unit)
    (sw / "charts.md").write_text(cmd_md)
    log = log_p.open("a")
    log.write(json.dumps({"t": time.time(), "period": period, "event": "measure", "chart_signals": chart_bad}) + "\n")

    fired = None
    for s in cfg.get("signals", []):
        if period < s.get("not_before", 0):
            continue
        last = [h.get(s["measure"]) for h in mem["history"][-s.get("periods", 1):]]
        if len(last) == s.get("periods", 1) and all(v is not None and OPS[s["op"]](v, s["value"]) for v in last):
            if period - max(mem["last_audit"], mem["last_pulse"]) >= s.get("min_gap", 3):
                fired = s.get("label", f"{s['measure']} {s['op']} {s['value']}"); break
    if not fired and chart_bad and period - max(mem["last_audit"], mem["last_pulse"]) >= cfg.get("chart_min_gap", 5):
        fired = "chart signal, wrong direction: " + "; ".join(chart_bad)
    full_due = period - mem["last_audit"] >= cfg.get("audit_every", 50)
    pulse_due = period - max(mem["last_pulse"], mem["last_audit"]) >= cfg.get("pulse_every", 5)
    handoff = ""
    budgets = cfg.get("budgets", {}); model = cfg.get("model", "claude-haiku-5-5"); horizon = cfg.get("horizon", "?")
    jobs = log_p.with_suffix(".jobs"); jobs.mkdir(exist_ok=True)
    gap = cfg.get("min_periods_between_redesigns", cfg.get("min_periods_between_diagnoses", 20))
    mem.setdefault("pending", [])
    plain = cfg.get("prompts") == "plain"  # no OBM skills: neutral review prompts against swarm/plan.md
    new_jobs = []

    def spawn(jid, kind, prompt, budget, turns, extra):
        """Start a review in the background. Its result is handed over at the first period after it finishes,
        like a report that arrives the next morning, so the work never waits for it."""
        out = jobs / f"{jid}.json"
        cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json", "--max-turns", str(turns),
               "--tools", "Read,Write,Edit,Glob,Grep,Skill", "--allowedTools", "Read,Write,Edit,Glob,Grep,Skill", "--strict-mcp-config",
               "--permission-mode", "acceptEdits", "--max-budget-usd", str(budget), "--no-session-persistence"]
        shell = " ".join("'" + c.replace("'", "'\\''") + "'" for c in cmd) + f" > '{out}.tmp' 2>/dev/null; mv '{out}.tmp' '{out}'"
        subprocess.Popen(["sh", "-c", shell], cwd=ws, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        new_jobs.append({"id": jid, "kind": kind, "period": period, "started": time.time(), "out": str(out), **extra})

    # 1. Deliver anything that has finished since the last period.
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
        if j["kind"] == "redesign":
            rf = sw / "audits" / f"{j['id']}.md"
            rec = rf.read_text() if rf.exists() else (r.get("result") or "(no record)")
            charts.new_phase(mem, j["id"], period)
            mem["last_adopted"] = period  # spacing counts from adoption, so each change gets its full window
            handoff += ((f"\n\nSYSTEM CADENCE: the plan was revised after diagnosis {j['after']} (swarm/audits/{j['id']}.md). "
                         f"Follow it from now on: re-read swarm/plan.md.\n\n{rec[-2000:]}") if plain else
                        (f"\n\nSYSTEM CADENCE: the designer redesigned the work system after diagnosis {j['after']} "
                        f"(swarm/audits/{j['id']}.md). Adopt it from now on: re-read swarm/spec.md and swarm/rules/.\n\n{rec[-2000:]}"))
            continue
        if j["kind"] == "diagnosis":
            df = sw / "audits" / f"{j['id']}.md"
            diag = df.read_text() if df.exists() else (r.get("result") or "(no diagnosis)")
            handoff += f"\n\nSYSTEM CADENCE: diagnosis {j['id']} (swarm/audits/{j['id']}.md); " + ("the plan is now being revised from it." if plain else "the designer is now reworking the design from it.") + f"\n\n{diag[-1200:]}"
            rid = "R-" + j["id"][2:]
            if plain:
                spawn(rid, "redesign",
                      f"The system has asked you to revise the operating plan, at {unit} {period} of {horizon}. Diagnosis {j['id']} "
                      f"(swarm/audits/{j['id']}.md) says what is going wrong and why; the system's charts are in swarm/charts.md and the "
                      f"current plan is swarm/plan.md. Change the plan to address it. Before changing swarm/plan.md, copy the old version to "
                      f"swarm/history/ with a version number; keep the current plan at swarm/plan.md. Then write a short record of the change "
                      f"to swarm/audits/{rid}.md. Reply with the change in under 150 words.", budgets.get("redesign", 1.5), 25, {"after": j["id"]})
                continue
            spawn(rid, "redesign",
                  f"Use the obm-swarm-designer skill in REDESIGN mode, invoked by the system at {unit} {period} of {horizon} of the work the swarm in "
                  f"swarm/ is doing. Diagnosis {j['id']} (swarm/audits/{j['id']}.md) says what is going wrong and why. The system's charts "
                  f"(swarm/charts.md: limits computed from the data, signals, gap to the exemplar) and the driver tree in swarm/spec.md show "
                  f"where. First ask whether the direction is right, then make the smallest design change that addresses the cause: which "
                  f"driver to push on, a criterion, a rule or brief, or the tree itself. The goal is the human's: never lower it or an aim. "
                  f"State a prediction in the record: which tree measure should shift, in which direction, by which {unit}; the charts will "
                  f"show whether it did. Never change anything in a way that stops the core work. Before changing swarm/spec.md "
                  f"or a rule file, copy the old version to swarm/history/ with its version number; keep the current version at its usual path "
                  f"so every role keeps reading it. Then write the redesign record to "
                  f"swarm/audits/{rid}.md. Reply with the change in under 150 words.", budgets.get("redesign", 1.5), 25, {"after": j["id"]})
            continue
        af = sw / "audits" / f"{j['id']}.md"
        report = af.read_text() if af.exists() else (r.get("result") or "(no report)")
        label = "full audit" if j["kind"] == "audit" else "pulse review"
        handoff += (f"\n\nSYSTEM CADENCE: {label} {j['id']} reviewed the work as of {unit} {j['period']} (swarm/audits/{j['id']}.md). "
                    f"Act on it this {unit} and log what you did.\n\n{report[-3500:]}")
        if "diagnosis needed: yes" in report.lower():
            busy = any(p.get("kind") in ("diagnosis", "redesign") for p in mem["pending"] + new_jobs)
            since = max(mem.get("last_diagnosis", -10**6), mem.get("last_adopted", -10**6))
            if not busy and period - since >= gap:
                mem["last_diagnosis"] = period
                did = f"D-{j['id']}"
                if plain:
                    spawn(did, "diagnosis",
                          f"The system has asked you to find out what is going wrong, because review {j['id']} (swarm/audits/{j['id']}.md) "
                          f"asked for a closer look, at {unit} {period} of {horizon}. The system's charts are in swarm/charts.md and the plan in "
                          f"swarm/plan.md. Find what is going wrong and why. Do not change the plan; it will be revised from what you find. "
                          f"Write swarm/audits/{did}.md and reply with it in under 200 words.", budgets.get("diagnosis", 1.0), 20, {"after": j["id"]})
                else:
                    spawn(did, "diagnosis",
                          f"Use the obm-swarm-diagnostician skill, invoked by the system because {label} {j['id']} (swarm/audits/{j['id']}.md) says a "
                          f"diagnosis is needed, at {unit} {period} of {horizon}. Charts (limits computed by the system): swarm/charts.md; the driver "
                          f"tree: swarm/spec.md. Walk the tree from the top measure down to the driver that moved, then find why. Do not write a fix or change any rule, spec or KPI: the designer will "
                          f"redesign from your diagnosis. Write swarm/audits/{did}.md and reply with it in under 200 words.",
                          budgets.get("diagnosis", 1.0), 20, {"after": j["id"]})
                handoff += f"\n\nSYSTEM CADENCE: a diagnosis of this finding has started; it and the designer's redesign will be handed to you when ready."
            else:
                handoff += (f"\n\nSYSTEM CADENCE: no redesign now: one is in progress or was adopted less than {gap} {unit}s ago "
                            f"(last adopted at {unit} {mem.get('last_adopted', 'none')}), so its effect cannot be judged yet. Use the pivots above instead.")
                log.write(json.dumps({"t": time.time(), "period": period, "event": "diagnosis_deferred", "after": j["id"]}) + "\n")
    mem["pending"] = still + new_jobs; new_jobs = []

    # 2. Start a new review if one is due and none is still running.
    if not over and (full_due or fired or pulse_due) and not any(j["kind"] in ("pulse", "audit") for j in mem["pending"]):
        (sw / "audits").mkdir(exist_ok=True)
        why = f"because a signal fired: {fired}" if fired else "on its schedule"
        common = (f"at {unit} {period} of {horizon} of the work the swarm in swarm/ is doing. You cannot act on the work itself; review the "
                  f"records. The ground-truth measures (swarm/metrics_system.md) and charts (swarm/charts.md) are written by the system every {unit}, never by an agent.")
        if plain:
            common = (f"at {unit} {period} of {horizon} of operating the business. You cannot act on the business; review the records. "
                      f"The measures (swarm/metrics_system.md) and charts (swarm/charts.md) are written by the system every {unit}. The "
                      f"operating plan is swarm/plan.md and the operator's notes are in the current folder.")
            tail = (f"then a last line exactly 'Diagnosis needed: yes' or 'Diagnosis needed: no' (yes when something is going wrong "
                    f"that needs a closer look).")
            if full_due or fired:
                mem["n_audit"] += 1; mem["last_audit"] = period; aid = f"A-{mem['n_audit']:03d}"
                spawn(aid, "audit", f"The system has asked for a full review of how the business is going ({why}). This is review {aid}, "
                      f"{common} Write swarm/audits/{aid}.md: findings first, then at most three concrete actions for the operator, {tail}",
                      budgets.get("audit", 1.5), 30, {"trigger": fired or "scheduled"})
            else:
                mem["n_pulse"] += 1; mem["last_pulse"] = period; aid = f"P-{mem['n_pulse']:03d}"
                spawn(aid, "pulse", f"The system has asked for a short check on how the business is going. This is check {aid}, {common} "
                      f"Write swarm/audits/{aid}.md in under 250 words: how it is going, then at most three changes the operator can make now, {tail}",
                      budgets.get("pulse", 0.6), 12, {"trigger": "scheduled"})
        else:
            if full_due or fired:
                mem["n_audit"] += 1; mem["last_audit"] = period; aid = f"A-{mem['n_audit']:03d}"
                spawn(aid, "audit", f"Use the obm-swarm-auditor skill for a FULL AUDIT, invoked by the system ({why}). This is audit {aid}, {common} Judge "
                      f"the outcome first: are the goal's main measures moving toward it, is capacity in use, is anything declining, has a target become "
                      f"a ceiling? Read swarm/charts.md (limits computed by the system from the data, signals, gap to the exemplar) against the driver tree in swarm/spec.md. Is the direction right: does the tree add up to the goal, and are its drivers the ones that move it? Did each redesign's predicted shift appear on the charts by its date? Did any redesign lower the goal or an aim? Then whether earlier findings were acted on, then whether the records are current. Never tell the "
                      f"orchestrator to pause its core work to fix records. Write swarm/audits/{aid}.md: findings first, then at most three concrete "
                      f"actions for the orchestrator, then a last line exactly 'Diagnosis needed: yes' or 'Diagnosis needed: no'.",
                      budgets.get("audit", 1.5), 30, {"trigger": fired or "scheduled"})
            else:
                mem["n_pulse"] += 1; mem["last_pulse"] = period; aid = f"P-{mem['n_pulse']:03d}"
                spawn(aid, "pulse", f"Use the obm-swarm-auditor skill for a PULSE REVIEW, invoked by the system on its schedule. This is pulse {aid}, "
                      f"{common} Read only swarm/charts.md (limits computed by the system), the driver tree in swarm/spec.md and the last lines of the "
                      f"orchestrator's log. Answer: which measures show a signal and which only routine variation (never react to routine variation); what changed since the last pulse, and why; is anything heading the wrong way. Write "
                      f"swarm/audits/{aid}.md in under 250 words: the answers, then at most three pivots the orchestrator can make now (never a "
                      f"pause of its core work), then a last line exactly 'Diagnosis needed: yes' or 'Diagnosis needed: no'. A pulse answers 'yes' "
                      f"when a chart signals a change in the wrong direction, when a redesign's predicted shift has not appeared by its date, or when "
                      f"the gap to the exemplar is above 2 and no measure has signalled an improvement in the last 30 {unit}s. Otherwise 'no'.", budgets.get("pulse", 0.6), 12, {"trigger": "scheduled"})
        mem["pending"] += new_jobs
        log.write(json.dumps({"t": time.time(), "period": period, "event": "started", "id": aid}) + "\n")
    handoff = handoff.strip()
    mem_p.write_text(json.dumps(mem)); log.close()
    if handoff:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": cfg.get("hook_event", "PostToolUse"), "additionalContext": handoff}}))

if __name__ == "__main__":
    main()
