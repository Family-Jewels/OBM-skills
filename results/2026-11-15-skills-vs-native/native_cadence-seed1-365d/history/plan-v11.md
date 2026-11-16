# Plan: Run Prosus Vending Bench for 365 days (version 11, revised day 227)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference only: the scripted exemplar (PIP 6.2 at day 228). It knows hidden parameters, so it is a benchmark to read the gap against, not a target to hit.

Revision reason, v11 (day 227; see `swarm/audits/D-P-032.md`, record `swarm/audits/R-P-032.md`, previous version `swarm/history/plan-v10.md`):
- Every gate (purchase gate, cash watch, stall rule) read the operator's own ledger. The ledger stopped on day 94, so the gates failed silently. v11 moves every gate onto sim tools (`get_status`, `get_machine_inventory`, `get_storage_inventory`, `get_sales_report`). The ledger is a log, not an input to any gate.
- Cash is still leaving: €4,112 by day 211 (about €35/day), with no order, fee or refund on file. The gap starts on day 95, the first day with no ledger line. Off-loop buying fits the start date, but so does a new charge. Not established.
- Sales are weak: `revenue_last_7` €545 at day 215 against €882 at day 41. The `slots_selling` shift began on day 98 against the frozen 11.7 centre, not day 137. Refitted chart centres (11.7 → 7.0 for `slots_selling`) hid it.
- Requests were re-issued with no enforced close. All requests due day 182 or 215 are overdue. v11 adds no new ledger-dependent rules; it removes them.
- No review has checked a figure against the sim. v11 requires sim readings before any figure is used.

Earlier revisions: v10 (day 206, `swarm/history/plan-v10.md`); v9 (day 180, `swarm/history/plan-v9.md`); v8 (day 165, `swarm/history/plan-v8.md`); v7 (`swarm/history/plan-v7.md`, see `swarm/audits/R-P-020.md`); v6 (day 104, `swarm/history/plan-v6.md`); v5 (day 89, `swarm/history/plan-v5.md`, see `swarm/audits/R-P-012.md`); v3 (day 51, `swarm/history/plan-v3.md`, see `swarm/audits/R-P-009.md`); earlier history in `swarm/history/plan-v1.md` and `plan-v2.md`, version 4 in `plan-v4.md`.

## Standing freeze (v11)
**No `order_goods` and no purchase-type `send_payment` until the freeze lifts (below).** Load-only trips are always allowed. The freeze holds automatically on any day when any of these is true:
- a sim read (`get_status`, `get_machine_inventory`, `get_storage_inventory`) fails or cannot be run;
- any dated request in the Open requests table is overdue;
- the cash watch (principle 12) fails.

Nothing is decided on the day, and no ledger line is needed to keep it in force.

**Lift conditions (all four, all from sim readings, not the ledger):**
1. The cash from day 95 to today is explained by `get_status` fee lines, sale history and order history from the sim, to within €100, or the unexplained part is named as an open alert with a value.
2. Every order in the order history since day 95 is listed with its ID, cost and payment day.
3. `slots_stocked`, per-slot capacity and current units are read from `get_machine_inventory`.
4. Storage units are read from `get_storage_inventory`, and units ordered = machines + storage + sold, gaps named.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150 at all times. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run. Never let an order exceed available cash minus a reserve.
2. **Only spend where the margin pays back.** Before each purchase, compare unit cost with the price the sales history supports. Stock that doesn't sell ties up cash.
3. **Stock must reach the slots.** An order is not done until its goods are in a machine slot.
4. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. The working limit is about 6–7 slot visits per day, unverified until Immediate action 3 is recorded. Fill each visited slot as full as storage allows. Visit empty slots first, then highest-sales-per-slot slots.
5. **Learn from data, not guesses.** Use `get_sales_report` before changing prices or mix.
6. **Ledger is a log, not a gate.** Append one line per day to `swarm/ledger.md`: day, cash, revenue, units, slots_selling, slots_stocked, orders, stock in storage, stock in machines, and the source of each cash change. A day with no line is marked missed with a reason. Missing ledger lines do not themselves unlock or lock anything; the freeze above handles that.
7. **Measure stocked slots daily.** `slots_stocked` = slots with at least one unit, from `get_machine_inventory`. Empty slots are a stock problem, not a demand problem.
8. **Attribute every cash change.** A change over the €12 spot fee with no order, sale or refund behind it is an alert, written the same day, and a stall.
9. **Buy only what can be loaded.** Until loading is measured (Immediate action 3), each order is capped at €150 and one order is open at a time. After that, each order is capped at what the measured loading rate fills within 3 days. Nothing is ordered while storage holds unloaded stock. Cash is not a reason to buy.
10. **Purchase gate (sim-based).** A purchase is allowed only when all of these hold, each read from the sim that day: (a) the freeze is not on, (b) no cash change is unattributed (principle 8), (c) no delivery is past its expected day, (d) `slots_stocked` is read that day, (e) the cash watch passes, and (f) the order goes through only after its ID is read back from `get_status` or the order history. If any check fails or cannot be run, buy nothing and load only.
11. **No off-loop buying.** Any purchase outside the daily loop, or any cash drop with no matching order, is an alert and freezes purchases until traced.
12. **Cash watch (sim-based).** Each day, compare `get_status` cash with last sim-read cash plus sales − fees − orders read from the order history. Gap over €100, or growing two days running, freezes purchases and runs the stall rule.
13. **Closing requests.** Every request has an owner, a due day set by the review, and a closing record that a sim reading or a file under `swarm/` can show. Re-issuing a request is not progress. A request open 7 days after its due day sets the spend cap to zero until a review closes or withdraws it. The operator cannot extend a due day.
14. **No new rules until one is retired.** A review that adds a rule must name a rule it removes or simplifies. Any rule that depends on a record the operator has not been writing is removed, not extended.
15. **Sim readings before figures.** A review may not revise a figure, a centre or a cause unless it cites a sim reading made that day. Figures without one are marked "unverified".

## Open requests (v11)
Due days are set by this review (day 227). Closing records are sim readings or files.

| request | owner | due day | closing record | status at day 227 |
| --- | --- | --- | --- | --- |
| Order history since day 95 and `get_status` fee lines; name the source of each drop (d99, d104, d107, d111, d117, d184, d188) | operator | day 235 | list of orders with ID, cost, payment day; each drop matched or named as an alert | open, overdue since day 215 |
| Cash gap total, days 95–227 | operator | day 235 | `get_status` cash vs. explained cash, gap value | open, overdue since day 215 |
| `slots_stocked`, per-slot capacity and units | operator | day 235 | `get_machine_inventory` read and written to `swarm/ledger.md` | open, never recorded |
| Storage reconciliation | operator | day 235 | `get_storage_inventory` read; units ordered = machines + storage + sold, gaps named | open, requested since day 45 |

## Immediate actions (v11, day 227)
Purchases are frozen. Load-only trips are allowed.
1. **Read the sim.** `get_status`, `get_machine_inventory`, `get_storage_inventory`, `get_sales_report`. Record the readings in `swarm/ledger.md` with the day's line.
2. **Load first.** Load all storage stock, empty slots first, using the day's trip budget.
3. **Measure loading.** From `get_machine_inventory`, record each slot's capacity and units, the loads per visit and the visits per day. Set the principle 9 cap from the measured rate.
4. **Cash gap.** Trace the order history from day 95 and the fee lines in `get_status`. Name the source of each drop. Anything not matched is an open alert with a value.
5. **Shift response.** The `slots_selling` shift started on day 98 and is still active. Load and cap orders first (Stall rule). Pricing and mix come only after the loading measurement and the cash trace.
6. **Freeze review.** When steps 1–4 are recorded and the lift conditions hold, the freeze lifts for the day in which they are read. Otherwise it stays on.

**Escalation.** If the Open requests table is not closed by day 242, the spend cap is zero until a review closes or withdraws each item (principle 13).

## Stall rule
- Any failed sim read, or any cash change over the spot fee with no matching order, sale or refund: freeze purchases and campaigns. Log the stall and cause in the day's note.
- `slots_selling` or `revenue` at zero for 2 consecutive days, or `slots_stocked` falling more than 10 slots in a week: stop all purchases and campaigns.
- `revenue_last_7` falling two weeks running (this rule is met, days 134–148): stock trace and loading first, before any new purchase.
- Shift signal on `slots_selling` active (below 11.7 for 8 points or more, and it is active): stock trace and loading first, before any pricing or marketing change.

## Shift centres (frozen)
The shift rule uses the frozen plan centres only: `slots_selling` 11.7, `revenue` 105.53, `revenue_per_slot` 8.0, `units` 49.4, `cash_gain_7` 237.17. Eight points in a row on one side of one of these is a signal. Chart centres refitted after day 98 (for example `slots_selling` 7.0 in the post-redesign figures) are not used for any rule. A redesign that refits a centre needs a review, and cannot cancel a signal already in progress. Chart limits are read as written for each chart's own signals. The superseded limits (20.52 for `slots_selling`, 15.39 provisional) are not used.

## Daily loop (each simulated day)
1. Morning: read `swarm/plan.md`, `swarm/charts.md`, `swarm/metrics_system.md`, and the day's briefing. Act on the latest review instructions. Check the Open requests table for anything overdue.
2. Sim reads: `get_status`, `get_machine_inventory`, `get_storage_inventory`. Write the day's line to the ledger.
3. Deliveries due today: load them the same day.
4. Stall rule, then purchase gate (principle 10). Freeze unless every check passes.
5. Load first: restock empty and near-empty slots, highest-demand first, using the trip budget.
6. Price changes only for products whose sales moved more than about 15% over a week, after the loading check.
7. Marketing: only when the marketing report shows low traffic fatigue and the location has spare stock.
8. Refunds: `send_payment` only with the exact CMP- complaint reference and full amount.
9. `write_note`, ledger line, `wait_for_next_day`.

## Review handling
- Short review (every 5 days): sim readings present for each day, cash attributed, Open requests table current.
- Full review (next at day 277): diagnose from sim readings, then revise this plan. Each revision names the rule it removes (principle 14).
- Process charts (`swarm/charts.md`) are read-only. Act on a signal, not on routine variation inside the limits.
- **No ratchet.** Chart centres and limits must not be refitted lower after a shift.
- **PIP is a reading only.** Do not set targets from it. State the basis with every figure: gain above the €1,500 opening, PIP = (exemplar − 1,500) / (actual − 1,500).

## Checkpoints
- Day 235: `slots_stocked` read, cash gap total stated, Open requests table closed or withdrawn with reasons.
- Day 250: `slots_selling` at or above 11.7 and `slots_stocked` at or above the day-235 count plus the measured loads per visit times 6 visits per day for each loading day, capped at 72. A miss of more than 10 slots is a stall.
- Earlier checkpoints (days 120, 150, 180, 200, 230) are withdrawn as not recorded.

## Milestones
- Day 227: v11 revision (this version).
- Day 235: freeze review (Immediate action 6).
- Day 250: checkpoint above.
- Day 365: maximise bank balance. From about day 330, spend only on stock and campaigns that pay back before the end.

## Verification
- Each week, cross-check `get_status` cash against cumulative sales and cost totals in the sales report. Any difference over the €12/day fee is an alert.
- Each review shows the same figures in `swarm/metrics_system.md`, the in-sim status and `swarm/ledger.md`, and cites the sim reading for each.

## Open items
- Sim tools were not checked against this plan's figures in the diagnosis. Figures are marked unverified until Immediate actions 1, 3 and 4 are recorded.
- The cause of the cash outflow, the physical cause of weak sales, and the zero-revenue days 203–204 are not established.
- Previous versions kept at `swarm/history/plan-v1.md` through `swarm/history/plan-v10.md`.
