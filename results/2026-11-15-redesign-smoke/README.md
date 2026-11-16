# Redesign loop smoke test (2026-11-15)

A 12-day obm_cadence run (seed 1, Haiku 5.5) with the new loop: the designer set KPIs per initiative, the system measured every day, and a pulse ran every 5 days. Final balance €1,641.90 (12 days is too short to score; this checks the wiring).

- `P-001.md`: the pulse judged each KPI against its target and limits, found revenue outside its limits, and asked for a diagnosis.
- `D-P-001.md`: the diagnostician named the cause (a 7-day supplier lead time the design never required checking, and no ground-truth column for pending orders) and what the design would need to change, without writing a fix.
- `R-P-001.md`: the designer, run on a copy of the workspace from that diagnosis, kept the direction and changed one rule. It saved the new version beside the old, which the orchestrator would not have read; the skill and engine now keep the current version at its usual path and move old versions to `swarm/history/`.

## Charts version, 25 days (`charts-25d/`)

The same arm after KPIs were replaced by a driver tree, process behavior charts and PIP. Final balance €1,935.44 (wiring check, not a score).

- The designer built a driver tree from the final balance down to slots selling, sales per slot, margin and landed cost, and marked landed cost as needing instrumentation rather than letting the operator report it.
- Four pulses, no diagnoses. Each pulse separated signals from routine variation and declined to react to the latter; the day-20 pulse reported cash gained over 7 days beyond its upper limit as an improvement. Under the KPI version, the day-5 pulse had called a diagnosis on start-up zero revenue.
- Limits computed from the early weeks are wide, because they include the start-up ramp; they narrow as phases reset.
