# Controls (risk branch, owner: controls) (day 77 of 91; C-008)

In force: none.

Withdrawn at C-008 (day 77): the depot-read gate on restock_machine (from D-005, REQ-006). Its stock condition cannot be checked from ground truth (the action log holds tool, period and clock only, not what a read showed), so no review could tell whether it held. The stock rule is still carried by the aims (swarm/aims.md: "Restock only products the depot read shows in stock"). A control returns only in a form the ground truth can show, once the depot quantity per restock is recorded (REQ-013).
