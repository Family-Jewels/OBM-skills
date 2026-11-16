# Cadence engine: the system invokes the roles

In long runs, roles told to call each other stop doing it within days. This engine takes the schedule away from the agents. It is task-agnostic: it knows periods, named measures, rules for when to act, and the skills. Everything about a particular task lives in a small adapter.

Each time the engine runs (once per period of the work), it:

1. **Measures.** Asks the adapter for this period's ground-truth measures and appends them to `swarm/metrics_system.md`, a file only the system writes.
2. **Runs a pulse review** every `pulse_every` periods: the auditor's short look at the numbers, ending in at most three pivots. This is the director's close ear on how the numbers are moving.
3. **Runs a full audit** every `audit_every` periods, or at once when a signal fires (a measure outside its limits).
4. **Runs the diagnostician** when an audit says a diagnosis is needed, or when the same problem shows in two pulses running.
5. **Hands the results to the orchestrator** as additional context on the hook event, so they cannot be skipped. Reviews run in the background while the work continues, and their findings arrive at the first period after they finish, like a report that lands the next morning. A run of 365 periods otherwise spent more time waiting on reviews than working.
6. **Spaces out rule changes.** At least `min_periods_between_diagnoses` (default 21) between changes, so each one's effect can be measured; in between, pulses give pivots.

## Using it on a task

Write an adapter: a class whose `read()` returns `{"period": int, "over": bool, "measures": {name: number}}` from ground truth (a state file, a database, a test run, a ledger), never from an agent's report. Then write a config and run the engine as a hook on whatever marks the end of a period.

```json
{
  "workspace": "/path/to/work", "log": "/path/to/cadence.jsonl",
  "adapter": "adapters.vending:VendingState", "adapter_args": {"state_path": "/path/to/state.json"},
  "unit": "day", "horizon": 365, "pulse_every": 7, "audit_every": 30, "model": "claude-haiku-5-5",
  "hook_event": "PostToolUse",
  "signals": [{"measure": "revenue", "op": "==", "value": 0, "periods": 2, "not_before": 8, "label": "revenue zero two days running"}],
  "budgets": {"pulse": 0.6, "audit": 1.5, "diagnosis": 1.5}
}
```

| Task | Period | Measures from ground truth | Hook |
| --- | --- | --- | --- |
| Vending Bench (`adapters/vending.py`) | A simulated day | Cash, revenue, units, slots selling, revenue over 7 days | PostToolUse on the day-advance tool |
| A software build (example) | A cycle, or a merged task | Tests passing, criteria met, spend, review share | PostToolUse on the board's status change, or a timer |
| Research or writing (example) | A section or a work session | Claims sourced, sections done, open questions | A timer |
