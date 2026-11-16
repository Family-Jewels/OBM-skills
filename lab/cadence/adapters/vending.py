"""Adapter for Prosus Vending Bench: a period is a simulated day, read from the simulator's own state file."""
import json
from pathlib import Path

class VendingState:
    def __init__(self, state_path):
        self.p = Path(state_path)

    def read(self):
        try:
            s = json.loads(self.p.read_text())
        except Exception:
            return None
        sl = s.get("sales_log", []); last = sl[-1] if sl else {}
        d = last.get("day", 0)
        rev = lambda lo, hi: round(sum(x["revenue"] for x in sl if lo <= x["day"] <= hi), 2)
        return {"period": s.get("day") or 0, "over": bool(s.get("finished") or s.get("terminated")),
                "measures": {"cash": round(s.get("balance", 0), 2), "revenue": last.get("revenue", 0), "units": last.get("units", 0),
                             "slots_selling": len(last.get("per_slot", [])),
                             "revenue_per_slot": round(last.get("revenue", 0) / len(last["per_slot"]), 2) if last.get("per_slot") else 0, "revenue_last_7": rev(d - 6, d),
                             "revenue_same_7_a_month_earlier": rev(d - 36, d - 30) if d > 36 else None}}
