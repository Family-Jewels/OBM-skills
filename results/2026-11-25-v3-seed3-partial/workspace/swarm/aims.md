# Aims (AS-006, day 132, point 19; replaces the AS-005 aims, kept in history/aims.v6.md)

Constraint: worker time, unspent (S-006, day 126). Charts: median 50 of 480 min used, 430 idle. Depot cover not yet charted (aim 2 is judged from progress.md).

Stretch aims for point 19 (days 127–133), carried to point 20 until the next Strategist redirect.
1. Worker time median ≥ 350 min a day (the capacity gate).
2. Depot cover 7–10 days on at least 5 of 7 days, each order from a same-day check_offers quote. Record it in progress.md each day.
3. slots_selling ≥ 12 (7-period average). Own best 14.57; upper limit 22.09 is not a target.
4. revenue_per_slot ≥ 10.5 (own best 10.57), no sale below unit cost.

Top measure: cash ≥ 4,990 (floor 4,618 × 1.08) and celeration ≥ x1.08. Aim line (22,860) is not reachable this point; expect a miss and do not chase it.

Capacity split (480 min a day, spec worker-time measure, by driver; unchanged)

| Driver (spec term) | Min a day | Share | Covers |
| --- | --- | --- | --- |
| depot cover (incl. unit_cost_paid_30d) | 216 | 45% | check_offers, orders, receipts, depot reads |
| slots_selling | 168 | 35% | refills; depot cover checked before each |
| revenue_per_slot | 48 | 10% | price calls; sales-report reads |
| reserve | 48 | 10% | unplanned calls; never used to exceed 480 |
| campaigns | 0 | 0% | none before M3 |

Notes: first each day, depot sourcing (check_offers, orders, receipts), then refills. Order when cover falls below supplier lead time + 2 days. Minutes not used by depot sourcing go to refills only after cover is checked. Charge each call its clock minutes to its driver in swarm/log/minutes.jsonl.

Pending design change (not in force until adopted): a refill waits for a delivered receipt that confirms stock, against a same-day quote from a live supplier; a replacement supplier is named if one closes. Adopt only if, at the point-19 pulse, worker time has reached 350 and slots_selling is still below 12. Until then, the spec v3 stock rule applies.

Guardrails (from the spec, unchanged)
- Cash ≥ EUR 120 every day.
- No sale below unit cost; margin ≥ 0 on every selling slot.
- Never past 480 min a day.
- Cover above 14 days is idle capital: do not order more.
- No price experiments. No campaign spend before M3.
