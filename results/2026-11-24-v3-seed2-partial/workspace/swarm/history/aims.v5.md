# Aims v5 (designer, aim update after S-002, written day 59)

For the next point: days 57-63 (point 9). S-002's stretch aims are carried forward unchanged; none is lowered. Point 8 (days 50-56) missed them. Previous version: history/aims.v4.md. Record: audits/AS-002.md.

Constraint: **stock reaching the machines** (slots selling). Point 8: 5 selling at day 56, 9 stocked at day 58 (of 72). Worker time is not the limit: median 250 of 480 min used. Capital is not the limit: about 7% in use. R-P-002 (depot covers two points' refills) is in force; its prediction for day 56 was missed. No design change before point 10 (day 70).

| Driver | Now (point 8, days 50-56) | Aim for days 57-63 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| Final cash (top) | 3,010 at day 56 (floor 1,817, aim 3,435 at point 8); 2,921 at day 59 | system floor x1.08 per point; aim x1.19 per point. Falling short triggers nothing | n/a | cash ≥ EUR 120 at every close |
| Slots selling | 5 at day 56; 18 at day 59 | **24 selling** (carried from S-002) | refills 270 first claim, then remaining minutes | a fill goes only to a slot whose product adds sales (no duplicate product at a location) |
| Stocked at day end | 9 at day 58 | **30 stocked** (carried from S-002) | refills | as above |
| Revenue per slot | 2.4 at day 56; 7-period average 8.9 (charts); own best 11.34 | **at or above 11.3** (carried from S-002) | shares slot and price work | units per location-day must not fall after a price rise |
| Unit cost paid | 1.387 at day 56 (flat, not falling) | **at the lowest offer seen at the order quantity, on every order** (carried from S-002; falls about x0.95 per point) | supplier work 135 min/day | buy only what sells through in about two points |
| Capital (depot) | 7% in use | depot holds stock for every empty priced slot plus the next two points' refills (R-P-002) | inside supplier work | cash ≥ EUR 120 after every purchase |
| Marketing | none | hold; no campaign | marketing 0 | fatigue in get_marketing_report is a stop |

## Worker time split (per working day, 480 minutes)

| Use | Minutes | Share |
| --- | --- | --- |
| Refills (restock_machine, 45 each) | 270 first claim, then any remaining minutes | 56% + |
| Supplier work (check_offers, order_goods) | 135 | 28% |
| Pricing (set_price) | 30 | 6% |
| Reads (get_status, get_machine_inventory, get_sales_report) | 30 | 6% |
| Slack (delays, failures) | 15 | 3% |
| Marketing | 0 | 0% |

Notes:
- The split is the plan, not the use. Use it: the median is 250 of 480.
- Daily sequence (operator rule v3): read status → list empty priced slots and read depot stock → order any missing product (two suppliers, then the lowest offer), within cash after purchase ≥ EUR 120 → refill → keep refilling while minutes remain → price the one product changed this point.
- A refill with no depot stock: do not end the day; order that product, refill later, log it in progress.md.
- Order each line from the supplier whose delivery lands before the refill day. Buy Mon-Thu (weekend sales are low).
- Revert check at day 63 (R-P-002 section 5): if cash falls below EUR 120 at any close, or slots selling is still at or below its centre (12.2), the Strategist and the diagnostician are brought forward; do not revert on your own.
- One price lever per product per point. Read the sales report before the next change.
- Stop buying stock that cannot sell before day 365 after day 335.

Next read: Strategist after point 9 (day 63), or earlier if the top measure is 3 points below the floor line.
