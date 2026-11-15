# OBM skills vs Claude Code native, Vending Bench 365 days, seed 1

Harness: [`../../lab/vending2`](../../lab/vending2). One run per usage window. Usage-limit cutoffs are environment failures and are not scored.

| Arm | Score | Completed | Cost | Turns | Stocked slots/day | Revenue by quarter | Gate refusals | Sub-agents | Skills used |
| --- | ---: | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| obm_enf | €9,292.79 | 365 of 365 days | $10.25 | 2,233 | 7.6 | €5,347 / €7,587 / €5,784 / €5,390 | 0 | 0 | 2 (designer, orchestrator) |
| native | pending | | | | | | | | |
| obm | pending | | | | | | | | |
| base | pending | | | | | | | | |

## Run 1: OBM skills + stop gate

Completed the year with €9,292.79 (start €1,500). The gate never had to refuse a stop. Revenue held roughly level across quarters, with no late-year decay.

**The skills were set up and then abandoned.** On day 1 the agent used the designer skill to build a full work system in `swarm/`: a spec with done criteria and milestones, a task board, a rules file and a metrics file. It kept a progress log until day 15. After that it ran the business directly for the remaining 350 days without touching the system again:

- The index was never updated after day 1. The progress log ends on day 15.
- No sub-agents were started. The checker, auditor and diagnostician never ran, so there were no audits, no milestone gates and no rule changes (`rules/operator.v1.md` is the only version).
- Average stocked slots, 7.6 per day, is close to the low-target run in the earlier batch (7.9). Nothing in the run reviewed whether stocking more would pay.

This is the same pattern as the earlier protocol-only run that stopped on day 179: a written management system is followed at the start and then fades. In behavior-analytic terms, the rules had no consequences attached, so following them extinguished. Whether enforcing the process itself (for example, the harness calling the auditor every 30 simulated days, or refusing to advance past a milestone without a scorecard entry) would keep the system alive is the obvious next question for the enforcement layer.
