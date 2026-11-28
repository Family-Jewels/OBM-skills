# Aims (designer, after S-002; read every day)

As of day 48 (after S-002), for days 49 to 55   Constraint: worker minutes that stock in the depot could fill. Minutes are idle (7-day median used 170 of 480) while 67 of 72 slots sit empty and 2,900 of capital is unused. Fills are the cheapest use of the 480 minutes. Cash must stay above the 120 reserve.

| Driver | Now | Aim for the next point | Guardrail |
| --- | --- | --- | --- |
| Worker minutes in use | latest 455; 7-day median 170; 1 day unused in 7 | median 440 a day, no day at zero | No day ends with minutes unused while a slot is empty and depot stock is there |
| slots_selling | 11 (day 48); 7-period average 8.86; own best 15 | 15 at day end | No slot filled with more than it can sell |
| revenue_per_slot | 13.47 (day 48); 7-period average 7.58; own best 8.4 | 8.4 as the 7-period average | Units must not fall faster than price rises |

## Capacity split
- 77% restock_machine: fill empty slots from depot stock, first action of the day (about 8 fills)
- 10% order_goods, check_offers: keep the depot ahead of the 3-day Zuidas lag (5 Kanaal, 8 Bakker), within cash above the 120 reserve
- 10% get_storage_inventory, get_machine_inventory: one read each, before the fills
- 3% write_note, list_emails: notes and mail

Notes:
- Fill first. The first action of the day is restock_machine from depot stock; reads follow the fills, not the other way round.
- Order before the depot runs short: a delivery takes 3 to 8 days, so order_goods for the days after next when depot stock would not cover the empty slots.
- Never end a day with minutes unused while a slot is empty and depot stock exists.
- Prices: set_price by the sales report and the spec's price rules. set_price is not in the Facts table yet, so its time shows as "other" in the Pursuit table and is not in the split (REQ-005 open).

Methods: swarm/spec.md and swarm/rules/.
