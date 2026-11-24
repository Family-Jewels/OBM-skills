# Aims v8 (designer, aim update after S-005, day 130, point 19)

S-005's aims were set for point 18 (days 120-126), which closed before this update. They apply from point 19 (days 127-133), the point now open, until the next redirect. Judged at the close of each point. The stock aims cannot land within point 19 (lead times 4-10 days), so they are judged at point 20 (days 134-140). No aim is lowered. Previous version: history/aims.v7.md. Record: audits/AS-005.md.

Constraint: **stock reaching the machines** (depot cover, then slots selling and stocked). Worker time is not the binding limit: S-005 measured a median of 270 of 480 min; the charts' worker-time row disagrees (see AS-005). Capital is not the limit: cash 5,901 at point 18, 4% in use, about 5,990 idle (charts). Idle time and cash are there to buy the lead time.

Design change needed: yes (AS-005). The work as written cannot reach the stock aims: brief rules/operator.md v5 rule 14 puts refills first, while this split puts supplier work first. Until the redesign, the split's order holds (below); the cash rule still applies to every purchase.

| Driver | Now (charts, point 18) | Aim | Judged at | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- | --- |
| Final cash (top) | 5,901 at point 18 close; floor 4,042, aim 18,835 (charts.md, system-computed) | track the floor and aim lines in charts.md; no hand-set figure | every point | n/a | cash ≥ EUR 120 at every close and after every purchase |
| Depot cover (not on charts; read from ledger and inventory daily) | not measured on charts | **1.0** for each product: depot stock covers its empty or near-empty priced slots plus the next two points' refills | point 20 | supplier work 225 | order from two suppliers, lowest offer; buy only what sells through in about two points; cash ≥ EUR 120 after every purchase |
| Slots selling | 7-period 7.86; latest 8; own best 15.43 | **20 selling** | point 20 | refills 180 | a fill goes only to a slot whose product adds sales; no duplicate product at a location |
| Slots stocked at day end | latest 6; median 5 | **24 stocked** | point 20 | refills 180 | as above |
| Revenue per slot | 7-period 10.72; own best 12.63 | **at or above 12.9** (above own best) | point 19 | pricing 30 | units per location-day must not fall after a price rise; one price lever per product per point |
| Worker minutes used | median 270 (S-005); charts row disagrees (AS-005) | **median 420 of 480 a day**, from the simulator clock | point 19 and point 20 | the split below | never past 480 minutes or 17:00 |
| Unit cost paid (30-day) | flat, x1.02 down | lowest offer seen at the order quantity across at least 2 suppliers | point 20 | supplier work 225 | price ≥ unit cost paid for that product |
| Marketing | none | hold | n/a | 0 | fatigue in get_marketing_report is a stop |

## Worker time split (per working day, 480 minutes; spec v3 terms)

| Use | Minutes | Share | Rule |
| --- | --- | --- | --- |
| Supplier work (check_offers, order_goods): first claim each day | 225 | 47% | order depot cover ahead of empty slots; lowest offer from two suppliers |
| Refills (restock_machine, 45 each), 4 a day | 180 | 38% | sized to depot stock; if depot is short for a product, its minutes go to supplier work, not idle |
| Pricing (set_price) | 30 | 6% | one product per point |
| Reads (get_status, get_machine_inventory, get_sales_report) | 30 | 6% | depot cover read and logged each day |
| Slack (delays, failures) | 15 | 3% | |
| Marketing | 0 | 0% | hold |

Notes:
- The split stands. The change is that it gets used: median 420 of 480 minutes a day, read from the clock. Unused minutes are idle, not saved.
- **Order conflict:** brief v5 rule 14 says refills take the first 270 minutes. This split puts supplier work first. Until the operator brief is changed in the redesign, do the supplier work first on each day, within the cash rule, and log it in progress.md.
- Order each line so it lands before its slot runs out: zuidas 4 days, kanaal-cash-carry 4-6 days, bakker-en-zoon 8-10 days.
- A refill with no depot stock: do not end the day; order that product, refill later, and log the skip in progress.md.
- Buy Mon-Thu. After day 335, do not buy stock that cannot sell before day 365.
- One price lever per product per point.

Next read: Strategist after point 21 (day 147), per the spec cadence, or earlier if the top measure is 3 points below the floor line.
