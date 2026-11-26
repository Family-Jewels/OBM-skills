# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash | up | 3 | 1333.01 | 1209.81 | 1456.22 | 2091.42 | IMPROVEMENT: beyond the upper limit |
| cash_gain_5d | up | 3 | 129.76 | -82.26 | 341.78 | 488.42 | IMPROVEMENT: beyond the upper limit |
| revenue | up | 3 | 61.5 | -105.98 | 228.98 | 178.0 | routine variation |
| units | up | 3 | 30.15 | -50.21 | 110.51 | 89 | routine variation |
| slots_selling | up | 3 | 6.9 | -1.92 | 15.72 | 16 | IMPROVEMENT: beyond the upper limit |
| revenue_per_slot | up | 3 | 5.96 | -6.23 | 18.16 | 11.12 | routine variation |
| unit_cost_paid_30d | down | 11 | 0.89 | 0.88 | 0.91 | 0.924 | routine variation |
| units_in_storage | down | 3 | 56.25 | -89.63 | 202.13 | 7 | routine variation |
| capacity_used_share | up | 3 | 0.37 | -0.34 | 1.08 | 0.021 | routine variation |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 30: actual 2091.42, exemplar 3228.0 (requirements.md: scripted reference operator that knows the hidden economy parameters; EUR 1,500 to about EUR 3,228 by day 30. Hindsight benchmark; aims rise once reached.). PIP = 1.5: the exemplar has gained 1.5x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash | 1828.08 | 1828.08 |
| cash_gain_5d | 287.06 | 287.06 |
| revenue | 97.11 | 84.97 |
| units | 48.14 | 40.86 |
| slots_selling | 11.14 | 11.14 |
| revenue_per_slot | 8.58 | 7.73 |
| unit_cost_paid_30d | 0.86 | 0.92 |
| units_in_storage | 34.43 | 98.29 |
| capacity_used_share | 0.68 | 0.36 |

## Behavior and cost (information only; never a target or a limit)

- Capacity used in the last day: 2%
- Opportunities open when the last day ended: 3 (O1 Slots empty at day end: at least 30% of the 72 slots are unstocked, O2 Worker time unused (at least 120 minutes) while some slots are not selling, O3 Units sitting in the depot while worker time (at least 45 minutes) is unused)
- Working agent's context: 151.7k tokens
- Management roles' cost so far: audit $0.03, check $0.01
