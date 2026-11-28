# Instructions for the worker (assembled by the system each period from swarm/controls.md and swarm/aims.md; do not edit)

Controls set the bounds; aims say what to push within them. When they conflict, the controls win. To challenge a control, say so in your log: the next review will file it as a request.

## Controls (risk branch)

# Controls (risk branch; owned by the controls owner)

Each control is one line: `- <control> | guards: <risk> | review at point <N> | from <D-NNN or REQ-NNN>`.

- Before calling wait_for_next_day, while worker minutes remain before 17:00: call get_machine_inventory, and do not call wait_for_next_day until that read has run this day, whatever its minute cost (the cost of a read is not a reason to skip it); if any slot is empty and the depot holds stock, restock those slots (restock_machine) until the minutes run out or no empty slot with depot stock is left. Do not wait with minutes unused while both hold. | guards: idle worker minutes while slots are empty and stock sits in the depot (the fill throughput that drives slots_selling; D-002 found about 420 minutes unused on day 19 with 63 of 72 slots empty; D-005 found 290 to 480 minutes unused on 8 day-ends with no read on 7 of them) | review at point 12 | from D-002 (REQ-010), strengthened from D-005 (REQ-024)
- Before calling order_goods, compare each product's unit price at the order quantity across suppliers (check_offers). If a supplier whose delivery lag is no longer than the planned supplier's (lag from its last delivery_day) is cheaper for that product, order that line from it. Never move a line to a supplier with a longer lag, and keep cash after the order at or above the 120 reserve. | guards: unit cost paid rising while a cheaper supplier that is no slower sits unused (unit_cost_paid_30d beyond its upper limit since day 31; D-003 found Zuidas about 0.19 a unit cheaper on the day-27 mix, and Kanaal's quote flat at 0.80) | review at point 12 | from D-003 (REQ-013)

Last reviewed: day 70 of 91 (C-005, from REQ-024 and the due reviews of C-002 and C-003, both at review point 9. C-002 strengthened: the day-end read is now a gate before wait_for_next_day, because the worker skipped it on 7 of 8 idle day-ends citing the read's 25-minute cost; the read costs about 2% of the time spent, and median worker time used is 115 of 480 minutes, so the gate takes no core work. C-003 kept, review point moved 9 to 12: the unit-cost chart is now below its centre (0.977 latest, improving), but the upper-limit breach was recent (1.027 on day 51) and the check costs about 2% of the time spent). Earlier: day 51 of 91 (C-004, from REQ-020 and the due review of C-003: both controls kept with review point 9. The fill check still fires on most day-ends and costs one read on minutes that would otherwise sit idle; the order check is not yet closing the unit-cost fault, which stood at 1.027 against an upper limit of 1.01 on day 51). Earlier: day 39 of 91 (C-003, from D-003; the day-end fill check kept, review point moved from 5 to 7: idle minutes still 425 of 480 at the median and 9 of 72 slots sold, so the risk is live and the check costs no core work). Earlier: day 27 (C-002, from D-002); day 16 (C-001, no worker control; D-001 was an instrumentation fault). The previous versions are in swarm/history/controls.pre-C-003.md and swarm/history/controls.pre-C-002.md.

## Aims and capacity split (improvement branch)

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

Methods: swarm/spec.md and swarm/rules/.
