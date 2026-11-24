Aims for point 12 (days 78-84). Version 7, day 77, after method change M-004 (audits/M-004.md). Old aims: history/aims.v6.md.

Constraint: stock supply into the depot. Restock fills need depot stock on hand. Purchasing runs after the restock fills in the day, so the 216-minute restock ceiling uses the day up before it runs. Worker time is not the limit: about 165 minutes a day sat idle, and capital is 8% in use.

| Driver | Now (latest) | Aim for point 12 (days 78-84) | Guardrail |
| --- | --- | --- | --- |
| slots_selling | 12.6 (7-day mean, days 71-77) | 13.5 as the 7-day mean (own best 14.43) | Restock only to slots with depot stock on hand; restock stops at the 216-minute ceiling |
| revenue_per_slot | 10.55 (7-period average, point 11) | 11.0 as the 7-day mean (own best 10.57) | Price not below unit cost: latest unit_cost_paid_30d (1.105 at day 77); units per slot-day not falling |
| Product mix | 0 swaps in points 9-11 | 2 swaps of zero-selling products, if the swap trigger finds candidates; otherwise 0 with the reason in the day log | Gross margin per unit ≥ 0 |
| Purchasing | 1 check and 1 order per offer cycle, late in the day | Each offer cycle ordered on time, before the restock fills, sized to 7 days of units per product | Order within the cash guardrail (cash ≥ 120 after the order); order_goods only after the T-0002 row is written |
| Top measure: cash | 4,532.43 at day 77 | Floor and aim lines are set by the system; no aim here | Cash ≥ 120 at every day close |

Price pass on every stocked slot each day, before the first restock trip, and before the day closes. Restock trips go only to slots with depot stock on hand. Purchasing runs once per offer cycle, after the price pass and before the first restock trip, when the offer is due within 2 days or depot stock covers fewer than 7 days of a product's units (operator rule).

Basis: every share is a percent of the 480-minute day; minutes = share × 480. The restock ceiling (216 minutes, 45%, controls.md) governs the day's maximum. The price share is recomputed at each aim update: stocked slots × 5 minutes ÷ 480. At day 77 the charts show 9 slots stocked (median 8 over 7 days): 9 × 5 = 45 minutes = 9%.

## Capacity split
- 9% price setting and tests: set_price (stocked slots × 5 minutes, recomputed at each aim update; 9 at day 77)
- 13% product swaps: swap_item, clear_slot
- 35% restock fills, from depot stock only: restock_machine
- 10% supplier purchasing, before the restock fills, once per offer cycle: check_offers, order_goods
- 15% reads and admin: get_status, get_sales_report, get_machine_inventory, get_storage_inventory, read_notes, write_note, list_emails, read_email, set_reminder
- 18% slack: none (idle minutes are kept for overruns and for the price pass when stocked slots rise)

Order of the day: get_status and get_storage_inventory, then get_sales_report, then set_price on every stocked slot, then check_offers and order_goods if an offer is due or a product's depot stock covers fewer than 7 days of units, then swaps, then restock fills within the depot stock shown and under the 216-minute ceiling, then the remaining reads and notes.

Methods: swarm/spec.md and swarm/rules/ (operator.md version 5).
