"""Tests for the celeration math (progress.py). Run: python3 -I test_progress.py"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import progress as P

def close(a, b, tol=1e-6):
    assert abs(a - b) <= tol * max(1, abs(b)), (a, b)

# Window derivation
w = P.derive_window(365, 7); assert w["w"] == 7 and w["n"] == 52 and w["ok"], w
w = P.derive_window(60, 1); assert w["w"] == 3 and w["n"] == 20 and w["ok"], w
w = P.derive_window(30, 7); assert not w["ok"], w          # 4 points: too short
w = P.derive_window(100, 2); assert w["w"] == 4, w          # whole cycles holding >= 3 observations
w = P.derive_window(500, 10, "budget"); assert w["w"] == 10 and w["n"] == 50, w

# Points: median of a flow per closed window; last value of a level; open window left out
ser = [(t, t % 7 + 1) for t in range(1, 22)]                # three closed windows of 7
pts = P.points(ser, 7, "flow"); assert [p[0] for p in pts] == [0, 1, 2] and all(p[2] == 7 for p in pts), pts
pts = P.points(ser[:-1], 7, "flow"); assert [p[0] for p in pts] == [0, 1], pts
lv = P.points([(t, 100 + t) for t in range(1, 15)], 7, "level"); assert lv == [(0, 107, 7), (1, 114, 7)], lv

# Exact doubling per point: both fit methods recover x2.00, zero bounce, range collapses to x2
for n in (3, 5, 7, 8, 12):
    f = P.fit([(k, 10 * 2 ** k, 1) for k in range(n)])
    close(f["cel"], 2.0); close(f["lo"], 2.0); close(f["hi"], 2.0); close(f["bounce"], 1.0)
    assert f["method"] == ("quarter-intersect" if n <= 7 else "Theil-Sen") and f["provisional"] == (n < 6)
    assert P.verdict(f) == "improving" and P.verdict(f, "down") == "wrong way"
assert P.fit([(0, 1, 1), (1, 2, 1)]) is None               # fewer than 3 points: collecting

# Robust to one bad week (least squares would swing)
good = [(k, 100 * 1.1 ** k, 1) for k in range(10)]
bad = good[:5] + [(5, 1.0, 1)] + good[6:]
close(P.fit(bad)["cel"], 1.1, 1e-3)

# Flat: noise around a constant level has a range spanning x1.0
flat = [(k, 100 * (1.2 if k % 2 else 0.85), 1) for k in range(8)]
assert P.verdict(P.fit(flat)) == "flat", P.fit(flat)

# Zeros sit under the record floor and are left out
f = P.fit([(0, 0, 1), (1, 10, 1), (2, 20, 1), (3, 40, 1)]); close(f["cel"], 2.0); assert f["n"] == 3

# Bounce: a x2 zigzag around a flat line gives a wide envelope
z = P.fit([(k, 100 * (2 if k % 2 else 1), 1) for k in range(10)]); assert z["bounce"] > 3, z

# Floor and aim lines on a level that grows x1.05 a point toward a target 10x away
mem = {}; spec = {"unit": "day", "horizon": 365, "cycle": 7, "top": "cash", "goal": {"type": "maximize", "value": 15000},
                  "measures": {"cash": {"kind": "level", "better": "up"}}}
evs = []
for t in range(1, 8 * 7 + 1):
    md, e = P.update(mem, spec, t, {"cash": 1500 * 1.05 ** ((t - 1) // 7)}, {})
    evs += e
L = mem["progress"]["lines"]
assert L and L["k0"] == 2 and L["aim"] > L["floor"] > 1, L
close(L["floor"], (15000 / (1500 * 1.05 ** 2)) ** (1 / (52 - 1 - 2)))
assert "Floor line" in md and "Aim line" in md
assert not any(x["kind"] == "below_floor" for x in evs)     # x1.05 beats the floor of about x1.04

# Below the floor: flat cash for 3 points after the lines are drawn
mem = {}; evs = []
for t in range(1, 7 * 7 + 1):
    md, e = P.update(mem, spec, t, {"cash": 1500.0}, {}); evs += e
assert any(x["kind"] == "below_floor" for x in evs) and any(x["kind"] == "flat_or_wrong" for x in evs)

# Aim met on 2 of 3 points: raised toward double the target
mem = {}; evs = []
for t in range(1, 12 * 7 + 1):
    md, e = P.update(mem, spec, t, {"cash": 1500 * 1.4 ** ((t - 1) // 7)}, {}); evs += e
assert any(x["kind"] == "aim_raised" for x in evs) and mem["progress"]["lines"]["aim_target"] >= 30000

# Phases: jump and turn reported after a phase change
mem = {}
for t in range(1, 6 * 7 + 1):
    P.update(mem, spec, t, {"cash": 1500 * 1.02 ** ((t - 1) // 7)}, {})
P.new_phase(mem)
for t in range(6 * 7 + 1, 10 * 7 + 1):
    md, _ = P.update(mem, spec, t, {"cash": 1500 * 1.02 ** 5 * 1.2 * 1.10 ** ((t - 1) // 7 - 6)}, {})
assert "Jump" in md and "Turn" in md and "needs" not in md.split("Turn")[1][:40], md[-400:]

# Guardrail breach and short horizon
mem = {}; sp2 = dict(spec, guardrails=[{"measure": "cash", "min": 120, "label": "reserve"}])
_, e = P.update(mem, sp2, 1, {"cash": 50}, {}); assert any(x["kind"] == "guardrail" for x in e)
mem = {}; md, _ = P.update(mem, dict(spec, horizon=30), 1, {"cash": 1500}, {}); assert "Celeration off" in md
print("all progress tests passed")
