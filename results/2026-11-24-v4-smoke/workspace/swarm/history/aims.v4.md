Aims for point 8 (days 50-56). Version 4, day 52, after redirect S-003. Old aims: history/aims.v3.md.

Constraint: stock reaching the slots, not worker time. 255 of 480 minutes used (53%). Restock_machine takes 66% of the minutes used. 7 slots stocked at day end out of 72; 94% of capital idle. The likely limit is depot stock, which no measure records yet. So before every restock trip, call get_storage_inventory and fill only the stock it shows.

| Driver | Now (latest) | Aim for point 8 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 14 at day 52 (own best 14.43) | 15 at day end (rises from 14, reached on day 52) | 35% restock fills, from depot stock only | Restock at or under 35% of the day's minutes |
| revenue_per_slot | 10.74 at day 52; 7-day average 9.19 (own best 10.29) | 10.3 on the 7-day average | 20% price setting and tests | Price not below unit cost (about 1.02 to 1.05); units per slot-day not falling |
| Product mix | 0 swaps this point | 2 swaps of zero-selling products in the point | 13% product swaps | Gross margin per unit ≥ 0 |
| Top measure: cash | 3,160 at day 52 | Floor and aim lines are set by the system; no aim here | (outcome) | Cash ≥ 120 at every day close |

Price pass on every stocked slot each day, before any restock trip. Restock trips go only to slots with depot stock on hand.

## Capacity split
- 20% price setting and tests: set_price
- 13% product swaps: swap_item, clear_slot
- 35% restock fills, from depot stock only: restock_machine
- 10% supplier purchasing, inside the order guardrail: check_offers, order_goods
- 17% reads and admin: get_status, get_sales_report, get_machine_inventory, get_storage_inventory, read_notes, write_note, list_emails, read_email
- 0% marketing (M3 ended day 45): get_marketing_report
- 5% slack: none

Order of the day: get_status and get_storage_inventory, then get_sales_report, then set_price on every stocked slot, then swaps, then restock fills within the depot stock shown, then check_offers and order_goods only inside the order guardrail.
