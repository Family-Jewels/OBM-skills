# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 315 | -42.09 | -130.11 | 45.92 | 120.77 | IMPROVEMENT: beyond the upper limit |
| revenue | up | 315 | 18.94 | -34.63 | 72.52 | 12.24 | routine variation |
| slots_selling | up | 315 | 2.35 | -1.43 | 6.13 | 5 | routine variation |
| revenue_per_slot | up | 315 | 5.64 | -5.66 | 16.94 | 2.45 | routine variation |
| units | up | 315 | 8.35 | -15.87 | 32.57 | 6 | routine variation |

## Since redesign R-P-014 (adopted day 315): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 131.76 (-75.51 to 339.04) | -9.62 | 51 | shift down: 8 in a row below the centre |
| revenue | 68.04 (-56.64 to 192.73) | 21.21 | 51 | no shift yet |
| slots_selling | 7.25 (0.11 to 14.39) | 2.78 | 51 | shift down: 8 in a row below the centre |
| revenue_per_slot | 8.18 (-2.51 to 18.86) | 5.63 | 51 | no shift yet |
| units | 33.05 (-23.93 to 90.03) | 9.57 | 51 | no shift yet |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 365: actual 7733.18, exemplar 61219.0 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 9.6: the exemplar has gained 9.6x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 550.81 | -9.82 |
| revenue | 133.5 | 30.43 |
| slots_selling | 14.29 | 4.71 |
| revenue_per_slot | 10.19 | 5.71 |
| units | 69.0 | 13.86 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 52 points across the horizon of 365.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 46). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 7 | x1.00 | /1.00 to x1.00 | x1.0 | x1.04 | flat |
| revenue | flow | up | 7 | /1.33 | /1.21 to x1.15 | x18.6 | x1.05 | flat |
| units | flow | up | 7 | /1.33 | /1.19 to x1.20 | x19.9 | x1.06 | flat |
| slots_selling | level | up | 7 | x1.05 (provisional) | x1.03 to x1.36 | x6.6 | x1.44 | improving |
| revenue_per_slot | flow | up | 7 | /1.31 | /1.32 to /1.11 | x2.8 | x1.05 | wrong way |
| unit_cost_paid_30d | level | down | 7 | /1.00 | /1.01 to x1.00 | x1.0 | /1.02 | flat |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.08 per point from point 3. Aim line (a deliberate overshoot: 61,219 by half the remaining horizon): x1.16 per point from point 3. Falling short of the aim is expected and triggers nothing.

Latest point 52 (days 358-364): 7,732.44; floor line 61,219.00; aim line 61,219.00. Required celeration from here to the target: x7.92; actual (this phase): x1.00.

## Since the phase change at point 46

Jump (first point / old line projected): /1.03. Turn (new celeration / old): /1.01.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 0 | 90 | 480 | 19% | 390 | 3 |
| slots stocked at day end | 4 | 5 | 72 | 7% | 67 | 0 |
| capital | 145.92 | 158.85 | 7759.1 | 2% | 7600.25 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 7733.18 | ok |
