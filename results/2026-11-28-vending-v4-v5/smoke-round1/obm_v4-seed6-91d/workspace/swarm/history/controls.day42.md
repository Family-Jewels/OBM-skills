# Controls (risk branch, owner: controls) (day 42 of 91)

In force:
- Before each restock loop, call get_storage_inventory once that period and restock only products the depot read shows in stock; a product with no stock on hand is not restocked. | guards: worker time (restocking 80% of the last point against a 45% plan) spent restocking empty shelves, which leaves sourcing and pricing without time | review at point 8 | from D-003 (REQ-006)

Why now: the depot-read line in AS-001 ran through point 6 and restocking still took 80% of capacity, so the aim alone is not holding against the brief's Done line and rule 12. A control takes precedence in a conflict until the operator brief is changed (REQ-012, designer). Cost: one 25-minute read per restock loop.
