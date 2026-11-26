# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash | up | 334 | 12765.57 | 12606.77 | 12924.37 | 13420.68 | IMPROVEMENT: beyond the upper limit |
| cash_gain_30d | up | 341 | 1188.29 | 1034.72 | 1341.86 | 875.63 | WORSE: beyond the lower limit |
| revenue | up | 311 | 88.14 | -104.7 | 280.97 | 9.3 | routine variation |
| units | up | 311 | 40.45 | -45.79 | 126.69 | 5 | routine variation |
| slots_selling | up | 311 | 12.4 | 1.34 | 23.46 | 5 | routine variation |
| revenue_per_slot | up | 311 | 7.02 | -2.86 | 16.89 | 1.86 | routine variation |
| unit_cost_paid_30d | down | 337 | 0.82 | 0.81 | 0.83 | 0.812 | routine variation |
| units_in_storage | down | 311 | 86.85 | -95.43 | 269.13 | 13 | routine variation |
| capacity_used_share | up | 311 | 0.45 | -0.4 | 1.3 | 0.0 | WORSE: 8 in a row below the centre |

## Since redesign R-A-006 (adopted day 311): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash | 11891.15 (11739.11 to 12043.18) | 12502.04 | 55 | shift up: beyond the upper limit |
| cash_gain_30d | 981.18 (783.92 to 1178.44) | 1072.12 | 55 | no shift yet |
| revenue | 90.36 (-131.23 to 311.96) | 73.32 | 55 | no shift yet |
| units | 41.9 (-57.64 to 141.44) | 33.16 | 55 | no shift yet |
| slots_selling | 9.85 (-4.29 to 23.99) | 11.02 | 55 | no shift yet |
| revenue_per_slot | 7.0 (-4.15 to 18.14) | 6.16 | 55 | no shift yet |
| unit_cost_paid_30d | 0.84 (0.83 to 0.85) | 0.83 | 55 | shift down: beyond the lower limit |
| units_in_storage | 78.3 (-100.62 to 257.22) | 92.0 | 55 | no shift yet |
| capacity_used_share | 0.42 (-0.35 to 1.19) | 0.33 | 55 | shift down: 8 in a row below the centre |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 365: actual 13420.68, exemplar 61219.0 (Requirements: benchmark scripted reference operator (knows the economy's hidden parameters): EUR 1,500 to about EUR 3,228 by day 30 and EUR 61,219 by day 365. Aim only; early periods are not expected to match it.). PIP = 4.6: the exemplar has gained 4.6x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash | 13362.78 | 13362.78 |
| cash_gain_30d | 1552.18 | 1072.59 |
| revenue | 139.7 | 48.44 |
| units | 65.14 | 21.71 |
| slots_selling | 15.29 | 7.71 |
| revenue_per_slot | 9.69 | 4.77 |
| unit_cost_paid_30d | 0.79 | 0.83 |
| units_in_storage | 2.0 | 28.29 |
| capacity_used_share | 0.7 | 0.1 |

## Behavior and cost (information only; never a target or a limit)

- Capacity used in the last day: 0%
- Opportunities open when the last day ended: 2 (O1 Machine slots are empty or unstocked while worker time is still spare, O3 Cash is idle while machine slots are empty)
- Working agent's context: 195.1k tokens
- Management roles' cost so far: pulse $0.28, check $0.27, audit $0.39, diagnosis $0.21, redesign $0.08
