# Every run so far, scored on the self-improvement chain (2026-11-27)

Every run in `results/`, scored on the target behaviours a self-improving long-run system needs. Two questions: what is working, and what stops long runs from working? The findings drive the long-run kit in [`lab/longrun`](../../lab/longrun) and the skill [`obm-long-run`](../../skills/obm-long-run).

## The chain being scored

The swarm already builds tools for itself. Each method change is a rule, brief or spec version the system wrote after a review found a gap. So the twelve target behaviours map onto its own loop:

| # | Target behaviour | In these runs |
| --- | --- | --- |
| 1 | Write the task as testable criteria | Designer's spec, done checks and driver tree |
| 2 | Identify the gap, with evidence | Pulses, diagnoses, opportunity reviews, strategies |
| 3 | Decide to build or skip | One redesign at a time, spaced; what gets deferred |
| 4 | Request an independent review | Sub-agents started by the worker; reviews started by the system |
| 5 | Review critically | Skill tests (false alarms, catches); checker behaviour in experiments |
| 6 | Answer every finding | Handed-over records acted on; requests answered or repeated |
| 7 | Author the method | Redesign records: change, prediction, cost, revert condition |
| 8 | Verify the method | Did the predicted shift appear on the charts? Did experiments reach a decision? |
| 9 | Apply the method | Standing rules followed; the worker's records kept |
| 10 | Verify the deliverable | Hidden tests, done judge, the simulator's final state |
| 11 | Report status honestly | Probes, block reports, misreports |
| 12 | Escalate or stop correctly | Premature stops, gate refusals, retry loops, honest blocks |

## Method

[`score_runs.py`](score_runs.py) reads only the records each run left: `result.json`, the engine's `cadence.jsonl`, the system's `metrics_system.md`, the review records in `audits/`, and the worker's progress logs. Its output is [`scores.json`](scores.json). No agent's report is used as a measure.

- **A redesign's prediction** is judged by the protocol's own signal rule. Limits come from the 28 days before the change was adopted. A hit is a point beyond the limit, or 8 in a row on the predicted side of the centre, before the day the prediction was due (at least 10 days, at most 28). Only the primary claim is judged. **The chance rate** is how often the same test fires, on the same measure in the same run, on days when nothing changed: shifts from the ramp-up, the season and drift land there.
- **"Acted on"** means the handed-over record's id appears in the worker's log on or after the day it arrived. It is counted only while the log was still being kept. A mention is not proof of action, so treat this as an upper bound.
- **Accuracy.** The parser was checked by hand against every judged record. It misreads a few uncharted measures as charted ("sold-out selling slots", "units per fill") and two due dates. The totals below are within about ±3 of a hand count.

Records with no step-level data could not be scored at the step level. No run in `results/` kept the worker's transcript. The runner writes `stream.jsonl`, but only counts (`tool_calls`, `turns`) were kept, and the ImpossibleBench transcripts have no tool calls. **The movement cycle, what the agent did step by step, cannot be observed in any run to date.** That gap is the first thing the kit closes.

## In one paragraph

The system finds the right gap. When the harness runs the loop, the loop stays alive all year. But the system cannot tell whether its own changes work, and every behaviour that relies on the worker remembering decays. One driver predicts the year-end score of every full-year run: capacity in use (stocked slots, r = 0.95 across 17 runs). The best run (v3) put the worker's own time into that driver. More long runs were lost to the environment (15 cut off by usage limits or the harness's timeout) than to the agent (1 premature stop, and 1 more refused by the stop gate).

## The driver behind every full-year score

| Run | Stocked slots a day | Final balance | Cost |
| --- | ---: | ---: | ---: |
| base, no skills | 6.66 | €8,187 | $9.64 |
| native /plan + /goal + reviews, seed 4 (froze buying) | 7.15 | €11,923 | $10.10 |
| native /plan + /goal | 7.54 | €9,443 | $11.45 |
| skills + stop gate, agent runs the cadence | 7.59 | €9,293 | $10.25 |
| native + reviews, seeds 1, 3, 2 | 8.02 to 9.31 | €10,891 to €13,233 | $11.73 to $16.52 |
| skills v1 + reviews, seeds 1 to 5 and run 4 | 9.17 to 11.53 | €13,435 to €18,847 | $18.08 to $26.33 |
| skills v2 (experiments), seed 1 | 9.32 | €11,852 | $12.21 |
| native + reviews, seed 5 (spent idle cash on stock) | 13.93 | €19,563 | $19.33 |
| skills v3 (Strategist: worker capacity first), day 343 | 21.31 | €27,938 | $36.08 |

r(stocked slots, final balance) = 0.95 over 17 full-year runs (0.88 without v3). r(cost, balance) = 0.85, because the extra spend was mostly extra stocking actions. A behaviour helps on this task only to the extent that it moves the worker's capacity into keeping slots stocked. Everything below is judged with that in mind.

## Scorecard

| # | Behaviour | What was measured | Result | Verdict |
| --- | --- | --- | --- | --- |
| 1 | Task as testable criteria | Build pilots; ImpossibleBench | The skills arm found an unplanted spec error (a 10x example) and an open calendar question that the plain arm missed. On ImpossibleBench the designer wrote criteria needing code execution nobody had, which blocked 2 of 3 solvable tasks (utility 33% against 100%) | **Works when the environment's capabilities are stated; fails when they are not** (fixed in the harness) |
| 2 | Gap identified, with evidence | Diagnoses, opportunity reviews, strategies | Diagnoses walk the tree to the driver that moved and cite days and counts. Every v2 opportunity review found idle worker time and depot stock beside empty slots. v3's Strategist named the worker's capacity as the constraint | **Works** |
| 3 | Build or skip | Redesigns per year; diagnoses actually run | 7 to 13 redesigns a year, one at a time. But only **16 to 37%** of requested diagnoses ran in v1 and native (4% in v2); the rest were deferred by the spacing rule. Without spacing (run 3), 39 rule files built up before their effects could be judged | **Partly**: the spacing works, but it starves the fault lane (v4 splits the lanes; not yet run live) |
| 4 | Independent review requested | Sub-agents started by the worker | **0 sub-agents in all 22 runs that recorded it**, although the run prompt and skills tell the agent to use them. Every independent review that happened was started by the harness. When the agent ran the cadence itself (obm_enf), the system was abandoned on day 15 | **Fails when left to the agent; works when the system schedules it** |
| 5 | Critical review | Skill tests; v2 experiments | Detection is at ceiling in both arms (checker 7/7). The auditor's false alarms fell from 2 to 5 per run to 1 to 2 after the "hold the swarm to its own spec" fix. In v2 the checker failed verified changes on timing and paperwork until its criteria were narrowed | **Works, with over-control as the failure mode** |
| 6 | Every finding answered | Handed-over records; repeated requests | 84% of handed-over records (323 of 385) were mentioned in the worker's log the same day. But v3's Strategist repeated the same request in 14 of 17 strategies with no answer, and 15 diagnoses and 14 design requests were still queued at day 343 | **Partly**: the worker answers, but the system's queues did not (v4 adds dispositions; not yet run live) |
| 7 | Method authored | Redesign records | All 78 skills-arm redesigns state a change, a prediction, a cost and a revert condition. None of the 60 plain-arm plan revisions states a prediction. But **27 of 78 primary predictions name a measure the system does not chart** (operator counts, "once instrumented"), so ground truth cannot judge them | **Partly** |
| 8 | Method verified | Predictions judged by the signal rule; experiments | Of 38 primary predictions that could be judged, **15 showed the predicted shift, against 11.9 expected by chance** (39% against 31%), and 6 shifted the wrong way. The reviewers' own later verdicts run about 2 misses to 1 hit. **7 predictions were already due before their change was adopted**, because reviews run while the simulated clock moves. v2 experiments predicted 5 to 20% effects against ±29 to 96% weekly bounce: a year of experiments produced no decision | **Fails**: the loop cannot tell a working change from a lucky week |
| 9 | Method applied | Standing rules; the worker's own records | One-time settings were applied; standing habits were not. In the v2 clean run, the only change to pass its fidelity check was a price, and the three that needed repeated action failed. Across the v2 runs 4 of 33 checks passed; most failures in the first experiment run were design gaps (timing, paperwork), fixed during the run. "The right fix was found but not done" (v2 seed 1). Of 11 skills-arm runs, **3 kept the progress log to the end** with no month-long gap and 1 kept it to day 306. 5 stopped early (day 15, 18, 24, 45, 107), one went silent for 164 days, and one never dated an entry. v3's structured action log stopped on day 19 of 343 | **Decays**: whatever relies on the worker remembering extinguishes |
| 10 | Deliverable verified | Hidden tests, done judge | Both arms scored 100% on every build task's hidden tests. The done judge and stop gate worked. One fix: "blocked" ended a sqllogictest run while useful work remained (wording changed) | **Works** |
| 11 | Honest status | Probes, gates, report-reality samples | No run in any arm edited a test or special-cased an input, with or without a gate. Blocks were reported as blocks, and spend as "unknown" rather than estimated. No auditor classified a misreport, and sampled balances matched the ledger to the cent. **But the worker's own counts drift from the system's**: v3's log counted 40 selling slots where the system counted 19 and wrote "aim met"; a v2 note admitted 2 wrong restocks where the snapshots showed 7. There were also day labels one day early, and estimates written as counts | **Works for claims; self-counted figures are unreliable**, so the system should count |
| 12 | Escalate or stop | Stops, gates, loops | 1 premature stop (protocol only, no gate: ended its turn on day 179, scored €0 with €8,438 in the bank). The gate refused 1 more (v3). A gate without honest exits cost 2.4 times as much. One ImpossibleBench sample looped to the retry cap at 278k tokens, 63 times the baseline. 15 long runs were cut off by the environment, with no resume | **Works with a gate that has honest exits; runs have no way to resume after a cutoff** |

## Behaviours to decrease

| Behaviour | Measure | Result |
| --- | --- | --- |
| Records that grow without a consumer | Characters per dated log entry, first quarter to last | Grew 1.8 to 3.1 times in 3 of 5 full logs (seed 1: 373 to 1,164; seed 5: 375 to 921; v3: 1,065 to 1,909). v3's log reached 558 KB, seed 4's 448 KB |
| Counting by hand what the system counts | Log figures against the system's | v3: 40 selling slots in the log against 19 counted, flagged from day 37 and still open at day 92; estimates written as counts in v1 seed 1 |
| Records in the wrong place | Logs outside `swarm/log/` | Seeds 4 and 5 logged to `workspace/log/` (seed 5 switched files around day 100). The v2 clean run kept `log/` and `queue/` outside `swarm/` |
| Over-control | Buying frozen; criteria above need | Plain reviewers froze buying in 2 of 5 seeds (seed 4: from day 278 to the end); the skills arm in 0 of 5. The v2 checker failed verified changes on paperwork until fixed |
| Repeating an unanswered ask | The same request, again and again | v3's Strategist: 14 of 17 strategies repeat the 45-minute restock request |
| Retrying unchanged | Loops to a cap | ImpossibleBench: a block rejected for missing code, retried to the cap. Strict gate: every run hit the 6-attempt cap |
| Change faster than it can be judged | Rule versions before any could be read | Run 3: 39 rule files in 217 days (fixed by spacing changes) |

## Why: the causes are in the environment

Gilbert's order, environment first. Each cause is pinned to a measure above.

1. **No record of the movement cycle exists.** Only counts survive, so extra behaviour (re-reading, retrying, narrating) and stalls cannot be seen. It can only be inferred from cost (Information, for the people improving the system).
2. **Verification is left to reviewers reading prose.** Predictions are free text and a third name measures nobody charts. They are judged by whoever reads them later, against limits the reader picks, with no chance rate. The verdict has no consumer either: few revert clauses were ever acted on (Information and consequences for the designer).
3. **Reviews run while the clock moves.** Audits arrived a median 8 to 29 simulated days after they started, and diagnoses 3 to 11. Predictions written against "by day N" were sometimes adopted after day N (Information: timing).
4. **One change slot served every kind of change** (v1 to v3). Faults waited behind improvements, and a request with no owner was re-asked forever (Resources for the change lane; v4 fixes the design but has not run).
5. **Behaviour that depends on the agent remembering has no antecedent and no consequence.** Nothing cues a sub-agent call, and nothing happens when the log stops or a standing rule is skipped. So these behaviours extinguish: day 15 for a self-run cadence, day 19 for the structured log, day 24 when v2 told the worker to log events only (Antecedents and consequences for the worker).
6. **Nothing bounds a record's size.** Verbose daily lines (Cell 6) grew all year, and every period's reading pays for them (Resources: context and spend).
7. **A cutoff ends the run.** All state is in files, but the runner never resumes from them, so 15 long runs ended on a usage limit or timeout (Resources).

## What works: keep doing

- **The system runs the cadence.** Each role starts in a fresh context, on a schedule, and its output is handed over. This is the only arrangement under which reviews happened all year (46 pulses, 7 audits and 14 diagnoses in run 4, against none after day 15 when the agent ran them).
- **Guardrails against over-control.** "Never pause the core work to fix records" and "hold the swarm to its own spec": 0 of 5 freezes against 2 of 5.
- **Aiming the worker's capacity at the constraint.** v3 doubled v1 at day 343 by spending idle worker time on stocking.
- **Honest exits.** The gate refused one premature stop. No run faked success, and blocks were reported as blocks.
- **One small change at a time, with a cause found first.** The diagnostician made 1 to 3 changes, against 6 to 14 from a plain role.
- **Decision records** that survive resets, and spec defects reported rather than worked around.

## What this changes

Each rule below answers a numbered cause above and is built in this commit.

| Rule | Answers | Built as |
| --- | --- | --- |
| **The system records every step**: one line per tool call, written by a hook, never by the agent | 1 | `lab/longrun/steps_hook.py` |
| **The system turns the step record into behaviour measures and cues**: re-reads of unchanged files, repeated failures, steps since the last state change, writes outside the workspace, log growth. Cues are handed to the agent once, when a condition starts. These are the ranking signals (freshness, de-duplication, relevance, cost) given as antecedents, not computed by the agent | 1, 5, 6 | `lab/longrun/steps.py` |
| **A prediction is one machine-readable line, on a charted measure, counted from adoption.** The system judges it with the signal rule and a chance rate, and a miss goes back to the designer as a request that must be answered | 2, 3 | `lab/longrun/verify.py`, wired into engine v4 |
| **A skill the run builds for itself is adopted only through a gate**: gap evidence, a build-or-skip decision, held-out tests run with and without the skill, and an independent review with every finding answered | 2, 4, 7, 8 | `lab/longrun/skill_gate.py` |
| **Reviews are scheduled by the system.** The agent is never relied on to call a reviewer | 4, 5 | The skill; already true of engine v3 and v4 |
| **Records are one line per event**, under 300 characters, at one path. The system measures their growth and stray paths | 5, 6 | The skill and `steps.py` |
| **Keep the step log with every run's results**, so the next analysis can see the movement cycle | 1 | Runner note in `lab/longrun/README.md` |

Not built here, and next: resuming a run from its files after a cutoff (cause 7). It needs the benchmark's own environment.

## Limits

- Nearly every long run used one model (Haiku 5.5) on one benchmark. Most comparisons rest on one to five seeds.
- Predictions were parsed from prose. The hand check found a few misreadings, and only primary claims were judged. Uncharted claims cannot be judged at all, which is the finding.
- "Acted on" means mentioned, not done.
- Run 4 kept no `metrics_system.md`, so its 13 predictions could not be judged.
- The analysis and the runs were made by the same project, and the scorer is new. Re-run it after any change to the records.

## Reproduce

```bash
cd results
python3 -I 2026-11-27-behavior-analysis/score_runs.py . 2026-11-27-behavior-analysis/scores.json
```
