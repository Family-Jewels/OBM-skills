As of day 0 (before S-001)   Constraint: worker time (480 min per working day) and starting cash (EUR 1,500) together; the first refills cost both.

| Driver | Now | Aim for the next point (days 0–7) | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 0 of 72 | ≥ 36 of 72 priced and holding stock by day 7, as cash allows | 55% of worker minutes (refills and swaps) | no slot selling below unit cost |
| revenue_per_slot | unknown | read from pulse 1; aim set then | 15% (price changes, reads) | price floor per product |
| unit_cost_paid_30d | unknown | the lowest quote for each product at the quantity ordered, every week | 15% (check_offers, orders) | margin ≥ 0 per unit |
| worker time | 0 used | 480 min per day; no day over 480 | 10% reserve for unplanned calls | never past 480 |
| cash | EUR 1,500 | never below EUR 120 on any day | n/a | reserve EUR 120 |
| campaigns | none | none (not until M3) | 0% | no spend |

Notes: first each day, read status and inventory (cheap), then priced refills of the highest-margin products in the slots with the most demand, then one order per product at the best weekly quote. Keep the depot-to-slot cycle under one stock-out. Record every order's quote, receipt and cash change. Do not run price experiments.
