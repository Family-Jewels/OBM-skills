# Aims (AS-004, day 94; replaces the AS-003 aims, kept in history/aims.v4.md)

Constraint: depot stock, not worker time (S-004, day 84). Worker time is not the gate; stock is. Slots are empty because refills are not reliably made from a current supply quote. Money is not the gate.

S-004 set these for point 13 (days 85–91), which ended before this update (day 94). Carried unchanged as the working aims for point 14 (days 92–98) until the next Strategist redirect.

Stretch aims for points 13–14
1. slots_selling ≥ 16 of 72 (7-day average). Past own best 14.57.
2. depot cover 7–10 days, from a same-day check_offers quote from a live supplier. Cover is not yet in charts.md (instrumentation needed, spec v3).
3. revenue_per_slot ≥ 10.0 (7-day average, about 5% under own best 10.57), with no sale below unit cost.

Top measure: cash holds the floor at point 13: ≥ 3,161 (charts.md floor 3,157.75). Celeration at or above x1.08. The aim line (8,352) is not reachable this point; expect a miss and do not chase it.

Capacity split (480 min a day, spec worker-time measure, by driver; target median used ≥ 200 min a day)

| Driver | Min a day | Share | Covers |
| --- | --- | --- | --- |
| depot cover (incl. unit_cost_paid_30d) | 192 | 40% | check_offers, orders, receipts, depot reads |
| slots_selling | 192 | 40% | refills; depot cover checked before each |
| revenue_per_slot | 48 | 10% | price calls; sales-report reads |
| reserve | 48 | 10% | unplanned calls; never used to exceed 480 |
| campaigns | 0 | 0% | none before M3 |

Charge each call its clock minutes to the driver it serves; log in swarm/log/minutes.jsonl.

Stock hold (spec v3, depot cover): hold 7–10 days of cover, from a check_offers quote valid on the day of the order. Order when cover falls below supplier lead time + 2 days (lead time 2–7 days). Cover above 14 days is idle capital: do not order more.

Pending design change (not in force until adopted): a refill waits for a delivered receipt that confirms stock, against a same-day quote from a live supplier; a replacement supplier is named if the current one is closed. Until the redesign is adopted, the spec v3 rule above applies.

Guardrails (from the spec, unchanged)
- Cash ≥ EUR 120 every day.
- No sale below unit cost; margin ≥ 0 on every selling slot.
- Never past 480 min a day; do not start a refill with under 45 min left.
- No price experiments. No campaign spend before M3.
