As of day 298 (after S-010, day 287, point 41; prior version history/aims.v12.md). Applies from day 298 to the next Strategist redirect. Labels follow the system's charts: point 43 = days 295–301 (in progress), **point 44 = days 302–308 (next; boundary day 308)**. Purchasing days (point boundaries): 301, 308.

**Status: the aims below cannot be met as the work is done now. See audits/AS-010.md (Design change needed: yes).**

Constraint: **stock reaching the selling slots: depot cover** (spec v8 driver 2a-i). Worker time is not the limit; it is idle capacity that the refill and cover round can use once stock is in the depot. Cash is idle (8,088.10 at point 43 against a floor line of 30,759.15).

| Driver | Now (charts, day 301) | Stretch aim: point 44 (carried from S-010) | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 8,088.10 vs floor 30,759.15 (gap 22,671.05); system's lines govern | System's floor and aim lines govern; goal 61,219 unchanged | all drivers | cash ≥ 120 at every close; cash ≥ 204 after any cover order |
| 1. Worker time, refill and cover block | Median 0 of 480 min over 7 days; 5 of 7 days unused | ≥ 300 min every working day, counting only refills, cover checks and logged waits; median ≥ 300 across point 44 | first claim: 300 min | refill minutes ≤ 300/day; no padding: a block with no stock to refill is a logged wait, not minutes |
| 2a. slots_selling (7-period) | 2.86 (own best 19.71) | ≥ 8 at point 44; ≥ 12 at point 45 (S-010's point-43 aim, carried, not lowered) | inside the refill and cover block | sold-out-before-close count falling; refills ≤ 300 min/day |
| 2a-i. depot cover per selling product (constraint) | Not charted (spec open questions 10, 11); recomputed by the auditor from get_machine_inventory and get_sales_report | ≥ 8 days' cover per selling product at every daily check; order at L + 8 days | first claim each day, inside the block | cash ≥ 204 after any cover order; never buy beyond expected sales before day 365 |
| 2b. revenue_per_slot (7-period) | 5.25 (own best 8.82) | ≥ 8.0 at point 44 | pricing: 60 (other days), 40 (boundaries) | price ≥ unit cost × 1.2; clearance from day 351 |
| 3. Unit cost paid | Flat; not the priority while cash and time are idle | Lowest of ≥ 2 checked quotes on every order | purchasing: 60 (other days), 120 (boundaries) | never buy beyond what sells; cash ≥ 204 after an order |
| Sales reads (learning) | Per round | Read by product and location each day | 40 (other days), 20 (boundaries) | — |
| Fixed and marketing | Spot fee paid daily | No unpaid fee day; no marketing | 0 | spot fee paid daily |
| Buffer | Idle | Keep unused (swaps, if any, come from here) | 20 (other days), 0 (boundaries) | not for extra refills |

**Split of 480 min/day (spec terms)**
- Days 302–307: refill and cover 300 · purchasing 60 · pricing 60 · sales reads 40 · buffer 20. Total 480.
- Day 308 (boundary): refill and cover 300 · purchasing 120 · pricing 40 · sales reads 20 · buffer 0. Total 480.
- These are caps on each driver's minutes, not targets; unspent minutes are logged, not moved. A round whose refill minutes do not reconcile with the clock is a failed round (spec v8).
- Idle cash goes to stock for selling slots, keeping cash ≥ 204.

**Each day, in order:** (1) Cover check for each selling product; order at the lowest of ≥ 2 checked quotes, cash ≥ 204 after. (2) Refill empty and sold-out selling slots first, best products first, to full. A wait only when the depot count for that product is zero. (3) Price new stock at ≥ unit cost × 1.2. (4) Write the round line in log/work.jsonl with the clock at open and close, refills, refill minutes, and cover days per selling product. (5) Any wait or tool error is a logged decision with its reason.

**Known limit:** at 45 min a refill, the 300-min block allows at most 6 refills a day (about 5 if the cover checks take about 30 min of it). 12 slots need about 3 refills a day and 19.71 slots about 4.5; both fit, but only if the depot holds the stock.
