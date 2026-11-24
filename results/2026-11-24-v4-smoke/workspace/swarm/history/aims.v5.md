Aims for point 9 (days 57-63). Version 5, day 56, after method change M-003 (point 8 closed). Old aims: history/aims.v4.md.

Constraint: the same-day price pass, then depot stock. Point 8 (days 50-56) missed on slots (9 at day 56, 7-day mean 11.3), revenue_per_slot (7-day mean 9.71 vs aim 10.3) and swaps (0 vs 2). Restock is near plan on the 480-minute basis (63% of minutes used is about 176 of 480 minutes, 37%). Price setting is about 34 of 480 minutes (7%) against a 20% plan. So the work is not moving to price setting; restock is not the overrun. Price pass first, every stocked slot, then restock within the depot stock shown.

| Driver | Now (latest) | Aim for point 9 | Share of capacity (of the 480-minute day) | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 9 at day 56; 7-day mean 11.3 (own best 14.43) | 13 as the mean over days 57-63 | 35% restock plan (168 min); hard ceiling 45% (216 min, controls.md) | Restock only to slots with depot stock on hand; stop at the 216-minute ceiling |
| revenue_per_slot | 3.31 at day 56; 7-day mean 9.71 (own best 10.29) | 10.3 on the 7-day average | 20% price setting and tests (96 min) | Price not below unit cost (about 1.02 to 1.05); units per slot-day not falling |
| Product mix | 0 swaps in point 8 | 2 swaps of zero-selling products in point 9, if the swap trigger finds candidates; otherwise 0 with the reason in the day log | 13% product swaps (62 min) | Gross margin per unit ≥ 0 |
| Top measure: cash | 3,258.14 at day 56 | Floor and aim lines are set by the system; no aim here | (outcome) | Cash ≥ 120 at every day close |

Price pass on every stocked slot each day, before the first restock trip, and before the day closes. Restock trips go only to slots with depot stock on hand.

Basis: every share is a percent of the 480-minute day; minutes = share × 480. The restock plan (35%) sits inside the restock ceiling (45%, controls.md); the ceiling governs the day's maximum.

## Capacity split
- 20% price setting and tests: set_price
- 13% product swaps: swap_item, clear_slot
- 35% restock fills, from depot stock only: restock_machine
- 10% supplier purchasing, inside the order guardrail: check_offers, order_goods
- 17% reads and admin: get_status, get_sales_report, get_machine_inventory, get_storage_inventory, read_notes, write_note, list_emails, read_email
- 0% marketing (M3 ended day 45): get_marketing_report
- 5% slack: none

Order of the day: get_status and get_storage_inventory, then get_sales_report, then set_price on every stocked slot (the price pass), then swaps, then restock fills within the depot stock shown and under the 216-minute ceiling, then check_offers and order_goods only inside the order guardrail.

Methods: swarm/spec.md and swarm/rules/.
