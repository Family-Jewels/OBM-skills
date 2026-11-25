As of day 199 (after S-007, day 175, point 25; prior version history/aims.v9.md, the day-189 version). Applies from day 199 to the next Strategist redirect. Labels follow the system's charts: point 28 = days 190–196, so point 29 = days 197–203 and point 30 = days 204–210. Days 203 and 210 are purchasing days (point boundaries). The S-007 stretch aims are carried unchanged, not lowered; no later Strategist redirect has replaced them.

Constraint: **stock reaching the selling slots: depot cover** (S-007, D-P-012). Worker time is idle (median 0 of 480 min over the last 7 days on the clock; 5 of 7 days unused) and cash is idle (6,974 against a floor line of 9,768). Stock is the limit, so the first claim each day is the cover check, then the refill block.

| Driver | Now (system charts, day 199 read) | Stretch aim, points 29–30 | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 6,974.30 at point 28; floor line 9,767.60; aim line 103,620.67 (system's lines govern) | System's floor and aim lines govern; goal 61,219 unchanged | all drivers | cash ≥ 120 at every close; cash ≥ 204 after any cover order |
| 2a. slots_selling | 7-period average 6.29 latest (own best 19.71); centre 10.1 | 7-period average back above its centre (10.1) by day 210; 19.71 (own best) remains the stretch | refill and cover, first claim: 300 min (other days and boundaries) | refills ≤ 300 min/day unless stock-out count is falling; sold-out-before-close count falling |
| 2a-i. depot cover per selling product (constraint) | Not a system chart (requested again, spec open question 10). Auditor recomputes from get_machine_inventory and get_sales_report until charted; round line carries cover days | Every selling product ≥ 8 days' cover at each daily check, from day 200; order at L + 8 days (spec v7) | inside the refill and cover block, first claim each day | cash ≥ 204 after any cover order; never buy beyond expected sales before day 365 |
| 2b. revenue_per_slot | 7-period average 6.05 latest (own best 8.82) | 7-period average ≥ 8.82 | pricing: 60 (other days), 40 (boundaries) | price ≥ unit cost × 1.2; clearance from day 351 |
| 3. Unit cost paid | Flat on the charts; not the priority while cash and time are idle | Lowest of ≥ 2 checked quotes on every order | purchasing: 60 (other days), 120 (boundaries) | never buy beyond what sells; cash ≥ 204 after an order |
| Sales reads (learning) | Per round | Read by product and location each day | 40 (other days), 20 (boundaries) | — |
| Fixed and marketing | Spot fee paid daily | No unpaid fee day; no marketing | 0 | spot fee paid daily |
| Buffer | Idle | Keep unused | 20 (other days), 0 (boundaries) | not for extra refills |

**Split of 480 min/day (spec terms)**
- Other days: refill and cover 300 · purchasing 60 · pricing 60 · sales reads 40 · buffer 20. Total 480.
- Point boundaries (days 203, 210): refill and cover 300 · purchasing 120 · pricing 40 · sales reads 20 · buffer 0. Total 480.
- These are caps on each driver's minutes, not targets; unspent minutes are logged, not moved. A round whose refill minutes do not reconcile with the clock is a failed round (spec v7).

**Each day, in order:** (1) Cover check under spec v7, for each selling product, from the supplier whose L fits; order at the lowest of ≥ 2 checked quotes, cash ≥ 204 after. (2) Refill empty and sold-out selling slots first, best products first, to full, using the in-stock sales rate; a wait only when the depot count for that product is zero. (3) Price new stock at ≥ unit cost × 1.2. (4) Write the round line in log/work.jsonl with refills, refill minutes and cover days per selling product. (5) Any wait is a logged decision with its reason in the round line.

**Known limit:** at 45 min a refill, the 300-min block allows about 6 refills a day, about 84 units at 14 units per refill. If the aims need more, the cap binds first; the Strategist decides that, not the operator.
