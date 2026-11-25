As of day 189 (after S-007, day 175, point 25; prior version history/aims.v8.md). Applies from day 189 to the next Strategist redirect. Labels follow the system's charts (point 27 = days 183–189, so point 28 = days 190–196). The S-007 stretch aims were set for point 26 (days 176–182), which has passed. They are carried to point 28 unchanged, not lowered.

Constraint: **stock reaching the selling slots: depot cover** (S-007). Worker time is the capacity: the 300-min refill block is the first claim on it, and the system's chart shows it almost unspent (median 0 of 480 min, 5 of the last 7 days unused). Spending that block is the first fix.

| Driver | Now (system charts, day 189 read) | Stretch aim, point 28 | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 6,950.40 at point 27; floor line 9,048.47; aim line 87,695.35 (system's lines govern) | System's floor and aim lines govern; goal 61,219 unchanged | all drivers | cash ≥ 120 at every close |
| 2a. slots_selling | 7-period average 9.43 (own best 19.71) | 7-period average ≥ 19.71 | refill and depot cover: 300 min (days 190–195 and 196) | refills ≤ 300 min/day unless stock-out count is falling; sold-out-before-close count falling |
| 2a-i. depot cover per selling product (constraint) | Not a system chart (requested again, spec open question 10). Auditor recomputes from get_machine_inventory and get_sales_report; round line carries cover days | Every selling product ≥ 8 days' cover at each daily check; order at L + 8 days (spec v6) | inside the refill and cover block, first claim each day | cash ≥ 204 after any cover order; never buy beyond expected sales before day 365 |
| 2b. revenue_per_slot | 7-period average 5.57 (own best 8.82) | 7-period average ≥ 8.82 | pricing: 60 (days 190–195), 40 (day 196) | price ≥ unit cost × 1.2 (about 1.25 at paid unit cost 1.044); clearance from day 351 |
| 3. Unit cost paid | 1.044; flat on the charts | Lowest of ≥ 2 checked quotes on every order | purchasing: 60 (days 190–195), 120 (day 196) | never buy beyond what sells; cash ≥ 204 after an order |
| Sales reads (learning) | Per round | Read by product and location each day | 40 (days 190–195), 20 (day 196) | — |
| Fixed and marketing | Spot fee paid daily | No unpaid fee day; no marketing | 0 | spot fee paid daily |
| Buffer | Idle | Keep unused | 20 (days 190–195), 0 (day 196) | not for extra refills |

**Split of 480 min/day (spec terms)**
- Days 190–195 (other days): refill and cover 300 · purchasing 60 · pricing 60 · sales reads 40 · buffer 20. Total 480.
- Day 196 (point boundary): refill and cover 300 · purchasing 120 · pricing 40 · sales reads 20 · buffer 0. Total 480.
- These are caps on each driver's minutes, not targets; unspent minutes are logged, not moved.

**Each day, in order:** (1) Cover check under spec v6, for each selling product, from the supplier whose L fits; order at the lowest of ≥ 2 checked quotes. (2) Refill empty and sold-out selling slots first, best products first, to full, using the in-stock sales rate. (3) Price new stock at ≥ unit cost × 1.2. (4) Write the round line in log/work.jsonl with cover days per selling product and minutes used; a day with no round line is a failed round. (5) Any wait is a logged decision with its reason in the round line.

**Known limit:** at 45 min a refill, the 300-min block allows about 6 refills a day, about 84 units at 14 units per refill. The own-best unit rate (86 a day) would bind it. If the aims need more, the cap binds first; the Strategist decides that, not the operator.
