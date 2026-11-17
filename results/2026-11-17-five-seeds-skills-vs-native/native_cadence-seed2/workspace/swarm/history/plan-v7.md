# Plan: operate Prosus Vending Bench for 365 days (EUR 1,500 start)

Revision 7 (day 201). Supersedes revision 6 kept in swarm/history/plan-v6.md. Written in response to swarm/audits/D-P-027.md, recorded in swarm/audits/R-P-027.md. Revision 6 (day 154) was written in response to D-P-022. Revision 5 (day 116) was written in response to D-P-017.

## Context
Goal: maximise final bank balance after 365 simulated days. Unfinished or bankrupt runs score zero. More than 10 consecutive unpaid spot-fee days ends the business (spot fee is EUR 12/day network-wide). Day 202 (swarm/charts.md): cash EUR 6,670 vs exemplar EUR 33,002 (PIP 6.1).

Failure (D-P-027, records through day 189): sales collapsed after day 171. 7-day revenue fell from 622 to 88 (gate 594). Selling slots fell from 9-10 to 1-6. Units per selling slot over days 176-189 were 2.82 (gate 4.3). The revision 6 day-170 review failed, but the failure was only recorded on day 189.

Leading cause (unconfirmed): stock is not reaching the machines. Days 174-189 show cash -17.5 where sales less the spot fee predict +272, a gap of about 290, mostly on day 177. Day 127 shows a similar gap (-99). These may be stock purchases made while slots emptied. Lower demand per slot (revenue per slot 8-9 down to 3-4) is not ruled out.

Corrections to revision 6
- The inventory-audit gate was never shown to be unmet. Revision 6 treated it as unmet because no note is in swarm/, but swarm/ holds no operator notes. Its status is unknown. Before acting on any gate, read the notes store directly for "inventory-audit", "daily-log" and "day-50-review". Record what each shows, or that it is absent. Do not infer from swarm/.
- Day-170 failure was late. Record review results on the day they run.

Rules that change now
- Freeze purchasing until the cash gap is explained. No purchase until the audit note includes a ledger reconciliation of days 127 and 174-189. Each unexplained amount is either given a cause or recorded as "cause unknown".
- Load before buying. Move stock from storage into existing selling slots first, highest-margin products first. Empty and near-empty slots come before dead slots. Confirm each slot holds stock after loading.
- Buy only when storage cannot fill the ranked touches. Then buy only what can be loaded within 2 days. Keep the EUR 200 reserve. No bulk buys.
- No new stocked slots while units per selling slot (14-day mean) is below 4.3.
- Demand test follows the distribution test. If a location's units per slot stays below 3 for 7 days after its slots are loaded, treat it as a demand problem. Stop restocking it and review its sales by product before any other change.
- Unit cost is not 0.73. Do not use 0.73 or 2.10 in any decision. Use cost per product from the ledger. Until recorded, margin is unknown and unknown-margin products are not bought.
- Cash is reported, not the success test. Success is units per selling slot (14-day mean) and 7-day revenue. Cash is checked against the ledger, because the unexplained gap means it cannot yet be read directly.
- Test one change at a time. This period's test is load-from-storage into existing slots, with purchasing frozen. Record units per selling slot and 7-day revenue weekly against day 189 (2.82 units per slot, revenue 88).
- Each new chart signal needs a diagnosis before the plan changes again. A point beyond a limit or 8 in a row on one side counts as a signal (charts.md rule).

Reviews
- Day 205: Write the "inventory-audit" note from the notes store and the ledger. Include: status of "inventory-audit", "daily-log" and "day-50-review"; ledger reconciliation of days 127 and 174-189; sales by product and location for days 176-189; stock in storage; units per selling slot (14-day mean).
- Day 210: Load test result. Record units per selling slot and 7-day revenue against 2.82 and 88. If units per slot is not rising, record the failure in an audit before any other change.
- Day 220: Decide whether to lift the purchasing freeze. Lift it only if the reconciliation is explained and storage is empty of sellable stock. Record the demand test result for each location.
- Day 230: Full review against swarm/metrics_system.md and swarm/charts.md, including the exemplar gap.

Daily loop
- Morning: get_status. Read swarm/charts.md level measures (selling slots, units, revenue per slot, cash_gain_7).
- get_sales_report by_product=true, days=7.
- Count storage stock. Load existing slots by the ranked rule above.
- Buy only under the purchasing rules.
- Write "daily-log": balance, selling slots (of total), units sold, units per selling slot, storage stock, stock loaded, purchases with reason, actions.
- wait_for_next_day.

Weekly
- check_offers at each 7-day validity change. Buy in bulk only after the freeze is lifted, when the offer is clearly below the ledger cost and the stock can be loaded within the week.
- Review supplier emails for delays or short shipments.
- Marketing: at most one campaign per location per week, only if 14-day mean units are rising.

Cash and risk
- Balance stays above EUR 200 at all times.
- Never let the network go unpaid for 10 days.
- Refunds only with the exact CMP- reference and the full amount.

Record hygiene
- R-P-017 was adopted on day 119 (swarm/charts.md), not day 116. Charts.md limits are authoritative for the pre-R-P-017 comparison.
- The day-120, day-130 and day-170 reviews were not recorded on their days. D-P-022 and D-P-027 record the misses.
- charts.md (day 202) shows cash_gain_7 at 347.96, inside limits. D-P-027 reports -6.1 on day 189, beyond the lower limit of 37.39. These cannot be reconciled from charts.md alone. Confirm against the day-189 chart row before using either figure.

Critical files
- swarm/plan.md (this plan), swarm/history/ (earlier versions: plan-v1.md to plan-v6.md)
- swarm/metrics_system.md, swarm/charts.md (daily system outputs)
- swarm/audits/ (diagnoses and change records: D-P-006, R-P-006, D-P-011, R-P-011, D-P-017, R-P-017, D-P-022, R-P-022, D-P-027, R-P-027)
- Notes keys: "state", "suppliers", "pricing", "daily-log", "inventory-audit", "day-11-review", "day-50-review"
- Reminders for reviews at days 205, 210, 220, 230

Verification
- Day 205: "inventory-audit" note exists, built from the notes store and ledger; days 127 and 174-189 are reconciled or recorded as "cause unknown".
- Day 210: no purchase made while the freeze applied; units per selling slot and 7-day revenue recorded against 2.82 and 88.
- Day 220: freeze decision and demand test result recorded in an audit.
- Day 230: full review recorded.

Status
Revision 7 written on day 201. Next live action: read the notes store for "inventory-audit", "daily-log" and "day-50-review". Then count storage stock and load existing selling slots. Purchasing stays frozen. No new stocked slots until units per selling slot reaches 4.3.
