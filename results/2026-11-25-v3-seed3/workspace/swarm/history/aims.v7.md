# Aims (version 7, after S-006 at day 126; written day 132, point 19; previous version in history/aims.v6.md)

Constraint: supply to slots. Worker time is no longer the limit: the charts show a median 270 of 480 min used over the last 7 days, 3 days unused. Slots stocked at day end: 7 latest, median 9 of 72. Capital: 7,207 of 7,487 idle. Refill minutes buy nothing without depot stock.

Aims for point 19 (days 127–133). Values are 7-period averages, judged on the charts at point 19. Point 20 (days 134–140) has no new aim; the split below holds until the Strategist's point-21 redirect.

| Driver | Now (point 18, S-006) | Stretch aim, point 19 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 15.14 (own best 20.0) | ≥ 20 (ceiling 72); first claim on the refill minutes | refills into slots with depot stock: 270 (56%), six 45-min trips | cash ≥ €120 every day; refill only into slots with depot stock |
| units per slot-day | 55.0 | ≥ 68, availability held | from the refill rows | availability held |
| revenue_per_slot | 7.32 (own best 8.15) | ≥ 8.2 | price setting and sales-report reads: 48 (10%) | price ≥ unit cost |
| cash (top measure) | 7,128 (point 18); floor line 5,113; aim 21,146; goal €61,219 | on or above the floor line; the aim is not expected to be met | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | improving (charts: /1.01 per point) | watched, not pushed; availability held | check_offers and orders: 48 (10%) | availability held; check_offers before every order |

Capacity split (480 min a day, per S-006):
- Refills into slots with depot stock: 270 (56%), six 45-min trips. First claim: slots_selling.
- Price setting and sales-report reads: 48 (10%).
- check_offers and orders: 48 (10%).
- Reads, admin, slack: 114 (24%). Core-day reads (get_status, get_machine_inventory, clock) come first from this row. Log spare time; do not fill it with unscheduled work.
- Marketing: 0.

Refill budget: the spec's milestone table caps refills at 60% of day-minutes (288 min); the spec's Budgets section sets no refill cap. The 270-minute split is inside both. A seventh trip (315 min, 66%) is outside the 60% milestone cap and is not in this split. It needs the design change flagged in AS-006.md before it runs.

Notes, in the spec's terms:
- Depot stock is the constraint. Before each refill, check that the fast seller has depot stock; if not, the refill minutes idle and are logged as a short, not filled with other work.
- Log each day: depot stock and sell-through per fast seller (uncharted, spec 2a), units per refill trip, minutes by tool, and the clock at day end.
- Before every order, check_offers at the planned quantity at all known suppliers. Size purchases to cover each fast seller to its lead time + 2 days, within the €120 reserve and 85% of deployable cash.
- The operator allowance is not published; do not assume a figure.

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; each fast seller's depot cover ≥ its supplier lead time + 2 days before a purchase; stock and marketing within 85% of deployable cash; spend only within the operator allowance.
