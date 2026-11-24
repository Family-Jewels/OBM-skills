As of day 0 (initial design, D-0; no strategy yet)   Constraint: worker time (480 min per working day; restock is 45 min a trip), with deployable cash (EUR 1,380 above reserve) as the second limit

| Driver | Now | Aim for the next point | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| Final cash (top measure) | EUR 1,500 | Cash at or above the rising aim line; exemplar pace is EUR 3,228 by day 30 | (outcome, not a share) | Cash ≥ EUR 120 at every day close |
| Stock-out slot-days | measured on day 1 | Below 25% of priced slots over 7 days | 50% restock fills | Gross margin per unit ≥ 0 |
| revenue_per_slot | measured on day 1 | Up 10% from day-1 level by the second week, through price tests and product mix | 10% price setting | Units per slot-day must not fall |
| unit_cost_paid_30d | measured from the first receipt | Lowest available across suppliers at comparable quantity, from M2 | 10% purchasing | Sell-through ≥ 60%; cash ≥ reserve after each order |
| Marketing lift | not yet readable | Not a driver until M3; test once per location in M3 | 5% (the M3 test; idle until then) | Cost recovered within 14 days |

## Capacity split
- 50% restock fills of demanded or near-empty slots: restock_machine
- 15% product swaps out of non-selling slots: swap_item, clear_slot
- 10% price setting and price tests: set_price
- 10% supplier purchasing: search_web, check_offers, order_goods, and the supplier email tool (name as the Facts table lists it on first use)
- 10% reads and admin: get_status, get_machine_inventory, get_sales_report, get_marketing_report, read_notes, write_note, send_payment
- 5% marketing: run_marketing

Notes: First each day, read get_status and get_sales_report (reads), then fill the slots with stock-outs at the highest revenue_per_slot, then set prices for newly stocked slots, then order only when check_offers shows a price inside the guardrail. Spend the day's remaining minutes on the capacity split; advance with wait_for_next_day only after the day's reads and fills. The M1 price test (T-0004) and the first supplier comparison (T-0002) come before any large order.
