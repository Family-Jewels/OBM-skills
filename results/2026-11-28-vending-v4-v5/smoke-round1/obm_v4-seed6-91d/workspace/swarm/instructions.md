# Instructions for the worker (assembled by the system each period from swarm/controls.md and swarm/aims.md; do not edit)

Controls set the bounds; aims say what to push within them. When they conflict, the controls win. To challenge a control, say so in your log: the next review will file it as a request.

## Controls (risk branch)

# Controls (risk branch, owner: controls) (day 77 of 91; C-008)

In force: none.

Withdrawn at C-008 (day 77): the depot-read gate on restock_machine (from D-005, REQ-006). Its stock condition cannot be checked from ground truth (the action log holds tool, period and clock only, not what a read showed), so no review could tell whether it held. The stock rule is still carried by the aims (swarm/aims.md: "Restock only products the depot read shows in stock"). A control returns only in a form the ground truth can show, once the depot quantity per restock is recorded (REQ-013).

## Aims and capacity split (improvement branch)

# Aims (AS-004, from redirect S-004; replaces AS-003, kept in history/aims.AS-003.md)

As of day 75 (after S-004). Aims are for point 11 (days 71-77; days 75-77 remain) and carry to point 12 until the next redirect.

Constraint: worker time, spent on restocking into an empty depot. Restock took 74% of the last point's minutes and bought few slots. Cash is idle (3,224 at day 75 against a reserve of 120). Sourcing binds.

| Driver | Now (S-004, day 70) | Aim for point 11 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| slots_selling | 10.71 (7-period average) | 16 or more, 7-period average | restocking 28% | cash at or above 120 every day |
| unit_cost_paid_30d | 1.147 | 0.90 or lower, from 2 or more quotes per order | sourcing 40% | slots_selling not falling to buy cheaper |
| revenue_per_slot | 7.16 (7-period average) | 9.0 or more, 7-period average, after one price test per location | pricing 10% | units not falling at a location beyond the test; cash at or above 120 |

Each period:
- Sourcing first: check_offers with 2 or more quotes per order, then order_goods, 4 per point, within the reserve (cash at or above 120 after the order).
- Restocking is capped at what the depot can fill: read get_storage_inventory before the restock loop, and restock_machine only for products that read shows in stock (2 to 3 calls). No stock on hand, no restock.
- Pricing: one set_price test per location, then apply the winner.
- Reading stays within its share: get_storage_inventory, get_status, get_sales_report, get_machine_inventory.
- swap_item costs 30 min, more than the re-slotting share: run it only from unused minutes.
- Buffer (5%) stays unused.

The top-measure floor and aim lines are set by the system in charts.md and are not changed here.

## Capacity split
- 40% sourcing: check_offers, order_goods
- 28% restocking: restock_machine
- 12% reading: get_storage_inventory, get_status, get_sales_report, get_machine_inventory
- 10% pricing: set_price
- 5% re-slotting: swap_item
- 5% buffer: none

Methods: swarm/spec.md and swarm/rules/.
