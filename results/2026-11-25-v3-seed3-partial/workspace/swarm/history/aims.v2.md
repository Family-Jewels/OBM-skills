As of day 24 (after S-001)   Constraint: worker time (median 370 of 480 min a day over the last 7 days, latest 450), with depot stock as the gate on refills. Reads take about 130 min a day of that time.

| Driver | Now | Aim for the next point (day 28) | Share of capacity (min a day) | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 20 of 72 (day 24) | ≥ 48 of 72 holding stock and priced | 66% (315: 7 refills of 45) | no slot selling below unit cost |
| revenue_per_slot | 13.85 latest; own best 9.86 | ≥ 9.9 | 6% (30: price calls) | price floor per product |
| unit_cost_paid_30d | rising (x1.01) | falls each point (celeration below x1.00) | 6% (30: check_offers, orders) | margin ≥ 0 per unit |
| reads (enabling, not a driver) | about 130 min a day | ≤ 60 min a day: get_status 5, get_machine_inventory 25, get_storage_inventory 25; email and payments only when needed | 12% (60) | none |
| reserve | n/a | 45 min for unplanned calls | 9% (45) | never past 480 min a day |
| campaigns | none | none | 0% | no spend before M3 |

Top measure: cash EUR 1,789 at day 24 is already above the day-28 aim line (about 1,713). Keep the EUR 120 reserve.

Notes:
1. Each day: get_status and get_machine_inventory once each; read the depot once before the first refill.
2. Refill empty slots first, then partly stocked ones, 7 refills a day when depot stock allows. Before each refill, check depot stock for that product; if it is short, pick another product and log the shortfall.
3. Hold depot stock ahead of the refill cycle: check_offers, then order, once a week before the first refill.
4. Log each call's minutes in swarm/log/minutes.jsonl; reconcile to the clock at day end.
5. Do not start a refill with under 45 min left. No price experiments. No campaigns.
