# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 148 | 236.51 | 20.67 | 452.35 (provisional) | 454.18 | IMPROVEMENT: beyond the upper limit |
| revenue | up | 148 | 89.97 | -124.1 | 304.05 (provisional) | 41.9 | routine variation |
| slots_selling | up | 148 | 9.35 | -1.71 | 20.41 (provisional) | 6 | routine variation |
| revenue_per_slot | up | 148 | 8.44 | -4.95 | 21.84 (provisional) | 6.98 | routine variation |
| units | up | 148 | 43.7 | -63.12 | 150.52 (provisional) | 18 | routine variation |

## Since redesign R-P-004 (adopted day 148): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 236.51 (20.67 to 452.35) | 439.04 | 6 | shift up: beyond the upper limit |
| revenue | 89.97 (-124.1 to 304.05) | 93.33 | 6 | no shift yet |
| slots_selling | 9.35 (-1.71 to 20.41) | 9.17 | 6 | no shift yet |
| revenue_per_slot | 8.44 (-4.95 to 21.84) | 9.66 | 6 | no shift yet |
| units | 43.7 (-63.12 to 150.52) | 46.83 | 6 | no shift yet |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 153: actual 6354.08, exemplar 24520.22 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 4.7: the exemplar has gained 4.7x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 631.06 | 443.6 |
| revenue | 146.26 | 83.14 |
| slots_selling | 14.57 | 8.86 |
| revenue_per_slot | 10.57 | 8.73 |
| units | 70.29 | 41.57 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 52 points across the horizon of 365.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 22). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 0 | collecting | | | x1.06 | collecting |
| revenue | flow | up | 0 | collecting | | | x1.25 | collecting |
| units | flow | up | 0 | collecting | | | x1.29 | collecting |
| slots_selling | level | up | 0 | collecting | | | x1.52 | collecting |
| revenue_per_slot | flow | up | 0 | collecting | | | /1.03 | collecting |
| unit_cost_paid_30d | level | down | 0 | collecting | | | x1.00 | collecting |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.08 per point from point 3. Aim line (a deliberate overshoot: 122,438 by half the remaining horizon): x1.18 per point from point 6. Falling short of the aim is expected and triggers nothing.

Latest point 21 (days 141-147): 6,013.40; floor line 5,800.73; aim line 31,977.70. Required celeration from here to the target: x1.08; actual (this phase): collecting.

## Since the phase change at point 22

Jump (first point / old line projected): needs a point and an old line. Turn (new celeration / old): needs 3 points in the new phase.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 0 | 35 | 480 | 7% | 445 | 3 |
| slots stocked at day end | 3 | 7 | 72 | 10% | 65 | 0 |
| capital | 128.35 | 216.22 | 6362.43 | 3% | 6146.21 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 6354.08 | ok |
