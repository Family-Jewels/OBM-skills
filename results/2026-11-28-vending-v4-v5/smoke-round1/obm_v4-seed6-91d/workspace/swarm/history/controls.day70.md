# Controls (risk branch, owner: controls) (day 63 of 91; re-reviewed under C-006, unchanged)

In force:
- Before each restock_machine call, check that this period's get_storage_inventory read shows that product with stock above zero. If the read is missing or shows none, do not restock that product this period; a restock that follows a read showing no stock is not allowed. | guards: worker time (restocking 73% of the last point against a 40% plan) spent restocking empty shelves, which leaves sourcing (13% against 25%) and pricing without time | review at point 10 | from D-005 (REQ-006)

Why this form: the earlier line let a restock follow the read whatever it showed (D-005). This control gates each restock call on the read, and it does not cap restocking or set a share of time. Products with stock on hand are restocked as before. Cost: one 25-minute read per restock loop, as before.
