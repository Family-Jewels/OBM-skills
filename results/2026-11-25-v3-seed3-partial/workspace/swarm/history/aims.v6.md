# Aims (AS-005, day 111, point 16; replaces the AS-004 aims, kept in history/aims.v5.md)

Constraint: worker time, unspent (S-005, day 105). Charts: median 225 of 480 min used over the last 7 days, 255 idle. Depot stock timing still limits what the slots can hold; the change for that is pending (see below).

Stretch aims for point 16 (days 106–112). Applies from day 111; carried to point 17 until the next Strategist redirect.
1. Depot cover 7–10 days on at least 5 of 7 days, each order from a same-day check_offers quote. Not on charts yet: record it in progress.md each day.
2. slots_selling ≥ 20 of 72 (7-period average). Own best 14.57; upper limit 22.09.
3. revenue_per_slot ≥ 10.5 (own best 10.57), no sale below unit cost.

Top measure: cash holds the floor line (point 16: 3,967) and celeration ≥ x1.08. The aim line (13,817) is not reachable this point; expect a miss and do not chase it.
Capacity, not a driver: median worker time used ≥ 350 min a day.

Capacity split (480 min a day, spec worker-time measure, by driver)

| Driver (spec term) | Min a day | Share | Covers |
| --- | --- | --- | --- |
| depot cover (incl. unit_cost_paid_30d) | 216 | 45% | check_offers, orders, receipts, depot reads |
| slots_selling | 168 | 35% | refills; depot cover checked before each |
| revenue_per_slot | 48 | 10% | price calls; sales-report reads |
| reserve | 48 | 10% | unplanned calls; never used to exceed 480 |
| campaigns | 0 | 0% | none before M3 |

Notes: first each day, depot sourcing (check_offers, orders, receipts), then refills. Order when cover falls below supplier lead time + 2 days. Charge each call its clock minutes to its driver in swarm/log/minutes.jsonl.

Pending design change (not in force until adopted): a refill waits for a delivered receipt that confirms stock, against a same-day quote from a live supplier; a replacement supplier is named if one closes. Until adopted, the spec v3 stock rule applies.

Guardrails (from the spec, unchanged)
- Cash ≥ EUR 120 every day.
- No sale below unit cost; margin ≥ 0 on every selling slot.
- Never past 480 min a day.
- Cover above 14 days is idle capital: do not order more.
- No price experiments. No campaign spend before M3.
