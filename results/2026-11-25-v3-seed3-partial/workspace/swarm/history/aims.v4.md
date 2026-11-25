# Aims (AS-003, day 67; replaces the AS-002 aims, kept in history/aims.v3.md)

Constraint: worker time (S-003, day 63). Median 205 of 480 min a day used; 275 min idle. But idle time is not the gap alone: 11 of 72 slots are selling, and 3,310 capital sits idle. Depot stock and ordering gate refills. Money is not the gate.

Applies from day 67 to the end of point 10 (day 70). Point 11 aims come from the next Strategist redirect.

Stretch aims for point 10
1. slots_selling ≥ 24 of 72 holding stock and priced (7-day average of the daily slots_selling). Above the upper limit of 22.49.
2. revenue_per_slot ≥ 11.0 (basis: 7-day average of the daily revenue_per_slot, not a single day; the daily reading is noisy), with no sale below unit cost. Own best 9.95, plus about 10%.
3. unit_cost_paid_30d celeration ≤ x0.97 a point, read once 3 points are in phase (point 12). Until then, no rise in the level.

Top measure: cash at point 10 ≥ 5,036 (aim line 4,268 × 1.18). Floor 2,516 (charts.md). No separate aim.

Capacity split (480 min a day, spec worker-time measure, by call type)

| Driver | Min a day | Share | Covers |
| --- | --- | --- | --- |
| slots_selling | 288 | 60% | refills, charged at each call's clock minutes (spec v3); about 6 refills a day at the 45-min planning figure; depot stock checked before each |
| revenue_per_slot | 72 | 15% | price calls; sales-report reads |
| unit_cost_paid_30d | 72 | 15% | check_offers and orders, once a week before the first refill |
| reserve | 48 | 10% | unplanned calls; never used to exceed 480 |
| campaigns | 0 | 0% | none before M3 |

Target: median worker time used at least 400 min a day across point 10. Reads (get_status, get_machine_inventory, depot read) are charged to the driver they serve. Log each call's clock minutes in swarm/log/minutes.jsonl.

Stock hold (spec v3, depot cover): depot cover = depot units ÷ units sold in the last 7 days. Hold 7–10 days of cover, from a check_offers quote valid on the day of the order. Order when cover falls below the supplier's lead time plus 2 days (lead time 2–7 days). Cover above 14 days is idle capital: do not order more.

Pending: the daily refill quota asked for in S-003 changes how the work is done, so it is not in this file. It goes to a design change (see audits/AS-003.md).

Guardrails (from the spec, unchanged)
- Cash ≥ EUR 120 every day.
- No sale below unit cost; margin ≥ 0 on every selling slot.
- Never past 480 min a day; do not start a refill with under 45 min left.
- No price experiments. No campaign spend before M3.
