# Controls (risk branch; written by the controls owner only; the worker reads them through swarm/instructions.md)

Limits and checks the worker stays within. Aims say what to push for inside them; controls win a conflict.

- Before each wait_for_next_day, call get_sales_report that day if it has not been called since the morning | guards: day's pricing decided without that day's sales, so revenue_per_slot and the cash guardrail drift unseen | review at point 5 | from D-001 (REQ-005)
