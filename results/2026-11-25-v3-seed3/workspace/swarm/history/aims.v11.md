# Aims (version 11; after S-010 at day 231, point 33; written day 243, point 35; previous version in history/aims.v10.md)

Constraint: the worker's own time. The charts show 0 of 480 min median used over the last 7 days (5 days unused). Behind it: slot stock (1 of 72 stocked) and depot cover, which is not yet charted. The split below is not yet run. See audits/AS-010.md.

Aims from S-010, for point 36 (days 246–252), the next point. S-010's window (point 34, days 232–238) closed before this update; its levels carry unchanged. 7-period averages. The floor and aim lines are the system's: read them on charts.md, not here.

| Driver | Last reading (charts.md) | Stretch aim, point 36 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 7-period 2.71; chart centre 3.3 (since day 209); own best 20 | ≥ 8 (ceiling 72); first claim on the minutes | refills into slots with depot stock: 270 (56%), six 45-min trips | cash ≥ €120 every day; refill only into slots with depot stock |
| units (chart total daily units) | 7-period 8.71; chart centre 2.15 (since day 221); own best 80.86 | ≥ 20, availability held | from the refill rows | availability held |
| revenue_per_slot | 7-period 4.36; chart centre 5.49 (since day 183); own best 8.51 | ≥ 7.4 | price setting and sales-report reads: 60 (12.5%) | price ≥ unit cost |
| cash (top measure) | 9,576.17 at point 35; floor line 17,691.40; aim line 122,438 | on or above the floor line; not expected to be met this point | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | watched, not pushed | availability held | check_offers and orders: 90 (19%) | check_offers at all suppliers before every order; each fast seller's depot cover ≥ lead time + 2 days before a purchase |

Note on the units aim: the label says "units per slot-day", but the figures are the chart's total daily units. The aim is applied to that row. Strategist to confirm the label.

Capacity split (480 min a day, per S-010; shares unchanged):
- Refills into slots with depot stock: 270 (56%), six 45-min trips. First claim: slots_selling.
- check_offers and orders: 90 (19%), sized to depot cover at lead time + 2 days.
- Price setting and sales-report reads: 60 (12.5%), revenue_per_slot.
- Core-day reads and admin: 60 (12.5%). Core reads (get_status, get_machine_inventory, clock) come first.
- Marketing: 0.

Notes, in the spec's terms:
- Each working day: core reads first, then check each fast seller's depot stock before its refill. If the depot is empty for a line, log the short and do not refill that line.
- Write the DEPOT line every working day (spec 2a). It is the only depot record until depot cover is charted (spec open question 8).
- Before every order, check_offers at the planned quantity at all known suppliers. Size each fast seller to lead time + 2 days, within the €120 reserve and 85% of deployable cash.
- The operator allowance is not published; do not assume a figure.

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; each fast seller's depot cover ≥ lead time + 2 days before a purchase; stock and marketing within 85% of deployable cash; spend only within the operator allowance.
