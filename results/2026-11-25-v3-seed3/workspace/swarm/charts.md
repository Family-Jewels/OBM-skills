# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 341 | -84.0 | -84.0 | -84.0 | -84.0 | routine variation |
| revenue | up | 323 | 0.0 | 0.0 | 0.0 | 0.0 | routine variation |
| slots_selling | up | 323 | 0.0 | 0.0 | 0.0 | 0 | routine variation |
| revenue_per_slot | up | 322 | 0.0 | 0.0 | 0.0 | 0 | routine variation |
| units | up | 323 | 0.0 | 0.0 | 0.0 | 0 | routine variation |

## Since redesign R-P-013 (adopted day 307): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | -82.44 (-85.04 to -79.83) | -72.06 | 59 | shift down: 8 in a row below the centre |
| revenue | 3.67 (-0.08 to 7.42) | 1.24 | 59 | shift down: 8 in a row below the centre |
| slots_selling | 1.25 (-0.01 to 2.51) | 0.42 | 59 | shift down: 8 in a row below the centre |
| revenue_per_slot | 1.37 (0.01 to 2.74) | 0.47 | 59 | shift down: beyond the lower limit |
| units | 2.1 (-0.14 to 4.34) | 0.71 | 59 | shift down: 8 in a row below the centre |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 365: actual 8827.57, exemplar 61219.0 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 8.1: the exemplar has gained 8.1x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 731.63 | -84.0 |
| revenue | 167.03 | 0.0 |
| slots_selling | 20.0 | 0.0 |
| revenue_per_slot | 8.51 | 0.0 |
| units | 80.86 | 0.0 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 52 points across the horizon of 365.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 44). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 9 | /1.01 | /1.01 to /1.01 | x1.0 | x1.03 | wrong way |
| revenue | flow | up | 9 | collecting | | | /1.15 | collecting |
| units | flow | up | 9 | collecting | | | /1.15 | collecting |
| slots_selling | level | up | 9 | collecting | | | /1.08 | collecting |
| revenue_per_slot | flow | up | 9 | collecting | | | /1.02 | collecting |
| unit_cost_paid_30d | level | down | 0 | collecting | | | /1.02 | collecting |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.08 per point from point 3. Aim line (a deliberate overshoot: 122,438 by half the remaining horizon): x1.17 per point from point 6. Falling short of the aim is expected and triggers nothing.

Latest point 52 (days 358-364): 8,839.57; floor line 61,219.00; aim line 122,438.00. Required celeration from here to the target: x6.93; actual (this phase): /1.01.

## Since the phase change at point 44

Jump (first point / old line projected): /1.01. Turn (new celeration / old): /1.01.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 0 | 0 | 480 | 0% | 480 | 7 |
| slots stocked at day end | 0 | 0 | 72 | 0% | 72 | 7 |
| capital | 28.69 | 28.69 | 8736.26 | 0% | 8707.57 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 8827.57 | ok |
