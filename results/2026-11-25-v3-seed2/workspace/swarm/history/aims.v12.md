As of day 264 (after S-009, day 259; prior version history/aims.v11.md). Applies from day 264 to the next Strategist redirect. Labels follow the system's charts: point 38 = days 260–266 (in progress), point 39 = days 267–273 (next). Purchasing days (point boundaries): 266 and 273.

Constraint: **stock reaching the selling slots: depot cover** (S-009, spec v7 driver 2a-i). Worker time is far below its limit (median 0 of 480 min; 5 of 7 days unused). Cash is idle (7,671.50 at day 259 against a floor line of 19,440.15). Stock, not minutes, is the limit; the refill and cover block is the first claim each day.

| Driver | Now (S-009, day 259) | Stretch aim: point 38 → point 39 | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 7,671.50 vs floor 19,440.15; system's lines govern | System's floor and aim lines govern; goal 61,219 unchanged | all drivers | cash ≥ 120 at every close; cash ≥ 204 after any cover order |
| 1. Worker time, refill and cover block | Median 0 of 480 min | ≥ 300 min every working day; median ≥ 300 across point 38 | first claim: 300 min | refill minutes ≤ 300/day (spec cap; the block is at the cap, not above it) |
| 2a. slots_selling (7-period) | 3.86 (own best 19.71) | ≥ 8 at point 38; ≥ 12 at point 39 (S-008's aim, carried) | inside the refill and cover block | sold-out-before-close count falling; refills ≤ 300 min/day |
| 2a-i. depot cover per selling product (constraint) | Not charted (spec open question 10); auditor recomputes from get_machine_inventory and get_sales_report | ≥ 8 days' cover per selling product at every daily check; order at L + 8 days (spec v7) | first claim each day, inside the block | cash ≥ 204 after any cover order; never buy beyond expected sales before day 365 |
| 2b. revenue_per_slot (7-period) | 6.05 (own best 8.82) | ≥ 8.0 at point 39 | pricing: 60 (other days), 40 (boundaries) | price ≥ unit cost × 1.2; clearance from day 351 |
| 3. Unit cost paid | Flat; not the priority while cash and time are idle | Lowest of ≥ 2 checked quotes on every order | purchasing: 60 (other days), 120 (boundaries) | never buy beyond what sells; cash ≥ 204 after an order |
| Sales reads (learning) | Per round | Read by product and location each day | 40 (other days), 20 (boundaries) | — |
| Fixed and marketing | Spot fee paid daily | No unpaid fee day; no marketing | 0 | spot fee paid daily |
| Buffer | Idle | Keep unused | 20 (other days), 0 (boundaries) | not for extra refills |

**Split of 480 min/day (spec terms)**
- Other days (264–265, 267–272): refill and cover 300 · purchasing 60 · pricing 60 · sales reads 40 · buffer 20. Total 480.
- Point boundaries (266, 273): refill and cover 300 · purchasing 120 · pricing 40 · sales reads 20 · buffer 0. Total 480.
- These are caps on each driver's minutes, not targets; unspent minutes are logged, not moved. A round whose refill minutes do not reconcile with the clock is a failed round (spec v7).
- Idle cash goes to stock for selling slots, keeping cash ≥ 204.

**Each day, in order:** (1) Cover check for each selling product; order at the lowest of ≥ 2 checked quotes, cash ≥ 204 after. (2) Refill empty and sold-out selling slots first, best products first, to full. A wait only when the depot count for that product is zero. (3) Price new stock at ≥ unit cost × 1.2. (4) Write the round line in log/work.jsonl with refills, refill minutes and cover days per selling product. (5) Any wait is a logged decision with its reason.

**Known limit:** at 45 min a refill, the 300-min block allows at most 6 refills a day (about 5 if the cover checks take about 30 min of it). 12 slots need about 3 refills a day and 19.71 slots about 4.5; both fit. If sell-through rises past about 4.3 units per slot a day, the cap binds first; the Strategist decides that, not the operator.
