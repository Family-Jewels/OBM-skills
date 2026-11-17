# Plan: operate Prosus Vending Bench for 365 days (EUR 1,500 start)

Revision 5 (day 116). Supersedes revision 4 kept in swarm/history/plan-v4.md. Written in response to swarm/audits/D-P-017.md, recorded in swarm/audits/R-P-017.md.

## Context
Goal: maximise final bank balance after 365 simulated days. Unfinished or bankrupt runs score zero. More than 10 consecutive unpaid spot-fee days ends the business (spot fee is EUR 12/day network-wide). Day 116: cash EUR 4,180 vs exemplar EUR 18,115 (PIP 6.2, swarm/charts.md).

Diagnosis (swarm/audits/D-P-017.md): cash gain fell from about +31/day (days 67-81) to +13/day (days 82-100) while revenue and units were flat. Stock is spreading across more selling slots with fewer units per slot (4.3 to 4.0). The unit-cost figure of EUR 0.73 is stale. Days 82-100 imply about EUR 1.35/unit, so margin may be near EUR 0.7, not 1.4. Purchasing has run without a cost gate since R-P-011.

## Rules that change now
- **Unit cost is not 0.73.** Do not use 0.73 or 2.10 in any decision. Use cost per product taken from the ledger and the inventory audit. Until it is recorded, treat margin as unknown.
- **Purchasing is gated.** No purchase until the "inventory-audit" note records cost per product (from the ledger) and is dated today. Then buy only for the top-ranked restock touches within 7 days. No bulk buys.
- **No new stocked slots** while units per selling slot (14-day mean) is below 4.3, the day 67-81 level. Fill and restock existing slots first.
- **Restock touches ranked by margin.** Rank by recent units per slot times the measured margin per unit for that product. Products with unknown or non-positive margin rank last and are not bought.
- **Shifts are recorded, not read as improvement.** cash_gain_7 has a signal since the R-P-011 redesign (13 points below the old centre 214.7, days 93-105). Judge it against the old limits in swarm/charts.md. Do not treat "routine variation" in the current status as progress.

## Gate: inventory audit (today, day 116)
Write or update note "inventory-audit". Record:
- total and stocked slots per machine, and units per selling slot (14-day mean);
- units bought vs loaded vs sold, per product, machine and slot;
- stock in machines vs storage;
- cost per product from the ledger, and margin per product from get_sales_report by_product=true, days=14.

Check for notes "day-50-review" and "daily-log". If missing, say so in the audit; do not assume them.

Audit day 91 (zero sales, zero slots): find the cause in the daily-log or ledger. If none is found, record "cause unknown" in the audit.

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
- Day 120: audit gate complete? Margin per product known? Record units per selling slot and cash gain since day 116.
- Day 130: units per selling slot at or above 4.3 and cash_gain_7 mean above its old-limit centre 214.7, or record the failure in an audit before changing anything else.
- Day 150: full review against metrics_system.md and charts.md, including the exemplar gap (day 116 PIP 6.2).
- Root-cause requests: investigate the flagged slot or location before changing the plan.

## Critical files
- swarm/plan.md (this plan), swarm/history/ (earlier versions: plan-v1.md to plan-v4.md)
- swarm/metrics_system.md, swarm/charts.md (daily system outputs)
- swarm/audits/ (diagnoses and change records: D-P-006, R-P-006, D-P-011, R-P-011, D-P-017, R-P-017)
- Notes keys: "state", "suppliers", "pricing", "daily-log", "inventory-audit", "day-11-review"
- Reminders for reviews at days 120, 130, 150

## Verification
- Day 116: "inventory-audit" note exists with cost per product from the ledger.
- Day 120: no purchase made before the audit note was written; margin per product recorded.
- Day 130: units per selling slot at or above 4.3, or the failure is recorded in an audit.

## Status
Revision 5 written on day 116. Next live action: the inventory audit (cost per product from the ledger), then ranked restock touches for today. No purchases until the audit is written.
