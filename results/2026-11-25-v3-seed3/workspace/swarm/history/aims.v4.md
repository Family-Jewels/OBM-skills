# Aims (version 4, after S-003 at day 63; written day 72, point 10; previous version in history/aims.v3.md)

Constraint: supply to the slots (depot stock and cover, spec 2a). Depot cover is still not charted. Worker time is still in dispute: the Strategist cites median 305 of 480 min used; charts.md shows median 0 used and 4 of the last 7 days unused (spec open question 6). Settle it before judging the capacity split.

Aims for point 10 (days 70–76). Values are 7-period averages. "Now" is charts.md's latest 7-period value; the Strategist's day-63 figures are in audits/AS-003.md.

| Driver | Now (charts) | Aim for point 10 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 10.57 (own best 20.0; routine upper limit 24.03) | ≥ 24.0 (ceiling 72); judged on the record | refills: 270 (56%), six 45-min trips | cash ≥ €120 every day |
| units per slot-day | 33.86 (own best 80.86) | ≥ 80, availability held | from the refill rows | availability held |
| revenue_per_slot | 5.89 (own best 8.02) | ≥ 8.5, price ≥ unit cost | price and sales-report reads: 48 (10%) | price ≥ unit cost |
| revenue | 70.96 (own best 167.03) | follows from the rows above; not pushed separately | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | not charted at a level; last value 0.897 (day 45) | no rise per point, availability held | check_offers and orders: 48 (10%) | availability held; check_offers before every order |

Capacity split (480 min a day, within the spec's refill budget of ≤ 60% of day-minutes):
- Refills, fast sellers first, only into slots with depot stock: 270 (56%), six 45-min trips.
- Price setting and sales-report reads: 48 (10%).
- check_offers and orders: 48 (10%).
- Reads, admin, swaps and slack: 114 (24%). Log spare time; do not fill it with unscheduled work.
- Marketing: 0.

Pending, not adopted: the Strategist's refill split of 330 min (69%; seven 45-min trips is 315, so 330 needs confirming). It exceeds the spec's ≤ 60% refill budget (288 min) in the milestone table. It takes effect only when a redesign revises that budget (audits/AS-003.md: Design change needed: yes).

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; stock and marketing within 85% of deployable cash.

Notes, in the spec's terms:
- Each working day: get_status and get_machine_inventory first, and record the clock.
- Refill fast sellers first. Do not spend refill minutes on a slot whose depot stock is zero.
- Each day, log units per refill trip, minutes by tool, the clock at day end, and depot stock and sell-through per fast seller. The system needs these to settle the worker-time record and to chart depot cover.
- Before every order, check_offers at the planned quantity. Never let purchases take cash below €120.
