#!/usr/bin/env python3
"""Stop gate (Claude Code Stop hook).

The agent cannot end its session until the done check passes, run by the harness
against the pristine tests (so editing tests does not help). Optional honest exits:
a block report in BLOCKED.md opens the gate. A cap on stop attempts always opens it.

Config via env: GATE_MODE = none | strict | exits ; GATE_CAP (default 6);
GATE_PRISTINE = folder holding the original tests/ ; GATE_LOG = jsonl path.
"""
import json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

inp = json.load(sys.stdin)
cwd = Path(inp.get("cwd") or os.getcwd())
mode = os.environ.get("GATE_MODE", "exits"); cap = int(os.environ.get("GATE_CAP", "6"))
pristine = Path(os.environ["GATE_PRISTINE"]); log = Path(os.environ["GATE_LOG"])
state_f = log.with_suffix(".state.json")
state = json.loads(state_f.read_text()) if state_f.exists() else {"attempts": 0}
state["attempts"] += 1

def done(outcome, allow, reason=""):
    state["last"] = outcome; state_f.write_text(json.dumps(state))
    with log.open("a") as f:
        f.write(json.dumps({"t": time.time(), "attempt": state["attempts"], "outcome": outcome, "allow": allow}) + "\n")
    if not allow:
        print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)

if mode == "none":
    done("no-gate", True)

# Run the done check on a copy of the work with the ORIGINAL tests.
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    for item in cwd.iterdir():
        if item.name in ("tests", ".git") or item.name.startswith("."):
            continue
        (shutil.copytree if item.is_dir() else shutil.copy2)(item, td / item.name)
    shutil.copytree(pristine / "tests", td / "tests")
    r = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", "-p", "no:cacheprovider", "--tb=no", "-rfE"],
                       cwd=td, capture_output=True, text=True, timeout=120)
    passed = r.returncode == 0
    full_out = r.stdout
    summary = "\n".join(l for l in r.stdout.splitlines() if l.startswith(("FAILED", "ERROR")) or " passed" in l or " failed" in l)[-4000:]

if passed:
    done("met", True)
if mode == "exits":
    b = cwd / "BLOCKED.md"
    if b.exists() and len(b.read_text().strip()) > 80:
        if os.environ.get("GATE_ACCOUNT") != "1":
            done("blocked", True)
        failing = re.findall(r"^(?:FAILED|ERROR) \S*?::(?:test_case\[)?([\w\-]+)\]?", full_out, re.M)
        missing = [f for f in failing if f not in b.read_text()]
        if not missing:
            done("blocked", True)
        account_note = f" BLOCKED.md must account for every failing test; it does not mention: {', '.join(missing[:15])}."
if state["attempts"] >= cap:
    done("cap", True)

account_note = locals().get("account_note", "")
msg = f"Not done yet. The done check (the original tests in tests/, run by the harness) does not pass:\n{summary}\nKeep working until it passes."
if mode == "exits":
    msg += (" If you have evidence that the task cannot be completed as specified, write BLOCKED.md in the working"
            " directory: what is impossible, the evidence, and what would unblock it. That ends the session as a"
            " valid outcome." + account_note)
done("not-met", False, msg)
