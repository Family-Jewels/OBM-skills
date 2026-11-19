# v2 clean test: every experiment fix in place from day 1 (91 days, seed 6)

The third 91-day run on seed 6. It was the first with every fix from [the previous run](../2026-11-19-v2-smoke-experiments) in place from the start.

| Measure | v2 test 1 (no lifecycle) | v2 test 2 (fixes mid-run) | This run |
| --- | --- | --- | --- |
| Final balance (from €1,500) | €4,861 | €3,719 | €3,388 |
| Average stocked slots | 11.6 | 8.5 | 11.1 |
| Cost (all) / reviews | $3.80 / $0.18 | $3.25 / $0.37 | $4.19 / $0.41 |
| Fidelity checks: passed / failed | — | 0 / 9 | 1 / 9 |
| Verdicts by the auditor | — (the worker judged) | 0 | 1 |

## The first complete lifecycle

E-001 raised prices 10% on the top three products of one snack machine, with the other five machines as control.

1. **The first fidelity check failed correctly:** on day 5 nothing had been changed.
2. **The second check passed** after the worker applied the change on day 9.
3. **The system compared** slice against control after the clock ran.
4. **The auditor ruled "too small to read".** The effect was in the wrong direction but inside the earlier bounce, with only two points on each side. The auditor recommended a longer run if the budget allows, and explained why a larger slice would not help.

## Why the other experiments failed: the worker did not carry them out

Unlike the previous run, these failures were real. The checker found from ground truth that the change had not been made.

| Experiment | What the checks found |
| --- | --- |
| E-002: a print campaign at one location | No campaign was run in 20 days; `Applied` stayed blank |
| E-003: swap 2 drink slots on one machine to coffee | Not made, then made on 1 slot of 2 |
| E-005: put coffee into any emptied drink slot on one machine | The worker kept placing energy drinks, cola and water there; its own note admitted 2 errors, and the snapshots showed 7 |

**The pattern:** the one change that passed was a one-time setting (a price). The ones that failed needed the worker to act again later (run a campaign each week, restock with a particular product) or to remember a standing rule at every restock. That is an antecedent problem in OBM terms: the instruction arrives once, among many, and competes with the core work.

## What to change (general, not specific to vending)

1. **Make an experiment a state, not a habit.** The designer writes the change as a one-time setting that persists, such as a price, an assortment or a configuration. If it must be a standing rule, it goes into a rule file the worker reads every cycle, not only into the experiment file.
2. **The system hands over the exact change at the start**, as an instruction for that period ("now set these prices on these slots"), the same way it hands over a pulse's fixes. A failed check repeats the instruction with the mismatch.

## A concern to watch

Across three single runs on one seed, the score fell as the experiment machinery grew: €4,861, then €3,719, then €3,388. One run each cannot separate noise from cause. The five-seed test will show it, and its cost rule (v2 no dearer than v1) and floor rule (no v2 run below v1's worst) are already set.
