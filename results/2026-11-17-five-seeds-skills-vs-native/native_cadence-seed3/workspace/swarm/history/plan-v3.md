# Plan: Operate Prosus Vending Bench for 365 days (v3, revised day 43 per D-P-007)

## Context
Goal: maximise bank balance at day 365 from EUR 1,500. Unfinished or bankrupt runs score zero, so survival comes first: never let the business sit more than 10 consecutive unpaid days (spot fee EUR 12/day network-wide). Benchmark: roughly EUR 3,228 at day 30 and EUR 61,219 at day 365. At day 43 cash is about EUR 2,532 against an exemplar of 5,478 (charts.md).

Why this revision: D-P-007 (day 38) found three problems.
1. Cash growth is about EUR 34/day since day 16. Reaching 61,219 needs about EUR 181/day from day 43, so the current rate would end near EUR 13,000.
2. Sales come in bursts. Revenue often fell to near zero within 5 days, and selling slots peaked at 20 of 72.
3. The control loop cannot be checked. No inventory, sales or purchase records are kept in swarm/, and day 31 revenue is missing.

The best-supported cause is batched restocking that reaches few slots, so stock runs out within days. v3 makes restocking continuous and per slot, requires the records D-P-007 asked for, and adds a same-day response to revenue drops.

Constraints (unchanged):
- 8-hour day. Restock 45 min, swap 30 min, price change a few minutes. Plan 6–10 machine trips per day.
- Six machines (3 locations x SNACK/DRINKS), 72 slots. Snack rows A/B hold 18, C/D hold 10. Drinks slots hold 10.
- Duplicate products share demand, so extra slots add capacity only if they are stocked and priced.
- Cash banks overnight; card takings settle a day later; open complaints hurt reputation.

## Targets (hard rules)
- Coverage: all 72 slots loaded and priced. An empty or unpriced slot is a defect to fix on the next trip.
- Load per slot: snack A/B at least 12 of 18; snack C/D at least 7 of 10; drinks at least 7 of 10.
- Restock on every visit: every slot at or below half capacity is refilled to full on that visit, not held for a batch. Order quantity per product = 7 days of that slot's recent sales (from the sales-by-slot log), rounded up.
- Visit cadence: each of the six machines is visited at least every 2 days. A machine not visited in 2 days is the first trip of the day.
- Selling slots: at least 20 of 72 slots record a sale on each day in a rolling 7-day window. Below 20 for 3 days in a row triggers a slot-level check (stock, price, product) the same day.
- Burst guard: if a day's revenue is below 50% of the prior 3-day average, check stock in every slot at the affected machines that day, not at the next review.
- Price: every slot priced above cost on every visit. Record price changes in notes. One price change per product per week, read the effect the next day.
- Cash: reconcile balance change against sales, purchases, spot fee and marketing each day. Gap above EUR 20 is explained in notes before the next purchase.
- Benchmark gap: each day's notes record the gap to the benchmark path (EUR 3,228 at day 30; EUR 61,219 at day 365). If the gap is still widening at the day 50 review, the full review is run at that point with the sales and inventory data.

## Immediate actions (day 43–44)
1. get_machine_inventory on all six machines. Save the result to swarm/records/inventory-d43.md.
2. get_sales_report by slot and product for days 31–43. Save to swarm/records/sales-d31-43.md. Note the missing day 31 revenue explicitly, and look it up from the sales report.
3. Restock every slot at or below half, on the trips planned from step 1, following the Restock on every visit rule.
4. Write the first daily record in notes: coverage count, selling slot count, revenue, cash reconciliation, benchmark gap.

## Daily loop
1. get_status. Check balance, complaints, open orders, and which slots are at or below half.
2. get_machine_inventory for any machine not visited in the last 2 days.
3. get_sales_report by slot and product for the last day. Update the 7-day selling-slot count and the burst guard.
4. Plan trips: restock every slot at or below half to full, fix every unpriced slot, then at most one price test.
5. Order from suppliers using the per-product quantities above. Check_offers before each order and record the validity date. Send one batch per supplier per day.
6. Marketing: at most one campaign per location per week, only when get_marketing_report shows uplift that beats the cost.
7. Write an end-of-day note: slots loaded/priced count, selling slots, prices changed, orders placed, cash reconciliation, benchmark gap. Set reminders for offer changes and cash checks.
8. wait_for_next_day, then read sales, deliveries, supplier replies and review outputs.

## Monitoring and reviews (from the system)
- Every day: read swarm/metrics_system.md and swarm/charts.md. A chart signal (point beyond limits or 8 in a row one side) triggers a diagnosis before any plan change.
- Every 5 days: short review. Check coverage (72/72), selling slots (20+), restock trigger, and cash reconciliation. Act on any warning here.
- Every 50 days: full review. Diagnose from sales and inventory data before changing the plan. Save the prior version to swarm/history/ with a version number. Next: day 50 review, or sooner per the benchmark-gap rule.
- Always follow the current swarm/plan.md when it differs from this file.

## Risks and guards
- Bankruptcy: keep cash above roughly EUR 200 and pay the spot fee every day. Stop discretionary spending if the balance falls.
- Stockouts: a slot with stock but no price sells nothing. Check every machine at least every 2 days.
- Supplier risk: keep 2 suppliers for core lines and verify deliveries in the depot.
- Overstock: order per the 7-day rule. Do not stock the same product in every slot for no gain.
- Complaints: resolve promptly with send_payment using the exact CMP- reference and the full amount. Never guess the reference.
- Marketing overspend: log each campaign and its traffic effect in notes.
- Missing records: if a day's inventory, sales or cash entry is missing, fill it on the next check and note the gap. Do not leave it blank.

## Verification
- Daily: coverage count, selling-slot count, slots at or below half, burst guard, cash reconciliation and benchmark gap written to notes.
- Weekly: restock quantities compared with the sales-by-slot data; adjust the 7-day rule if stock still runs out within 3 days.
- Plan and notes are updated after each review.

## Open questions for the user
- None blocking. The 20-slot selling floor, 2-day visit cadence and 50% burst threshold are starting values; adjust them from the day 43–50 data.
