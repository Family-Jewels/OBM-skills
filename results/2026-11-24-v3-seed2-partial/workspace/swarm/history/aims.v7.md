# Aims v7 (designer, aim update after S-004, day 101, point 15)

S-004's aims were set for point 14 (days 92-98), which had closed before this update. They apply from point 15 (days 99-105) until the next redirect. No aim is lowered. Previous version: history/aims.v6.md. Record: audits/AS-004.md.

Constraint: **stock reaching the machines** (depot stock, then slots stocked). Worker time is not the limit: median 90 of 480 min used over the last 7 days, 390 idle (charts). Capital is not the limit: cash 4,860 at day 101, 3% in use (charts). Stock ordered now lands in 4-10 days, so these aims can be reached at point 16 at the earliest. The work as it now runs cannot reach them (AS-004). Design change needed: yes, queued behind any diagnosis. Until a redesign is adopted, the work follows spec v2 and rules/operator.md v4.

| Driver | Now (charts, day 101) | Aim, point 15 onward | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| Final cash (top) | 4,860. Floor and aim lines: charts.md (system-computed, point 14: floor 2,936, aim 9,536). Falling short of the aim triggers nothing | track the floor and aim lines in charts.md | n/a | cash ≥ EUR 120 at every close and after every purchase |
| Slots selling | 9 latest; 7-period 6.0; own best 15.43 | **20 selling** | refills 180 (split below) | a fill goes only to a slot whose product adds sales; no duplicate product at a location |
| Stocked at day end | 3 latest; 3 median over 7 days | **24 stocked** | refills | as above |
| Depot cover (not on charts; read from the ledger and inventory daily) | not measured on charts | **1.0**: stock for every empty priced slot plus the next two points' refills | supplier work 225 | buy only what sells through in about two points; cash ≥ EUR 120 after every purchase |
| Revenue per slot | 13.51 latest day; 7-period 11.84; own best 12.38 | **at or above 12.4** (above own best) | slot and price work | units per location-day must not fall after a price rise |
| Unit cost paid | collecting | lowest offer seen at the order quantity, across at least 2 suppliers (carried) | supplier work | buy only what sells through in about two points; price ≥ unit cost paid |
| Marketing | none | hold | 0 | fatigue in get_marketing_report is a stop |

## Worker time split (per working day, 480 minutes; spec v2 terms)

| Use | Minutes | Share |
| --- | --- | --- |
| Supplier work (check_offers, order_goods): first claim each day | 225 | 47% |
| Refills (restock_machine, 45 each): sized to depot stock, 4 a day | 180 | 38% |
| Pricing (set_price) | 30 | 6% |
| Reads (get_status, get_machine_inventory, get_sales_report) | 30 | 6% |
| Slack (delays, failures) | 15 | 3% |
| Marketing | 0 | 0% |

Notes:
- The split is the plan. Use it. Never past 480 minutes or 17:00.
- Order each line so it lands before its slot runs out: zuidas 4 days, kanaal-cash-carry 4-6 days, bakker-en-zoon 8-10 days (progress.md, day 1).
- A refill with no depot stock: do not end the day; order that product, refill later, log it in progress.md.
- Buy Mon-Thu. Stop buying stock that cannot sell before day 365 after day 335.
- One price lever per product per point.

Next read: Strategist after point 15 (day 105), per the spec cadence, or earlier if the top measure is 3 points below the floor line.
