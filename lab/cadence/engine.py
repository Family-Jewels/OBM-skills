#!/usr/bin/env python3
"""OBM cadence engine: the system, not the agents, invokes the roles on a schedule. Task-agnostic.

Run it as a hook that fires once per period of the work (for example, a PostToolUse hook on the tool that ends a period,
or a scheduler). Each time it runs:
  1. Measurement (no model): asks the task's adapter for this period's ground-truth measures and appends them to
     swarm/metrics_system.md.
  2. Pulse review every `pulse_every` periods: a short auditor review of the numbers, ending in at most three pivots.
  3. Full audit every `audit_every` periods, or at once when a signal rule fires (a measure out of its limits).
  4. Diagnosis when a pulse or audit ends with "Diagnosis needed: yes".
  5. Hand-off: findings and any rule change go back to the orchestrator as additional context on the hook's event.

usage: engine.py <config.json>      (reads the hook's JSON on stdin and ignores it)
Config keys: workspace, log, adapter ("module.path:Class"), adapter_args, unit ("day", "cycle", ...), horizon,
pulse_every, audit_every, min_periods_between_diagnoses (default 21: a rule must have time to show its effect),
signals ([{measure, op, value, periods, label, not_before, min_gap}]), model, hook_event (default PostToolUse),
budgets ({pulse, audit, diagnosis} in USD).
"""
import importlib, json, operator, subprocess, sys, time
from pathlib import Path

OPS = {"==": operator.eq, "<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge, "!=": operator.ne}

def main():
    sys.stdin.read()
    cfg = json.loads(Path(sys.argv[1]).read_text())
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
    log = log_p.open("a")
    log.write(json.dumps({"t": time.time(), "period": period, "event": "measure"}) + "\n")

    fired = None
    for s in cfg.get("signals", []):
        if period < s.get("not_before", 0):
            continue
        last = [h.get(s["measure"]) for h in mem["history"][-s.get("periods", 1):]]
        if len(last) == s.get("periods", 1) and all(v is not None and OPS[s["op"]](v, s["value"]) for v in last):
            if period - max(mem["last_audit"], mem["last_pulse"]) >= s.get("min_gap", 3):
                fired = s.get("label", f"{s['measure']} {s['op']} {s['value']}"); break
    full_due = period - mem["last_audit"] >= cfg.get("audit_every", 30)
    pulse_due = period - max(mem["last_pulse"], mem["last_audit"]) >= cfg.get("pulse_every", 7)
    handoff = ""
    if not over and (full_due or fired or pulse_due):
        (sw / "audits").mkdir(exist_ok=True)
        budgets = cfg.get("budgets", {}); model = cfg.get("model", "claude-haiku-5-5"); horizon = cfg.get("horizon", "?")
        def run(prompt, budget, timeout, turns):
            p = subprocess.run(["claude", "-p", prompt, "--model", model, "--output-format", "json", "--max-turns", str(turns), "--tools", "Read,Write,Edit,Glob,Grep,Skill",
                                "--allowedTools", "Read,Write,Edit,Glob,Grep,Skill", "--strict-mcp-config", "--permission-mode", "acceptEdits",
                                "--max-budget-usd", str(budget), "--no-session-persistence"], cwd=ws, capture_output=True, text=True, timeout=timeout)
            try: return json.loads(p.stdout)
            except Exception: return {}
        why = f"because a signal fired: {fired}" if fired else "on its schedule"
        common = (f"at {unit} {period} of {horizon} of the work the swarm in swarm/ is doing. You cannot act on the work itself; review the "
                  f"records. The ground-truth measures are in swarm/metrics_system.md, written by the system every {unit}, never by an agent.")
        if full_due or fired:
            mem["n_audit"] += 1; mem["last_audit"] = period; kind, aid = "audit", f"A-{mem['n_audit']:03d}"
            r = run(f"Use the obm-swarm-auditor skill for a FULL AUDIT, invoked by the system ({why}). This is audit {aid}, {common} Judge the "
                    f"outcome first: are the goal's main measures moving toward it, is capacity in use, is anything declining, has a target become "
                    f"a ceiling? Then whether earlier pulse and audit findings were acted on, then whether the records are current. Never tell the "
                    f"orchestrator to pause its core work to fix records. Write swarm/audits/{aid}.md: findings first, then at most three concrete "
                    f"actions for the orchestrator, then a last line exactly 'Diagnosis needed: yes' or 'Diagnosis needed: no'.",
                    budgets.get("audit", 1.5), 600, 30)
        else:
            mem["n_pulse"] += 1; mem["last_pulse"] = period; kind, aid = "pulse", f"P-{mem['n_pulse']:03d}"
            r = run(f"Use the obm-swarm-auditor skill for a PULSE REVIEW, invoked by the system on its schedule. This is pulse {aid}, {common} "
                    f"Read only swarm/metrics_system.md, the targets in swarm/spec.md and the last lines of the orchestrator's log. Answer: are "
                    f"the numbers moving toward the goal; what changed since the last pulse, and why; is anything heading the wrong way. Write "
                    f"swarm/audits/{aid}.md in under 250 words: the answers, then at most three pivots the orchestrator can make now (never a "
                    f"pause of its core work), then a last line exactly 'Diagnosis needed: yes' or 'Diagnosis needed: no'. A pulse answers 'yes' only "
                    f"when the same problem appears in this pulse and the one before it (read the last pulse in swarm/audits/); a problem seen "
                    f"once gets a pivot, not a rule change.", budgets.get("pulse", 0.6), 240, 12)
        log.write(json.dumps({"t": time.time(), "period": period, "event": kind, "trigger": fired or "scheduled", "id": aid,
                              "cost": r.get("total_cost_usd"), "turns": r.get("num_turns")}) + "\n")
        af = sw / "audits" / f"{aid}.md"
        report = af.read_text() if af.exists() else (r.get("result") or "(no report)")
        label = "full audit" if kind == "audit" else "pulse review"
        handoff = f"SYSTEM CADENCE: {label} {aid} ran at {unit} {period} (swarm/audits/{aid}.md). Act on it this {unit} and log what you did.\n\n{report[-3500:]}"
        gap = cfg.get("min_periods_between_diagnoses", 21)
        diag_ok = period - mem.get("last_diagnosis", -10**6) >= gap
        if "diagnosis needed: yes" in report.lower() and not diag_ok:
            handoff += (f"\n\nSYSTEM CADENCE: no new rule change this {unit}: the last one was made at {unit} {mem['last_diagnosis']} and "
                        f"needs {gap} {unit}s before its effect can be judged. Use the pivots above instead.")
            log.write(json.dumps({"t": time.time(), "period": period, "event": "diagnosis_deferred", "after": aid}) + "\n")
        if "diagnosis needed: yes" in report.lower() and diag_ok:
            mem["last_diagnosis"] = period
            r2 = run(f"Use the obm-swarm-diagnostician skill, invoked by the system because {label} {aid} (swarm/audits/{aid}.md) says a diagnosis "
                     f"is needed, at {unit} {period} of {horizon}. Ground-truth measures: swarm/metrics_system.md. Make ONE rule change the "
                     f"orchestrator can apply next {unit}: write the new versioned rule file in swarm/rules/ and a short rule-change record in "
                     f"swarm/rules/changes.md. Reply with the rule change in under 150 words.", budgets.get("diagnosis", 1.5), 400, 20)
            log.write(json.dumps({"t": time.time(), "period": period, "event": "diagnosis", "after": aid, "cost": r2.get("total_cost_usd"),
                                  "turns": r2.get("num_turns")}) + "\n")
            handoff += f"\n\nSYSTEM CADENCE: the diagnostician made a rule change after {aid}. Apply it from now on:\n{(r2.get('result') or '(no reply)')[-1500:]}"
    mem_p.write_text(json.dumps(mem)); log.close()
    if handoff:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": cfg.get("hook_event", "PostToolUse"), "additionalContext": handoff}}))

if __name__ == "__main__":
    main()
