# Aims (version 12; after S-011 at day 273, point 39; written day 293, point 42; previous version in history/aims.v11.md)

Constraint: the worker's own time. The charts show 0 of 480 min median used over the last 7 days (7 days unused). Behind it: slot stock (0 of 72 stocked at day end) and depot cover, which is not yet charted. The split below has not run. See audits/AS-011.md.

Aims from S-011, for point 43 (days 295–301), the next point. S-011's window (point 40, days 274–280) closed before this update; its levels carry unchanged to point 43. 7-period averages. The floor and aim lines are the system's: read them on charts.md, not here.

| Driver | Last reading (charts.md, point 42) | Stretch aim, point 43 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | latest 0; chart centre 3.3 (since day 209); own best 20 | ≥ 12 (ceiling 72); first claim on the minutes | refills into slots with depot stock: 270 (56%), six 45-min trips | cash ≥ €120 every day; refill only into lines with depot stock |
| units (chart total daily units) | latest 0; chart centre 2.15 (since day 221); own best 80.86 | ≥ 20, availability held | from the refill rows | availability held |
| revenue_per_slot | latest 0; chart centre 5.49 (since day 183); own best 8.51 | ≥ 8.5 | price setting and sales-report reads: 60 (12.5%) | price ≥ unit cost |
| cash (top measure) | 9,566.17 at point 42; floor line 29,495.41; aim line 122,438 | on or above the floor line; not expected to be met this point | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | watched, not pushed | availability held | check_offers and orders: 90 (19%) | check_offers at all suppliers before every order; each fast seller's depot cover ≥ lead time + 2 days before a purchase; no stock bought whose sell-through cannot reach day 365 |

Note on the units aim: the label says "units per slot-day", but the figures are the chart's total daily units. The aim is applied to that row. Strategist to confirm the label.

Capacity split (480 min a day, per S-011; shares unchanged):
- Refills into slots with depot stock: 270 (56%), six 45-min trips. First claim: slots_selling.
- check_offers and orders: 90 (19%), sized to depot cover at lead time + 2 days.
- Price setting and sales-report reads: 60 (12.5%), revenue_per_slot.
- Core-day reads and admin: 60 (12.5%). Core reads (get_status, get_machine_inventory, clock) come first.
- Marketing: 0.

Notes, in the spec's terms:
- Each working day: core reads first, then check each fast seller's depot stock before its refill. If the depot is empty for a line, log the short and do not refill that line.
- Write the DEPOT line, the clock time and the refill trip count every working day (spec 2a; open questions 8 and 10). Until depot cover and clock minutes are charted, these lines are the only record of them.
- Each refill trip is read back: slot stock before and after, clock before and after.
- Before every order, check_offers at the planned quantity at all known suppliers. Size each fast seller to lead time + 2 days, within the €120 reserve and 85% of deployable cash.
- The operator allowance is not published; do not assume a figure.

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; each fast seller's depot cover ≥ lead time + 2 days before a purchase; no stock bought after its sell-through can no longer reach day 365 (M6); stock and marketing within 85% of deployable cash; spend only within the operator allowance.
