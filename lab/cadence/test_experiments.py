"""Tests for the experiment lifecycle (experiments.py). Run: python3 -I test_experiments.py"""
import random, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import experiments as X, progress as P

W = 7
spec = {"unit": "day", "horizon": 365, "cycle": 7, "top": "cash", "goal": {"value": 60000},
        "measures": {"cash": {"kind": "level", "better": "up"}, "unit_cost_paid_30d": {"kind": "level", "better": "down"}},
        "unit_measures": {"machine_revenue": {"kind": "flow", "better": "up"}}}
U = ["A", "B", "C", "D"]

def run(lift, days=84, start=43, slice_=("A",), seed=1):
    random.seed(seed)
    sw = Path(tempfile.mkdtemp()) / "swarm"; (sw / "experiments").mkdir(parents=True)
    (sw / "experiments" / "E-001.md").write_text(
        f"# E-001\nDriver: machine_revenue   Slice: {', '.join(slice_)}   Control: rest\nChange: x\nStart: day {start}   End: day {start + 21}\n")
    mem = {}; acts_all = []
    for t in range(1, days + 1):
        P.update(mem, spec, t, {"cash": 1500 + 10 * t}, {})
        s = mem.get("exp", {}).get("E-001", {})
        on = s.get("state") in ("running", "verdict", "done") and s.get("start_t", 10**9) <= t
        X.record_units(mem, t, {u: {"machine_revenue": 100 * random.uniform(0.9, 1.1) * (lift if (on and u in slice_) else 1)} for u in U})
        md, acts = X.step(mem, spec, sw, t, mem["progress"]["last_point"], True, W)
        for a in acts:
            acts_all.append((t, a[0]))
            if a[0] == "fidelity":
                X.fidelity_result(mem, "E-001", "checked\nFidelity: pass", t, W)
            if a[0] == "verdict":
                X.verdict_result(mem, "E-001", "Verdict: keep")
    return mem["exp"]["E-001"], acts_all, md

s, acts, md = run(1.5)
assert [a for _, a in acts] == ["note", "fidelity", "verdict"], acts   # the start note hands over the change
assert s["state"] == "done" and s["start_t"] == 46 and s["end_t"] == 67, s   # clock starts at the fidelity check, not at Start
c = s["cmp"]; assert c["effect"] > 1.3 and c["reading"].startswith("better beyond"), c
assert "slice (A) / control" in c["how"]
s, _, _ = run(1.0); assert s["cmp"]["reading"].startswith("too small"), s["cmp"]
s, _, _ = run(0.6); assert s["cmp"]["reading"].startswith("worse beyond"), s["cmp"]
assert "| E-001 | machine_revenue | A |" in md

# Driver not measured: void, with a note naming the measures
sw = Path(tempfile.mkdtemp()) / "swarm"; (sw / "experiments").mkdir(parents=True)
(sw / "experiments" / "E-002.md").write_text("Driver: footfall per location\nSlice: A\nStart: 5\nEnd: 30\n")
mem = {}; P.update(mem, spec, 1, {"cash": 1500}, {})
md, acts = X.step(mem, spec, sw, 1, 0, True, W)
assert mem["exp"]["E-002"]["state"] == "void" and acts[0][0] == "note" and "machine_revenue" in acts[0][1]

# Overlapping slices queue; disjoint ones run side by side
sw = Path(tempfile.mkdtemp()) / "swarm"; (sw / "experiments").mkdir(parents=True)
(sw / "experiments" / "E-001.md").write_text("Driver: machine_revenue\nSlice: A, B\nStart: 25\nEnd: 50\nApplied: 25\n")
(sw / "experiments" / "E-002.md").write_text("Driver: machine_revenue\nSlice: B\nStart: 25\nEnd: 50\nApplied: 25\n")
(sw / "experiments" / "E-003.md").write_text("Driver: machine_revenue\nSlice: C\nStart: 25\nEnd: 50\nApplied: 25\n")
mem = {}
for t in range(1, 26): P.update(mem, spec, t, {"cash": 1500}, {})
md, acts = X.step(mem, spec, sw, 25, mem["progress"]["last_point"], True, W)
st = {k: v["state"] for k, v in mem["exp"].items()}
assert st == {"E-001": "fidelity", "E-002": "queued", "E-003": "fidelity"}, st
assert any(a[0] == "note" and "E-002 is queued" in a[1] for a in acts)

# Network driver (whole system): judged against its own earlier line; better = down for cost
sw = Path(tempfile.mkdtemp()) / "swarm"; (sw / "experiments").mkdir(parents=True)
(sw / "experiments" / "E-004.md").write_text("Driver: unit_cost_paid_30d\nSlice: all\nStart: 43\nEnd: 64\nApplied: 43\n")
mem = {}
random.seed(3)
for t in range(1, 85):
    on = mem.get("exp", {}).get("E-004", {}).get("start_t", 10**9) <= t
    P.update(mem, spec, t, {"cash": 1500, "unit_cost_paid_30d": random.uniform(0.98, 1.02) * (0.7 if on else 1.0)}, {})
    md, acts = X.step(mem, spec, sw, t, mem["progress"]["last_point"], True, W)
    for a in acts:
        if a[0] == "fidelity": X.fidelity_result(mem, "E-004", "Fidelity: pass", t, W)
c = mem["exp"]["E-004"]["cmp"]; assert c["effect"] < 0.8 and c["reading"].startswith("better beyond"), c

# Fidelity failing three times voids the experiment
mem = {"exp": {"E-9": {"state": "fidelity", "fails": 2, "check_pending": True}}}
ok, state = X.fidelity_result(mem, "E-9", "mismatch\nFidelity: fail", 10, W); assert not ok and state == "void"
# Baseline: nothing starts before 3 points; then it starts with the exact change handed over
sw = Path(tempfile.mkdtemp()) / "swarm"; (sw / "experiments").mkdir(parents=True)
(sw / "experiments" / "E-006.md").write_text("Driver: machine_revenue\nSlice: A\nChange: set price 1.50 on A1\nStart: 5\nEnd: 40\n")
mem = {}
for t in range(1, 6): P.update(mem, spec, t, {"cash": 1500}, {})
md, acts = X.step(mem, spec, sw, 5, mem["progress"]["last_point"], True, W)
assert mem["exp"]["E-006"]["state"] == "queued" and "baseline" in acts[0][1], acts
for t in range(6, 23): P.update(mem, spec, t, {"cash": 1500}, {})
md, acts = X.step(mem, spec, sw, 22, mem["progress"]["last_point"], True, W)
assert any("starts now" in a[1] and "set price 1.50 on A1" in a[1] for a in acts if a[0] == "note"), acts

# Capacity: required when the task declares one, and held to the experiment budget
cspec = dict(spec, capacity="worker time", experiment_share=0.10)
sw = Path(tempfile.mkdtemp()) / "swarm"; (sw / "experiments").mkdir(parents=True)
(sw / "experiments" / "E-007.md").write_text("Driver: machine_revenue\nSlice: A\nStart: 25\nEnd: 50\nApplied: 25\n")
(sw / "experiments" / "E-008.md").write_text("Driver: machine_revenue\nSlice: B\nCapacity: 30 minutes a day\nStart: 25\nEnd: 50\nApplied: 25\n")
(sw / "experiments" / "E-009.md").write_text("Driver: machine_revenue\nSlice: C\nCapacity: 30\nStart: 25\nEnd: 50\nApplied: 25\n")
mem = {}
for t in range(1, 26): P.update(mem, cspec, t, {"cash": 1500}, {})
md, acts = X.step(mem, cspec, sw, 25, mem["progress"]["last_point"], True, W, 480)
st = {k: v["state"] for k, v in mem["exp"].items()}
assert st == {"E-007": "void", "E-008": "fidelity", "E-009": "queued"}, st   # no Capacity: void; 30 + 30 > 48 (10% of 480)
notes = " ".join(a[1] for a in acts if a[0] == "note")
assert "no 'Capacity:' line" in notes and "above the experiment budget of 48" in notes, notes
print("all experiment tests passed")
