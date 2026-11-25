# Aims (version 1, designer's initial set; the first Strategist redirect replaces it)

As of day 0 (before the first point)   Constraint: worker time (480 min per working day; a restock is 45 min, a swap 30 min)

| Driver | Now | Aim for the next point (day 7) | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | read at day 0 from get_machine_inventory | ≥ 36 and rising every point, with stretch toward 72 | ~60% (refill trips) | cash ≥ €120 every day |
| revenue per refill trip (units per trip × price) | not yet measured | highest available: chosen rows and products | inside the refill share | price ≥ unit cost |
| revenue_per_slot | read at day 0 | above day-0 level | ~5% (price setting) | margin ≥ 0 per unit |
| unit_cost_paid_30d | read at first order | not above its first value | ~10% (check_offers and orders) | availability held |
| Reads, reports, admin | — | minimal | ~10% (get_status, sales report, inventory) | — |
| Marketing | — | none until day 14; then moderate | ~5% after day 14 | fatigue; limits |

Total: 60 + 5 + 10 + 10 + 5 = 90%. The remaining ~10% is held for swaps (30 min each) and slack.

Notes, what to do first each period, in the spec's terms:
- Each working day: get_status and get_machine_inventory first, record the clock. Then fill empty or unpriced slots in the order of expected units per refill trip.
- Use rows A and B (small products, 18 units per fill) for fast sellers; rows C and D (large, 10 units) for the rest.
- Before every order, check_offers at the planned quantity. Never let committed purchases take cash below €120.
- Never set a price below unit cost. Learn price response from the sales report; do not run price tests.
- Do not buy stock that cannot sell before day 365.
- Measure at milestone 1: does one restock fill one slot or a whole machine? Record the result in log/progress.md.
