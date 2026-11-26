"""Engine v1.1 on a made-up task (no vending): design loading, opportunities, hand-offs, execution-event reviews,
fact-checked guidance, the agent's own policies checked, diagnosis to redesign. Roles run as a stub (no model).
usage: python3 -I test_engine_v11.py"""
import json, subprocess, sys, tempfile, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
TMP = Path(tempfile.mkdtemp(prefix="v11-"))

(TMP / "fake_task.py").write_text('''
import json
from pathlib import Path
class Task:
    def __init__(self, state): self.p = Path(state)
    def spec(self):
        return {"unit": "round", "horizon": 40, "top": "score", "goal": {"type": "maximize", "value": 1000, "source": "a made-up best"},
                "measures": {"score": {"kind": "level", "better": "up"}, "made": {"kind": "flow", "better": "up"}},
                "resources": ["agent time", "benches"], "capacity": "agent time"}
    def read(self):
        s = json.loads(self.p.read_text())
        return {"period": s["round"], "over": s["round"] >= 40, "measures": {"score": 10 * s["round"], "made": s["round"] % 5},
                "resources": {"agent time": {"used": s.get("used", 30), "available": 100}, "benches": {"used": 2, "available": 5}}}
    def on_period_end(self):
        s = json.loads(self.p.read_text()); s["ended"] = s.get("ended", 0) + 1; self.p.write_text(json.dumps(s))
    def snapshot(self): return "| bench | busy |\\n| --- | --- |\\n| 1 | yes |\\n"
''')
# A stub role: writes the record the prompt asks for, as a model would, and prints a result line like claude -p.
(TMP / "stub_role.py").write_text('''
import json, re, sys
from pathlib import Path
p = sys.argv[1]
rec = re.search(r"swarm/(audits|checks)/([A-Z]-[A-Z0-9-]+)\\.md", p)
path = Path(rec.group(0)); path.parent.mkdir(parents=True, exist_ok=True); jid = rec.group(2)
if jid.startswith("C-"):
    lines = [f"Proposal: {x.strip()} | Verdict: accepted | Reason: the numbers hold" for x in re.findall(r"(swarm/guidance/proposed/[^,.\\s]+\\.md)", p)]
    if "Files the working agent changed" in p:
        lines.append('- **Statement:** "benches are never worth filling" | File: notes.md | Verdict: refuted | Evidence: made rose in rounds 5-9')
    path.write_text("\\n".join(lines) + "\\n")
elif jid.startswith("P-") or jid.startswith("A-"):
    Path("swarm/guidance/proposed").mkdir(parents=True, exist_ok=True)
    Path(f"swarm/guidance/proposed/{jid}-1.md").write_text("# Fill free benches early\\nApplies when: O1\\nWhat good looks like: free benches filled before the round ends\\nWhy: made rises\\nSource: " + jid + "\\nRevisit: round 30\\n")
    path.write_text(f"Summary: capacity was left unused.\\n\\nEnvironment change: proposed {jid}-1\\n**Diagnosis needed: " + ("yes" if jid == "P-001" else "no") + "**\\n")
elif jid.startswith("D-"):
    path.write_text("Summary: the agent never saw that benches were free.\\n")
else:
    Path("swarm/system.json").write_text(json.dumps({**json.loads(Path("swarm/system.json").read_text()), "charts": [{"name": "made", "better": "up"}]}))
    path.write_text("Summary: chart made only.\\nEnvironment change: charts\\n")
print(json.dumps({"total_cost_usd": 0.01, "num_turns": 2, "result": "done"}))
''')
ws = TMP / "ws"; (ws / "swarm" / "guidance").mkdir(parents=True)
state = TMP / "state.json"; state.write_text(json.dumps({"round": 0}))
cfg = {"workspace": str(ws), "log": str(TMP / "cadence.jsonl"), "adapter": "fake_task:Task", "adapter_args": {"state": str(state)},
       "runner": [sys.executable, "-I", str(TMP / "stub_role.py"), "{prompt}"], "review_timeout_s": 60}
cp = TMP / "cfg.json"; cp.write_text(json.dumps(cfg))
env = {"PYTHONPATH": str(TMP), "PATH": "/usr/bin:/bin"}
def eng(*extra, stdin="{}"):
    r = subprocess.run([sys.executable, str(HERE / "engine_v11.py"), str(cp), *extra], input=stdin, capture_output=True, text=True, env=env, cwd=TMP)
    assert r.returncode == 0, r.stderr
    return r.stdout

eng("--interface")
iface = (ws / "swarm" / "system_interface.md").read_text()
assert "agent time" in iface and "opportunities" in iface and "guardrail" not in iface.lower()
(ws / "swarm" / "system.json").write_text(json.dumps({
    "charts": [{"name": "score", "better": "up"}, {"name": "made", "better": "up"}, {"name": "nonsense", "better": "up"}],
    "opportunities": [{"id": "O1", "label": "benches free", "when": [{"resource": "Benches", "unused_at_least": 1}]},
                      {"id": "O2", "label": "bad", "when": [{"resource": "no such thing", "unused_at_least": 1}]}],
    "cadence": {"pulse_every": 50, "audit_every": 100, "min_periods_between_redesigns": 1, "check_every": 2, "event_min_gap": 2}}))
(ws / "swarm" / "guidance" / "G-001.md").write_text("# Use the time you have\nApplies when: always\nWhat good looks like: a round that uses most of its time\nWhy: from the brief\nSource: brief\nRevisit: round 100\n")

outs = []
for rnd in range(1, 21):
    if rnd > 1: eng("--pre")
    st = json.loads(state.read_text()); st["round"] = rnd; state.write_text(json.dumps(st))
    if rnd == 4: (ws / "notes.md").write_text("Policy: benches are never worth filling.\n")
    o = eng(); outs.append(json.loads(o)["hookSpecificOutput"]["additionalContext"] if o.strip() else "")
    mem = json.loads((TMP / "cadence.mem.json").read_text())
    for _ in range(100):  # let background roles finish, as real time passes between periods
        if all(Path(j["out"]).exists() for j in mem["pending"]): break
        time.sleep(0.05)

ev = [json.loads(l) for l in (TMP / "cadence.jsonl").read_text().splitlines()]
kinds = [e.get("event") for e in ev]
d0 = next(e for e in ev if e.get("event") == "design_loaded")
assert d0["charts"] == ["score", "made"] and d0["opportunities"] == ["O1"] and len(d0["problems"]) == 3, d0
assert "'Benches' read as 'benches'" in d0["problems"], d0
assert "you decide what to do" in outs[0].lower() and "G-001" in outs[0] and "a round that uses most of its time" in outs[0]
assert "Guidance G-001" not in outs[5], "always-guidance is shown once, not every period"
assert "Open now: O1 benches free (3)" in outs[1] and "you used 30% of your capacity" in outs[1]
assert any("execution_event" == k for k in kinds), kinds
pulses = [e for e in ev if e.get("event") == "started" and e.get("kind") == "pulse"]
assert pulses and pulses[0]["trigger"] == "event", pulses
lags = [e["lag"] for e in ev if e.get("event") == "pulse" and e.get("lag") is not None]
assert lags, "lag from event to delivery is measured"
lib = sorted(p.name for p in (ws / "swarm" / "guidance").glob("G-*.md"))
assert len(lib) >= 2 and "Fact check: C-" in (ws / "swarm" / "guidance" / lib[1]).read_text(), lib
assert "refuted" in (ws / "swarm" / "checks" / "policies.md").read_text()
assert any("Fact check of your note" in o and "refuted" in o for o in outs)
assert "diagnosis" in kinds and "redesign" in kinds
assert any(e.get("event") == "design_loaded" and e.get("after") for e in ev)
assert any("The designer changed the environment" in o for o in outs)
for o in outs:  # nothing the system hands the agent is an order
    low = o.lower()
    assert not any(w in low for w in ("you must", "act on it", "adopt it", "follow it", "re-read")), o
assert "capacity_used_share" in (ws / "swarm" / "metrics_system.md").read_text()
assert "Behavior and cost (information only" in (ws / "swarm" / "charts.md").read_text()
print("engine v1.1: all checks pass;", len(lib), "guidance entries,", len(pulses), "pulses,", kinds.count("check"), "fact checks")
