# Aims (AS-002, day 47; replaces the day-24 aims, kept in history/aims.v2.md)

Constraint: worker time is far below its limit (charts.md, day 48: 315 of 480 min used, median 100 over the last 7 days, 1 day unused). Depot stock is the gate on refills: 8 of 72 slots stocked at day end. Capital is idle (2,513 of 2,572 not in use), so money is not the gate.

Stretch aims for point 7 (day 49)
1. slots_selling ≥ 30 of 72 holding stock and priced (latest 8). The M1 line of 48 stands.
2. revenue_per_slot ≥ 9.9 (spec definition: revenue ÷ slots_selling; latest 8.44), with no sale below unit cost.
3. unit_cost_paid_30d celeration ≤ x0.97 a point (latest 1.092, rising).

Top measure: final cash. Cash on hand 2,620.54 (day 48) is read against the floor and aim lines in charts.md. No separate aim here.

Capacity split (480 min a day, spec worker-time measure, by call type)

| Driver | Min a day | Share | Covers |
| --- | --- | --- | --- |
| slots_selling | 288 | 60% | refills at 45 min each (about 6 a day); depot stock checked before each |
| revenue_per_slot | 72 | 15% | price calls; sales-report reads |
| unit_cost_paid_30d | 72 | 15% | check_offers and orders, once a week before the first refill |
| reserve | 48 | 10% | unplanned calls; never used to exceed 480 |
| campaigns | 0 | 0% | none before M3 |

Reads (get_status, get_machine_inventory, depot read) are charged to the driver they serve, not to the reserve. Log each call's clock minutes in swarm/log/minutes.jsonl.

Stock hold (spec v3, depot cover): depot cover = depot units ÷ units sold in the last 7 days. Hold 7–10 days of cover, from a check_offers quote valid on the day of the order. Order when cover falls below the supplier's lead time plus 2 days (lead time 2–7 days). Cover above 14 days is idle capital: do not order more.

Guardrails (from the spec, unchanged)
- Cash ≥ EUR 120 every day.
- No sale below unit cost; margin ≥ 0 on every selling slot.
- Never past 480 min a day; do not start a refill with under 45 min left.
- No price experiments. No campaign spend before M3.
