"""Adapter for Prosus Vending Bench: a period is a simulated day, read from the simulator's own state file.

read() keeps every v1 measure. Engine v2 also uses spec(), snapshot(), and the 'resources' and per-machine 'units' in each
reading (see ADAPTER_SPEC.md). A unit is one machine (a location's snack or drinks machine), so experiments can run on some
machines with the rest as control.
"""
import json
from pathlib import Path

class VendingState:
    DAY_MINUTES = 480  # the working day, 09:00 to 17:00: the worker's capacity

    def __init__(self, state_path, horizon=365, ceiling=None, ceiling_source=None, daily_fee=12.0, max_unpaid_days=10, clock_log=None,
                 storage_measure=False):
        self.p = Path(state_path); self.horizon = horizon
        self.storage_measure = storage_measure  # v1.1: units waiting in the storage room, so a design can see stock not yet loaded
        self.clock_log = Path(clock_log) if clock_log else None
        self.ceiling, self.ceiling_source = ceiling, ceiling_source
        self.reserve = daily_fee * max_unpaid_days  # below this the business is at risk of termination for non-payment

    def spec(self):
        """Task facts for engine v2: horizon, natural cycle, clock, goal, measures, guardrails."""
        return {
            "unit": "day", "horizon": self.horizon,
            "cycle": 7,  # demand has a day-of-week pattern, so a point holds whole weeks
            "clock": "period",
            "period_end_tool": "mcp__vending__wait_for_next_day",  # the tool that ends the working day
            "top": "cash",
            "goal": {"type": "maximize", "value": self.ceiling, "source": self.ceiling_source or "none given"},
            "measures": {
                "cash": {"kind": "level", "better": "up"},           # the bank balance: positive, so it can go on a log scale
                "revenue": {"kind": "flow", "better": "up"},         # euros a day
                "units": {"kind": "flow", "better": "up"},
                "slots_selling": {"kind": "level", "better": "up"},
                "revenue_per_slot": {"kind": "flow", "better": "up"},
                "unit_cost_paid_30d": {"kind": "level", "better": "down"},  # euros per unit across purchase orders paid in the last 30 days
                **({"units_in_storage": {"kind": "level", "better": "down"}} if self.storage_measure else {}),
            },
            "unit_name": "machine",
            "unit_measures": {  # per machine, for experiments on a slice with the other machines as control
                "machine_revenue": {"kind": "flow", "better": "up"},
                "machine_units": {"kind": "flow", "better": "up"},
                "machine_stocked_slots": {"kind": "level", "better": "up"},
            },
            "resources": ["worker time (minutes a day)", "slots stocked at day end", "capital"],
            "capacity": "worker time (minutes a day)",  # the worker's own capacity: every fill, check and experiment draws on it
            "experiment_share": 0.10,
            "resource_sources": {
                "worker time (minutes a day)": "the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used)",
                "slots stocked at day end": "the simulator's machine state",
                "capital": "the simulator's balance and the cost of stock on hand",
            },
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
        paid = [o for o in (s.get("orders") or {}).values() if o.get("paid_day") is not None and o["paid_day"] > (s.get("day") or 0) - 30]
        q = sum(l.get("quantity", 0) for o in paid for l in o.get("lines", []))
        cost30 = round(sum(o.get("amount_paid") or o.get("total") or 0 for o in paid) / q, 3) if q else None
        units = {}
        for slot, v in mach.items():
            m = slot.rsplit(":", 1)[0]
            u = units.setdefault(m, {"machine_revenue": 0.0, "machine_units": 0, "machine_stocked_slots": 0})
            u["machine_stocked_slots"] += 1 if (v.get("quantity") or 0) > 0 else 0
        for x in last.get("per_slot", []):
            u = units.setdefault(x.get("machine") or x["slot"].rsplit(":", 1)[0], {"machine_revenue": 0.0, "machine_units": 0, "machine_stocked_slots": 0})
            u["machine_revenue"] = round(u["machine_revenue"] + x.get("revenue", 0), 2); u["machine_units"] += x.get("units", 0)
        return {"period": s.get("day") or 0, "over": bool(s.get("finished") or s.get("terminated")),
                "measures": {"cash": round(bal, 2), "revenue": last.get("revenue", 0), "units": last.get("units", 0),
                             "slots_selling": len(last.get("per_slot", [])),
                             "revenue_per_slot": round(last.get("revenue", 0) / len(last["per_slot"]), 2) if last.get("per_slot") else 0, "revenue_last_7": rev(d - 6, d),
                             "revenue_same_7_a_month_earlier": rev(d - 36, d - 30) if d > 36 else None, "unit_cost_paid_30d": cost30,
                             **({"units_in_storage": sum((v.get("quantity") or 0) for v in store.values())} if self.storage_measure else {})},
                "units": units,
                "resources": {
                    "worker time (minutes a day)": {"used": self._minutes_used(s.get("day") or 0), "available": self.DAY_MINUTES},
                    "slots stocked at day end": {"used": sum(1 for v in mach.values() if (v.get("quantity") or 0) > 0), "available": len(mach) or None},
                    "capital": {"used": round(stock_value, 2), "available": round(stock_value + max(0.0, bal - self.reserve), 2)},
                }}

    def on_period_end(self):
        """Called by the system just before the working day ends: note the simulator's clock, for the worker's time used."""
        if not self.clock_log:
            return
        try:
            s = json.loads(self.p.read_text())
            with self.clock_log.open("a") as f:
                f.write(json.dumps({"day": s.get("day"), "minute": s.get("minute")}) + "\n")
        except Exception:
            pass

    def snapshot(self):
        """Ground truth of what the operator controls, for fidelity checks: every machine slot and the storage room."""
        try:
            s = json.loads(self.p.read_text())
        except Exception:
            return "(state unreadable)"
        rows = ["| slot | product | price | quantity | unit cost | loaded day |", "| --- | --- | --- | --- | --- | --- |"]
        for slot, v in sorted((s.get("machine") or {}).items()):
            rows.append(f"| {slot} | {v.get('product_id') or '—'} | {v.get('price') if v.get('price') is not None else '—'} | "
                        f"{v.get('quantity') or 0} | {v.get('unit_cost') if v.get('unit_cost') is not None else '—'} | {v.get('loaded_day') or '—'} |")
        mk = s.get("marketing") or []
        if mk:
            rows += ["", "| marketing campaign | detail |", "| --- | --- |"]
            for c in (mk if isinstance(mk, list) else list(mk.values()))[-20:]:
                rows.append(f"| {c.get('id', '—') if isinstance(c, dict) else '—'} | {json.dumps(c)[:300] if isinstance(c, dict) else str(c)[:300]} |")
        rows += ["", "| storage product | quantity | batches (quantity @ unit cost, received day) |", "| --- | --- | --- |"]
        for pid, v in sorted((s.get("storage") or {}).items()):
            b = "; ".join(f"{x.get('quantity')} @ {x.get('unit_cost')}, day {x.get('received_day')}" for x in v.get("batches", []))
            rows.append(f"| {pid} | {v.get('quantity') or 0} | {b or '—'} |")
        rows += ["", "| order | supplier | status | paid day | due day | delivered day | lines |", "| --- | --- | --- | --- | --- | --- | --- |"]
        for oid, o in sorted((s.get("orders") or {}).items())[-15:]:
            ln = "; ".join(f"{l.get('product_id')} {l.get('quantity')} @ {l.get('unit_price')}" for l in o.get("lines", []))
            rows.append(f"| {oid} | {o.get('supplier_name') or o.get('supplier_id')} | {o.get('status')} | {o.get('paid_day')} | "
                        f"{o.get('delivery_day')} | {o.get('delivered_day')} | {ln} |")
        return "\n".join(rows) + "\n"

    def _minutes_used(self, day):
        """Minutes of the working day used on the last completed day, from the simulator's clock read just before the day
        ended. A day missing from the log rolled over by itself, because the worker's calls ran past 17:00: all used."""
        if not self.clock_log or day <= 1:
            return None
        rec = {}
        try:
            for line in self.clock_log.read_text().splitlines():
                r = json.loads(line); rec[r["day"]] = r["minute"]
        except Exception:
            return None
        m = rec.get(day - 1)
        return self.DAY_MINUTES if m is None else max(0, min(self.DAY_MINUTES, m - 540))
