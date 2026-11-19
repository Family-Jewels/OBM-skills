# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 83 | 562.94 | 358.39 | 767.5 (provisional) | 491.4 | routine variation |
| revenue | up | 83 | 94.09 | -46.16 | 234.34 (provisional) | 5.3 | routine variation |
| slots_selling | up | 83 | 11.44 | 5.13 | 17.76 (provisional) | 3 | WORSE: beyond the lower limit |
| revenue_per_slot | up | 83 | 7.45 | -1.75 | 16.65 (provisional) | 1.77 | routine variation |
| units | up | 83 | 45.0 | -27.15 | 117.15 (provisional) | 3 | routine variation |

## Since redesign R-O-002 (adopted day 83): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 295.05 (7.6 to 582.51) | 562.94 | 9 | shift up: 8 in a row above the centre |
| revenue | 72.1 (-120.12 to 264.32) | 94.09 | 9 | no shift yet |
| slots_selling | 9.75 (-2.15 to 21.65) | 11.44 | 9 | no shift yet |
| revenue_per_slot | 6.37 (-4.41 to 17.14) | 7.45 | 9 | no shift yet |
| units | 34.5 (-52.72 to 121.72) | 45.0 | 9 | no shift yet |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 91: actual 3722.66, exemplar 13787.56 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 5.5: the exemplar has gained 5.5x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 607.16 | 607.16 |
| revenue | 141.46 | 80.37 |
| slots_selling | 14.43 | 9.86 |
| revenue_per_slot | 9.49 | 7.16 |
| units | 63.71 | 39.29 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 13 points across the horizon of 91.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 12). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 2 | collecting | | | x1.04 | collecting |
| revenue | flow | up | 2 | collecting | | | /1.10 | collecting |
| units | flow | up | 2 | collecting | | | /1.15 | collecting |
| slots_selling | level | up | 2 | collecting | | | /1.14 | collecting |
| revenue_per_slot | flow | up | 2 | collecting | | | /1.05 | collecting |
| unit_cost_paid_30d | level | down | 2 | collecting | | | /1.01 | collecting |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.48 per point from point 3. Aim line (a deliberate overshoot: 61,219 by half the remaining horizon): x2.20 per point from point 3. Falling short of the aim is expected and triggers nothing.

Latest point 13 (days 85-91): 3,722.66; floor line 61,219.00; aim line 61,219.00. Required celeration from here to the target: x16.44; actual (this phase): collecting.

## Since the phase change at point 12

Jump (first point / old line projected): x1.17. Turn (new celeration / old): needs 3 points in the new phase.

## Resources (used / available, written by the system)

| resource | used | available | in use | idle |
| --- | --- | --- | --- | --- |
| slots stocked at day end | 2 | 72 | 3% | 70 |
| capital | 35.36 | 3638.02 | 1% | 3602.66 |

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 3722.66 | ok |

## Units (for experiment slices; latest point, median per day)

| unit | machine_revenue | machine_units | machine_stocked_slots |
| --- | --- | --- | --- |
| AI-HOUSE:DRINKS | 5.0 | 2 | 1 |
| AI-HOUSE:SNACK | 21.3 | 12 | 1 |
| AI-LOUNGE:DRINKS | 0.0 | 0 | 0 |
| AI-LOUNGE:SNACK | 12.5 | 7 | 2 |
| MAIN-LOUNGE:DRINKS | 0.0 | 0 | 0 |
| MAIN-LOUNGE:SNACK | 23.2 | 12 | 2 |

## Experiments (run and judged by the system; verdicts by the auditor)

Lifecycle: planned, queued (its slice overlaps a running one), fidelity (the checker is verifying the change), running (the clock started when fidelity passed), verdict (the auditor is ruling), done. Effect: the driver after the start divided by its expected value (slice against control where the driver is measured per unit); read against the envelope of the earlier bounce.

| experiment | driver | slice | start | end | clock started | state | effect | envelope | reading |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E-001 | machine_revenue | AI-HOUSE:SNACK | 7 | 28 | — | void |  | | |
| E-002 | machine_units | MAIN-LOUNGE:DRINKS, MAIN-LOUNGE:SNACK | 14 | 35 | — | void |  | | |
| E-003 | slots_selling | AI-HOUSE:DRINKS, AI-HOUSE:SNACK | 33 | 54 | — | void |  | | |
