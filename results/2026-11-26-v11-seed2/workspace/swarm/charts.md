# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash | up | 343 | 5907.77 | 5874.79 | 5940.75 | 5908.7 | routine variation |
| cash_change_per_day | up | 180 | 9.4 | -137.63 | 156.42 | -7.2 | routine variation |
| revenue | up | 180 | 44.75 | -61.45 | 150.95 | 4.5 | routine variation |
| slots_selling | up | 180 | 7.55 | 0.41 | 14.69 | 2 | routine variation |
| revenue_per_slot | up | 180 | 5.24 | -4.89 | 15.36 | 2.25 | routine variation |
| unit_cost_paid_30d | down | 298 | 0.75 | 0.73 | 0.77 | 0.759 | routine variation |
| units_in_storage | down | 180 | 58.2 | -62.2 | 178.6 | 0 | IMPROVEMENT: 8 in a row below the centre |
| units | up | 3 | collecting | |  | 3 | — |
| revenue_change_7_periods | up | 180 | 4.62 | -118.21 | 127.44 | -9.3 | routine variation |
| capacity_used_share | up | 180 | 0.22 | -0.66 | 1.11 | 0.0 | routine variation |

## Since redesign R-A-003 (adopted day 180): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash | 5771.91 (5698.57 to 5845.24) | 5338.38 | 186 | shift up: beyond the upper limit |
| cash_change_per_day | 15.86 (-85.72 to 117.43) | 7.67 | 186 | no shift yet |
| revenue | 46.7 (-95.75 to 189.15) | 34.77 | 186 | no shift yet |
| slots_selling | 7.25 (-2.41 to 16.91) | 5.79 | 186 | no shift yet |
| revenue_per_slot | 5.49 (-4.99 to 15.97) | 4.97 | 186 | no shift yet |
| unit_cost_paid_30d | 0.78 (0.78 to 0.79) | 0.77 | 186 | shift down: beyond the lower limit |
| units_in_storage | 43.6 (-68.96 to 156.16) | 36.86 | 186 | shift down: 8 in a row below the centre |
| revenue_change_7_periods | -2.04 (-251.4 to 247.31) | -0.95 | 186 | no shift yet |
| capacity_used_share | 0.24 (-0.81 to 1.3) | 0.18 | 186 | no shift yet |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 365: actual 5908.7, exemplar 61219.0 (swarm/requirements.md: the benchmark's scripted reference operator (knows the hidden economy parameters); EUR 3,228 by day 30 and EUR 61,219 by day 365. An aim, not a ceiling.). PIP = 10.4: the exemplar has gained 10.4x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash | 5941.58 | 5914.49 |
| cash_change_per_day | 58.28 | 5.01 |
| revenue | 97.74 | 16.97 |
| slots_selling | 12.71 | 4.14 |
| revenue_per_slot | 9.43 | 2.9 |
| unit_cost_paid_30d | 0.69 | 0.74 |
| units_in_storage | 1.71 | 1.71 |
| revenue_change_7_periods | 50.14 | 3.0 |
| capacity_used_share | 0.56 | 0.03 |

## Behavior and cost (information only; never a target or a limit)

- Capacity used in the last day: 0%
- Opportunities open when the last day ended: 3 (O1 Empty slots and worker time left at day end: stock or reprice slots that can earn, O3 Cash is available to spend and worker time is unused: stock or reprice slots that can earn, after loading stock already waiting in the depot, O4 Stocked slots are empty and the depot holds no stock: the next order is what fills them)
- Working agent's context: 778.2k tokens
- Management roles' cost so far: pulse $0.15, check $0.18, audit $0.38, diagnosis $0.11, redesign $0.04
