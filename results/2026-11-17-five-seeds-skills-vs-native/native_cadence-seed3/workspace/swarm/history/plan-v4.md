# Plan: Operate Prosus Vending Bench for 365 days (v4, revised day 84 per D-P-011)

## Context
Goal: maximise bank balance at day 365 from EUR 1,500. Unfinished or bankrupt runs score zero, so survival comes first: never let the business sit more than 10 consecutive unpaid days (spot fee EUR 12/day network-wide). Benchmark: roughly EUR 3,228 at day 30 and EUR 61,219 at day 365. At day 84 cash is EUR 4,135.65 against an exemplar of 12,575.8 (PIP 4.2, charts.md). Pace since day 47 is about EUR 43/day; the benchmark needs about EUR 192/day. At the current pace the benchmark will not be reached, so this plan aims to raise pace rather than assume the benchmark.

Why this revision: D-P-011 (day 68 diagnosis, checked against charts at day 84) found:
1. Cash is far behind the benchmark path, and the gap is widening.
2. Sales follow a roughly 7-day cycle. Troughs fell on days 7, 21, 28, 42, 49, 56 and 63, with peaks 2–5 days later. The likely cause is stockouts tied to a weekly restock or demand cycle; records would separate the two.
3. Selling slots average about 10 of 72. The 20-slot floor is too low; the benchmark needs about 40.
4. The control loop is unverifiable: no records, notes or full review. The day 50 review never ran.

v4 sets a 40-slot target, times full restocks to the weekly cycle, adds a test that separates restock from demand, requires the records, and holds the full review now.

Constraints (unchanged):
- 8-hour day. Restock 45 min, swap 30 min, price change a few minutes. Plan 6–10 machine trips per day.
- Six machines (3 locations x SNACK/DRINKS), 72 slots. Snack rows A/B hold 18, C/D hold 10. Drinks slots hold 10.
- Duplicate products share demand, so extra slots add capacity only if they are stocked and priced.
- Cash banks overnight; card takings settle a day later; open complaints hurt reputation.

## Targets (hard rules)
- Coverage: all 72 slots loaded and priced. An empty or unpriced slot is a defect to fix on the next trip.
- Load per slot: snack A/B at least 12 of 18; snack C/D at least 7 of 10; drinks at least 7 of 10.
- Restock on every visit: every slot at or below half capacity is refilled to full on that visit. Order quantity per product = 7 days of that slot's recent sales (from the sales-by-slot log), rounded up.
- Weekly full stock: on the day before each predicted trough, all six machines are visited and every slot is filled to full, including slots above half. Predicted troughs follow the 7-day cycle from day 63: days 70, 77, 84, 91, 98. Confirm each against sales; if a trough does not appear, record it and re-time the cycle.
- Visit cadence: each of the six machines is visited at least every 2 days.
- Selling slots: target 40 of 72 slots with a sale in a rolling 7-day window. Interim: 30 by day 110. Below 30 for 3 days in a row triggers a slot-level check (stock, price, product) the same day.
- Burst guard: if a day's revenue is below 50% of the prior 3-day average, check stock in every slot at the affected machines that day, not at the next review.
- Price: every slot priced above cost on every visit. Record price changes in notes. One price change per product per week, read the effect the next day.
- Cash: reconcile balance change against sales, purchases, spot fee and marketing each day. Gap above EUR 20 is explained in notes before the next purchase.
- Pace: each daily note records the gap to the benchmark path and the 7-day average cash gain. At the day 120 review, if the average gain is still under EUR 60/day, run a full diagnosis of product mix and pricing before the next change.

## Immediate actions (day 84–90)
1. Run the full review now (day 50 review was never run). Save it to swarm/audits/ with the D-P-011 test results.
2. get_machine_inventory on all six machines. Save to swarm/records/inventory-d84.md.
3. get_sales_report by slot and product, days 31–84. Save to swarm/records/sales-d31-84.md. Fill missing days 31, 40, 44, 61 and 70 from the report. Record whether day 70 revenue was under 50 (the D-P-011 test).
4. Restock every slot at or below half, fix every unpriced slot, and check stock and price in every slot.
5. On the day-90 trips, fill all 72 slots to full (weekly full stock rule, trough on day 91).
6. Write the first daily note: coverage count, selling slot count, revenue, cash reconciliation, pace, benchmark gap.

## Daily loop
1. get_status. Check balance, complaints, open orders, and which slots are at or below half.
2. get_machine_inventory for any machine not visited in the last 2 days.
3. get_sales_report by slot and product for the last day. Update the 7-day selling-slot count and the burst guard.
4. Plan trips: restock every slot at or below half to full, fix every unpriced slot, then at most one price test. On the day before a predicted trough, fill all slots to full.
5. Order from suppliers using the per-product quantities above. Check_offers before each order and record the validity date. Send one batch per supplier per day.
6. Marketing: at most one campaign per location per week, only when get_marketing_report shows uplift that beats the cost.
7. Write an end-of-day note: slots loaded/priced count, selling slots, prices changed, orders placed, cash reconciliation, pace, benchmark gap. Set reminders for offer changes and cash checks.
8. wait_for_next_day, then read sales, deliveries, supplier replies and review outputs.

## Test (day 91)
- Stock was full on all slots on day 90. If day 91 revenue is under 50, stockouts are not the main cause; the next change targets demand (product mix and prices across the weekly cycle).
- If day 91 revenue is 50 or more, the weekly restock cycle is supported; keep the weekly full stock rule and move the next change to the 40-slot target.
- Record the result in notes and in the next review.

## Monitoring and reviews (from the system)
- Every day: read swarm/metrics_system.md and swarm/charts.md. A chart signal (point beyond limits or 8 in a row one side) triggers a diagnosis before any plan change.
- Every 5 days: short review. Check coverage (72/72), selling slots (30+ interim, 40 target), weekly full stock, restock trigger, and cash reconciliation. Act on any warning here.
- Day 120: pace review (see Targets).
- Every 50 days: full review. Next: day 134. Diagnose from sales and inventory data before changing the plan. Save the prior version to swarm/history/ with a version number.
- Always follow the current swarm/plan.md when it differs from this file.

## Risks and guards
- Bankruptcy: keep cash above roughly EUR 200 and pay the spot fee every day. Stop discretionary spending if the balance falls.
- Stockouts: a slot with stock but no price sells nothing. Check every machine at least every 2 days.
- Overstock: the weekly full stock rule adds stock. Order per the 7-day rule and do not stock the same product in every slot for no gain.
- Supplier risk: keep 2 suppliers for core lines and verify deliveries in the depot.
- Complaints: resolve promptly with send_payment using the exact CMP- reference and the full amount. Never guess the reference.
- Marketing overspend: log each campaign and its traffic effect in notes.
- Missing records: if a day's inventory, sales or cash entry is missing, fill it on the next check and note the gap. Do not leave it blank.

## Verification
- Daily: coverage count, selling-slot count, slots at or below half, burst guard, cash reconciliation, pace and benchmark gap written to notes.
- Weekly: trough-day revenue compared with the full-stock days; restock quantities compared with the sales-by-slot data.
- Plan and notes are updated after each review.

## Open questions for the user
- None blocking. The 30/40 selling-slot targets, the day-120 pace threshold of EUR 60/day and the weekly trough timing are starting values; adjust them from the day 91 test and the day 84–120 data.
