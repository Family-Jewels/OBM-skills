# Plan: Run Prosus Vending Bench for 365 days (version 2, revised day 9)

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference benchmark: about €3,228 at day 30 and €61,219 at day 365. Day-30 is the milestone to track against.

Revision reason (see `swarm/audits/R-P-001.md`, diagnosis `swarm/audits/D-P-001.md`): the machines made no sales from day 0 to day 6 while about €450 was spent before day 2. The stock was most likely bought but not loaded into slots. Version 1 had no check that stock reached the machines, and no interim targets between day 7 and day 30.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150 at all times. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run. Never let an order exceed available cash minus a reserve.
2. **Only spend where the margin pays back.** Before each purchase, compare the unit cost with the price the sales history supports. Stock that doesn't sell ties up cash.
3. **Stock must reach the slots.** An order is not done until its goods are in a machine slot. Track every order from purchase to loaded slot (see Stock trace below).
4. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. Plan at most about 4–5 machine trips per day, and put the trips where the sales lift is largest.
5. **Learn from data, not guesses.** Use `get_sales_report` (by product and by location) before changing prices or the product mix.
6. **Keep a written trail.** Write a note at the end of each day with state, prices, supplier terms, and the next day's list. Also append one line per day to `swarm/ledger.md` (day, cash, revenue, units, slots_selling, open orders, stock in storage, stock in machines). The notes must exist as files so a stall can be traced later.

## Stock trace (required after every `order_goods`)
1. Record the order in `swarm/ledger.md`: order ID, products, quantity, unit cost, total spend, expected delivery day.
2. On delivery day, call `get_storage_inventory`. Stock that has arrived must be loaded into slots within the same day's trip budget, highest-demand slots first.
3. Reconcile: units ordered = units in machines + units in storage + units sold. Any gap is an alert.
4. If an order has not arrived by its expected day, check `list_emails` and `get_status`, then chase the supplier. Do not reorder until the first order is accounted for.

## Stall rule
- If `slots_selling` or `revenue` is zero for 2 consecutive days, or a cash drop is larger than the spot fee with no matching order in the ledger, stop all purchases and campaigns.
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
2. `get_status` for cash and open orders. Update `swarm/ledger.md`.
3. Run the stock trace for any delivery due today, and run the stall rule.
4. Every 7 days: `check_offers` on each supplier and buy the best weekly discounts. Keep stock levels just above expected sales for 2–3 days so cash isn't tied up.
5. Restock or swap the slots that are near empty or whose demand is highest. Respect the trip budget.
6. Adjust prices for any product whose sales have changed by more than about 15%, using the price response from the sales report.
7. Marketing: only moderate use, and only when the marketing report shows traffic fatigue is low and the location has spare stock. Track the cost against the sales lift. Never spam channels.
8. Refunds: use `send_payment` only with the exact CMP- complaint reference and the full amount. Never send a payment with a guessed reference.
9. Write the day's note (`write_note`), append the ledger line, set reminders for weekly offer checks, and call `wait_for_next_day`.

## Review handling
- Short review (every 5 days): check whether margins, stock-outs, cash, and the interim checkpoints are on track. Make small corrections only.
- Full review (every 50 days): diagnose what is going wrong with the review tool's findings, then revise `swarm/plan.md` accordingly. Don't change the core strategy without evidence from sales data.
- Always follow the current `swarm/plan.md` when it conflicts with this file.
- Process charts (`swarm/charts.md`) are read-only signals. Act only on a signal (a point beyond a limit, or 8 in a row on one side of the centre). Do not react to routine variation inside the limits. Charts stay in the collecting phase until day 8, so no signal is available before then.

## Interim checkpoints (days 7–30)
Targets come from the day-9 gap to the exemplar (cash €1,067.7 against €2,018.4). Each checkpoint is a floor, not a forecast.
- Day 14: `slots_selling` at least 24 of 72. `revenue_last_7` above the previous 7-day figure.
- Day 21: `slots_selling` at least 40 of 72. `revenue_last_7` above day 14's figure. Cash at or above €1,150.
- Day 30: cash at or above ~€3,200 (reference benchmark). Revenue for the last 7 days rising for three weeks in a row.
- If a checkpoint is missed: run the stock trace and stall rule first. Then review pricing and product mix. Marketing comes last.

## Milestones and checks
- Day 100: positive trend in weekly net profit. Stock-out rate low in all six machines.
- Day 365: maximise the bank balance. From about day 330, stop spending on stock and campaigns that won't pay back before the end.

## Verification
- Cross-check the bank balance from `get_status` against the cumulative sales and cost totals in the sales report each week.
- Each review should show the same numbers in `swarm/metrics_system.md` as the in-sim status and in `swarm/ledger.md`.

## Open items
- `ExitPlanMode` is not in my tool list, so this plan is saved to the file path above but I cannot formally request approval from here. Operation should start only after the plan is approved.
- Previous version kept at `swarm/history/plan-v1.md`.
