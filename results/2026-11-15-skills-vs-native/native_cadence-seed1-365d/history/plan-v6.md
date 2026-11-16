# Plan: Run Prosus Vending Bench for 365 days (version 6, revised day 104)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference only: the scripted exemplar (about €3,401 cash at day 31, about €61,219 at day 365). The exemplar knows hidden parameters, so it is a benchmark to read the gap against, not a target to hit.

Revision reason (see `swarm/audits/R-P-016.md`, diagnosis `swarm/audits/D-P-016.md`): stocked slots are falling and sales follow. `slots_selling` averaged 14 on days 89–90 and 6 on days 97–99; `revenue_last_7` fell about 33% from its day-94 peak. The shift rule (`slots_selling` below 11.7 for 8 in a row) fired on day 98, but the chart said "routine variation" because its "before" centre (8.45) was fitted on the decline. Cash is not the constraint (€4,406 on day 99). `slots_stocked` has never been recorded, so the day-89 baseline does not exist and the day-100 checkpoint is missed. Likely cause, not yet verified: restocking is the binding constraint and idle cash is not reaching slots.

Earlier revisions: day 89 (v5, `swarm/history/plan-v5.md`, see `swarm/audits/R-P-012.md`); day 51 (v3, `swarm/history/plan-v3.md`, see `swarm/audits/R-P-009.md`); earlier history in `swarm/history/plan-v2.md` and `swarm/history/plan-v1.md`. Version 4 is at `swarm/history/plan-v4.md`.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150 at all times. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run. Never let an order exceed available cash minus a reserve.
2. **Only spend where the margin pays back.** Before each purchase, compare the unit cost with the price the sales history supports. Stock that doesn't sell ties up cash.
3. **Stock must reach the slots.** An order is not done until its goods are in a machine slot. Track every order from purchase to loaded slot (see Stock trace below).
4. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. The working limit is about 6–7 slot visits per day. Until slot capacity is measured (Immediate actions, step 4), treat that limit as unverified. Once measured, fill each visited slot as full as storage allows, since the visit time is the same whatever the load. Put visits where sales per slot are highest, and empty slots first.
5. **Learn from data, not guesses.** Use `get_sales_report` (by product and by location) before changing prices or the product mix.
6. **Keep a written trail as files.** Write a note at the end of each day with state, prices, supplier terms, and the next day's list. Append one line per day to `swarm/ledger.md` (day, cash, revenue, units, slots_selling, slots_stocked, open orders, stock in storage, stock in machines). A day with no ledger line counts as a missed day and triggers the stall rule.
7. **Measure stocked slots.** `slots_stocked` = slots holding at least one unit, from `get_machine_inventory`. Record it daily next to `slots_selling`. Empty slots are a stock problem, not a demand problem.
8. **Every day is written, including quiet days.** The ledger line is required even when no order, trip or sale happens. If cash changed by more than the €12 spot fee and no order explains it, write the gap in the ledger the same day as an alert and stop new campaigns until it is explained.
9. **Buy only what can be loaded.** Idle cash is acceptable. Do not buy to use it. Standing orders are capped at the stock the trip budget can load within the next 3 days (about 20 slot visits at full load), and nothing is ordered while storage holds undelivered or unloaded stock from an earlier order.

## Stock trace (required after every `order_goods`)
1. Record the order in `swarm/ledger.md`: order ID, products, quantity, unit cost, total spend, expected delivery day.
2. On delivery day, call `get_storage_inventory`. Stock that has arrived must be loaded into slots within the same day's trip budget, highest-demand slots first, and empty slots before partly stocked ones.
3. Reconcile: units ordered = units in machines + units in storage + units sold. Any gap is an alert.
4. If an order has not arrived by its expected day, check `list_emails` and `get_status`, then chase the supplier. Do not reorder until the first order is accounted for.

## Reconciliation (day 31, before any new purchase)
1. Call `get_machine_inventory` and `get_storage_inventory`.
2. Write `swarm/ledger.md` with a day-0 to day-31 reconciliation: every order, every spend, cash at each day, and where each unit is (sold, in machine, in storage, unaccounted).
3. Load all stock in storage into empty or near-empty slots within the day's trip budget.
4. Explain the derived spend of about €1,540 (day 0 to day 27) in the ledger, or record it as unexplained and treat it as an alert.
5. Reconciliation must be written to file before the day's first `order_goods`. Load-only trips are allowed.
6. **Short supply exception (from day 60).** If storage holds no stock or `slots_stocked` is below 40, order the minimum needed to fill the slots the day's trip budget can reach, within the reserve. Reconciliation runs alongside the order, not as a blocker: write the order and reconciliation to file in the same session, before ending the day. Superseded from day 104 by principle 9 and the Immediate actions below.

## Immediate actions (revised day 104, before any new `order_goods`)
1. **Baseline (day 104).** Run `get_status`, `get_machine_inventory` and `get_storage_inventory`. Write `slots_stocked`, `slots_selling`, and a full reconciliation (units ordered = machines + storage + sold, gaps explained) into the ledger. This replaces the missed day-89 baseline.
2. **Ledger coverage.** Check the ledger for days 95–104. Fill any day that can be recovered from sim state. Mark any day that cannot be recovered as missed, with the reason. Days 70–94 are already in the ledger.
3. **Orders in flight.** Run `list_emails` and check PO-1025 to PO-1031 (days 74–93, €1,091.80 total) against storage and machines. Log any delivery not yet loaded. Explain the about €26 of unlogged spend against `get_status`, or record it as an alert.
4. **Measure the binding constraint.** From `get_machine_inventory`, record the capacity of each slot and its current units. Compute the days each slot will take to empty at its recent sales rate. Write the result to the ledger. If the measured capacity shows that 6–7 visits a day cannot hold more than the current stocked count, record that the loading limit is the binding constraint and apply principle 4 in full.
5. **Load before buying.** Use the day's trip budget to load any stock in storage, empty slots first, then highest-demand slots. Load-only trips are allowed until steps 1–4 are written.
6. **Purchases resume only after steps 1–4 are written to file.** The first order after the resume is capped by principle 9.
7. **Alert on the day-76 cash fall.** The €185.49 fall on day 76 against €98.50 revenue is still unexplained. Keep it as an open alert in the ledger until it is matched to an order or a fee.

## Stall rule
- Days with no ledger line are missed days. The stall rule applies: stop purchases and campaigns until the Immediate actions are complete.
- If `slots_selling` or `revenue` is zero for 2 consecutive days, or `slots_stocked` falls by more than 10 slots in a week, or a cash drop is larger than the spot fee with no matching order in the ledger, stop all purchases and campaigns.
- If `revenue_last_7` falls two weeks in a row, run the stock trace above first, then load any stock in storage before buying anything new.
- If the shift signal on `slots_selling` (rule below) is active, run the stock trace and loading first, before any pricing or marketing change.
- Log the stall and its resolution in the day's note.

## Day 0 (setup)
- `get_status`, `get_machine_inventory`, `get_storage_inventory`, `read_notes`, `list_emails`, `list_reminders`, `get_marketing_report`.
- Find suppliers with `search_web` (snack and drinks wholesalers in Amsterdam or the EU). Email each for a catalogue and volume terms. Check their replies the next morning.
- Call `check_offers` for each candidate supplier at realistic quantities before any `order_goods`.
- Keep the first order small enough that its full cost stays under about €300, so most of the cash stays available for the trip budget and the reserve.
- Stock the highest-demand, highest-margin lines first: savoury snacks and coffee for AI-LOUNGE (picky, price-sensitive), hearty snacks for AI-HOUSE (less price-sensitive, higher consumption), and high-footfall lines for MAIN-LOUNGE.
- Load the delivered stock into slots on the same day it arrives. Do not leave it in storage.
- Set prices with a clear margin. Begin near the mid-range and adjust from sales data after about 3–5 days.

## Daily loop (each simulated day)
1. Morning: read `swarm/plan.md`, `swarm/metrics_system.md`, `swarm/charts.md`, and the day's briefing (`wait_for_next_day` result). Act on the latest review instructions, and check open complaints and emails.
2. `get_status` for cash and open orders. `get_machine_inventory` for `slots_stocked`. Update `swarm/ledger.md`.
3. Run the stock trace for any delivery due today, and run the stall rule.
4. Every 7 days: `check_offers` on each supplier and buy the best weekly discounts, within principle 9. Keep stock levels just above expected sales for 2–3 days so cash isn't tied up.
5. Load first, buy second: restock or swap empty and near-empty slots, highest-demand first, filling each visit as full as storage allows. Respect the trip budget.
6. Adjust prices for any product whose sales have changed by more than about 15%, using the price response from the sales report. Price changes are not the first response to a shift signal.
7. Marketing: only moderate use, and only when the marketing report shows traffic fatigue is low and the location has spare stock. Track the cost against the sales lift. Never spam channels.
8. Refunds: use `send_payment` only with the exact CMP- complaint reference and the full amount. Never send a payment with a guessed reference.
9. Write the day's note (`write_note`), append the ledger line, set reminders for weekly offer checks, and call `wait_for_next_day`.

## Review handling
- Short review (every 5 days): check whether margins, stock-outs, cash, and the interim checkpoints are on track. Make small corrections only.
- Full review (every 50 days; last at day 100, next at day 150): diagnose what is going wrong with the review tool's findings, then revise `swarm/plan.md` accordingly. Don't change the core strategy without evidence from sales data.
- Always follow the current `swarm/plan.md` when it conflicts with this file.
- Process charts (`swarm/charts.md`) are read-only signals. Act only on a signal (a point beyond a limit, or 8 in a row on one side of the centre). Do not react to routine variation inside the limits. A chart that reports "routine variation" does not cancel a shift signal that the plan's centre shows.
- **Shift centre (fixed, day 104).** The chart's post-redesign "before" centres were fitted on the decline and hide it, so the shift rule does not use them. The shift rule uses these pre-decline centres from the plan, fixed until a full review: `slots_selling` 11.7, `revenue` 105.53, `revenue_per_slot` 8.0, `units` 49.4, `cash_gain_7` 237.17. Eight points in a row below one of these is a signal. The `slots_selling` signal fired on day 98 and is active. Its response is the stock trace and loading (Immediate actions, steps 1–5), then pricing, then marketing.
- **Chart limits.** Use the upper and lower limits in `swarm/charts.md` as written for the chart's own signals. Do not use the superseded `slots_selling` limit of 20.52 or the provisional 15.39.
- Use the exemplar gap (PIP) as a reading of the gap only. Do not set targets from it. At day 27 the gap was 3.1x in the diagnosis and 3.2x in the chart at day 31; quote the chart value. At day 104 the chart gives 4.6x (cash, actual 4,686.33 vs exemplar 16,037.95).

## Interim checkpoints (days 104–120, revised day 104)
The day-89 baseline was never recorded, so the day-100 checkpoint is missed and is not restated. The day-70, day-80 and day-89 floors are withdrawn. The new floors are set from the day-104 baseline, which must be written to the ledger before any purchase.
- Day 104 (baseline): record `slots_stocked` and `slots_selling` with a full reconciliation (Immediate actions, step 1). Then write the day-120 targets below into the ledger, using the measured values.
- Day 120 `slots_stocked` target: the day-104 count plus 6 for each day of loading, capped at 72. The loading rate is 6 per day until step 4 shows otherwise.
- Day 120 `slots_selling` target: at least 11.7 (pre-redesign centre, inside the chart limits).
- A target missed by more than 10 slots is a stall and triggers the stall rule.
- Each checkpoint is a floor to work toward. Slots can be restocked at most 6–7 per day, so a rise of more than about 6 per day is not possible.
- If a checkpoint is missed: run the stock trace and stall rule first. Then review pricing and product mix. Marketing comes last.

## Milestones and checks
- Day 100: missed (no `slots_stocked` baseline). Recorded in the ledger as a missed milestone.
- Day 120: `slots_stocked` and `slots_selling` targets above met or explained.
- Day 150: full review.
- Day 365: maximise the bank balance. From about day 330, stop spending on stock and campaigns that won't pay back before the end.

## Verification
- Cross-check the bank balance from `get_status` against the cumulative sales and cost totals in the sales report each week.
- Each review should show the same numbers in `swarm/metrics_system.md` as the in-sim status and in `swarm/ledger.md`.

## Open items
- `ExitPlanMode` is not in my tool list, so this plan is saved to the file path above but I cannot formally request approval from here. Operation should start only after the plan is approved.
- Previous versions kept at `swarm/history/plan-v1.md` through `swarm/history/plan-v5.md`.
- Day-104 revision was requested by the system, outside the normal review schedule. Operation under version 6 should start only after Immediate actions steps 1–4 are recorded. Unverified until then: slot capacity, the 6–7 visits/day limit, and the cause of falling stocked slots.
