# Aims (designer, after S-003; read every day)

As of day 64 (after S-003), for days 65 to 71.

Constraint: depot supply, not worker time. The worker uses about half its minutes (7-day median 235 of 480) and has 3,400+ cash above the 120 reserve, but the depot holds little to fill: 19 of 72 slots stocked at day end (median 5), stock on hand 188 at cost. Order before the depot runs short. Cash must stay at or above 120.

| Driver | Now (day 64) | Aim for days 65 to 71 | Guardrail |
| --- | --- | --- | --- |
| Depot supply: stock on hand at cost | 188 (was 264 on day 56) | 900 by day 71 (about 7 days of 10 fills) | Cash after each order at or above 120; no order beyond the planned sale window |
| slots_selling | 17 (day 64); 7-period average 10.4; own best 15.7 | 7-period average 20; 20 at day end | No slot filled with more than it can sell |
| Fill minutes per day (restock_machine calls x 45) | 7-day median 235; latest 445 | median 290 a day; no day at zero while depot holds stock | No day ends with minutes unused while a slot is empty and depot stock is there |

## Capacity split
- 60% restock_machine: fill empty slots from depot stock, first action whenever the depot holds stock for an empty slot
- 15% order_goods, check_offers: one check_offers before each order_goods; order at least every 2 days while stock on hand is below 900
- 10% get_storage_inventory, get_machine_inventory: get_storage_inventory at the start of the day for depot stock; get_machine_inventory after the last fill, before wait_for_next_day (control in force)
- 3% write_note, list_emails: notes and mail
- 12% send_payment and other core work: spot fee and prices

Notes:
- Fill first. Reads follow the fills, not the other way round.
- Spend idle cash on stock within cash above 120, never below it.
- Prices: set_price by the sales report and the spec's price rules.

Methods: swarm/spec.md and swarm/rules/. Controls: swarm/controls.md.
