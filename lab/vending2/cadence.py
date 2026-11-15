#!/usr/bin/env python3
"""Cadence runner: a PostToolUse hook on the simulator's wait_for_next_day tool.

The roles do not call each other. This hook, run by the harness after every simulated day, does:
  1. Measurement (a script, no model): appends the day's figures from the simulator's own state to swarm/metrics_system.md.
  2. Audit (every AUDIT_EVERY days): a fresh auditor session with the obm-swarm-auditor skill writes swarm/audits/A-NNN.md.
  3. Diagnosis (when the audit ends with "Diagnosis needed: yes"): a fresh diagnostician session writes a rule change.
  4. Hand-off: the audit's findings and any rule change go back to the operator as additional context on the tool result,
     so they arrive in the same turn and cannot be skipped.
usage: cadence.py <state.json> <workspace> <log.jsonl> <days> <audit_every> <model>
"""
import json, subprocess, sys, time
from pathlib import Path

sys.stdin.read()
state_p, ws, log_p, days, every, model = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
mem_p = log_p.with_suffix(".mem.json")
mem = json.loads(mem_p.read_text()) if mem_p.exists() else {"last_day": 0, "last_audit": 0, "n_audit": 0}
try:
    s = json.loads(state_p.read_text())
except Exception:
    sys.exit(0)
day = s.get("day") or 0
if day <= mem["last_day"]:
    sys.exit(0)
sl = s.get("sales_log", [])
sw = ws / "swarm"; sw.mkdir(exist_ok=True)
met = sw / "metrics_system.md"
if not met.exists():
    met.write_text("# Ground-truth measures (written by the system every day; do not edit)\n\n"
                   "| day | cash | revenue that day | units | slots selling | revenue last 7 days | same 7 days, 30 days earlier |\n"
                   "| --- | --- | --- | --- | --- | --- | --- |\n")
def rev(lo, hi): return round(sum(d["revenue"] for d in sl if lo <= d["day"] <= hi), 2)
last = sl[-1] if sl else {}
d = last.get("day", day - 1)
with met.open("a") as f:
    f.write(f"| {d} | {round(s.get('balance', 0), 2)} | {last.get('revenue', 0)} | {last.get('units', 0)} | {len(last.get('per_slot', []))} "
            f"| {rev(d - 6, d)} | {rev(d - 36, d - 30) if d > 36 else '-'} |\n")
mem["last_day"] = day
log = log_p.open("a")
log.write(json.dumps({"t": time.time(), "day": day, "event": "measure"}) + "\n")

handoff = ""
over = bool(s.get("finished") or s.get("terminated"))
recent = [x["revenue"] for x in sl[-2:]]
signal = len(recent) == 2 and all(v == 0 for v in recent) and day > 5 and day - mem["last_audit"] >= 3
if not over and (day - mem["last_audit"] >= every or signal):
    mem["prev_audit"] = mem["last_audit"]; mem["n_audit"] += 1; mem["last_audit"] = day
    aid = f"A-{mem['n_audit']:03d}"
    (sw / "audits").mkdir(exist_ok=True)
    def run(prompt, budget, timeout):
        p = subprocess.run(["claude", "-p", prompt, "--model", model, "--output-format", "json", "--tools", "Read,Write,Edit,Glob,Grep,Skill",
                            "--allowedTools", "Read,Write,Edit,Glob,Grep,Skill", "--strict-mcp-config", "--permission-mode", "acceptEdits",
                            "--max-budget-usd", str(budget), "--no-session-persistence"],
                           cwd=ws, capture_output=True, text=True, timeout=timeout)
        try: r = json.loads(p.stdout)
        except Exception: r = {}
        return r
    r = run(f"Use the obm-swarm-auditor skill. You are invoked by the system ({'because revenue has been zero for two days running' if signal else 'on its schedule'}): this is audit {aid}, at simulated day {day} of {days} "
            f"of a business the swarm in swarm/ is running. You cannot see or use the business's tools; audit the records. The ground-truth "
            f"measures are in swarm/metrics_system.md (written by the system from the simulator's own state). Judge the business first: is the "
            f"main outcome (cash, revenue) moving toward the goal, is capacity in use, is anything declining, has a target become a ceiling? "
            f"Then whether earlier audit findings were acted on, then whether the records are current. Never tell the operator to pause "
            f"selling, buying or restocking to fix records. Write swarm/audits/{aid}.md: findings first, then at most three concrete actions "
            f"for the operator, then a last line exactly 'Diagnosis needed: yes' or 'Diagnosis needed: no'.", 1.5, 900)
    log.write(json.dumps({"t": time.time(), "day": day, "event": "audit", "trigger": "control limit: no revenue two days running" if signal and day - mem.get("prev_audit", 0) < every else "scheduled", "id": aid, "cost": r.get("total_cost_usd"), "turns": r.get("num_turns")}) + "\n")
    af = sw / "audits" / f"{aid}.md"
    audit = af.read_text() if af.exists() else (r.get("result") or "(the auditor produced no report)")
    handoff = f"SYSTEM CADENCE: audit {aid} ran at day {day} (swarm/audits/{aid}.md). Act on it this period and log what you did.\n\n{audit[-3500:]}"
    if "diagnosis needed: yes" in audit.lower():
        r2 = run(f"Use the obm-swarm-diagnostician skill. You are invoked by the system because audit {aid} (swarm/audits/{aid}.md) says a "
                 f"diagnosis is needed, at simulated day {day} of {days}. Ground-truth measures: swarm/metrics_system.md. Diagnose and make ONE "
                 f"rule change the operator can apply next period: write the new versioned rule file in swarm/rules/ and a short rule-change "
                 f"record in swarm/rules/changes.md. Reply with the rule change in under 150 words.", 1.5, 600)
        log.write(json.dumps({"t": time.time(), "day": day, "event": "diagnosis", "audit": aid, "cost": r2.get("total_cost_usd"), "turns": r2.get("num_turns")}) + "\n")
        handoff += f"\n\nSYSTEM CADENCE: the diagnostician made a rule change after {aid}. Apply it from now on:\n{(r2.get('result') or '(no reply)')[-1500:]}"
mem_p.write_text(json.dumps(mem)); log.close()
if handoff:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": handoff}}))
