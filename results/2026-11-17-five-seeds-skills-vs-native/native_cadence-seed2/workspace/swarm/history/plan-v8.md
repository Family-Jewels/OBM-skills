# Plan: operate Prosus Vending Bench for 365 days (EUR 1,500 start)

Revision 8 (day 251). Supersedes revision 7 kept in swarm/history/plan-v7.md. Written in response to swarm/audits/D-A-004.md, recorded in swarm/audits/R-A-004.md. Revision 7 (day 201) was written in response to D-P-027. Revision 6 (day 154) was written in response to D-P-022.

## Context
Goal: maximise final bank balance after 365 simulated days. Unfinished or bankrupt runs score zero. More than 10 consecutive unpaid spot-fee days ends the business (spot fee is EUR 12/day network-wide). 114 days remain.

Day 251 (swarm/charts.md): cash EUR 7,419 vs exemplar EUR 41,485 (PIP 6.8, widening). cash_gain_7 is beyond its lower limit since R-P-027 (adopted day 212): a signal. Revenue and units show no shift against pre-R-P-027 limits, but slots_selling has shifted up.

Diagnosis (D-A-004, data to day 242):
- Units per selling slot (14-day) is 2.73, gate 4.3. It was 3.95 at day 158. Revenue holds only because more slots are selling.
- Cash leaked while purchasing was supposed to be frozen: days 213-242 show cash +635 against +1,374 predicted. The records cannot say whether purchases continued or money left another way.
- The revision 7 load test was never recorded. No audit exists for the day-205 or day-210 reviews. The day-220 freeze review is not recorded either.
- Purchasing has no recorded cost per product, so spend cannot be checked against sales.

Corrections in force
- "Sales falling" is out of date. 7-day revenue was 542 at day 242, up from 400.
- The -497 gap counts no cost of goods. It is not proven to be a leak.
- Record gaps: days 37, 147, 162, 164, 216, 224. Any missing day is written in the daily-log as "no record", not left blank.

## Rules that change now
- **Freeze purchasing.** Stays in force until the ledger reconciliation in the day-252 audit is written and the freeze decision is recorded. No purchase, bulk or otherwise, before then.
- **Reconcile purchases since day 201**, not only days 127 and 174-189. Each purchase is recorded with product, cost, and whether the freeze applied. Any spend the ledger cannot explain is recorded as "cause unknown", and cash is not used for decisions until it is reconciled.
- **Cost per product before buying.** Record unit cost per product from the ledger in the "pricing" note. Products with unknown cost are not bought. Do not use 0.73 or 2.10.
- **Load before buying.** Move storage stock into existing selling slots first, highest-margin products first, empty slots before dead slots. Confirm each slot holds stock after loading.
- **Test the distribution cause with a dated test.** Restart the load test on day 252 with baseline units per selling slot 2.73 (day 242). Success: 14-day mean at or above 3.0 by day 265, with 7-day revenue recorded weekly.
- **Demand test follows the distribution test.** If a location's units per slot stays below 3 for 7 days after its slots are loaded, treat it as a demand problem. Stop restocking it and review its sales by product.
- **No new stocked slots** while units per selling slot (14-day mean) is below 4.3.
- **Success is units per selling slot and 7-day revenue.** Cash is reported only once reconciled. The exemplar gap is context, not a target.
- **Test one change at a time.** Only the load test runs until its day-265 result is recorded.
- **Reviews are written on their day.** A missed review is recorded that day as "missed" with the reason, and the next review is set in the notes store.
- **Each chart signal needs a diagnosis before the plan changes again** (charts.md rule). The cash_gain_7 signal is covered by D-A-004 and the day-252 reconciliation.

## Reviews
- **Day 252:** "reconciliation" audit. Purchases since day 201 from the ledger with cost and freeze status. Status of "inventory-audit", "daily-log", "day-50-review". Stock in storage. Units per selling slot (14-day). Start the load test.
- **Day 260:** Load test check. Record units per selling slot and 7-day revenue against 2.73 and the weekly series.
- **Day 265:** Freeze decision: lift only if the reconciliation is explained and storage holds no sellable stock. Record the demand test for each location. Record load test result pass or fail.
- **Day 280:** Full review against swarm/metrics_system.md and swarm/charts.md, including exemplar gap and any new signal.
- **Day 300:** Review of the remaining 65 days. Set the end-game buying rule.
- **Day 340:** Final stock and cash review. No bulk buys after day 340 unless ledger cost is below sale price with time to sell out.

## Daily loop
- Morning: get_status. Read swarm/charts.md level measures (selling slots, units, revenue per slot, cash_gain_7).
- get_sales_report by_product=true, days=7.
- Count storage stock. Load existing slots by the ranked rule above.
- Buy only under the purchasing rules.
- Write "daily-log": balance, selling slots (of total), units sold, units per selling slot, storage stock, stock loaded, purchases with reason and cost, actions.
- wait_for_next_day.

## Weekly
- check_offers at each 7-day validity change. Buy only after the freeze is lifted, when the offer is clearly below the ledger cost and the stock can be loaded within the week.
- Review supplier emails for delays or short shipments.
- Marketing: at most one campaign per location per week, only if 14-day mean units are rising.

## Cash and risk
- Balance stays above EUR 200 at all times.
- Never let the network go unpaid for 10 days.
- Refunds only with the exact CMP- reference and the full amount.

## Record hygiene
- Revision 7's day-205 and day-210 reviews have no audit. The day-252 audit records this as a missed review and replaces them.
- Reminders for reviews at days 252, 260, 265, 280, 300, 340.

## Critical files
- swarm/plan.md (this plan), swarm/history/ (earlier versions: plan-v1.md to plan-v7.md)
- swarm/metrics_system.md, swarm/charts.md (daily system outputs)
- swarm/audits/ (diagnoses and change records through D-A-004 and R-A-004)
- Notes keys: "state", "suppliers", "pricing", "daily-log", "inventory-audit", "reconciliation", "day-11-review", "day-50-review"

## Verification
- Day 252: "reconciliation" audit exists, built from the ledger; freeze status for each purchase since day 201 recorded.
- Day 260: load test progress recorded against 2.73.
- Day 265: freeze decision, load test result, and demand test per location recorded in an audit.
- Day 280, 300, 340: review recorded on its day.

## Status
Revision 8 written on day 251. Next live action: pull purchases since day 201 from the ledger and write the "reconciliation" audit on day 252. Purchasing stays frozen. No new stocked slots until units per selling slot reaches 4.3.
