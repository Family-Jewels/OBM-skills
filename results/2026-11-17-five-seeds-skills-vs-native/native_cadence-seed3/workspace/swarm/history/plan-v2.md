# Plan: Operate Prosus Vending Bench for 365 days (v2, revised day 14 per D-P-001)

## Context
Goal: maximise bank balance at day 365 from EUR 1,500. Unfinished or bankrupt runs score zero, so survival comes first: never let the business sit more than 10 consecutive unpaid days (spot fee EUR 12/day network-wide). Benchmark: roughly EUR 3,228 at day 30 and EUR 61,219 at day 365. The scripted exemplar held 2,306 cash at day 14; we hold about 1,262 (charts.md).

Why this revision: D-P-001 found that only 9 of 72 slots ever sold, selling slots fell from 9 to 3, and revenue per slot fell from 11.72 to 2.25. The cause is capacity: stock and prices did not reach most slots, and restocking started late. The v1 plan had no quantities, coverage target or restock trigger, so none of this was checked. v2 sets those explicitly.

Constraints (unchanged):
- 8-hour day. Restock 45 min, swap 30 min, price change a few minutes. Plan 6–10 machine trips per day.
- Six machines (3 locations x SNACK/DRINKS), 72 slots. Snack rows A/B hold 18, C/D hold 10. Drinks slots hold 10.
- Duplicate products share demand, so extra slots add capacity only if they are stocked and priced.
- Cash banks overnight; card takings settle a day later; open complaints hurt reputation.

## Targets (hard rules)
- Coverage: every one of the 72 slots is loaded and priced. Target 72/72 by end of day 16. An empty or unpriced slot counts as a defect to fix on the next trip.
- Load per slot: snack A/B at least 12 of 18; snack C/D at least 7 of 10; drinks at least 7 of 10.
- Restock trigger: any slot at or below half its capacity is restocked on the next visit to that machine.
- Price: every slot has a price above cost on every visit. Record the price in notes.
- Sales check: get_sales_report by slot and product each day. A slot with stock and no sales for 3 days is either unpriced, the wrong product, or a demand problem. Fix or swap it.
- Cash: each day reconcile balance change against sales, purchases, spot fee and marketing. Any gap above EUR 20 is explained in notes before the next purchase.

## Day 1 to 16 recovery sequence
1. Day 14–15 (first actions): get_machine_inventory on all six machines and get_sales_report by product for the last 5 days. Record empty, unpriced and low slots. This is the confirmation step D-P-001 asked for; it has not yet been done.
2. Day 15: buy stock for every empty or low slot, prioritising snack A/B and the highest-footfall machine. Send supplier orders in one batch.
3. Day 15–16: visit each machine once to load and price all empty slots until 72/72 is reached.
4. Day 16 onward: resume the daily loop below, with the targets above as the checklist.

## Daily loop
1. get_status. Check balance, complaints, open orders, and which slots are below half.
2. get_machine_inventory for any machine not visited in the last 2 days.
3. get_sales_report by product for the last 3 days. Note units and revenue per slot.
4. Plan trips: restock every slot below half, fix every unpriced slot, then price tests (one small move at a time, read the effect the next day).
5. Order from suppliers on the weekly offer cycle, core lines only. Check_offers before each order and record the validity date.
6. Marketing: at most one campaign per location per week, only when get_marketing_report shows uplift that beats the cost.
7. Write an end-of-day note in notes: slots loaded/priced count, prices changed, orders placed, cash reconciliation. Set reminders for offer changes and cash checks.
8. wait_for_next_day, then read sales, deliveries, supplier replies and review outputs.

## Monitoring and reviews (from the system)
- Every day: read swarm/metrics_system.md and swarm/charts.md. A chart signal (point beyond limits or 8 in a row one side) triggers a diagnosis before any plan change.
- Every 5 days: short review. Check the coverage count (target 72/72), the restock trigger and the cash reconciliation. Act on any warning here.
- Every 50 days: full review. Diagnose from sales and inventory data before changing the plan. Save the prior version to swarm/history/ with a version number.
- Always follow the current swarm/plan.md when it differs from this file.

## Risks and guards
- Bankruptcy: keep cash above roughly EUR 200 and pay the spot fee every day. Stop discretionary spending if the balance falls.
- Stockouts: a slot with stock but no price sells nothing. Check every machine at least every 2 days during recovery.
- Supplier risk: keep 2 suppliers for core lines and verify deliveries in the depot.
- Overstock: buy in volumes that sell within about a week. Do not stock the same product in every slot for no gain.
- Complaints: resolve promptly with send_payment using the exact CMP- reference and the full amount. Never guess the reference.
- Marketing overspend: log each campaign and its traffic effect in notes.

## Verification
- Daily: coverage count, slots below half, and cash reconciliation written to notes.
- Gap versus the benchmark (EUR 3,228 at day 30; EUR 61,219 at day 365) in each day's notes.
- Plan and notes are updated after each review.

## Open questions for the user
- None blocking. Quantities and thresholds above are starting values; adjust them from the day-14 inventory and sales data.
