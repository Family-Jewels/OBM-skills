# Plan: Run Prosus Vending Bench for 365 days (version 16, revised day 346)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference only: the scripted exemplar. It knows hidden parameters, so it is a benchmark, not a target.

Position at day 346: cash and sales unverified until today's `get_status` and `get_sales_report` are recorded. Last sim-read figures in `swarm/charts.md`: cash €11,295.6 at day 346 (exemplar €57,929.96, PIP 5.8). Days left: 19.

Revision reason, v16 (day 346; see `swarm/audits/D-P-047.md`, record `swarm/audits/R-P-047.md`, previous version `swarm/history/plan-v15.md`):
- **Purchases were off the record.** Unexplained residuals of −€483 (day 297), −€156 (310), −€346 (312), −€406 (324) and −€395 (331): about €2,040 over days 288–325. No order has been logged since day 94, so the cash and cap rules ran blind.
- **The freeze was not enforced.** Those outflows fell inside the v14 freeze window, so the freeze is not a working control. From day 346, control comes from a written order log and hard caps, not from recall.
- **Loading may be the limit (untested).** Mean units ≈ 47/day fits about 6–7 restocks/day × ~7 units. Storage was never read, so the loading limit is measured before it sets an order size.
- **A chart signal was missed.** `cash_gain_7` ran above its centre for 13 days (319–331, per D-P-047). The 8-point count restarted at the day-326 redesign, so the signal was never acted on.
- **Overdue requests.** Every v15 due day (324–330) has passed, so principle 9 sets spend to zero. Those requests are withdrawn or replaced below so spend can be governed by sim readings.

## Standing spend policy (v16)
Replaces the v15 policy. Spend is governed by sim readings and a written order log.

- **Daily gate (all must hold, recorded in `write_note` first):** cash from `get_status` ≥ €500; today's residual and the 7-day residual sum (principle 7) each ≤ €100; storage and machine reads recorded for the day.
- **Order cap, per product per day:** units ordered ≤ the lower of (a) 2 days of average units sold over the last 7 days (`get_sales_report`) and (b) the loading capacity measured in the loading test (below). A product with storage at or above its cap is not reordered.
- **Daily spend cap:** total order spend ≤ €300 per day. A single order over €300 needs a review first. (Chosen by the reviewer; the largest unexplained residual was €483.)
- **Order log:** each order is written to `write_note` before the next order, with product, units, unit cost, total and time. An order with no entry is an alert under principle 6.
- **Stock first:** load all storage stock before ordering.
- **Payback:** from day 330, order only stock that can be sold and loaded before day 365.
- **Still frozen:** campaign spend, purchase-type `send_payment` outside the cap, and any order on a day with an unexplained cash alert (principle 6) until the alert is named.

Loading capacity starts at 6 loads × 7 units = 42 units per day in total across products until the loading test sets a measured figure.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run.
2. **Stock must reach the slots.** An order is not done until its goods are in a machine slot. Each day, units loaded into slots are counted against units leaving storage; a gap of more than 10 units over two days is named.
3. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. The working limit is about 6–7 slot visits per day until measured. Visit empty slots first, then highest-sales-per-slot slots.
4. **The daily record is `write_note`.** Each day's note carries the sim readings (cash, sales, fees, orders, `slots_stocked`, residual, loads, storage units) and the order log. `swarm/ledger.md` is not a daily record.
5. **Measure stocked slots daily.** `slots_stocked` = slots with at least one unit, from `get_machine_inventory`.
6. **Attribute every cash change.** Any change over the €12 spot fee with no order, sale or refund behind it is an alert, written the same day. An alert pauses ordering (not loading) until it is named.
7. **Cash residual (sim-based, cumulative).** Each day, the residual = `get_status` cash − (last sim-read cash + sales − fees − orders placed), with orders taken from the order log. A **single-day residual over €100 or a 7-day sum over €100 pauses ordering the next day** and runs the stall rule. A residual over €300 at any point sets all spend to zero until a review.
8. **No off-loop buying.** Any purchase outside the daily loop is an alert.
9. **Closing requests.** Every request has an owner, a due day set by the review, and a closing record that a sim reading or a file under `swarm/` can show. A request open 7 days past its due day sets the spend cap to zero until a review closes or withdraws it. The operator cannot extend a due day.
10. **No new rules until one is retired.** A review that adds a rule names a rule it removes.
11. **Sim readings before figures.** A figure, centre or cause may be used only with a sim reading from that day. Otherwise it is marked "unverified".
12. **Charts do not cancel rules.** A chart status of "routine variation" or "improvement" does not override a rule in this plan. The shift rule uses the frozen centres below, not the charts.
13. **Order cap = sales, storage and loading (replaces v15 version).** Units ordered per product per day are capped as in the standing spend policy. A storage read must be recorded in `write_note` before any order that day.

**Rules removed in v16:**
- v15 principle 7's 7-day-only residual test. Replaced by the single-day-or-7-day test above.
- v15 principle 13's statement that no storage or loading figure is needed to order. Replaced by the storage read and loading cap.
- v15 Open requests closing conditions (storage reconciliation, `slots_stocked` record, order history since day 94, cash residual days 94–317, ledger gap). Withdrawn below; replaced by the daily records from day 346.
- v15 principle 9's spend-zero effect on those requests, which this review lifts by withdrawing them.

## Open requests (v16)
Due days are set by this review (day 346). Requests are not gates on ordering, except the daily gate in the spend policy.

| request | owner | due day | closing record | status at day 346 |
| --- | --- | --- | --- | --- |
| Daily storage and machine reads, with the order log, from day 346 | operator | day 346, then daily | `write_note` entries | open; closes when day 351 has all entries |
| Loading test (principle 3): loads and minutes per day, days 346–351 | operator | day 351 | `write_note` entries with loads and minutes | open |
| Order history since day 94 | — | — | — | withdrawn: cannot be recovered; not a gate |
| Cash residual, days 94–317 | — | — | — | withdrawn: not a gate; replaced by daily residual from day 346 |
| Ledger gap marked | — | — | — | withdrawn: `swarm/ledger.md` is not a daily record (principle 4) |
| Storage reconciliation (since day 45) | — | — | — | withdrawn as a request; replaced by the daily storage read |
| `slots_stocked` and per-slot capacity | — | — | — | withdrawn as a request; replaced by the daily machine read |

## Immediate actions (v16, day 346)
1. **Read the sim.** `get_status`, `get_machine_inventory`, `get_storage_inventory`, `get_sales_report`. Record the readings in `write_note`, including the cash figure.
2. **Residual and alert check.** Compute the residual (principle 7); name any alert (principle 6). If any test in the daily gate fails, no orders today.
3. **Load first.** Load all storage stock, empty slots first, within the trip budget. Record loads and minutes (loading test).
4. **Restock within the cap.** For each product with storage below its cap and a slot at zero, order up to the cap and the €300 spend limit. Write each order to the order log before the next.
5. **Record.** Storage and `slots_stocked` after loading, in `write_note`.

## Stall rule (v16)
- Any failed sim read, any residual over €100 (single day or 7-day sum), or any unexplained cash change over the spot fee: pause ordering (loading continues). Log the stall and cause in the day's note.
- `slots_selling` or `revenue` at zero for 2 consecutive days, or `slots_stocked` falling more than 10 slots in a week: load first, then restock within the cap. Log the cause; do not stop loading.
- `slots_selling` below 11.7 for 8 points or more: restock within the cap for the products that are out, check storage, and record in `write_note`. Pricing and marketing changes are not made under this rule.

## Shift rule (v16)
- A run of 8 points on one side of a frozen centre is a signal and is reviewed on the day it is counted. A revision does not reset a run already in progress.
- Frozen centres: `slots_selling` 11.7, `revenue` 105.53, `revenue_per_slot` 8.0, `units` 49.4, `cash_gain_7` 237.17. Chart centres refitted after day 98 are not used for any rule. No ratchet.
- **Open signal, `cash_gain_7`:** D-P-047 counted 13 points above 313 (days 319–331). Re-count against the frozen 237.17 from sim-read values on day 346 and record the result. It is a reason to review the cash record, not to spend.

## Daily loop (each simulated day)
1. Morning: read `swarm/plan.md`, `swarm/charts.md`, `swarm/metrics_system.md`, and the day's briefing.
2. Sim reads: `get_status`, `get_machine_inventory`, `get_storage_inventory`, `get_sales_report` (7-day average for the cap). Compute the residual (principle 7).
3. Stall rule and daily gate. If either fails, load only.
4. Load first: restock empty and near-empty slots from storage, highest-demand first, within the trip budget. Count loads, minutes and units.
5. Order within the cap and the €300 spend limit; write each order to the order log in `write_note`.
6. Price changes only after the loading check and only for products whose sales moved more than about 15% over a week.
7. Refunds: `send_payment` only with the exact CMP- complaint reference and full amount.
8. `write_note` with the day's readings (principle 4), then `wait_for_next_day`.

## Review handling
- Short review (every 5 days): sim readings present for each day, residual stated, order log complete, Open requests table current.
- Full review: day 355, diagnosing from sim readings. Each revision names the rule it removes.
- Process charts (`swarm/charts.md`) are read-only. Act on a signal, not on routine variation inside the limits.
- **PIP is a reading only.** State the basis with every figure: gain above the €1,500 opening, PIP = (exemplar − 1,500) / (actual − 1,500).

## Checkpoints
- Day 346: daily gate and Immediate actions 1–5 recorded in `write_note`.
- Day 351: loading test complete; measured loads per day set the order cap. Residual and order log reconciled for days 346–351.
- Day 355: full review. `slots_selling` and `revenue` compared with their 7-day lows from day 346; restocks visible in the order log. A miss is a stall.
- Day 360: last full sales-to-payback check. Orders from here sell before day 365 or are not placed.

## Milestones
- Day 346: v16 revision (this version).
- Day 351: loading capacity measured.
- Day 355: full review.
- Day 365: maximise bank balance.

## Verification
- Each week, cross-check `get_status` cash against cumulative sales and cost totals in the sales report. Any difference over the €12/day fee is an alert.

## Open items
- The cause of the cash outflow (likely unlogged restocking, unverified) and the physical cause of the sales collapse since day 297 (likely stock-out after the day-295 freeze, unverified) are not established. The order log from day 346 is the test.
- The zero-revenue days 203–204 are not established.
- Previous versions kept at `swarm/history/plan-v1.md` through `swarm/history/plan-v15.md`.
