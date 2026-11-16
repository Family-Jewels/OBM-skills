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
