# Controls (risk branch, owner: controls) (day 35 of 91)

No controls in force.

Standby (held, not in force; the worker does not act on it yet):
- Before restock_machine for a product, confirm depot stock for it (get_storage_inventory); skip the restock if the depot shows none. | guards: worker time spent restocking empty products, which the sourcing and pricing lines need (restocking 83% of the last point against a 45% plan) | held for the reopen trigger: only add it if the depot-stock-per-restock record (REQ-010) shows restock_machine running with no depot stock for the product | review at point 6 | from D-002 (REQ-006)

Why held: aims AS-001 already asks the worker to read depot stock before each restock, so a control now would duplicate that line and add 25 min to each 45 min restock. Judge the trigger when REQ-010 is recorded or at point 6, whichever comes first.
