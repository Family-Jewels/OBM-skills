# Aims v6 (designer, aim update after S-003, day 75, point 11)

For the next point: days 71-77 (point 11). S-003's stretch aims are set out below; none is lowered. Point 10 (days 64-70) missed slots selling, stocked and revenue per slot. Previous version: history/aims.v5.md. Record: audits/AS-003.md.

Constraint: **stock reaching the machines** (slots selling, stocked at day end). Worker time is not the limit: median 50 of 480 min used over the last 7 days (latest 25). Capital is not the limit: about 6% in use (cash 3,887 at day 75). The work as it is now cannot reach these aims (AS-003 section 4); a design change is needed and is queued behind the diagnosis. Until it is adopted, the work follows rules/operator.md v3.

| Driver | Now (day 75, charts) | Aim for days 71-77 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| Final cash (top) | 3,887 at day 75. Point 11 lines: floor 2,303 (x1.08 on 2,132); aim 5,745 (x1.19 on 4,828) | system floor x1.08 per point; aim x1.19 per point. Falling short triggers nothing | n/a | cash ≥ EUR 120 at every close |
| Slots selling | 4 on day 75; 7-period average 10.6 | **20 selling** | refills 270 first claim, then remaining minutes | a fill goes only to a slot whose product adds sales (no duplicate product at a location) |
| Stocked at day end | 2 on day 75; 12 at day 70 | **24 stocked** | refills | as above |
| Revenue per slot | 10.0 (7-period latest) | **at or above 11.3** (own best 11.66, carried) | shares slot and price work | units per location-day must not fall after a price rise |
| Unit cost paid | collecting; not judgeable from the charts | at the lowest offer seen at the order quantity, on every order (carried) | supplier work 135 min/day | buy only what sells through in about two points |
| Capital (depot) | about 6% in use | depot holds stock for every empty priced slot plus the next two points' refills | inside supplier work | cash ≥ EUR 120 after every purchase |
| Marketing | none | hold | marketing 0 | fatigue in get_marketing_report is a stop |

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
- The split is the plan, not the use. Use it. Minutes now go unused because there is nothing in the depot to load; the fix is supply, not more minutes.
- Supplier lead times (progress.md, day 1): zuidas 4 days, kanaal-cash-carry 4-6 days, bakker-en-zoon 8-10 days. Order each line so it lands before the slot runs out, not after.
- Daily sequence (operator rule v3, unchanged): read status → list empty priced slots and read depot stock → order any missing product (two suppliers, then the lowest offer), within cash after purchase ≥ EUR 120 → refill → keep refilling while minutes remain → price the one product changed this point.
- A refill with no depot stock: do not end the day; order that product, refill later, log it in progress.md.
- Buy Mon-Thu (weekend sales are low). Stop buying stock that cannot sell before day 365 after day 335.
- One price lever per product per point. Read the sales report before the next change.
- Revert check (R-P-002 section 5) fired at day 63: slots selling at or below its centre. Not reverted by the designer; see AS-003.

Next read: Strategist after point 12 (day 84), or earlier if the top measure is 3 points below the floor line.
