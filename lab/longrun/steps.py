"""The movement cycle, recorded by the system: one line per tool call, and the behaviour measures and cues built from it.

Every finding about extra behaviour in the runs to date (re-reading, retrying, narrating, logs in the wrong place, stalls)
had to be inferred from cost, because no run kept a step-level record and the worker's own logs stopped or bloated. This
module is written by a hook, never by the agent, so it cannot extinguish or grow with the agent's habits.

Each step record: {"i", "t", "tool", "kind", "target", "sig", "ok", "out", "hash", "bytes_in"}.
  kind:   read | write | run | task_read | task_act | agent | skill | other
  sig:    hash of the tool and its canonical input (the same call made again has the same sig)
  hash:   content hash of a file read (so an unchanged re-read can be told from a read of a changed file)

Cues are the ranking signals from the design discussion, given to the agent as antecedents rather than computed by it:
  freshness   a file read again with nothing changed since the last read: use what you read
  diversity   the same call failing again with the same input: change the input, the route, or record a block
  relevance   many steps with no state-changing action: the next one should change state toward the goal, or record a block
  placement   a write outside the workspace roots: records belong at their protocol paths
  economy     the agent's own logs growing past their budget: one line per event
Each cue fires once, when its condition starts (a change of state), like every trigger in the cadence engine.
"""
import fnmatch, hashlib, json, os, time
from pathlib import Path

READ_TOOLS = {"Read", "Glob", "Grep", "NotebookRead", "WebFetch", "WebSearch", "LS"}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
READ_ONLY_TASK = ["get_*", "list_*", "check_*", "read_*", "search_*", "view_*", "query_*", "fetch_*", "describe_*"]
READ_ONLY_SHELL = {"cat", "head", "tail", "less", "more", "ls", "grep", "rg", "find", "wc", "echo", "pwd", "stat", "file", "du", "df",
                   "diff", "cmp", "tree", "which", "date", "env", "printenv", "git-log"}

DEFAULTS = {"no_progress_steps": 20, "repeat_failures": 2, "window": 50, "log_bytes_per_window": 8000, "health_every": 25,
            "workspace_roots": [], "own_logs": [], "read_only_task_tools": READ_ONLY_TASK}

def _canon(x):
    return json.dumps(x, sort_keys=True, default=str)

def classify(tool, inp, cfg=None):
    """(kind, target) for a tool call. Task tools are any MCP tools; read-only ones are named by patterns."""
    cfg = cfg or DEFAULTS
    inp = inp if isinstance(inp, dict) else {}
    if tool in READ_TOOLS:
        return "read", str(inp.get("file_path") or inp.get("path") or inp.get("pattern") or inp.get("url") or inp.get("query") or "")[:200]
    if tool in WRITE_TOOLS:
        return "write", str(inp.get("file_path") or inp.get("notebook_path") or "")[:200]
    if tool == "Bash":
        cmd = str(inp.get("command") or "").strip()
        first = os.path.basename(cmd.split()[0]) if cmd.split() else ""
        return ("read" if first in READ_ONLY_SHELL else "run"), " ".join(cmd.split()[:3])[:120]
    if tool in ("Agent", "Task"):
        return "agent", str(inp.get("subagent_type") or inp.get("description") or "")[:120]
    if tool == "Skill":
        return "skill", str(inp.get("skill") or "")[:120]
    if tool.startswith("mcp__"):
        name = tool.split("__")[-1]
        ro = any(fnmatch.fnmatch(name, p) for p in cfg.get("read_only_task_tools", READ_ONLY_TASK))
        return ("task_read" if ro else "task_act"), name
    return "other", tool[:120]

def failed(resp):
    """Best-effort reading of a tool response as failed. Unknown shapes count as success, so a cue never rests on a guess."""
    if isinstance(resp, dict):
        if resp.get("is_error") or resp.get("error") or resp.get("interrupted"):
            return True
        code = resp.get("exit_code", resp.get("returncode"))
        return isinstance(code, int) and code != 0
    if isinstance(resp, str):
        head = resp.lstrip()[:200].lower()
        return head.startswith(("error", "tool_use_error", "<tool_use_error>")) or "permission denied" in head
    return False

def file_hash(path):
    try:
        p = Path(path)
        if p.is_file():
            return hashlib.sha256(p.read_bytes()[:4_000_000]).hexdigest()[:16]
    except OSError:
        pass
    return None

def make_record(i, tool, inp, resp, cfg=None):
    kind, target = classify(tool, inp, cfg)
    rec = {"i": i, "t": round(time.time(), 3), "tool": tool, "kind": kind, "target": target,
           "sig": hashlib.sha256((tool + _canon(inp)).encode()).hexdigest()[:12], "ok": not failed(resp),
           "out": len(_canon(resp)) if resp is not None else 0}
    if tool == "Read" and isinstance(inp, dict) and inp.get("file_path"):
        rec["hash"] = file_hash(inp["file_path"])
    if kind == "write" and isinstance(inp, dict):
        rec["bytes_in"] = len(str(inp.get("content") or inp.get("new_string") or inp.get("new_source") or ""))
    return rec

def _inside(path, roots):
    if not roots or not path:
        return True
    ap = os.path.abspath(path)
    return any(ap == os.path.abspath(r) or ap.startswith(os.path.abspath(r).rstrip(os.sep) + os.sep) for r in roots)

def _own_log(path, logs):
    return bool(path) and any(os.path.abspath(path).endswith(os.path.normpath(l)) for l in logs)

def new_state():
    return {"n": 0, "reads": {}, "fail_run": {}, "last_sig": None, "since_progress": 0, "max_since_progress": 0,
            "log_bytes": [], "fired": {}, "counts": {}, "rereads": 0, "repeat_failures": 0, "retries_unchanged": 0,
            "stray": [], "own_log_bytes": 0, "progress_steps": 0, "failures": 0}

def update(state, rec, cfg=None):
    """Fold one step into the running state; return the cues that start at this step (each fires once per condition)."""
    cfg = {**DEFAULTS, **(cfg or {})}
    s, cues = state, []
    s["n"] += 1
    s["counts"][rec["kind"]] = s["counts"].get(rec["kind"], 0) + 1
    fired = s["fired"]
    # freshness: an unchanged re-read
    if rec["tool"] == "Read" and rec.get("hash"):
        prev = s["reads"].get(rec["target"])
        if prev == rec["hash"]:
            s["rereads"] += 1
            key = f"reread:{rec['target']}:{rec['hash']}"
            if key not in fired:
                fired[key] = s["n"]
                cues.append(f"{rec['target']} has not changed since you last read it: use what you read.")
        s["reads"][rec["target"]] = rec["hash"]
    if rec["kind"] == "write" and rec["target"] in s["reads"]:
        s["reads"].pop(rec["target"], None)  # the agent changed it; the next read is not a re-read
    # diversity: the same call failing again
    if not rec["ok"]:
        s["failures"] += 1
        if s.get("last_sig") == rec["sig"] and s.get("last_ok") is False:
            s["retries_unchanged"] += 1
        run = s["fail_run"].get(rec["sig"], 0) + 1
        s["fail_run"][rec["sig"]] = run
        if run >= cfg["repeat_failures"]:
            s["repeat_failures"] += 1
            key = f"fail:{rec['sig']}"
            if key not in fired:
                fired[key] = s["n"]
                cues.append(f"{rec['tool']} {rec['target']} has failed {run} times with the same input. Change the input, "
                            f"take another route, or record a block with the smallest step that would unblock it.")
    else:
        s["fail_run"].pop(rec["sig"], None)
    s["last_sig"], s["last_ok"] = rec["sig"], rec["ok"]
    # relevance: steps since the last successful state change (a write, an acting task call, a run)
    progress = rec["ok"] and rec["kind"] in ("write", "task_act", "run", "agent")
    if progress and not _own_log(rec["target"], cfg["own_logs"]):
        s["since_progress"] = 0; s["progress_steps"] += 1
        fired.pop("stall", None)
    else:
        s["since_progress"] += 1
        s["max_since_progress"] = max(s["max_since_progress"], s["since_progress"])
        if s["since_progress"] >= cfg["no_progress_steps"] and "stall" not in fired:
            fired["stall"] = s["n"]
            cues.append(f"{s['since_progress']} steps with no state-changing action. The next step should change something "
                        f"toward the goal (the constraint first), or record a block.")
    # placement: writes outside the workspace
    if rec["kind"] == "write" and not _inside(rec["target"], cfg["workspace_roots"]):
        if rec["target"] not in s["stray"]:
            s["stray"].append(rec["target"])
            cues.append(f"You wrote {rec['target']}, outside the workspace ({', '.join(cfg['workspace_roots'])}). "
                        f"Records belong at their protocol paths.")
    # economy: the agent's own logs
    if rec["kind"] == "write" and _own_log(rec["target"], cfg["own_logs"]):
        b = rec.get("bytes_in", 0)
        s["own_log_bytes"] += b
        s["log_bytes"] = (s["log_bytes"] + [[s["n"], b]])[-500:]
    recent = sum(b for n, b in s["log_bytes"] if n > s["n"] - cfg["window"])
    over = recent > cfg["log_bytes_per_window"]
    if over and "logsize" not in fired:
        fired["logsize"] = s["n"]
        cues.append(f"Your log grew {recent} bytes over the last {cfg['window']} steps. One line per event, under 300 "
                    f"characters; the system already records every step and every measure.")
    elif not over:
        fired.pop("logsize", None)
    return cues

def summarize(steps, cfg=None):
    """Behaviour measures for a whole step log (post-run analysis, or the health panel)."""
    s = new_state()
    cues = {"freshness": 0, "diversity": 0, "relevance": 0, "placement": 0, "economy": 0}
    for r in steps:
        for c in update(s, r, cfg):  # the same cues the hook would have handed over, by kind
            k = ("freshness" if "has not changed" in c else "diversity" if "with the same input" in c else
                 "relevance" if "no state-changing" in c else "placement" if "outside the workspace" in c else "economy")
            cues[k] += 1
    n = max(1, s["n"])
    tools = {}
    for r in steps:
        tools[r["tool"]] = tools.get(r["tool"], 0) + 1
    return {"steps": s["n"], "by_kind": s["counts"], "state_changing_share": round(s["progress_steps"] / n, 3),
            "unchanged_rereads": s["rereads"], "reread_share": round(s["rereads"] / n, 3), "failures": s["failures"],
            "repeat_failures": s["repeat_failures"], "retries_unchanged": s["retries_unchanged"],
            "longest_no_progress": s["max_since_progress"], "stray_writes": s["stray"], "own_log_bytes": s["own_log_bytes"],
            "cues": cues, "top_tools": sorted(tools.items(), key=lambda x: -x[1])[:8]}

def health_markdown(m):
    k = ", ".join(f"{a} {b}" for a, b in sorted(m["by_kind"].items(), key=lambda x: -x[1]))
    return ("## Step health (computed by the system from every tool call; the agent writes none of it)\n\n"
            f"- Steps: {m['steps']} ({k}); state-changing share {m['state_changing_share']:.0%}.\n"
            f"- Unchanged re-reads: {m['unchanged_rereads']} ({m['reread_share']:.0%} of steps).\n"
            f"- Failures: {m['failures']}; the same call failing again: {m['repeat_failures']}; retried unchanged: {m['retries_unchanged']}.\n"
            f"- Longest run of steps with no state change: {m['longest_no_progress']}.\n"
            f"- Writes outside the workspace: {', '.join(m['stray_writes']) or 'none'}.\n"
            f"- Bytes written to the agent's own logs: {m['own_log_bytes']}.\n"
            f"- Cues the step record raised (handed to the agent only in cue mode): "
            + ", ".join(f"{k} {v}" for k, v in m.get("cues", {}).items()) + ".\n"
            f"- Most-used tools: " + ", ".join(f"{t} {c}" for t, c in m["top_tools"]) + ".\n")

def load(path):
    out = []
    p = Path(path)
    if p.exists():
        for line in p.read_text().splitlines():
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "summarize":
        cfg = json.loads(Path(sys.argv[3]).read_text()) if len(sys.argv) > 3 else None
        m = summarize(load(sys.argv[2]), cfg)
        print(json.dumps(m, indent=1))
        print(health_markdown(m))
    else:
        print("usage: python3 -I steps.py summarize <steps.jsonl> [config.json]")
