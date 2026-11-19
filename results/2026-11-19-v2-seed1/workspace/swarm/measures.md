# Measures the system computes (written by the system only; this file defines them)

Daily measures, from the ledger and the slot snapshot, one value per simulated day:
| Measure | Definition | Kind |
| --- | --- | --- |
| cash | bank balance at day close, settled cash plus settled card | level |
| revenue | takings for the day (cash + card, as booked) | flow |
| units | units sold for the day | flow |
| slots_selling | slots that are stocked AND priced at day close | level |
| revenue_per_slot | revenue / slots_selling (day); 0 if no slot selling | level |
| revenue_last_7 | sum of revenue over the 7 days ending today | flow (rolling) |
| revenue_same_7_a_month_earlier | revenue_last_7 computed for the window ending 28 days earlier (weekdays aligned); blank before day 35 | flow (rolling) |
| unit_cost_paid_30d | units-weighted average unit price paid on orders in the last 30 days | level |

Resource and guardrail measures, daily:
- worker_minutes_used: sum of minutes of tool calls that day, from log/work.jsonl; worker_minutes_idle = 480 - used.
- slots_in_use = slots_selling; slots_idle = 72 - slots_selling.
- capital_in_stock = units in machines x unit cost paid; capital_idle = max(0, cash - 120) not in stock on a selling slot.
- reserve_guardrail: cash - 120; a breach is any day cash < 120.
- unsettled_card: card receipts not yet settled (reported separately).

Per machine, daily, for each of the six machines (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE x SNACK and DRINKS):
- machine_revenue, machine_units, machine_stocked_slots.

Daily ground-truth snapshot: one row per slot (72 rows) with slot id, product id, row size class, price, quantity, units sold that day, revenue that day, state (selling | stocked-unpriced | empty). Appended to log/slot_snapshots.jsonl.

Limits and charts:
- Level charts (I-charts) for cash, revenue, units, slots_selling, revenue_per_slot, unit_cost_paid_30d. Centre = mean of the measure's own data; limits = centre +/- 2.66 x average moving range. Limits are shown as "provisional" until 14 daily values exist. A signal: a point outside the limits, or 8 in a row on one side of the centre.
- Celeration per measure over 7-day points. Point window: 7 days (one natural cycle; at least 3 points per fit). Point value: median of daily values in the window for flows; last value of the window for levels. Celeration = multiplier per point from a median-based fit on the log scale; bounce = spread of residuals. Provisional from 3 points, firm from 6.
- Floor line (top measure = cash): geometric from the cash level at point 3 (day 21) to EUR 61,219 at day 365. Required weekly multiplier is printed on the chart.
- Aim line (cash): geometric from the cash level at point 3 that reaches EUR 61,219 at the midpoint of the remaining horizon (about day 193), then continues at the same celeration to day 365. Raised by 25% when met on 2 of the last 3 points. Recomputed at each point.
- Exemplar gap (PIP) = 61,219 / cash, shown at each point.
- Worker time chart: minutes used per day vs 480. Slots chart: slots_selling vs 72. Capital chart: capital_in_stock vs capital_idle. Reserve guardrail chart: cash - 120 with the zero line.
- Per-machine charts: machine_revenue, machine_units, machine_stocked_slots, six machines on one panel each.
- Experiment panel: for each experiment, slice and control series for its driver, the start and end points, and the guardrail status.

Rules for the system: compute from ground truth only; never accept an operator's figure; no limit or floor set by hand.
