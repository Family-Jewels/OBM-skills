As of day 351 (after S-011, day 336, redirect; prior version history/aims.v13.md). Applies from day 351 to day 365 (end). Points are the system's: the S-011 aims for days 337–350 have passed and are not judged here.

**Status: Design change needed: yes. See audits/AS-011.md.** Two rules in spec v9 conflict with these aims from day 351 (cover trigger has no end-of-horizon exception; clearance pricing from day 351). The aims below follow the spec's end-state rules and do not change the spec.

Constraint: **worker time in the refill and cover block (first claim), with depot stock as the gate** (S-011). Cash is idle (8,413.70 at day 336 against a floor of 45,085.46); the top measure cannot reach its goal, so the aims below are the working targets, not the goal.

| Driver | Stretch aim, days 351–357 | Share of worker time | Guardrail |
| --- | --- | --- | --- |
| 1. Worker time, refill and cover block | ≥ 300 min each working day, counting refill, cover-check and re-pricing minutes only; logged waits are not minutes; median ≥ 300 | first claim: 300 min | refill minutes ≤ 300/day and reconciled to the clock; no padding |
| 2a. slots_selling | ≥ 12 at the day-357 check, with every stocked slot sellable before day 365; no new slots added after day 351 | inside the block | sold-out-before-close count falling; cash ≥ 120 at every close |
| 2a-i. depot cover per selling product | ≥ 8 days' cover at every daily check while 8 days remain to day 365; from day 358, cover target = days left to day 365 | first claim each day, inside the block | cash ≥ 204 after any order; buy only stock that arrives and sells by day 365 |
| 2b. revenue per slot | Price ≥ unit cost × 1.2 until day 350; from day 351, clearance pricing on remaining stock (spec). The ≥ 8.0 aim is dropped for this window | pricing: 40 | clearance per spec; no price below unit cost after stock is sold |
| 3. Unit cost paid | Lowest of ≥ 2 checked quotes on any order placed | purchasing: 90 (days 351, 357 only) | never buy beyond what sells before day 365 |
| Sales reads (learning) | Read by product and location each day | 30 | — |
| Buffer | Keep unused | 20 | not for extra refills |

**Split of 480 min/day (spec terms, S-011's split):** refill and cover 300 · purchasing 90 (days 351 and 357 only; other days move to refill and cover, up to 300 total) · pricing 40 · reads 30 · buffer 20. Caps on each driver's minutes, not targets; unspent minutes are logged, not moved.

**From day 358:** no purchase unless it arrives and sells before day 365; no cover buying beyond that; clearance on all remaining stock; no open orders by day 365.

**Each day, in order:** (1) Cover check per selling product against the rule above; order only at the lowest of ≥ 2 checked quotes, cash ≥ 204 after. (2) Refill empty and sold-out selling slots first, best products first, to full; wait only when the depot count is zero. (3) Price per the window above. (4) Write the round line in log/work.jsonl (clock at open and close, refills, refill minutes, cover days per product). (5) Any wait or tool error is a logged decision with its reason.

**Known limit:** at 45 min a refill, the 300-min block allows about 6 refills a day. Clearance and endgame cover checks take part of the block, so expect about 5.
