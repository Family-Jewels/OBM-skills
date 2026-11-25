# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 338 | 35.0 | -83.3 | 153.3 | -35.5 | WORSE: 8 in a row below the centre |
| revenue | up | 338 | 28.88 | -39.45 | 97.2 | 0.0 | routine variation |
| slots_selling | up | 338 | 4.6 | -1.42 | 10.62 | 0 | WORSE: 8 in a row below the centre |
| revenue_per_slot | up | 338 | 4.49 | -3.83 | 12.81 | 0 | routine variation |
| units | up | 338 | 13.2 | -16.76 | 43.16 | 0 | routine variation |

## Since redesign R-P-014 (adopted day 338): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 103.59 (-43.72 to 250.9) | 24.21 | 28 | shift down: 8 in a row below the centre |
| revenue | 43.4 (-62.72 to 149.52) | 22.68 | 28 | shift down: 8 in a row below the centre |
| slots_selling | 4.7 (-2.44 to 11.84) | 3.75 | 28 | shift down: 8 in a row below the centre |
| revenue_per_slot | 6.4 (-6.51 to 19.32) | 3.95 | 28 | no shift yet |
| units | 19.55 (-27.07 to 66.17) | 10.39 | 28 | shift down: 8 in a row below the centre |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 365: actual 8424.2, exemplar 61219.0 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 8.6: the exemplar has gained 8.6x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 686.23 | -5.64 |
| revenue | 166.36 | 6.57 |
| slots_selling | 19.71 | 1.29 |
| revenue_per_slot | 8.82 | 2.57 |
| units | 86.43 | 3.14 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 52 points across the horizon of 365.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 49). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 4 | x1.00 (provisional) | /1.00 to x1.01 | x1.0 | x1.08 | flat |
| revenue | flow | up | 4 | /2.03 (provisional) | /3.16 to /1.40 | x10.0 | x1.02 | wrong way |
| units | flow | up | 4 | /1.87 (provisional) | /2.47 to /1.37 | x8.6 | x1.04 | wrong way |
| slots_selling | level | up | 4 | /1.82 (provisional) | /3.30 to /1.35 | x29.3 | x1.44 | wrong way |
| revenue_per_slot | flow | up | 4 | /1.11 (provisional) | /1.44 to x1.13 | x3.9 | /1.03 | flat |
| unit_cost_paid_30d | level | down | 4 | x1.09 (provisional) | x1.04 to x1.16 | x1.5 | /1.01 | wrong way |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.08 per point from point 3. Aim line (a deliberate overshoot: 122,438 by half the remaining horizon): x1.18 per point from point 6. Falling short of the aim is expected and triggers nothing.

Latest point 52 (days 358-364): 8,434.70; floor line 61,219.00; aim line 122,438.00. Required celeration from here to the target: x7.26; actual (this phase): x1.00.

## Since the phase change at point 49

Jump (first point / old line projected): /1.01. Turn (new celeration / old): /1.00.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 0 | 0 | 480 | 0% | 480 | 7 |
| slots stocked at day end | 0 | 1 | 72 | 1% | 71 | 2 |
| capital | 31.59 | 32.1 | 8335.79 | 0% | 8303.69 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 8424.2 | ok |
