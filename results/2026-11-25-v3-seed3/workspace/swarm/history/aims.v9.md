# Aims (version 9, after S-008 at day 168; written day 174, point 25; previous version in history/aims.v8.md)

Constraint: supply to slots: depot stock reaching the slots, and refill trips that land it. Worker time is not the binding link: the chart shows 16% used (median 75 of 480 min, 405 idle). S-008 read it as zero use; see audits/AS-008.md.

Aims from S-008, for point 25 (days 169–175), 7-period averages. Point 25 closes at day 175; these carry unchanged into point 26 (days 176–182) until the next strategy (S-009, point 27). The floor and aim lines are the system's: read them on charts.md, not here.

| Driver | Last reading | Stretch aim, point 25 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | latest 10 (day 176); chart centre 14.3; own best 20 | ≥ 16 (ceiling 72); first claim on the minutes | refills into slots with depot stock: 225 (47%), five 45-min trips | cash ≥ €120 every day; refill only into slots with depot stock; check storage before each refill |
| units (daily, all slots) | latest 14 (day 176); chart centre 53.9 | ≥ 50, availability held | from the refill rows | availability held |
| revenue_per_slot | latest 2.49; chart centre 7.39 | ≥ 7.4 | price setting and sales-report reads: 60 (12.5%) | price ≥ unit cost |
| cash (top measure) | 9,075.57 (day 176) | on or above the floor line (charts.md); the aim is not expected to be met | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | 0.916 (day 176) | watched, not pushed; availability held | check_offers and orders: 90 (19%) | check_offers at all suppliers before every order; each fast seller's depot cover ≥ lead time + 2 days before a purchase |

Note on the units aim: S-008 labels it "units per slot-day", but its figures (chart centre 53.9) are the chart's total daily units. The aim is applied to that row. Strategist to confirm the label.

Capacity split (480 min a day, per S-008):
- Refills into slots with depot stock: 225 (47%), five 45-min trips. First claim: slots_selling.
- check_offers and orders: 90 (19%), sized to depot cover at lead time + 2 days, drawn on idle capital.
- Price setting and sales-report reads: 60 (12.5%), revenue_per_slot.
- Core-day reads and admin: 60 (12.5%). Core reads (get_status, get_machine_inventory, clock) come first.
- Slack, logged: 45 (9%). Marketing: 0.

Notes, in the spec's terms:
- Each working day: core reads first, then check each fast seller's depot stock before its refill. If the depot is empty for a line, log the short and do not refill that line.
- Write the DEPOT line every working day (spec 2a). Until the redesign adds units per refill trip, the DEPOT line is the only depot record.
- Before every order, check_offers at the planned quantity at all known suppliers. Size each fast seller to lead time + 2 days, within the €120 reserve and 85% of deployable cash.
- The operator allowance is not published; do not assume a figure.

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; each fast seller's depot cover ≥ lead time + 2 days before a purchase; stock and marketing within 85% of deployable cash; spend only within the operator allowance.
