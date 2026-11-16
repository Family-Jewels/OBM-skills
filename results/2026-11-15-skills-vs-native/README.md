# OBM skills vs Claude Code native, Vending Bench 365 days, seed 1

Harness: [`../../lab/vending2`](../../lab/vending2). One run per usage window. Usage-limit cutoffs are environment failures and are not scored.

| Arm | Score | Completed | Cost | Turns | Stocked slots/day | Revenue by quarter | Gate refusals | Sub-agents | Skills used |
| --- | ---: | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| obm_enf | €9,292.79 | 365 of 365 days | $10.25 | 2,233 | 7.6 | €5,347 / €7,587 / €5,784 / €5,390 | 0 | 0 | 2 (designer, orchestrator) |
| native (/plan + /goal) | €9,442.60 | 365 of 365 days | $11.45 | 2,320 | 7.5 | €7,971 / €8,423 / €6,340 / €3,298 | n/a | 0 | 0 |
| obm_cadence (replaces obm) | not scored: harness timeout at day 217 (cash €9,698) | | | | 9.6 | €7,427 / €9,872 / partial | | | |
| obm_cadence, charts (run 4) | €18,847.26 | 365 of 365 days | $20.55 (incl. $1.54 cadence) | 2,967 | 10.9 | €9,560 / €11,424 / €7,539 / €9,128 | 0 | 0 | 6 |
| native + system reviews (run 6) | €11,890.10 | 365 of 365 days | $19.47 (incl. $1.03 reviews) | 2,374 | 8.7 | €8,307 / €6,723 / €5,996 / €8,782 | n/a | 0 | 0 |
| base (no skills, no plan or goal) | €8,187.24 | 365 of 365 days | $9.64 | 1,936 | 6.7 | €6,910 / €6,727 / €4,894 / €3,588 | n/a | 0 | 0 |

## Summary

Five arms, one seed, the same benchmark (start €1,500; the benchmark's reference operator, which knows the hidden parameters, reaches about €61,200):

| Arm | Score | What its workspace shows |
| --- | ---: | --- |
| base | €8,187 | Nothing: no files. Revenue fell every quarter, from €6,910 to €3,588. |
| obm_enf (skills + stop gate) | €9,293 | A full work system built on day 1 and abandoned on day 15. |
| native (/plan + /goal) | €9,443 | A plan written blind (plan mode blocked the business tools), then no records. Revenue fell to €3,298 in Q4. |
| obm_cadence, KPIs (run 3) | not scored | Harness timeout at day 217 with €9,698, ahead of every arm at that point. |
| native + system reviews (run 6) | €11,890 | The same reviews, charts and loop as run 4, without the skills. Its 14 plan revisions drifted into record-keeping and spending freezes. |
| **obm_cadence, charts (run 4)** | **€18,847** | 46 pulses, 7 audits, 14 diagnoses and 13 redesigns over the full year, each read and noted by the operator. |

Skills alone (run 1) did about as well as Claude Code's own tools (run 2), both a little above the bare agent. The difference came when the system, not the agent, ran the reviews: run 4 doubled the other completed arms, stocked more slots (10.9 a day against 6.7 to 7.6) and had no late-year decay. It also cost about twice as much ($20.55 against $9.64 to $11.45). One seed is not enough to call this a finding; more seeds are the next step.

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


## Run 4: OBM with the cadence and process behavior charts, full year

Completed the year with **€18,847.26**, about twice runs 1 and 2 (€9,293 and €9,443). Same harness as run 3, with the 5/50 cadence, charts in place of KPIs, the diagnose-then-redesign loop and the benchmark's reference operator as the exemplar. Cost $20.55, of which the cadence reviews were $1.54. Runtime 87 minutes.

- **Capacity in use** averaged 10.9 stocked slots a day (runs 1 and 2: 7.5 to 7.6). Revenue was higher than both other arms in every quarter, with no late-year decay: Q4 (€9,128) recovered from a Q3 dip.
- **The cadence ran all year:** 46 pulses, 7 full audits (5 scheduled, 2 triggered by a wrong-direction chart signal on days 300 and 336), 14 diagnoses, 24 diagnosis requests deferred by the spacing rule, and 13 redesigns (spec v1 to v12, operator brief v1 to v10, every old version kept in `history/`).
- **The operator acted on what it was handed.** Each pulse, audit, diagnosis and redesign is noted in its progress log on the day it arrived, with the pivots it applied or why it didn't.
- **Redesign predictions mostly did not hold.** Most redesigns predicted a rise in stocked selling slots; the charts showed no upward shift for most of them, and later records say so plainly (R-P-029 corrects a wrong baseline; R-P-038 declines to change rules while an earlier prediction is still being judged). The loop was honest about its misses, but it never found the change that moved the top measure. The recurring cause it diagnosed: one slot per restock call, with depot stock-outs and late drinks deliveries.
- **Gap to the exemplar:** PIP 3.4 at day 365 (the reference operator, which knows the hidden parameters, gained 3.4 times as much).

**Weaknesses this run exposed:**

- The charts have no notion of season. The holiday demand drop in the last two weeks (the benchmark's multiplier falls to 0.05) showed as wrong-direction signals and triggered an audit and a diagnosis. Seasonal demand needs either a seasonal baseline or a measure that is not affected by it (sales per stocked slot against expected demand).
- Two redesigns landed 11 days apart (R-P-041 on day 327, R-P-042 on day 332, adopted); the spacing check counts from when a redesign starts rather than when the previous one was adopted.
- The operator stopped restocking in the last two weeks; with holiday demand near zero that cost little.

Records: `obm_cadence-seed1-365d/` (result, cadence log, final spec, charts, rules, every pulse, audit, diagnosis and redesign, and earlier versions).

One seed: twice the score of the other arms is a large difference, but it needs other seeds before it is a finding.

## Run 3: OBM with the system running the cadence, cut off by the harness (not scored)

The run was stopped by the harness's own wall-clock limit at simulated day 217, with €9,698 in cash, ahead of every other arm at that point (run 1 and run 2 finished the full year at about €9,300 to €9,400). The benchmark labels it "stopped before the horizon", but the agent did not stop: the cadence work runs inside the operator's turn, and 29 pulses, 7 audits and 34 diagnoses added more than the limit allowed. It is an environment failure and is not scored. The run's audits and cadence log are kept in `obm_cadence-seed1-365d-harness-timeout/`.

**What it showed before the cutoff:**

- The system kept the skills alive. Unlike run 1, where the swarm was abandoned after day 15, every scheduled pulse and audit ran and was handed to the operator.
- Capacity in use rose: 9.6 stocked slots a day, against 7.5 to 7.6 for runs 1 and 2. Revenue in the second quarter (€9,872) was the highest of any arm.
- Rules changed too often: almost every weekly pulse asked for a diagnosis, because a persisting problem counts as a repeat, and the run collected 39 rule files. Rules changed faster than their effect could be measured.

**Fixes before the rerun (harness, not skills):** at least 21 periods between rule changes, with pivots in between; and turn limits on each review so the cadence pauses stay short.

## Run 5: base (no skills, no /plan or /goal)

Completed the year with €8,187.24, the lowest completed score, at the lowest cost ($9.64, 27 minutes). The workspace is empty: the agent kept no plan, log or records. It averaged 6.7 stocked slots a day, and revenue fell every quarter (€6,910, €6,727, €4,894, €3,588), the same late-year decay seen in run 2 but steeper.

## Run 6: Claude Code native (/plan + /goal) with the system running the reviews

The direct comparison with run 4. The harness ran the identical cadence: the same charts and exemplar, a check every 5 days, a full review every 50, a diagnosis when a review asked for one, and a plan revision from it, at least 20 days apart, all handed to the operator in the day-advance result. The only difference is that no OBM skills were installed. The work system was the plan Claude wrote in plan mode (kept as `swarm/plan.md`), and the reviewers got plain instructions: check how it is going, find what is wrong, revise the plan. The operator ran under /goal rather than the stop gate (which never refused a stop in run 4).

Completed the year with **€11,890.10**: more than every arm without system-run reviews (€8,187 to €9,443), but €6,957 short of run 4 (€18,847). Cost $19.47, close to run 4's $20.55; the reviews cost $1.03. PIP 5.7, against 3.4 for run 4.

| | Run 4: skills + system reviews | Run 6: native + system reviews |
| --- | ---: | ---: |
| Score | €18,847 | €11,890 |
| Stocked slots/day | 10.9 | 8.7 |
| Revenue by quarter | €9,560 / €11,424 / €7,539 / €9,128 | €8,307 / €6,723 / €5,996 / €8,782 |
| Checks / full reviews / diagnoses / revisions | 46 / 7 / 14 / 13 | 50 / 6 / 15 / 14 |
| Diagnoses deferred by spacing | 24 | 40 |
| Cost | $20.55 | $19.47 |

**What the workspace shows.** The reviews ran just as reliably, and the operator received all of them. The difference is in what the reviewers asked for. Without the skills, the plan revisions turned toward record-keeping and spending control: reconcile spend before ordering (v4), a purchase gate (v7, v8), a standing freeze on orders until records were complete (v9), a self-enforcing freeze (v10), a total freeze on orders and campaigns (v12). The freeze was replaced with a capped restock only at v15 on day 317. Revenue fell from about €2,800 a month in the first four months to €1,640 to €2,310 in months five to nine, while these gates and freezes were in force. It recovered to €3,000 to €3,300 in months ten and eleven, as later revisions dropped the ledger requirement (v13, day 287) and then replaced the freeze (v15). That is the same failure the 35-day smoke test of the skills found and fixed (an audit that paused buying until records were complete); the auditor and orchestrator skills now say to judge the outcome first and never pause the core work to fix records. Without those rules, the plain reviewers fell into it over and over.

**What this says.** On this seed, running the reviews from the system lifted Claude Code's native tools by about €2,450 (run 2 to run 6). Adding the skills to the same reviews lifted it by another €6,950 (run 6 to run 4). Most of the gain came from what the skills tell the reviewers to look at, not just from having reviews at all. One seed each; this needs more seeds.

Records: `native_cadence-seed1-365d/` (result, cadence log, every plan version, every review, diagnosis and revision).
