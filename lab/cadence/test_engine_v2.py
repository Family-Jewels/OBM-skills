"""Whole-engine tests for v2 in dry-run mode (no model calls). Run: python3 -I test_engine_v2.py"""
import contextlib, io, json, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import engine_v2

class Synthetic:
    """A task with a weekly cycle, a capacity resource and slowly growing cash."""
    def __init__(self, day, horizon=182):
        self.day, self.h = day, horizon
    def spec(self):
        return {"unit": "day", "horizon": self.h, "cycle": 7, "clock": "period", "top": "cash",
                "goal": {"type": "maximize", "value": 50000}, "capacity": "worker time", "experiment_share": 0.10,
                "measures": {"cash": {"kind": "level", "better": "up"}, "revenue": {"kind": "flow", "better": "up"}},
                "unit_measures": {"machine_revenue": {"kind": "flow", "better": "up"}}, "resources": ["worker time"], "guardrails": []}
    def read(self):
        d = self.day
        return {"period": d, "over": d >= self.h, "measures": {"cash": 1500 + 5 * d, "revenue": 50 + (d % 7)},
                "resources": {"worker time": {"used": 400, "available": 480}},
                "units": {u: {"machine_revenue": 20 + (d % 3)} for u in ("A", "B", "C")}}

def run(days, files, **extra):
    tmp = Path(tempfile.mkdtemp()); ws = tmp / "ws"; (ws / "swarm" / "experiments").mkdir(parents=True)
    for name, text in files.items():
        (ws / "swarm" / "experiments" / name).write_text(text)
    import types
    m = types.ModuleType("synthmod"); m.Synthetic = Synthetic; sys.modules["synthmod"] = m
    for d in range(1, days + 1):
        cfg = {"version": 2, "workspace": str(ws), "log": str(tmp / "cadence.jsonl"), "dry_run": True,
               "adapter": "synthmod:Synthetic", "adapter_args": {"day": d},
               "charts": {"not_before": 8, "min_points": 8, "baseline_points": 20, "measures": [{"name": "revenue", "better": "up"}]}, **extra}
        with contextlib.redirect_stdout(io.StringIO()):
            engine_v2.main(cfg)
    ev = [json.loads(l) for l in (tmp / "cadence.jsonl").read_text().splitlines()]
    started = {}
    for e in ev:
        if e["event"] == "started":
            started.setdefault(e["kind"], []).append(e["period"])
    return ev, started, json.loads((tmp / "cadence.mem.json").read_text())

# Seed 1's bug: experiments written without a Capacity line, queued during the baseline, held off every opportunity review.
ev, started, mem = run(70, {"E-001.md": "Driver: machine_revenue\nSlice: A\nChange: x\nStart: day 4\nEnd: day 40\n",
                            "E-002.md": "Driver: machine_revenue\nSlice: B\nChange: y\nStart: day 9\nEnd: day 45\n"})
assert started.get("opportunity") and started["opportunity"][0] <= 28, started          # a review by point 4
assert mem["exp"]["E-001"]["state"] == "void" and mem["exp"]["E-002"]["state"] == "void", mem["exp"]
assert len(started.get("pulse", [])) >= 8, started                                         # a pulse every point (then spaced)
pre = [e for e in ev if e["event"] == "preflight"][0]; assert pre["problems"] == [], pre

# An experiment that does start holds off reviews, but never past 6 points without one.
ev, started, mem = run(120, {"E-003.md": "Driver: machine_revenue\nSlice: A\nCapacity: 20\nChange: z\nStart: day 22\nEnd: day 110\nApplied: day 22\n"})
opp = started.get("opportunity", [])
gaps = [b - a for a, b in zip([0] + opp, opp)]
assert opp and max(gaps) <= 7 * 7, (opp, gaps)
assert mem["exp"]["E-003"]["state"] in ("running", "verdict", "done"), mem["exp"]

# A task with no capacity declared fails preflight.
spec = Synthetic(1).spec(); spec.pop("capacity")
assert any("no capacity declared" in p for p in engine_v2.preflight(spec, Synthetic(1).read()))
# v3: the Strategist after the baseline and every 3 points, each followed at once by the designer's aim update; no experiments.
ev, started, mem = run(91, {"E-001.md": "Driver: machine_revenue\nSlice: A\nCapacity: 5\nStart: 22\nEnd: 60\nApplied: 22\n"}, version=3)
st, am = started.get("strategist", []), started.get("aims", [])
assert st and st[0] == 21 and all(14 <= b - a <= 21 for a, b in zip(st, st[1:])), st   # first at point 3; then every 2-3 points
assert len(am) == len(st) or len(am) == len(st) - 1, (st, am)                          # each strategy gets its aim update
assert all(a - s <= 2 for s, a in zip(st, am)), (st, am)                               # right away, not behind redesign spacing
assert "opportunity" not in started and "fidelity" not in started and not mem.get("exp"), started
assert any(e["event"] == "aims" for e in ev)

# v3: faults first. Every pulse asks for a diagnosis; deferred ones queue and all run, none is dropped.
ev, started, mem = run(140, {}, version=3, dry_run_diagnosis="yes")
asked = sum(1 for e in ev if e["event"] in ("pulse", "audit"))
ran = len(started.get("diagnosis", [])); queued = sum(1 for e in ev if e["event"] == "diagnosis_queued")
assert ran >= 4 and queued >= 1 and not any(e["event"] == "diagnosis_deferred" for e in ev), (asked, ran, queued)
assert ran + len(mem.get("diag_queue", [])) >= queued, (ran, queued, mem.get("diag_queue"))
print("all engine tests passed")
