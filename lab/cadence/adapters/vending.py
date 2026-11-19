"""Adapter for Prosus Vending Bench: a period is a simulated day, read from the simulator's own state file.

read() is unchanged for engine v1. Engine v2 also uses spec() and the 'resources' in each reading (see ADAPTER_SPEC.md).
"""
import json
from pathlib import Path

class VendingState:
    def __init__(self, state_path, horizon=365, ceiling=None, ceiling_source=None, daily_fee=12.0, max_unpaid_days=10):
        self.p = Path(state_path); self.horizon = horizon
        self.ceiling, self.ceiling_source = ceiling, ceiling_source
        self.reserve = daily_fee * max_unpaid_days  # below this the business is at risk of termination for non-payment

    def spec(self):
        """Task facts for engine v2: horizon, natural cycle, clock, goal, measures, guardrails."""
        return {
            "unit": "day", "horizon": self.horizon,
            "cycle": 7,  # demand has a day-of-week pattern, so a point holds whole weeks
            "clock": "period",
            "top": "cash",
            "goal": {"type": "maximize", "value": self.ceiling, "source": self.ceiling_source or "none given"},
            "measures": {
                "cash": {"kind": "level", "better": "up"},           # the bank balance: positive, so it can go on a log scale
                "revenue": {"kind": "flow", "better": "up"},         # euros a day
                "units": {"kind": "flow", "better": "up"},
                "slots_selling": {"kind": "level", "better": "up"},
                "revenue_per_slot": {"kind": "flow", "better": "up"},
            },
            "resources": ["selling slots", "capital"],
            "guardrails": [{"measure": "cash", "min": self.reserve,
                            "label": f"cash reserve: {self.reserve:.0f} covers the fees for the days the building tolerates unpaid"}],
        }

    def read(self):
        try:
            s = json.loads(self.p.read_text())
        except Exception:
            return None
        sl = s.get("sales_log", []); last = sl[-1] if sl else {}
        d = last.get("day", 0)
        rev = lambda lo, hi: round(sum(x["revenue"] for x in sl if lo <= x["day"] <= hi), 2)
        mach = s.get("machine", {}) or {}; store = s.get("storage", {}) or {}
        stock_value = sum((v.get("quantity") or 0) * (v.get("unit_cost") or 0) for v in mach.values())
        stock_value += sum((b.get("quantity") or 0) * (b.get("unit_cost") or 0) for v in store.values() for b in v.get("batches", []))
        bal = s.get("balance", 0)
        return {"period": s.get("day") or 0, "over": bool(s.get("finished") or s.get("terminated")),
                "measures": {"cash": round(bal, 2), "revenue": last.get("revenue", 0), "units": last.get("units", 0),
                             "slots_selling": len(last.get("per_slot", [])),
                             "revenue_per_slot": round(last.get("revenue", 0) / len(last["per_slot"]), 2) if last.get("per_slot") else 0, "revenue_last_7": rev(d - 6, d),
                             "revenue_same_7_a_month_earlier": rev(d - 36, d - 30) if d > 36 else None},
                "resources": {
                    "selling slots": {"used": sum(1 for v in mach.values() if (v.get("quantity") or 0) > 0), "available": len(mach) or None},
                    "capital": {"used": round(stock_value, 2), "available": round(stock_value + max(0.0, bal - self.reserve), 2)},
                }}
