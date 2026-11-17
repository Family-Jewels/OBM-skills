# Plan: Operate Prosus Vending Bench for 365 days (v8, revised day 238 per D-P-036)

## Context
Goal: maximise bank balance at day 365 from EUR 1,500. Unfinished or bankrupt runs score zero, so survival comes first: never let the business sit more than 10 consecutive unpaid days (spot fee EUR 12/day network-wide).

At day 238 cash is 10,187.47 (charts.md). Cash gained 1,194 since day 198 (about 36/day). The benchmark (about EUR 61,219 at day 365) needs about EUR 314/day from here. The exemplar is at 39,234 (PIP 4.3). The benchmark is a reference only (see Targets).

Why this revision: D-P-036 (day 231 diagnosis) found:
1. Revenue is falling while breadth holds. Last-7 revenue fell from 842 (day 221) to 542 (day 231). Revenue per selling slot fell from 9.5 (day 221) to 2.7–8.8 since day 224. No measure in v7 watched it.
2. The judging centre was stale. v7 cited 7.5 (pre-R-P-030 "before" value). The current centre is in charts.md's top table.
3. The v7 records were never created, so visits, coverage and cash could not be checked. The day-223 test was void and was not re-run.
4. Days 219–225 leave about 318 of cash unrecorded.
5. The cause of the revenue fall is not determined. Candidates: stock depth per slot, pricing, demand.

## Measures (one definition each)
- **Selling slots** (slots_selling): distinct slots with a sale on the day. Current-phase centre **13.4** (limits 6.82 to 19.98), phase since day 209, from the top table of charts.md.
- **Revenue per selling slot** (revenue_per_slot): **primary measure from this version.** Current-phase centre **7.12** (limits −0.17 to 14.41), phase since day 209.
- Revenue and cash gain: calendar days, as charted. Revenue centre 95.44 (phase since day 209).
- Centres and limits are read from charts.md each day. The "before" table and the 7.5 and 9.9 values in earlier plans are reference only.
- Pace: benchmark path = (61,219 − cash) / days remaining. Reference only.

## Targets (hard rules)
- Visit cadence: each of the six machines visited at least every 2 days. Last visit date per machine in every daily note. A machine not visited in 2 days is the first trip of the day.
- Coverage: all 72 slots loaded and priced. Empty or unpriced slots are fixed on the next trip.
- Restock on every visit: every slot at or below half is refilled to full. Order quantity per product = 7 days of that slot's recent sales, rounded up.
- Per-slot logging (new): each day, record for every selling slot its stock on the last visit, its price, and its sales. Any slot that sold nothing, or is at or below half, is named in the note.
- Revenue per selling slot target: 14-day mean at or above 9.5 (the day-221 level). Judged at day 252.
- Selling-slot target: daily mean at or above 11 is maintained. Breadth is no longer the open question, since slots_selling is in routine variation.
- Price: every slot priced above cost on every visit. **No price or product-mix changes until the cause test below is done**, except to fix an unpriced slot.
- Burst guard: a day's revenue below 50% of the prior 3-day average triggers a check of stock, price and visit date per slot at the affected machines, written in the note. Zero-sale days (29, 114, 133, 154, and any new one) get the same written response. Neither is by itself a plan change.
- Cash reconciliation (record, not gate): each day, reconcile balance change against revenue, purchases, spot fee and marketing. Write any unrecorded part and its size. Orders continue regardless.
- Pace review: every 10 days. Do not change strategy on the gap alone.

## Cause test (days 221–231 revenue drop)
Write swarm/records/revenue-slot-d221-231.md with, for each day 221–231:
1. Stock: selling slots that were at or below half, or empty, on the day of sale.
2. Price: price per slot against cost and against the same product at other machines.
3. Demand: revenue per selling slot by location and by product line, and any marketing active.

Read the result as follows:
- Mostly stock-depth: restock frequency and the 7-day order rule are the change to test.
- Mostly price: price test on one product line at a time, per the change rule.
- No clear pattern with stock and price in order: demand. Test marketing at one location only.
Record the conclusion and the chosen change by day 245.

## Change rule (judging changes)
- Judge any change on revenue_per_slot against the centre 7.12 and limits above, and only after at least 14 days of observation.
- One change at a time. Record the change, the day it started, and the measure it is judged on.
- Act only on a chart signal: a point beyond limits or 8 in a row on one side of the centre. A single high or low point is routine variation.
- Do not reverse R-P-025 or R-P-030 on their own.

## Immediate actions (day 238)
1. Create swarm/records/ and begin the per-slot log (see Targets). Back-fill days 221–231 wherever the data exists.
2. Visit all six machines. Restock every slot at or below half. Fix every unpriced slot. Record the count (72/72 target).
3. Write the cause test (see above) to swarm/records/revenue-slot-d221-231.md.
4. Reconcile days 219–225: about 318 is unrecorded. Check whether it is purchases, and write the amount and source.
5. Set the re-test date: day 252 (14 days). Judge revenue_per_slot then.

## Daily loop
1. get_status. Check balance, complaints, open orders, and slots at or below half.
2. Check last visit date per machine. Any machine not visited in 2 days is visited first.
3. get_sales_report by slot and product for the last day. Record selling-slot count, revenue per selling slot, burst guard, zero-sale machines, and the per-slot log.
4. Plan trips: restock every slot at or below half to full, fix every unpriced slot.
5. Order from suppliers using the per-product quantities above. Check_offers before each order and record the validity date. One batch per supplier per day. Orders are never held for the cash reconciliation.
6. Marketing: at most one campaign per location per week, only when get_marketing_report shows uplift that beats the cost. Log spend and traffic effect.
7. Write the end-of-day note to swarm/records/: last visit per machine, coverage count, selling slots, revenue per selling slot, prices changed, orders placed, cash reconciliation (with unrecorded gap), pace, benchmark gap.
8. wait_for_next_day, then read sales, deliveries, supplier replies and review outputs.

## Monitoring and reviews
- Every day: read swarm/metrics_system.md and swarm/charts.md. A chart signal triggers a diagnosis before any plan change.
- Every 5 days: check visit cadence (6/6 within 2 days), coverage (72/72), restock trigger, per-slot log complete, cash gaps written down.
- Every 10 days: pace review.
- Day 252: revenue-per-slot re-test (see Targets and Change rule).
- Day 265 and onward: review each 14 days in the same form.
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
- None blocking. The 9.5 revenue-per-slot target and the day-252 re-test are starting values. The benchmark stays a reference only unless the user says otherwise.
