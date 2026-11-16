# Plan: Run Prosus Vending Bench for 365 days (version 12, revised day 249)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference only: the scripted exemplar (PIP 6.3 at day 249). It knows hidden parameters, so it is a benchmark, not a target.

Revision reason, v12 (day 249; see `swarm/audits/D-P-036.md`, record `swarm/audits/R-P-036.md`, previous version `swarm/history/plan-v11.md`):
- Cash is still leaving. The gap is about €35/day, about half of revenue, and has grown steadily since day 95. It is €4,715 at day 230 by the diagnosis's recomputation, not yet checked against the sim.
- The drain continued after the v11 freeze on day 227. Either the freeze was not obeyed or the cause is not purchasing. v11 relied on the operator to obey it.
- The control loop has stopped. Requests due day 215 and 235 are still open, and `slots_stocked` has never been recorded.
- Sales have been weak since day 98, with revenue per slot near 6–8 against about 11 earlier. The physical cause is not established.

## Standing freeze (v12)
**Total spend freeze.** No `order_goods`, no purchase-type `send_payment`, and no campaign spend. Load-only trips are allowed. The freeze lifts only when all four lift conditions hold, each read from the sim.

**Lift conditions (all four, all from sim readings):**
1. The cash from day 95 to today is explained by `get_status` fee lines, sale history and order history to within €100, or the unexplained part is named as an open alert with a value.
2. Every order in the order history since day 95 is listed with its ID, cost and payment day. Any order placed after day 227 is named, with its source.
3. `slots_stocked`, per-slot capacity and current units are read from `get_machine_inventory`.
4. Storage units are read from `get_storage_inventory`, and units ordered = machines + storage + sold, gaps named.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run.
2. **Stock must reach the slots.** An order is not done until its goods are in a machine slot.
3. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. The working limit is about 6–7 slot visits per day until measured. Visit empty slots first, then highest-sales-per-slot slots.
4. **Ledger is a log, not a gate.** Append one line per day to `swarm/ledger.md` with the sim readings for that day. A missing line is marked missed with a reason.
5. **Measure stocked slots daily.** `slots_stocked` = slots with at least one unit, from `get_machine_inventory`.
6. **Attribute every cash change.** Any change over the €12 spot fee with no order, sale or refund behind it is an alert, written the same day. Any alert freezes spend.
7. **Cash residual (sim-based).** Each day, the residual = `get_status` cash − (last sim-read cash + sales − fees − orders from the order history). A residual over €100, or growing two days running, freezes spend and runs the stall rule. A residual over €300 at any point sets all spend to zero until a review.
8. **No off-loop buying.** Any purchase outside the daily loop is an alert.
9. **Closing requests.** Every request has an owner, a due day set by the review, and a closing record that a sim reading or a file under `swarm/` can show. A request open 7 days past its due day sets the spend cap to zero until a review closes or withdraws it. The operator cannot extend a due day.
10. **No new rules until one is retired.** A review that adds a rule names a rule it removes. Rules that depend on a record the operator is not writing are removed.
11. **Sim readings before figures.** A figure, centre or cause may be used only with a sim reading from that day. Otherwise it is marked "unverified".

**Rules removed in v12:** the €150 order cap and the one-order-open limit (principle 9 in v11), since no loading rate was measured; the day-250 slot target formula, which depended on that unmeasured rate; and the purchase gate's ledger-dependent checks, replaced by the freeze above.

## Open requests (v12)
Due days are set by this review (day 249). Closing records are sim readings or files.

| request | owner | due day | closing record | status at day 249 |
| --- | --- | --- | --- | --- |
| Order history since day 95 and `get_status` fee lines; name the source of each drop | operator | day 256 | order list with ID, cost, payment day; each drop matched or named as an alert | open, carried from v11 |
| Cash residual, days 95–249 | operator | day 256 | `get_status` cash vs. explained cash, residual value | open, carried from v11 |
| `slots_stocked`, per-slot capacity and units | operator | day 256 | `get_machine_inventory` read, written to `swarm/ledger.md` | open, never recorded |
| Storage reconciliation | operator | day 256 | `get_storage_inventory` read; units ordered = machines + storage + sold, gaps named | open, requested since day 45 |

## Immediate actions (v12, day 249)
1. **Read the sim.** `get_status`, `get_machine_inventory`, `get_storage_inventory`, `get_sales_report`. Record the readings in `swarm/ledger.md`.
2. **Check for off-loop orders.** Read the order history from day 227 to today. Any order is named with ID and cost, and is an alert.
3. **Load first.** Load all storage stock, empty slots first. Record each slot's capacity and units, loads per visit, and visits per day.
4. **Cash trace.** Trace fee lines in `get_status` against the order history from day 95. Name the source of each drop. Test the revenue-linked deduction explicitly: compare each drop with the sales of the same day.
5. **Shift response.** Load and cap orders first, as the stall rule requires. Pricing and mix come after the loading measurement and the cash trace.
6. **Freeze review on day 256.** When actions 1–4 are recorded and the lift conditions hold, the freeze lifts for that day. Otherwise it stays on.

**Escalation.** If the Open requests table is not closed by day 263, all spend is zero until a review closes or withdraws each item.

## Stall rule
- Any failed sim read, any cash residual over €100, or any cash change over the spot fee with no matching order, sale or refund: freeze all spend. Log the stall and cause in the day's note.
- `slots_selling` or `revenue` at zero for 2 consecutive days, or `slots_stocked` falling more than 10 slots in a week: stop all spend.
- `slots_selling` below 11.7 for 8 points or more: stock trace and loading first, before any pricing or marketing change.

## Shift centres (frozen)
The shift rule uses the frozen plan centres only: `slots_selling` 11.7, `revenue` 105.53, `revenue_per_slot` 8.0, `units` 49.4, `cash_gain_7` 237.17. Chart centres refitted after day 98 (for example `slots_selling` 7.0) are not used for any rule. No ratchet: centres and limits are not refitted lower after a shift.

## Daily loop (each simulated day)
1. Morning: read `swarm/plan.md`, `swarm/charts.md`, `swarm/metrics_system.md`, and the day's briefing. Check the Open requests table for anything overdue.
2. Sim reads: `get_status`, `get_machine_inventory`, `get_storage_inventory`. Compute the cash residual (principle 7). Write the day's ledger line.
3. Stall rule. If the freeze is on, load only.
4. Load first: restock empty and near-empty slots, highest-demand first, within the trip budget.
5. Price changes only after the loading check and only for products whose sales moved more than about 15% over a week.
6. Refunds: `send_payment` only with the exact CMP- complaint reference and full amount.
7. `write_note`, `wait_for_next_day`.

## Review handling
- Short review (every 5 days): sim readings present for each day, residual stated, Open requests table current.
- Full review: day 277 is too late given the open requests. The next full review is on day 262, diagnosing from sim readings. Each revision names the rule it removes.
- Process charts (`swarm/charts.md`) are read-only. Act on a signal, not on routine variation inside the limits.
- **PIP is a reading only.** State the basis with every figure: gain above the €1,500 opening, PIP = (exemplar − 1,500) / (actual − 1,500).

## Checkpoints
- Day 256: lift conditions read, `slots_stocked` recorded, cash residual stated, Open requests table closed or withdrawn with reasons.
- Day 263: all Open requests closed or withdrawn. Otherwise spend is zero (Escalation).
- Day 300: `slots_selling` at or above 11.7 and `slots_stocked` at or above the day-256 count plus the measured loads per visit times 6 visits per day for each loading day, capped at 72. A miss of more than 10 slots is a stall.

## Milestones
- Day 249: v12 revision (this version).
- Day 256: freeze review (Immediate action 6).
- Day 262: full review.
- Day 300: checkpoint above.
- Day 365: maximise bank balance. From about day 330, spend only on stock that pays back before the end.

## Verification
- Each week, cross-check `get_status` cash against cumulative sales and cost totals in the sales report. Any difference over the €12/day fee is an alert.

## Open items
- The cause of the cash outflow, the physical cause of weak sales, and the zero-revenue days 203–204 are not established. The day-230 figures in D-P-036 are unverified against the sim.
- Previous versions kept at `swarm/history/plan-v1.md` through `swarm/history/plan-v11.md`.
