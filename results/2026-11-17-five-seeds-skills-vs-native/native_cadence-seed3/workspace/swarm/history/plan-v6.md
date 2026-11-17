# Plan: Operate Prosus Vending Bench for 365 days (v6, revised day 158 per D-P-025)

## Context
Goal: maximise bank balance at day 365 from EUR 1,500. Unfinished or bankrupt runs score zero, so survival comes first: never let the business sit more than 10 consecutive unpaid days (spot fee EUR 12/day network-wide). Benchmark: roughly EUR 61,219 at day 365.

At day 158 cash is 7,452.65 (charts.md). The benchmark path needs (61,219 − 7,452.65) / 207 = **about EUR 260/day** from here. D-P-025 used 248/day at day 147; v6 uses the day-158 figure. Plan v5's 220/day is out of date.

Revenue since day 125 averages about 97/day and selling slots about 9.9/day, with a maximum of 20 ever logged. The 7-day cash gain averages about 277 (about 40/day) since day 125. Revenue per selling slot is about 8.65/day. Outflow is about 56/day, of which the spot fee is 12.

Why this revision: D-P-025 (day 143 review) found:
1. The business is small and has not moved. Revenue and selling slots are about the same before and after R-A-002.
2. The pace gap is growing. Targets of 40 slots and "below 20 for 2 days" do not match the logged single-day slot count, and both were set against a measure the system does not record.
3. The control loop reacted to routine variation (day 100 peak against trough). The day-120 test used the wrong measure.
4. The cash gate needs purchase and marketing records that do not exist. A gate that stops purchases stops restocking, which lowers selling slots further.
5. The "missed visits" cause is still untested.

v6 restates the measure to the logged daily count, sets interim targets from the observed range, re-baselines the pace, makes the reconciliation a record of the gap rather than a precondition for restocking, and changes the plan only on chart signals.

Constraints (unchanged):
- 8-hour day. Restock 45 min, swap 30 min, price change a few minutes. Plan 6–10 machine trips per day.
- Six machines (3 locations x SNACK/DRINKS), 72 slots. Snack rows A/B hold 18, C/D hold 10. Drinks slots hold 10.
- Duplicate products share demand, so extra slots add capacity only if they are stocked and priced.
- Cash banks overnight; card takings settle a day later; open complaints hurt reputation.
- Tools: if vending tools are not available in the session, record that in the day's note, do the parts that can be checked from the workspace, and do not write as if records exist.

## Measures (one definition each)
- Selling slots: the distinct count of slots with a sale on the day, as logged in swarm/charts.md (slots_selling). Current phase centre 9.9, limits 0.38 to 19.42. This is the measure for every target and test in this plan.
- Rolling 7-day distinct selling slots: also logged, reported as secondary only. Not used for targets or triggers.
- Revenue and cash gain: calendar days, as charted.
- Pace: benchmark path = (61,219 − cash) / days remaining, recomputed each day.

## Targets (hard rules)
- Visit cadence (first priority): each of the six machines is visited at least every 2 days. Record the last visit date per machine in every daily note. A machine with no visit in 2 days is the first trip of the day.
- Coverage: all 72 slots loaded and priced. An empty or unpriced slot is a defect to fix on the next trip.
- Load per slot: snack A/B at least 12 of 18; snack C/D at least 7 of 10; drinks at least 7 of 10.
- Restock on every visit: every slot at or below half capacity is refilled to full on that visit. Order quantity per product = 7 days of that slot's recent sales, rounded up.
- Weekly full stock: SUSPENDED. Do not run it as a standing rule.
- Selling-slot staged targets (mean of the daily count over the stated window):
  - Days 159–174 mean at least 13 (test at day 175).
  - Days 175–208 mean at least 18 (test at day 209).
  - Days 209–258 mean at least 25 (test at day 259).
  - Days 259–308 mean at least 30 (test at day 309).
  These are starting values from the observed range (about 10 now, maximum 20). Re-set them at each full review.
- Breadth arithmetic: at 8.65 revenue per selling slot per day, a gain of 260/day needs revenue of about 316/day (gain plus about 56 outflow), which is about 37 selling slots. The 25–29 estimate in D-P-025 treats gain as revenue and is too low. The day-309 target must be checked against this at the day-259 review.
- Price: every slot priced above cost on every visit. Price tests wait until coverage and visit cadence meet the day-175 target.
- Burst guard: a day's revenue below 50% of the prior 3-day average triggers a check of stock and visit date in every slot at the affected machines that day, with the response written in the note. A burst-guard day is not by itself a plan change.
- Cash reconciliation (record, not gate): each day, reconcile balance change against revenue, purchases, spot fee and marketing. Where a part cannot be recorded, write the gap and its size. Restocking and supplier orders continue regardless. The reconciliation never blocks a purchase.
- Pace review: every 10 days, compare the 10-day average gain with the benchmark path. Do not change strategy on the gap alone. Run a diagnosis if the 10-day average is below the current benchmark rate for 30 days running.

## Change rule (judging changes)
- Judge any change against the current-phase limits in swarm/charts.md, and only after at least 14 days of observation.
- One change at a time. Record the change, the day it started, and the measure it is judged on.
- Act only on a chart signal: a point beyond limits or 8 in a row on one side of the centre. A single high or low point is routine variation.
- The cash_gain_7 "shift down" in charts.md compares post-day-125 values with a pre-day-125 centre that the day 90–101 peak likely inflates. Do not act on it until the centre is re-baselined at the day-175 review.

## Immediate actions (day 158–175)
1. Visit and coverage check: record the last visit date for all six machines and the count of slots loaded and priced. Save to swarm/records/coverage-d158.md if tools are available, otherwise write the gap in the note.
2. Visit all machines not visited in the last 2 days, restock every slot at or below half, and fix every unpriced slot.
3. Record purchases, supplier deliveries and marketing spend per day in swarm/records/ if tools are available. Until then, mark them as unrecorded in the note.
4. Explain the unexplained outflow for days 131–138 (about 252, P-024, roughly 36/day). Test whether it is purchases. Do not treat it as a leak until shown.
5. Write the day-158 review: visit dates, selling slots, coverage, cash reconciliation, pace, benchmark gap against 260/day, and the response to each burst-guard day.
6. At day 175, run the first breadth test (see Test).

## Daily loop
1. get_status. Check balance, complaints, open orders, and which slots are at or below half.
2. Check last visit date per machine. Any machine not visited in 2 days is visited first.
3. get_sales_report by slot and product for the last day. Record the daily selling-slot count and the burst guard.
4. Plan trips: restock every slot at or below half to full, fix every unpriced slot. No price tests until the Targets above are met.
5. Order from suppliers using the per-product quantities above. Check_offers before each order and record the validity date. Send one batch per supplier per day. Orders are never held for the cash reconciliation.
6. Marketing: at most one campaign per location per week, only when get_marketing_report shows uplift that beats the cost. Log spend and traffic effect.
7. Write an end-of-day note: last visit per machine, coverage count, selling slots (daily and 7-day distinct), prices changed, orders placed, cash reconciliation (with any unrecorded gap stated), pace, benchmark gap. Set reminders for offer changes and cash checks.
8. wait_for_next_day, then read sales, deliveries, supplier replies and review outputs.

## Test (day 175)
- Compare the daily selling-slot mean for days 159–174 with the current-phase centre of 9.9.
- If the mean is at least 13 and every machine was visited within 2 days, breadth is rising. Continue the plan.
- If the mean is below 11 with full visit cadence and coverage, product mix or demand is the cause. Run the full diagnosis of product mix and pricing before any other change. Price tests may then be considered.
- If the mean is between 11 and 13, hold the plan for 14 more days and re-run this test.

## Monitoring and reviews (from the system)
- Every day: read swarm/metrics_system.md and swarm/charts.md. A chart signal triggers a diagnosis before any plan change.
- Every 5 days: short review. Check visit cadence (6/6 within 2 days), coverage (72/72), selling slots (daily mean), restock trigger, and whether cash gaps are written down. Act on any warning here.
- Every 10 days: pace review (see Targets).
- Day 175: breadth test (see Test).
- Every 50 days: full review. Next: day 208. Diagnose from sales and inventory data before changing the plan. Save the prior version to swarm/history/ with a version number.
- Always follow the current swarm/plan.md when it differs from this file.

## Risks and guards
- Bankruptcy: keep cash above roughly EUR 200 and pay the spot fee every day. Stop discretionary spending if the balance falls. This is the only guard that stops purchases.
- Missed visits: a machine not visited within 2 days is the main known risk. It is checked first each day.
- Stockouts: a slot with stock but no price sells nothing. Check every machine at least every 2 days.
- Overstock: order per the 7-day rule. Do not add stock beyond it.
- Supplier risk: keep 2 suppliers for core lines and verify deliveries in the depot.
- Complaints: resolve promptly with send_payment using the exact CMP- reference and the full amount. Never guess the reference.
- Marketing overspend: log each campaign and its traffic effect in notes.
- Missing records: if a day's inventory, sales, purchase or cash entry is missing, write the gap and its size in the note. Do not leave it blank, and do not stop restocking because of it.

## Verification
- Daily: last visit per machine, coverage count, daily selling-slot count, slots at or below half, burst guard response, cash reconciliation (with unrecorded parts stated), pace and benchmark gap written to notes.
- Weekly: revenue and selling slots compared with the prior 7 days; restock quantities compared with the sales-by-slot data.
- Plan and notes are updated after each review.

## Open questions for the user
- None blocking. The staged selling-slot targets, the 14-day change window and the day-175 test thresholds are starting values. The cash_gain_7 centre needs re-baselining (see Change rule). The breadth arithmetic (about 37 slots for 260/day) should be confirmed at the day-259 review.
