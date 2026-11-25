# Aims (version 3, after S-002 at day 42; written day 45, point 6; previous version in history/aims.v2.md)

As of day 45 (after S-002)   Constraint: supply to the slots (depot stock and cover, spec 2a), not yet on the charts. Worker time is not the binding limit: median used 315 of 480 min (66%), 165 idle (charts.md).

Aims for point 7 (day 49). Values are 7-period averages from charts.md.

| Driver | Now (charts) | Aim for point 7 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 15.43 (own best 20.0) | ≥ 20.0 | refills: 270 (56%), six 45-min trips | cash ≥ €120 every day |
| revenue_per_slot | 6.87 (own best 8.02) | ≥ 8.0 | price and sales-report reads: 48 (10%) | price ≥ unit cost |
| revenue | 111.39 (own best 167.03) | ≈ 160; follows from the two rows above, not pushed separately | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | 0.897, rising ×1.03 per point | no rise: ≤ 0.897 per point, availability held | check_offers and orders: 48 (10%) | availability held; check_offers before every order |

Capacity split (480 min a day, within the spec's refill budget of ≤ 60% of day-minutes):
- Refills, fast sellers first, only into slots with depot stock: 270 (56%), six 45-min trips.
- Price setting and sales-report reads: 48 (10%).
- check_offers and orders: 48 (10%).
- Reads, admin, swaps and slack: 114 (24%). Log any spare time; do not fill it with unscheduled work.
- Marketing: 0.

Pending, not adopted: the Strategist's split of refills 360 (75%, eight trips). It exceeds the spec's ≤ 60% refill budget. It takes effect only when a redesign revises that budget (audits/AS-002.md: Design change needed: yes).

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; stock and marketing within 85% of deployable cash.

Notes, in the spec's terms:
- Each working day: get_status and get_machine_inventory first, and record the clock.
- Refill fast sellers first. Do not spend refill minutes on a slot whose depot stock is zero.
- Each day, log units per refill trip, minutes by tool and the clock at day end. The system needs these to settle the worker-time record (spec open question 6).
- Before every order, check_offers at the planned quantity. Never let purchases take cash below €120.
