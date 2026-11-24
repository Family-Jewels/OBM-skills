# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 226 | 229.02 | 81.73 | 376.3 (provisional) | 228.0 | routine variation |
| revenue | up | 226 | 74.84 | -60.46 | 210.13 (provisional) | 33.0 | routine variation |
| slots_selling | up | 226 | 8.6 | -0.64 | 17.84 (provisional) | 5 | routine variation |
| revenue_per_slot | up | 226 | 9.05 | -2.82 | 20.93 (provisional) | 6.6 | routine variation |
| units | up | 226 | 28.8 | -22.86 | 80.46 (provisional) | 13 | routine variation |

## Since redesign R-P-006 (adopted day 226): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 229.02 (81.73 to 376.3) | 315.46 | 4 | no shift yet |
| revenue | 74.84 (-60.46 to 210.13) | 62.53 | 4 | no shift yet |
| slots_selling | 8.6 (-0.64 to 17.84) | 7.25 | 4 | no shift yet |
| revenue_per_slot | 9.05 (-2.82 to 20.93) | 8.5 | 4 | no shift yet |
| units | 28.8 (-22.86 to 80.46) | 25.75 | 4 | no shift yet |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 229: actual 8783.13, exemplar 37676.39 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 5.0: the exemplar has gained 5.0x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 531.3 | 304.51 |
| revenue | 149.97 | 70.91 |
| slots_selling | 15.43 | 8.71 |
| revenue_per_slot | 12.63 | 8.2 |
| units | 60.0 | 28.0 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 52 points across the horizon of 365.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 33). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 0 | collecting | | | x1.06 | collecting |
| revenue | flow | up | 0 | collecting | | | x1.07 | collecting |
| units | flow | up | 0 | collecting | | | x1.07 | collecting |
| slots_selling | level | up | 0 | collecting | | | /1.02 | collecting |
| revenue_per_slot | flow | up | 0 | collecting | | | x1.08 | collecting |
| unit_cost_paid_30d | level | down | 0 | collecting | | | /1.00 | collecting |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.08 per point from point 3. Aim line (a deliberate overshoot: 122,438 by half the remaining horizon): x1.19 per point from point 6. Falling short of the aim is expected and triggers nothing.

Latest point 32 (days 218-224): 8,715.73; floor line 12,376.28; aim line 122,438.00. Required celeration from here to the target: x1.10; actual (this phase): collecting.

## Since the phase change at point 33

Jump (first point / old line projected): needs a point and an old line. Turn (new celeration / old): needs 3 points in the new phase.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 50 | 50 | 480 | 10% | 430 | 1 |
| slots stocked at day end | 1 | 7 | 72 | 10% | 65 | 0 |
| capital | 402.81 | 438.35 | 9065.94 | 5% | 8627.59 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 8783.13 | ok |
