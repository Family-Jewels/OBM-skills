#!/usr/bin/env python3
"""Stop gate for the vending benchmark (Claude Code Stop hook).

Reads the simulator's own state file (outside the agent's tools) and refuses to let the
session end before the simulation is over. Honest exits: the business has ended (finished,
bankrupt or terminated), or a cap on refused stops is reached. The CLI's dollar cap also ends
the session regardless.

Env: VB_STATE (state.json path), VB_GATE_LOG (jsonl), VB_GATE_CAP (default 40).
"""
import json, os, sys, time
from pathlib import Path

sys.stdin.read()
state_p = Path(os.environ["VB_STATE"]); log = Path(os.environ["VB_GATE_LOG"])
cap = int(os.environ.get("VB_GATE_CAP", "40"))
cnt_p = log.with_suffix(".count")
n = int(cnt_p.read_text()) + 1 if cnt_p.exists() else 1
cnt_p.write_text(str(n))
try:
    s = json.loads(state_p.read_text())
except Exception as e:
    s = {}
day, horizon = s.get("day"), os.environ.get("VB_DAYS")
over = bool(s.get("finished") or s.get("terminated"))
allow = over or n >= cap or not s
with log.open("a") as f:
    f.write(json.dumps({"t": time.time(), "attempt": n, "day": day, "finished": s.get("finished"),
                        "terminated": s.get("terminated"), "allow": allow}) + "\n")
if not allow:
    print(json.dumps({"decision": "block", "reason":
        f"The operation is not over: it is simulated day {day}"
        + (f" of {horizon}" if horizon else "")
        + ". Stopping now scores zero. Continue operating (use wait_for_next_day to advance) until the tools report SIMULATION OVER."}))
sys.exit(0)
