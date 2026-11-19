# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 328 | 218.02 | 42.8 | 393.24 | 149.81 | routine variation |
| revenue | up | 328 | 90.48 | -11.04 | 192.01 | 3.7 | WORSE: 8 in a row below the centre |
| slots_selling | up | 328 | 13.4 | 7.66 | 19.14 | 2 | WORSE: beyond the lower limit |
| revenue_per_slot | up | 328 | 6.47 | -0.18 | 13.13 | 1.85 | routine variation |
| units | up | 328 | 45.7 | -4.28 | 95.68 | 2 | WORSE: 8 in a row below the centre |

## Since redesign R-O-005 (adopted day 328): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 288.24 (50.25 to 526.23) | 261.86 | 38 | no shift yet |
| revenue | 113.98 (-43.74 to 271.7) | 71.17 | 38 | shift down: 8 in a row below the centre |
| slots_selling | 13.25 (4.99 to 21.51) | 11.53 | 38 | shift down: beyond the lower limit |
| revenue_per_slot | 8.06 (0.15 to 15.98) | 5.42 | 38 | shift down: 8 in a row below the centre |
| units | 59.5 (-22.54 to 141.54) | 36.24 | 38 | shift down: 8 in a row below the centre |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 365: actual 11832.66, exemplar 61219.0 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 5.8: the exemplar has gained 5.8x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 596.12 | 192.06 |
| revenue | 170.3 | 31.69 |
| slots_selling | 16.0 | 6.29 |
| revenue_per_slot | 10.43 | 3.76 |
| units | 81.57 | 16.57 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 52 points across the horizon of 365.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 47). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 6 | x1.03 | x1.03 to x1.03 | x1.0 | x1.15 | improving |
| revenue | flow | up | 6 | /1.30 | /1.53 to x1.10 | x7.2 | x1.39 | flat |
| units | flow | up | 6 | /1.33 | /1.55 to x1.12 | x7.6 | x1.42 | flat |
| slots_selling | level | up | 6 | /1.40 | /1.64 to x1.08 | x37.8 | x1.39 | flat |
| revenue_per_slot | flow | up | 6 | /1.32 | /1.36 to /1.08 | x2.6 | x1.12 | wrong way |
| unit_cost_paid_30d | level | down | 6 | x1.01 | /1.01 to x1.01 | x1.1 | /1.03 | flat |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.08 per point from point 3. Aim line (a deliberate overshoot: 122,438 by half the remaining horizon): x1.20 per point from point 6. Falling short of the aim is expected and triggers nothing.

Latest point 52 (days 358-364): 11,841.16; floor line 61,219.00; aim line 122,438.00. Required celeration from here to the target: x5.17; actual (this phase): x1.03.

## Since the phase change at point 47

Jump (first point / old line projected): /1.03. Turn (new celeration / old): /1.01.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 0 | 0 | 480 | 0% | 480 | 5 |
| slots stocked at day end | 8 | 8 | 72 | 11% | 64 | 0 |
| capital | 126.25 | 133.86 | 11838.91 | 1% | 11705.05 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 11832.66 | ok |

## Units (for experiment slices; latest point, median per day)

| unit | machine_revenue | machine_units | machine_stocked_slots |
| --- | --- | --- | --- |
| AI-HOUSE:DRINKS | 4.2 | 2 | 2 |
| AI-HOUSE:SNACK | 3.6 | 2 | 0 |
| AI-LOUNGE:DRINKS | 0.0 | 0 | 1 |
| AI-LOUNGE:SNACK | 3.7 | 2 | 4 |
| MAIN-LOUNGE:DRINKS | 0.0 | 0 | 0 |
| MAIN-LOUNGE:SNACK | 9.6 | 5 | 1 |

## Experiments (run and judged by the system; verdicts by the auditor)

Lifecycle: planned, queued (its slice overlaps a running one), fidelity (the checker is verifying the change), running (the clock started when fidelity passed), verdict (the auditor is ruling), done. Effect: the driver after the start divided by its expected value (slice against control where the driver is measured per unit); read against the envelope of the earlier bounce.

| experiment | driver | slice | capacity | start | end | clock started | state | effect | envelope | reading |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E-001 | revenue_per_slot | MAIN-LOUNGE:DRINKS, AI-LOUNGE:DRINKS | 5 | 4 | 8 | 41 | done: too small to read | /1.05 | within x1.29 | too small to read: inside the earlier bounce |
| E-002 | machine_revenue | MAIN-LOUNGE:DRINKS, MAIN-LOUNGE:SNACK | 5 | 4 | 8 | 78 | done: too small to read | /1.04 | within x1.61 | too small to read: inside the earlier bounce |
| E-003 | machine_revenue | AI-LOUNGE:DRINKS, AI-LOUNGE:SNACK | 20 | 3 | 20 | — | void |  | | |
| E-004 | machine_revenue | AI-HOUSE:SNACK | 5 | 197 | 217 | 247 | done: too small to read | /1.12 | within x1.96 | too small to read: inside the earlier bounce |
| E-005 | machine_revenue | AI-HOUSE:SNACK | 45 | 316 | 336 | — | void |  | | |
