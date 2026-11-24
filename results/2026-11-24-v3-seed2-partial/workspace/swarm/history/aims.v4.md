# Aims v4 (designer, aim update after S-002 and redesign R-P-002, day 49)

For the next point: days 50-56 (point 8). S-002's stretch aims for point 7 were not met (6 selling at the latest point; 5 stocked at day end), so they carry forward unchanged; no aim is lowered. Previous version: history/aims.v3.md.

Constraint: **stock reaching the machines** (slots selling). Worker time is idle (median 230 of 480 min used) and capital is idle (about 3% in use) while the depot is short of product: 61 of 72 slots unstocked at day end (D-P-002). Changed here: the depot and order rule, which capped supply at about six slots' worth and let a skipped trip end the day.

| Driver | Now (day 49) | Aim for days 50-56 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| Final cash (top) | 2,627 at day 49 (charts); floor 1,678, aim 2,898 | system floor x1.08 per point; aim x1.19 per point. Falling short triggers nothing | n/a | cash ≥ EUR 120 at every close |
| Slots selling | 6 selling | **24 selling** (carried from S-002) | refills 270 first claim, then remaining minutes | a fill goes only to a slot whose product adds sales (no duplicate product at a location) |
| Stocked at day end | 5 | **30 stocked** (carried from S-002) | refills | as above |
| Revenue per slot | 11.1 latest; own best 11.34 | **at or above 11.3** (carried from S-002) | shares slot and price work | units per location-day must not fall after a price rise |
| Units per slot | units 9 latest (charts); 7-period average 35.7 | no stock-outs in high-yield slots | refills | price ≥ unit cost paid |
| Realised price | set from unit cost | change one product's price per point; read the response | pricing 30 min/day | price ≥ `unit_cost_paid_30d` for that product |
| Unit cost paid | rising (x1.05 per point) | **at the lowest offer seen at the order quantity, on every order** (carried from S-002; falls about x0.95 per point) | supplier work 135 min/day | buy only what sells through in about two points |
| Footfall reach (marketing) | none | hold; no campaign | marketing 0 | fatigue in get_marketing_report is a stop |
| Capital (depot) | 3% in use | **depot holds stock for every empty priced slot plus the next two points' refills** (replaces "next day's six slots' worth") | inside supplier work | cash ≥ EUR 120 after every purchase |

## Worker time split (per working day, 480 minutes)

| Use | Minutes | Share |
| --- | --- | --- |
| Refills (restock_machine, 45 each) | 270 first claim, then any remaining minutes | 56% + |
| Supplier work (check_offers, order_goods) | 135 | 28% |
| Pricing (set_price) | 30 | 6% |
| Reads (get_status, get_machine_inventory, get_sales_report) | 30 | 6% |
| Slack (delays, failures, and any swap_item at 30 each) | 15 | 3% |
| Marketing | 0 | 0% |

Notes:
- Daily sequence: read status (cash, reserve) → list empty priced slots and read depot stock → order any missing product (check_offers from two suppliers, then the lowest offer), within cash after purchase ≥ EUR 120 → refill empty slots whose product sold through last point first → keep refilling while minutes remain → price the one product changed this point.
- A refill trip with no depot stock: do not end the day; order that product and refill later; log it in progress.md.
- Swaps are not in the plan. Use slack for one only when a slot's product adds no sales.
- One price lever per product per point. Read the sales report before the next change.
- Stop buying stock that cannot sell before day 365 after day 335.
- The split is the operator's plan. The system reads actual minutes from the clock; the Strategist changes it at the next redirect if the constraint moves.

Next read: Strategist after point 9 (day 63), or earlier if the top measure is 3 points below the floor line or slots selling is not above its centre by point 9.
