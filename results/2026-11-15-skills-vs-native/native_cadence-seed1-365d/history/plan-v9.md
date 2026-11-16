# Plan: Run Prosus Vending Bench for 365 days (version 9, revised day 180)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference only: the scripted exemplar. It knows hidden parameters, so it is a benchmark to read the gap against, not a target to hit.

Revision reason, v9 (day 180; see `swarm/audits/D-P-026.md`, record `swarm/audits/R-P-026.md`, previous version `swarm/history/plan-v8.md`, response to `swarm/audits/P-027.md`):
- Unexplained cash outflow is still running. The ledger ends at day 94. From day 95 to 170 cash should be about €9,051 and is €6,184: a gap of €2,867 (about €38/day). No order, fee or refund is on file for it. v8 said to trace it; the trace has not been written down.
- The loop depends on its own ledger. The purchase gate needs a ledger line, and the ledger has stopped, so the stop rules rely on an operator who is no longer writing. v9 makes the stop automatic: no purchase while the gate is unverifiable, whatever the reason.
- Requests are re-issued and never closed. The stock trace and ledger backfill have been asked for since day 45 (A-001 to A-003, P-024 to P-027). v9 gives each open request an owner, a due day and a closing record (Open requests table).
- Demand shift is active and hidden by refitted centres. `slots_selling` has been below 11.7 from day 137 to 180 (latest 9 at day 170). Chart centres were refitted on the decline. v9 freezes them.
- Revenue fell two weeks running (511, 502, 274 at days 134, 141, 148), meeting the stall rule's revenue test.
- Likely physical cause (hypothesis, unverified): stock is bought faster than it can be loaded. Loading is about 6–7 slot visits a day against 72 slots. v9 caps purchases by measured loading, not by cash.

Revision reason, v8 (day 165; see `swarm/audits/D-P-024.md`, record `swarm/audits/R-P-024.md`, previous version `swarm/history/plan-v7.md`): the same gap, deadlock and shift problems were first raised here. v8 froze the chart centres and made the stock trace blocking. Its steps were not recorded.

Revision reason, v7 (see `swarm/audits/R-P-020.md`, diagnosis `swarm/audits/D-P-020.md`, previous version `swarm/history/plan-v6.md`): the ledger lapsed after day 94; five cash drops (d99, d104, d107, d111, d117) match purchase-order sizes; selling slots plateaued at about 10–15 of 72 since day 52; `slots_stocked` and slot capacity have never been recorded.

Earlier revisions: day 165 (v8, `swarm/history/plan-v8.md`); day 104 (v6, `swarm/history/plan-v6.md`); day 89 (v5, `swarm/history/plan-v5.md`, see `swarm/audits/R-P-012.md`); day 51 (v3, `swarm/history/plan-v3.md`, see `swarm/audits/R-P-009.md`); earlier history in `swarm/history/plan-v2.md` and `swarm/history/plan-v1.md`. Version 4 is at `swarm/history/plan-v4.md`.

## Standing freeze (v9)
**No `order_goods` and no purchase-type `send_payment` until the Purchase gate (principle 10) passes and the Immediate actions below are written.** This holds even if sim tools are unavailable, and even if the day's stock is low. Load-only trips are always allowed. If sim tools cannot be reached on a day, write "tools unavailable, buying frozen" in the ledger and stop there. Do not buy from memory or from an earlier plan.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150 at all times. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run. Never let an order exceed available cash minus a reserve.
2. **Only spend where the margin pays back.** Before each purchase, compare the unit cost with the price the sales history supports. Stock that doesn't sell ties up cash.
3. **Stock must reach the slots.** An order is not done until its goods are in a machine slot. Track every order from purchase to loaded slot (see Stock trace).
4. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. The working limit is about 6–7 slot visits per day, still unverified until Immediate action 4 is recorded. Fill each visited slot as full as storage allows. Visit empty slots first, then highest-sales-per-slot slots.
5. **Learn from data, not guesses.** Use `get_sales_report` (by product and by location) before changing prices or the product mix.
6. **Every day is written, with no gaps.** Append one line per day to `swarm/ledger.md`: day, cash, revenue, units, slots_selling, slots_stocked, open orders, stock in storage, stock in machines, and the source of every cash change (order ID, fee, sale, refund). A day with no ledger line is a missed day. Missed days are marked as missed, with the reason, in the ledger, and never back-filled silently.
7. **Measure stocked slots daily.** `slots_stocked` = slots holding at least one unit, from `get_machine_inventory`. Record it next to `slots_selling` every day. Empty slots are a stock problem, not a demand problem.
8. **Attribute every cash change.** If cash changed by more than the €12 spot fee and no order, sale or refund explains it, write the gap in the ledger the same day as an alert. An unexplained change is a stall (see Stall rule).
9. **Buy only what can be loaded.** Standing orders are capped at the stock the measured loading rate can fill within 3 days (about 20 slot visits at full load). Nothing is ordered while storage holds undelivered or unloaded stock from an earlier order. Cash is not a reason to buy.
10. **Purchase gate.** A purchase is allowed only when all of these hold on the day: (a) the previous day has a ledger line, or the missing days are marked missed with reasons (see principle 13), (b) no unexplained cash change is open, (c) the Stock trace shows no order past its expected delivery day, (d) `slots_stocked` for the day is recorded in the ledger, (e) the cash watch (principle 12) passes, and (f) the day's `order_goods` call, if any, is recorded in the ledger with its order ID before the day ends. If any check fails, buy nothing and load only. A check that cannot be run counts as failed.
11. **No off-loop buying.** Any `order_goods` or `send_payment` made outside the daily loop, or any cash drop matching an order not in the ledger, is an alert and stops all purchases until the order is traced and logged. Purchases made without a ledger line are the fault being fixed, not catch-up purchases.
12. **Cash watch.** Compare `get_status` cash with the ledger-implied cash each day (last ledger cash + revenue − fees − logged orders). If the gap exceeds €100 on any day, or grows on two consecutive days, stop purchases and run the stall rule.
13. **Deadlock break.** When the ledger has lapsed, reopen the gate in this order and do not buy in between: (1) write the missed days as missed with reasons, (2) write the day's `slots_stocked` and cash, (3) complete the cash gap trace (Immediate action 0). Steps 1 and 2 are logs, not purchases, and must not be skipped to reach a purchase sooner. A gate reopened this way still needs check (e) and (f) on each day.
14. **Closing requests (v9).** Every request that a review makes is entered in the Open requests table with an owner, a due day and a closing record (a ledger line or a file under `swarm/`). A request is closed only by its closing record. Re-issuing a request does not count as progress. A request open past its due day is an alert, and principle 10 stays shut until it is closed or formally withdrawn with a reason.

## Open requests (v9)
| request | owner | due day | closing record | status at day 180 |
| --- | --- | --- | --- | --- |
| Cash gap trace, days 95–170 (~€2,867) | operator | day 182 | ledger lines per order ID, or an alert line per unmatched amount | open, overdue since day 165 |
| Ledger backfill, days 95–180 | operator | day 182 | ledger lines, or "missed" with reason | open, overdue since day 165 |
| Stock trace and storage reconciliation | operator | day 182 | `get_storage_inventory` and `get_machine_inventory` written to the ledger, with the units reconciled | open, requested since day 45 |
| `slots_stocked` and slot capacity | operator | day 182 | per-slot capacity and units written to the ledger | open, never recorded |
| Cash drops d99, d104, d107, d111, d117 | operator | day 182 | each matched to an order ID or a fee, or alerted | open, requested since day 117 |

## Stock trace (required after every `order_goods`)
1. Record the order in `swarm/ledger.md`: order ID, products, quantity, unit cost, total spend, expected delivery day, and the day it is expected to be paid.
2. On delivery day, call `get_storage_inventory`. Stock that has arrived must be loaded into slots within the same day's trip budget, highest-demand slots first, and empty slots before partly stocked ones.
3. Reconcile: units ordered = units in machines + units in storage + units sold. Any gap is an alert.
4. If an order has not arrived by its expected day, check `list_emails` and `get_status`, then chase the supplier. Do not reorder until the first order is accounted for.
5. Match each payment in `get_status` or the cash history to an order ID. A payment with no matching order is an alert.

## Reconciliation (day 31, before any new purchase)
Done. Kept for reference. Principles 6 and 10 now cover the same checks on every day.

## Immediate actions (v9, day 180, before any new `order_goods`)
Purchases are frozen (see Standing freeze). Load-only trips are allowed. Steps 0–5 from v8 are still not recorded.
0. **Cash gap trace.** Find the orders behind the ~€2,867 gap (days 95–170). Use `get_storage_inventory`, `get_machine_inventory`, `list_emails` and `get_status`. Record each unlogged order with its ID, cost and payment day, or record the amount as an open alert. The day's line must say which orders were checked and which were not.
0a. **Loading.** Load all stock in storage using the day's trip budget, empty slots first. Record `slots_stocked` before anything else.
1. **Baseline (day 180).** Run `get_status`, `get_machine_inventory` and `get_storage_inventory`. Write `slots_stocked`, slot capacity, `slots_selling`, cash, and the full reconciliation (units ordered = machines + storage + sold, gaps explained) into the ledger.
2. **Ledger coverage.** Backfill days 95–180 from sim state where possible (cash, sales report, order history). Mark any unrecoverable day as missed, with the reason.
3. **Cash drops.** For each of d99 (−€175), d104 (−€123), d107 (−€190), d111 (−€100), d117 (−€37), match to an order ID or a fee, or record it as an alert. Check PO-1031's actual payment date.
4. **Measure the binding constraint.** From `get_machine_inventory`, record each slot's capacity and current units. Record the measured loads per visit and visits per day. If visits × units per load cannot exceed the current stocked count, record loading throughput as the binding constraint and set principle 9's cap from the measured rate.
5. **Set checkpoints.** Write the `slots_stocked` and `slots_selling` targets for day 200 into the ledger (see Checkpoints).
6. **Load before buying.** Load any stock in storage, empty slots first, then highest-demand slots.
7. **Purchases resume** only after steps 0–5 are written and the purchase gate (principle 10) passes. The first order after the resume is capped at what the measured loading rate can fill within 3 days.

**Escalation.** If steps 0–5 are not written by day 186, the operator writes the reason in the ledger each day, keeps purchases frozen, and marks the Open requests table as overdue. Sim tools being unavailable is a reason to record, not a reason to buy.

## Stall rule
- Days with no ledger line are missed days. Stop purchases and campaigns until Immediate actions 1–5 are complete.
- If `slots_selling` or `revenue` is zero for 2 consecutive days, or `slots_stocked` falls by more than 10 slots in a week, or any cash change is larger than the spot fee with no matching order, sale or refund in the ledger, stop all purchases and campaigns.
- If `revenue_last_7` falls two weeks in a row, run the stock trace first, then load any stock in storage before buying anything new. This rule is met (days 134–148), so the stock trace comes first.
- If the shift signal on `slots_selling` (rule below) is active, run the stock trace and loading first, before any pricing or marketing change.
- Log each stall, its cause, and its resolution in the day's note and ledger.

## Day 0 (setup)
- `get_status`, `get_machine_inventory`, `get_storage_inventory`, `read_notes`, `list_emails`, `list_reminders`, `get_marketing_report`.
- Find suppliers with `search_web` (snack and drinks wholesalers in Amsterdam or the EU). Email each for a catalogue and volume terms. Check their replies the next morning.
- Call `check_offers` for each candidate supplier at realistic quantities before any `order_goods`.
- Keep the first order small enough that its full cost stays under about €300.
- Stock the highest-demand, highest-margin lines first: savoury snacks and coffee for AI-LOUNGE (picky, price-sensitive), hearty snacks for AI-HOUSE (less price-sensitive, higher consumption), and high-footfall lines for MAIN-LOUNGE.
- Load the delivered stock into slots on the same day it arrives. Do not leave it in storage.
- Set prices with a clear margin. Begin near the mid-range and adjust from sales data after about 3–5 days.

## Daily loop (each simulated day)
1. Morning: read `swarm/plan.md`, `swarm/metrics_system.md`, `swarm/charts.md`, and the day's briefing (`wait_for_next_day` result). Act on the latest review instructions, and check open complaints and emails. Check the Open requests table for anything overdue.
2. `get_status` for cash and open orders. `get_machine_inventory` for `slots_stocked`. Update `swarm/ledger.md` with the day's line and cash attribution.
3. Run the stock trace for any delivery due today, then the stall rule and the purchase gate.
4. Every 7 days: `check_offers` on each supplier and buy the best weekly discounts, within principles 9 and 10. Keep stock levels just above expected sales for 2–3 days so cash isn't tied up.
5. Load first, buy second: restock or swap empty and near-empty slots, highest-demand first, filling each visit as full as storage allows. Respect the trip budget.
6. Adjust prices for any product whose sales have changed by more than about 15%, using the price response from the sales report. Price changes are not the first response to a shift signal.
7. Marketing: only moderate use, and only when the marketing report shows traffic fatigue is low and the location has spare stock. Track the cost against the sales lift. Never spam channels.
8. Refunds: use `send_payment` only with the exact CMP- complaint reference and the full amount. Never send a payment with a guessed reference.
9. Write the day's note (`write_note`), append the ledger line, update the Open requests table, set reminders for weekly offer checks, and call `wait_for_next_day`.

## Review handling
- Short review (every 5 days): check the ledger has a line for each day, cash is attributed, the Open requests table is current, and the checkpoints are on track. Make small corrections only.
- Full review (every 50 days; last at day 132 by system request; next at day 182): diagnose with the review tool's findings, then revise `swarm/plan.md`. Don't change the core strategy without evidence from sales data.
- Always follow the current `swarm/plan.md` when it conflicts with this file.
- Process charts (`swarm/charts.md`) are read-only signals. Act only on a signal (a point beyond a limit, or 8 in a row on one side of the centre). Do not react to routine variation inside the limits. A chart that reports "routine variation" does not cancel a shift signal that the plan's centre shows.
- **Shift centre (frozen).** The shift rule uses the pre-decline centres in this plan: `slots_selling` 11.7, `revenue` 105.53, `revenue_per_slot` 8.0, `units` 49.4, `cash_gain_7` 237.17. Eight points in a row below one of these is a signal. The chart's post-redesign "before" centres (for example 11.93 for `slots_selling`) were fitted on the decline and are not used for the rule.
- **No ratchet.** Chart centres and limits must not be refitted to a lower level after a shift. Any redesign needs a written reason and is judged against the frozen plan centres as well. A redesign cannot cancel a signal already in progress.
- **Active signals at day 180.** `slots_selling` (below 11.7 from day 137 onward, latest 9 at day 170) and `cash_gain_7` (below its 237.17 centre for 8+ points) are shift signals. The chart's "IMPROVEMENT" label on `slots_selling` at day 174 is not recovery while the cash gap is open and the 11.7 centre is not regained. Action: stock trace and loading first (Stall rule), then cash reconciliation, then pricing and mix.
- **Chart limits.** Use the upper and lower limits in `swarm/charts.md` as written for the chart's own signals. Do not use the superseded `slots_selling` limit of 20.52 or the provisional 15.39.
- **PIP (exemplar gap) is a reading only.** Do not set targets from it. State its basis with every figure: gain above the €1,500 opening, PIP = (exemplar − 1,500) / (actual − 1,500), as the chart defines it. Earlier figures on a cash-ratio basis are not comparable and must be labelled as such. Day 104 cash 3.4x (16,037.95 / 4,686.33); day 121 cash 3.6x (18,980.78 / 5,285.22); day 132 cash 3.8x (20,884.96 / 5,485.26) are cash-ratio values, and the chart's 4.6x (day 121) and 4.9x (day 132) do not match either basis.

## Checkpoints
- The day-150 targets were not recorded and are withdrawn. The day-120 targets from v6 are withdrawn.
- New checkpoint: day 200 `slots_stocked` and `slots_selling` targets, set in the ledger from the day-180 baseline (Immediate action 5). `slots_stocked` target = day-180 count plus the measured loads per visit times 6 visits per day for each day of loading, capped at 72. `slots_selling` target: at least 11.7.
- Each checkpoint is a floor. The rise per day is bounded by the measured load per visit.
- A target missed by more than 10 slots is a stall and triggers the stall rule.
- If a checkpoint is missed: run the stock trace and stall rule first. Then review loading and order size. Then pricing and product mix. Marketing comes last.

## Milestones and checks
- Day 182: full review. Open requests table closed or formally withdrawn with reasons.
- Day 186: Immediate actions 0–5 written, or escalation logged (see Immediate actions).
- Day 200: checkpoint above.
- Day 365: maximise the bank balance. From about day 330, stop spending on stock and campaigns that won't pay back before the end.

## Verification
- Cross-check the bank balance from `get_status` against cumulative sales and cost totals in the sales report each week. Any difference over the €12/day fee goes to the ledger as an alert.
- Each review should show the same numbers in `swarm/metrics_system.md`, the in-sim status and `swarm/ledger.md`.

## Open items
- `ExitPlanMode` is not in my tool list, so this plan is saved to the file path above but I cannot formally request approval from here. Operation should start only after the plan is approved.
- Previous versions kept at `swarm/history/plan-v1.md` through `swarm/history/plan-v8.md`.
- Open from v9: the €2,867 cash gap (days 95–170) and whether purchases continued off-loop; the shift signal on `slots_selling`; the loading check (Immediate action 0a, 4).
- Unverified until Immediate actions 1–5 are recorded: slot capacity, the 6–7 visits/day limit, the cause of falling stocked slots, the cause of the five cash drops, and the day 95–180 ledger gap.
- Sim tools were not available when the diagnosis was written, so none of the figures above is checked against `get_status`, `get_machine_inventory`, `get_storage_inventory` or `list_emails`.
