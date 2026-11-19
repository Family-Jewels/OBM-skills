# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 83 | 158.12 | 70.19 | 246.06 (provisional) | 65.71 | WORSE: beyond the lower limit |
| revenue | up | 83 | 23.58 | -20.61 | 67.76 (provisional) | 2.75 | routine variation |
| slots_selling | up | 83 | 3.78 | 0.45 | 7.1 (provisional) | 1 | routine variation |
| revenue_per_slot | up | 83 | 6.05 | -3.62 | 15.72 (provisional) | 2.75 | routine variation |
| units | up | 83 | 9.11 | -7.51 | 25.74 (provisional) | 1 | routine variation |

## Since redesign R-A-002 (adopted day 83): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 502.92 (181.17 to 824.67) | 158.12 | 9 | shift down: beyond the lower limit |
| revenue | 141.42 (-56.89 to 339.73) | 23.58 | 9 | shift down: 8 in a row below the centre |
| slots_selling | 16.6 (5.54 to 27.66) | 3.78 | 9 | shift down: beyond the lower limit |
| revenue_per_slot | 7.96 (0.51 to 15.41) | 6.05 | 9 | no shift yet |
| units | 63.35 (-26.95 to 153.65) | 9.11 | 9 | shift down: 8 in a row below the centre |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 91: actual 4867.77, exemplar 13787.56 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 3.6: the exemplar has gained 3.6x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 618.43 | 138.15 |
| revenue | 163.75 | 20.99 |
| slots_selling | 18.86 | 3.43 |
| revenue_per_slot | 9.35 | 6.24 |
| units | 77.0 | 8.0 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 13 points across the horizon of 91.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 12). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 2 | collecting | | | x1.16 | collecting |
| revenue | flow | up | 2 | collecting | | | /1.23 | collecting |
| units | flow | up | 2 | collecting | | | /1.23 | collecting |
| slots_selling | level | up | 2 | collecting | | | x1.13 | collecting |
| revenue_per_slot | flow | up | 2 | collecting | | | /1.08 | collecting |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.47 per point from point 3. Aim line (a deliberate overshoot: 61,219 by half the remaining horizon): x2.15 per point from point 3. Falling short of the aim is expected and triggers nothing.

Latest point 13 (days 85-91): 4,867.77; floor line 61,219.00; aim line 61,219.00. Required celeration from here to the target: x12.58; actual (this phase): collecting.

## Since the phase change at point 12

Jump (first point / old line projected): /1.17. Turn (new celeration / old): needs 3 points in the new phase.

## Resources (used / available, written by the system)

| resource | used | available | in use | idle |
| --- | --- | --- | --- | --- |
| slots stocked at day end | 2 | 72 | 3% | 70 |
| capital | 56.68 | 4804.45 | 1% | 4747.77 |

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 4867.77 | ok |

## Experiments (judged on the system's data)

| experiment | driver | start | end | cash celeration before | since start | status |
| --- | --- | --- | --- | --- | --- | --- |
| E-001 | net_unit_price | 8 | 28 | — | x1.15 | ended: keep or revert |
| E-002 | units_per_slot_day | 29 | 49 | x1.14 | x1.12 | ended: keep or revert |
| E-003 | footfall per location | 50 | 70 | x1.18 | x1.07 | ended: keep or revert |
| E-004 | unit_cost | 30 | 56 | x1.14 | x1.12 | ended: keep or revert |
| E-005 | stock availability (stock-out slot-days). | 30 | 56 | x1.14 | x1.12 | ended: keep or revert |
