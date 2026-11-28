# OBM skills vs Claude Code's native /plan and /goal, on Prosus Vending Bench

Every arm gets the benchmark's briefing, its 22 business tools and the same extra tools: a private workspace folder (Read, Write, Edit, Glob, Grep), sub-agents (Agent) and skills (Skill). Same model (Haiku 5.5) and seed. **There is no dollar cap unless `--budget` is given**; the account's usage limits still apply, and a cutoff is tagged as an environment failure, never as an agent stop. Per-job caps stay: the designer's set-up ($2), native's planning session ($3) and each review the engine runs (its budgets).

| Arm | Adds |
| --- | --- |
| `base` | Nothing |
| `native` | A planning session in Claude Code's plan mode, then the same session resumed with `/goal`: met only when a tool reports SIMULATION OVER. Plan mode blocks the benchmark's look-up tools, so the plan is made from the briefing alone |
| `native_cadence` | `native`, with the system running the same reviews as the cadence arms, with plain prompts and no OBM skills |
| `obm` | The OBM swarm skills installed; told to run the business as a one-agent OBM swarm |
| `obm_enf` | `obm` plus `vb_stop_gate2.py`, a Stop hook that reads the simulator's own state and refuses to stop before the last day |
| `obm_cadence` | The system runs the review cadence (engine v1), with the stop gate |
| `obm_v2`, `obm_v3` | Engines v2 (experiments, opportunity reviews) and v3 (the Strategist) |
| `obm_v4` | Engine v4: separate risk and improvement branches, the fact register from every action, the request ledger, the Organizer, and change verdicts judged by the system ([`../longrun/verify.py`](../longrun/verify.py)). The operator uses the orchestrator skill |
| `obm_v5` | `obm_v4`, with the operator on the [`obm-long-run`](../../skills/obm-long-run/SKILL.md) skill instead of the orchestrator's (which is not installed, so the model has one way to run the work), and the system's step cues on |

## Flags

| Flag | Default | What it does |
| --- | --- | --- |
| `--budget USD` | none | A dollar cap on the operator's sessions. Without it, only the usage limits and the per-job caps bound spend |
| `--timeout S` | 21600 | The harness's wall clock, for a hung run. A year at v3's pace takes about 7,000 s |
| `--steps observe\|cue\|off` | `cue` for `obm_v5`, else `observe` | Every arm's tool calls are recorded to `<out>/steps.jsonl` by [`../longrun/steps_hook.py`](../longrun/steps_hook.py), and `result.json` gets the behaviour summary. `cue` also hands the agent the step cues, so it is an intervention |

`result.json` also records `budget_usd`, `steps_mode`, the step summary (`steps`) and, for engine v4, the change verdicts (`change_verdicts`: judged, as predicted, expected by chance, the wrong way, could not judge).

## Before a run

The runner and the hooks run from copies on the run machine: the repo's `lab/` at `/home/claude/obm-lab` and its `skills/` at `/home/claude/obm-skills/skills`. Copy both before every batch. The preflight then refuses to start, before creating anything, if the copy lacks what the arm needs. That covers the hook scripts, the engine, the verifier (engine v4 is imported to check it can load it) and each skill the arm installs. Otherwise those failures are silent: the engine would run without verdicts, and a missing hook file errors without stopping the run.

```bash
python3 -I test_run_arms2.py      # every arm's launch, dry: no simulator, no model, no spend
```

The dry run imports this runner and fakes only the simulator and the Claude CLI. It checks each arm's flags, skills, hooks and engine configuration, runs each step hook command as written, and checks that the preflight refuses a broken copy.

## History

The first smoke test (5 simulated days) had four arms, all of which completed: the OBM arms loaded the skills and built `swarm/`, and the native arm planned and then ran under `/goal`. Each run also records stocked slots per day (to catch targets acting as a ceiling) and revenue by quarter (to catch drift).
