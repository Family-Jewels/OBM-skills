As of day 0 (initial design, before any baseline; after no Strategist record yet)   Constraint: worker time for refills (the capacity that turns stock into selling slots); working cash is the second limit in the first weeks. The first pulse (point 1) decides which binds.

| Driver | Now | Aim for the next point | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling (1a1) | baseline at day 1 (to be read from status) | 24 by day 14 (M1 pass); 48 by day 60 (M2); 72 at horizon | 55% of worker minutes (refills) | Cash ≥ €120 every day |
| revenue_per_slot (1a2) | baseline pending (first sales report) | Rising 2 points out of 3 from point 2 | 10% (price and swap) | Margin per unit > 0; no falling units for 2 points |
| unit_cost_paid_30d (1b) | baseline pending (first offers) | Within 5% of the lowest offer seen on each stocked product | 10% (offers and orders) | Never buy below reserve |
| Balance (top measure, read only) | €1,500 | ≥ €3,228 on day 30 (exemplar checkpoint) | — | Cash ≥ €120 every day |
| Marketing (1d) | none | None in M1 and M2; test once per location in M3 | 5% (from M3) | Limits in get_marketing_report |
| Unallocated and audit time | — | Never below 10% of each point | 10% | — |

Notes:
- **First, in the first point:** read status and inventory, check offers for every supplier, stock the highest-value slots first, and set prices above unit cost. Log the minutes each call type takes (price change, status read, refill, swap, order), because the split above is provisional until those numbers exist.
- **Do not** raise slot counts past the cash that restocking can fund; a refill that drops cash under €120 waits.
- **Do not** cut price to raise units unless the revenue per slot check says it pays.
- Aims for points 2 and later are set by the Strategist after point 3 (day 21). Until then the numbers above are the provisional aims.
- Overshoot: the balance floor line runs to €61,219 at day 365; the system computes the overshoot aim line. Falling short of an aim is expected and triggers nothing; the Strategist is brought forward only when the balance is below its floor line 3 points in a row.
