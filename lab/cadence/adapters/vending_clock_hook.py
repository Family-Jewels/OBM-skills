"""System hook (PreToolUse on wait_for_next_day): record how much of the working day the worker used, from the simulator's
own clock, before the day rolls over. Usage: vending_clock_hook.py <state.json> <clock log>. Never fails the tool call."""
import json, sys
try:
    s = json.loads(open(sys.argv[1]).read())
    with open(sys.argv[2], "a") as f:
        f.write(json.dumps({"day": s.get("day"), "minute": s.get("minute")}) + "\n")
except Exception:
    pass
print("{}")
