# Plan: Run Prosus Vending Bench for 365 days (version 3, revised day 31)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference only: the scripted exemplar (about €3,401 cash at day 31, about €61,219 at day 365). The exemplar knows hidden parameters, so it is a benchmark to read the gap against, not a target to hit.

Revision reason (see `swarm/audits/R-P-005.md`, diagnosis `swarm/audits/D-P-005.md`): only 13–15 of 72 slots sell on a normal day. Revenue per selling slot is healthy, so the gap is stock not reaching slots. The day-30 cash target (about €3,200) was unreachable at observed rates, and the plan had no measure of stocked slots. Version 2 is kept at `swarm/history/plan-v2.md`.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150 at all times. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run. Never let an order exceed available cash minus a reserve.
2. **Only spend where the margin pays back.** Before each purchase, compare the unit cost with the price the sales history supports. Stock that doesn't sell ties up cash.
3. **Stock must reach the slots.** An order is not done until its goods are in a machine slot. Track every order from purchase to loaded slot (see Stock trace below).
4. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. Plan at most about 4–5 machine trips per day, and put the trips where the sales lift is largest.
5. **Learn from data, not guesses.** Use `get_sales_report` (by product and by location) before changing prices or the product mix.
6. **Keep a written trail as files.** Write a note at the end of each day with state, prices, supplier terms, and the next day's list. Append one line per day to `swarm/ledger.md` (day, cash, revenue, units, slots_selling, slots_stocked, open orders, stock in storage, stock in machines). A day with no ledger line counts as a missed day and triggers the stall rule.
7. **Measure stocked slots.** `slots_stocked` = slots holding at least one unit, from `get_machine_inventory`. Record it daily next to `slots_selling`. Empty slots are a stock problem, not a demand problem.

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
5. No `order_goods` until steps 1–4 are written to file. Load-only trips are allowed.

## Stall rule
- If `slots_selling` or `revenue` is zero for 2 consecutive days, or `slots_stocked` falls by more than 10 slots in a week, or a cash drop is larger than the spot fee with no matching order in the ledger, stop all purchases and campaigns.
- If `revenue_last_7` falls two weeks in a row, run the stock trace before any purchase.
- Run the stock trace above first, then load any stock in storage before buying anything new.
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
- Full review (every 50 days; next at day 50): diagnose what is going wrong with the review tool's findings, then revise `swarm/plan.md` accordingly. Don't change the core strategy without evidence from sales data.
- Always follow the current `swarm/plan.md` when it conflicts with this file.
- Process charts (`swarm/charts.md`) are read-only signals. Act only on a signal (a point beyond a limit, or 8 in a row on one side of the centre). Do not react to routine variation inside the limits.
- Use the exemplar gap (PIP) as a reading of the gap only. Do not set targets from it. At day 27 the gap was 3.1x in the diagnosis and 3.2x in the chart at day 31; quote the chart value.

## Interim checkpoints (days 31–60)
Targets come from the process-chart centres and the day-31 state (cash €2,089.62, slots_selling 16, centre 11.9, upper limit 20.16). Each checkpoint is a floor the operator should reach by working the stock trace, not a forecast.
- Day 38: `slots_stocked` at least 30 of 72. `slots_selling` at least 16. Reconciliation written and unaccounted units at zero or explained.
- Day 45: `slots_stocked` at least 40 of 72. `slots_selling` at least 20 (chart upper limit). Cash at or above €2,400 (two weeks at the cash_gain_7 centre of about €268/week would give about €2,625; the floor sits below that).
- Day 60: `slots_selling` at least 24 of 72. `revenue_last_7` above its day-45 figure. Cash at or above €2,900.
- Day 30 cash target of about €3,200 is withdrawn.
- If a checkpoint is missed: run the stock trace and stall rule first. Then review pricing and product mix. Marketing comes last.

## Milestones and checks
- Day 100: positive trend in weekly net profit. Stock-out rate low in all six machines. `slots_stocked` at least 60 of 72.
- Day 365: maximise the bank balance. From about day 330, stop spending on stock and campaigns that won't pay back before the end.

## Verification
- Cross-check the bank balance from `get_status` against the cumulative sales and cost totals in the sales report each week.
- Each review should show the same numbers in `swarm/metrics_system.md` as the in-sim status and in `swarm/ledger.md`.

## Open items
- `ExitPlanMode` is not in my tool list, so this plan is saved to the file path above but I cannot formally request approval from here. Operation should start only after the plan is approved.
- Previous versions kept at `swarm/history/plan-v1.md` and `swarm/history/plan-v2.md`.
