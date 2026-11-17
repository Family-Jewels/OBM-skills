# Plan: Operate Prosus Vending Bench for 365 days (v5, revised day 113 per D-A-002)

## Context
Goal: maximise bank balance at day 365 from EUR 1,500. Unfinished or bankrupt runs score zero, so survival comes first: never let the business sit more than 10 consecutive unpaid days (spot fee EUR 12/day network-wide). Benchmark: roughly EUR 61,219 at day 365. At day 113 cash is about EUR 5,290 (day 101, A-002) and the exemplar gap is 11,869 and widening. The benchmark needs about EUR 220/day from here. cash_gain_7 is below its lower control limit (162.09 for days 106–113 against 301.05).

Why this revision: D-A-002 (day 113 diagnosis) found:
1. Cash has breached its limit. Revenue has halved: days 107–113 total 510.25, down from 1,022.75 at day 100.
2. Selling slots fell from about 14 to 7.7 on average. Revenue per unit is steady at about 2.35, so the loss is breadth of sales, not price.
3. The stockout explanation is unsupported. Troughs after the weekly full-stock rule average 23.9, against 19.9 before it. The rule has not lifted troughs.
4. The fall in selling slots fits empty slots from missed visits. This is not yet confirmed.
5. The control loop still cannot be checked: no records, notes, inventory or sales files.

v5 therefore puts a visit and coverage check first, suspends the weekly full-stock rule, changes the selling-slot count to match its target, and makes the cash reconciliation a gate before purchases.

Constraints (unchanged):
- 8-hour day. Restock 45 min, swap 30 min, price change a few minutes. Plan 6–10 machine trips per day.
- Six machines (3 locations x SNACK/DRINKS), 72 slots. Snack rows A/B hold 18, C/D hold 10. Drinks slots hold 10.
- Duplicate products share demand, so extra slots add capacity only if they are stocked and priced.
- Cash banks overnight; card takings settle a day later; open complaints hurt reputation.
- Tools: if vending tools are not available in the session, record that in the day's note, do the parts that can be checked from the workspace, and do not write as if records exist.

## Targets (hard rules)
- Visit cadence (first priority): each of the six machines is visited at least every 2 days. Record the last visit date per machine in every daily note. A machine with no visit in 2 days is the first trip of the day.
- Coverage: all 72 slots loaded and priced. An empty or unpriced slot is a defect to fix on the next trip.
- Load per slot: snack A/B at least 12 of 18; snack C/D at least 7 of 10; drinks at least 7 of 10.
- Restock on every visit: every slot at or below half capacity is refilled to full on that visit. Order quantity per product = 7 days of that slot's recent sales, rounded up.
- Weekly full stock: SUSPENDED. It has not lifted troughs. Do not run it as a standing rule. It may be re-tested once as a single controlled comparison if the day 113–120 diagnosis points to restock.
- Selling slots: count distinct slots with a sale in the rolling 7 days. This is the measure for the target and is reported daily. Target 40 of 72. Interim: 30. Below 20 for 2 days in a row triggers a slot-level check (stock, price, product, visit) the same day.
- Burst guard: if a day's revenue is below 50% of the prior 3-day average, check stock and visit date in every slot at the affected machines that day. Write the response in the note the same day.
- Price: every slot priced above cost on every visit. Price tests are on hold until coverage and visit cadence meet target, because revenue per unit is steady and the loss is in breadth.
- Cash: reconcile balance change against revenue, purchases, spot fee and marketing each day. Gap above EUR 20 is explained in notes before the next purchase.
- Pace: each daily note records the gap to the benchmark path and the 7-day cash gain, calendar basis (the same window used by revenue and cash). At the day 120 review, if the average gain is still under EUR 60/day, run a full diagnosis before the next change.

## Immediate actions (day 113–120)
1. Visit and coverage check: record the last visit date for all six machines and the count of slots loaded and priced. Save to swarm/records/coverage-d113.md if the tools are available. If not, write the gap in the note.
2. Visit all machines not visited in the last 2 days, restock every slot at or below half, and fix every unpriced slot.
3. Reconcile cash for days 106–113: revenue 510.25 against a gain of 162.09 leaves about 348 of outflow, of which the spot fee is about 84. Explain the remaining ~264 (purchases, marketing, other) in notes before the next purchase.
4. get_sales_report by slot and product, days 106–113, if available. Save to swarm/records/sales-d106-113.md. Fill any missing day from the report.
5. Write the day 113 review: visit dates, selling slots (7-day distinct count), coverage, cash reconciliation, pace, benchmark gap, and the response to each burst-guard day.
6. Decide at the day 120 review whether the visit fix restored selling slots. Only then consider a price test or the one-off restock comparison.

## Daily loop
1. get_status. Check balance, complaints, open orders, and which slots are at or below half.
2. Check last visit date per machine. Any machine not visited in 2 days is visited first.
3. get_sales_report by slot and product for the last day. Update the 7-day distinct selling-slot count and the burst guard.
4. Plan trips: restock every slot at or below half to full, fix every unpriced slot. No price tests until the Targets above are met.
5. Order from suppliers using the per-product quantities above. Check_offers before each order and record the validity date. Send one batch per supplier per day.
6. Marketing: at most one campaign per location per week, only when get_marketing_report shows uplift that beats the cost.
7. Write an end-of-day note: last visit per machine, coverage count, selling slots (7-day distinct), prices changed, orders placed, cash reconciliation, pace, benchmark gap. Set reminders for offer changes and cash checks.
8. wait_for_next_day, then read sales, deliveries, supplier replies and review outputs.

## Test (day 120)
- Compare selling slots and revenue for days 114–120 with days 100–113. If selling slots rise to 20 or more and revenue recovers with no burst-guard days, the visit gap was the main cause.
- If selling slots stay below 20 despite every machine visited within 2 days and all slots loaded, the cause is product mix or demand. Run the full diagnosis of product mix and pricing before any other change.

## Monitoring and reviews (from the system)
- Every day: read swarm/metrics_system.md and swarm/charts.md. A chart signal (point beyond limits or 8 in a row one side) triggers a diagnosis before any plan change.
- Every 5 days: short review. Check visit cadence (6/6 within 2 days), coverage (72/72), selling slots (7-day distinct count), restock trigger, and cash reconciliation. Act on any warning here.
- Day 120: pace and test review (see Targets and Test).
- Every 50 days: full review. Next: day 134. Diagnose from sales and inventory data before changing the plan. Save the prior version to swarm/history/ with a version number.
- Always follow the current swarm/plan.md when it differs from this file.

## Risks and guards
- Bankruptcy: keep cash above roughly EUR 200 and pay the spot fee every day. Stop discretionary spending if the balance falls.
- Missed visits: a machine not visited within 2 days is the main known risk. It is checked first each day.
- Stockouts: a slot with stock but no price sells nothing. Check every machine at least every 2 days.
- Overstock: order per the 7-day rule. Do not add stock beyond it.
- Supplier risk: keep 2 suppliers for core lines and verify deliveries in the depot.
- Complaints: resolve promptly with send_payment using the exact CMP- reference and the full amount. Never guess the reference.
- Marketing overspend: log each campaign and its traffic effect in notes.
- Missing records: if a day's inventory, sales or cash entry is missing, fill it on the next check and note the gap. Do not leave it blank.

## Verification
- Daily: last visit per machine, coverage count, selling-slot count, slots at or below half, burst guard response, cash reconciliation, pace and benchmark gap written to notes.
- Weekly: revenue and selling slots compared with the prior 7 days; restock quantities compared with the sales-by-slot data.
- Plan and notes are updated after each review.

## Open questions for the user
- None blocking. The 40 and 30 selling-slot targets, the day-120 pace threshold of EUR 60/day and the day 120 test thresholds are starting values. The cash_gain_7 chart definition differs from the calendar-7-day basis used here; it should be corrected so one measure is tested.
