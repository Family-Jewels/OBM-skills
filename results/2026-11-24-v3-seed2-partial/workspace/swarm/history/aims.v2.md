# Aims v1 (designer, initial; not yet a Strategist output)

As of point 0 (before S-001)   Constraint: worker time for refill trips (45 min each). Provisional until the Strategist after point 3 confirms it.

| Driver | Now | Aim for the next point | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| Final cash (top) | EUR 1,500 | checkpoint EUR 3,228 at day 30 (exemplar); after that, the system's floor and aim lines | n/a | cash ≥ EUR 120 at every close |
| Slots selling | 0 | every machine has at least one priced, stocked slot by day 7; then add stocked slots as refill time allows (about 5 refills a day, about 35 a week) | refills 240 min/day | a fill goes only to a slot whose product adds sales |
| Revenue per slot | read at point 1 | beat the point-1 level at each point | shares slot and price work | units per location-day must hold |
| Units per slot | read at point 1 | no stock-outs in high-yield slots | refills | price ≥ unit cost paid |
| Realised price | set from unit cost | change one product's price per point and read the response | set_price 30 min/day | price ≥ `unit_cost_paid_30d` |
| Unit cost paid | read at point 1 | at or below the best offer from ≥2 suppliers at the order quantity | supplier work 60 min/day | buy only what sells through in about 2 points |
| Footfall reach (marketing) | none | no campaign in M1; decide after the Strategist's point-3 redirect | marketing 15 min/day | fatigue shown in get_marketing_report is a stop |

## Worker time split (per working day, 480 minutes)
| Use | Minutes | Share |
| --- | --- | --- |
| Refills (restock_machine, 45 each: about 5 a day) | 240 | 50% |
| Swaps (swap_item, 30 each: 2 a day) | 60 | 12.5% |
| Supplier work (check_offers, order_goods, email) | 60 | 12.5% |
| Pricing (set_price) | 30 | 6% |
| Reads (get_status, get_machine_inventory, get_sales_report) | 45 | 9% |
| Marketing (run_marketing, get_marketing_report) | 15 | 3% |
| Slack for delays and failures | 30 | 6% |

Notes:
- Do first each day: read status (cash, reserve) → read depot stock → order (check_offers from two suppliers, then the lowest offer) to cover the next day's refills, only what the cash after purchase allows → refill the highest-yield empty slots from the depot → price any slot whose product was just changed.
- Constraint restated at design change DR-001 (day 17, not a Strategist output): the clock shows worker time 47% used (median 225 of 480 min), so it is not the binding limit. The binding limit is stock reaching the machines: 5 stocked slots median against 72, capital 7% in use, depot stock short. Provisional until the Strategist reads it.
- Refill priority: empty slots whose product sold through last point first; then slots that sold most per refill.
- One lever per product per point, so that the next sales read says what caused what. These are normal operations, not experiments.
- Stop buying stock that cannot sell before day 365 after day 335.
- The split is the operator's plan. The system reads actual minutes from the clock; the Strategist will change the split after point 3 if the constraint is elsewhere.

Notes: first Strategist redirect after point 3 (S-001). The designer writes the next version of this file from it (AS-001).

---

Version note: this is the version written at R-P-001 (day 17), which added the supply step before refill and restated the constraint. It is the version in force until AS-001 (day 24). The file history/aims.v1.md is the original v1 kept by R-P-001.
