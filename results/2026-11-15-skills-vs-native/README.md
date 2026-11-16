# OBM skills vs Claude Code native, Vending Bench 365 days, seed 1

Harness: [`../../lab/vending2`](../../lab/vending2). One run per usage window. Usage-limit cutoffs are environment failures and are not scored.

| Arm | Score | Completed | Cost | Turns | Stocked slots/day | Revenue by quarter | Gate refusals | Sub-agents | Skills used |
| --- | ---: | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| obm_enf | €9,292.79 | 365 of 365 days | $10.25 | 2,233 | 7.6 | €5,347 / €7,587 / €5,784 / €5,390 | 0 | 0 | 2 (designer, orchestrator) |
| native (/plan + /goal) | €9,442.60 | 365 of 365 days | $11.45 | 2,320 | 7.5 | €7,971 / €8,423 / €6,340 / €3,298 | n/a | 0 | 0 |
| obm_cadence (replaces obm) | not scored: harness timeout at day 217 (cash €9,698) | | | | 9.6 | €7,427 / €9,872 / partial | | | |
| base | pending | | | | | | | | |

## Run 1: OBM skills + stop gate

Completed the year with €9,292.79 (start €1,500). The gate never had to refuse a stop. Revenue held roughly level across quarters, with no late-year decay.

**The skills were set up and then abandoned.** On day 1 the agent used the designer skill to build a full work system in `swarm/`: a spec with done criteria and milestones, a task board, a rules file and a metrics file. It kept a progress log until day 15. After that it ran the business directly for the remaining 350 days without touching the system again:

- The index was never updated after day 1. The progress log ends on day 15.
- No sub-agents were started. The checker, auditor and diagnostician never ran, so there were no audits, no milestone gates and no rule changes (`rules/operator.v1.md` is the only version).
- Average stocked slots, 7.6 per day, is close to the low-target run in the earlier batch (7.9). Nothing in the run reviewed whether stocking more would pay.

This is the same pattern as the earlier protocol-only run that stopped on day 179: a written management system is followed at the start and then fades. In behavior-analytic terms, the rules had no consequences attached, so following them extinguished. Whether enforcing the process itself (for example, the harness calling the auditor every 30 simulated days, or refusing to advance past a milestone without a scorecard entry) would keep the system alive is the obvious next question for the enforcement layer.

## Run 2: Claude Code native (/plan + /goal)

Completed the year with €9,442.60, within €150 of run 1. Plan mode blocked every business tool, including read-only ones, so the plan was written from the briefing alone (`native-seed1-365d/plan.md`). /goal then kept the session running to day 365. Revenue fell in the second half, to €3,298 in the last quarter: the same late-year decay as the earlier baseline.

## Run 3 replaced: OBM with a cadence run by the system

Run 1 showed the skills being set up and then abandoned, because each role relied on the others to call it. Run 3 now tests the alternative: the harness runs the cadence (daily ground-truth measures, an audit every 30 simulated days, a diagnosis when the audit asks for one, all handed back to the operator in the day-advance result). Harness: `lab/vending2/cadence.py`. The skills were updated to match (protocol section 2.2).

A first 35-day smoke test of this arm found a serious problem: the day-30 audit told the operator to stop buying until its records were complete, and every machine was empty within four days. The auditor and orchestrator skills now judge the business outcome first and never pause the core work to fix records.

## Run 3: OBM with the system running the cadence, cut off by the harness (not scored)

The run was stopped by the harness's own wall-clock limit at simulated day 217, with €9,698 in cash, ahead of every other arm at that point (run 1 and run 2 finished the full year at about €9,300 to €9,400). The benchmark labels it "stopped before the horizon", but the agent did not stop: the cadence work runs inside the operator's turn, and 29 pulses, 7 audits and 34 diagnoses added more than the limit allowed. It is an environment failure and is not scored. The run's audits and cadence log are kept in `obm_cadence-seed1-365d-harness-timeout/`.

**What it showed before the cutoff:**

- The system kept the skills alive. Unlike run 1, where the swarm was abandoned after day 15, every scheduled pulse and audit ran and was handed to the operator.
- Capacity in use rose: 9.6 stocked slots a day, against 7.5 to 7.6 for runs 1 and 2. Revenue in the second quarter (€9,872) was the highest of any arm.
- Rules changed too often: almost every weekly pulse asked for a diagnosis, because a persisting problem counts as a repeat, and the run collected 39 rule files. Rules changed faster than their effect could be measured.

**Fixes before the rerun (harness, not skills):** at least 21 periods between rule changes, with pivots in between; and turn limits on each review so the cadence pauses stay short.
