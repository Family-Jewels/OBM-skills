# Plan: Run Prosus Vending Bench for 365 days

## Context
Goal: maximise final bank balance from €1,500 over 365 simulated days across three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Unfinished or bankrupt runs score zero, so solvency and continuity come first. Reference benchmark: about €3,228 at day 30 and €61,219 at day 365. Day-30 is the milestone to track against.

Plan mode blocked all vending tools, and the workspace is empty, so this plan is built from the briefing alone. Day 0 must start with live state (status, inventory, notes, marketing and sales reports) before any spending.

## Operating principles
1. **Solvency first.** Keep cash above roughly €150 at all times. The €12/day spot fee must always be payable, since more than 10 consecutive unpaid days ends the run. Never let an order exceed available cash minus a reserve.
2. **Only spend where the margin pays back.** Before each purchase, compare the unit cost with the price the sales history supports. Stock that doesn't sell ties up cash.
3. **Use the day's time budget.** Each restock is 45 min and each swap 30 min, in an 8-hour day. Plan at most about 4–5 machine trips per day, and put the trips where the sales lift is largest.
4. **Learn from data, not guesses.** Use `get_sales_report` (by product and by location) before changing prices or the product mix.
5. **Keep notes and reminders current.** Write a note at the end of each day with state, prices, supplier terms, and the next day's list.

## Day 0 (setup)
- `get_status`, `get_machine_inventory`, `get_storage_inventory`, `read_notes`, `list_emails`, `list_reminders`, `get_marketing_report`.
- Find suppliers with `search_web` (snack and drinks wholesalers in Amsterdam or the EU). Email each for a catalogue and volume terms. Check their replies the next morning.
- Call `check_offers` for each candidate supplier at realistic quantities before any `order_goods`.
- Stock the highest-demand, highest-margin lines first: savoury snacks and coffee for AI-LOUNGE (picky, price-sensitive), hearty snacks for AI-HOUSE (less price-sensitive, higher consumption), and high-footfall lines for MAIN-LOUNGE.
- Set prices with a clear margin. Begin near the mid-range and adjust from sales data after about 3–5 days.

## Daily loop (each simulated day)
1. Morning: read `swarm/plan.md`, `swarm/metrics_system.md`, `swarm/charts.md`, and the day's briefing (`wait_for_next_day` result). Act on the latest review instructions, and check open complaints and emails.
2. `get_status` for cash and open orders.
3. Every 7 days: `check_offers` on each supplier and buy the best weekly discounts. Keep stock levels just above expected sales for 2–3 days so cash isn't tied up.
4. Restock or swap the slots that are near empty or whose demand is highest. Respect the trip budget.
5. Adjust prices for any product whose sales have changed by more than about 15%, using the price response from the sales report.
6. Marketing: only moderate use, and only when the marketing report shows traffic fatigue is low and the location has spare stock. Track the cost against the sales lift. Never spam channels.
7. Refunds: use `send_payment` only with the exact CMP- complaint reference and the full amount. Never send a payment with a guessed reference.
8. Write the day's note (`write_note`), set reminders for weekly offer checks, and call `wait_for_next_day`.

## Review handling
- Short review (every 5 days): check whether margins, stock-outs, and cash are on track. Make small corrections only.
- Full review (every 50 days): diagnose what is going wrong with the review tool's findings, then revise `swarm/plan.md` accordingly. Don't change the core strategy without evidence from sales data.
- Always follow the current `swarm/plan.md` when it conflicts with this file.

## Milestones and checks
- Day 30: cash at or above ~€3,200 (reference benchmark). If behind, review pricing and product mix first, then marketing.
- Day 100: positive trend in weekly net profit. Stock-out rate low in all six machines.
- Day 365: maximise the bank balance. From about day 330, stop spending on stock and campaigns that won't pay back before the end.

## Verification
- Cross-check the bank balance from `get_status` against the cumulative sales and cost totals in the sales report each week.
- Each review should show the same numbers in `swarm/metrics_system.md` as the in-sim status.

## Open items
- `ExitPlanMode` is not in my tool list, so this plan is saved to the file path above but I cannot formally request approval from here. Operation should start only after the plan is approved.
