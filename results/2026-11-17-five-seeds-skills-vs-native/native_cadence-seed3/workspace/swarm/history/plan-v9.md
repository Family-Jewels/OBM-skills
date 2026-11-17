# Plan: Operate Prosus Vending Bench for 365 days (v9, revised day 286 per D-A-005)

## Context
Goal: maximise bank balance at day 365 from EUR 1,500. Unfinished or bankrupt runs score zero, so survival comes first: never let the business sit more than 10 consecutive unpaid days (spot fee EUR 12/day network-wide).

At day 286 cash is 12,015.23 (charts.md). Cash gain over the last 13 days is about 41/day. The exemplar is at 47,543.51 (PIP 4.4). The benchmark is a reference only (see Targets).

Why this revision: D-A-005 (day 273 diagnosis) found:
1. Selling breadth has collapsed. Selling slots averaged 13.4 before the redesign and 8.27 per day since day 244 (−38%). Every point since day 244 is below the 13.4 centre. This explains most of the revenue fall (95.44 → 78.87).
2. v8 made revenue per selling slot the primary measure. It rose (7.12 → 9.14), so v8 hid the breadth drop. The day-252 re-test on that measure failed (9.15 against 9.5).
3. The cause of the breadth loss is not known. The per-slot records planned for day 238 were never created, so unpriced slots, empty slots, visit gaps and the 7-day order rule cannot be checked. The cause test due day 245 was not done.
4. Cash does not reconcile. Days 261–273 leave about 36/day unrecorded, probably purchases. v8 had no purchases line.
5. The chart label "beyond the lower limit" on slots_selling is wrong. 8.27 is above 6.82. The valid signal is the run of points below the 13.4 centre.

## Measures (one definition each)
- **Selling slots** (slots_selling): distinct slots with a sale on the day. **Primary measure from this version.** Judging centre **13.4** (limits 6.82 to 19.98), from the "since redesign" table in charts.md. Do not judge against the top-table centre (8.55), which re-centres on the new low level.
- **Revenue** (calendar days): outcome measure. Judging centre **95.44** (limits −24.82 to 215.7), from the "since redesign" table.
- **Revenue per selling slot**: diagnostic only. Not a success measure.
- Cash gain: reported, not judged on its own.
- Pace: benchmark path = (61,219 − cash) / days remaining. Reference only.
- Centres and limits are read from charts.md each day. Record conflicts (redesign day 238 vs 244, phase 209 vs 244) are settled by charts.md.

## Targets (hard rules)
- Breadth target: 14-day mean of selling slots at or above **13.4** (pre-redesign centre). Interim check day 300; decision day 315.
- Visit cadence: each of the six machines visited at least every 2 days. Last visit date per machine in every daily note. A machine not visited in 2 days is the first trip of the day.
- Coverage: all 72 slots loaded and priced. Empty or unpriced slots are fixed on the next trip.
- Restock on every visit: every slot at or below half is refilled to full. Order quantity per product = 7 days of that slot's recent sales, rounded up.
- Per-slot log (started day 286, required): each day, for all 72 slots, record stock on the last visit, price, sales, and last visit date. Name every slot that sold nothing, or is at or below half. A missing day is written as a gap with its size. The log is not a gate for restocking.
- Price: every slot priced above cost on every visit. Fixing an unpriced slot is always allowed. No other price or product-mix change until the breadth cause test is written.
- Burst guard: a day's revenue below 50% of the prior 3-day average triggers a check of stock, price and visit date per slot at the affected machines, written in the note. Zero-sale days (29, 114, 133, 154, and any new one) get the same written response. Neither is by itself a plan change.
- Breadth alarm: if selling slots are below 8 on two consecutive days, check every machine's visit date and every slot's stock and price that day, and write the result.
- Cash reconciliation (record, not gate): each day, reconcile balance change against revenue, purchases, spot fee and marketing. Write any unrecorded part and its size. Orders continue regardless.
- Pace review: every 10 days. Do not change strategy on the gap alone.

## Breadth cause test (days 244–286)
Write swarm/records/breadth-d244-286.md by day 295, using the per-slot log where it exists and sales and order records for the rest. For each day 244–286:
1. Price: slots unpriced or priced at or below cost, per visit.
2. Stock: slots at or below half, or empty, on the day of sale; days between visits per machine.
3. Order rule: whether 7-day order quantities ran out before the next delivery.
4. Demand: selling slots by machine and by product line, and any marketing active.

Read the result as follows:
- Unpriced or empty slots explain most of the 13.4 → 8.27 drop: fix and restock on every visit first. This is already required and needs no further test.
- Visit gaps or long intervals: visit cadence is the change to test.
- No clear pattern: demand. Test marketing at one location only.
Record the conclusion and the chosen change in the same file. If the test cannot be written from records, write which records are missing and the day they started.

## Change rule (judging changes)
- Judge any change on selling slots against the centre 13.4 and limits above, after at least 14 days of observation. Revenue is the outcome check.
- One change at a time. Record the change, the day it started, and the measure it is judged on.
- Act on a chart signal: a point beyond limits or 8 in a row on one side of the centre. The run below 13.4 since day 244 is already a signal. Do not wait for more data before acting on the cause test's result.
- Fixes for unpriced slots, empty slots and missed visits do not need the cause test.
- Do not reverse R-P-036 or R-P-025 or R-P-030 without a cause-test result.

## Immediate actions (day 286)
1. Create swarm/records/ and start the per-slot log today. Back-fill days 261–285 where the data exists.
2. Visit all six machines. Restock every slot at or below half. Fix every unpriced slot. Record the count (72/72 target).
3. Add a purchases line to the cash reconciliation. Back-fill purchases for days 261–286 from order records and write the residual.
4. Start the breadth cause test: write swarm/records/breadth-d244-286.md by day 295.
5. Set the judging dates: interim day 300, decision day 315 (selling slots against 13.4).

## Daily loop
1. get_status. Check balance, complaints, open orders, and slots at or below half.
2. Check last visit date per machine. Any machine not visited in 2 days is visited first.
3. get_sales_report by slot and product for the last day. Record selling-slot count (against 13.4), revenue, burst guard, zero-sale machines, breadth alarm, and the per-slot log.
4. Plan trips: restock every slot at or below half to full, fix every unpriced slot.
5. Order from suppliers using the per-product quantities above. Check_offers before each order and record the validity date. One batch per supplier per day. Orders are never held for the cash reconciliation.
6. Marketing: at most one campaign per location per week, only when get_marketing_report shows uplift that beats the cost. Log spend and traffic effect.
7. Write the end-of-day note to swarm/records/: last visit per machine, coverage count, selling slots, revenue, per-slot log status, prices changed, orders placed, cash reconciliation (purchases, spot fee, marketing, unrecorded gap), pace, benchmark gap.
8. wait_for_next_day, then read sales, deliveries, supplier replies and review outputs.

## Monitoring and reviews
- Every day: read swarm/metrics_system.md and swarm/charts.md. A chart signal triggers a diagnosis before any plan change.
- Every 5 days: check visit cadence (6/6 within 2 days), coverage (72/72), restock trigger, per-slot log complete, cash gaps written down.
- Every 10 days: pace review.
- Day 295: breadth cause test written.
- Day 300: interim breadth check against 13.4.
- Day 315: breadth decision and next change, if any.
- Day 330 and onward: review each 14 days in the same form.
- Always follow the current swarm/plan.md when it differs from this file.

## Risks and guards
- Bankruptcy: keep cash above roughly EUR 200 and pay the spot fee every day. Stop discretionary spending if the balance falls. This is the only guard that stops purchases.
- Missed visits: a machine not visited within 2 days is the main known risk. It is checked first each day.
- Stockouts: a slot with stock but no price sells nothing. Check every machine at least every 2 days.
- Overstock: order per the 7-day rule. Do not add stock beyond it.
- Supplier risk: keep 2 suppliers for core lines and verify deliveries in the depot.
- Complaints: resolve promptly with send_payment using the exact CMP- reference and the full amount. Never guess the reference.
- Marketing overspend: log each campaign and its traffic effect.
- Missing records: write the gap and its size in the note. Do not stop restocking because of it.

## Open questions for the user
- None blocking. The 13.4 breadth target and the day 300 and 315 dates are starting values. The benchmark stays a reference only unless the user says otherwise.
