# Controls (risk branch, owner: controls) (day 28 of 91)

No controls in force.

C-001 (day 19) reviewed D-001 and found the capacity-split drift environmental; no control added. Its reopen trigger is still pending. C-002 (day 28) checked it against REQ-006 and found it not met:
- Its precondition is a reconciled worker-time measure. That is still open (REQ-005 to designer, REQ-008 to human), and Resources (median 30 min a day used) still conflicts with the Facts table (restock_machine 88% of the last point).
- Depot stock before each restock is not in the Facts table or the charts. The evidence that restocks ran without stock is the worker's behaviour, not a measure.
- The depot-read line is already requested to the designer (S-001, REQ-009). A control for the same read would duplicate it and add a read of 25 min median to each restock of 45 min.

Reopen trigger (unchanged): if the reconciled worker-time measure shows restock_machine running without depot stock for the product, add one check: "confirm depot stock for the product (get_storage_inventory) before restock_machine". Review at point 5.
