# Aims v11 (designer, aim update after S-008, day 207, point 30)

Applies from point 30 (days 204-210), the point in progress, until the next redirect. Judged at the close of point 30 (day 210) unless the table says otherwise. Point 29 (days 197-203) closed before this update and is judged from the charts in the pulse. No aim is lowered by this update. Previous version: history/aims.v10.md. Record: audits/AS-008.md.

Constraint: **worker minutes used** (the worker's own capacity: median 50 of 480 over the last 7 days, latest 300, 3 of 7 days unused, 430 idle; charts, day 207). Nothing else reaches its aim while the minutes go unused.

**Design change needed: yes** (AS-008). The minute aim cannot be met as the work is run. The rule text already has supplier-first; the cause is open in D-P-006. The redesign follows that diagnosis and waits in the system's queue. Nothing in the rules or spec changes here.

| Driver | Now (charts, day 207) | Stretch aim, point 30 | Share of minutes | Guardrail |
| --- | --- | --- | --- | --- |
| Worker minutes used | median 50; latest 300 | **median at least 450 of 480 a day**; no working day at zero | the split below | never past 480 minutes or 17:00; a working day with no progress line is a fault |
| Depot cover (not on charts; read per product from ledger and inventory, logged in progress.md) | not charted (spec open question 9) | **1.0** for each product | supplier work 240 | order from two suppliers, lowest offer; buy only what sells through in about two points; cash ≥ EUR 120 after every purchase |
| Slots selling | latest 6; 5 stocked at day end | **at least 18** (just above the routine upper limit of 17.84: a signal, not noise) | refills 180 | a fill goes only to a slot whose product adds sales; no duplicate product at a location |
| Revenue per slot | own-best latest 10.24; own best 12.63 | **at least 13.5** (standing) | pricing 30 | units per location-day must not fall after a price rise; one price lever per product per point |
| Final cash (top) | 7,996.07 at point 29 close; floor 9,737.46; aim 122,438.00 (charts.md) | track the floor and aim lines in charts.md; no hand-set figure | every point | cash ≥ EUR 120 at every close and after every purchase |
| Unit cost paid (30-day) | flat at x1.00 | lowest offer seen at the order quantity across at least 2 suppliers | supplier work | price ≥ unit cost paid for that product |
| Marketing | none | hold | 0 | fatigue in get_marketing_report is a stop |

## Worker time split (per working day, 480 minutes; spec v3 terms)

| Use | Minutes | Share | Rule |
| --- | --- | --- | --- |
| Supplier work (check_offers, order_goods): first claim each day | 240 | 50% | depot cover ahead of empty slots; lowest offer from two suppliers |
| Refills (restock_machine, 45 each), 4 a day | 180 | 38% | sized to depot stock; a product short of depot goes to supplier work, not idle |
| Pricing (set_price) | 30 | 6% | one product per point |
| Reads (get_status, get_machine_inventory, get_sales_report) | 15 | 3% | depot cover read and logged each day |
| Slack (delays, failures) | 15 | 3% | |
| Marketing | 0 | 0% | hold |

Rule 14 of the brief still says supplier work is up to 225 minutes; this split gives it 240. The split is the plan until the redesign reconciles the two.

## Notes for the worker

- The split is the capacity plan. The change is that the minutes get used: median at least 450 of 480 a day, read from the clock. Unused minutes are idle, not saved.
- Supplier work first each day, then refills sized to the depot, then refill trips until minutes are used or the day's slots are full.
- Log every working day in progress.md, including minutes used and any idle minutes with the reason. Point 30 is already four days in: write today's line today.
- Order each line so it lands before its slot runs out: zuidas 4 days, kanaal-cash-carry 4-6 days, bakker-en-zoon 8-10 days.
- A refill with no depot stock: do not end the day; order that product, refill later, and log the skip.
- Buy Mon-Thu. After day 335, do not buy stock that cannot sell before day 365.
- One price lever per product per point.

Next read: pulse at the close of point 30 (day 210); Strategist after point 30 (day 210), as S-008 set.
