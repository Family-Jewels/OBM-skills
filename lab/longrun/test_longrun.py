"""Tests for the long-run kit: step record and cues, change verification, the skill build gate. Run: python3 -I test_longrun.py"""
import json, random, subprocess, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import steps, verify, skill_gate

tmp = Path(tempfile.mkdtemp())
ws = tmp / "ws"; (ws / "swarm" / "log").mkdir(parents=True)
f1 = ws / "swarm" / "spec.md"; f1.write_text("spec v1")
CFG = {**steps.DEFAULTS, "workspace_roots": [str(ws)], "own_logs": ["swarm/log/progress.md"], "no_progress_steps": 5,
       "window": 10, "log_bytes_per_window": 500}

# ---------- classification ----------
assert steps.classify("Read", {"file_path": "/a"})[0] == "read"
assert steps.classify("Edit", {"file_path": "/a"})[0] == "write"
assert steps.classify("Bash", {"command": "cat /a | head"})[0] == "read"
assert steps.classify("Bash", {"command": "pytest -q tests"})[0] == "run"
assert steps.classify("mcp__vending__get_balance", {})[0] == "task_read"
assert steps.classify("mcp__vending__restock_machine", {})[0] == "task_act"
assert steps.failed({"is_error": True}) and steps.failed("Error: no such file") and not steps.failed({"stdout": "ok"})
assert steps.failed({"exit_code": 2}) and not steps.failed(None)

def feed(calls, cfg=CFG):
    s, cues = steps.new_state(), []
    for i, (tool, inp, resp) in enumerate(calls, 1):
        cues.append(steps.update(s, steps.make_record(i, tool, inp, resp, cfg), cfg))
    return s, cues

# ---------- freshness: an unchanged re-read fires once; a read after the agent's own write does not ----------
rd = ("Read", {"file_path": str(f1)}, {"ok": 1})
s, cues = feed([rd, rd, rd])
assert s["rereads"] == 2 and len([c for c in cues[1] if "has not changed" in c]) == 1 and not cues[2], cues
s, cues = feed([rd, ("Edit", {"file_path": str(f1), "new_string": "x"}, {"ok": 1}), rd])
assert s["rereads"] == 0 and not any("has not changed" in c for cc in cues for c in cc)
f1.write_text("spec v2")  # changed outside the agent: a read of new content is not a re-read
s2 = steps.new_state(); steps.update(s2, {"i": 1, "tool": "Read", "kind": "read", "target": str(f1), "sig": "a", "ok": True, "hash": "old"}, CFG)
assert not steps.update(s2, steps.make_record(2, "Read", {"file_path": str(f1)}, {}, CFG), CFG)

# ---------- diversity: the same call failing again ----------
bad = ("Bash", {"command": "make build"}, {"is_error": True})
s, cues = feed([bad, bad, bad])
assert any("failed 2 times" in c for c in cues[1]) and not any("failed" in c for c in cues[2]), cues
assert s["retries_unchanged"] == 2 and s["repeat_failures"] == 2

# ---------- relevance: steps with no state change; resets on progress ----------
reads = [("Grep", {"pattern": f"x{i}"}, {}) for i in range(6)]
s, cues = feed(reads + [("Write", {"file_path": str(ws / "out.txt"), "content": "done"}, {})] + reads)
fired = [i for i, c in enumerate(cues) if any("no state-changing" in x for x in c)]
assert fired == [4, 11], fired  # fires at the 5th idle step, again after progress and 5 more idle steps

# ---------- placement and economy ----------
s, cues = feed([("Write", {"file_path": "/elsewhere/log/progress.md", "content": "x"}, {})])
assert any("outside the workspace" in c for c in cues[0])
big = ("Edit", {"file_path": str(ws / "swarm/log/progress.md"), "new_string": "y" * 300}, {})
s, cues = feed([big, big])
assert any("Your log grew 600 bytes" in c for c in cues[1]) and s["own_log_bytes"] == 600
# writing the own log is not progress
s, cues = feed([big] * 6)
assert any("no state-changing" in c for cc in cues for c in cc)

# ---------- summary and health panel ----------
m = steps.summarize([steps.make_record(i, *c, CFG) for i, c in enumerate([rd, rd, bad, bad], 1)], CFG)
assert m["unchanged_rereads"] == 1 and m["repeat_failures"] == 1 and "Step health" in steps.health_markdown(m)
assert m["cues"]["freshness"] == 1 and m["cues"]["diversity"] == 1 and "Cues the step record raised" in steps.health_markdown(m)

# ---------- the hook end to end ----------
hcfg = tmp / "hook.json"
hcfg.write_text(json.dumps({**CFG, "steps_log": str(ws / "swarm/log/steps.jsonl"), "health_md": str(ws / "swarm/step_health.md"),
                            "health_every": 2}))
outs = []
for _ in range(3):
    p = subprocess.run([sys.executable, "-I", str(HERE / "steps_hook.py"), str(hcfg)], input=json.dumps(
        {"hook_event_name": "PostToolUse", "tool_name": "Read", "tool_input": {"file_path": str(f1)}, "tool_response": {"content": "x"}}),
        capture_output=True, text=True, timeout=30)
    outs.append(json.loads(p.stdout))
lines = (ws / "swarm/log/steps.jsonl").read_text().splitlines()
assert len(lines) == 3 and json.loads(lines[0])["kind"] == "read"
assert outs[0] == {} and "has not changed" in outs[1]["hookSpecificOutput"]["additionalContext"] and outs[2] == {}
assert (ws / "swarm/step_health.md").exists()
p = subprocess.run([sys.executable, "-I", str(HERE / "steps_hook.py"), str(tmp / "missing.json")], input="{}", capture_output=True, text=True)
assert p.returncode == 0 and json.loads(p.stdout) == {}  # never fails the tool call
ocfg = tmp / "observe.json"; ocfg.write_text(json.dumps({"steps_log": str(tmp / "obs/steps.jsonl"), "cues": False}))
obs = [json.loads(subprocess.run([sys.executable, "-I", str(HERE / "steps_hook.py"), str(ocfg)], capture_output=True, text=True, input=json.dumps(
    {"tool_name": "Read", "tool_input": {"file_path": str(f1)}, "tool_response": {}})).stdout) for _ in range(2)]
assert obs == [{}, {}] and len((tmp / "obs/steps.jsonl").read_text().splitlines()) == 2  # observation-only: records, never cues

# ---------- verification: parsing ----------
charted = ["slots_selling", "revenue", "cash_gain_7"]
pr, prob = verify.parse("## Change\n...\nPrediction: slots_selling up within 2 points\n", charted)
assert pr == {"measure": "slots_selling", "dir": "up", "n": 2, "unit": "point"} and prob is None
pr, prob = verify.parse("**Prediction:** `revenue` down within 14 days", charted)
assert pr["unit"] == "period" and pr["n"] == 14
pr, prob = verify.parse("Prediction: empty_slots_0900 down within 2 points", charted)
assert pr is None and "does not chart" in prob
pr, prob = verify.parse("Prediction. slots_selling should rise by day 40.", charted)
assert pr is None and "no machine-readable prediction" in prob

# ---------- verification: verdicts ----------
rnd = random.Random(7)
flat = [[d, 10 + rnd.uniform(-1, 1)] for d in range(1, 61)]
step_up = [[d, v + (6 if d > 30 else 0)] for d, v in flat]
step_dn = [[d, v - (6 if d > 30 else 0)] for d, v in flat]
P = lambda: {"id": "M-001", "adopted": 30, "measure": "slots_selling", "dir": "up", "n": 2, "unit": "point"}
assert verify.judge(P(), step_up, 35, 7) is None                       # not due yet
assert verify.judge(P(), step_up, 44, 7)["verdict"].startswith("shift as predicted")
assert verify.judge(P(), flat, 44, 7)["verdict"] == "no shift"
assert verify.judge(P(), step_dn, 44, 7)["verdict"] == "shift the wrong way"
assert verify.judge(P(), flat[:36], 44, 7)["verdict"] == "not enough data"   # 6 of the window's 14 periods observed
trend = [[d, d * 1.0] for d in range(1, 121)]                          # a rising series: an 'up' hit is what chance gives
j = verify.judge({**P(), "adopted": 60}, trend, 74, 7)
assert j["verdict"].startswith("shift as predicted (weak") and j["chance"] >= 0.5, j
assert verify.chance(flat + [[d, 10 + rnd.uniform(-1, 1)] for d in range(61, 200)], 14, "up") < 0.2

# register / update / markdown, as the engine uses them
mem = {}
ser = {"slots_selling": step_up}
assert verify.register(mem, "M-001", "Prediction: slots_selling up within 2 points", charted, 30, lambda m: ser.get(m, [])) is None
prob = verify.register(mem, "M-002", "We expect fewer empty slots.", charted, 32, lambda m: ser.get(m, []))
assert "no machine-readable" in prob
assert verify.update(mem, 40, 7, lambda m: ser.get(m, [])) == []
new = verify.update(mem, 44, 7, lambda m: ser.get(m, []))
assert len(new) == 1 and new[0]["verdict"].startswith("shift as predicted")
md = verify.markdown(mem, "day")
assert "M-001" in md and "M-002" in md and "not judged" in md

# replay on a real run: obm_cadence seed 1, R-P-021 (adopted day 161, slots_selling up, due day 170) was a hit for the
# analysis scorer; the system's verifier must agree on the same data
metrics = HERE.parent.parent / "results/2026-11-17-five-seeds-skills-vs-native/obm_cadence-seed1/workspace/swarm/metrics_system.md"
if metrics.exists():
    rows = [l.split("|")[1:-1] for l in metrics.read_text().splitlines() if l.startswith("| ") and l.split("|")[1].strip().isdigit()]
    real = [[int(r[0]), float(r[4])] for r in rows]
    r = verify.test(real, 161, 171, "up")
    assert r["hit"] and not r["wrong_way"], r
    r = verify.test(real, 116, 132, "up")   # R-A-002: a miss for the scorer
    assert not r["hit"], r

# ---------- the skill build gate ----------
def skill(root, **over):
    d = root / over.get("name", "ok-skill"); (d / "tests").mkdir(parents=True); (d / "reviews").mkdir()
    (d / "decision.md").write_text(over.get("decision", "Gap: orders sized by guess\nEvidence: D-P-003 (stock-outs days 11-17)\n"
                                                        "Reuse: every weekly order\nDecision: build\n"))
    (d / "SKILL.md").write_text(over.get("skill", "---\nname: order-sizing\ndescription: Size each order from the sales rate.\n---\n"
                                               "# Order sizing\n## When to use\nBefore any order.\n## Steps\n1. Read the rate.\n## Done when\nEvery line sized.\n"))
    cases = over.get("cases", [{"id": "c1", "held_out": False}, {"id": "c2", "held_out": False}, {"id": "c3", "held_out": True},
                               {"id": "c4", "held_out": True}])
    (d / "tests/cases.jsonl").write_text("\n".join(json.dumps({"input": "...", "expect": "...", **c}) for c in cases) + "\n")
    (d / "verification.json").write_text(json.dumps(over.get("ver", {"held_out": ["c3", "c4"], "baseline": {"passed": 0, "of": 2},
                                                                      "with_skill": {"passed": 2, "of": 2}, "how": "replay", "by": "system"})))
    (d / "reviews/R-1.md").write_text(over.get("review", "Reviewer: checker-2\nAuthor: worker-1\n## Findings\n- F1: step 1 vague\n"
                                                        "## Dispositions\n- F1: done | named the report\n"))
    return d

g = tmp / "gate"
assert skill_gate.check(skill(g))[0] == "adopt"
assert skill_gate.check(skill(g, name="skip", decision="Gap: x\nEvidence: y\nReuse: once\nDecision: skip\n"))[0] == "not built"
st_, rs, _ = skill_gate.check(skill(g, name="nogain", ver={"held_out": ["c3", "c4"], "baseline": {"passed": 2, "of": 2},
                                                        "with_skill": {"passed": 2, "of": 2}, "how": "replay", "by": "system"}))
assert st_ == "fail" and any("no measured gain" in r for r in rs)
st_, rs, _ = skill_gate.check(skill(g, name="noheld", cases=[{"id": f"c{i}", "held_out": False} for i in range(4)]))
assert any("held out" in r for r in rs)
st_, rs, _ = skill_gate.check(skill(g, name="self", review="Reviewer: worker-1\nAuthor: worker-1\n## Findings\n## Dispositions\n"))
assert any("reviewer is the author" in r for r in rs) and any("no independent review" in r for r in rs)
st_, rs, _ = skill_gate.check(skill(g, name="unanswered", review="Reviewer: c\nAuthor: w\n## Findings\n- F1: a\n- F2: b\n## Dispositions\n- F1: declined | why\n"))
assert any("no disposition: F2" in r for r in rs)
st_, rs, _ = skill_gate.check(skill(g, name="nodone", skill="---\nname: a\ndescription: b\n---\n## When to use\n## Steps\n"))
assert any("when it is done" in r for r in rs)
st_, rs, _ = skill_gate.check(skill(g, name="noevidence", decision="Gap: x\nDecision: build\n"))
assert st_ == "fail" and any("Evidence" in r for r in rs)
p = subprocess.run([sys.executable, "-I", str(HERE / "skill_gate.py"), str(g / "ok-skill")], capture_output=True, text=True)
assert p.returncode == 0 and json.loads(p.stdout)["status"] == "adopt"
print("all long-run kit tests passed")
