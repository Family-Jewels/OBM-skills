#!/usr/bin/env python3
"""Stop gate: refuses to end the session before the simulation is over.
usage (as a Stop hook command): vb_stop_gate2.py <state.json> <gate_log.jsonl> <days> [cap]
Paths come as arguments, not environment variables, so the agent's own environment never holds the state path."""
import json, sys, time
from pathlib import Path
sys.stdin.read()
state_p, log, days = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
cap = int(sys.argv[4]) if len(sys.argv) > 4 else 40
cnt = log.with_suffix(".count"); n = int(cnt.read_text()) + 1 if cnt.exists() else 1; cnt.write_text(str(n))
try: s = json.loads(state_p.read_text())
except Exception: s = {}
over = bool(s.get("finished") or s.get("terminated"))
allow = over or n >= cap or not s
with log.open("a") as f:
    f.write(json.dumps({"t": time.time(), "attempt": n, "day": s.get("day"), "finished": s.get("finished"), "terminated": s.get("terminated"), "allow": allow}) + "\n")
if not allow:
    print(json.dumps({"decision": "block", "reason": f"The operation is not over: it is simulated day {s.get('day')} of {days}. "
        "Stopping now scores zero. Continue operating (use wait_for_next_day to advance) until the tools report SIMULATION OVER."}))
