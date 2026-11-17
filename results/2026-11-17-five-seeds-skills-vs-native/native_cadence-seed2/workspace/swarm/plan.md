# Plan: operate Prosus Vending Bench for 365 days (EUR 1,500 start)

Revision 10 (day 336). Supersedes revision 9 kept in swarm/history/plan-v9.md. Written in response to swarm/audits/D-P-041.md (data to day 324), recorded in swarm/audits/R-P-041.md. Revision 9 (day 288) was written in response to D-P-036. Revision 8 (day 251) was written in response to D-A-004.

## Context
Goal: maximise final bank balance after 365 simulated days. Unfinished or bankrupt runs score zero. More than 10 consecutive unpaid spot-fee days ends the business (spot fee is EUR 12/day network-wide). 29 days remain.

Day 324 (D-P-041 data): 7-day revenue 375.95 (peak 930 at day 258). Units per selling slot, 14-day: 3.57, against the 4.3 gate. Selling slots about 10 a day, down from about 13. Revenue per slot roughly stable; the loss is slots not selling.
Money: over days 296 to 324, revenue 2,108.35, fees 336, cash change 829.74. About 942 is unexplained (about 0.93 per unit sold). Possible ongoing purchases. Unverified.

Corrections in force
- Reconciliation was due on day 252 and day 288. Neither is written. Every revision since rev 6 has prescribed it; none has executed it. This is the open loop.
- PIP basis is gain (exemplar gain / actual gain), as in swarm/charts.md. The 5.25 and 5.59 figures in revs 8 and 9 used raw cash and are withdrawn. PIP is 6.1 at day 276 and 6.2 at day 324 and day 336 (cash 10,353.87 vs exemplar 56,198.88).
- The 4.3 distribution gate has no day-305 result recorded. Treat it as failed. Current 14-day figure: 3.57.
- Missed and unrecorded reviews: days 252, 260, 265 (rev 8 gates), 288 (reconciliation), 295 (distribution check), 305 (gate and freeze decision). Record each as "missed" with the reason "records not written". Do not backdate.
- R-A-004 is dated day 251 in the plan and the audit. charts.md says day 254. Treat day 251 as correct until checked.
- Cash is not used for decisions until the reconciliation is written.

## Rules that change now
- **Reconciliation is the first action, today (day 336).** Write the "reconciliation" audit from the ledger: all purchases since day 251 with product, cost, freeze status, and units sold since then. Count storage. Record any unexplained spend as "cause unknown". If the ledger or notes cannot be read, write that as the blocker. Do not estimate.
- **Purchasing stays frozen** until the reconciliation audit is written. Any purchase made while the freeze is in force is logged as a breach in the audit.
- **Test the hypothesis directly.** Compare stock bought with stock loaded into slots. If stock is being bought and not loaded, stop all purchasing at once and record it.
- **Load before buying.** Move storage stock into selling slots, highest-margin products first, empty slots before dead slots. Confirm each slot holds stock after loading. Stock in storage counts as not selling until loaded.
- **No new stocked slots** while units per selling slot (14-day mean) is below 4.3. Dead slots are not restocked.
- **Late-game buying rule.** A purchase is allowed only if the ledger unit cost is below the sale price and the stock can sell out before day 365. Otherwise it is not bought.
- **Success is bank balance at day 365.** Protect cash. Units per selling slot and 7-day revenue are tracked as diagnostics. The exemplar gap is context, not a target.
- **Test one change at a time.** Only one change runs at once. Each chart signal needs a diagnosis before the plan changes again (charts.md rule).
- **Reviews are written on their day.** A missed review is recorded that day as "missed" with the reason.

## Reviews
- **Day 336 (today):** Reconciliation audit as above. Record the missed reviews listed under Corrections. Storage counted. Storage stock loaded into slots. Freeze status recorded.
- **Day 340:** Freeze decision. Lift only if the reconciliation is explained and storage holds no unloaded stock. If lifted, buys follow the late-game buying rule only.
- **Day 345:** Units per selling slot (14-day), 7-day revenue, and reconciled cash change, recorded against the day-336 baseline.
- **Day 355:** End-game check. Stop all buying unless stock can sell out before day 365. Confirm balance and log cash.
- **Day 365:** Final balance recorded in the daily-log.

## Daily loop
- Morning: get_status. Read swarm/charts.md level measures.
- get_sales_report by_product=true, days=7.
- Count storage stock and selling-slot stock. Load existing slots by the ranked rule above.
- Buy only under the purchasing rules.
- Write "daily-log": balance, selling slots (of total), units sold, units per selling slot, storage stock, stock loaded, purchases with reason and ledger cost, actions. Write "no record" for any missing day.
- wait_for_next_day.

## Weekly
- check_offers at each 7-day validity change. Buy only after the freeze is lifted, when the offer is clearly below ledger cost and the stock can be loaded and sold within the week.
- Review supplier emails for delays or short shipments.
- Marketing: none unless 14-day mean units are rising at that location.

## Cash and risk
- Balance stays above EUR 200 at all times.
- Never let the network go unpaid for 10 days.
- Refunds only with the exact CMP- reference and the full amount.

## Critical files
- swarm/plan.md (this plan), swarm/history/ (earlier versions: plan-v1.md to plan-v9.md)
- swarm/metrics_system.md, swarm/charts.md (daily system outputs)
- swarm/audits/ (diagnoses and change records through D-P-041 and R-P-041)
- Notes keys: "state", "suppliers", "pricing", "daily-log", "inventory-audit", "reconciliation", "day-11-review", "day-50-review"

## Verification
- Day 336: "reconciliation" audit exists, built from the ledger, with storage counted and missed reviews recorded.
- Day 340: freeze decision recorded in an audit.
- Day 345 and 355: review recorded on its day.
- Day 365: final balance recorded.

## Status
Revision 10 written on day 336. Next live action: write the "reconciliation" audit from the ledger today. Purchasing stays frozen. No new stocked slots while units per selling slot is below 4.3.
