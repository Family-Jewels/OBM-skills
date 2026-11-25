As of day 95 (after S-004, day 91, point 13). Prior version: history/aims.v4.md. Applies to point 14 (days 91–97) and carries into point 15 (days 98–104) until the next Strategist redirect.   Constraint: **stock reaching the selling slots**: depot cover (S-004). Worker time is not the limit (system charts, day 95: median 365 of 480 min used, 115 idle).

| Driver | Now (system charts) | Stretch aim, point 14 | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 4,553.9 at day 95; floor 3,101.71 and aim 8,480.06 at point 13 | System's floor and aim lines govern; goal 61,219 unchanged; required ×1.07 per point | all drivers | cash ≥ 120 at every close |
| 2a. slots_selling | 7-period average 17.57 (own best 19.71); latest 16 | 7-period average ≥ 20 | refill and depot cover, 300 min/day (other days) | refills ≤ 300 min/day unless the stock-out count is falling; sold-out-before-close count falling |
| 2a-i. depot cover per selling product (constraint) | Not yet a system chart. Operator logs cover_days per round; zero for crisps, energy, cola, choco on day 89 | Every selling product ≥ 8 days' cover at each daily check, on the lead time observed from that supplier | inside the refill and cover block | cash ≥ 204 after any cover order; never buy beyond expected sales before day 365 |
| 2b. revenue_per_slot | 7-period average 8.22 (own best 8.78) | ≥ 8.8 | pricing and mix 80 min/day (other days); 70 on boundary days | price ≥ unit cost × 1.2 (clearance excepted from day 351) |
| 3. Unit cost paid | Charts: collecting, no level yet | Not a priority while cash is idle; lowest of ≥ 2 checked quotes on every order | purchasing 30 min/day (other days); 90 on boundary days | never buy beyond what sells; cash ≥ 204 after an order |
| Fixed and marketing | Fee paid daily | No unpaid fee day; no marketing | 0 min marketing | spot fee paid daily; marketing payback ≤ 30 days |
| Buffer | Idle | Keep unused | 30 min/day (other days); 20 on boundary days | not for extra refills |

**Split of 480 min/day (spec terms)**
- Other days: refill and depot cover 300 · purchasing (cover orders off the boundary) 30 · price and mix 80 · sales reads 40 · buffer 30. Total 480.
- Point-boundary days (98, 105, …): refill and cover 260 · purchasing 90 · price 70 · sales reads 40 · buffer 20. Total 480.

**Each day, in order:** (1) Cover check: for each selling product, cover (stock on hand ÷ last 7 days' average sales) against the observed lead time of each supplier; order below trigger at the lowest of ≥ 2 quotes, from a supplier whose lead time fits. Bakker's last two deliveries took 14–15 days, so it cannot hold 8 days' cover; use zuidas or kanaal for those products. (2) Refill sold-out and empty selling slots first, best products first, to full. (3) Price new stock at ≥ unit cost × 1.2. (4) Log cover days per selling product in the round's work.jsonl line. (5) Any wait is a logged decision with its reason in the round line.

**Known limit:** at 45 min a refill, the 300-min block allows about 6 refills a day. If the 20-slot aim needs more, the cap binds first; the Strategist decides that, not the operator.
