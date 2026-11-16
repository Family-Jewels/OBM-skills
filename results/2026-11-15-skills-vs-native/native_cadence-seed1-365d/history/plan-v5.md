# Plan: Run Prosus Vending Bench for 365 days (version 5, revised day 89)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference only: the scripted exemplar (about €3,401 cash at day 31, about €61,219 at day 365). The exemplar knows hidden parameters, so it is a benchmark to read the gap against, not a target to hit.

Revision reason (see `swarm/audits/R-P-009.md`, diagnosis `swarm/audits/D-P-009.md`): at day 51 cash was healthy (€2,734.80) but restocking had stopped (last order day 41, PO-1017 undelivered), `slots_stocked` was never recorded, no ledger lines were written for days 43–51, and about €260 of cash outflow in days 46–51 had no logged cause. `slots_selling` fell from 10–14 to 4. Version 3 is kept at `swarm/history/plan-v3.md`. Earlier history: `swarm/history/plan-v2.md`.

Revision at day 89 (see `swarm/audits/R-P-012.md`, diagnosis `swarm/audits/D-P-012.md`): stock is not reaching the machines. `slots_selling` fell from an average of 11.7 to 8.3 over days 67–76, while cash (€3,582 on day 76) and revenue per selling slot are normal. Restocking was never measured, the day-60 baseline does not exist, the ledger has no lines for days 70–76, PO-1023 (due day 71) has no stock trace, and the €185.49 cash fall on day 76 is unexplained. Version 4 is kept at `swarm/history/plan-v4.md`.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150 at all times. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run. Never let an order exceed available cash minus a reserve.
2. **Only spend where the margin pays back.** Before each purchase, compare the unit cost with the price the sales history supports. Stock that doesn't sell ties up cash.
3. **Stock must reach the slots.** An order is not done until its goods are in a machine slot. Track every order from purchase to loaded slot (see Stock trace below).
4. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. The physical limit is about 6–7 slots restocked per day, so plan the day's trips to that figure and put them where the sales lift is largest. Floors below are set to this limit.
5. **Learn from data, not guesses.** Use `get_sales_report` (by product and by location) before changing prices or the product mix.
6. **Keep a written trail as files.** Write a note at the end of each day with state, prices, supplier terms, and the next day's list. Append one line per day to `swarm/ledger.md` (day, cash, revenue, units, slots_selling, slots_stocked, open orders, stock in storage, stock in machines). A day with no ledger line counts as a missed day and triggers the stall rule.
7. **Measure stocked slots.** `slots_stocked` = slots holding at least one unit, from `get_machine_inventory`. Record it daily next to `slots_selling`. Empty slots are a stock problem, not a demand problem.
8. **Every day is written, including quiet days.** The ledger line is required even when no order, trip or sale happens. If cash changed by more than the €12 spot fee and no order explains it, write the gap in the ledger the same day as an alert and stop new campaigns until it is explained.

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
6. **Short supply exception (from day 60).** If storage holds no stock or `slots_stocked` is below 40, order the minimum needed to fill the slots the day's trip budget can reach, within the reserve. Reconciliation runs alongside the order, not as a blocker: write the order and reconciliation to file in the same session, before ending the day.

## Immediate actions (revised day 89, before any new `order_goods`)
1. Write the missing ledger lines for days 70–76 from the sim state where it can be recovered. Mark any day that cannot be recovered as missed, in the ledger, with the reason.
2. Run `get_status`, `get_machine_inventory`, `get_storage_inventory` and `list_emails`, and record the results in the ledger.
3. Stock trace on PO-1023 (due day 71): find its delivery status, confirm whether it arrived, and reconcile units ordered = machines + storage + sold. If it arrived, load it into the highest-demand empty slots first.
4. Explain the €185.49 cash fall on day 76 against the €98.50 revenue. Check whether PO-1023 (€207.90) or PO-1024 was debited. Until it is explained, treat "already paid" for PO-1023 and PO-1024 as unverified and log the day-76 gap as an alert.
5. Start the daily `slots_stocked` record from the next day and keep it every day, including quiet days. Stock trips take priority over new purchases.
6. Purchases resume only after steps 1–4 are written to file. Load-only trips are allowed before then.

## Stall rule
- Days 70–76 with no ledger line are missed days. The stall rule applies: stop purchases and campaigns until the Immediate actions are complete.
- If `slots_selling` or `revenue` is zero for 2 consecutive days, or `slots_stocked` falls by more than 10 slots in a week, or a cash drop is larger than the spot fee with no matching order in the ledger, stop all purchases and campaigns.
- If `revenue_last_7` falls two weeks in a row, run the stock trace above first, then load any stock in storage before buying anything new.
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
4. Every 7 days: `check_offers` on each supplier and buy the best weekly discounts. Keep stock levels just above expected sales for 2–3 days so cash isn't tied up.
5. Load first, buy second: restock or swap empty and near-empty slots, highest-demand first. Respect the trip budget.
6. Adjust prices for any product whose sales have changed by more than about 15%, using the price response from the sales report.
7. Marketing: only moderate use, and only when the marketing report shows traffic fatigue is low and the location has spare stock. Track the cost against the sales lift. Never spam channels.
8. Refunds: use `send_payment` only with the exact CMP- complaint reference and the full amount. Never send a payment with a guessed reference.
9. Write the day's note (`write_note`), append the ledger line, set reminders for weekly offer checks, and call `wait_for_next_day`.

## Review handling
- Short review (every 5 days): check whether margins, stock-outs, cash, and the interim checkpoints are on track. Make small corrections only.
- Full review (every 50 days; last at day 50, next at day 100): diagnose what is going wrong with the review tool's findings, then revise `swarm/plan.md` accordingly. Don't change the core strategy without evidence from sales data.
- Always follow the current `swarm/plan.md` when it conflicts with this file.
- Process charts (`swarm/charts.md`) are read-only signals. Act only on a signal (a point beyond a limit, or 8 in a row on one side of the centre). Do not react to routine variation inside the limits.
- **Shift centre (set explicitly, day 89).** The chart judges the post-redesign period against its own fitted centre, which hides the decline. For the shift rule, use the pre-redesign centres from the charts' "before" column (`slots_selling` 11.7, `revenue` 105.53, `revenue_per_slot` 8.0, `units` 49.4, `cash_gain_7` 237.17). Eight points in a row below one of these is a signal: run the stock trace first, then pricing, then marketing. Reset the centre only at a full review.
- **Chart limits.** Use the upper and lower limits in `swarm/charts.md` as written. Do not use the superseded `slots_selling` limit of 20.52 or the provisional 15.39.
- Use the exemplar gap (PIP) as a reading of the gap only. Do not set targets from it. At day 27 the gap was 3.1x in the diagnosis and 3.2x in the chart at day 31; quote the chart value.

## Interim checkpoints (days 89–120, revised day 89)
The day-70 and day-80 floors are withdrawn. The day-60 baseline was never recorded, and the day-70 `slots_selling` floor of 20 used a superseded chart limit. The floors below use the 6–7 slots/day limit and are set from the first measured baseline.
- Day 89 (the next morning): write `slots_stocked` and `slots_selling` into the ledger with a full reconciliation (units ordered = machines + storage + sold, gaps explained). This is the baseline.
- Day 100: `slots_stocked` at least 60 of 72. `slots_selling` at least 11.7 (pre-redesign centre, inside the chart limits).
- Day 120: `slots_stocked` at least 66 of 72. `slots_selling` at least 13.
- Each checkpoint is a floor to work toward. Slots can be restocked at most 6–7 per day, so a rise of more than about 6 per day is not possible.
- If a checkpoint is missed: run the stock trace and stall rule first. Then review pricing and product mix. Marketing comes last.

## Milestones and checks
- Day 100: positive trend in weekly net profit. Stock-out rate low in all six machines. `slots_stocked` at least 60 of 72.
- Day 365: maximise the bank balance. From about day 330, stop spending on stock and campaigns that won't pay back before the end.

## Verification
- Cross-check the bank balance from `get_status` against the cumulative sales and cost totals in the sales report each week.
- Each review should show the same numbers in `swarm/metrics_system.md` as the in-sim status and in `swarm/ledger.md`.

## Open items
- `ExitPlanMode` is not in my tool list, so this plan is saved to the file path above but I cannot formally request approval from here. Operation should start only after the plan is approved.
- Previous versions kept at `swarm/history/plan-v1.md`, `swarm/history/plan-v2.md`, `swarm/history/plan-v3.md` and `swarm/history/plan-v4.md`.
- Day-89 revision was requested by the system, outside the normal review schedule. Operation under version 5 should start only after the Immediate actions are recorded.
