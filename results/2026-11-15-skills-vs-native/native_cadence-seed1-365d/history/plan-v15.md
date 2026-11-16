# Plan: Run Prosus Vending Bench for 365 days (version 15, revised day 317)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference only: the scripted exemplar. It knows hidden parameters, so it is a benchmark, not a target.

Position at day 317 (from `swarm/charts.md` and `swarm/audits/D-A-006.md`; to be confirmed by today's `get_status`): cash about €9,400–9,670 (the two sources differ; use the `get_status` reading). Exemplar €52,910. Days left: 48. Sales: 7-day revenue fell from 1,021 (day 297) to 384 (day 309); units from 150 to 26 a day.

Revision reason, v15 (day 317; see `swarm/audits/D-A-006.md`, record `swarm/audits/R-A-006.md`, previous version `swarm/history/plan-v14.md`):
- The v14 freeze has become a deadlock. Stock likely ran out after the day-295 freeze stopped purchases. Principle 13 allows zero orders without a loading trace, and no trace has been recorded, so nothing can be reordered. Sales have collapsed while cash sits idle.
- The cash drain has largely stopped: residual over days 298–309 is about −€56, and `cash_gain_7` (+36.56) is inside its limits. The cash case for a total freeze has passed.
- The order history since day 94 was never recorded. Lift condition 2 and the Open requests that depend on it cannot be met, so the freeze can never lift under v14.
- Escalation (day 301) has passed. Spend is currently zero under principle 9 for the same unmet requests.
- The chart signals for revenue and units ("improvement, beyond upper limit") are on provisional limits and are not used for any rule.

## Standing spend policy (v15)
**Staged restock, replacing the total freeze.** The v14 total freeze is lifted for restock only, under these caps. Each restock is a sim-read decision, and the cap is set from sim readings, not from the ledger or the loading trace.

- **Cash gate:** cash from `get_status` ≥ €500, and the 7-day residual sum (principle 7) ≤ €100.
- **Order cap (per product, per day):** units ordered ≤ 2 days of average units sold over the last 7 days, from `get_sales_report`. A product with storage units at or above 2 days' sales is not reordered.
- **Stock first:** load all storage stock before ordering. Storage counts from `get_storage_inventory` are the loading trace; no separate trace is needed to order.
- **Payback:** from day 330, order only stock that can be sold and loaded before day 365.
- **Still frozen:** campaign spend, purchase-type `send_payment` outside the cap, and any order after an unexplained cash alert (principle 6) until the alert is named.

The freeze is lifted for the day when the cash gate and storage read are recorded in `write_note`.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run.
2. **Stock must reach the slots.** An order is not done until its goods are in a machine slot. Each day, units loaded into slots are counted against units leaving storage; a gap of more than 10 units over two days is named.
3. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. The working limit is about 6–7 slot visits per day until measured. Visit empty slots first, then highest-sales-per-slot slots.
4. **The daily record is `write_note`.** Each day's note carries the sim readings for that day (cash, sales, fees, orders, `slots_stocked`, residual, loads, storage units). `swarm/ledger.md` is not a daily record.
5. **Measure stocked slots daily.** `slots_stocked` = slots with at least one unit, from `get_machine_inventory`.
6. **Attribute every cash change.** Any change over the €12 spot fee with no order, sale or refund behind it is an alert, written the same day. An alert pauses ordering (not loading) until it is named.
7. **Cash residual (sim-based, cumulative).** Each day, the residual = `get_status` cash − (last sim-read cash + sales − fees − orders placed). The residual is summed over the last 7 days. A 7-day sum over €100 pauses ordering and runs the stall rule. A residual over €300 at any point sets all spend to zero until a review.
8. **No off-loop buying.** Any purchase outside the daily loop is an alert.
9. **Closing requests.** Every request has an owner, a due day set by the review, and a closing record that a sim reading or a file under `swarm/` can show. A request open 7 days past its due day sets the spend cap to zero until a review closes or withdraws it. The operator cannot extend a due day.
10. **No new rules until one is retired.** A review that adds a rule names a rule it removes.
11. **Sim readings before figures.** A figure, centre or cause may be used only with a sim reading from that day. Otherwise it is marked "unverified".
12. **Charts do not cancel rules.** A chart status of "routine variation" or "improvement" does not override a rule in this plan. The shift rule uses the frozen centres below, not the charts.
13. **Order cap = sales and storage (replaces v14 version).** Units ordered per product per day are capped at 2 days of average sales (`get_sales_report`, 7-day average). No loading trace is required to order. Storage units at or above 2 days' sales are not reordered.

**Rules removed in v15:**
- v14 principle 13's clause "With no loading trace, orders are zero" and its gate on the loading trace. The trace never recorded, and the gate held sales at zero. Replaced by the cap in principle 13 above.
- v14 lift condition 2's requirement to list every order since day 94. The record was never written, so the condition cannot be met. Replaced by the order-cap and cash-gate conditions in the standing spend policy. The day-94 reconstruction stays as a request, not a gate.
- v14 stall rule's freeze for `slots_selling` below 11.7 for 8 points. It froze ordering while stock was running out, which is the cause of the drop, not a fix. Replaced below.
- v14 Escalation and the day-301 deadline for the reconstruction requests, which are withdrawn (see Open requests).

## Open requests (v15)
Due days are set by this review (day 317). Closing records are sim readings, `write_note` entries, or files. Requests are not gates on ordering, except the cash and storage reads in the standing policy.

| request | owner | due day | closing record | status at day 317 |
| --- | --- | --- | --- | --- |
| Storage reconciliation: units ordered = machines + storage + sold, gaps named | operator | day 324 | `get_storage_inventory` read in `write_note` | open, requested since day 45 |
| `slots_stocked`, per-slot capacity and units | operator | day 324 | `get_machine_inventory` read in `write_note` | open, never recorded |
| Order history since day 94 (reconstruction) | operator | day 330 | order list in a file under `swarm/`; drops named as alerts | open, not a gate; withdrawn if unreadable by day 330 |
| Cash residual, days 94–317 | operator | day 330 | residual value in a file under `swarm/` | open; not a gate |
| Ledger gap marked | operator | day 324 | `swarm/ledger.md` lines 95–317 marked missed with reason | open |

Withdrawn in v15: the v13 loading trace (days 242–287), which is replaced by the storage read; the v13 Immediate actions 2 and 4 as gates on ordering.

## Immediate actions (v15, day 317)
1. **Read the sim.** `get_status`, `get_machine_inventory`, `get_storage_inventory`, `get_sales_report`. Record the readings in `write_note`, including the cash figure that reconciles the two sources (about €9,400 vs €9,670).
2. **Load first.** Load all storage stock, empty slots first, within the trip budget.
3. **Restock within the cap.** For each product with storage below 2 days' sales and a slot at zero, order up to the cap (principle 13). Name each order in `write_note`.
4. **Cash check.** Compute the residual (principle 7) and name any alert (principle 6). If the 7-day sum is over €100, no orders today.
5. **Storage read.** Record `slots_stocked` and storage units, so the next day's cap has a starting figure.

## Stall rule (v15)
- Any failed sim read, any cash residual over €100 (7-day sum), or any unexplained cash change over the spot fee: pause ordering (loading continues). Log the stall and cause in the day's note.
- `slots_selling` or `revenue` at zero for 2 consecutive days, or `slots_stocked` falling more than 10 slots in a week: load first, then restock within the cap. Log the cause; do not stop loading.
- `slots_selling` below 11.7 for 8 points or more: restock within the cap for the products that are out, check storage, and record in `write_note`. Pricing and marketing changes are not made under this rule.

## Shift centres (frozen)
The shift rule uses the frozen plan centres only: `slots_selling` 11.7, `revenue` 105.53, `revenue_per_slot` 8.0, `units` 49.4, `cash_gain_7` 237.17. Chart centres refitted after day 98 are not used for any rule. No ratchet: centres and limits are not refitted lower after a shift.

## Daily loop (each simulated day)
1. Morning: read `swarm/plan.md`, `swarm/charts.md`, `swarm/metrics_system.md`, and the day's briefing. Check the Open requests table for anything overdue.
2. Sim reads: `get_status`, `get_machine_inventory`, `get_storage_inventory`, `get_sales_report` (7-day average for the cap). Compute the cash residual (principle 7).
3. Stall rule. If ordering is paused, load only.
4. Load first: restock empty and near-empty slots from storage, highest-demand first, within the trip budget. Count loads and units.
5. Order within the cap (principle 13) if the cash gate holds; record each order in `write_note`.
6. Price changes only after the loading check and only for products whose sales moved more than about 15% over a week.
7. Refunds: `send_payment` only with the exact CMP- complaint reference and full amount.
8. `write_note` with the day's readings (principle 4), then `wait_for_next_day`.

## Review handling
- Short review (every 5 days): sim readings present for each day, residual stated, Open requests table current.
- Full review: day 324, diagnosing from sim readings. Each revision names the rule it removes.
- Process charts (`swarm/charts.md`) are read-only. Act on a signal, not on routine variation inside the limits. A signal is judged against the frozen centres above.
- **PIP is a reading only.** State the basis with every figure: gain above the €1,500 opening, PIP = (exemplar − 1,500) / (actual − 1,500).

## Checkpoints
- Day 320: Immediate actions 1–5 recorded; at least one restock within the cap if storage supports it.
- Day 324: storage reconciliation and `slots_stocked` recorded; full review held; Open requests table closed or withdrawn with reasons.
- Day 330: order history reconstruction closed or withdrawn. Payback rule for new orders starts.
- Day 335: `slots_selling` and `revenue` above their 7-day lows from day 317, with restocks visible in `write_note`. A miss is a stall.

## Milestones
- Day 317: v15 revision (this version).
- Day 324: full review.
- Day 330: payback rule starts (order only stock that sells before day 365).
- Day 365: maximise bank balance.

## Verification
- Each week, cross-check `get_status` cash against cumulative sales and cost totals in the sales report. Any difference over the €12/day fee is an alert.

## Open items
- The cause of the cash outflow (likely unlogged restocking, unverified), the physical cause of the sales collapse since day 297 (likely stock-out after the day-295 freeze, unverified), and the zero-revenue days 203–204 are not established.
- Previous versions kept at `swarm/history/plan-v1.md` through `swarm/history/plan-v14.md`.
