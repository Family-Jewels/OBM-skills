# Aims (AS-002, from redirect S-002; replaces AS-001, kept in history/aims.AS-001.md)

As of day 41 (after S-002). Aims are for point 6 (days 36-42) and carry into point 7 until the next redirect.

Constraint: worker time. Restocking took 85% of the last point's 480 minutes, and a restock fills a slot only with depot stock. Nothing has refilled the depot since day 23, so restocks run against empty shelves. Cash is a symptom.

| Driver | Now (point 5) | Aim (point 6) | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 11 (latest) | 24 or more at point end | restocking 40% | cash at or above 120 every period |
| unit_cost_paid_30d | 0.97 | 0.93 or lower | sourcing 25% | slots_selling not falling to buy cheaper |
| revenue_per_slot | 5.22 (7-period average) | 8.14 or more, 7-period average | pricing 10% | units and cash reserve |

Reading (10%) supports all three: it is the depot read before each restock loop.

Each period:
- Read get_storage_inventory before each restock loop. Restock only products the depot read shows in stock. A product with no stock on hand is not restocked.
- order_goods 3 or more times per point, each after check_offers with 2 or more quotes, within the reserve.
- One price test per location, then apply the winner (pricing share).
- Keep the actual split near the shares below. Reading and sourcing stay short.

The top-measure floor and aim lines are set by the system in charts.md and are not changed here. Split alone does not reach them (S-002): the three aims together roughly double revenue, and the restock rule in the operator brief must change (designer request, see audits/AS-002.md).

## Capacity split
- 40% restocking: restock_machine
- 25% sourcing: check_offers, order_goods, search_web
- 10% pricing: set_price
- 10% reading: get_storage_inventory, get_status, get_machine_inventory, get_sales_report
- 5% re-slotting: swap_item
- 10% buffer: none
