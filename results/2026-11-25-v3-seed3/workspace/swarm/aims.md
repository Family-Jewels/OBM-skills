# Aims (version 13; after S-012 at day 315, point 45; written day 346, point 50; previous version in history/aims.v12.md)

Constraint: the worker's own time, 0 of 480 min median over the last 7 days (7 days unused). Behind it now: depot stock is nearly gone (no order since day 242; about 100 units across six lines at day 307) and demand is 0–5 sales a day in the winter lull. Slot stock 0 of 72 at day end. The split below has not run. See audits/AS-012.md.

Aims from S-012, for point 51 (days 351–357), the next point. Point 50 (days 344–350) is in progress; the S-012 aims for point 46 (days 316–322) have closed and are carried here, not re-run. 7-period averages. The floor and aim lines are the system's: read them on charts.md, not here.

| Driver | Last reading (charts.md, point 49) | Stretch aim, point 51 | Minutes a day | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | latest 0; chart centre 1.25 (since day 323 phase); own best 20 | ≥ 12 (ceiling 72); first claim on the minutes, only into lines with depot stock | refills into slots with depot stock: 270 (56%), six 45-min trips | cash ≥ €120 every day; refill only into lines with depot stock |
| units (chart total daily units) | latest 0; own best 80.86 | ≥ 20, availability held | from the refill rows | availability held |
| revenue_per_slot | latest 0; own best 8.51 | ≥ 8.5 | price setting and sales-report reads: 60 (12.5%) | price ≥ unit cost |
| cash (top measure) | 9,091.57 at point 49 (days 337–343); floor line 49,175.26; aim line 122,438 | on or above the floor line; not expected to be met | from the rows above | cash ≥ €120 every day |
| unit_cost_paid_30d | watched, not pushed | availability held | check_offers and orders: 90 (19%) | check_offers at all suppliers before every order; each fast seller's depot cover ≥ lead time + 2 days before a purchase; no stock bought whose sell-through cannot reach day 365 |

Units aim: applied to the chart's total daily units row (confirmed at AS-011). Label still to be confirmed by the Strategist.

Capacity split (480 min a day, per S-012; shares unchanged):
- Refills into slots with depot stock: 270 (56%), six 45-min trips. First claim: slots_selling.
- check_offers and orders: 90 (19%), sized to depot cover at lead time + 2 days.
- Price setting and sales-report reads: 60 (12.5%), revenue_per_slot.
- Core-day reads and admin: 60 (12.5%). Core reads (get_status, get_machine_inventory, clock) come first.
- Marketing: 0.

Notes, in the spec's terms:
- Each working day: core reads first. Check each fast seller's depot stock and cover. If the depot is short for a line, the order check comes before its refill (see audits/AS-012.md: the order round is the step that can create refill work now; the rule order is a redesign question).
- Before every order, check_offers at the planned quantity at all known suppliers. Size per fast seller in whole cases to sell through to day 365 and cover lead time + 2 days, within the €120 reserve and 85% of deployable cash.
- Write the DEPOT line, the clock time and the refill trip count every working day, and read each refill trip back (slot stock and clock before and after). Depot cover and clock minutes are not yet charted.
- The operator allowance is not published; do not assume a figure.

Guardrails (from the spec): cash ≥ €120 every day; price ≥ unit cost; availability held; each fast seller's depot cover ≥ lead time + 2 days before a purchase; no stock bought after its sell-through can no longer reach day 365 (M6); stock and marketing within 85% of deployable cash; spend only within the operator allowance.
