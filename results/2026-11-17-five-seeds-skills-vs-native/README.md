# Five seeds: OBM skills vs Claude Code /plan + /goal, both with system-run reviews

Prosus Vending Bench, 365 simulated days, seeds 1–5, model claude-haiku-5-5. Score = final bank balance (start €1,500; the scripted reference operator reaches about €61,219).

Both arms run under the same cadence engine: a pulse review every 5 days, a full audit every 50, diagnosis on a chart signal or a large gap to the reference, and a redesign after each diagnosis. Redesigns are spaced at least 20 days after the last one was adopted, one at a time (fix 0b55524). The arms differ only in what the reviewers and the worker are given:

- **obm_cadence**: the OBM swarm skills (designer, orchestrator, auditor, diagnostician; protocol), with a designed work system (spec, driver tree, rules) and the stop gate.
- **native_cadence**: Claude Code's built-in plan mode and goal. The plan from plan mode becomes `swarm/plan.md`. Reviewers get neutral prompts with no skills, and revisions rewrite the plan.

## Decision rule (set before the runs)

The skills arm counts as better if it wins **at least 4 of 5 seeds** and the **mean gain is clearly above zero**.

**Result: not met.** The skills arm won 4 of 5, but seed 5 went strongly the other way. The mean gain is +€653 (about 5%), with a standard deviation of the paired differences of about €4,000. An exact sign-flip test gives p ≈ 0.41 (one-sided), so the mean gain is not distinguishable from zero.

## Scores

| Seed | Skills + system reviews | /plan + /goal + system reviews | Difference |
|---|---:|---:|---:|
| 1 | €15,006 | €10,902 | +€4,105 |
| 2 | €14,171 | €10,891 | +€3,279 |
| 3 | €13,666 | €13,233 | +€433 |
| 4 | €13,435 | €11,923 | +€1,512 |
| 5 | €13,497 | €19,563 | −€6,066 |
| **Mean** | **€13,955** | **€13,302** | **+€653** |
| SD across seeds | €655 | €3,629 | €4,023 |

All ten runs completed 365 days with no usage-limit rejection in their streams. Two attempts were cut off and not scored; their folders are kept outside the repo as `stopped-*`:

- an obm_cadence seed 2 run, stopped at Jules's request to save usage;
- a native_cadence seed 4 run, which hit the 5-hour usage limit at day 292.

## What else differed

| Measure (mean over 5 seeds) | Skills | /plan + /goal |
|---|---:|---:|
| Stocked selling slots a day | 10.5 (range 9.2–11.5) | 9.4 (range 7.2–13.9) |
| API cost a run | $20.57 (+$1.21 reviews) | $14.09 (+$0.69 reviews) |
| Pulses / audits / diagnoses | 41 / 7.2 / 8.0 | 43 / 7.2 / 9.0 |
| Redesigns adopted | 7.6 | 8.4 |
| Runs that froze buying | 0 of 5 | 2 of 5 (seeds 2 and 4) |

Quarterly revenue (€):

| Seed | Skills Q1–Q4 | /plan + /goal Q1–Q4 |
|---|---|---|
| 1 | 9,420 · 10,035 · 7,088 · 10,115 | 5,676 · 9,193 · 6,551 · 5,016 |
| 2 | 6,152 · 11,528 · 9,876 · 8,859 | 6,166 · 6,890 · 6,240 · 5,574 |
| 3 | 10,768 · 15,723 · 6,729 · 3,939 | 8,550 · 8,258 · 7,673 · 4,774 |
| 4 | 6,316 · 9,455 · 11,882 · 6,958 | 10,318 · 8,586 · 3,435 · 3,287 |
| 5 | 5,761 · 10,414 · 8,684 · 8,806 | 6,839 · 11,952 · 14,544 · 9,136 |

## Findings

- **The skills arm was much more consistent, but not reliably better.** Its five scores sit within €1,600 of each other. The /plan + /goal arm ranged from €10,891 to €19,563. The consistency was not part of the pre-set rule, so it is an observation to test, not a result.
- **Stocked slots track the score in both arms.** The best run of all, /plan + /goal seed 5, kept 13.9 slots stocked a day. Its plan revisions pushed toward spending idle cash on stock and filling empty slots to capacity; its final plan states that "idle cash is a loss, not a reserve". The worst /plan + /goal runs went the other way.
- **Over-control was the /plan + /goal arm's main failure, and the skills arm avoided it.** In seeds 2 and 4, the plain reviewers' plan revisions froze buying until records or cash reconciliations were complete. In seed 4 the freeze ran from day 278 to the end, and audits kept re-triggering it. No skills run froze buying. Their only holds were on prices or product mix, and on stock that could not sell before day 365.
- **The skills arm's ceiling is the problem.** No skills run went above €15,006. Every run, in both arms, ended at least four times below the reference operator. The skills keep the business from collapsing, but they did not find what /plan + /goal seed 5 found.
- **Redesign predictions.** Skills redesigns state a testable prediction, and later reviews judge it. A keyword screen of the review records finds misses at least as often as hits, which matches the earlier single-seed run. /plan + /goal revisions rarely state a prediction.
- **Cost.** The skills arm cost about 45% more a run ($20.57 against $14.09).

## What this means for the skills (general changes only, not tuned to this bench)

1. Do not claim a performance gain from this benchmark. A claim of lower variance needs its own pre-set test.
2. The gap to the best was visible all year, yet no redesign closed it. The general question is whether the diagnostician and designer are told plainly to look for under-used resources, as well as for faults. This is one hypothesis, to be tested on a different task before any change.
3. Guardrails against over-control (never pause the core work to fix records) appear to do their job. Keep them.

## Reproduce

Each run folder holds `result.json`, the cadence engine log `cadence.jsonl`, and the full workspace: spec, plan and plan history, audits, diagnoses, redesigns and the operator log. `tabulate.py` rebuilds the tables from these folders:

```
SEEDS_DIR=. python3 -I tabulate.py /dev/null
```

Runner: `lab/vending2/run_arms2.py --arm {obm_cadence,native_cadence} --seed N --days 365 --budget 40 --timeout 7000`. Engine: `lab/cadence/engine.py`.

The script's freeze count is a keyword screen. The "froze buying" row above comes from reading the hits.
