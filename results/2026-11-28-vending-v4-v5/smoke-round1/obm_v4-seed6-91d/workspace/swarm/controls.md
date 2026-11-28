# Controls (risk branch, owner: controls) (day 91 of 91; C-009)

In force: none.

Withdrawn at C-008 (day 77): the depot-read gate on restock_machine (from D-005, REQ-006). Its stock condition cannot be checked from ground truth (the action log holds tool, period and clock only, not what a read showed), so no review could tell whether it held. The stock rule is still carried by the aims (swarm/aims.md: "Restock only products the depot read shows in stock"). A control returns only in a form the ground truth can show, once the depot quantity per restock is recorded (REQ-013).

Reviewed at C-009 (day 91): no new control. The capacity-split drift (D-011) is a brief and measurement fault (designer REQ-012, human REQ-019), not a risk to the floor: cash is 3,965 against a reserve of 120, and the guardrail is ok. No control added. See swarm/audits/C-009.md.
