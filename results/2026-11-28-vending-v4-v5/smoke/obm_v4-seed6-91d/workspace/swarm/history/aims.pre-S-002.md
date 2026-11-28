# Aims (designer, after S-001; read every day)

As of day 27 (after S-001), for days 28 to 34   Constraint: worker minutes that the depot's stock cannot fill (the depot runs dry on some days, so the minutes sit idle)

| Driver | Now | Aim for the next point | Guardrail |
| --- | --- | --- | --- |
| Worker minutes in use | median 410 of 480; day 27 about 185; day 26 about 10 | 450 a day or more | No day ends with minutes unused while a slot is empty and depot stock is there |
| slots_selling | 9 (day 27) | 18 at day end | No slot filled with more than it can sell |
| revenue_per_slot | 6.37 (7-period average 7.03; own best 8.4) | 8.4 as the 7-period average | Units must not fall faster than price rises |

## Capacity split
- 86% restock_machine: fill empty slots from depot stock, after the first read of the day
- 8% order_goods, check_offers: keep the depot ahead of the next day's empty slots, within cash above the 120 reserve
- 4% get_machine_inventory, get_storage_inventory, get_sales_report: reads before a fill
- 2% write_note, set_reminder, list_emails: notes and mail

Notes:
- Start each day with get_storage_inventory (depot units) and get_machine_inventory (empty slots).
- If the depot holds fewer units than the empty slots need, order_goods first, then fill. A day with no stock to fill is a day of idle minutes; order before the depot runs dry.
- Fill before reading. Never end a day with minutes unused while a slot is empty and depot stock exists.
- Prices: set_price by the sales report, following the spec's price rules. set_price is not in the Facts table yet, so it is not in the split.
