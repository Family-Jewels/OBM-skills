As of day 0, design (before point 1). Written by the designer; no Strategist redirect yet (first Strategist: after point 3, day 21).

Constraint: **worker time** (480 min/day; refills at 45 min, about 10 per day at most) for slots_selling. Cash (EUR 1,500, reserve EUR 120) binds first in days 0–2; time binds once stock covers the selling slots.

| Driver | Now | Aim for point 1 (day 7) | Share of worker time | Guardrail |
| --- | --- | --- | --- | --- |
| Top: final bank balance (exemplar path) | EUR 1,500 | Cash at day 30 at or above EUR 3,228 (exemplar), the stretch; the system's overshoot aim line is in charts.md | all drivers | cash ≥ EUR 120 at every close |
| 2a. slots_selling | 0 | At least 12 slots selling, at least 2 in each of the six machines | 270 min refills (about 6 refills) per day; days 0–1 may use up to 9 refills a day for initial stocking | refills ≤ 300 min/day after day 2 |
| 2b. revenue_per_slot | unknown | Baseline only: units per product per location read from get_sales_report by day 7; no aim until then | 40 min pricing (set_price) | price ≥ unit cost × 1.2 |
| 3. Unit cost paid | unknown | Quotes from at least 2 suppliers by day 7; each order at the lowest checked quote | 40 min purchasing (check_offers, order_goods), once per point | never buy beyond what sells; cash ≥ EUR 120 after order |
| 4. Fixed and discretionary costs | EUR 12/day fixed | Zero unpaid spot-fee days; no marketing until point 3 | 10 min marketing | fee paid daily; marketing payback ≤ 30 days |
| 5. Worker time on drivers | 0% | 90% of the 480 min on drivers 2a–3 (see split) | Split below | total ≤ 480 min |

## How the worker's 480 minutes are split (planning split; M1 replaces the assumed call costs with measured ones)

| Activity | Minutes/day | Note |
| --- | --- | --- |
| Refill (driver 2a) | 270 | about 6 refills; 45 min each |
| Swap (driver 2b-i, product mix) | 30 | at most 1 per day; 30 min each |
| Pricing (driver 2b-ii) | 40 | set_price calls, assumed about 5 min each |
| Purchasing (driver 3) | 40 | check_offers and order_goods, once per point (the day of the point boundary) |
| Status and sales reads (learning) | 40 | get_status, get_machine_inventory, get_sales_report |
| Marketing (driver 4) | 10 | only where the rule allows; none before point 3 |
| Buffer (delays, outages, deliveries) | 50 | keep unused; not for extra refills |
| **Total** | **480** | |

## Notes: what to do first each period
1. Day open (09:00): read status and inventory; list selling slots that are empty or near empty.
2. Refill in this order: sold-out selling slots in the best-selling products first, then slots sold out yesterday, then empty slots that had demand.
3. Price every new product at or above unit cost × 1.2. Read the sales report at each point boundary; do not run deliberate price experiments.
4. At each point boundary (days 0, 7, 14, …): check_offers at ≥ 2 suppliers for the same product list, then order only at the lowest quote and within the cash guardrail.
5. Do not add a product or slot for demand that has not been read; no marketing until the demand read exists.
6. Keep the unused buffer; it is not for extra refills.
