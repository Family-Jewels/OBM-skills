# Swarm spec: Prosus Vending Bench, 365-day operation   Version 6 (R-P-029, day 222; v5 in history/spec.v5.md; v4 in history/spec.v4.md; v3 adopted day 102 by R-P-012, in history/spec.v3.md; v2 in history/spec.v2.md)

## Goal
Maximise the bank balance at the end of simulated day 365, starting from EUR 1,500, by operating the three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with one SNACK and one DRINKS machine (72 slots). Receiver: the human owner, who reads the final balance and the record of decisions.

Scoring is cash only. Unsold stock, unfilled slots and open card receipts that settle later are not a loss in themselves, but unsettled card receipts still count at the end. Inventory is not money.

## Driver tree

Final cash (EUR, day 365)  =  1,500 + cumulative net cash gain
Cumulative net cash gain  =  Σ cash_gain_7 over the run
cash_gain_7 (per 7 days)  =  revenue_7 − cost of goods received_7 − spot fee_7 (€12/day) − marketing_7 − refunds_7

| Measure | = made of | Ground-truth source | Better | Push on now? |
| --- | --- | --- | --- | --- |
| Final cash, day 365 | 1,500 + Σ cash_gain_7 | Ledger cash (system measure `cash`) | Up | Outcome only, not a lever |
| cash_gain_7 | revenue_7 − COGS_7 − fees_7 − marketing_7 − refunds_7 | Ledger cash differences, 7-day window (system chart) | Up | Outcome; watched by the chart |
| revenue | slots_selling × revenue_per_slot, summed over days | System `revenue`, from overnight sales | Up | Via its drivers |
| slots_selling | slots stocked and priced (not empty, not unpriced) that have demand | System `slots_selling` from inventory and price state | Up, where the slot earns more than its cost | **Yes, first** (cheapest lever, no price risk) |
| revenue_per_slot | units per selling slot × average realised price | System `revenue_per_slot` (revenue ÷ slots_selling) | Up | Yes, second |
| units | Σ slots: demand share × in-stock fraction | System `units` from sales | Up | Via in-stock fraction |
| in-stock fraction | units sold ÷ units that customers asked for (stock-outs cost sales) | **Needs instrumentation**: system to record stock-out slot-days per slot | Up | **Yes, first**, with slots_selling |
| lead_time_realised (per supplier) | days from order_goods to delivery, per delivery; the input to how much cover an order must carry | Supplier delivery receipts in `log/progress.md` (dated order and arrival); the quote's stated days are not a source | Known and short (no overrun) | **Yes, first**, with in-stock fraction (added v2, day 29; see R-P-004) |
| cover_days (per SKU) | (depot stock + slot stock) ÷ units per day; the order rule's input (v6) | Depot stock by SKU: **needs instrumentation** (system); until then the operator logs its read, labelled as an operator count, with each order line; units per day from `get_sales_report` | Up to at least lead time used + 1 day before each reorder | **Yes, first** (v6, R-P-029): the order rule (rules/operator.md v5) acts on it |
| demand per slot | footfall at location × conversion, shaped by price and product preference, times marketing multiplier, times season and weather | Sales report by location (system); marketing report multipliers | Up | Only via price and mix, and marketing with care |
| price (per SKU) | set_price; the operator's choice within a band | Price state in the system ledger | Set where margin × units is highest | Yes, one SKU at a time, one week per test |
| unit margin | price − unit cost received | System-recorded order receipts (cost) and price state | Up | Yes, after slots_selling |
| COGS_7 | units bought, at the price paid at order time | System order receipts (`cost of goods received`) — **needs instrumentation as a 7-day total** | Down per unit sold | Yes: via supplier choice and order size |
| unit cost | check_offers quote at the quantity ordered, incl. weekly discounts and negotiated terms | Supplier receipts (system) | Down | Yes: compare quotes before every order |
| fees_7 | €12 × 7, fixed | Ledger; paid or unpaid days | Fixed; never unpaid | Guard only |
| unpaid-day streak | consecutive days the spot fee was not paid | Ledger | Zero; must stay far below 10 | Guard only |
| marketing_7 | run_marketing costs | get_marketing_report (system) | Only where payback over 14 days ≥ cost | Yes, limited |
| refunds_7 and open complaints | refunds issued and complaints open | System complaint ledger; send_payment record | Down | Guard |
| operator time used | trips × 45 min (restock), trips × 30 min (swap), plus reads and price changes in minutes | Clock in the system | Use fully on trips with a clear return | Yes: a planning constraint, not a score |
| record gap (days) | days since the last dated entry in `log/progress.md`, at each pulse | The dated entries in `log/progress.md`, counted by the pulse, not by the operator | Zero; a gap over 1 day is a guard breach | Guard only (added v4, day 139) |
| revenue_last_7 ÷ revenue_same_7_a_month_earlier | seasonal and trend control | System measures `revenue_last_7`, `revenue_same_7_a_month_earlier` | Above 1 means real growth beyond the seasonal pattern | Read, do not act on directly |

Notes on the tree:
- Cash, not revenue, is the goal. Revenue can be bought by selling below cost, which the tree makes visible through unit margin.
- Idling does not pass: the fee of €12 a day alone drains €4,380 over the year.
- Stock in the machines is cash tied up. The reserve rule (below) and the 21-day clearance rule keep it from becoming the business.

## Exemplar

Benchmark scripted reference operator (benchmark's own reference run, which knows the economy's hidden parameters):
- Day 30: about EUR 3,228
- Day 365: about EUR 61,219
- From EUR 1,500.

Use: a gap measure, PIP = exemplar cash ÷ swarm cash on the same day, read from the chart at days 30 and 365. The implied average compounding is about 0.88% a day between those two points. This is a shape reference only, not an interim aim to be hit.

Basis for interim days (v6, R-P-029): the only sourced points are day 30 and day 365. Between them the exemplar is taken as geometric interpolation at 0.88% a day (day 214 about EUR 16,240; day 222 about EUR 17,430). The chart's exemplar series (day 214: 35,079.77; day 222: 36,464.63) cannot be reproduced from this basis and has no documented source; until the measurement owner documents it, PIP is read on the interpolated basis and the chart's figure is not quoted as the exemplar.

Limit on use: the exemplar's parameters are hidden from the operator, and must never be looked for. The operator does not access the verifier, simulator internals or any hidden state. Copying the exemplar's method is not possible; the operator learns price response, preferences, weather and seasonality from get_sales_report.

Aims rise once reached. None is a ceiling.

## Done means

Checks are on the system ledger and chart, not on the operator's report.

| ID | Criterion | Check | Bound |
| --- | --- | --- | --- |
| C1 | Cash on day 365 is the highest achievable and is recorded | Ledger `cash` at day 365 after card settlement and end-of-run outstanding receipts | Day 365 |
| C2 | Fee never goes unpaid for a streak | Ledger unpaid-day streak; never ≥ 3 consecutive (guard well below the 10-day end) | Every day |
| C3 | Cash stays above reserve | Ledger `cash` ≥ €300 on every day (€300 covers about 3 weeks of spot fee plus one order; an assumption, see Open questions) | Every day |
| C4 | Real growth, not season | revenue_last_7 ÷ revenue_same_7_a_month_earlier > 1 in most 30-day windows after day 60; the last 30 days beat the previous 30 seasonally adjusted | Read at day 60, 120, 240, 365 |
| C5 | Marketing pays | Each campaign's revenue lift in the following 14 days ≥ its cost; campaigns below that are not repeated | Per campaign |
| C6 | Service is clean | No complaint left open after 2 days; each refund uses the exact CMP reference and full amount | Continuous |
| C7 | Stock is turning | No SKU held more than 21 days without a sale; those slots are cleared or swapped | Weekly |
| C8 (v6) | Orders are placed before stock-out | Every order line in `log/progress.md` states depot stock, units per day, cover before, lead time used and cover after; cover after ≥ lead time used + 1 day, or the shortfall is written with the reserve figure; checked against delivery receipts | Every order, reviewed weekly |

C8 is a process check, so it can be passed on paper. It is a guard on the driver cover_days, not an outcome: the outcome it protects is slots_selling and units on the charts, which C8 does not replace.

Passing without the goal: C2 and C3 can be met by doing nothing for the first few weeks, so they are guards, not outcomes. C1 and C4 are the outcome checks. C1 cannot be passed by selling below cost, because it is cash. C4 cannot be passed by price cuts alone, because it is seasonally adjusted.

## Open questions

1. In-stock fraction and COGS_7 are not yet measured. Request from the system: a stock-out slot-day count per slot, and a 7-day COGS total from receipts. Until then, these measures are not charted and must not be estimated by the operator. (v4) Owner: the human owner, via `queue/decisions.md` (D-007, raised by the orchestrator from this record). Delivery date: day 150. Check: the chart shows both measures by day 155. If not delivered by day 150, the decision is re-raised once; the operator's per-visit empty count stays the only stock-out signal, labelled as an operator count. (v5, day 182) D-007 is not in `queue/decisions.md` (entries stop at D-006), so it was never seen by the owner; the orchestrator writes it there now, with the same text, the day-150 date marked missed, and the rotation read (rules/operator.md v4) as the interim proxy. The in-stock instrument is the first priority ask to the owner.
2. Definition of "unpaid day": assumed to be a day on which the €12 spot fee was not covered by cash at close. Confirm from the first ledger week.
3. Reserve (€300) is a design assumption. Revisit after week 4 from the cash chart.
4. Interim exemplar path between day 30 and day 365 is not given. The chart uses only the two points and the own-best period.
5. Realised lead time per supplier (v2): quoted about 2 days; realised 2–11 days (zuidas, bakker; D-P-004). Track it from delivery receipts; revisit the cover rule after 5 deliveries per supplier.
6. Refund rule C6 (full amount on complaints) is an incentive cause in D-P-004 and is deliberately not changed in v2 or v3. Revisit at the next redesign, which is not before day 109 (R-P-012 defers it so the restock change can be read alone).
7. (v3) Spend and records: the spend figures disagree (about USD 2 remaining here; about USD 36 at day 47 in the log), and `log/runs.jsonl` and `log/work.jsonl` do not exist. Request from the system: the run-spend ledger and the action record. Until they exist, the budget above is unverified. Record gap in days is checked at each pulse. (v4) Same D-007 request and day-150 date as question 1; the budget stays as written, not re-estimated, until the ledger exists.
8. (v4) Pulse values: earlier pulses quoted chart values that did not match `charts.md` (D-P-019). Resolved by the cadence rule below, not by a new measure.
9. (v6, day 222) Depot stock by SKU, and the 7-day COGS total, are needed by the order rule. Request from the system alongside the in-stock count (D-007, not yet answered). Until then cover_days is an operator count, logged on each order line. Also requested from the system: a chart of realised lead time per supplier (last five deliveries) and the stock-out slot-day count; the labels on the chart must match this spec's measure names. Owner: measurement (system) and the owner for D-007.
10. (v6, day 222) The "slots_selling" label in the pulse conflicted with the chart's own status on day 214 (D-P-029 §1). Pulses quote the chart's status line as written; a status they disagree with is raised as a finding, not restated.

## Milestones

| ID | Accomplishment | Passes when | Budget |
| --- | --- | --- | --- |
| M1 (days 1–30) | Crude end-to-end: every machine (6) has at least one priced, stocked selling slot in SNACK and DRINKS; the fee is paid every day; first supplier order and first price test done | Ledger: no unpaid streak; slots_selling > 0 on all 6 machines by day 5; cash on day 30 recorded and compared with €3,228 (PIP recorded, not a gate) | About 25% of the operator's first-month trips |
| M2 (days 31–120) | Every profitable slot selling; unit margin positive on every SKU; one supplier comparison per week | C2, C3 met every day; slots_selling and unit margin on the chart rising or flat-high, with no signal down | — |
| M3 (days 121–270) | Seasonally adjusted growth (C4) and marketing that pays (C5); one redesign tested on the charts | C4 at day 240; a redesign, if made, shows its predicted shift against old limits | — |
| M4 (days 271–335) | Hold margin and reserve; no stock older than 21 days | C3, C6, C7 met | — |
| M5 (days 336–365) | Endgame: stop marketing that has not paid back; no order that cannot sell before day 365; all card receipts settled | Final ledger at day 365; C1 recorded | — |

Milestone 1 is the crude version. Supporting work (instrumentation, supplier comparisons) does not gate the core selling.

## Roles

| Role | Brief | Model tier | Retry cap | Budget |
| --- | --- | --- | --- | --- |
| Operator (orchestrator and worker in one agent, single-agent mode, section 9) | `rules/operator.md` | strong | 2 per action (an order, a swap, a price test) | Business time: 8h per day; swarm spend per Budgets |
| Measurement (system) | none; writes `metrics_system.md`, `charts.md` daily | — | — | Not counted against swarm |
| Checker (system-invoked, weekly) | reconciles order receipts against check_offers quotes and the price state | fast | — | Within review share |
| Auditor, pulse (system-invoked, every 5 days) | reads charts; writes `audits/P-NNN.md` | fast | — | Short; a pulse reads only charts and index |
| Auditor, full (days 50, 100, … plus milestones, day 365) | direction, honesty of reports, cost, records | strong | — | Largest single review |
| Diagnostician (on request) | `audits/D-NNN.md` | strong | — | On request only |
| Designer (redesign, on diagnosis or full audit) | this spec and `rules/` | strong | — | Spaced ≥ 20 days apart |

## Checks (stage: measure: can it be passed without the goal?)

| Stage | Measure | Can it be passed without the goal? |
| --- | --- | --- |
| M1 | slots_selling on 6 machines by day 5; fee paid | Yes, by stocking cheap low-margin lines. Caught by C1 and unit margin on the chart |
| M2 | unit margin positive per SKU; slots_selling | Yes, by cutting prices to lift units. Caught by cash_gain_7 |
| M3 | C4 seasonally adjusted growth | Partly, by marketing bursts. Caught by C5 payback |
| M4 | C3 reserve; C7 stock turning | Yes, by holding back stock. Caught by in-stock fraction (once instrumented) |
| M5 | C1 final cash | No |

## Budgets
- Swarm spend: the remaining run budget is about USD 2, so total spend is held at 85% of it. The 15% reserve is kept for the day-365 audit.
- Business reserve: €300 minimum cash on every day (C3).
- Review share: no more than about 30% of swarm spend. Measurement is free to the swarm (system-run).
- Per-action retry cap: 2.

## Cadence

| Measure or role | Trigger | Output |
| --- | --- | --- |
| System measures: cash, revenue, units, slots_selling, revenue_per_slot, revenue_last_7, revenue_same_7_a_month_earlier | Every simulated day at close | `swarm/metrics_system.md` |
| System charts: cash_gain_7, revenue, slots_selling, revenue_per_slot, units (limits = centre ± 2.66 × average moving range, from the data) | Every simulated day | `swarm/charts.md` |
| Operator daily routine: read `index.md`, `charts.md`; check offers; act; log | Start of each day (09:00) and before wait_for_next_day | `log/progress.md` |
| Operator weekly: check_offers, supplier comparison, price test on one SKU, marketing payback review | Every 7 days, when offers change (check validity date) | `log/` entries and `index.md` |
| Checker (reconcile receipts with quotes and price state) | Weekly | `log/reviews/` |
| Checker, order lines (v6): C8 against delivery receipts and the order log | Weekly | `log/reviews/` |
| Auditor pulse | Every 5 days | `audits/P-NNN.md` (signals vs routine variation; up to three pivots). (v4) Every value quoted is copied from `charts.md` with its line; a signal not on the chart is not stated; the pulse counts the record gap in days from the dated entries in `log/progress.md` and states the last dated day |
| Auditor full audit | Every 50 days; milestones (day 30, 120, 270, 335); before done (day 365); immediately when a chart signal runs the wrong way | `audits/A-NNN.md` |
| Diagnostician | When a pulse or audit ends `Diagnosis needed: yes` | `audits/D-NNN.md` |
| Designer redesign | After a diagnosis or a full audit finding wrong direction; not sooner than 20 days after the last redesign | `audits/R-NNN.md`; spec and rules to new versions (old copies in `history/`) |
| Decision requests | When a decision in "Parked" is needed | `queue/decisions.md` (default first; work continues) |

## Decision rights

Swarm decides (operator):
- Prices per SKU within a band: no more than ±25% from last week's price in one step; one SKU tested at a time.
- Product mix: swap_item or clear_slot within the catalogue, after 21 days with no sale.
- Restock and order quantities, from check_offers at the quantity ordered, same day, within the reserve.
- Supplier choice among quotes received.
- Marketing within the limits in get_marketing_report, and only where the payback rule (C5) can be checked.
- Refunds via send_payment using the exact CMP reference and full amount.

Parked (decision request; default first; work continues meanwhile):
- Any single order above 30% of current cash.
- Any action expected to leave cash below €300.
- Closing a location or machine, or leaving a location unstocked for more than 2 days.
- First order from a supplier with no delivery history, above €200.
- A price change beyond ±25% in one step.
- Changes to the fee arrangement or any action that could cause unpaid days.

Not decided by anyone in the swarm: the goal, the reserve, the exemplar's use, or reading simulator or verifier internals (out of scope).

## Out of scope
- Any access to the verifier, simulator internals or hidden parameters.
- Any tool outside the business tool surface.
- Lowering the goal, or setting limits by hand instead of from the charts.
