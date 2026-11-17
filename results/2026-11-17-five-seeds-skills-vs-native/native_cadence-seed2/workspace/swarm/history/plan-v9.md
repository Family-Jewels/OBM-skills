# Plan: operate Prosus Vending Bench for 365 days (EUR 1,500 start)

Revision 9 (day 288). Supersedes revision 8 kept in swarm/history/plan-v8.md. Written in response to swarm/audits/D-P-036.md, recorded in swarm/audits/R-P-036.md. Revision 8 (day 251) was written in response to D-A-004. Revision 7 (day 201) was written in response to D-P-027. Revision 6 (day 154) was written in response to D-P-022.

## Context
Goal: maximise final bank balance after 365 simulated days. Unfinished or bankrupt runs score zero. More than 10 consecutive unpaid spot-fee days ends the business (spot fee is EUR 12/day network-wide). 77 days remain.

Day 276 (D-P-036 data): 7-day revenue 586, down from 930 at day 258. cash_gain_7 225, below its centre since day 268. Units per selling slot weekly: 4.27, 3.28, 3.94. Selling slots fell from about 13 to about 10 a day.

Corrections in force
- The rev 8 gates on days 252, 260 and 265 have no audit. They are recorded as "missed" with the reason "records not written", not backdated.
- PIP recomputed: 5.59 at day 251 and 5.25 at day 276. The 6.1 in swarm/charts.md is wrong. Use the recomputed figure until the charts are corrected.
- R-A-004 is dated day 251 in the plan and the audit. charts.md says day 254. Treat day 251 as correct until checked.
- The 3.84 units-per-slot headline averages over a fall. Use weekly figures.
- Cash rises about 0.8-1.0 less than revenue minus the EUR 12 fee per unit sold. Spend is still unexplained. Cash is not used for decisions.

## Rules that change now
- **Reconciliation first, today.** Write the "reconciliation" audit on day 288 from the ledger: all purchases since day 251 with product, cost, and freeze status, compared with units sold. Count storage. Any unexplained spend is recorded as "cause unknown".
- **Purchasing stays frozen** until the reconciliation audit is written and the freeze decision is recorded. No purchase, bulk or otherwise, before then.
- **Storage is a test, not a fact.** Each day, count stock in storage and stock loaded into selling slots. Restocked stock is treated as not selling until loaded and confirmed in a slot.
- **Load before buying.** Move storage stock into existing selling slots first, highest-margin products first, empty slots before dead slots. Confirm each slot holds stock after loading.
- **Cost per product before buying.** Record unit cost per product from the ledger in the "pricing" note. Products with unknown cost are not bought.
- **Distribution test restarts on day 289** from the current 14-day units per selling slot, recorded in the audit. Success: 14-day mean at or above 4.3 by day 305, with 7-day revenue recorded weekly.
- **Demand test follows the distribution test.** If a location's units per slot stays below 3 for 7 days after its slots are loaded, treat it as a demand problem. Stop restocking it and review its sales by product.
- **No new stocked slots** while units per selling slot (14-day mean) is below 4.3.
- **Success is units per selling slot and 7-day revenue.** Cash is reported only once reconciled. The exemplar gap is context, not a target.
- **Test one change at a time.** Only the distribution test runs until its day-305 result is recorded.
- **Reviews are written on their day.** A missed review is recorded that day as "missed" with the reason, and the next review is set in the notes store.
- **Each chart signal needs a diagnosis before the plan changes again** (charts.md rule). The cash_gain_7 and slots_selling signals are covered by D-P-036 and the day-289 reconciliation.

## Reviews
- **Day 288 (today):** "reconciliation" audit as above. Record the missed day-252, 260 and 265 reviews. Start the distribution test.
- **Day 295:** Distribution test check. Units per selling slot (14-day) and 7-day revenue against the day-289 baseline.
- **Day 305:** Freeze decision: lift only if the reconciliation is explained and storage holds no sellable stock. Record the demand test for each location. Record distribution test pass or fail.
- **Day 320:** Full review against swarm/metrics_system.md and swarm/charts.md, including exemplar gap and any new signal.
- **Day 340:** Final stock and cash review. No bulk buys after day 340 unless ledger cost is below sale price with time to sell out.
- **Day 355:** End-game check. Stop all buying unless stock can sell out before day 365.

## Daily loop
- Morning: get_status. Read swarm/charts.md level measures (selling slots, units, revenue per slot, cash_gain_7).
- get_sales_report by_product=true, days=7.
- Count storage stock. Load existing slots by the ranked rule above.
- Buy only under the purchasing rules.
- Write "daily-log": balance, selling slots (of total), units sold, units per selling slot, storage stock, stock loaded, purchases with reason and cost, actions. Write "no record" for any missing day.
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
- Missed gates at days 252, 260 and 265 are recorded as "missed" in the day-288 audit. Their reviews are not reconstructed.
- Reminders for reviews at days 288, 295, 305, 320, 340, 355.

## Critical files
- swarm/plan.md (this plan), swarm/history/ (earlier versions: plan-v1.md to plan-v8.md)
- swarm/metrics_system.md, swarm/charts.md (daily system outputs; PIP figure to be corrected)
- swarm/audits/ (diagnoses and change records through D-P-036 and R-P-036)
- Notes keys: "state", "suppliers", "pricing", "daily-log", "inventory-audit", "reconciliation", "day-11-review", "day-50-review"

## Verification
- Day 288: "reconciliation" audit exists, built from the ledger; freeze status for each purchase since day 251 recorded; storage counted; missed gates recorded.
- Day 295: distribution test progress recorded against the day-289 baseline.
- Day 305: freeze decision, distribution test result, and demand test per location recorded in an audit.
- Day 320, 340, 355: review recorded on its day.

## Status
Revision 9 written on day 288. Next live action: write the "reconciliation" audit from the ledger on day 288. Purchasing stays frozen. No new stocked slots until units per selling slot reaches 4.3.
