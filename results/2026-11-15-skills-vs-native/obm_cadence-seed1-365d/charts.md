# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 327 | 481.31 | 213.06 | 749.56 | 63.8 | WORSE: beyond the lower limit |
| revenue | up | 327 | 123.98 | -70.17 | 318.14 | 0.0 | WORSE: 8 in a row below the centre |
| slots_selling | up | 327 | 14.15 | 1.41 | 26.89 | 0 | WORSE: beyond the lower limit |
| revenue_per_slot | up | 327 | 7.88 | 0.45 | 15.31 | 0 | WORSE: beyond the lower limit |
| units | up | 327 | 52.35 | -27.03 | 131.73 | 0 | WORSE: 8 in a row below the centre |

## Since redesign R-P-042 (adopted day 332): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 281.51 (27.28 to 535.74) | 378.88 | 34 | shift down: 8 in a row below the centre |
| revenue | 103.89 (-93.22 to 301.0) | 81.51 | 34 | shift down: 8 in a row below the centre |
| slots_selling | 11.3 (-0.88 to 23.48) | 10.18 | 34 | shift down: 8 in a row below the centre |
| revenue_per_slot | 8.43 (-1.65 to 18.52) | 6.0 | 34 | no shift yet |
| units | 43.1 (-34.88 to 121.08) | 34.47 | 34 | shift down: 8 in a row below the centre |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 365: actual 18859.26, exemplar 61219.0 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 3.4: the exemplar has gained 3.4x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 718.81 | 89.3 |
| revenue | 168.97 | 18.97 |
| slots_selling | 17.0 | 2.71 |
| revenue_per_slot | 11.41 | 2.73 |
| units | 74.86 | 7.86 |
