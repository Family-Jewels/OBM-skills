"""PostToolUse hook for every tool: append the step to the system's step log, update the behaviour state, and hand the
agent any cue that starts at this step. Written by the system; the agent cannot edit what it records about itself if the
step log sits in a protected path. Never fails or blocks the tool call.

usage (in the hooks settings, matcher ".*"):  python3 -I steps_hook.py <config.json>     (hook JSON arrives on stdin)

config.json: {"steps_log": "<path>/steps.jsonl", "health_md": "<path>/step_health.md", "workspace_roots": ["<abs path>"],
              "own_logs": ["swarm/log/progress.md"], "no_progress_steps": 20, "repeat_failures": 2, "window": 50,
              "log_bytes_per_window": 8000, "health_every": 25, "hook_event": "PostToolUse"}
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

def main():
    out = {}
    try:
        cfg = json.loads(Path(sys.argv[1]).read_text())
        ev = json.loads(sys.stdin.read() or "{}")
        tool = ev.get("tool_name") or ""
        if not tool:
            return out
        import fcntl, steps
        log = Path(cfg["steps_log"]); log.parent.mkdir(parents=True, exist_ok=True)
        st_p = log.with_suffix(".state.json")
        with open(log.with_suffix(".lock"), "w") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)  # parallel tool calls run their hooks at the same time
            state = json.loads(st_p.read_text()) if st_p.exists() else steps.new_state()
            rec = steps.make_record(state["n"] + 1, tool, ev.get("tool_input"), ev.get("tool_response"), cfg)
            with log.open("a") as f:
                f.write(json.dumps(rec) + "\n")
            cues = steps.update(state, rec, cfg)
            st_p.write_text(json.dumps(state))
            if cfg.get("health_md") and state["n"] % int(cfg.get("health_every", 25)) == 0:
                Path(cfg["health_md"]).write_text(steps.health_markdown(steps.summarize(steps.load(log), cfg)))
        if cues and cfg.get("cues", True):  # "cues": false records without intervening (an observation-only arm)
            out = {"hookSpecificOutput": {"hookEventName": cfg.get("hook_event", "PostToolUse"),
                                          "additionalContext": "SYSTEM STEP CUES: " + " ".join(cues[:2])}}
    except Exception:
        out = {}
    return out

if __name__ == "__main__":
    print(json.dumps(main()))
