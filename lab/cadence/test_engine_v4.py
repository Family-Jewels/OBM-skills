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
# Deferred requests are answered and held, never closed; repeats still escalate by count.
ev, st, mem, sw = run(84, dry={"pulse": ask, "disposition": "deferred"})
assert all(r["status"] in ("open", "in_progress", "deferred") for r in mem["ledger"]["reqs"]), mem["ledger"]["reqs"]
assert sum(1 for r in mem["ledger"]["reqs"] if r["key"] == "chart-minutes") == 1   # never queued twice
assert any(e["event"] == "escalation" and "asked" in e["text"] for e in ev)
# Unanswered requests (no disposition) go back to open and escalate by age.
once = "Pulse {id}.\nFault: no\n" + "\n## Requests\n- to: designer | key: once | Chart it.\n"
L0 = ledger.Ledger({}); L0.file("P-1", ledger.parse_requests(once), 1, 7); L0.take(L0.open_for("designer"), "M-1")
assert L0.answer("M-1", "## Dispositions\n", 1) == [("REQ-001", "open")]
assert [w for _, w in L0.escalations(4)] == ["unanswered 3 points"]
# A request filed inside the method lane's gap is answered at once (answer-only), not left waiting to escalate.
L1 = ledger.Ledger({}); L1.file("P-1", ledger.parse_requests(once), 5, 35); L1.take(L1.open_for("designer"), "M-2")
assert L1.answer("M-2", "## Dispositions\n- REQ-001: deferred | will chart it at point 8\n", 5, 8) == [("REQ-001", "deferred")]
assert L1.escalations(7) == [] and L1.open_for("designer") == []
L1.release(8); assert [r["id"] for r in L1.open_for("designer")] == ["REQ-001"] and L1.escalations(8) == []
ev, st, mem, sw = run(84, dry={"pulse": ask, "disposition": "deferred"})
assert not any(e["event"] == "escalation" and "unanswered" in e["text"] for e in ev), [e["text"] for e in ev if e["event"] == "escalation"]

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

# Unit checks.
assert ledger.parse_requests("x\n## Requests\n- to: Controls | key: A B | do it\n- nonsense\n") == [{"to": "controls", "key": "a-b", "text": "do it"}]
assert ledger.parse_dispositions("## Dispositions\n- REQ-002: declined | fixed by sim\n")["REQ-002"] == ("declined", "fixed by sim")
assert facts.parse_split("## Capacity split\n- 75% fills: mcp__v__restock_machine, check\n")[0]["tools"] == ["restock_machine", "check"]
assert profile.validate("checker", "off", {"checker": "sample_claims"}, {"checker": ["off", "sample_claims"]}) == (True, "off")

# 8. Records decorated with markdown parse the same as plain ones.
import mdtext
assert ledger.parse_requests("**Requests**\n- to: `designer` | key: `x-y` | do it\n") == [{"to": "designer", "key": "x-y", "text": "do it"}]
assert ledger.parse_dispositions("## Dispositions (2)\n- **REQ-004**: done | added\n")["REQ-004"][0] == "done"
assert facts.parse_split("## Capacity split:\n- **60%** fills: `restock_machine`\n* 40% orders: order\n")[1]["planned"] == 0.4
assert "Fault: yes" in mdtext.plain("**Fault: yes**") and "Fault key: cash-low" in mdtext.plain("*Fault key:* `cash-low`")
assert mdtext.plain("* bullet stays\n5 * 3") == "* bullet stays\n5 * 3"
bold = "Pulse {id}.\n**Fault: yes**\n**Fault key:** `unpriced-slots`\n\n**Corrections**\n- price slot 3\n"
ev, st, mem, sw = run(35, dry={"pulse": bold})
assert any(e["event"] == "fault" and e["key"] == "unpriced-slots" for e in ev), [e for e in ev if e["event"] == "fault"]
ev, st, mem, sw = run(100, dry={"organizer": "**Config change:** `strategy_every = 2`\nreason"})
assert mem["config"]["strategy_every"] == 2

# 9. A diagnosis that names the designer as the owner of the change is not also filed to the controls owner.
to_des = "D {id}\n\n## Requests\n- to: designer | key: day-order | the aims starve prices\n"
ev, st, mem, sw = run(70, dry={"pulse": flt, "diagnosis": to_des})
reqs = mem["ledger"]["reqs"]
assert any(r["to"] == "designer" and r["key"] == "day-order" for r in reqs) and not any(r["to"] == "controls" for r in reqs), reqs
assert "controls" not in st, st.get("controls")

# 10. Actions named in the capacity split but never called are shown as measured zero.
ev, st, mem, sw = run(35, dry={"aims_md": "# Aims\n\n## Capacity split\n- 80% fills: fill\n- 20% swaps: swap\n"}, actions=lambda d: [("mcp__t__fill", 45, 4)])
assert "never called (0 calls, measured): swap" in (sw / "charts.md").read_text()
# 11. Pursuit is on the plan's basis: shares of the capacity of the days worked, with slack compared to unused capacity.
sp = facts.parse_split("## Capacity split\n- 50% fills: fill\n- 20% slack: none\n")
cs = [(1, "fill", 240), (1, "read", 96), (2, "fill", 240), (2, "read", 96)]   # 336 of 480 minutes used each day
rows = {r["label"]: r for r in facts.pursuit(sp, cs, 2, 7, 480)}
assert abs(rows["fills"]["actual"] - 0.5) < 1e-9 and abs(rows["slack"]["actual"] - 0.3) < 1e-9 and abs(rows["other (not in the split)"]["actual"] - 0.2) < 1e-9, rows
rows = {r["label"]: r for r in facts.pursuit(facts.parse_split("## Capacity split\n- 50% fills: fill\n"), cs, 2, 7, 480)}
assert abs(rows["unused capacity"]["actual"] - 0.3) < 1e-9, rows
rows = {r["label"]: r for r in facts.pursuit(sp, cs, 2, 7)}   # no capacity reported: shares of what was spent
assert abs(rows["fills"]["actual"] - 480 / 672) < 1e-9
# 12. The Requests table always lists every live request, however many were closed recently.
L2 = ledger.Ledger({})
for i in range(30):
    L2.file("P-1", [{"to": "designer", "key": f"k{i}", "text": "x"}], 1, 7)
L2.take(L2.open_for("designer")[5:], "M-1"); L2.answer("M-1", "## Dispositions\n" + "".join(f"- REQ-{i:03d}: done | ok\n" for i in range(6, 31)), 2)
tab = L2.table(2)
assert all(f"REQ-{i:03d}" in tab for i in range(1, 6)), tab
print("all v4 engine tests passed")
