Aims for point 10 (days 64-70). Version 6, day 65, after redirect S-004 (AS-004). Old aims: history/aims.v5.md.

Constraint: stock supply into the depot. Restock fills need depot stock on hand, and purchasing ran at 2% of the 480-minute day against a 10% plan. Worker time is not the limit: about 165 minutes a day sat idle.

| Driver | Now (latest) | Aim for point 10 (days 64-70) | Guardrail |
| --- | --- | --- | --- |
| slots_selling | 12.0 (7-day mean, day 63) | 14 as the 7-day mean (own best 14.43) | Restock only to slots with depot stock on hand; restock stops at the 216-minute ceiling |
| revenue_per_slot | 10.03 (7-period average) | 11.0 as the 7-day mean (own best 10.57) | Price not below unit cost: latest unit_cost_paid_30d (1.066 at day 65; 1.119 at days 63-64); units per slot-day not falling |
| Product mix | 0 swaps in point 9 | 2 swaps of zero-selling products, if the swap trigger finds candidates; otherwise 0 with the reason in the day log | Gross margin per unit ≥ 0 |
| Top measure: cash | 3,611.69 at day 65 | Floor and aim lines are set by the system; no aim here | Cash ≥ 120 at every day close |

Price pass on every stocked slot each day, before the first restock trip, and before the day closes. Restock trips go only to slots with depot stock on hand. Purchasing takes first claim on idle time so depot stock is there for the restock fills.

Basis: every share is a percent of the 480-minute day; minutes = share × 480. The restock ceiling (216 minutes, 45%, controls.md) governs the day's maximum.

## Capacity split
- 15% price setting and tests: set_price
- 13% product swaps: swap_item, clear_slot
- 35% restock fills, from depot stock only: restock_machine
- 20% supplier purchasing, first claim on idle time: check_offers, order_goods
- 12% reads and admin: get_status, get_sales_report, get_machine_inventory, get_storage_inventory, read_notes, write_note, list_emails, read_email, set_reminder
- 5% slack: none

Order of the day: get_status and get_storage_inventory, then get_sales_report, then set_price on every stocked slot, then swaps, then restock fills within the depot stock shown and under the 216-minute ceiling, then check_offers and order_goods within the order guardrail.

Methods: swarm/spec.md and swarm/rules/.
