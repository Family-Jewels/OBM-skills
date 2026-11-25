# Aims (version 6, after S-005 at day 105; written day 109, point 15; previous version in history/aims.v5.md)

Constraint: the worker's own time. At 0 of 480 min used on day 105's charts, the cheapest opening is unused capacity. Refill minutes buy nothing without depot stock, so spend them on refills into slots that have depot stock, then on prices.

Aims for point 16 (days 106–112). Values are 7-period averages. Judged at point 16 on the charts.

| Driver | Now (point 15) | Stretch aim, point 16 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 8.57 (own best 20.0); wrong-way /1.84 | ≥ 14 (ceiling 72); first claim on the refill minutes | refills: 270 (56%), six 45-min trips | cash ≥ €120 every day; refill only into slots with depot stock |
| units per slot-day | 29.14 (own best 80.86); flat | ≥ 40, availability held | from the refill rows | availability held |
| revenue_per_slot | 6.24 (own best 8.02); flat | ≥ 8.0 | price and sales-report reads: 48 (10%) | price ≥ unit cost |
| cash (top measure) | 5,913 (point 15); floor line 4,107; aim 13,098; goal €61,219 | on or above the floor line | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | last value 0.897 (day 45) | watched, not pushed; no rise, availability held | check_offers and orders: 48 (10%) | availability held; check_offers before every order |

Capacity split (480 min a day; refill budget ≤ 60% of day-minutes, spec Budgets):
- Refills into slots with depot stock: 270 (56%), six 45-min trips.
- Price setting and sales-report reads: 48 (10%).
- check_offers and orders: 48 (10%).
- Reads, admin, slack: 114 (24%). Log spare time; do not fill it with unscheduled work.
- Marketing: 0.

If depot stock is short, refill minutes idle and that is logged as a short, not filled with other work. Depot cover (spec 2a) is still uncharted; the operator logs depot stock and sell-through per fast seller each day until it is.

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; each fast seller's depot cover ≥ its supplier lead time + 2 days before a purchase; stock and marketing within 85% of deployable cash; spend only within the operator allowance (not yet published; do not assume a figure).

Notes, in the spec's terms:
- Each working day: get_status and get_machine_inventory first, and record the clock.
- Each day, log units per refill trip, minutes by tool, the clock at day end, and depot stock and sell-through per fast seller.
- Before every order, check_offers at the planned quantity. Never let purchases take cash below €120.
