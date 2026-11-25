As of day 47 (after S-002; prior version in history/aims.v2.md)   Constraint: **depot stock** (S-002). Contested: refill minutes, see AS-002. Worker time: charts show median 450 of 480 min used, 30 idle (day 47).

| Driver | Now (charts, day 47) | Aim for point 7 (days 43–49) | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 3,083.9 at day 47 | Floor 1,961 at day 49; aim 2,673 (S-002) | all drivers | cash ≥ 120 at every close |
| 2a. slots_selling | 7-period average 18.57 (own best 19.43) | 7-period average ≥ 20 | refills 250 min/day (first claim) | refills ≤ 300 min/day; each sale-out before close counted |
| 2b. revenue_per_slot | 7-period average 8.29 (own best 8.78) | ≥ 8.8 | pricing and product mix 80 min/day (incl. swaps) | price ≥ unit cost × 1.2 |
| 3. Unit cost paid | rising ×1.01 (wrong way) | falls /1.03 per point or better; each order at the lowest of ≥ 2 checked quotes | quotes and purchasing 90 min on each point-boundary day | never buy beyond what sells; cash ≥ 120 after order (≥ 204 for depot cover) |
| Depot cover (the constraint) | not charted yet | every selling product ≥ 8 days cover, checked daily | inside the refill block | cash ≥ 204 after a cover order |
| Fixed and marketing | fee paid daily | zero unpaid fee days; no marketing | 0 min marketing | fee paid daily; marketing payback ≤ 30 days |
| Buffer | 30 min/day idle (charts) | keep unused | 110 min/day; 20 on boundary days | not for extra refills |

Split of 480 min/day, non-boundary days: refills 250 (2a) · pricing and mix 80 (2b) · sales reads 40 · buffer 110. Total 480.
Point-boundary days: refills 250 · quotes and purchasing 90 (3) · pricing and mix 80 · sales reads 40 · buffer 20. Total 480.

Notes, in order each day: (1) Depot cover check before refills (spec, from day 14): any selling product under 8 days of cover is ordered that day at the lowest of ≥ 2 checked quotes, cash ≥ 204 after the order. (2) Refill sold-out selling slots first, best products first, to full (18 or 10). (3) Price new stock at ≥ unit cost × 1.2. (4) Wait for the next day is always its own call. (5) Tortilla and oat have no depot stock: the cover check applies to them. (6) No deliberate price tests; no new slots or products without a sales read.

---
Copy note (AS-003, day 72): the text above is the day-47 aims as written by AS-002. The file as it stood when AS-003 was written also carried the day-69 edits, reproduced in full below (Reading line, note 4 changed):

As of day 47 (after S-002; prior version in history/aims.v2.md)   Constraint: **depot stock** (S-002). Contested: refill minutes, see AS-002. Worker time: charts show median 450 of 480 min used, 30 idle (day 47).

| Driver | Now (charts, day 47) | Aim for point 7 (days 43–49) | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 3,083.9 at day 47 | Floor 1,961 at day 49; aim 2,673 (S-002) | all drivers | cash ≥ 120 at every close |
| 2a. slots_selling | 7-period average 18.57 (own best 19.43) | 7-period average ≥ 20 | refills 250 min/day (first claim) | refills ≤ 300 min/day; each sale-out before close counted |
| 2b. revenue_per_slot | 7-period average 8.29 (own best 8.78) | ≥ 8.8 | pricing and product mix 80 min/day (incl. swaps) | price ≥ unit cost × 1.2 |
| 3. Unit cost paid | rising ×1.01 (wrong way) | falls /1.03 per point or better; each order at the lowest of ≥ 2 checked quotes | quotes and purchasing 90 min on each point-boundary day | never buy beyond what sells; cash ≥ 120 after order (≥ 204 for depot cover) |
| Depot cover (the constraint) | not charted yet | every selling product ≥ 8 days cover, checked daily | inside the refill block | cash ≥ 204 after a cover order |
| Fixed and marketing | fee paid daily | zero unpaid fee days; no marketing | 0 min marketing | fee paid daily; marketing payback ≤ 30 days |
| Buffer | 30 min/day idle (charts) | keep unused | 110 min/day; 20 on boundary days | not for extra refills |

Reading (v4, day 69, R-P-008): aims 2a and 2b are read against idle slots (of 72) and idle worker minutes; cash is the top measure's watch, not the driver's. The numbers above stand; none is lowered.

Split of 480 min/day, non-boundary days: refills 250 (2a) · pricing and mix 80 (2b) · sales reads 40 · buffer 110. Total 480.
Point-boundary days: refills 250 · quotes and purchasing 90 (3) · pricing and mix 80 · sales reads 40 · buffer 20. Total 480.

Notes, in order each day: (1) Depot cover check before refills (spec, from day 14): any selling product under 8 days of cover is ordered that day at the lowest of ≥ 2 checked quotes, cash ≥ 204 after the order. (2) Refill sold-out selling slots first, best products first, to full (18 or 10). (3) Price new stock at ≥ unit cost × 1.2. (4) A wait is a logged decision: an empty selling slot with depot stock, or a product under its cover threshold, is not waited on; any wait gives its reason in the round line (v4, day 69). (5) Tortilla and oat have no depot stock: the cover check applies to them. (6) No deliberate price tests; no new slots or products without a sales read.
