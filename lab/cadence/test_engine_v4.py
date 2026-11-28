"""Whole-engine tests for v4 in dry-run mode (no model calls). Run: python3 -I test_engine_v4.py"""
import contextlib, io, json, sys, tempfile, types
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import engine_v4, ledger, facts, profile

class Synth:
    """A task with a weekly cycle, a capacity resource, slowly growing cash and a profile."""
    def __init__(self, day, horizon=182, reversible=False, guard_day=None):
        self.day, self.h, self.rev, self.gd = day, horizon, reversible, guard_day
    def spec(self):
        return {"unit": "day", "horizon": self.h, "cycle": 7, "clock": "period", "top": "cash",
                "goal": {"type": "maximize", "value": 50000}, "capacity": "worker time",
                "profile": {"work_shape": "operation", "feedback_lag": 7, "reversible": self.rev},
                "action_clock": {"start": 540},
                "measures": {"cash": {"kind": "level", "better": "up"}, "revenue": {"kind": "flow", "better": "up"}},
                "resources": ["worker time"], "guardrails": [{"measure": "cash", "min": 1000, "label": "cash reserve"}]}
    def read(self):
        d = self.day
        cash = 1500 + 5 * d if not (self.gd and self.gd <= d < self.gd + 3) else 900
        return {"period": d, "over": d >= self.h, "measures": {"cash": cash, "revenue": 50 + (d % 7)},
                "resources": {"worker time": {"used": 400, "available": 480}}}

def run(days, dry=None, actions=None, **extra):
    tmp = Path(tempfile.mkdtemp()); ws = tmp / "ws"; (ws / "swarm").mkdir(parents=True)
    m = types.ModuleType("synth4"); m.Synth = Synth; sys.modules["synth4"] = m
    alog = tmp / "actions.jsonl"
    args = extra.pop("adapter_args", {})
    for d in range(1, days + 1):
        if actions:
            with alog.open("a") as f:
                clock = 540
                for tool, cost, n in actions(d):
                    for _ in range(n):
                        clock += cost; f.write(json.dumps({"tool": tool, "period": d, "clock": clock}) + "\n")
        cfg = {"version": 4, "workspace": str(ws), "log": str(tmp / "cadence.jsonl"), "dry_run": True, "action_log": str(alog),
               "adapter": "synth4:Synth", "adapter_args": {"day": d, **args}, "dry": dry or {},
               "charts": {"not_before": 8, "min_points": 8, "baseline_points": 20, "measures": [{"name": "revenue", "better": "up"}]}, **extra}
        with contextlib.redirect_stdout(io.StringIO()):
            engine_v4.main(cfg)
    ev = [json.loads(l) for l in (tmp / "cadence.jsonl").read_text().splitlines()]
    started = {}
    for e in ev:
        if e["event"] == "started":
            started.setdefault(e["kind"], []).append(e["period"])
    return ev, started, json.loads((tmp / "cadence.mem.json").read_text()), ws / "swarm"

# 1. The rhythm on a quiet task: both branches run on their own clocks.
ev, st, mem, sw = run(182)
pre = [e for e in ev if e["event"] == "preflight"][0]
assert pre["problems"] == [] and pre["config"]["strategy_every"] == 3 and pre["config"]["risk_sweep_every"] == 1, pre
assert st["strategist"][0] == 21 and all(b - a == 21 for a, b in zip(st["strategist"], st["strategist"][1:])), st["strategist"]
assert all(a - s <= 1 for s, a in zip(st["strategist"], st["aims"])), (st["strategist"], st["aims"])  # aims follow at once
assert len(st["pulse"]) >= 20, st["pulse"]                      # a routine risk sweep every point (irreversible task)
assert 10 <= len(st["check"]) <= 14, st["check"]                # claim samples every 2 points
assert len(st["audit"]) == 3 and len(st["organizer"]) == 3, st  # full audit and the Organizer at each inner quarter
assert "diagnosis" not in st and "controls" not in st and "method" not in st, st  # nothing to fix, nothing asked: no change jobs
assert (sw / "instructions.md").read_text().index("Controls") < (sw / "instructions.md").read_text().index("Aims")

# 2. A reversible task sweeps every 2 points.
ev, st, mem, sw = run(98, adapter_args={"reversible": True})
assert 6 <= len(st["pulse"]) <= 8, st["pulse"]

# 3. Repeated requests merge, escalate at the third ask, and close only with a disposition.
ask = "Pulse {id}.\nFault: no\n\n## Requests\n- to: designer | key: chart-minutes | Chart minutes per action.\n"
ev, st, mem, sw = run(84, dry={"pulse": ask, "disposition": "declined"})
reqs = mem["ledger"]["reqs"]
assert len([r for r in reqs if r["key"] == "chart-minutes"]) == 1   # one request however often it is asked
first = reqs[0]
assert first["asked"] >= 5 and len(st.get("method", [])) >= 3, (first, st.get("method"))  # declined, re-asked: reopened and taken again
assert any(e["event"] == "escalation" for e in ev) or first["asked"] < 3, [e for e in ev if e["event"] == "escalation"]
assert len(st.get("method", [])) >= 1
# Unanswered requests go back to open and are taken again.
ev, st, mem, sw = run(84, dry={"pulse": ask, "disposition": "deferred"})
assert all(r["status"] in ("open", "in_progress") for r in mem["ledger"]["reqs"]), mem["ledger"]["reqs"]
assert sum(1 for r in mem["ledger"]["reqs"] if r["key"] == "chart-minutes") == 1   # never queued twice
assert any(e["event"] == "escalation" and "asked" in e["text"] for e in ev)

# 4. Faults go through the risk branch and never wait for the improvement branch.
flt = "Pulse {id}.\nFault: yes\nFault key: unpriced-slots\n\n## Corrections\n- price slot 3\n"
ev, st, mem, sw = run(140, dry={"pulse": flt, "strategist": "S {id}\n\n## Requests\n- to: designer | key: restock-step | change it\n"})
assert len(st["diagnosis"]) >= 5 and len(st["controls"]) >= 5, (st.get("diagnosis"), st.get("controls"))
assert len(st["strategist"]) >= 5, st["strategist"]           # improvement branch unaffected by the stream of faults
assert any(e["event"] == "adopted" and e["branch"] == "risk" for e in ev)
assert any(e["event"] == "adopted" and e["branch"] == "improvement" for e in ev)
assert "control from" in (sw / "instructions.md").read_text()
assert not mem.get("fault_queue") or len(mem["fault_queue"]) <= 1   # the same key never piles up

# 5. A guardrail fires once on entry, not every day it lasts.
ev, st, mem, sw = run(60, adapter_args={"guard_day": 40})
g = [e for e in ev if e["event"] == "risk_event" and e["kind"] == "guardrail"]
assert len(g) == 1 and g[0]["period"] == 40, g

# 6. Facts and pursuit from the action log; a plan not followed is a risk event.
acts = lambda d: [("mcp__t__fill", 45, 4), ("mcp__t__order", 10, 2)]
aims = "# Aims\n\n## Capacity split\n- 80% fills: fill\n- 20% orders: order\n"
ev, st, mem, sw = run(49, dry={"aims_md": aims}, actions=acts)
ch = (sw / "charts.md").read_text()
assert "| fill | " in ch and "| 45 |" in ch.replace("45.0", "45"), ch[ch.find("Facts"):ch.find("Facts") + 400]
assert "Pursuit" in ch
aims2 = "# Aims\n\n## Capacity split\n- 30% fills: fill\n- 70% orders: order\n"
ev, st, mem, sw = run(49, dry={"aims_md": aims2}, actions=acts)
assert any(e["event"] == "risk_event" and e["kind"] == "off plan" for e in ev)

# 7. The Organizer changes one setting within bounds; out of bounds is refused.
ev, st, mem, sw = run(100, dry={"organizer": "Config change: strategy_every = 2\nreason"})
assert mem["config"]["strategy_every"] == 2 and any(e["event"] == "config_change" for e in ev)
assert any(e["event"] == "escalation" and e["kind"] == "config change" for e in ev)
ev, st, mem, sw = run(100, dry={"organizer": "Config change: strategy_every = 9\nreason"})
assert mem["config"]["strategy_every"] == 3 and any(e["event"] == "config_refused" for e in ev)

# 8. The system judges each adopted method change from the charts; a miss, or a prediction it cannot judge, goes back to
#    the designer as a request that must be answered. (Synthetic revenue repeats a weekly pattern, so nothing shifts.)
ask_d = "Pulse {id}.\nFault: no\n\n## Requests\n- to: designer | key: restock-step | change how restocking is done\n"
ev, st, mem, sw = run(120, dry={"pulse": ask_d, "method": "M {id}: batch the restock.\n\nPrediction: revenue up within 2 points\n"})
reg = [e for e in ev if e["event"] == "prediction_registered"]
ver = [e for e in ev if e["event"] == "change_verdict"]
assert reg and ver and ver[0]["verdict"] == "no shift" and ver[0]["period"] >= reg[0]["period"] + 14, (reg, ver)
assert any(r["key"].startswith("verdict-m-") and r["from"] == "system" for r in mem["ledger"]["reqs"]), mem["ledger"]["reqs"]
ch = (sw / "charts.md").read_text()
assert "Change verdicts" in ch and "no shift" in ch and "shifted as predicted against" in ch
# A prediction the system cannot judge (no line, or a measure it does not chart) is returned; a restated one is judged.
ev, st, mem, sw = run(120, dry={"pulse": ask_d, "method": ["M {id}: batch the restock. We expect fewer empty slots.\n",
                                                           "M {id}: restated.\n\nPrediction: revenue up within 2 points\n"]})
assert any(e["event"] == "prediction_problem" for e in ev)
assert any(r["key"] == "prediction-m-001" for r in mem["ledger"]["reqs"])
assert any(e["event"] == "prediction_restated" and e["id"] == "M-001" for e in ev), [e for e in ev if "predict" in e["event"]]
assert any(e["event"] == "change_verdict" and e["id"] == "M-001" for e in ev)
ev, st, mem, sw = run(60, dry={"pulse": ask_d, "method": "M {id}\n\nPrediction: empty_slots down within 2 points\n"})
assert any(e["event"] == "prediction_problem" and "does not chart" in (e.get("problem") or "") for e in ev)

# Unit checks.
assert ledger.parse_requests("x\n## Requests\n- to: Controls | key: A B | do it\n- nonsense\n") == [{"to": "controls", "key": "a-b", "text": "do it"}]
assert ledger.parse_dispositions("## Dispositions\n- REQ-002: declined | fixed by sim\n")["REQ-002"] == ("declined", "fixed by sim")
assert facts.parse_split("## Capacity split\n- 75% fills: mcp__v__restock_machine, check\n")[0]["tools"] == ["restock_machine", "check"]
assert profile.validate("checker", "off", {"checker": "sample_claims"}, {"checker": ["off", "sample_claims"]}) == (True, "off")
print("all v4 engine tests passed")
