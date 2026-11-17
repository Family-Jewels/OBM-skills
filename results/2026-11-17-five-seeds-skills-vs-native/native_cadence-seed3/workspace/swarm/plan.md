# Plan: Operate Prosus Vending Bench for 365 days (v10, revised day 332 per D-P-044)

## Context
Goal: maximise bank balance at day 365 from EUR 1,500. Unfinished or bankrupt runs score zero, so survival comes first: never let the business sit more than 10 consecutive unpaid days (spot fee EUR 12/day network-wide).

At day 332 cash is 12,770.09 (charts.md). The exemplar is at 55,506.45 (PIP 4.8). The benchmark is a reference only. 33 days remain.

Why this revision: D-P-044 (day 322 diagnosis) found:
1. Breadth has collapsed since redesign R-A-005 (day 295). Selling slots average 6.03 against a before-centre of 8.55. Breadth explains the revenue fall (56.68 against 80.39).
2. The chart is under-reporting it. Days 297–316 are 20 consecutive points below 8.55. The "8 in a row" signal is met and was labelled "no shift yet".
3. v9 judged slots against 13.4, which does not appear in charts.md. The 14-day target was unreachable (about 6 a day).
4. The v9 diagnostic steps were not carried out. swarm/records/ does not exist. The cause of the breadth loss is unknown.
5. The day-315 decision passed with no record. Recorded as missed.

## Measures (one definition each)
- **Selling slots** (slots_selling): distinct slots with a sale on the day. **Primary measure.** Judging centre **8.55** (limits 3.09 to 14.01), from the "before" column of the "since redesign" table in charts.md. The 13.4 centre is withdrawn.
- **Revenue** (calendar days): outcome measure. Judging centre **80.39** (limits −32.03 to 192.81), same table.
- **Revenue per selling slot**: diagnostic only. Not a success measure.
- Cash gain: reported, not judged on its own.
- Pace: benchmark path = (61,219 − cash) / days remaining. Reference only.
- Centres and limits are read from charts.md each day. If charts.md changes, charts.md wins.

## Targets (hard rules)
- Breadth target: 14-day mean of selling slots at or above **8.55**. Interim check day 340; decision day 350.
- Active signal: the run below 8.55 since day 297 is an active signal now. Act on the fixes below without waiting for the cause test.
- Records first: create swarm/records/ today and start the per-slot log. No further strategy change (price, product mix, order rule, marketing, visit pattern) until the per-slot log exists for at least 3 days and the cause test is written.
- Visit cadence: each of the six machines visited at least every 2 days. Last visit date per machine in every daily note. A machine not visited in 2 days is the first trip of the day.
- Coverage: all 72 slots loaded and priced. Empty or unpriced slots are fixed on the next trip.
- Restock on every visit: every slot at or below half is refilled to full. Order quantity per product = 7 days of that slot's recent sales, rounded up.
- Per-slot log (required, from day 332): each day, for all 72 slots, record stock on the last visit, price, sales, and last visit date. Name every slot that sold nothing, or is at or below half. A missing day is written as a gap with its size. The log is not a gate for restocking.
- Price: every slot priced above cost on every visit. Fixing an unpriced slot is always allowed.
- Burst guard: a day's revenue below 50% of the prior 3-day average triggers a check of stock, price and visit date per slot at the affected machines, written in the note. Zero-sale days get the same written response. Neither is by itself a plan change.
- Breadth alarm: if selling slots are below 8 on two consecutive days, check every machine's visit date and every slot's stock and price that day, and write the result.
- Cash reconciliation (record, not gate): each day, reconcile balance change against revenue, purchases, spot fee and marketing. Write any unrecorded part and its size. Orders continue regardless.
- Pace review: every 10 days. Do not change strategy on the gap alone.

## Breadth cause test (days 297–332)
Write swarm/records/breadth-d297-332.md by day 338, from the per-slot log and sales and order records. Where a record is missing, write which one and the day it started. For each day:
1. Price: slots unpriced or priced at or below cost, per visit.
2. Stock: slots at or below half, or empty, on the day of sale; days between visits per machine.
3. Order rule: whether 7-day order quantities ran out before the next delivery.
4. Demand: selling slots by machine and product line, and any marketing active.

Read the result as follows:
- Unpriced or empty slots or visit gaps explain the drop: the fixes below are the change. Judge them on selling slots.
- No clear pattern: demand. Test marketing at one location only, for at least 14 days.
Record the conclusion and the chosen change in the same file.

## Immediate actions (day 332)
1. Create swarm/records/ and start the per-slot log today.
2. Visit all six machines. Restock every slot at or below half. Fix every unpriced slot. Record the count (72/72 target).
3. Add a purchases line to the cash reconciliation. Back-fill from order records where possible and write the residual.
4. Record that the day-315 decision was missed (see R-P-044).
5. Set the judging dates: cause test day 338, interim check day 340, decision day 350 (selling slots against 8.55).

## Change rule (judging changes)
- Judge any change on selling slots against 8.55 and its limits, after at least 14 days of observation. Revenue is the outcome check.
- One change at a time. Record the change, the day it started, and the measure it is judged on.
- Fixes for unpriced slots, empty slots and missed visits do not need the cause test.
- Do not reverse R-P-036, R-P-025 or R-P-030 without a cause-test result.
- With 33 days left, a change started after day 350 cannot be judged. Changes after day 350 are limited to fixes.

## Daily loop
1. get_status. Check balance, complaints, open orders, and slots at or below half.
2. Check last visit date per machine. Any machine not visited in 2 days is visited first.
3. get_sales_report by slot and product for the last day. Record selling-slot count (against 8.55), revenue, burst guard, zero-sale machines, breadth alarm, and the per-slot log.
4. Plan trips: restock every slot at or below half to full, fix every unpriced slot.
5. Order from suppliers using the per-product quantities above. Check_offers before each order and record the validity date. One batch per supplier per day. Orders are never held for the cash reconciliation.
6. Marketing: at most one campaign per location per week, only when get_marketing_report shows uplift that beats the cost. Log spend and traffic effect.
7. Write the end-of-day note to swarm/records/: last visit per machine, coverage count, selling slots, revenue, per-slot log status, prices changed, orders placed, cash reconciliation (purchases, spot fee, marketing, unrecorded gap), pace, benchmark gap.
8. wait_for_next_day, then read sales, deliveries, supplier replies and review outputs.

## Monitoring and reviews
- Every day: read swarm/metrics_system.md and swarm/charts.md. A chart signal triggers a diagnosis before any plan change.
- Every 5 days: check visit cadence (6/6 within 2 days), coverage (72/72), restock trigger, per-slot log complete, cash gaps written down.
- Every 10 days: pace review.
- Day 338: breadth cause test written.
- Day 340: interim breadth check against 8.55.
- Day 350: breadth decision and last change, if any.
- Day 360: final review of the run and closing cash record.
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
- None blocking. The 8.55 breadth centre and the day 338, 340 and 350 dates are working values from charts.md and the calendar. The benchmark stays a reference only unless the user says otherwise.
