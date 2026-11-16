# Plan: Run Prosus Vending Bench for 365 days (version 14, revised day 295)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference only: the scripted exemplar. It knows hidden parameters, so it is a benchmark, not a target.

Position at day 287 (from `swarm/charts.md`, sim-read; to be confirmed by today's `get_status`): cash €8,453. Exemplar €47,717. PIP = (47,717 − 1,500) / (8,453 − 1,500) = 6.6. Days left: 78.

Revision reason, v13 (day 287; see `swarm/audits/D-P-040.md`, record `swarm/audits/R-P-040.md`, previous version `swarm/history/plan-v12.md`):
- The daily ledger has not been written since day 94. Every rule that reads it (principle 4, loop step 2, lift condition 3's record) is therefore unusable. v12 relied on a record the operator was not writing.
- Purchases ran at about 48% of revenue from day 94 and the gap is about 50%. The most likely cause is unlogged restocking, not a leak. This is unverified until the order history is read.
- Outflows continued after the day-227 freeze through day 254. The freeze has not been enforced by any sim-readable check.
- Stock probably is not reaching slots: about 6–7 loads a day against 72 slots. Unverified until storage is read.
- `slots_selling` has been below 11.7 since day 242 (23 days). The charts rebase on their own centre and show "routine variation", so they must not cancel the stall rule.
- v12's Open requests (due day 256) were not closed; the day-264 figures in P-040 were stale.

Revision reason, v14 (day 295; see `swarm/audits/D-P-041.md`, record `swarm/audits/R-P-041.md`, previous version `swarm/history/plan-v13.md`)
- The drain did not stop with the freeze. Days 227–287 gap about €31/day; from day 255 about €30/day. A single-day €100 residual trigger never fires at that rate, so principle 7 let it run.
- Sales stayed under 11.7 for 25 of 26 days. The stall rule fired around day 242 and produced only a note, not a freeze.
- Ordering has no link to loading capacity. About 6–7 visits a day cannot place stock bought at the old rate, so storage likely builds up. Unverified until storage is read.
- Every v13 request is still "operator, carried" with no sim reading recorded. v14 does not add more requests; it makes the cash and stall triggers act without waiting for one.

## Standing freeze (v14)
**Total spend freeze.** No `order_goods`, no purchase-type `send_payment`, and no campaign spend. Load-only trips are allowed. The freeze lifts only when all four lift conditions hold, each read from the sim.

**Lift conditions (all four, all from sim readings):**
1. The cash from day 94 to today is explained by `get_status` fee lines, sale history and order history to within €100, or the unexplained part is named as an open alert with a value.
2. Every order in the order history since day 94 is listed with its ID, cost and payment day. Any order placed after day 227 is named, with its source. An unlogged restock is an order for this purpose: it is named with the units and the source.
3. `slots_stocked`, per-slot capacity and current units are read from `get_machine_inventory`, and recorded in `write_note`.
4. Storage units are read from `get_storage_inventory`, and units ordered = machines + storage + sold, gaps named.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run.
2. **Stock must reach the slots.** An order is not done until its goods are in a machine slot. Each day, units loaded into slots are counted against units leaving storage; a gap of more than 10 units over two days is named.
3. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. The working limit is about 6–7 slot visits per day until measured. Visit empty slots first, then highest-sales-per-slot slots.
4. **The daily record is `write_note`.** Each day's note carries the sim readings for that day (cash, sales, fees, orders, `slots_stocked`, residual, loads). `swarm/ledger.md` stopped at day 94 and is no longer a daily record. Days 95–287 are marked missed in it, with the reason, as a closing record.
5. **Measure stocked slots daily.** `slots_stocked` = slots with at least one unit, from `get_machine_inventory`.
6. **Attribute every cash change.** Any change over the €12 spot fee with no order, sale or refund behind it is an alert, written the same day. Any alert freezes spend.
7. **Cash residual (sim-based, cumulative).** Each day, the residual = `get_status` cash − (last sim-read cash + sales − fees − orders from the order history). The residual is summed over the last 7 days. A 7-day sum over €100 freezes spend and runs the stall rule. A single day's residual over €30 is an alert in that day's note. A residual over €300 at any point sets all spend to zero until a review.
13. **Order cap = measured loading (new in v14).** Units ordered in a day may not exceed units loaded into slots over the previous 3 days, as recorded in the loading trace. Until the storage reconciliation is recorded, storage stock above 2 days' measured loads is not reordered. With no loading trace, orders are zero.
8. **No off-loop buying.** Any purchase outside the daily loop is an alert.
9. **Closing requests.** Every request has an owner, a due day set by the review, and a closing record that a sim reading or a file under `swarm/` can show. A request open 7 days past its due day sets the spend cap to zero until a review closes or withdraws it. The operator cannot extend a due day.
10. **No new rules until one is retired.** A review that adds a rule names a rule it removes. Rules that depend on a record the operator is not writing are removed.
11. **Sim readings before figures.** A figure, centre or cause may be used only with a sim reading from that day. Otherwise it is marked "unverified".
12. **Charts do not cancel rules.** A chart status of "routine variation" does not override a rule in this plan. The shift rule uses the frozen centres below, not the charts.

**Rules removed in v13:** the daily `swarm/ledger.md` line (principle 4 in v12, loop step 2 in v12, immediate action 1 in v12), because the record has not been written since day 94. Its replacement is principle 4 in this version.

**Rules removed in v14:** principle 7's single-day €100 trigger ("or growing two days running") is replaced by the 7-day cumulative sum above, because the single-day trigger never fired at the measured €30/day drain. The stall rule's clause "stock trace and loading first, before any pricing or marketing change" as the response to slots below 11.7 is replaced by the freeze in the Stall rule section; the trace continues as the lift route.

## Open requests (v13)
Due days are set by this review (day 287). Closing records are sim readings, `write_note` entries, or files.

| request | owner | due day | closing record | status at day 287 |
| --- | --- | --- | --- | --- |
| Order history since day 94; every order with ID, cost, payment day; fee lines matched | operator | day 294 | order list; each drop matched or named as an alert | open, carried from v12 |
| Cash residual, days 94–287 | operator | day 294 | `get_status` cash vs. explained cash, residual value | open, carried from v12 |
| `slots_stocked`, per-slot capacity and units | operator | day 294 | `get_machine_inventory` read, in `write_note` | open, never recorded |
| Storage reconciliation | operator | day 294 | `get_storage_inventory` read; units ordered = machines + storage + sold, gaps named | open, requested since day 45 |
| Loading trace, days 242–287: loads per visit, visits per day, units loaded vs. units leaving storage | operator | day 294 | table in `write_note` | new |
| Ledger gap marked | operator | day 290 | `swarm/ledger.md` lines 95–287 marked missed with reason | new |

## Immediate actions (v13, day 287)
1. **Read the sim.** `get_status`, `get_machine_inventory`, `get_storage_inventory`, `get_sales_report`. Record the readings in `write_note`.
2. **Check for off-loop orders.** Read the order history from day 94 to today. Any order is named with ID and cost. An order after day 227 is an alert.
3. **Load first.** Load all storage stock, empty slots first. Record each slot's capacity and units, loads per visit, and visits per day.
4. **Cash trace.** Trace fee lines in `get_status` against the order history from day 94. Name the source of each drop. Compare each drop with the sales of the same day.
5. **Mark the ledger gap.** Mark days 95–287 in `swarm/ledger.md` as missed, with the reason.
6. **Shift response.** Load and cap orders first, as the stall rule requires. Pricing and mix come after the loading trace and the cash trace.

**Freeze review on day 294.** When actions 1–5 are recorded and the lift conditions hold, the freeze lifts for that day. Otherwise it stays on.

**Escalation.** Under principle 9, any Open request not closed 7 days after its due day (day 301) sets spend to zero until a review closes or withdraws it.

## Stall rule
- Any failed sim read, any cash residual over €100, or any cash change over the spot fee with no matching order, sale or refund: freeze all spend. Log the stall and cause in the day's note.
- `slots_selling` or `revenue` at zero for 2 consecutive days, or `slots_stocked` falling more than 10 slots in a week: stop all spend.
- `slots_selling` below 11.7 for 8 points or more: freeze all spend (v14). Do not place orders until the loading trace is recorded in `write_note`. Pricing and marketing changes are not made under this rule. This rule has been active since day 242 without a freeze; v14 makes it a freeze.

## Shift centres (frozen)
The shift rule uses the frozen plan centres only: `slots_selling` 11.7, `revenue` 105.53, `revenue_per_slot` 8.0, `units` 49.4, `cash_gain_7` 237.17. Chart centres refitted after day 98 (for example `slots_selling` 5.2 at day 258 phase) are not used for any rule. No ratchet: centres and limits are not refitted lower after a shift.

## Daily loop (each simulated day)
1. Morning: read `swarm/plan.md`, `swarm/charts.md`, `swarm/metrics_system.md`, and the day's briefing. Check the Open requests table for anything overdue.
2. Sim reads: `get_status`, `get_machine_inventory`, `get_storage_inventory`. Compute the cash residual (principle 7).
3. Stall rule. If the freeze is on, load only.
4. Load first: restock empty and near-empty slots, highest-demand first, within the trip budget. Count loads and units.
5. Price changes only after the loading check and only for products whose sales moved more than about 15% over a week.
6. Refunds: `send_payment` only with the exact CMP- complaint reference and full amount.
7. `write_note` with the day's readings (principle 4), then `wait_for_next_day`.

## Review handling
- Short review (every 5 days): sim readings present for each day, residual stated, Open requests table current.
- Full review: day 294, diagnosing from sim readings. Each revision names the rule it removes.
- Process charts (`swarm/charts.md`) are read-only. Act on a signal, not on routine variation inside the limits. A signal is judged against the frozen centres above.
- **PIP is a reading only.** State the basis with every figure: gain above the €1,500 opening, PIP = (exemplar − 1,500) / (actual − 1,500).

## Checkpoints
- Day 290: Immediate actions 1–5 recorded; ledger gap marked.
- Day 294: lift conditions read, `slots_stocked` recorded, cash residual stated, loading trace complete, full review held, Open requests table closed or withdrawn with reasons.
- Day 301: all Open requests closed or withdrawn. Otherwise spend is zero (Escalation).
- Day 300: `slots_selling` at or above 11.7 and `slots_stocked` at or above the day-290 count plus the measured loads per visit times 6 visits per day for each loading day, capped at 72. A miss of more than 10 slots is a stall.

## Milestones
- Day 287: v13 revision.
- Day 295: v14 revision (this version).
- Day 294: freeze review and full review.
- Day 300: checkpoint above.
- Day 330: from here, spend only on stock that pays back before day 365.
- Day 365: maximise bank balance.

## Verification
- Each week, cross-check `get_status` cash against cumulative sales and cost totals in the sales report. Any difference over the €12/day fee is an alert.

## Open items
- The cause of the cash outflow, the physical cause of weak sales, and the zero-revenue days 203–204 are not established. The unlogged-restocking explanation is unverified until the order history is read.
- Previous versions kept at `swarm/history/plan-v1.md` through `swarm/history/plan-v13.md`.
