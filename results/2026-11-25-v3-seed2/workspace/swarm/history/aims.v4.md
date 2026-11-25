As of day 72 (after S-003, point 9; prior version in history/aims.v3.md). Applies to point 11, days 71–77.   Constraint: **stock reaching the selling slots** (S-003). Worker time is not the limit (charts: 455 of 480 min idle). Refill is fixed at 45 min each (spec), so refill throughput is capped by the 300-min guardrail. Depot cover is not yet charted.

| Driver | Now (charts, day 72) | Stretch aim, point 11 (days 71–77) | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 3,576.7 at day 72 | Floor ≈ 2,663 and aim ≈ 6,066 at day 77 (the system's lines on charts govern) | all drivers | cash ≥ 120 at every close |
| 2a. slots_selling | 7-period average 8.86 (own best 19.71) | 7-period average ≥ 21 | refill and depot cover 280 min/day | refills ≤ 300 min/day; sold-out-before-close count falling |
| 2a-i. depot cover per selling product (constraint) | not charted; zero for crisps, cola, choco, oat at day 71 | every selling product ≥ 8 days cover at each daily check, using each supplier's last observed lead time | inside the refill and cover block | cash ≥ 204 after a cover order; never buy beyond expected sales before day 365 |
| 2b. revenue_per_slot | 7-period average 4.63 (own best 8.78) | ≥ 9.0 | pricing and mix 80 min/day | price ≥ unit cost × 1.2 |
| 3. Unit cost paid | 1.000 (rising from 0.969 at day 63) | falls /1.03 per point (≈ 0.97 by day 77); each order at the lowest of ≥ 2 checked quotes | purchasing 30 min on other days; 90 on day 77 | never buy beyond what sells; cash ≥ 204 after order |
| Fixed and marketing | fee paid daily | zero unpaid fee days; no marketing | 0 min marketing | spot fee paid daily; marketing payback ≤ 30 days |
| Buffer | idle | keep unused | 50 min/day on other days; 20 on day 77 | not for extra refills |

**Split of 480 min/day (spec terms)**
- Other days: refill and depot cover 280 · purchasing (cover orders off the point boundary) 30 · price and swap 80 · sales reads 40 · buffer 50. Total 480.
- Day 77 (point boundary): refill and depot cover 260 · purchasing (quotes and orders) 90 · price 70 · sales reads 40 · buffer 20. Total 480.

**Each day, in order:** (1) depot cover check against each product's observed lead time; order any product below its trigger at the lowest of ≥ 2 quotes. (2) Refill sold-out selling slots first, best products first, to full. (3) Price new stock at ≥ unit cost × 1.2. (4) Log cover days per selling product in the round's work.jsonl line. (5) A wait is a logged decision, with its reason in the round line (v4, day 69). (6) Wait for the next day is always its own call.
