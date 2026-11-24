As of day 278 (point 40), after S-010 (audits/AS-010.md). Applies from point 41 (days 281-287); point 40 runs on the point-38 aims (history/aims.point38.md). Constraint: stocked selling slots, held down by depot cover at refill time (D3a); refill minutes bind once the depot holds product. Worker minutes read 0 of 480 on the clock, unverified against the log (spec question 7); D4 is not judged until that is settled.

| Driver (priority) | Now (charts, point 39) | Aim for point 41 (days 281-287) | Share of 408 usable min | Guardrail |
| --- | --- | --- | --- | --- |
| D3a order cover | not charted (spec question 10) | each selling product ≥14 days of depot cover | within D3's 63 | cash ≥ EUR 120 after each order; cover read from the depot |
| D1 stocked at day end, median | 4 (7 days); latest 1 | ≥8 | 315 min: 7 refills × 45, depot-stocked slots only | refill only where the depot read shows the product; no slot stocked below unit cost |
| D1 slots selling | 4.57 (own best 12.57) | ≥8 | (as D1) | no duplicate slot beyond sell-through |
| D2 revenue per slot | 6.6 (own best 12.79) | ≥12.8 (carried, not lowered) | 30 min: price checks | price never below unit cost |
| D3 unit cost paid, 30 days | level 1.188 (AS-007); improving | not rising; no numeric aim | 63 min with D3a: orders and reads | equal-quantity quotes |
| D4a failed-refill minutes | not charted (spec question 11) | zero | inside D1's 315 | refill only where the depot read shows the product |
| D4 clock minutes on selling work | 0 of 480 (median, unverified) | ≥380 a day, matching the refill log; never above 408 | total | a day whose clock reading is below its logged refill minutes is unmeasured, not zero |
| Slack | — | none | 72 min kept unused | no extra calls |
| M0 cash (top measure) | 7,567.75 at close of point 39; floor line 21,365.38; aim line 61,219 | ≥10,537 at close of point 41 (7,567.75 × 1.18 × 1.18); the floor line governs | — | cash ≥ EUR 120 every day |

Split check: 315 + 63 + 30 = 408 usable; + 72 slack = 480.

Notes: read this file at the first action of each point. Before each refill block, one depot read; refill only the slots it shows stocked, and log each refill (slot, product, units, clock minutes) in log/progress.md. At each order, log each selling product's cover before and after. Log each day's minutes. 315 min is seven refills; if eight slots empty in one day, the eight-slot aim needs units per refill (spec question 1) or refills that last more than a day. Report any refill that cannot be logged as a block, not a skip.

Design change needed: yes. See audits/AS-010.md.
