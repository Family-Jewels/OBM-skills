# Plan: Operate Prosus Vending Bench for 365 days (v7, revised day 198 per D-P-030)

## Context
Goal: maximise bank balance at day 365 from EUR 1,500. Unfinished or bankrupt runs score zero, so survival comes first: never let the business sit more than 10 consecutive unpaid days (spot fee EUR 12/day network-wide). Benchmark: roughly EUR 61,219 at day 365.

At day 198 cash is 8,723.33 (charts.md). The benchmark path needs (61,219 − 8,723.33) / 167 = **about EUR 314/day** from here. The exemplar is at 32,310 (PIP 4.3). The benchmark cannot be reached at current breadth: at 8.65 revenue per selling slot, about 316/day of revenue needs about 37 selling slots, and the record maximum is 20. The pace target is therefore re-based (see Targets). The 260/day figure in v6 is retired.

Why this revision: D-P-030 (day 185 diagnosis) found:
1. Selling breadth fell from 11.3/day (days 140–152) to 6.0 (days 153–164) and 7.8 (days 165–185). The day-175 test failed (days 159–174 mean 6.9 against a target of 13).
2. The drop began on day 153, twelve days before R-P-025 (day 165). The redesign changed measures and targets only, so it is not the trigger. Its adoption may have been a response to the drop.
3. charts.md and plan.md used different centres (7.5 and 9.9). This plan fixes one.
4. The cause of the drop is unverified. The leading candidate is coverage or visits at specific slots and machines from about day 153.
5. There are no records (no swarm/records/ folder). Visits, coverage, purchases and cash cannot be checked.
6. Outflow for days 131–138 implies about 394 (about 49/day), not the 252 in P-024.

Constraints (unchanged):
- 8-hour day. Restock 45 min, swap 30 min, price change a few minutes. Plan 6–10 machine trips per day.
- Six machines (3 locations x SNACK/DRINKS), 72 slots. Snack rows A/B hold 18, C/D hold 10. Drinks slots hold 10.
- Duplicate products share demand, so extra slots add capacity only if they are stocked and priced.
- Cash banks overnight; card takings settle a day later; open complaints hurt reputation.
- Tools: if vending tools are not available in the session, record that in the day's note, do the parts that can be checked from the workspace, and do not write as if records exist.

## Measures (one definition each)
- Selling slots: the distinct count of slots with a sale on the day, as logged in swarm/charts.md (slots_selling).
- **Current-phase centre: 7.5 (limits 0.5 to 14.5), phase since day 165, as in the top table of charts.md.** This is the only centre for judging signals and tests. The 9.9 centre in v6 and the "before" table in charts.md are reference values only.
- Rolling 7-day distinct selling slots: logged, secondary only.
- Revenue and cash gain: calendar days, as charted.
- Pace: benchmark path = (61,219 − cash) / days remaining, recomputed each day. Reference only, see Targets.

## Targets (hard rules)
- Visit cadence (first priority): each of the six machines is visited at least every 2 days. Record the last visit date per machine in every daily note. A machine with no visit in 2 days is the first trip of the day.
- Coverage: all 72 slots loaded and priced. An empty or unpriced slot is a defect to fix on the next trip.
- Load per slot: snack A/B at least 12 of 18; snack C/D at least 7 of 10; drinks at least 7 of 10.
- Restock on every visit: every slot at or below half capacity is refilled to full on that visit. Order quantity per product = 7 days of that slot's recent sales, rounded up.
- Weekly full stock: SUSPENDED.
- Selling-slot interim target: the mean of the daily count for days 199–222 is at least 11 (the pre-drop level was 11.3, days 140–152). Test at day 223. The v6 ladder (18, 25, 30) is suspended until the breadth cause is found.
- Pace target: re-based at day 223 from measured breadth and revenue per selling slot. Until then, the benchmark gap is reported in notes, not treated as a target or trigger.
- Price: every slot priced above cost on every visit. No price tests until the day-223 coverage and cadence checks pass.
- Burst guard: a day's revenue below 50% of the prior 3-day average triggers a check of stock and visit date in every slot at the affected machines that day, with the response written in the note. Zero-sale days (29, 114, 133, 154, and any new one) also get a written response: stock, price and visit date per slot at that machine. A burst-guard or zero-sale day is not by itself a plan change.
- Cash reconciliation (record, not gate): each day, reconcile balance change against revenue, purchases, spot fee and marketing. Write any unrecorded part and its size. Restocking and supplier orders continue regardless.
- Pace review: every 10 days. Do not change strategy on the gap alone.

## Change rule (judging changes)
- Judge any change against the current-phase centre and limits above, and only after at least 14 days of observation.
- One change at a time. Record the change, the day it started, and the measure it is judged on.
- Act only on a chart signal: a point beyond limits or 8 in a row on one side of the centre (7.5). A single high or low point is routine variation.
- Do not reverse R-P-025 on its own. The measures it set stay until a coverage or visit cause is tested.
- The cash_gain_7 "shift down" in charts.md compares post-day-125 values with a pre-day-125 centre. Re-baseline at the day-208 review before acting on it.

## Immediate actions (day 198–223)
1. Create swarm/records/ now. Log per day: last visit per machine, slots loaded and priced (of 72), selling slots, purchases and deliveries, marketing spend, and the cash gap. Back-fill from days 150 onward where the data exists.
2. Pull sales by slot and the visit and stock log for days 150–156. Test the day-153 step: which slots and machines lost sales, and whether they were empty, unpriced or unvisited. Write the result in swarm/records/breadth-d150-156.md.
3. Coverage and visit recovery: visit all six machines, restock every slot at or below half, fix every unpriced slot. Record the count.
4. Reconcile days 131–138: write the implied outflow (about 394) next to the P-024 figure (252) and state which one the records support.
5. Write the day-208 full review (see Monitoring): cause of breadth drop, coverage result, zero-sale and burst-guard responses, pace, and the re-based targets.
6. Day 223: run the breadth test (see Test).

## Daily loop
1. get_status. Check balance, complaints, open orders, and which slots are at or below half.
2. Check last visit date per machine. Any machine not visited in 2 days is visited first.
3. get_sales_report by slot and product for the last day. Record the daily selling-slot count, the burst guard and any zero-sale machine.
4. Plan trips: restock every slot at or below half to full, fix every unpriced slot.
5. Order from suppliers using the per-product quantities above. Check_offers before each order and record the validity date. One batch per supplier per day. Orders are never held for the cash reconciliation.
6. Marketing: at most one campaign per location per week, only when get_marketing_report shows uplift that beats the cost. Log spend and traffic effect.
7. Write the end-of-day note to swarm/records/: last visit per machine, coverage count, selling slots, prices changed, orders placed, cash reconciliation (with unrecorded gap), pace, benchmark gap.
8. wait_for_next_day, then read sales, deliveries, supplier replies and review outputs.

## Test (day 223)
- Compare the daily selling-slot mean for days 199–222 with the current-phase centre of 7.5 and the target of 11.
- If the mean is at least 11 and every machine was visited within 2 days with 72/72 coverage, the coverage cause is confirmed and the recovery holds. Re-set the ladder and pace target at this review.
- If the mean is below 11 with full cadence and coverage, product mix or demand is the cause. Run the full diagnosis of product mix and pricing. Price tests may then be considered.
- If cadence or coverage was not met, the test is void for cause. Fix cadence and coverage and re-run at day 237.

## Monitoring and reviews (from the system)
- Every day: read swarm/metrics_system.md and swarm/charts.md. A chart signal triggers a diagnosis before any plan change.
- Every 5 days: short review. Check visit cadence (6/6 within 2 days), coverage (72/72), selling slots (daily mean), restock trigger, and whether cash gaps are written down. Act on any warning here.
- Every 10 days: pace review.
- Day 208: full review. Diagnose from sales and inventory data before changing the plan. Save the prior version to swarm/history/ with a version number.
- Day 223: breadth test (see Test).
- Always follow the current swarm/plan.md when it differs from this file.

## Risks and guards
- Bankruptcy: keep cash above roughly EUR 200 and pay the spot fee every day. Stop discretionary spending if the balance falls. This is the only guard that stops purchases.
- Missed visits: a machine not visited within 2 days is the main known risk. It is checked first each day.
- Stockouts: a slot with stock but no price sells nothing. Check every machine at least every 2 days.
- Overstock: order per the 7-day rule. Do not add stock beyond it.
- Supplier risk: keep 2 suppliers for core lines and verify deliveries in the depot.
- Complaints: resolve promptly with send_payment using the exact CMP- reference and the full amount. Never guess the reference.
- Marketing overspend: log each campaign and its traffic effect in notes.
- Missing records: write the gap and its size in the note. Do not leave it blank, and do not stop restocking because of it.

## Verification
- Daily: last visit per machine, coverage count, selling-slot count, slots at or below half, burst guard and zero-sale responses, cash reconciliation (with unrecorded parts stated), pace and benchmark gap written to swarm/records/.
- Weekly: revenue and selling slots compared with the prior 7 days; restock quantities compared with the sales-by-slot data.
- Plan and notes are updated after each review.

## Open questions for the user
- None blocking. The day-223 target of 11, the pace re-base and the 14-day window are starting values. Confirm at the day-208 review whether the benchmark is still a target or only a reference.
