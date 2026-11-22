# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 342 | 639.68 | 441.02 | 838.34 (provisional) | 846.7 | IMPROVEMENT: beyond the upper limit |
| revenue | up | 342 | 191.34 | 17.26 | 365.42 (provisional) | 59.5 | routine variation |
| slots_selling | up | 342 | 23.55 | 14.03 | 33.07 (provisional) | 22 | routine variation |
| revenue_per_slot | up | 342 | 7.79 | 0.84 | 14.74 (provisional) | 2.7 | routine variation |
| units | up | 342 | 90.0 | 8.66 | 171.34 (provisional) | 29 | routine variation |

## Since redesign R-P-031 (adopted day 342): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 639.68 (441.02 to 838.34) | 613.1 | 2 | shift up: beyond the upper limit |
| revenue | 191.34 (17.26 to 365.42) | 141.9 | 2 | no shift yet |
| slots_selling | 23.55 (14.03 to 33.07) | 23.5 | 2 | no shift yet |
| revenue_per_slot | 7.79 (0.84 to 14.74) | 5.84 | 2 | no shift yet |
| units | 90.0 (8.66 to 171.34) | 67.0 | 2 | no shift yet |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 343: actual 27938.25, exemplar 57410.64 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 2.1: the exemplar has gained 2.1x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 1422.43 | 442.17 |
| revenue | 272.57 | 181.41 |
| slots_selling | 29.0 | 24.29 |
| revenue_per_slot | 10.17 | 7.16 |
| units | 125.29 | 85.29 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 52 points across the horizon of 365.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 49). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 1 | collecting | | | — | collecting |
| revenue | flow | up | 1 | collecting | | | — | collecting |
| units | flow | up | 1 | collecting | | | — | collecting |
| slots_selling | level | up | 1 | collecting | | | — | collecting |
| revenue_per_slot | flow | up | 1 | collecting | | | — | collecting |
| unit_cost_paid_30d | level | down | 1 | collecting | | | — | collecting |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.08 per point from point 3. Aim line (a deliberate overshoot: 122,438 by half the remaining horizon): x1.18 per point from point 6. Falling short of the aim is expected and triggers nothing.

Latest point 49 (days 337-343): 27,938.25; floor line 49,000.89; aim line 122,438.00. Required celeration from here to the target: x1.30; actual (this phase): collecting.

## Since the phase change at point 49

Jump (first point / old line projected): x1.01. Turn (new celeration / old): needs 3 points in the new phase.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 435 | 440 | 480 | 92% | 40 | 0 |
| slots stocked at day end | 57 | 54 | 72 | 75% | 18 | 0 |
| capital | 2044.01 | 2073.13 | 29862.26 | 7% | 27789.13 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 27938.25 | ok |
