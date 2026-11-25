As of day 234 (after S-008, day 224; prior version history/aims.v10.md). Applies from day 234 to the next Strategist redirect. Labels follow the system's charts: point 34 = days 232–238 (in progress), point 35 = days 239–245 (next). Purchasing days (point boundaries): 238 and 245. The S-008 point-33 aims (days 225–231) ended unmet; their values carry into point 34 as the bridge, not lowered.

Constraint: **stock reaching the selling slots: depot cover** (S-008, spec v7 driver 2a-i). Worker time is far below its limit (median 0 of 480 min; 4 of 7 days unused). Cash is idle (7,262 at point 33 against a floor line of 14,317). Minutes are not the limit; the refill and cover block must be spent every day.

| Driver | Now (system charts, latest) | Stretch aim: point 34 → point 35 | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 7,262 at point 33; floor 14,316.93; aim 122,438 (system's lines govern) | System's floor and aim lines govern; goal 61,219 unchanged | all drivers | cash ≥ 120 at every close; cash ≥ 204 after any cover order |
| 2a. slots_selling | 7-period 7.71 (own best 19.71); daily 9 | 7-period ≥ 12 → ≥ 19.71 (own best) | refill and cover, first claim: 300 min | refills ≤ 300 min/day unless stock-out count is falling; sold-out-before-close count falling |
| 2a-i. depot cover per selling product (constraint) | Not charted (spec open question 10, requested again). Auditor recomputes from get_machine_inventory and get_sales_report; round line carries cover days | Every selling product ≥ 8 days' cover at each daily check, from day 234; order at L + 8 days (spec v7) | inside the refill and cover block, first claim each day | cash ≥ 204 after any cover order; never buy beyond expected sales before day 365 |
| 2b. revenue_per_slot | 7-period 4.76 (own best 8.82) | 7-period ≥ 8.0 at point 34 and point 35 | pricing: 60 (other days), 40 (boundaries) | price ≥ unit cost × 1.2; clearance from day 351 |
| 3. Unit cost paid | Flat; not the priority while cash and time are idle | Lowest of ≥ 2 checked quotes on every order | purchasing: 60 (other days), 120 (boundaries) | never buy beyond what sells; cash ≥ 204 after an order |
| Sales reads (learning) | Per round | Read by product and location each day | 40 (other days), 20 (boundaries) | — |
| Fixed and marketing | Spot fee paid daily | No unpaid fee day; no marketing | 0 | spot fee paid daily |
| Buffer | Idle | Keep unused | 20 (other days), 0 (boundaries) | not for extra refills |

**Split of 480 min/day (spec terms)**
- Other days (234–237, 239–244): refill and cover 300 · purchasing 60 · pricing 60 · sales reads 40 · buffer 20. Total 480.
- Point boundaries (238, 245): refill and cover 300 · purchasing 120 · pricing 40 · sales reads 20 · buffer 0. Total 480.
- These are caps on each driver's minutes, not targets; unspent minutes are logged, not moved. A round whose refill minutes do not reconcile with the clock is a failed round (spec v7).

**Each day, in order:** (1) Cover check for each selling product; order at the lowest of ≥ 2 checked quotes, cash ≥ 204 after. (2) Refill empty and sold-out selling slots first, best products first, to full. A wait only when the depot count for that product is zero. (3) Price new stock at ≥ unit cost × 1.2. (4) Write the round line in log/work.jsonl with refills, refill minutes and cover days per selling product. (5) Any wait is a logged decision with its reason.

**Known limit:** 45 min a refill means the 300-min block allows about 6 refills a day, about 84 units at 14 units per refill. At the observed sell-through (about 3 units per selling slot a day), 12 slots need about 3 refills a day and 19.71 slots about 4.5; both sit inside the cap. If sell-through rises past about 4.3 units per slot a day, the cap binds first; the Strategist decides that, not the operator.
