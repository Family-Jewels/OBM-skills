# Aims v10 (designer, aim update after S-007, day 177, point 26)

S-007's aims for point 25 (days 169-175) closed before this update and are judged from the charts in the pulse. These apply from point 26 (days 176-182) until the next redirect. Judged at the close of point 26 unless the table says otherwise. No aim is lowered. Previous version: history/aims.v9.md. Record: audits/AS-007.md.

Constraint: **worker minutes used** (the worker's own capacity: median 115 of 480 over the last 7 days, 365 idle; charts, day 177). Nothing else reaches its aim while the minutes go unused.

**Design change needed: yes** (AS-007). The minute aim is not reachable with the work as it is run. Brief v6 already has the supplier-first order, so the change is not in the rules text; the diagnostician must find why the minutes are not used (see AS-007).

| Driver | Now (charts, day 177) | Stretch aim, point 26 | Share of minutes | Guardrail |
| --- | --- | --- | --- | --- |
| Worker minutes used | median 115; latest 390 | **median at least 450 of 480 a day**; no working day at zero | the split below | never past 480 minutes or 17:00; a working day with no progress line is a fault |
| Depot cover (not on charts; pulse reads ledger and inventory per product) | not charted (spec open question 9) | **1.0** for each product at close of point 26 | supplier work 240 | order from two suppliers, lowest offer; buy only what sells through in about two points; cash ≥ EUR 120 after every purchase |
| Slots selling | latest 4; median 8.75 | **at least 22** (above the routine upper limit of 18.27: a stretch, not a signal) | refills 180 | a fill goes only to a slot whose product adds sales; no duplicate product at a location |
| Revenue per slot | 7-period 10.93; own best 12.63 | **at least 13.5** (not the priority this point; pricing minutes continue) | pricing 30 | units per location-day must not fall after a price rise; one price lever per product per point |
| Final cash (top) | 7,766.41 at point 25 close; floor 7,072.72, aim 61,986.81 (charts.md) | track the floor and aim lines in charts.md; no hand-set figure | every point | cash ≥ EUR 120 at every close and after every purchase |
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

## Notes for the worker

- The split is the capacity plan. The change is that the minutes get used: median at least 450 of 480 a day, read from the clock. Unused minutes are idle, not saved.
- Supplier work first each day (brief v6 rule 14), then refills sized to the depot, then refill trips until minutes are used or the day's slots are full.
- Log every working day in progress.md, including the minutes used and any idle minutes with the reason.
- Order each line so it lands before its slot runs out: zuidas 4 days, kanaal-cash-carry 4-6 days, bakker-en-zoon 8-10 days.
- A refill with no depot stock: do not end the day; order that product, refill later, and log the skip.
- Buy Mon-Thu. After day 335, do not buy stock that cannot sell before day 365.
- One price lever per product per point.

Next read: pulse at the close of point 26 (day 182); Strategist after point 27 (day 189), per the spec cadence, or earlier on a three-point signal.
