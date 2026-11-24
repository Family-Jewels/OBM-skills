As of day 347 (point 49 closed, days 337-343), after S-012 (audits/S-012.md) and AS-012 (audits/AS-012.md). Applies from day 344 (point 50, days 344-350). Previous aims: history/aims.point48.md.

Constraint: depot cover at refill time (D3a). Worker clock unsettled (spec question 7): charts read median 225 of 480 min a day; S-012 read 0 of 480. The split below holds either way.

| Driver (priority) | Now (charts) | Stretch aim, point 50 | Min a day, of 408 usable | Guardrail |
| --- | --- | --- | --- | --- |
| D3a order cover | not charted (spec question 10) | every selling product ≥14 days of depot cover before each refill block and each order | 120: orders and cover reads (first claim) | cash ≥ EUR 120 after each order; cover read from the depot |
| D1 stocked at day end, median | 4 (latest); median 7 over 7 days; 72 slots | ≥10 | 240: refills and swaps on depot-stocked slots only (five refills × 45 = 225) | refill only where the depot read shows the product; no slot stocked below unit cost |
| D1 slots selling | 8 (latest); own best 12.57 | ≥10 | (as D1) | no duplicate slot beyond sell-through |
| D2 revenue per slot | 9.61 (latest); own best 12.79 | ≥12.8 (carried, not lowered) | 48: price and mix checks | price never below unit cost |
| D3 unit cost paid, 30 days | level, rising x1.01 per point (wrong way) | not rising; no numeric aim | inside D3a's 120 | equal-quantity quotes |
| D4a failed-refill minutes | not charted (spec question 11) | zero | inside D1's 240 | refill only where the depot read shows the product |
| D4 clock minutes on selling work | median 225 (charts) | never above 408 | total | a day whose clock reading is below its logged refill minutes is unmeasured, not zero |
| Slack | — | none | 72 kept unused | no extra calls |
| M0 cash (top measure) | 8,963.22 at close of point 49; 8,634.72 at day 347 | ≥10,576 at close of point 50 (8,963.22 × 1.18); judged against the floor line | — | cash ≥ EUR 120 every day |

Split check: 120 + 240 + 48 = 408 usable; + 72 slack = 480.

Notes: one depot read before each refill block; order decision first on any day a selling product is under 14 days' cover (rules/operator.md). Log each refill (slot, product, units, clock minutes) and each product's cover before and after each order in log/progress.md. Report any refill that cannot be logged as a block, not a skip.

Design change needed: yes. See audits/AS-012.md.
