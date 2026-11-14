#!/usr/bin/env python3
"""PreToolUse hook: deny writes to protected paths. PROTECTED = colon-separated path prefixes relative to cwd.
Logs every denial to PROTECT_LOG (jsonl). Bash is checked heuristically: a command that names a protected path
together with a write-like operation is denied. The final defence is the done check, which uses pristine copies."""
import json, os, re, sys, time
inp = json.load(sys.stdin)
cwd = os.path.realpath(inp.get("cwd") or os.getcwd())
prot = [os.path.realpath(os.path.join(cwd, p)) for p in os.environ.get("PROTECTED", "tests:fixtures").split(":") if p]
tool, ti = inp.get("tool_name"), inp.get("tool_input", {})
def hit(path):
    rp = os.path.realpath(path if os.path.isabs(path) else os.path.join(cwd, path))
    return any(rp == p or rp.startswith(p + os.sep) for p in prot)
deny = None
if tool in ("Write", "Edit", "NotebookEdit", "MultiEdit"):
    if hit(ti.get("file_path", "")): deny = ti.get("file_path")
elif tool == "Bash":
    cmd = ti.get("command", "")
    writey = re.search(r"(>|\btee\b|\bsed\s+-i|\brm\b|\bmv\b|\bcp\b|\btruncate\b|\bchmod\b|\bgit\s+(checkout|restore|apply|stash)|open\([^)]*['\"][wa])", cmd)
    names = [p for p in prot if os.path.relpath(p, cwd) in cmd or p in cmd]
    if writey and names: deny = f"bash: {cmd[:200]}"
if deny:
    log = os.environ.get("PROTECT_LOG")
    if log:
        with open(log, "a") as f: f.write(json.dumps({"t": time.time(), "tool": tool, "target": deny}) + "\n")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
        "permissionDecisionReason": "That path is protected: it holds the measuring instruments (tests, fixtures, criteria). "
        "Producers may not change it. If a test or fixture looks wrong, report it with your evidence instead."}}))
sys.exit(0)
