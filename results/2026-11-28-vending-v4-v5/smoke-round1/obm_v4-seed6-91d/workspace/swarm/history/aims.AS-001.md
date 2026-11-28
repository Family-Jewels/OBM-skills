# Aims (AS-001, from redirect S-001; replaces the day-0 aims, kept in history/aims.day0.md)

Constraint: worker time. Restocking takes 88% of the day's 480 minutes, and a restock fills no slot without depot stock. Only sourcing refills the depot. Cash (reserve 120) and idle capital are symptoms, not the limit.

Aims for the next point (point 5):

| Driver | Aim | Condition |
| --- | --- | --- |
| slots_selling | 22 or more (own best: 22, day 18) | restock only products with stock on hand |
| unit_cost_paid_30d | 0.93 or lower (own best: 0.93) | 2 or more check_offers quotes per order |
| revenue_per_slot | 7.4 or more, averaged over the point (own best: 7.42) | one price test per location, then apply the winner |

Guardrail: cash stays at or above 120 every period. The top-measure lines (floor, aim) are set by the system in charts.md and are not changed here.

Each period:
- Read get_storage_inventory before each restock loop. Restock only products that show stock on hand.
- Place order_goods at least 2 times per point, each after check_offers, within the reserve.
- Keep the actual split near the shares below. Reading and sourcing stay short.

## Capacity split
- 45% restocking: restock_machine
- 25% sourcing: check_offers, order_goods, search_web
- 10% pricing: set_price
- 10% reading: get_storage_inventory, get_status, get_machine_inventory, get_sales_report
- 5% re-slotting: swap_item
- 5% buffer: none
