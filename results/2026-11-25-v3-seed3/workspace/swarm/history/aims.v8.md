# Aims (version 8, after S-007 at day 147; written day 156, point 23; previous version in history/aims.v7.md)

Constraint: supply to slots. Worker time is 56% used (median 270 of 480 min, 210 idle), so idle minutes are not the limit. Depot stock is: slots stocked at day end fell to 19 of 72 at point 21, and refill minutes buy nothing without it. Capital: 7,749 idle while 53 slots are empty.

Aims for point 23 (days 155–161), from S-007. S-007's window (point 22, days 148–154) closed before this update, so its aims carry to the next point. Values are 7-period averages, judged on the charts at point 23.

| Driver | Last reading (S-007) | Stretch aim, point 23 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 15.86 mean since day 141; latest 11 (own best 20) | ≥ 22 (ceiling 72); first claim on the refill minutes | refills into slots with depot stock: 270 (56%), six 45-min trips | cash ≥ €120 every day; refill only into slots with depot stock |
| units per slot-day | 49.7 mean; latest 17 | ≥ 60 (pre-redesign level 55), availability held | from the refill rows | availability held |
| revenue_per_slot | 6.52 mean; latest 3.03 (own best 8.15) | ≥ 8.2 | price setting and sales-report reads: 60 (12.5%) | price ≥ unit cost |
| cash (top measure) | 7,894 (point 21); floor line on the charts | on or above the floor line; the aim is not expected to be met | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | watched, not pushed | availability held | check_offers and orders: 60 (12.5%) | availability held; check_offers before every order; each fast seller's depot cover ≥ lead time + 2 days before a purchase |

Capacity split (480 min a day, per S-007):
- Refills into slots with depot stock: 270 (56%), six 45-min trips. First claim: slots_selling. Within the spec's 60% milestone cap (288 min).
- check_offers and orders: 60 (12.5%), sized to depot cover at lead time + 2 days.
- Price setting and sales-report reads: 60 (12.5%), revenue_per_slot.
- Core-day reads, admin, slack: 90 (19%). Core-day reads (get_status, get_machine_inventory, clock) come first from this row. Log spare time; do not fill it with unscheduled work.
- Marketing: 0.

Notes, in the spec's terms:
- Depot stock is the constraint. Before each refill, check that the fast seller has depot stock; if not, the refill minutes idle and are logged as a short, not filled with other work.
- Log each day: the DEPOT field (depot units and units sold per day, per fast seller; spec 2a), units per refill trip, minutes by tool, and the clock at day end.
- Before every order, check_offers at the planned quantity at all known suppliers. Size purchases to cover each fast seller to its lead time + 2 days, within the €120 reserve and 85% of deployable cash. Idle cash is not a reason to skip a cover-backed order.
- The operator allowance is not published; do not assume a figure.

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; each fast seller's depot cover ≥ its supplier lead time + 2 days before a purchase; stock and marketing within 85% of deployable cash; spend only within the operator allowance.
