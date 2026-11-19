# Adapter spec (engine version 2)

The adapter is the contract between a task and the system. It is code, written once per task, and agents never fill it in. Every aim, chart, interval and trigger is derived from it, so a human signs it off before any run.

An adapter is a class with two methods.

## `spec()`: facts about the task

| Key | What it defines | Vending Bench | A software build (example) |
| --- | --- | --- | --- |
| `unit` | The name of one period | `"day"` | `"session"` |
| `horizon` | The deadline or budget, in clock units | 365 | 60 |
| `cycle` | The task's repeating rhythm, in clock units: a point holds whole cycles | 7 (demand has a day-of-week pattern) | 1 |
| `clock` | `"period"` (calendar) or `"budget"` (spend, read from `clock` in each reading) | `"period"` | `"budget"` |
| `top` | The measure the goal is judged on | `"cash"` | `"tests_passing"` |
| `goal` | `{"type": "target" or "maximize", "value": number, "source": text}`; for maximize, `value` is the best known ceiling | maximize; ceiling 61,219 (the reference operator) | target: every hidden test |
| `measures` | Each measure with `kind` (`"flow"`: an amount per period, or `"level"`: a positive stock) and `better` (`"up"`/`"down"`); optional `from` | cash (level), revenue, units, revenue per slot (flows), slots selling (level) | tests passing (level), tests newly passing (flow) |
| `resources` | The names of the resources each reading reports | slots stocked at day end, capital | agent hours, budget |
| `capacity` | Required: the name of the resource that is the worker's own capacity (time, actions or budget per period), reported in every reading. Every task, fix and experiment draws on it | worker time, 480 minutes a working day, read from the simulator's clock before each day ends | agent hours or budget per session |
| `resource_sources` | Optional: how each resource is measured, shown under the resources table so reviewers know it is ground truth | the simulator clock, machine state, balance | the harness budget meter |
| `experiment_share` | The share of capacity experiments may use together (default 0.10) | 0.10 | 0.10 |
| `guardrails` | `{measure, min or max, label}`: a side not to cross; experiments stay inside | cash ≥ 120 (ten days of fees, the limit before termination) | no test files edited (count = 0) |
| `unit_name`, `unit_measures` | Optional: the units experiments can be sliced by, and the measures recorded per unit | machine; machine_revenue, machine_units, machine_stocked_slots | module; tests passing per module |

## `read()`: one reading per period, from ground truth

```python
{"period": int, "over": bool,
 "clock": number,                      # only when clock is "budget"
 "measures": {name: number},           # from the task's own state, never from an agent's report
 "units": {unit_id: {measure: number}}, # optional: per-unit measures, for slice-against-control experiments
 "resources": {name: {"used": number, "available": number}}}
```

## `snapshot()`: optional, for experiment fidelity

Returns text (markdown) of the ground truth the swarm controls: every lever an experiment could pull, such as each slot's product, price and stock, and each marketing campaign. A lever missing from the snapshot cannot be checked, so an experiment using it cannot start. The system saves one each period in `swarm/snapshots/`, and the checker compares them to confirm an experiment's change was made as written, on its slice only.

## What the system derives from it

- **The point window** (`progress.derive_window`): the shortest span that holds whole cycles and at least 3 observations while leaving at least 12 points across the horizon. Vending gives 7 days. A 60-session build with a cycle of 1 gives 3 sessions. If no window fits, the horizon is too short for celeration and only level charts run.
- **Every interval, counted in points:** a pulse every point (every second point after three quiet pulses), redesigns at least 3 points after the last adoption, an opportunity review every 3 points without one (not while an experiment runs), full audits at each quarter of the horizon.
- **The floor line** from the top measure's level after 3 points to the goal at the horizon, and **the aim**: the same goal by half the remaining horizon, raised toward double whenever met on 2 of the last 3 points.

## Preflight

On its first reading, the engine checks the adapter and logs any problem (`event: preflight`) and hands it to the orchestrator:

1. a horizon exists, and the top measure is one of the measures;
2. a goal value or ceiling exists, so the floor and aim lines can be drawn;
3. every measure returns a number, and none is negative (celeration needs a positive flow or level);
4. every resource reports an available amount above zero, and the capacity resource is declared and reported;
5. every guardrail has a side;
6. the horizon is long enough for celeration.

A human signs the adapter off after a clean preflight. During the run, the designer reads it and flags gaps but cannot edit it, and each full audit asks whether the measures still track the goal.
