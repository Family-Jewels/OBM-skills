# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 84 | 573.91 | 355.84 | 791.97 (provisional) | 833.8 | IMPROVEMENT: beyond the upper limit |
| revenue | up | 84 | 120.95 | -91.83 | 333.73 (provisional) | 47.8 | routine variation |
| slots_selling | up | 84 | 12.5 | 5.66 | 19.34 (provisional) | 11 | routine variation |
| revenue_per_slot | up | 84 | 9.45 | -4.66 | 23.57 (provisional) | 4.35 | routine variation |
| units | up | 84 | 44.62 | -31.0 | 120.25 (provisional) | 20 | routine variation |

## Since redesign M-004 (adopted day 84): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 409.53 (235.04 to 584.02) | 573.91 | 8 | shift up: beyond the upper limit |
| revenue | 130.06 (-58.97 to 319.08) | 120.95 | 8 | no shift yet |
| slots_selling | 12.5 (6.06 to 18.94) | 12.5 | 8 | no shift yet |
| revenue_per_slot | 10.1 (-1.3 to 21.51) | 9.45 | 8 | no shift yet |
| units | 49.5 (-19.24 to 118.24) | 44.62 | 8 | no shift yet |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 91: actual 5679.48, exemplar 13787.56 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 2.9: the exemplar has gained 2.9x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 611.14 | 611.14 |
| revenue | 148.99 | 130.72 |
| slots_selling | 14.43 | 12.71 |
| revenue_per_slot | 10.79 | 10.12 |
| units | 70.14 | 48.57 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 13 points across the horizon of 91.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 13). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 1 | collecting | | | — | collecting |
| revenue | flow | up | 1 | collecting | | | — | collecting |
| units | flow | up | 1 | collecting | | | — | collecting |
| slots_selling | level | up | 1 | collecting | | | — | collecting |
| revenue_per_slot | flow | up | 1 | collecting | | | — | collecting |
| unit_cost_paid_30d | level | down | 1 | collecting | | | — | collecting |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.44 per point from point 3. Aim line (a deliberate overshoot: 61,219 by half the remaining horizon): x2.07 per point from point 3. Falling short of the aim is expected and triggers nothing.

Latest point 13 (days 85-91): 5,679.48; floor line 61,219.00; aim line 61,219.00. Required celeration from here to the target: x10.78; actual (this phase): collecting.

## Since the phase change at point 13

Jump (first point / old line projected): x1.06. Turn (new celeration / old): needs 3 points in the new phase.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 300 | 300 | 480 | 62% | 180 | 0 |
| slots stocked at day end | 12 | 8 | 72 | 11% | 64 | 0 |
| capital | 117.62 | 176.58 | 5677.1 | 3% | 5500.52 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 5679.48 | ok |

## Facts measured by the system (from the harness's log of every action; cost in worker time (minutes a day))

Read these instead of asking: they are measured, not assumed.

| action | calls | median cost | share of capacity, last point |
| --- | --- | --- | --- |
| restock_machine | 356 | 45.0 | 60% |
| set_price | 428 | 5.0 | 15% |
| get_machine_inventory | 58 | 25.0 | 8% |
| get_sales_report | 74 | 25.0 | 8% |
| get_storage_inventory | 45 | 25 | 7% |
| write_note | 89 | 5 | 2% |
| get_status | 15 | 5 | 1% |
| read_notes | 1 | 5 | 0% |
| list_emails | 14 | 5.0 | 0% |
| get_marketing_report | 2 | 5.0 | 0% |
| read_email | 7 | 5 | 0% |
| search_web | 1 | 25 | 0% |
| check_offers | 22 | 25.0 | 0% |
| order_goods | 27 | 25 | 0% |
| set_reminder | 15 | 5 | 0% |

## Pursuit: planned vs actual capacity split (last point; plan from swarm/aims.md)

| label | planned | actual | gap |
| --- | --- | --- | --- |
| restock fills, from depot stock only | 45% | 60% | +15% |
| price setting and tests | 15% | 15% | -0% |
| supplier purchasing, inside the order guardrail | 10% | 0% | -10% |
| reads and admin | 16% | 26% | +10% |
| slack | 14% | 0% | -14% |
| other (not in the split) | 0% | 0% | +0% |

## Facts proposed by roles (not measured by the system; each with its cited source)

- One offer cycle needs check_offers and order_goods: 25 + 25 = 50 minutes per 7 days, about 1.5% of the 480-minute day, against a 20% (96-minute) daily plan (source: swarm/charts.md Facts table (median cost 25 each); swarm/history/aims.v6.md Capacity split; from M-004)
- check_offers ran 20 times and order_goods 25 times over the run (source: swarm/charts.md Facts table (calls); from M-004)
- Restock fills were 56% of minutes used at the last point, against a 35% plan (source: swarm/charts.md Pursuit table; from M-004)
- Capital in use is 8% (379.14 of 4,791.57) (source: swarm/charts.md Resources; from M-004)
- The v6 aims constraint text said purchasing planned at 10%, and the capacity split said 20% (source: swarm/history/aims.v6.md (constraint line; Capacity split); from M-004)
- rules/operator.md v4 had no unit-cost price floor and no 1.02 to 1.05 text (source: swarm/rules/operator.md v4 (grep); swarm/audits/A-003.md; from M-004)
- Restock ceiling is 216 minutes a day (45% of 480); a fifth fill (180 + 45 = 225) is refused by it (source: swarm/controls.md line 6; from AS-005)
- PO-1025 total 189.80 = 60x0.81 + 60x0.64 + 40x1.57 + 40x1.00 from the day-78 rows (source: swarm/log/day-83.md line 7; swarm/log/T-0002.md (day 78 table); from P-013)
- Orders in the day logs with no T-0002 row dated on or before the order day (source: swarm/log/day-*.md order lines cross-read against swarm/log/T-0002.md (proposed; the harness order log that would settle it is not in the workspace, see REQ-055); from C-010)
- Day-71 order PO-1023 (263.40) has no T-0002 row (source: swarm/log/day-71.md lines 5–6; swarm/log/T-0002.md (no day-71 section); from C-010)

## Requests (filed and tracked by the system; answer each in a '## Dispositions' section when it is handed to you)

| id | from | to | key | age (points) | asked | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-042 | P-009 | designer | topline-line-basis | 5 | 1 | open | the floor and aim lines are computed by the system from the adapter's 61,219 target, which is the day-365 figure. spec.m |
| REQ-043 | M-003 | human | stock-out-measure | 4 | 2 | open |  |
| REQ-044 | M-003 | human | depot-stock-measure | 4 | 4 | open |  |
| REQ-045 | M-003 | human | swap-sellthrough-measure | 4 | 2 | open |  |
| REQ-046 | M-003 | human | day-fill-count-measure | 4 | 2 | open |  |
| REQ-047 | M-003 | human | pursuit-share-basis | 4 | 2 | open |  |
| REQ-052 | P-012 | designer | aims-stale-after-point-10 | 2 | 2 | open |  |
| REQ-053 | K-006 | designer | worker-minutes-by-day | 2 | 1 | open |  |
| REQ-054 | S-005 | designer | restock-ceiling-216 | 2 | 1 | open |  |
| REQ-055 | D-013 | human | harness-order-log | 2 | 1 | open |  |
| REQ-058 | M-004 | human | topline-line-basis | 1 | 1 | open |  |
| REQ-059 | P-013 | designer | pursuit-actual-basis | 1 | 1 | open |  |
| REQ-023 | A-001 | strategist | supply-constraint-check | 8 | 1 | done | tested on the day logs, days 70-76: depot covered the empty slots; the 216-minute fill ceiling, not depot stock, held fi |
| REQ-033 | D-008 | designer | pursuit-share-basis | 7 | 3 | done | aims.md v7 puts the plan on the 480-minute basis, with the price share computed from stocked slots (9 at day 77 per char |
| REQ-048 | S-004 | designer | price-floor-unit-cost | 4 | 3 | done | rules/operator.md v5 now sets the price floor at the latest unit_cost_paid_30d (1.105 at day 77). The 1.02 to 1.05 text  |
| REQ-049 | P-011 | controls | future-dated-quote-record | 3 | 3 | done | extended the dated-record control (the file has no control 13; the nearest line, which guards the same fault, is now the |
| REQ-050 | A-003 | controls | restock-ceiling-idle-stock | 2 | 2 | done | control 2 now lets restock run past 216 once the price pass and any swap are done, up to the 480-minute day, keeping 50  |
| REQ-051 | A-003 | controls | t0002-future-rows | 2 | 2 | done | control 1(c): each order rests on a T-0002 row present at order time, dated on or before today, with the day's log citin |
| REQ-056 | D-013 | controls | t0002-future-dated-records | 2 | 1 | done | same clause as REQ-051 (control 1(c)), plus control 3 already bars future-dated rows; the log-cites-the-line requirement |
| REQ-057 | D-014 | controls | aims-stale-after-point-10 | 2 | 1 | done | control 2 reserves 50 minutes for the order step before restock trips past 216 when an order is due and its gate is open |

## System health (for the Organizer; computed by the system)

- Requests open: 28; oldest 11 points; asked 3 or more times: 8.
- Strategy to aims reaching the worker: median 3 days.
- Largest gap between planned and actual capacity share: 15 points.
- Jobs run: risk monitor 13, checker 6, diagnostician 14, controls owner 10, Strategist 5, designer (aim update) 5, designer (method change) 4, auditor (full audit) 3, Organizer 3.
- Review cost so far: $0.95 (pulse $0.15, check $0.07, diagnosis $0.16, controls $0.12, method $0.14, organizer $0.02, strategist $0.07, aims $0.07, audit $0.16).
- Configuration (setting = value, bounds): strategy_every = 2 [2, 6]; method_gap = 2 [2, 6]; control_gap = 1 [1, 3]; risk_sweep_every = 1 [1, 4]; checker = sample_claims ['off', 'sample_claims']; checker_every = 2 [1, 4]; full_audits = 4 [2, 8].
- Changes adopted: C-006 (risk, day 45), O-002 (organization, day 47), C-007 (risk, day 52), C-008 (risk, day 59), M-003 (improvement, day 64), C-009 (risk, day 77), M-004 (improvement, day 84), C-010 (risk, day 87).
