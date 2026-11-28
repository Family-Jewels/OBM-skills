# Vending Bench, v4 and v5: plan and decision rules, set before the runs (2026-11-28)

Written before any run, as the five-seed test was. Results go in this folder's README when they exist.

## The arms

Both arms use Haiku 5.5 with the stop gate. There is no dollar cap, but the account's usage limits apply. The harness clock is 6 hours.

| Arm | Engine | The operator's skill | Step record |
| --- | --- | --- | --- |
| `obm_v4` | v4: two branches, fact register, request ledger, Organizer, **change verdicts by the system** | `obm-swarm-orchestrator` | Recorded, no cues (`observe`) |
| `obm_v5` | The same | **`obm-long-run`** (the orchestrator's skill is not installed) | Recorded, **cues on** (`cue`) |

The two arms differ only in the operator's skill and the step cues. So v5 against v4 measures the long-run skill and cues together, not each one alone. Separating them would need a third arm (v4 with cues).

## Sequence

1. **Smoke runs, seed 6, 91 days** (outside the test seeds): `obm_v4`, then `obm_v5`. At v3's pace a 91-day run costs about $10, so both should fit in one usage window. Seeds start only when every check below holds for both arms. If one fails, it is fixed and smoked again, and no seed is spent on a known defect.
   - The preflight passed, and the engine's first event says `verification: true`.
   - All 91 days completed.
   - Every adopted method change was either registered with a machine-readable prediction, or got a request to restate it, which was answered. At least one verdict appeared, if a change was adopted before about day 70.
   - `steps.jsonl` has a line for nearly every tool call: within 5% of `tool_calls` in `result.json`.
   - The progress log is at `swarm/log/progress.md`, with no writes outside the workspace.
   - In v5 the cues fired, but not on most steps. If they fire on more than about one step in ten, the thresholds are tuned before seeds.
   - Cost per simulated day is recorded, to size the seed batches against the usage windows.
2. **Seeds 1 to 5, 365 days**, alternating arms by seed (v4 s1, v5 s1, v4 s2, ...). A change in the environment mid-batch then falls on both arms, not one. At v3's pace a year costs about $38 and takes about 2 hours, which is roughly one usage window per run.

## Cutoffs

A run cut off by a usage limit is an environment failure. It is not scored: it is rerun on the same seed in the next window (resume is not built yet). If more than 3 of the 10 seed runs are cut off, the batch pauses so we can decide between building resume, using a shorter horizon or billing through the API.

## Decision rules

| Question | Rule |
| --- | --- |
| **Primary: does v5 beat v4?** | v5 counts as better if it wins **at least 4 of 5 seeds** (paired by seed) **and the mean paired gain is above zero**. This is the rule the five-seed test used. The exact sign-flip p is reported |
| **Floor: is each arm safe?** | An arm counts as safe only if **no run ends below €13,435**, v1's worst five-seed run |
| Against earlier versions | Descriptive only: v1's five seeds (mean €13,955), plain /plan + /goal (mean €13,302), and v3 seed 1 (€27,938 at day 343). No rule |
| Cost | Dollars per euro gained, per arm. No rule |

Reported for both arms, with no rule. They describe how the result was reached:

- **The movement cycle**, from `steps.jsonl`: share of unchanged re-reads, repeated failures, retries unchanged, the longest stretch with no state change, bytes written to the operator's own log per day, writes outside the workspace, and (v5) the cues raised by kind.
- **Change verification**, from `change_verdicts`: changes judged, how many shifted as predicted against the number expected by chance, how many went the wrong way, and how many could not be judged as written. The earlier skills arms came true 15 of 38 times against 11.9 by chance.
- **The driver**: stocked slots a day. Across 17 earlier full-year runs it tracked the final balance (r = 0.95).

## Commands

Copy the repo's `lab/` to `/home/claude/obm-lab` and its `skills/` to `/home/claude/obm-skills/skills` first. The runner refuses to start if anything it needs is missing.

```bash
python -I /home/claude/obm-lab/vending2/run_arms2.py --arm obm_v4 --seed 6 --days 91 --output RUNS
python -I /home/claude/obm-lab/vending2/run_arms2.py --arm obm_v5 --seed 6 --days 91 --output RUNS
# after the smoke checks pass:
for s in 1 2 3 4 5; do
  python -I /home/claude/obm-lab/vending2/run_arms2.py --arm obm_v4 --seed $s --days 365 --output RUNS
  python -I /home/claude/obm-lab/vending2/run_arms2.py --arm obm_v5 --seed $s --days 365 --output RUNS
done
python3 -I results/2026-11-27-behavior-analysis/score_runs.py RUNS RUNS/scores.json
```
