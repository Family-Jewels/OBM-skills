# Controls (risk branch; written by the controls owner only; the worker reads them through swarm/instructions.md)

Limits and checks the worker stays within. Aims say what to push for inside them; controls win a conflict.

- Before each wait_for_next_day, call get_sales_report that day if it has not been called since the morning | guards: day's pricing decided without that day's sales, so revenue_per_slot and the cash guardrail drift unseen | review at point 7 | from D-001 (REQ-005; re-costed in C-003)
- Before each restock_machine, if the depot holds fewer units of that product than the slots will sell before the supplier's quoted lead time, and no order for it is open, call order_goods for it first; restocking continues from depot stock on hand | guards: slots emptied by stock-outs when depot cover runs shorter than supplier lead time (stock-outs on days 13-14) | review at point 6 | from D-002 (REQ-010)
- Before each order_goods, call check_offers for that product that day, and confirm the quote ordered from has the lowest unit price among quotes whose lead time meets the cover rule above; a check, never a reason to delay an order the cover rule requires | guards: unit_cost_paid_30d above its upper limit (1.026 on day 35 against 1.02), eroding margin on each unit | review at point 7 | from D-005 (REQ-021)
