# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 59 | 244.55 | 95.89 | 393.21 | 359.96 | routine variation |
| revenue | up | 59 | 84.91 | -58.23 | 228.04 | 4.9 | routine variation |
| slots_selling | up | 59 | 14.2 | 2.16 | 26.24 | 3 | routine variation |
| revenue_per_slot | up | 59 | 5.34 | -0.75 | 11.42 | 1.63 | routine variation |
| units | up | 59 | 54.05 | -35.13 | 143.23 | 3 | routine variation |

## Since redesign R-O-001 (adopted day 59): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 59.35 (-59.34 to 178.04) | 275.01 | 32 | shift up: beyond the upper limit |
| revenue | 44.88 (-62.49 to 152.24) | 79.22 | 32 | no shift yet |
| slots_selling | 7.9 (-2.74 to 18.54) | 13.03 | 32 | no shift yet |
| revenue_per_slot | 4.47 (-1.86 to 10.8) | 5.28 | 32 | no shift yet |
| units | 29.9 (-40.52 to 100.32) | 49.94 | 32 | no shift yet |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 91: actual 3392.01, exemplar 13787.56 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 6.5: the exemplar has gained 6.5x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 358.5 | 310.48 |
| revenue | 107.69 | 63.7 |
| slots_selling | 17.0 | 10.71 |
| revenue_per_slot | 6.14 | 4.97 |
| units | 68.43 | 38.57 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 13 points across the horizon of 91.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 9). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 5 | x1.10 (provisional) | x1.09 to x1.11 | x1.1 | x1.07 | improving |
| revenue | flow | up | 5 | /1.16 (provisional) | /1.28 to /1.14 | x1.6 | x1.44 | wrong way |
| units | flow | up | 5 | /1.17 (provisional) | /1.28 to /1.13 | x1.7 | x1.44 | wrong way |
| slots_selling | level | up | 5 | /1.11 (provisional) | /2.06 to x1.41 | x139.8 | x2.08 | flat |
| revenue_per_slot | flow | up | 5 | /1.04 (provisional) | /1.14 to /1.02 | x1.6 | x1.22 | wrong way |
| unit_cost_paid_30d | level | down | 5 | x1.03 (provisional) | x1.03 to x1.03 | x1.0 | /1.01 | wrong way |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.45 per point from point 3. Aim line (a deliberate overshoot: 61,219 by half the remaining horizon): x2.10 per point from point 3. Falling short of the aim is expected and triggers nothing.

Latest point 13 (days 85-91): 3,392.01; floor line 61,219.00; aim line 61,219.00. Required celeration from here to the target: x18.05; actual (this phase): x1.10.

## Since the phase change at point 9

Jump (first point / old line projected): x1.15. Turn (new celeration / old): x1.02.

## Resources (used / available, written by the system)

| resource | used | available | in use | idle |
| --- | --- | --- | --- | --- |
| slots stocked at day end | 6 | 72 | 8% | 66 |
| capital | 49.44 | 3321.45 | 1% | 3272.01 |

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 3392.01 | ok |

## Units (for experiment slices; latest point, median per day)

| unit | machine_revenue | machine_units | machine_stocked_slots |
| --- | --- | --- | --- |
| AI-HOUSE:DRINKS | 6.0 | 4 | 1 |
| AI-HOUSE:SNACK | 8.91 | 6 | 1 |
| AI-LOUNGE:DRINKS | 6.3 | 3 | 4 |
| AI-LOUNGE:SNACK | 11.1 | 8 | 3 |
| MAIN-LOUNGE:DRINKS | 12.0 | 6 | 0 |
| MAIN-LOUNGE:SNACK | 5.2 | 4 | 1 |

## Experiments (run and judged by the system; verdicts by the auditor)

Lifecycle: planned, queued (its slice overlaps a running one), fidelity (the checker is verifying the change), running (the clock started when fidelity passed), verdict (the auditor is ruling), done. Effect: the driver after the start divided by its expected value (slice against control where the driver is measured per unit); read against the envelope of the earlier bounce.

| experiment | driver | slice | start | end | clock started | state | effect | envelope | reading |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E-001 | machine_revenue | AI-HOUSE:SNACK | 2 | 5 | 16 | done: too small to read | /1.13 | within x1.21 | too small to read: inside the earlier bounce |
| E-002 | machine_units | AI-LOUNGE:DRINKS, AI-LOUNGE:SNACK | 3 | 6 | — | void |  | | |
| E-003 | machine_revenue | MAIN-LOUNGE:DRINKS | 4 | 7 | — | void |  | | |
| E-005 | machine_revenue | AI-LOUNGE:DRINKS | 57 | 77 | — | fidelity |  | | |
