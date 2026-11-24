As of day 26 (point 4, after S-001)   Constraint: stocked, priced, margin-positive slots. Worker time is not the limit (median 230 of 480 min used; ~250 idle). Capital is idle (~1,233 of 1,335).

| Driver | Now (charts, day 26) | Aim for point 4 (day 28) | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| M0 Final cash | EUR 1,401.8 | at least EUR 1,366. Already met on day 26; raise at the next aim update | — | cash ≥ EUR 120 every day; no order that takes cash below it |
| D1 slots_selling (margin-positive only) | 11 selling (see AS-001: 5 stocked at day end does not reconcile) | 15 selling | 56%: refills, 6 × 45 min = 270 min | no slot stocked below unit cost; no duplicate slot beyond sell-through |
| D2 revenue_per_slot | 10.32 latest; own best 9.34 | 8.8 as set by S-001; it is below the current figure, so hold it, and the Strategist restates | 16%: swaps, price, mix, 75 min | price ≥ unit cost on every slot |
| D3 unit_cost_paid_30d | not in S-001; collecting | no new aim; first order at or below quoted offer, falling vs first order | 13%: orders and reads, 63 min | no order that breaks the reserve |
| D4 worker minutes on selling work | 230 median used | 408 used (270 + 75 + 63); slack 72 kept | 15% slack, 72 min kept unused | never above 408 used |

Notes, what to do first each period:
1. Read the sales report and the bank before any trip each day.
2. Spend spare minutes first on refills of empty slots, each with a checked, margin-positive product from a current offer. Log refill quantity and clock cost of each call.
3. Set each slot's price at or above unit cost. Prices are read from sales, not tested: no experiments.
4. Order only what the cash reserve allows (EUR 120), and record unit cost paid per order.
5. Keep 72 min/day unused. Do not spend it on extra calls.
6. The day-30 reference (EUR 3,228) is not reachable as the work is done. Margin needs a design change (AS-001). Do not chase it by overbuying stock.
