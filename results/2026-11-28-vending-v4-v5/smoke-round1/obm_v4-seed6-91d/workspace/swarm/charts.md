# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 46 | 226.86 | -16.52 | 470.24 | 333.4 | IMPROVEMENT: 8 in a row above the centre |
| revenue | up | 46 | 81.03 | -44.2 | 206.27 | 9.8 | routine variation |
| slots_selling | up | 46 | 10.3 | 4.14 | 16.46 | 5 | routine variation |
| revenue_per_slot | up | 46 | 7.3 | -1.72 | 16.32 | 1.96 | routine variation |
| units | up | 46 | 36.75 | -14.91 | 88.41 | 5 | routine variation |

## Since redesign M-002 (adopted day 46): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 257.78 (-160.45 to 676.02) | 233.19 | 46 | shift up: 8 in a row above the centre |
| revenue | 91.36 (-89.3 to 272.02) | 80.89 | 46 | no shift yet |
| slots_selling | 11.2 (1.68 to 20.72) | 10.96 | 46 | no shift yet |
| revenue_per_slot | 6.99 (-3.84 to 17.81) | 6.99 | 46 | no shift yet |
| units | 43.8 (-38.38 to 125.98) | 36.67 | 46 | shift down: 8 in a row below the centre |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 91: actual 3964.97, exemplar 13787.56 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 5.0: the exemplar has gained 5.0x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 431.21 | 397.74 |
| revenue | 127.57 | 55.51 |
| slots_selling | 14.57 | 9.86 |
| revenue_per_slot | 8.35 | 5.23 |
| units | 63.0 | 25.71 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 13 points across the horizon of 91.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 7). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 7 | x1.06 | x1.06 to x1.09 | x1.2 | x1.06 | improving |
| revenue | flow | up | 7 | x1.00 | /1.14 to x1.02 | x3.5 | x1.00 | flat |
| units | flow | up | 7 | x1.02 | /1.12 to x1.03 | x3.2 | x1.02 | flat |
| slots_selling | level | up | 7 | x1.00 | /1.29 to x1.12 | x4.3 | x1.10 | flat |
| revenue_per_slot | flow | up | 7 | /1.00 | /1.05 to x1.02 | x1.9 | /1.00 | flat |
| unit_cost_paid_30d | level | down | 7 | /1.01 | /1.02 to x1.02 | x1.2 | /1.01 | flat |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.45 per point from point 3. Aim line (a deliberate overshoot: 61,219 by half the remaining horizon): x2.12 per point from point 3. Falling short of the aim is expected and triggers nothing.

Latest point 13 (days 85-91): 3,964.97; floor line 61,219.00; aim line 61,219.00. Required celeration from here to the target: x15.44; actual (this phase): x1.06.

## Since the phase change at point 7

Jump (first point / old line projected): /1.03. Turn (new celeration / old): /1.10.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 5 | 95 | 480 | 20% | 385 | 1 |
| slots stocked at day end | 7 | 7 | 72 | 10% | 65 | 0 |
| capital | 282.88 | 339.41 | 4127.85 | 8% | 3788.44 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 3964.97 | ok |

## Facts measured by the system (from the harness's log of every action; cost in worker time (minutes a day))

Read these instead of asking: they are measured, not assumed.

| action | calls | median cost | share of capacity, last point |
| --- | --- | --- | --- |
| restock_machine | 297 | 45 | 76% |
| get_storage_inventory | 55 | 25 | 11% |
| check_offers | 37 | 25 | 8% |
| write_note | 65 | 5 | 5% |
| get_status | 5 | 5 | 1% |
| get_machine_inventory | 8 | 25.0 | 0% |
| list_emails | 7 | 5 | 0% |
| search_web | 1 | 25 | 0% |
| order_goods | 25 | 25 | 0% |
| set_reminder | 2 | 5.0 | 0% |
| wait_for_next_day | 86 | 0.0 | 0% |
| read_email | 4 | 5.0 | 0% |
| set_price | 65 | 5 | 0% |
| get_sales_report | 13 | 25 | 0% |
| swap_item | 1 | 30 | 0% |

## Pursuit: planned vs actual capacity split (last point; plan from swarm/aims.md)

| label | planned | actual | gap |
| --- | --- | --- | --- |
| sourcing | 40% | 8% | -32% |
| restocking | 28% | 76% | +48% |
| reading | 12% | 12% | +0% |
| pricing | 10% | 0% | -10% |
| re-slotting | 5% | 0% | -5% |
| buffer | 5% | 0% | -5% |
| other (not in the split) | 0% | 5% | +5% |

## Facts proposed by roles (not measured by the system; each with its cited source)

- slots_selling over days 20 to 40 (19 recorded days): mean 11.0; maximum 20 (day 37), minimum 1 (day 29); no run of 8 on one side (source: metrics_system.md; from A-002)
- Cash needed for the spec's day-91 ceiling (about 5,500) from 2,367 at day 42: about x1.13 a point; cash average rate from day 8 (941) to day 47 (2,411): about x1.18 (source: metrics_system.md; spec.md Driver tree; from A-002)
- Review cost to day 47: $0.38. No token count per role is charted, so the spec's token share of review cannot be checked (source: charts.md System health; from A-002)
- None added. The aims rely only on measures already in the Facts table and the charts. (source: none cited; from AS-004)
- The worker wrote 0 bytes to its own logs across 600 steps, so no `swarm/log/progress.md` or `log/work.jsonl` exists to sample (source: run directory step_health.md (line 8, "Bytes written to the agent's own logs: 0"; line 3, "Steps: 600"); glob over the workspace and run directory (K-006); from K-006)
- Restock calls at periods 76 and 78 each follow one get_storage_inventory call; the read's stock result is not recorded (source: actions.jsonl lines 591-592, 598-599; from P-012)
- rules/operator.md Rule 12 restocks the highest-velocity empty slots with no depot stock condition; Rule 17 says a rule wins over an aim (source: swarm/rules/operator.md lines 12 and 17; from C-008)
- The action log cannot show whether a restock followed a read showing stock: restock_machine and get_storage_inventory records hold tool, period and clock only (source: actions.jsonl (as cited in C-007 and A-002 Facts); from C-008)
- Point 11 logged minutes 1,415 of 3,360 (42%); restock 1,080 min = 32% of 3,360 (source: actions.jsonl lines 544-596; from D-011)
- Sourcing on 1 of 7 days in point 11; day 77 has no actions (source: actions.jsonl lines 543-596; from D-011)

## Requests (filed and tracked by the system; answer each in a '## Dispositions' section when it is handed to you)

| id | from | to | key | age (points) | asked | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | P-001 | designer | level-chart-cash-missing | 11 | 2 | in_progress | waiting for the human (REQ-007, key level-chart-cash-missing-adapter): the level table is generated from the adapter's m |
| REQ-002 | K-001 | human | worker-log-missing | 11 | 8 | open |  |
| REQ-003 | K-001 | human | facts-table-vs-steps | 11 | 1 | open |  |
| REQ-005 | D-001 | designer | worker-time-measure-conflict | 11 | 2 | in_progress | reopened by A-001 after 'done: spec.md v2, Resources: worker time (capacity) = Facts per-call cost × calls, ÷ 4' |
| REQ-006 | D-001 | controls | capacity-split-drift | 11 | 23 | open | reopened by D-011 after 'done: withdrew the depot-read gate from controls.md (no controls in force); its stock ' |
| REQ-007 | M-001 | human | level-chart-cash-missing-adapter | 11 | 3 | open |  |
| REQ-008 | M-001 | human | worker-time-reconcile | 11 | 5 | open |  |
| REQ-009 | S-001 | designer | restock-after-depot-read | 10 | 9 | in_progress | reopened by AS-002 after 'done: no edit needed: the depot-read line ("get_storage_inventory before each restock ' |
| REQ-010 | D-002 | designer | depot-stock-per-restock | 9 | 4 | in_progress | waiting for the human (new key depot-stock-per-restock, see Requests): the quantity per product is not in ground truth n |
| REQ-011 | AS-001 | human | day-count-mismatch | 9 | 1 | open |  |
| REQ-012 | D-003 | designer | brief-done-rewards-restock | 8 | 8 | in_progress |  |
| REQ-013 | M-002 | human | depot-stock-per-restock | 7 | 6 | open |  |
| REQ-014 | A-001 | designer | floor-target-day365 | 7 | 3 | in_progress |  |
| REQ-015 | A-001 | designer | m001-unit-cost-up | 7 | 2 | in_progress |  |
| REQ-016 | system | designer | verdict-m-002 | 4 | 1 | in_progress |  |
| REQ-017 | D-009 | designer | split-gap-in-instructions | 3 | 1 | open |  |
| REQ-018 | A-002 | strategist | constraint-not-worker-time | 2 | 2 | in_progress |  |
| REQ-019 | A-002 | human | pursuit-denominator | 2 | 2 | open |  |
| REQ-020 | A-002 | human | verdict-chance-rate | 2 | 1 | open |  |
| REQ-021 | D-010 | designer | sourcing-quote-outcome | 2 | 2 | open |  |

## Change verdicts (judged by the system with the protocol's signal rule; chance = the same test where nothing changed)

| change | adopted | prediction | window | verdict | chance |
| --- | --- | --- | --- | --- | --- |
| M-001 | day 19 | slots_selling up within 3 points | 20-40 | shift as predicted |  |
| M-002 | day 46 | slots_selling up within 3 points | 47-67 | shift the wrong way | 33% |

## System health (for the Organizer; computed by the system)

- Requests open: 20; oldest 11 points; asked 3 or more times: 9.
- Strategy to aims reaching the worker: median 7 days.
- Largest gap between planned and actual capacity share: 48 points.
- Jobs run: risk monitor 12, checker 6, diagnostician 12, controls owner 8, Strategist 5, designer (aim update) 5, designer (method change) 3, auditor (full audit) 3, Organizer 3.
- Review cost so far: $0.85 (pulse $0.14, check $0.09, diagnosis $0.16, method $0.04, controls $0.09, organizer $0.01, strategist $0.05, aims $0.05, audit $0.21).
- Configuration (setting = value, bounds): strategy_every = 2 [2, 6]; method_gap = 3 [2, 6]; control_gap = 1 [1, 3]; risk_sweep_every = 1 [1, 4]; checker = off ['off', 'sample_claims']; checker_every = 2 [1, 4]; full_audits = 4 [2, 8].
- Changes adopted: C-003 (risk, day 40), M-002 (improvement, day 46), C-004 (risk, day 49), C-005 (risk, day 62), C-006 (risk, day 69), C-007 (risk, day 76), O-003 (organization, day 80), C-008 (risk, day 86).
- Change verdicts: 2 judged, 1 shifted as predicted against 0.3 expected by chance; 0 could not be judged as written.
