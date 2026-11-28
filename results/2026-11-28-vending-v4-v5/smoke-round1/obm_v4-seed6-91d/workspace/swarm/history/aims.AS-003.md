# Aims (AS-003, from redirect S-003; replaces AS-002, kept in history/aims.AS-002.md)

As of day 60 (after S-003). Aims are for point 9 (days 57-63) and carry until the next redirect.

Constraint: worker time, spent on restocking. Restocks run against an empty depot, so restocking took 67% of the last point's minutes and bought few slots. Cash is idle (2,892 against a reserve of 120). Sourcing is the step that binds.

| Driver | Now (day 60) | Aim for point 9 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 8.86 (7-period average) | 16 or more, 7-period average; 20 or more at point end | restocking 35% | cash at or above 120 every day |
| revenue_per_slot | 7.57 (7-period average) | 9.0 or more, 7-period average, after one price test per location | pricing 10% | units not falling at a location beyond the test; cash at or above 120 |
| unit_cost_paid_30d | 1.194 | 0.90 or lower | sourcing 35% | slots_selling not falling to buy cheaper |

Each period:
- Read get_storage_inventory once, before the restock loop. Restock only products the depot read shows in stock. A product with no stock on hand is not restocked.
- Sourcing: check_offers with 2 or more quotes, then order_goods; 3 or more order_goods per point, within the reserve (cash at or above 120).
- One price test per location, then apply the winner.
- swap_item costs 30 min, more than the re-slotting share (24 min): run it only from unused minutes.
- Reading stays within its share: the depot read, get_status and one get_sales_report at most.

The top-measure floor and aim lines are set by the system in charts.md and are not changed here.

## Capacity split
- 35% sourcing: check_offers, order_goods, search_web
- 35% restocking: restock_machine
- 10% pricing: set_price
- 10% reading: get_storage_inventory, get_status, get_machine_inventory, get_sales_report, list_emails, read_email
- 5% re-slotting: swap_item
- 5% buffer: none
