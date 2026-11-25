As of day 23 (after S-001; prior version in history/aims.v1.md)   Constraint: **depot stock** (upstream of the slots; the charts do not measure it yet). Worker time is not the limit: median 330 of 480 min used, 150 idle.

| Driver | Now | Stretch aim for point 4 (days 21–27) | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash (final bank balance path) | 1,129.5 at day 23; 1,443.70 at day 21 | Cash floor 1,559 at day 28; aim 1,689 | all drivers | cash ≥ 120 at every close |
| 2a. slots_selling | 19 latest; 7-period average 10.86 | 7-period average ≥ 18, each machine ≥ 3 | refills 225 min/day (first claim) | refills ≤ 300 min/day; each sale-out before close counted |
| 2b. revenue_per_slot | 7-period average 6.94 (own best 7.26) | ≥ 7.5 | pricing and product mix 75 min/day (incl. swaps) | price ≥ unit cost × 1.2 |
| 3. Unit cost paid | falling, /1.02 (provisional, not proof) | falls at /1.03 per point or better; each order at the lowest of ≥ 2 checked quotes | quotes and purchasing 90 min on each point-boundary day | never buy beyond what sells; cash ≥ 120 after order (≥ 204 for depot cover) |
| 4. Fixed and marketing | fee paid daily | zero unpaid fee days; no marketing | 0 min marketing (hold) | fee paid daily; marketing payback ≤ 30 days |
| Buffer | 50 min/day | keep unused | 50 min/day | not for extra refills |

Split of 480 min/day: refills 225 (2a) · quotes and purchasing 90 (3, boundary days) · pricing and mix 75 (2b, incl. swaps) · sales reads and learning 40 · buffer 50 · marketing 0. Total 480.

Notes: (1) Depot stock is the constraint: check every selling product's cover daily (last 7 days' average sales × 8 days). A product short of cover is ordered that day at the lowest of ≥ 2 checked quotes, within cash ≥ 204 after the order. This is the spec's depot-cover rule, which the spec starts at day 14; the Strategist asks for it now. Until the spec changes, it cannot be applied as written (see AS-001). (2) Refill sold-out selling slots first, best products first. (3) Price new stock at ≥ unit cost × 1.2. (4) No deliberate price tests; no new slots or products without a sales read.
