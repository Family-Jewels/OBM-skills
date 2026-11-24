As of day 328 (point 47 closed, days 323-329), after S-011 (audits/S-011.md) and AS-011 (audits/AS-011.md). Applies from point 48 (days 330-336). S-011's point-45 window (days 309-315) has passed, so its aims are restated here from the latest close. Constraint: depot cover at refill time (D3a); worker minutes read 0 of 480 on the clock, unverified against the log (spec question 7), so D4 is not judged until that is settled.

| Driver (priority) | Now (charts, point 47) | Aim for point 48 (days 330-336) | Share of 408 usable min a day | Guardrail |
| --- | --- | --- | --- | --- |
| D3a order cover | not charted (spec question 10) | every selling product ≥14 days of depot cover before each refill block | 96 | cash ≥ EUR 120 after each order; cover read from the depot |
| D1 stocked at day end, median | 5 (latest); 72 slots | ≥9 | 270: six refills × 45, depot-stocked slots only | refill only where the depot read shows the product; no slot stocked below unit cost |
| D1 slots selling | 6.43 (7-period avg); own best 12.57 | ≥9 | (as D1) | no duplicate slot beyond sell-through |
| D2 revenue per slot | 8.46 (latest); own best 12.79 | ≥12.8 (carried, not lowered) | 42: price and mix checks | price never below unit cost |
| D3 unit cost paid, 30 days | level, wrong way (x1.02 per point) | not rising; no numeric aim | inside D3a's 96 | equal-quantity quotes |
| D4a failed-refill minutes | not charted (spec question 11) | zero | inside D1's 270 | refill only where the depot read shows the product |
| D4 clock minutes on selling work | 0 of 480 (median, unverified) | not judged until spec question 7 is settled; never above 408 | total | a day whose clock reading is below its logged refill minutes is unmeasured, not zero |
| Slack | — | none | 72 kept unused | no extra calls |
| M0 cash (top measure) | 8,561.62 at close of point 47; floor line 40,836.59; aim line 61,219 | ≥10,103 at close of point 48 (8,561.62 × 1.18); the floor line governs | — | cash ≥ EUR 120 every day |

Split check: 96 + 270 + 42 = 408 usable; + 72 slack = 480.

Notes: one depot read before each refill block; refill only the slots it shows stocked; log each refill (slot, product, units, clock minutes) in log/progress.md. Six refills is what 270 minutes buys; a stocked median of 9 needs stock that lasts past one day, or the units-per-refill answer (spec question 1). Log each selling product's cover before and after each order. Report any refill that cannot be logged as a block, not a skip.

Design change needed: yes. See audits/AS-011.md.
