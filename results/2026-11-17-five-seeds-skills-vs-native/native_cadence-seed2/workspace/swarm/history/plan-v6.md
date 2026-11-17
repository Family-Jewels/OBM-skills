# Plan: operate Prosus Vending Bench for 365 days (EUR 1,500 start)

Revision 6 (day 154). Supersedes revision 5 kept in swarm/history/plan-v5.md. Written in response to swarm/audits/D-P-022.md, recorded in swarm/audits/R-P-022.md. Revision 5 (day 116) was written in response to swarm/audits/D-P-017.md, recorded in swarm/audits/R-P-017.md.

## Context
Goal: maximise final bank balance after 365 simulated days. Unfinished or bankrupt runs score zero. More than 10 consecutive unpaid spot-fee days ends the business (spot fee is EUR 12/day network-wide). Day 154: cash EUR 5,364 vs exemplar EUR 24,693 (PIP 6.0, swarm/charts.md).

Diagnosis (swarm/audits/D-P-017.md, carried forward): cash gain fell from about +31/day (days 67-81) to +13/day (days 82-100) while revenue and units were flat. The unit-cost figure of EUR 0.73 is stale and margin is unknown.

Diagnosis (swarm/audits/D-P-022.md, day 146 records): sales are slipping. Revenue over 7 days is 467 (day 146), about 21% below the 594 of a month earlier. Units per selling slot fell from 4.31 (days 67-81) to 3.23 (days 139-146), below the 4.3 gate. Selling slots rose from 8.7 to 9.6 a day while units per day fell from 35.1 to 31.1, so stock is spreading thinner. Cash is rising (5,184 at day 146) while slots thin. The likely cause is that the purchasing gate and no-new-slot rule have slowed restocking. This is untested: no "inventory-audit" note exists.

## Rules that change now
- **Unit cost is not 0.73.** Do not use 0.73 or 2.10 in any decision. Use cost per product taken from the ledger and the inventory audit. Until it is recorded, treat margin as unknown.
- **Cash is not the success test.** cash_gain_7 since day 119 is a recovery to the pre-dip level (about 217 a week), not growth beyond it. Success is measured by units per selling slot (14-day mean) and 7-day revenue. Cash is reported, not used to judge the plan.
- **Purchasing is gated, and the gate must be reachable.** No purchase until the "inventory-audit" note records cost per product (from the ledger) and is dated today. Once it does, restock existing selling slots (not new ones) for the top-ranked touches within 7 days. No bulk buys. Keep the EUR 200 reserve.
- **No new stocked slots** while units per selling slot (14-day mean) is below 4.3. Fill and restock existing slots first.
- **Restock touches ranked by margin.** Rank by recent units per slot times the measured margin per unit for that product. Products with unknown or non-positive margin rank last and are not bought.
- **Test one change at a time.** Restock-first is the test this period. Record units per selling slot and 7-day revenue weekly against the day-146 values (3.23 units per slot, revenue 467).

## Gate: inventory audit (today, day 154)
The audit has never been written, so no gate has been met. Write the "inventory-audit" note first. Record:
- total and stocked slots per machine, and units per selling slot (14-day mean);
- units bought vs loaded vs sold, per product, machine and slot;
- stock in machines vs storage;
- cost per product from the ledger, and margin per product from get_sales_report by_product=true, days=14.

Check for notes "day-50-review" and "daily-log". If missing, say so in the audit; do not assume them.

Investigate the unexplained cash events in the ledger or daily-log: day 127 (cash -103.5 on revenue 7.1) and day 91 (cash +14.8 on zero revenue and zero slots). If no cause is found, record "cause unknown" in the audit.

## Restock throughput
1. Each day, rank the roughly 8 restock touches by expected margin per touch (see rules above).
2. Fill empty high-margin slots first, from storage where possible. Then near-empty slots. Clear dead slots last.
3. Do not buy for slots that cannot be touched within 7 days.

## Purchasing
- Keep the EUR 200 reserve. Above it, buy only what the ranked touches in the next 7 days can load, and only after the audit gate is met.
- Do not buy stock that will sit in storage beyond 7 days.
- Reprice only products with a confirmed positive margin.

## Daily loop
- Morning: get_status. Read swarm/charts.md level measures (selling slots, units, revenue per slot, cash_gain_7).
- get_sales_report by_product=true, days=7.
- Rank and perform restock touches (see above). Buy only per the purchasing rule.
- Write "daily-log": balance, selling slots (of total), units sold, units per selling slot, margin per touch, actions.
- wait_for_next_day.

## Weekly
- check_offers at each 7-day validity change. Buy in bulk only when the offer is clearly below the ledger cost and the stock can be loaded within the week.
- Review supplier emails for delays or short shipments.
- Marketing: at most one campaign per location per week, only if 14-day mean units are rising.

## Cash and risk
- Balance stays above EUR 200 at all times.
- Never let the network go unpaid for 10 days.
- Refunds only with the exact CMP- reference and the full amount.

## Reviews
- Day 160: inventory audit written and restock-first running? Units per selling slot (14-day mean) and 7-day revenue recorded against day 146.
- Day 170: units per selling slot at or above 4.3 and 7-day revenue at or above 594 (the day-146 month-earlier level). If not, record the failure in an audit before changing anything else.
- Day 180: full review against metrics_system.md and charts.md, including the exemplar gap (day 154 PIP 6.0).
- Root-cause requests: investigate the flagged slot or location before changing the plan.

## Record hygiene
- R-P-017 was adopted on day 119 (swarm/charts.md), not day 116 as plan.md once said. The old centre is 153.76 in charts.md and 214.7 in earlier plan text. charts.md limits are authoritative for the pre-R-P-017 comparison.
- The day-120 and day-130 reviews were not recorded as completed. D-P-022 records the day-130 miss.

## Critical files
- swarm/plan.md (this plan), swarm/history/ (earlier versions: plan-v1.md to plan-v5.md)
- swarm/metrics_system.md, swarm/charts.md (daily system outputs)
- swarm/audits/ (diagnoses and change records: D-P-006, R-P-006, D-P-011, R-P-011, D-P-017, R-P-017, D-P-022, R-P-022)
- Notes keys: "state", "suppliers", "pricing", "daily-log", "inventory-audit", "day-11-review"
- Reminders for reviews at days 160, 170, 180

## Verification
- Day 154: "inventory-audit" note exists with cost per product from the ledger, and the day 127 and day 91 events are explained or recorded as "cause unknown".
- Day 160: no purchase made before the audit note was written; margin per product recorded; restock-first results recorded.
- Day 170: units per selling slot at or above 4.3 and 7-day revenue at or above 594, or the failure is recorded in an audit.

## Status
Revision 6 written on day 154. Next live action: write the inventory audit (cost per product from the ledger), then ranked restock touches for existing selling slots. No new stocked slots until units per selling slot reaches 4.3.
