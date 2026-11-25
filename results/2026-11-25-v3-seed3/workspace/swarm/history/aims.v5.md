# Aims (version 5, after S-004 at day 84; written day 91, point 13; previous version in history/aims.v4.md)

Constraint: supply to the slots. Worker time is not the limit: charts.md shows median 75 of 480 min used (16%), 3 of the last 7 days unused, and 405 min idle. Depot cover (spec 2a) is still not charted, so refill minutes may buy nothing until it is.

Aims for point 14 (days 92–98). Values are 7-period averages. "Now" is the 7-period value on the charts (own-best table); the Strategist's S-004 figures are in audits/S-004.md.

| Driver | Now | Aim for point 14 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 15.57 (own best 20.0; routine upper limit 24.03) | ≥ 24.0 (ceiling 72); judged on the record | refills: 270 (56%), six 45-min trips | cash ≥ €120 every day; refill only into slots with depot stock |
| revenue_per_slot | 5.79 (own best 8.02) | ≥ 8.5 | price and sales-report reads: 48 (10%) | price ≥ unit cost |
| units per slot-day | 46.86 (own best 80.86) | ≥ 60, availability held; restore 80 once slots_selling reaches 24 | from the refill rows | availability held |
| cash | latest 5,449.37 (point 13); floor line 3,548.72 | on or above the floor line | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | not charted at a level; last value 0.897 (day 45) | watched, not pushed; no rise, availability held | check_offers and orders: 48 (10%) | availability held; check_offers before every order |

Capacity split (480 min a day, within the spec's refill budget of ≤ 60% of day-minutes):
- Refills, fast sellers first, only into slots with depot stock: 270 (56%), six 45-min trips.
- Price setting and sales-report reads: 48 (10%).
- check_offers and orders: 48 (10%).
- Reads, admin, swaps and slack: 114 (24%). Log spare time; do not fill it with unscheduled work.
- Marketing: 0.

Not adopted: the Strategist's 66% refill split (315 min, seven trips). It exceeds the spec's ≤ 60% refill budget (288 min). It takes effect only when a redesign revises that budget (audits/AS-004.md: Design change needed: yes).

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; each fast seller's depot cover ≥ its supplier lead time + 2 days before a purchase; stock and marketing within 85% of deployable cash; spend only within the operator allowance (not yet published; do not assume a figure).

Notes, in the spec's terms:
- Each working day: get_status and get_machine_inventory first, and record the clock.
- Each day, log units per refill trip, minutes by tool, the clock at day end, and depot stock and sell-through per fast seller. The system needs these to settle the worker-time record and to chart depot cover.
- Before every order, check_offers at the planned quantity. Never let purchases take cash below €120.
