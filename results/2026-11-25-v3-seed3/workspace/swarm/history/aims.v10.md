# Aims (version 10, after S-009 at day 196; written day 206, point 30; previous version in history/aims.v9.md)

Constraint: supply to the slots: depot stock for the fast sellers, and the refill trips that land it. Worker time is the cheapest opening, but the charts show 0 of 480 min median used over the last 7 days (5 days unused), against 75 read in S-009. Until the operator's day runs, no split below is spent. See audits/AS-009.md.

Aims from S-009, for point 30 (days 204–210), 7-period averages. S-009's own window (point 29, days 197–203) closed before this update; its aims carry to point 30, the next point. The floor and aim lines are the system's: read them on charts.md, not here.

| Driver | Last reading (charts.md) | Stretch aim, point 30 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | latest 3; chart centre 7.85; own best 20 | ≥ 12 (ceiling 72); first claim on the minutes | refills into slots with depot stock: 270 (56%), six 45-min trips | cash ≥ €120 every day; refill only into slots with depot stock; check storage before each refill |
| units (chart total daily units) | latest 4; chart centre 21.75; own best 80.86 | ≥ 35, availability held | from the refill rows | availability held |
| revenue_per_slot | latest 2.9; chart centre 5.49; own best 8.51 | ≥ 7.4 | price setting and sales-report reads: 60 (12.5%) | price ≥ unit cost |
| cash (top measure) | 9,756.07 (latest in charts.md); floor line 11,415.19 at point 29 | on or above the floor line; the aim is not expected to be met | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | watched, not pushed | availability held | check_offers and orders: 90 (19%) | check_offers at all suppliers before every order; each fast seller's depot cover ≥ lead time + 2 days before a purchase |

Note on the units aim: the S-008 and S-009 label says "units per slot-day", but the figures are the chart's total daily units. The aim is applied to that row. Strategist to confirm the label.

Capacity split (480 min a day, per S-009):
- Refills into slots with depot stock: 270 (56%), six 45-min trips. First claim: slots_selling.
- check_offers and orders: 90 (19%), sized to depot cover at lead time + 2 days.
- Price setting and sales-report reads: 60 (12.5%), revenue_per_slot.
- Core-day reads and admin: 60 (12.5%). Core reads (get_status, get_machine_inventory, clock) come first.
- Marketing: 0.

Notes, in the spec's terms:
- Each working day: core reads first, then check each fast seller's depot stock before its refill. If the depot is empty for a line, log the short and do not refill that line.
- Write the DEPOT line every working day (spec 2a). Depot cover is not yet charted (spec open question 8); the DEPOT line is the only depot record.
- Before every order, check_offers at the planned quantity at all known suppliers. Size each fast seller to lead time + 2 days, within the €120 reserve and 85% of deployable cash.
- The operator allowance is not published; do not assume a figure.

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; each fast seller's depot cover ≥ lead time + 2 days before a purchase; stock and marketing within 85% of deployable cash; spend only within the operator allowance.
