Aims for point 6 (days 36-42). Version 3, day 37, after redirect S-002. Old aims: history/aims.v2.md.

Constraint: restock time, not worker time. 210 of 480 minutes were used in the last week (44%), so 270 minutes sit idle. Restock_machine takes 82% of the minutes used and fills 11 of 72 slots, while price setting and swaps, the cheapest yield per minute, get 0%. Spend the idle minutes on price and swaps first.

| Driver | Now (latest) | Aim for day 42 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| revenue_per_slot | 11.3 at day 37 (7-day average 7.9; own best 10.29) | 10.3 on the 7-day average | 25% price setting and tests | Price not below unit cost (about 1.05); units per slot-day not falling |
| slots_selling | 16 at day end (own best 14.43) | 15 at day end | 35% restock fills, fuller per trip | Restock at or under 35% of the day's minutes |
| Product mix | 0 swaps out of non-selling slots this point | 2 swaps out of non-selling slots in the point | 15% product swaps | Gross margin per unit ≥ 0 |
| Top measure: cash | 2,548 at day 37 | Floor and aim lines are set by the system; no aim here | (outcome) | Cash ≥ 120 at every day close |

Fill each trip fuller on the slots with the highest revenue_per_slot. Do not let the freed minutes go back to restock.

## Capacity split
- 25% price setting and tests: set_price
- 15% product swaps: swap_item, clear_slot
- 35% restock fills, fuller per trip: restock_machine
- 5% supplier purchasing: check_offers, order_goods
- 10% reads and admin: get_status, get_sales_report, get_machine_inventory, get_storage_inventory, read_notes, write_note
- 5% marketing set-up: get_marketing_report
- 5% slack: none

Order of the day: reads first (get_status, get_sales_report), then prices for stocked slots, then swaps, then fills on the highest-yield slots, then supplier orders only when check_offers shows a price inside the guardrail and the quote is unexpired.
