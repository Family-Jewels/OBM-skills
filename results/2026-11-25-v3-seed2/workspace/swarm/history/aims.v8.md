As of day 155 (after S-006, day 147, point 21; prior version history/aims.v7.md). Applies from day 155 to the next Strategist redirect or the point-23 close (day 161), whichever comes first. Labels follow the system's charts (point 22 = days 148–154, so point 23 = days 155–161). The S-006 targets are carried unchanged, not lowered: S-006 set them as its stretch aims and no later redirect exists. Day 161 is a purchasing day (point boundary).

Constraint: **stock reaching the selling slots: depot cover** (S-006). Worker time is the capacity, not the limit: median 90–135 of 480 min used, 3 of the last 7 days unused. The 300-min refill block is the part not being spent; that is the first fix.

| Driver | Now (system charts, day 158 read) | Stretch aim, point 23 | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 6,175.40 at point 22; floor line 6,173.24; aim line 38,073.90 (system's lines govern) | System's floor and aim lines govern; goal 61,219 unchanged | all drivers | cash ≥ 120 at every close |
| 2a. slots_selling | 7-period average 7.29 (own best 19.71); process upper limit 20.35 | 7-period average ≥ 20 | refill and depot cover: 300 min (other days), 260 (day 161) | refills ≤ 300 min/day unless stock-out count is falling; sold-out-before-close count falling |
| 2a-i. depot cover per selling product (constraint) | Not a system chart yet (requested). Measured from the round line's cover days per product (spec open question 8); auditor recomputes from get_machine_inventory and get_sales_report | Every selling product ≥ 8 days' cover at each daily check; order at L + 8 days (spec v5) | inside the refill and cover block, first claim each day | cash ≥ 204 after any cover order; never buy beyond expected sales before day 365 |
| 2b. revenue_per_slot | 7-period average 5.95 (own best 8.79) | ≥ 8.8 | pricing and mix: 80 (other days), 70 (day 161) | price ≥ unit cost × 1.2 (about 1.25 at paid unit cost 1.044); clearance from day 351 |
| 3. Unit cost paid | 1.044; wrong way on celeration (charts) | Not a priority while cash is idle; lowest of ≥ 2 checked quotes on every order | purchasing: 30 (other days), 90 (day 161) | never buy beyond what sells; cash ≥ 204 after an order |
| Fixed and marketing | Spot fee paid daily | No unpaid fee day; no marketing | 0 | spot fee paid daily |
| Sales reads | Per round | Read by product and location each day; full read at day 161 | 40 (every day) | — |
| Buffer | Idle | Keep unused | 30 (other days), 20 (day 161) | not for extra refills |

**Split of 480 min/day (spec terms)**
- Other days: refill and cover 300 · purchasing 30 · pricing and mix 80 · sales reads 40 · buffer 30. Total 480.
- Day 161 (point boundary): refill and cover 260 · purchasing 90 · pricing 70 · sales reads 40 · buffer 20. Total 480.
- These are caps on each driver's minutes, not targets; unspent minutes are logged, not moved.

**Each day, in order:** (1) Cover check under spec v5, for each selling product, from the supplier whose L fits; order at the lowest of ≥ 2 checked quotes. (2) Refill empty and sold-out selling slots first, best products first, to full. (3) Price new stock at ≥ unit cost × 1.2. (4) Write the round line in log/work.jsonl with cover days per selling product and minutes used; a day with no round line is a failed round. (5) Any wait is a logged decision with its reason in the round line.

**Known limit:** at 45 min a refill, the 300-min block allows about 6 refills a day. If the 20-slot aim needs more, the cap binds first; the Strategist decides that, not the operator.
