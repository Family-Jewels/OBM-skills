# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 348 | 301.68 | 83.47 | 519.9 (provisional) | 577.1 | IMPROVEMENT: beyond the upper limit |
| revenue | up | 348 | 82.19 | -86.45 | 250.84 (provisional) | 16.7 | routine variation |
| slots_selling | up | 348 | 9.28 | -3.55 | 22.11 (provisional) | 7 | routine variation |
| revenue_per_slot | up | 348 | 6.67 | -1.27 | 14.62 (provisional) | 2.39 | routine variation |
| units | up | 348 | 34.33 | -36.08 | 104.75 (provisional) | 8 | routine variation |

## Since redesign R-P-011 (adopted day 348): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 190.34 (-60.76 to 441.45) | 301.68 | 18 | shift up: beyond the upper limit |
| revenue | 71.36 (-106.87 to 249.59) | 82.19 | 18 | no shift yet |
| slots_selling | 6.0 (-4.08 to 16.08) | 9.28 | 18 | no shift yet |
| revenue_per_slot | 9.06 (-5.56 to 23.69) | 6.67 | 18 | no shift yet |
| units | 28.3 (-40.3 to 96.9) | 34.33 | 18 | no shift yet |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 365: actual 9738.92, exemplar 61219.0 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 7.2: the exemplar has gained 7.2x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 586.9 | 586.9 |
| revenue | 121.13 | 92.06 |
| slots_selling | 12.57 | 10.14 |
| revenue_per_slot | 12.79 | 6.52 |
| units | 50.29 | 40.14 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 52 points across the horizon of 365.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 50). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 3 | x1.06 (provisional) | x1.05 to x1.06 | x1.0 | x1.11 | improving |
| revenue | flow | up | 3 | x1.26 (provisional) | /1.01 to x1.61 | x3.9 | x1.50 | flat |
| units | flow | up | 3 | x1.28 (provisional) | x1.04 to x1.57 | x3.2 | x1.47 | improving |
| slots_selling | level | up | 3 | x1.07 (provisional) | /2.56 to x2.92 | x296.7 | x1.09 | flat |
| revenue_per_slot | flow | up | 3 | /1.25 (provisional) | /1.32 to /1.18 | x1.4 | x1.13 | wrong way |
| unit_cost_paid_30d | level | down | 3 | x1.03 (provisional) | x1.01 to x1.06 | x1.1 | /1.02 | wrong way |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.08 per point from point 3. Aim line (a deliberate overshoot: 61,219 by half the remaining horizon): x1.18 per point from point 3. Falling short of the aim is expected and triggers nothing.

Latest point 52 (days 358-364): 9,733.62; floor line 61,219.00; aim line 61,219.00. Required celeration from here to the target: x6.29; actual (this phase): x1.06.

## Since the phase change at point 50

Jump (first point / old line projected): /1.04. Turn (new celeration / old): x1.04.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 5 | 50 | 480 | 10% | 430 | 1 |
| slots stocked at day end | 6 | 8 | 72 | 11% | 64 | 0 |
| capital | 37.69 | 54.34 | 9656.61 | 1% | 9602.27 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 9738.92 | ok |
