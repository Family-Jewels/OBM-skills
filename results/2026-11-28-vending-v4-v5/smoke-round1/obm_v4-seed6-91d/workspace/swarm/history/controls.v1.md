# Controls (risk branch, owner: controls) (day 19 of 91)

No controls in force.

C-001 (day 19) reviewed D-001 (capacity-split-drift) and found the fault is environmental: stale day-0 aims and a split with no line for depot reading or stock purchase. No bound on the worker closes it, so none was added. Reopen trigger: if the reconciled worker-time measure (REQ-005 / REQ-008) shows restock_machine running without depot stock for the product, consider one check before restocking: "confirm depot stock for the product (get_storage_inventory) before restock_machine".
