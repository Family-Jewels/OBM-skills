"""System hook (PostToolUse on the task's tools): log each action the worker takes, with the task's clock after it, for
the fact register and the pursuit measure (facts.py). Generic: the adapter only supplies action_clock() -> (period, clock).
Usage: action_hook.py <engine config.json>; the hook's JSON input arrives on stdin. Never fails the tool call."""
import importlib, json, sys
from pathlib import Path
try:
    cfg = json.loads(Path(sys.argv[1]).read_text())
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    tool = json.loads(sys.stdin.read() or "{}").get("tool_name", "")
    mod, cls = cfg["adapter"].split(":")
    a = getattr(importlib.import_module(mod), cls)(**cfg.get("adapter_args", {}))
    period, clock = a.action_clock()
    if tool and period is not None and clock is not None:
        with open(cfg["action_log"], "a") as f:
            f.write(json.dumps({"tool": tool, "period": period, "clock": clock}) + "\n")
except Exception:
    pass
print("{}")
