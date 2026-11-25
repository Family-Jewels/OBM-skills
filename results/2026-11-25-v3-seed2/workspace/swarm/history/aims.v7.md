As of day 121 (after S-005, day 112, point 16; prior version history/aims.v6.md). Applies to point 18 (days 120–126) and carries until the next Strategist redirect. S-005's aims were labelled point 17 (days 113–119), which had ended; they are carried unchanged, not lowered. Pending: R-P-010's revert condition is met (AS-005); these aims stand until the diagnosis and any redesign land.   Constraint: **stock reaching the selling slots: depot cover** (S-005). Worker time is not the limit: most days leave 300+ of 480 min idle.

| Driver | Now (system charts, metrics day 122) | Stretch aim, point 18 | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: cash | 5,325 at day 122; point 17: 5,229.90 vs floor 4,211.64, aim 16,530.21 | System's floor and aim lines govern; goal 61,219 unchanged | all drivers | cash ≥ 120 at every close |
| 2a. slots_selling | 7-period average 7.0 (own best 19.71); 0 selling on days 119–120, 16 on day 122 | 7-period average ≥ 20 | refill and depot cover, 300 min/day (other days) | refills ≤ 300 min/day unless stock-out count is falling; sold-out-before-close count falling |
| 2a-i. depot cover per selling product (constraint) | Not a system chart yet (requested). Last logged cover: day 89, zero for crisps, energy, cola, choco. No round lines in work.jsonl after day 89 | Every selling product ≥ 8 days' cover at each daily check, under spec v5 (order at L + 8 days' cover, L = longest delivery of the chosen supplier in its last 3 receipts) | inside the refill and cover block | cash ≥ 204 after any cover order; never buy beyond expected sales before day 365 |
| 2b. revenue_per_slot | 7-period average 5.27 (own best 8.79) | ≥ 8.8 | pricing and mix 80 min/day (other days) | price ≥ unit cost × 1.2 (about 1.25 at paid unit cost 1.044); clearance from day 351 |
| 3. Unit cost paid | 1.044, wrong way on celeration (charts) | Not a priority while cash is idle; lowest of ≥ 2 checked quotes on every order | purchasing 30 min/day (other days) | never buy beyond what sells; cash ≥ 204 after an order |
| Fixed and marketing | Fee paid daily | No unpaid fee day; no marketing | 0 min marketing | spot fee paid daily; marketing payback ≤ 30 days |
| Buffer | Idle | Keep unused | 30 min/day (other days) | not for extra refills |

**Split of 480 min/day (spec terms)**
- Days 120–125: refill and depot cover 300 · purchasing 30 · price and mix 80 · sales reads 40 · buffer 30. Total 480.
- Point-boundary day 126: refill and cover 260 · purchasing 90 · price 70 · sales reads 40 · buffer 20. Total 480.

**Each day, in order:** (1) Cover check under spec v5, for each selling product, from the supplier whose L fits; order at the lowest of ≥ 2 checked quotes. (2) Refill empty and sold-out selling slots first, best products first, to full. (3) Price new stock at ≥ unit cost × 1.2. (4) Write the round line in log/work.jsonl with cover days per selling product; a day with no round line is a failed round. (5) Any wait is a logged decision with its reason in the round line.

**Known limit:** at 45 min a refill, the 300-min block allows about 6 refills a day. If the 20-slot aim needs more, the cap binds first; the Strategist decides that, not the operator.
