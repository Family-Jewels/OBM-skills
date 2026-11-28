# Process behavior charts (written by the system every day; do not edit)

Limits come from each measure's own data (centre +/- 2.66 x average moving range), never from an agent. Inside the limits is routine variation: do not react to it. A signal is a point beyond a limit or 8 in a row on one side of the centre.

| measure | better | phase since day | centre | lower | upper | latest | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cash_gain_7 | up | 52 | 453.23 | 202.16 | 704.3 | 544.09 | routine variation |
| revenue | up | 52 | 143.49 | -90.13 | 377.11 | 26.4 | routine variation |
| slots_selling | up | 52 | 14.65 | 8.07 | 21.23 | 8 | WORSE: beyond the lower limit |
| revenue_per_slot | up | 52 | 9.5 | -2.59 | 21.59 | 3.3 | routine variation |
| units | up | 52 | 60.95 | -26.13 | 148.03 | 11 | WORSE: 8 in a row below the centre |
| cash | up | 62 | 4633.98 | 4453.92 | 4814.04 | 5836.21 | IMPROVEMENT: beyond the upper limit |
| unit_cost_paid_30d | down | 69 | 1.13 | 1.1 | 1.15 | 1.095 | IMPROVEMENT: beyond the lower limit |

## Since redesign M-002 (adopted day 52): judged against the limits from before it

| measure | before: centre (limits) | since: mean | points | shift |
| --- | --- | --- | --- | --- |
| cash_gain_7 | 381.18 (113.34 to 649.02) | 416.62 | 40 | shift up: 8 in a row above the centre |
| revenue | 136.92 (7.84 to 266.0) | 123.33 | 40 | no shift yet |
| slots_selling | 14.0 (8.12 to 19.88) | 12.28 | 40 | shift down: beyond the lower limit |
| revenue_per_slot | 9.81 (1.52 to 18.11) | 9.72 | 40 | no shift yet |
| units | 59.8 (3.8 to 115.8) | 51.73 | 40 | shift down: 8 in a row below the centre |
| cash | 4060.89 (3827.66 to 4294.11) | 4613.72 | 40 | shift up: beyond the upper limit |
| unit_cost_paid_30d | 1.05 (1.02 to 1.08) | 1.09 | 40 | shift up: beyond the upper limit |

## Gap to the exemplar (PIP = exemplar gain / actual gain)

cash at day 91: actual 5836.21, exemplar 13787.56 (the benchmark's scripted reference operator, which knows the economy's hidden parameters). PIP = 2.8: the exemplar has gained 2.8x as much.

## Own best (7-period average)

| measure | best so far | latest |
| --- | --- | --- |
| cash_gain_7 | 696.21 | 474.1 |
| revenue | 180.29 | 89.36 |
| slots_selling | 17.71 | 9.57 |
| revenue_per_slot | 10.95 | 9.0 |
| units | 80.0 | 36.0 |
| cash | 5585.35 | 5585.35 |
| unit_cost_paid_30d | 0.91 | 1.11 |

## Progress: celeration (written by the system; do not edit)

Point window: 7 periods per point: whole cycles of 7, at least 3 observations each, 13 points across the horizon of 91.

Celeration is the multiplier per point (7 days), fitted on the log scale in the current phase (since point 8). Range: the middle half of the pairwise slopes. Bounce: the envelope at +/- 2 SD, top / bottom. Provisional below 6 points.

| measure | kind | better | points | celeration | range | bounce | own best | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cash | level | up | 6 | x1.08 | x1.08 to x1.10 | x1.2 | x1.08 | improving |
| revenue | flow | up | 6 | /1.06 | /1.20 to x1.04 | x2.6 | /1.06 | flat |
| units | flow | up | 6 | /1.10 | /1.26 to x1.01 | x3.2 | /1.10 | flat |
| slots_selling | level | up | 6 | /1.29 | /1.29 to /1.05 | x2.6 | /1.29 | wrong way |
| revenue_per_slot | flow | up | 6 | x1.01 | /1.04 to x1.09 | x1.8 | x1.01 | flat |
| unit_cost_paid_30d | level | down | 6 | x1.02 | x1.01 to x1.03 | x1.1 | x1.02 | wrong way |

## Top measure: cash

Floor line (minimum celeration to reach 61,219 by the horizon): x1.45 per point from point 3. Aim line (a deliberate overshoot: 61,219 by half the remaining horizon): x2.09 per point from point 3. Falling short of the aim is expected and triggers nothing.

Latest point 13 (days 85-91): 5,836.21; floor line 61,219.00; aim line 61,219.00. Required celeration from here to the target: x10.49; actual (this phase): x1.08.

## Since the phase change at point 8

Jump (first point / old line projected): /1.14. Turn (new celeration / old): /1.13.

## Resources (used / available, written by the system; median over the last 7 days)

| resource | latest | median used | available | in use | idle | days unused (of last 7) |
| --- | --- | --- | --- | --- | --- | --- |
| worker time (minutes a day) (the capacity of the work) | 220 | 195 | 480 | 41% | 285 | 0 |
| slots stocked at day end | 8 | 8 | 72 | 11% | 64 | 0 |
| capital | 299.52 | 399.53 | 6015.73 | 7% | 5616.2 | 0 |

Measured by the system from ground truth, never from an agent's log: worker time (minutes a day): the simulator's own clock, read by the system just before each working day ends (09:00 to 17:00; a day the worker's calls ran past 17:00 counts as all used); slots stocked at day end: the simulator's machine state; capital: the simulator's balance and the cost of stock on hand.

## Guardrails (a side that must not be crossed; experiments stay inside them)

| guardrail | rule | latest | status |
| --- | --- | --- | --- |
| cash reserve: 120 covers the fees for the days the building tolerates unpaid | cash >= 120.0 | 5836.21 | ok |

## Facts measured by the system (from the harness's log of every action; cost in worker time (minutes a day); as of day 91, so the step log may already hold later calls)

Read these instead of asking: they are measured, not assumed. The last column is each action's share of the time that was spent, not of the time available; how much of the working day is in use is under Resources.

| action | calls | median cost | share of the time spent, last point |
| --- | --- | --- | --- |
| restock_machine | 413 | 45 | 68% |
| get_sales_report | 87 | 25 | 12% |
| get_storage_inventory | 76 | 25.0 | 10% |
| write_note | 60 | 5.0 | 3% |
| get_status | 79 | 5 | 2% |
| get_machine_inventory | 32 | 25.0 | 2% |
| send_payment | 10 | 25.0 | 2% |
| list_emails | 18 | 5.0 | 0% |
| read_email | 6 | 5.0 | 0% |
| search_web | 1 | 25 | 0% |
| check_offers | 36 | 25.0 | 0% |
| order_goods | 37 | 25 | 0% |
| wait_for_next_day | 88 | 0.0 | 0% |
| set_price | 87 | 5 | 0% |
| swap_item | 2 | 30.0 | 0% |

## Pursuit: planned vs actual capacity split (last point; plan from swarm/aims.md)

| label | planned | actual | gap |
| --- | --- | --- | --- |
| Source and buy | 40% | 10% | -30% |
| Restock slots | 35% | 68% | +33% |
| Pay, price and read | 20% | 19% | -1% |
| Notes and day close | 5% | 3% | -2% |
| other (not in the split) | 0% | 0% | +0% |

## Facts proposed by roles (not measured by the system; each with its cited source)

- Restock share of time spent 64% of the median 290 minutes used is about 186 minutes, about 39% of 480 (source: swarm/charts.md, Pursuit (last point) and Resources (latest 290, median used 290); from C-007)
- slots_selling under its centre of 14 for five consecutive days, 66 to 70 (values 11, 11, 11, 10, 11) (source: swarm/metrics_system.md, slots_selling column, rows 66 to 70; from C-007)
- Cash was at least 2,907 at every close from day 43 to day 70 (source: swarm/metrics_system.md, cash column, rows 43 to 70; from C-007)
- Restock is about 40% of available minutes (67% of 290 spent) (source: swarm/metrics_system.md Resources; swarm/charts.md Pursuit table; from D-014)
- controls item 8 cites 40% for restock; aims AS-004 gives 35% (source: swarm/controls.md item 8; swarm/aims.md Capacity split; from D-014)
- The day-75 row has cash 4880.65. Deducting PO-1034's €125.20 gives 4755.45, matching the worker's D75 "Cash 4755 after order". (source: swarm/metrics_system.md, row 75; swarm/log/progress.md, D75 line; from K-006)
- The day-76 and day-77 rows have units 30 and 12, matching the worker's sales reads for D75 and D76 (30 and 12 units), and their cash matches the worker's opening cash for those days. This supports the (source: swarm/metrics_system.md, rows 76 and 77; swarm/log/progress.md, D76 and D77 lines; from K-006)
- Cash rose from 4,564.25 (day 71) to 4,889.55 (day 77), about 54 a day; at that pace day 91 is about 5,650 (source: swarm/metrics_system.md, rows for days 71 and 77; from S-005)
- Steps record for order_goods holds ok and output length only, no price (source: steps.jsonl (tool mcp__vending__order_goods, fields ok and out); from D-015)
- Restock median 186 of 480 minutes (39%) on the spec basis (source: charts.md Resources and Pursuit; spec.md Resources; from D-015)

## Requests (filed and tracked by the system; answer each in a '## Dispositions' section when it is handed to you)

| id | from | to | key | age (points) | asked | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-045 | S-004 | designer | restock-cap-sourcing-first | 3 | 4 | open |  |
| REQ-046 | S-004 | designer | top-lines-day91 | 3 | 1 | open |  |
| REQ-047 | D-012 | designer | depot-check-costs-more-than-restock | 3 | 1 | open |  |
| REQ-048 | P-013 | designer | pursuit-actual-basis | 3 | 2 | open |  |
| REQ-049 | P-014 | designer | instructions-stale-aims | 3 | 1 | open |  |
| REQ-050 | AS-004 | human | top-lines-day91 | 3 | 1 | open |  |
| REQ-051 | P-015 | designer | restock-share-35-vs-40 | 2 | 3 | open |  |
| REQ-052 | A-003 | designer | m002-verdict-window | 2 | 1 | open |  |
| REQ-053 | A-003 | designer | daily-log-line | 2 | 1 | open |  |
| REQ-054 | A-003 | controls | c006-restock-cap-judged | 2 | 1 | in_progress |  |
| REQ-055 | C-007 | strategist | restock-cap-vs-slots | 2 | 1 | open |  |
| REQ-056 | D-014 | controls | restock-share-over-control | 2 | 1 | in_progress |  |
| REQ-057 | K-006 | human | set-price-target-unmeasured | 2 | 1 | open |  |
| REQ-058 | S-005 | designer | depot-stock-charted | 2 | 1 | open |  |
| REQ-059 | D-015 | controls | faults-slots-selling-signal-down-unit-cost-risi | 1 | 1 | open |  |
| REQ-021 | D-005 | controls | unit-cost-rising | 9 | 7 | declined | no new buy control. C-003 is kept and its check fires on 31 of 32 orders; margin holds (revenue per unit about 2.2 again |
| REQ-031 | D-006 | controls | faults-restock-share-over-plan-unit-cost-rising | 8 | 2 | done | verified C-006's restock bound holds on the spec's basis (about 186 of 192 minutes, day 70); renewed its review at point |
| REQ-039 | AS-003 | controls | c002-blocks-depot-empty | 5 | 2 | declined | C-002 cannot refuse a call (it is an instruction); all 352 restock_machine calls in steps.jsonl are ok: true; the step r |
| REQ-041 | A-002 | strategist | as002-verdict | 5 | 1 | done | verdict above; split restated on spec basis; supply still the constraint. |
| REQ-042 | A-002 | controls | c001-benefit-check | 5 | 2 | done | removed C-001 at review point 7: revenue_per_slot inside limits with no signal, cash at least 2,907 at every close again |

## Change verdicts (judged by the system with the protocol's signal rule; chance = the same test where nothing changed)

| change | adopted | prediction | window | verdict | chance |
| --- | --- | --- | --- | --- | --- |
| M-001 | day 17 | slots_selling up within 3 points | 18-38 | shift as predicted |  |
| M-002 | day 52 | slots_selling up within 7 points | | pending | |

## System health (for the Organizer; computed by the system)

- Requests open: 39; oldest 12 points; asked 3 or more times: 12.
- Strategy to aims reaching the worker: median 7 days.
- Largest gap between planned and actual capacity share: 33 points.
- Jobs run: risk monitor 18, checker 6, diagnostician 16, controls owner 8, Strategist 5, designer (aim update) 5, designer (method change) 3, auditor (full audit) 3, Organizer 3.
- Review cost so far: $1.03 (check $0.07, pulse $0.16, method $0.16, diagnosis $0.22, controls $0.13, strategist $0.08, organizer $0.02, aims $0.08, audit $0.11).
- Configuration (setting = value, bounds): strategy_every = 2 [2, 6]; method_gap = 3 [2, 6]; control_gap = 1 [1, 3]; risk_sweep_every = 1 [1, 4]; checker = sample_claims ['off', 'sample_claims']; checker_every = 2 [1, 4]; full_audits = 4 [2, 8].
- Changes adopted: O-001 (organization, day 25), C-002 (risk, day 32), C-003 (risk, day 39), C-004 (risk, day 48), M-002 (improvement, day 52), C-005 (risk, day 53), C-006 (risk, day 64), C-007 (risk, day 81).
- Change verdicts: 1 judged, 1 shifted as predicted against 0.0 expected by chance; 0 could not be judged as written.
