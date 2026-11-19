"""Replay engine v2 on a recorded run, with no model calls, to see what it would have triggered and when.

usage: python3 -I replay.py <recorded run folder> <scratch folder> [ceiling]
Reads the run's swarm/metrics_system.md (written by the system each period) and feeds it to engine v2 one row at a time,
in dry-run mode (each review "finishes" at once with a neutral report). Prints the event counts and the periods of each.
"""
import json, subprocess, sys, shutil
from pathlib import Path
HERE = Path(__file__).resolve().parent

class Rows:
    """Adapter over a recorded metrics table; spec() from the vending adapter, no resources."""
    def __init__(self, table, row, horizon, ceiling):
        self.rows = [l for l in Path(table).read_text().splitlines() if l.startswith("| ") and l[2:3].isdigit()]
        self.head = [h.strip() for h in Path(table).read_text().splitlines()[2].strip("|").split("|")]
        self.i = int(row); self.h = horizon; self.c = ceiling
    def spec(self):
        sys.path.insert(0, str(HERE)); from adapters.vending import VendingState
        return VendingState("/dev/null", self.h, self.c, "replay").spec()
    def read(self):
        cells = [c.strip() for c in self.rows[self.i].strip("|").split("|")]
        m = {}
        for h, c in zip(self.head[1:], cells[1:]):
            try: m[h] = float(c)
            except ValueError: m[h] = None
        return {"period": int(cells[0]), "over": self.i == len(self.rows) - 1, "measures": m}

def main():
    run, scratch = Path(sys.argv[1]), Path(sys.argv[2]); ceiling = float(sys.argv[3]) if len(sys.argv) > 3 else 61219
    table = run / "workspace" / "swarm" / "metrics_system.md"
    n = len(Rows(table, 0, 365, ceiling).rows)
    if scratch.exists(): shutil.rmtree(scratch)
    (scratch / "ws").mkdir(parents=True)
    for i in range(n):
        cfg = {"version": 2, "workspace": str(scratch / "ws"), "log": str(scratch / "cadence.jsonl"), "dry_run": True,
               "adapter": "replay:Rows", "dry_run_redesign": True, "adapter_args": {"table": str(table), "row": i, "horizon": 365, "ceiling": ceiling},
               "charts": {"not_before": 8, "min_points": 8, "baseline_points": 20, "measures": [
                   {"name": "cash_gain_7", "from": "cash", "diff": 7, "better": "up"}, {"name": "revenue", "better": "up"},
                   {"name": "slots_selling", "better": "up"}, {"name": "revenue_per_slot", "better": "up"}, {"name": "units", "better": "up"}]}}
        (scratch / "cfg.json").write_text(json.dumps(cfg))
        p = subprocess.run([sys.executable, "-I", str(HERE / "engine.py"), str(scratch / "cfg.json")], input="{}", text=True,
                           capture_output=True, cwd=HERE, env={"PYTHONPATH": str(HERE)})
        if p.returncode:
            print(p.stderr); sys.exit(1)
    ev = [json.loads(l) for l in (scratch / "cadence.jsonl").read_text().splitlines()]
    started = {}
    for e in ev:
        if e["event"] == "started":
            started.setdefault(e["kind"], []).append(e["period"])
    for k, v in started.items():
        print(f"{k:12s} {len(v):3d}  at {v}")
    for k in ("preflight", "aim_raised", "guardrail", "diagnosis_deferred"):
        xs = [e for e in ev if e["event"] == k]
        if xs: print(k, len(xs), [x.get("period") for x in xs][:12], xs[0].get("problems", xs[0].get("label", "")))
    print("progress flags by kind:", {k: sum(1 for e in ev if k in (e.get("progress") or [])) for k in ("below_floor", "flat_or_wrong", "below_own_line", "aim_raised")})

if __name__ == "__main__":
    main()
