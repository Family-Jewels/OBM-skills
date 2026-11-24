# Aims v9 (designer, aim update after S-006, day 157, point 23)

S-006's aims were set for point 22 (days 148-154), which closed before this update. They apply from point 23 (days 155-161), open now, until the next redirect. Judged at the close of each point, except where the table says otherwise. No aim is lowered. Previous version: history/aims.v8.md. Record: audits/AS-006.md.

Constraint: **worker minutes used** (the worker's own capacity: median 230 of 480 over the last 7 days, 250 idle, 2 days unused, charts). The minutes must buy depot cover first: slots cannot sell without stock, and stock lands 4-10 days after order.

Design change needed: yes (AS-006). Brief rules/operator.md v5 rule 14 still puts refills first (first 270 minutes), so the supplier-first order these aims need is not in the work as written.

| Driver | Now (charts, day 158) | Aim | Judged at | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- | --- |
| Worker minutes used | median 230 (7 days); latest 25 | **median at least 450 of 480 a day**; no working day at zero | point 23 | the split below | never past 480 minutes or 17:00 |
| Depot cover (not on charts; read from ledger and inventory daily) | not charted (spec open question 9) | **1.0** for each product: depot covers its empty or near-empty priced slots plus the next two points' refills | point 24 | supplier work 240 | order from two suppliers, lowest offer; buy only what sells through in about two points; cash ≥ EUR 120 after every purchase |
| Slots selling | latest 8; median 8.75 | **at least 22** | point 24 (stock ordered in point 23 lands in 4-10 days) | refills 180 | a fill goes only to a slot whose product adds sales; no duplicate product at a location |
| Revenue per slot | latest 9.82; own best 12.63 | **at least 13.5** (above own best) | point 23 | pricing 30 | units per location-day must not fall after a price rise; one price lever per product per point |
| Final cash (top) | 7,208.56 at day 158; floor and aim lines in charts.md (system-computed) | track the floor and aim lines in charts.md; no hand-set figure | every point | n/a | cash ≥ EUR 120 at every close and after every purchase |
| Unit cost paid (30-day) | improving, x1.02 down | lowest offer seen at the order quantity across at least 2 suppliers | point 24 | supplier work | price ≥ unit cost paid for that product |
| Marketing | none | hold | n/a | 0 | fatigue in get_marketing_report is a stop |

## Worker time split (per working day, 480 minutes; spec v3 terms)

| Use | Minutes | Share | Rule |
| --- | --- | --- | --- |
| Supplier work (check_offers, order_goods): first claim each day | 240 | 50% | order depot cover ahead of empty slots; lowest offer from two suppliers |
| Refills (restock_machine, 45 each), 4 a day | 180 | 38% | sized to depot stock; if depot is short for a product, its minutes go to supplier work, not idle |
| Pricing (set_price) | 30 | 6% | one product per point |
| Reads (get_status, get_machine_inventory, get_sales_report) | 15 | 3% | depot cover read and logged each day |
| Slack (delays, failures) | 15 | 3% | |
| Marketing | 0 | 0% | hold |

## Notes for the worker

- The split is the capacity plan. The change is that the minutes get used: median at least 450 of 480 a day, read from the clock. Unused minutes are idle, not saved.
- **Order conflict:** brief v5 rule 14 says refills take the first 270 minutes. This split puts supplier work first. Until the operator brief is changed in the redesign, do the supplier work first each day, within the cash rule, and log it in progress.md.
- Order each line so it lands before its slot runs out: zuidas 4 days, kanaal-cash-carry 4-6 days, bakker-en-zoon 8-10 days.
- A refill with no depot stock: do not end the day; order that product, refill later, and log the skip in progress.md.
- Buy Mon-Thu. After day 335, do not buy stock that cannot sell before day 365.
- One price lever per product per point.

Next read: Strategist after point 24 (day 168), per the spec cadence, or earlier if the top measure is 3 points below the floor line.
