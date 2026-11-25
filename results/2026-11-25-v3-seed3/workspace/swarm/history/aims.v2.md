# Aims (version 2, after S-001 at day 23; previous version in history/aims.v1.md)

As of day 23 (after S-001)   Constraint: worker time (480 min per working day, 09:00–17:00), as S-001 states. Conflict open: see audits/AS-001.md (charts show 360 min median used, not 450).

| Driver | Latest (charts) | Aim for the next point (day 28) | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| revenue (7-period average) | 143.59 own best | ≥ 130.6 (as S-001) | from the lines below | cash ≥ €120 every day |
| slots_selling | 25 | ≥ 24 (as S-001) | refills: 312 (65%) | cash ≥ €120 every day |
| revenue_per_slot | 8.27 | ≥ 8.0 (as S-001) | price and sales-report reads: 48 (10%) | price ≥ unit cost |
| unit_cost_paid_30d | rising ×1.03 per point | watch, not a priority (as S-001) | check_offers and orders: 48 (10%) | availability held; every-purchase check in spec still applies |

Capacity split (480 min a day, as S-001):
- Refills, fast-selling rows first (slots_selling, revenue_per_slot): 312 min = six 45-min trips (270) plus 42 min that cannot fund a seventh trip.
- Price setting and sales-report reads: 48 min.
- check_offers and orders: 48 min.
- Reads, reports, admin: 24 min.
- Swaps (30 min each) and slack: 48 min.
- Marketing: 0 until the next point.

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; no unit-cost gain bought at the cost of availability.

Notes, in the spec's terms:
- Each working day: get_status and get_machine_inventory first, record the clock. Then refill and price fast sellers first.
- Before every order, check_offers at the planned quantity. Never let purchases take cash below €120.
- If refills are still under 60% of worker time at day 28, the work itself must change (S-001). Minutes by tool must be published for this check; see AS-001.
