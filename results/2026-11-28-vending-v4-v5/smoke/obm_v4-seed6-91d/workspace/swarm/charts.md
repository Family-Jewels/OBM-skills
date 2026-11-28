# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 49 | 355.99 | 72.3 | 639.69 | 558.39 | IMPROVEMENT: 8 in a row above the centre |
| revenue | up | 49 | 99.91 | -132.14 | 331.96 | 18.4 | routine variation |
| slots_selling | up | 49 | 12.2 | -3.06 | 27.46 | 5 | routine variation |
| revenue_per_slot | up | 49 | 7.44 | -3.45 | 18.33 | 3.68 | routine variation |
| units | up | 49 | 45.95 | -59.33 | 151.23 | 8 | routine variation |
| cash | up | 60 | 3843.01 | 3628.87 | 4057.15 | 5193.61 | IMPROVEMENT: beyond the upper limit |
| unit_cost_paid_30d | down | 70 | 0.98 | 0.96 | 0.99 | 0.987 | WORSE: 8 in a row above the centre |

## Since redesign M-002 (adopted day 49): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 419.22 (73.26 to 765.18) | 418.22 | 38 | shift up: 8 in a row above the centre |
| revenue | 87.93 (-94.74 to 270.6) | 101.33 | 38 | no shift yet |
| slots_selling | 10.25 (-4.03 to 24.53) | 11.76 | 38 | no shift yet |
| revenue_per_slot | 6.54 (-2.79 to 15.86) | 7.65 | 38 | no shift yet |
| units | 41.8 (-45.56 to 129.16) | 46.58 | 38 | no shift yet |
| cash | 3396.29 (3137.44 to 3655.15) | 3902.1 | 38 | shift up: beyond the upper limit |
| unit_cost_paid_30d | 0.99 (0.97 to 1.01) | 0.98 | 38 | shift down: 8 in a row below the centre |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 91: actual 5193.61, exemplar 13787.56 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 3.3: the exemplar has gained 3.3x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 637.75 | 597.62 |
| revenue | 155.19 | 60.81 |
| slots_selling | 16.14 | 7.71 |
| revenue_per_slot | 9.81 | 6.14 |
| units | 70.86 | 27.29 |
| cash | 4898.65 | 4898.65 |
| unit_cost_paid_30d | 0.83 | 0.99 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 13 points across the horizon of 91.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 8). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 6 | x1.10 | x1.08 to x1.11 | x1.1 | x1.10 | improving |
| revenue | flow | up | 6 | x1.19 | /1.29 to x1.42 | x14.6 | x1.19 | flat |
| units | flow | up | 6 | x1.20 | /1.32 to x1.42 | x15.4 | x1.20 | flat |
| slots_selling | level | up | 6 | /1.34 | /1.42 to /1.10 | x4.0 | /1.34 | wrong way |
| revenue_per_slot | flow | up | 6 | x1.12 | /1.15 to x1.19 | x4.9 | x1.12 | flat |
| unit_cost_paid_30d | level | down | 6 | x1.00 | /1.01 to x1.01 | x1.1 | x1.00 | flat |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.44 per point from point 3. Aim line (a deliberate overshoot: 61,219 by half the remaining horizon): x2.08 per point from point 3. Falling short of the aim is expected and triggers nothing.

Latest point 13 (days 85-91): 5,193.61; floor line 61,219.00; aim line 61,219.00. Required celeration from here to the target: x11.79; actual (this phase): x1.10.

## Since the phase change at point 8

Jump (first point / old line projected): /1.01. Turn (new celeration / old): /1.06.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 180 | 75 | 480 | 16% | 405 | 1 |
| slots stocked at day end | 2 | 4 | 72 | 6% | 68 | 0 |
| capital | 13.08 | 22.11 | 5086.69 | 0% | 5064.58 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 5193.61 | ok |

## Facts measured by the system (from the harness's log of every action; cost in worker time (minutes a day); as of day 91, so the step log may already hold later calls)

Read these instead of asking: they are measured, not assumed. The last column is each action's share of the time that was spent, not of the time available; how much of the working day is in use is under Resources.

| action | calls | median cost | share of the time spent, last point |
| --- | --- | --- | --- |
| restock_machine | 410 | 45.0 | 87% |
| get_machine_inventory | 30 | 25.0 | 6% |
| get_storage_inventory | 28 | 25.0 | 4% |
| send_payment | 10 | 25.0 | 2% |
| write_note | 58 | 5.0 | 1% |
| list_emails | 20 | 5.0 | 0% |
| read_email | 10 | 5.0 | 0% |
| get_status | 3 | 5 | 0% |
| read_notes | 1 | 5 | 0% |
| get_marketing_report | 1 | 5 | 0% |
| search_web | 1 | 25 | 0% |
| check_offers | 17 | 25 | 0% |
| order_goods | 27 | 25 | 0% |
| set_reminder | 8 | 5.0 | 0% |
| wait_for_next_day | 78 | 0.0 | 0% |

## Pursuit: planned vs actual capacity split (last point; plan from swarm/aims.md)

| label | planned | actual | gap |
| --- | --- | --- | --- |
| restock_machine | 60% | 0% | -60% |
| order_goods, check_offers | 15% | 0% | -15% |
| get_storage_inventory, get_machine_inventory | 10% | 0% | -10% |
| write_note, list_emails | 3% | 0% | -3% |
| send_payment and other core work | 12% | 0% | -12% |
| other (not in the split) | 0% | 100% | +100% |

## Facts proposed by roles (not measured by the system; each with its cited source)

- Days 59 to 61: no restock_machine (source: actions.jsonl lines 508 to 512; from D-006)
- Orders on days 57, 62, 64, each after check_offers (source: actions.jsonl lines 498 to 499, 514 to 515, 542 to 543; from D-006)
- Receipts PO-1005 to PO-1009: 105 to 210 units each (source: order_goods results, transcript lines 1031, 1218, 1412, 1416 (as cited in K-002); from D-006)
- Days 71 and 73 ended with 265 and 360 minutes unused, no machine read after the last fill (source: actions.jsonl lines 586 to 593 and 603 to 607; from P-010)
- No order_goods between days 64 and 71 (source: actions.jsonl lines 542-543 and 592; from D-007)
- No get_machine_inventory on days 66, 67, 68 and 72 (source: actions.jsonl lines 550-560, 561, 595-603; from D-007)
- Day 68: no restock and no inventory read, about 470 minutes unused; whether depot stock was present is unverified (no depot read that day) (source: actions.jsonl lines 561-562; from D-007)
- Day-70 action order: depot read at 09:25, first fill at 10:10, fills to 15:25 on day 70 (source: transcript stamps (lines 4277, 4289, 4303 to 4331); the Facts table counts calls but not their order.; from K-005)
- Stock on hand 188 (day 64) to 31 (day 77); no order after day 64 (source: charts.md Resources (capital); Facts proposed (orders on days 57, 62, 64); from S-004)
- slots_selling 7-day average, days 72 to 78: 12.7 (source: metrics_system.md rows 72 to 78; from S-004)

## Requests (filed and tracked by the system; answer each in a '## Dispositions' section when it is handed to you)

| id | from | to | key | age (points) | asked | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-005 | P-002 | designer | set-price-missing-from-facts | 11 | 2 | in_progress | set_price is in actions.jsonl (30 calls) but not in the system's Facts table, which only the system can write. Asked of  |
| REQ-007 | P-002 | designer | pursuit-table-missing | 11 | 4 | in_progress | the Pursuit table now exists in charts.md, but its actual column is wrong: it reads restock_machine 0% and "other" 100%, |
| REQ-008 | M-001 | human | day7-measure-backfill | 11 | 5 | open |  |
| REQ-009 | D-002 | designer | stock-cover-vs-fill-rate | 10 | 6 | in_progress | reopened by A-001 after 'done: spec.md v3, section "Depot cover": the depot holds the next day's fills (about 1' |
| REQ-011 | P-004 | human | pursuit-table-missing | 9 | 5 | open |  |
| REQ-012 | D-003 | designer | supplier-choice-aim | 8 | 4 | in_progress |  |
| REQ-014 | M-002 | human | day-row-completeness-check | 6 | 1 | open |  |
| REQ-015 | M-002 | human | set-price-missing-from-facts | 6 | 1 | open |  |
| REQ-016 | M-002 | human | depot-units-charted | 6 | 6 | open |  |
| REQ-019 | A-001 | designer | m001-miss | 6 | 1 | in_progress |  |
| REQ-020 | A-001 | controls | c002-review-due | 6 | 2 | in_progress | reopened by A-002 after 'done: Reviewed C-002's fill check: it still fires on most day-ends (days 37, 39, 43, 4' |
| REQ-021 | A-001 | human | floor-target-61219 | 6 | 2 | open |  |
| REQ-022 | A-001 | human | m001-verdict-record | 6 | 2 | open |  |
| REQ-023 | D-005 | designer | read-budget-vs-controls | 4 | 2 | in_progress |  |
| REQ-024 | D-005 | controls | idle-minutes-with-depot-stock | 4 | 3 | in_progress | reopened by D-006 after 'done: C-002 now gates wait_for_next_day on a day's get_machine_inventory read; review ' |
| REQ-025 | K-004 | human | day56-sales-vs-simulator-report | 4 | 1 | open |  |
| REQ-026 | A-002 | controls | c003-review-due | 3 | 1 | in_progress |  |
| REQ-027 | D-006 | controls | faults-depot-stall-no-orders-precheck-skipped-b | 3 | 1 | in_progress |  |
| REQ-028 | D-007 | controls | faults-unit-cost-signal-worse-idle-minutes-with | 1 | 1 | open |  |
| REQ-029 | S-004 | designer | top-line-horizon-mismatch | 1 | 1 | open |  |

## Change verdicts (judged by the system with the protocol's signal rule; chance = the same test where nothing changed)

| change | adopted | prediction | window | verdict | chance |
| --- | --- | --- | --- | --- | --- |
| M-001 | day 20 | slots_selling up within 2 points | 21-34 | shift as predicted |  |
| M-002 | day 49 | slots_selling up within 10 points | | pending | |

## System health (for the Organizer; computed by the system)

- Requests open: 22; oldest 12 points; asked 3 or more times: 8.
- Strategy to aims reaching the worker: median 5 days.
- Largest gap between planned and actual capacity share: 60 points.
- Jobs run: risk monitor 11, checker 5, diagnostician 8, controls owner 6, Strategist 4, designer (aim update) 4, designer (method change) 3, auditor (full audit) 3, Organizer 3.
- Review cost so far: $1.19 (pulse $0.17, diagnosis $0.20, check $0.32, controls $0.07, method $0.06, organizer $0.02, strategist $0.06, aims $0.06, audit $0.23).
- Configuration (setting = value, bounds): strategy_every = 2 [2, 6]; method_gap = 3 [2, 6]; control_gap = 1 [1, 3]; risk_sweep_every = 1 [1, 4]; checker = sample_claims ['off', 'sample_claims']; checker_every = 2 [1, 4]; full_audits = 4 [2, 8].
- Changes adopted: C-001 (risk, day 18), M-001 (improvement, day 20), C-002 (risk, day 30), C-003 (risk, day 45), M-002 (improvement, day 49), O-002 (organization, day 53), C-004 (risk, day 63), C-005 (risk, day 75).
- Change verdicts: 1 judged, 1 shifted as predicted against 0.0 expected by chance; 0 could not be judged as written.
