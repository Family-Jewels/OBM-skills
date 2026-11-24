Aims for days 78-84 (point 12). Version 8, day 80, after redirect S-005 (AS-005). Old aims: history/aims.v7.md.

Constraint: restock fills at the 216-minute ceiling (controls.md). Four fills a day at 45 minutes each; depot stock covers the empty slots. Worker time is not the limit (about 170 minutes a day idle). Purchasing feeds the depot and is due now: last order day 73.

| Driver | Now (latest) | Aim for days 78-84 | Guardrail |
| --- | --- | --- | --- |
| slots_selling | 14 at day 80; 7-day mean 12.6 (own best 14.43) | 14 as the 7-day mean | Restock best sellers first, only to slots with depot stock on hand; stop at the 216-minute ceiling |
| Supplier purchasing | 4% of the day (plan 20%) | One order cycle this week, placed before any product's depot falls under one fill (10 units); 10% of the day (48 minutes) on order days | Order gate in controls.md: comparison table and unexpired offers before any order_goods |
| revenue_per_slot | 11.89 at day 80; 7-day mean 10.55 (own best 10.57) | 11.0 as the 7-day mean | Price at or above unit cost: unit_cost_paid_30d 1.116 at day 80 and rising; units per slot-day not falling |
| Top measure: cash | 4,627.93 at day 80 | Floor and aim lines are set by the system; no aim here | Cash ≥ 120 at every day close |

Price pass on every stocked slot each day, before the first restock trip, and before the day closes. Restock trips go only to slots with depot stock on hand.

Basis: every share is a percent of the 480-minute day; minutes = share × 480. The restock ceiling (216 minutes, 45%, controls.md) governs the day's maximum.

## Capacity split
- 45% restock fills, from depot stock only: restock_machine
- 15% price setting and tests: set_price
- 10% supplier purchasing, inside the order guardrail: check_offers, order_goods
- 16% reads and admin: get_status, get_sales_report, get_machine_inventory, get_storage_inventory, read_notes, write_note, list_emails, read_email, set_reminder, get_marketing_report
- 14% slack: none

Order of the day: get_status and get_storage_inventory, then get_sales_report, then set_price on every stocked slot, then check_offers and order_goods if an order cycle is due (inside the order guardrail), then restock fills within the depot stock shown and under the 216-minute ceiling, then the remaining reads and notes.

Methods: swarm/spec.md and swarm/rules/.
