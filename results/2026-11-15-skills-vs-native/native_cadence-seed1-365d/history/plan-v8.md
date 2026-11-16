# Plan: Run Prosus Vending Bench for 365 days (version 8, revised day 165)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference only: the scripted exemplar (about €3,401 cash at day 31, about €61,219 at day 365). The exemplar knows hidden parameters, so it is a benchmark to read the gap against, not a target to hit.

Revision reason, v8 (day 165; see `swarm/audits/D-P-024.md`, record `swarm/audits/R-P-024.md`, previous version `swarm/history/plan-v7.md`):
- Unexplained cash outflow continues: about €2,335 from day 95 to day 159, about €36/day, not stopped (about €22/day days 149–159). Purchases appear to continue outside the gated loop. v8 makes the gate enforceable and stops all buying until the gap is traced.
- Deadlock: the purchase gate needs a ledger line, but the ledger lapsed at day 94, so the gate stayed shut while money still left. v8 gives a way to reopen the gate that does not depend on buying (principle 10, Immediate action 0).
- Sales shift: `slots_selling` has been below the fixed 11.7 centre since day 144 (8+ in a row, still below at day 159). The chart said "no shift yet" because its centre was refitted on the decline. v8 freezes the chart centres out of the shift rule (Review handling).
- Revenue: `revenue_last_7` fell two weeks running (511, 502, 274, 340 at days 134–159), meeting the stall rule's revenue trigger.
- Every review since day 45 has asked for the stock trace; none is on file. v8 makes it a blocking step.

Revision reason, v7 (see `swarm/audits/R-P-020.md`, diagnosis `swarm/audits/D-P-020.md`, previous version `swarm/history/plan-v6.md`):
- The ledger lapsed after day 94. Days 95–121 have no ledger line, so the stall rule never ran. Cash rose about €870 where sales less fees implied about €2,006; about €1,136 is unexplained.
- Five large cash drops (d99, d104, d107, d111, d117) match purchase-order sizes. The d99 drop is close to PO-1031 (€162.60), which the ledger records as paid on d93. Purchasing appears to have continued while the gate was closed.
- Selling slots have plateaued at about 10–15 of 72 since day 52. The likely binding constraint is loading throughput, not demand or cash (cash €5,285 on day 121). Unverified: `slots_stocked` and slot capacity have never been recorded.
- Chart PIP values were wrong (see Review handling). Plan v6's day-100 and day-120 checkpoints were never met or recorded.

Earlier revisions: day 104 (v6, `swarm/history/plan-v6.md`); day 89 (v5, `swarm/history/plan-v5.md`, see `swarm/audits/R-P-012.md`); day 51 (v3, `swarm/history/plan-v3.md`, see `swarm/audits/R-P-009.md`); earlier history in `swarm/history/plan-v2.md` and `swarm/history/plan-v1.md`. Version 4 is at `swarm/history/plan-v4.md`.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150 at all times. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run. Never let an order exceed available cash minus a reserve.
2. **Only spend where the margin pays back.** Before each purchase, compare the unit cost with the price the sales history supports. Stock that doesn't sell ties up cash.
3. **Stock must reach the slots.** An order is not done until its goods are in a machine slot. Track every order from purchase to loaded slot (see Stock trace).
4. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. The working limit is about 6–7 slot visits per day, still unverified until Immediate action 4 is recorded. Fill each visited slot as full as storage allows, since the visit time is the same whatever the load. Visit empty slots first, then highest-sales-per-slot slots.
5. **Learn from data, not guesses.** Use `get_sales_report` (by product and by location) before changing prices or the product mix.
6. **Every day is written, with no gaps.** Append one line per day to `swarm/ledger.md`: day, cash, revenue, units, slots_selling, slots_stocked, open orders, stock in storage, stock in machines, and the source of every cash change (order ID, fee, sale, refund). A day with no ledger line is a missed day. Missed days are never back-filled silently: mark them as missed, with the reason, in the ledger.
7. **Measure stocked slots daily.** `slots_stocked` = slots holding at least one unit, from `get_machine_inventory`. Record it next to `slots_selling` every day. Empty slots are a stock problem, not a demand problem.
8. **Attribute every cash change.** If cash changed by more than the €12 spot fee and no order, sale or refund explains it, write the gap in the ledger the same day as an alert. An unexplained change is a stall (see Stall rule).
9. **Buy only what can be loaded.** Idle cash is acceptable. Do not buy to use it. Standing orders are capped at the stock the trip budget can load within the next 3 days (about 20 slot visits at full load). Nothing is ordered while storage holds undelivered or unloaded stock from an earlier order.
10. **Purchase gate.** A purchase is allowed only when all of these hold on the day: (a) the previous day has a ledger line, (b) no unexplained cash change is open, (c) the Stock trace shows no order past its expected delivery day, (d) `slots_stocked` for the day is recorded in the ledger, and (e) the day's `order_goods` call is recorded in the ledger with its order ID before the day ends. If any check fails, buy nothing and load only.
11. **No off-loop buying.** Any `order_goods` or `send_payment` made outside the daily loop, or any cash drop matching an order not in the ledger, is an alert and stops all purchases until the order is traced and logged. Purchases made without a ledger line are not "catch-up" purchases; they are the fault being fixed.
12. **Cash watch.** Compare `get_status` cash with the ledger-implied cash each day (last ledger cash + revenue − fees − logged orders). If the gap exceeds €100 on any day, or grows on two consecutive days, stop purchases and run the stall rule.
13. **Deadlock break.** When the ledger has lapsed, reopen the gate in this order and do not buy in between: (1) write the missed days as missed with reasons, (2) write the day's `slots_stocked` and cash, (3) complete the cash gap trace (Immediate action 0). Step (1) and (2) are logs, not purchases, and must not be skipped to reach a purchase sooner.

## Stock trace (required after every `order_goods`)
1. Record the order in `swarm/ledger.md`: order ID, products, quantity, unit cost, total spend, expected delivery day, and the day it is expected to be paid.
2. On delivery day, call `get_storage_inventory`. Stock that has arrived must be loaded into slots within the same day's trip budget, highest-demand slots first, and empty slots before partly stocked ones.
3. Reconcile: units ordered = units in machines + units in storage + units sold. Any gap is an alert.
4. If an order has not arrived by its expected day, check `list_emails` and `get_status`, then chase the supplier. Do not reorder until the first order is accounted for.
5. Match each payment in `get_status` or the cash history to an order ID. A payment with no matching order is an alert.

## Reconciliation (day 31, before any new purchase)
Done. Kept for reference. Principles 6 and 10 now cover the same checks on every day.

## Immediate actions (revised day 165, before any new `order_goods`)
Purchases are frozen until steps 0–5 are written to file. Load-only trips are allowed. Steps 1–5 from v7 remain open; none is recorded in the files at day 165.
0. **Cash gap trace (day 165, added in v8).** Find the orders behind the ~€2,335 gap (days 95–159). Use `get_storage_inventory`, `get_machine_inventory`, `list_emails` and `get_status`. Record each unlogged order with its ID, cost, and payment day in the ledger, or record the gap as an open alert. If sim tools are unavailable, say so in the ledger and keep purchases frozen.
0a. **Loading.** Load all stock in storage using the day's trip budget, empty slots first. Record `slots_stocked` before any purchase.
1. **Baseline (day 165 or the next day with sim tools).** Run `get_status`, `get_machine_inventory` and `get_storage_inventory`. Write `slots_stocked`, `slots_selling`, cash, and a full reconciliation (units ordered = machines + storage + sold, gaps explained) into the ledger.
2. **Ledger coverage.** Days 95–121 are missing and must be recovered from sim state where possible (cash, sales report, order history). Any day that cannot be recovered is marked missed, with the reason. Days 122–131 must also be checked. Write the result before any purchase.
3. **Cash drops.** For each of d99 (−€175), d104 (−€123), d107 (−€190), d111 (−€100), d117 (−€37), match to an order ID, a fee, or record it as an alert. First check PO-1031's actual payment date. Note whether a second order of similar size exists. Use `list_emails` and `get_status` for order history.
4. **Measure the binding constraint.** From `get_machine_inventory`, record each slot's capacity and current units. Compute the days each slot takes to empty at its recent sales rate. Record the measured loads per visit and visits per day. If visits × units per load cannot exceed the current stocked count, record loading throughput as the binding constraint.
5. **Set checkpoints.** Using the step-1 baseline, write the day-150 `slots_stocked` and `slots_selling` targets into the ledger (see Checkpoints).
6. **Load before buying.** Use the day's trip budget to load any stock in storage, empty slots first, then highest-demand slots. Load-only trips continue until steps 1–5 are written.
7. **Purchases resume** only after steps 1–5 are written and the purchase gate (principle 10) passes. The first order after the resume is capped by principle 9, and its size is set to what the measured loading rate can fill within 3 days.

## Stall rule
- Days with no ledger line are missed days. Stop purchases and campaigns until Immediate actions 1–5 are complete.
- If `slots_selling` or `revenue` is zero for 2 consecutive days, or `slots_stocked` falls by more than 10 slots in a week, or any cash change is larger than the spot fee with no matching order, sale or refund in the ledger, stop all purchases and campaigns.
- If `revenue_last_7` falls two weeks in a row, run the stock trace first, then load any stock in storage before buying anything new.
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
1. Morning: read `swarm/plan.md`, `swarm/metrics_system.md`, `swarm/charts.md`, and the day's briefing (`wait_for_next_day` result). Act on the latest review instructions, and check open complaints and emails.
2. `get_status` for cash and open orders. `get_machine_inventory` for `slots_stocked`. Update `swarm/ledger.md` with the day's line and cash attribution.
3. Run the stock trace for any delivery due today, then the stall rule and the purchase gate.
4. Every 7 days: `check_offers` on each supplier and buy the best weekly discounts, within principles 9 and 10. Keep stock levels just above expected sales for 2–3 days so cash isn't tied up.
5. Load first, buy second: restock or swap empty and near-empty slots, highest-demand first, filling each visit as full as storage allows. Respect the trip budget.
6. Adjust prices for any product whose sales have changed by more than about 15%, using the price response from the sales report. Price changes are not the first response to a shift signal.
7. Marketing: only moderate use, and only when the marketing report shows traffic fatigue is low and the location has spare stock. Track the cost against the sales lift. Never spam channels.
8. Refunds: use `send_payment` only with the exact CMP- complaint reference and the full amount. Never send a payment with a guessed reference.
9. Write the day's note (`write_note`), append the ledger line, set reminders for weekly offer checks, and call `wait_for_next_day`.

## Review handling
- Short review (every 5 days): check the ledger has a line for each day, cash is attributed, and the checkpoints are on track. Make small corrections only.
- Full review (every 50 days; last at day 132 by system request; next at day 182): diagnose with the review tool's findings, then revise `swarm/plan.md`. Don't change the core strategy without evidence from sales data.
- Always follow the current `swarm/plan.md` when it conflicts with this file.
- Process charts (`swarm/charts.md`) are read-only signals. Act only on a signal (a point beyond a limit, or 8 in a row on one side of the centre). Do not react to routine variation inside the limits. A chart that reports "routine variation" does not cancel a shift signal that the plan's centre shows.
- **Shift centre (fixed, since day 104; frozen again in v8).** The shift rule uses the pre-decline centres from the plan: `slots_selling` 11.7, `revenue` 105.53, `revenue_per_slot` 8.0, `units` 49.4, `cash_gain_7` 237.17. Eight points in a row below one of these is a signal. The chart's post-redesign "before" centres (for example 11.93 for `slots_selling`) were fitted on the decline and are not used for the rule.
- **No ratchet (v8).** Chart centres and limits must not be refitted to a lower level after a shift. Any redesign needs a written reason and is judged against the frozen plan centres as well. A redesign cannot cancel a signal already in progress.
- **Active signals at day 165.** `slots_selling` (below 11.7 since day 144, 23 days running to day 159) and `cash_gain_7` (8+ in a row below its centre) are shift signals under the rule above. Action: stock trace and loading first (Stall rule), then reconcile cash, then pricing and mix. Do not read the chart's "routine variation" or "IMPROVEMENT" labels as recovery while the cash gap is open.
- **Chart limits.** Use the upper and lower limits in `swarm/charts.md` as written for the chart's own signals. Do not use the superseded `slots_selling` limit of 20.52 or the provisional 15.39.
- **PIP (exemplar gap) is a reading only.** Do not set targets from it. Corrected values, recomputed from the chart's own figures: day 104 cash 3.4x (16,037.95 / 4,686.33); day 121 cash 3.6x (18,980.78 / 5,285.22); day 132 cash 3.8x (20,884.96 / 5,485.26). The chart's 4.6x (day 121) and 4.9x (day 132) are arithmetic errors. Quote the corrected values.

## Checkpoints (days 132–150, set from the day-132 baseline)
v8 (day 165): the day-150 checkpoints were not recorded and are missed. Day-150 targets are withdrawn as stale. New checkpoint: day 182 (full review) `slots_stocked` and `slots_selling` targets, set from the day-165 or next baseline, using the same rule as below (day-132 count plus measured loads per visit, capped at 72). Until then, the rule for a missed checkpoint applies.
The day-120 targets from v6 were never recorded, so they are withdrawn. Targets are set from the day-132 baseline, written to the ledger before any purchase (Immediate actions, step 5).
- Day 132 (baseline): record `slots_stocked`, `slots_selling`, cash, and the reconciliation.
- Day 150 `slots_stocked` target: the day-132 count plus 6 for each day of loading, capped at 72. Use the measured loads per visit from step 4 once it is recorded, in place of 6.
- Day 150 `slots_selling` target: at least 11.7 (pre-decline centre, inside the chart limits).
- Each checkpoint is a floor to work toward. Slots can be restocked at most 6–7 visits per day, so the rise per day is bounded by the measured load per visit.
- A target missed by more than 10 slots is a stall and triggers the stall rule.
- If a checkpoint is missed: run the stock trace and stall rule first. Then review loading and order size. Then pricing and product mix. Marketing comes last.

## Milestones and checks
- Day 132: baseline, Immediate actions 1–5 written. Missed milestones (day 100, day 120) remain recorded as missed.
- Day 150: `slots_stocked` and `slots_selling` checkpoints met or explained.
- Day 182: full review.
- Day 365: maximise the bank balance. From about day 330, stop spending on stock and campaigns that won't pay back before the end.

## Verification
- Cross-check the bank balance from `get_status` against cumulative sales and cost totals in the sales report each week. Any difference over the €12/day fee goes to the ledger as an alert.
- Each review should show the same numbers in `swarm/metrics_system.md`, the in-sim status and `swarm/ledger.md`.

## Open items
- `ExitPlanMode` is not in my tool list, so this plan is saved to the file path above but I cannot formally request approval from here. Operation should start only after the plan is approved.
- Previous versions kept at `swarm/history/plan-v1.md` through `swarm/history/plan-v7.md`.
- Open from v8: the ~€2,335 cash gap (days 95–159) and whether purchases continued off-loop; the sales shift signal; the 0a loading check. Sim tools were not available when v8 was written, so none of these is verified.
- Unverified until Immediate actions 1–5 are recorded: slot capacity, the 6–7 visits/day limit, the cause of falling stocked slots, the cause of the five cash drops, and the day 95–121 ledger gap.
- The chart's PIP figures for day 121 and day 132 need correcting by the system. The plan uses the corrected values above.
