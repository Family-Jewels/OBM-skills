# Cadence engine: the system invokes the roles

In long runs, roles told to call each other stop doing it within days. This engine takes the schedule away from the agents. It is task-agnostic: it knows periods, named measures, rules for when to act, and the skills. Everything about a particular task lives in a small adapter.

Each time the engine runs (once per period of the work), it:

1. **Measures and charts.** Asks the adapter for this period's ground-truth measures, appends them to `swarm/metrics_system.md`, and rewrites `swarm/charts.md` (`charts.py`): process behavior charts whose limits are computed from each measure's own data (centre ± 2.66 × average moving range), the signals (a point beyond a limit, or 8 in a row on one side), the gap to an exemplar (PIP) and the swarm's own best. Both files are written only by the system. A signal in the wrong direction triggers an audit. When a redesign is adopted, the old limits are kept to test it.
2. **Runs a pulse review** every `pulse_every` periods: the auditor's short look at the numbers, ending in at most three pivots. This is the director's close ear on how the numbers are moving.
3. **Runs a full audit** every `audit_every` periods, or at once when a signal fires (a measure outside its limits).
4. **Runs the diagnostician** when a review says a diagnosis is needed (a chart signal in the wrong direction, a redesign whose predicted shift did not appear, or a large gap to the exemplar with no improvement). It reports what is wrong and why, and changes nothing.
5. **Calls the designer back to redesign** from the diagnosis: the smallest versioned change to the spec, driver tree or rules, with a redesign record that predicts which charted measure will shift.
6. **Hands the results to the orchestrator** as additional context on the hook event, so they cannot be skipped. Reviews run in the background while the work continues, and their findings arrive at the first period after they finish, like a report that lands the next morning. A run of 365 periods otherwise spent more time waiting on reviews than working.
7. **Spaces out redesigns.** At least `min_periods_between_redesigns` (default 20) between them, so each one's effect can be measured; in between, pulses give pivots.

## Using it on a task

Write an adapter: a class whose `read()` returns `{"period": int, "over": bool, "measures": {name: number}}` from ground truth (a state file, a database, a test run, a ledger), never from an agent's report. Then write a config and run the engine as a hook on whatever marks the end of a period.

```json
{
  "workspace": "/path/to/work", "log": "/path/to/cadence.jsonl",
  "adapter": "adapters.vending:VendingState", "adapter_args": {"state_path": "/path/to/state.json"},
  "unit": "day", "horizon": 365, "pulse_every": 5, "audit_every": 50, "model": "claude-haiku-5-5",
  "hook_event": "PostToolUse",
  "signals": [{"measure": "revenue", "op": "==", "value": 0, "periods": 2, "not_before": 8, "label": "revenue zero two days running"}],
  "budgets": {"pulse": 0.6, "audit": 1.5, "diagnosis": 1.0, "redesign": 1.5}, "min_periods_between_redesigns": 20
}
```

| Task | Period | Measures from ground truth | Hook |
| --- | --- | --- | --- |
| Vending Bench (`adapters/vending.py`) | A simulated day | Cash, revenue, units, slots selling, revenue over 7 days | PostToolUse on the day-advance tool |
| A software build (example) | A cycle, or a merged task | Tests passing, criteria met, spend, review share | PostToolUse on the board's status change, or a timer |
| Research or writing (example) | A section or a work session | Claims sourced, sections done, open questions | A timer |

## Version 1.1: a curated environment around a fully autonomous agent

`engine_v11.py`, arm `obm_v11` in `lab/vending2/run_arms2.py`, skills in `skills/` on this branch (v1's skills, changed as
below; v1 itself is unchanged on `skills-v1`). It tests the autonomy question from the other side: v2 to v4 added rules,
controls and gates, and results fell. v1.1 keeps v1's loop and gives the agent full autonomy inside a curated
environment. The requirements are in the "Operating Environment Requirements" doc (R1 to R12).

- **The designer owns everything task-specific (R12).** Before the run the engine writes `swarm/system_interface.md` from
  the adapter (`--interface`): the measures, resources and capacity it reports, and the formats. The designer reads it,
  the task's briefing and the human's requirements (`swarm/requirements.md`), and writes `swarm/spec.md`,
  `swarm/system.json` (charts, signals, opportunities, exemplar, cadence) and the first guidance. The engine and the
  harness carry no charts, signals or exemplar of their own. Bad entries in `system.json` are dropped and logged.
- **Guidance, never orders (R1).** `swarm/guidance/G-NNN.md`: what good looks like, why, when it applies (an opportunity
  or always), its source and a revisit point. Nothing assigns, requires, forbids, blocks or caps an action.
- **A hand-off every period (R2, R3, R8).** The engine runs as a PreToolUse hook on the period-ending tool (`--pre`: the
  state as the agent ends its period) and as the PostToolUse hook. The note gives the capacity used in the period that
  ended, the opportunities open at its end and now, the guidance that fits (at most five; text the first time, then a
  path), and anything new. It is also kept in `swarm/handoff.md`.
- **Reviews change the environment (R4, R7).** Pulses, audits and redesigns propose guidance in
  `swarm/guidance/proposed/`. A fact check (the checker, `C-NNN`) tests each against `metrics_system.md` and the state
  snapshots in `swarm/ground_truth/`, and refutes any that is not advice. Accepted entries enter the library; refuted ones
  are kept with the reason.
- **The agent's own policies are checked, not adopted (R5).** When files the agent wrote change (default every 5
  periods), the fact check quotes its policies and beliefs and checks their facts. Results go to
  `swarm/checks/policies.md` and to the agent's next note.
- **Reviews on what the agent does (R6).** A pulse starts when a period ended with at least half its capacity unused and
  an opportunity open, on repeated early ends, or on a statement the ground truth refutes, at most every 3 periods. The
  5-period pulse and 50-period audit remain as a backstop. Each delivery logs its lag from the event.
- **Behavior and cost as information (R9, R11).** Capacity used, opportunities open when each period ended, the agent's
  context size and each role's cost go into `metrics_system.md` and `charts.md`. They never trigger a redesign.
- **Any model in any role (R10).** `role_models` sets a model per role, and `runner` replaces the `claude -p` command
  with any command template (`{prompt}`, `{model}`, `{budget}`, `{turns}`).

Not built: a fresh working session each period (R8 asks that it be possible; the hand-off is written to allow it). The
harness's Stop gate stays as in v1: it refuses to end the whole task before the task is over, and never stops a period
from ending. Tests: `python3 -I lab/cadence/test_engine_v11.py` (a made-up task, roles stubbed).

## Version 2: the improvement half

Set `"version": 2` in the config to use `engine_v2.py` (the plain, no-skills arm stays on v1). v1 is unchanged and kept on the branch `skills-v1`.

- **The adapter states the task's facts** in a `spec()` method: horizon, natural cycle, clock, goal (a target, or maximize with a ceiling), each measure's kind (flow or level) and better direction, resources and guardrails. Each reading adds resources in use. See [`ADAPTER_SPEC.md`](ADAPTER_SPEC.md). A preflight checks the adapter on the first reading.
- **Progress (`progress.py`):** a point window derived from the adapter (the shortest span of whole cycles holding at least 3 observations that leaves at least 12 points); celeration per measure from a median-based log-scale fit (quarter-intersect up to 7 points, then Theil-Sen), with its range, bounce, own best, phases, jump and turn; the top measure's floor line and stretch aim; resources in use and idle; guardrails; experiments judged on the system's data. All of it is appended to `swarm/charts.md`.
- **Intervals in points:** a pulse every point (every second point after three quiet pulses); full audits at each quarter of the horizon; an opportunity review every 3 points without one, or when the top measure has 3 points in a row below its floor line or a flat or wrong-way celeration, waiting while an experiment runs but never more than 6 points; pulses and full audits run side by side; redesigns at least 3 points after the last design change. Setting up an experiment does not start a new phase.
- **Tests and replay:** `python3 -I test_progress.py` checks the celeration math. `python3 -I replay.py <run folder> <scratch folder>` replays a recorded run through v2 with no model calls and prints what it would have triggered and when.

### Experiments (`experiments.py`)

No role judges its own work. The designer writes an experiment with a recorded driver, a slice of the units and the rest as control; the orchestrator makes the change and writes `Applied`; the system calls the checker for a fidelity check against its ground-truth snapshots, and the clock starts only when it passes; experiments with overlapping slices queue; at the end the system compares slice against control on the driver (or the driver against its own earlier line) and reads the effect against the earlier bounce; the system calls the auditor for the verdict (keep, revert, too small to read) and writes it into the experiment file; the orchestrator applies it. `python3 -I test_experiments.py` tests the lifecycle, and `python3 -I test_engine_v2.py` runs the whole engine on a synthetic task in dry-run mode.

## Version 3: the Strategist

Set `"version": 3` (arm `obm_v3`). Same engine file as v2, with experiments and opportunity reviews switched off. The system calls the Strategist (`obm-swarm-strategist`) after the first 3 points and every 3 points, brought forward after at least 2 when the top measure has 3 points below its floor line or a flat or wrong-way celeration. Right after each strategy it calls the designer in AIM UPDATE mode to rewrite `swarm/aims.md`, in its own lane, not held back by redesign spacing. An aim update that ends `Design change needed: yes` queues a redesign behind any fault diagnosis; deferred diagnoses queue instead of being dropped. `ENGINE_VERSION=3 python3 -I replay.py <run> <scratch>` replays a recorded run through v3.
