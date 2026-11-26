# System interface (written by the system; do not edit)

The work runs in days, 30 in all. At the end of every day the system reads the task's own state (ground truth, never an agent's report), charts it, and hands the working agent a short note. You decide, in swarm/system.json, what it charts, what pulls a review early, what counts as an opportunity, and the exemplar.

## Measures the system reads every day

| measure | kind | better |
| --- | --- | --- |
| cash | level | up |
| revenue | flow | up |
| units | flow | up |
| slots_selling | level | up |
| revenue_per_slot | flow | up |
| unit_cost_paid_30d | level | down |
| units_in_storage | level | down |

## Resources (used and available, every day)

- `worker time (minutes a day)`  (the working agent's own capacity): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used)
- `slots stocked at day end`: the simulator's machine state
- `capital`: the simulator's balance and the cost of stock on hand

## Goal as the task states it

maximize cash

## swarm/system.json

```json
{
 "charts": [
  {
   "name": "<a measure above, or a new name>",
   "from": "<measure>",
   "diff": "<optional: change over this many periods>",
   "better": "up|down"
  }
 ],
 "signals": [
  {
   "measure": "<measure>",
   "op": "== | < | <= | > | >= | !=",
   "value": 0,
   "periods": 2,
   "not_before": 8,
   "label": "<why this matters>"
  }
 ],
 "opportunities": [
  {
   "id": "O1",
   "label": "<what is open, in the task's own words>",
   "when": [
    {
     "resource": "<resource>",
     "unused_at_least": 1
    },
    {
     "resource": "<resource>",
     "unused_share_at_least": 0.3
    },
    {
     "measure": "<measure>",
     "op": ">",
     "value": 0
    }
   ]
  }
 ],
 "exemplar": {
  "measure": "<measure>",
  "points": {
   "0": 0,
   "<period>": 0
  },
  "origin": 0,
  "source": "<where it comes from>"
 },
 "cadence": {
  "pulse_every": 5,
  "audit_every": 50,
  "min_periods_between_redesigns": 20,
  "check_every": 5,
  "event_min_gap": 3,
  "early_end_unused_share": 0.5,
  "repeated_early_ends": 3,
  "repeated_window": 5,
  "not_before": 3
 }
}
```

Use measure and resource names exactly as listed above. Every condition in an opportunity's `when` must hold for it to show as open. Opportunities are information: the system never ranks, assigns or requires them. Cadence keys you leave out keep the defaults shown.

## A guidance entry (swarm/guidance/G-NNN.md; later ones go to swarm/guidance/proposed/)

```markdown
# <short title>
Applies when: always | <opportunity ids, comma-separated>
What good looks like: <advice, a guideline or an example>
Why: <the reason and the evidence>
Source: <brief | review or diagnosis id>
Revisit: day <N>
```

A proposal may add `Revises: G-NNN` or `Retires: G-NNN`. Guidance is never an instruction: it never requires, forbids or caps an action.
