# Aims v3 (designer, aim update after S-001, day 24)

As of point 3 (after S-001). For the next point: days 22-28 (point 4). Previous version: history/aims.v2.md.

Constraint: **stock reaching the machines** (slots selling). Not worker time: median 325 of 480 min used, 155 idle (charts). 62 of 72 slots unstocked at day end; capital 11% in use.

| Driver | Now | Aim for days 22-28 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| Final cash (top) | 1,486 at day 24 (charts) | system floor x1.08 per point (about 1,316 at day 28); aim x1.17 (about 1,426), an overshoot that triggers nothing if missed | n/a | cash ≥ EUR 120 at every close |
| Slots selling | 13 selling (latest point); 10 stocked at day end (median) | **20 selling** | refills 270 min/day | a fill goes only to a slot whose product adds sales (no duplicate product at a location) |
| Revenue per slot | 17.6 latest; own best 9.4 (S-001) | at or above 9.4 | shares slot and price work | units per location-day must not fall after a price rise |
| Units per slot | units 87 latest | no stock-outs in high-yield slots | refills | price ≥ unit cost paid |
| Realised price | set from unit cost | change one product's price per point; read the response | pricing 30 min/day | price ≥ `unit_cost_paid_30d` for that product |
| Unit cost paid | 1.159 at day 17 (rising, wrong way) | **falls about x0.95 per point**, to at or below the lowest of ≥2 offers at the order quantity | supplier work 90 min/day | buy only what sells through in about 2 points |
| Footfall reach (marketing) | none | hold; no campaign | marketing 0 | fatigue in get_marketing_report is a stop |
| Capital idle | 11% in use | depot holds the next day's planned refills (six slots' worth), not more | inside supplier work | cash ≥ EUR 120 after every purchase |

## Worker time split (per working day, 480 minutes)

| Use | Minutes | Share |
| --- | --- | --- |
| Refills (restock_machine, 45 each: 6 trips) | 270 | 56% |
| Supplier work (check_offers, order_goods) | 90 | 19% |
| Pricing (set_price) | 30 | 6% |
| Reads (get_status, get_machine_inventory, get_sales_report) | 30 | 6% |
| Slack (delays, failures, and any swap_item at 30 each) | 60 | 12% |
| Marketing | 0 | 0% |

Notes:
- Daily sequence: read status (cash, reserve) → read depot stock → order (check_offers from two suppliers, then the lowest offer) for the next day's planned refills, within cash after purchase ≥ EUR 120 → refill empty slots whose product sold through last point first, then the slots that sold most per refill → price the one product changed this point.
- A refill trip with no depot stock for its product: skip it, log it in progress.md, and make the next order cover it.
- Swaps are not in the plan. Use slack for one only when a slot's product adds no sales.
- One price lever per product per point. Read the sales report before the next change.
- Stop buying stock that cannot sell before day 365 after day 335.
- The split is the operator's plan. The system reads actual minutes from the clock; the Strategist changes it at the next redirect if the constraint moves.

Next read: Strategist after point 6 (day 42), or earlier if the top measure is 3 points below the floor line.
