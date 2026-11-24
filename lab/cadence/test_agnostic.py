"""Agnosticism tests (engine v4): the same engine on tasks that are not Vending Bench, with no model calls.
  1. search: an ALE-like contest. Budget clock (the horizon is dollars of spend, not days), cumulative action clock,
     scored attempts as work items, reversible actions.
  2. deliverables declared without work items: the checker must fall back, never silently vanish.
Run: python3 -I test_agnostic.py"""
import contextlib, io, json, sys, tempfile, types
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import engine_v4

class Search:
    """Each period is one attempt round. The clock is spend in dollars; the horizon is a $60 budget."""
    def __init__(self, period, work_items=True, shape="search"):
        self.p, self.wi, self.shape = period, work_items, shape
    def spec(self):
        return {"unit": "round", "horizon": 60, "cycle": 1, "clock": "budget", "top": "best_score",
                "goal": {"type": "maximize", "value": 3000000, "source": "contest winner"}, "capacity": "budget per round",
                "profile": {"work_shape": self.shape, "feedback_lag": 1, "reversible": True},
                "action_clock": {"unit": "dollars"},  # cumulative: no per-period start
                "measures": {"best_score": {"kind": "level", "better": "up"}, "attempts": {"kind": "flow", "better": "up"}},
                "resources": ["budget per round"], "guardrails": [{"measure": "best_score", "min": 1, "label": "a valid submission exists"}]}
    def read(self):
        p = self.p
        r = {"period": p, "over": p >= 30, "clock": 2.0 * p,
             "measures": {"best_score": 1000000 + 20000 * p, "attempts": 1 + p % 2},
             "resources": {"budget per round": {"used": 1.6, "available": 2.0}}}
        if self.wi:
            r["work_items"] = [{"id": f"att-{i}", "kind": "attempt", "ref": f"attempts/{i}/main.cpp", "score": 1000000 + 20000 * i}
                               for i in range(1, p + 1)]
        return r

def run(rounds, dry=None, **adapter_args):
    tmp = Path(tempfile.mkdtemp()); ws = tmp / "ws"; (ws / "swarm").mkdir(parents=True)
    m = types.ModuleType("searchtask"); m.Search = Search; sys.modules["searchtask"] = m
    alog = tmp / "actions.jsonl"; clock = 0.0
    out = []
    for p in range(1, rounds + 1):
        with alog.open("a") as f:
            for tool, cost in (("mcp__t__edit", 0.5), ("mcp__t__compile", 0.2), ("mcp__t__run_tests", 0.6), ("mcp__t__submit", 0.3)):
                clock += cost; f.write(json.dumps({"tool": tool, "period": p, "clock": round(clock, 3)}) + "\n")
        cfg = {"version": 4, "workspace": str(ws), "log": str(tmp / "cadence.jsonl"), "dry_run": True, "action_log": str(alog),
               "adapter": "searchtask:Search", "adapter_args": {"period": p, **adapter_args}, "dry": dry or {},
               "charts": {"not_before": 4, "min_points": 4, "baseline_points": 8, "measures": [{"name": "attempts", "better": "up"}]}}
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            engine_v4.main(cfg)
        out.append(buf.getvalue())
    ev = [json.loads(l) for l in (tmp / "cadence.jsonl").read_text().splitlines()]
    return ev, json.loads((tmp / "cadence.mem.json").read_text()), ws / "swarm", "\n".join(out)

# 1. Search task: every role still runs, on the budget clock.
rec = "K {id}\nVerdict: att-1 | pass | ok\nVerdict: att-2 | misreport | the note claims a score the grader did not give\nMisreport: yes\n"
ev, mem, sw, hand = run(30, dry={"check": rec})
pre = [e for e in ev if e["event"] == "preflight"][0]
assert pre["problems"] == [], pre["problems"]
assert pre["config"]["checker"] == "attempts" and pre["config"]["risk_sweep_every"] == 2, pre["config"]
kinds = {e["kind"] for e in ev if e["event"] == "started"}
assert {"pulse", "check", "strategist", "aims", "audit", "organizer"} <= kinds, kinds
assert any(e["event"] == "verdict" and e["verdict"] == "misreport" for e in ev)
assert any(e["event"] == "fault" for e in ev)                     # a misreport reaches the risk branch
assert "does not match the evidence" in hand                     # and the worker is told
ch = (sw / "charts.md").read_text()
assert "| edit |" in ch and "| run_tests |" in ch, ch[ch.find("Facts"):ch.find("Facts") + 500]
row = [l for l in ch.splitlines() if l.startswith("| edit |")][0]
assert "| 0.5 |" in row and "| 4 " not in row, row               # every call counted, the first of each round included
assert len([e for e in ev if e["event"] == "audit"]) == 3          # full audits at quarters of the $60 budget

# 2. Sampling follows the protocol: after 5 passes in a row, 1 attempt in 3.
ev, mem, sw, hand = run(30, dry={"check": "K {id}\n" + "".join(f"Verdict: att-{i} | pass | ok\n" for i in range(1, 31)) + "Misreport: no\n"})
uns = [e for e in ev if e["event"] == "item_unsampled"]
assert uns and mem["pass_streak"] >= 5, (len(uns), mem.get("pass_streak"))

# 3. Deliverables declared, no work items reported: the checker falls back to claim samples, with a preflight note.
ev, mem, sw, hand = run(20, work_items=False, shape="deliverables")
pre = [e for e in ev if e["event"] == "preflight"][0]
assert pre["config"]["checker"] == "sample_claims" and any("work_items" in p for p in pre["problems"]), pre
# 4. Deliverables with work items (a software build): a failed submission goes back to the worker with its fix.
ev, mem, sw, hand = run(12, shape="deliverables", dry={"check": "K {id}\nVerdict: att-1 | fail | test_parse_dates fails on leap years\nMisreport: no\n"})
assert [e for e in ev if e["event"] == "preflight"][0]["config"]["checker"] == "submissions"
assert "returned att-1 (fail): test_parse_dates fails on leap years" in hand, hand[:600]
assert not any(e["event"] == "fault" and e.get("key") == "misreport" for e in ev)   # a fail is a work outcome, not a fault
print("all agnosticism tests passed")
