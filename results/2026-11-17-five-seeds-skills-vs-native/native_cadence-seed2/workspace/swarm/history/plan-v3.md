# Plan: operate Prosus Vending Bench for 365 days (EUR 1,500 start)

Revision 3 (day 40). Supersedes revision 2 kept in swarm/history/plan-v2.md. Written in response to swarm/audits/D-P-006.md, recorded in swarm/audits/R-P-006.md.

## Context
Goal: maximise final bank balance after 365 simulated days. Unfinished or bankrupt runs score zero. More than 10 consecutive unpaid spot-fee days ends the business (spot fee is EUR 12/day network-wide). Reference at day 40: exemplar cash about EUR 4,959 vs swarm about EUR 1,964 (swarm/charts.md, PIP 7.5).

Diagnosis (swarm/audits/D-P-006.md, day 35): the charts show no signal, but that means stable, not healthy. The gap is a level problem. Sales are bursty and falling, selling slots track restocks, unit economics are thin (about EUR 2 revenue per unit), and about EUR 1,500 cash sits idle above the reserve. The day-11 inventory audit was never recorded.

## Gate: inventory audit (today, day 40)
No new stock purchase until note "inventory-audit" exists. Record:
- units bought vs units loaded vs units sold, per machine and per slot;
- stock held in machines vs storage vs unsold stock in storage;
- stocked slots vs total slots per machine (the gap is the restock backlog);
- unit margin per product (sell price minus supplier cost), from get_sales_report by_product=true, days=7.

If the audit cannot be completed today, buy nothing and record why.

## Immediate actions (days 40 to 42)
1. Restock from storage first. Fill empty and near-empty slots from storage before buying anything. Priority: slots with positive margin that sold in the last 7 days.
2. Stop buying for slots that cannot be filled. A restock takes 45 min, about 8 touches per day. Plan each day's touches on slots with the highest expected sales per touch, not on the most slots.
3. Cap idle cash. Keep the EUR 200 reserve. Buy only what the loaded slots can sell within 7 days, based on the audit's sales rate. Do not hold stock in storage beyond that.
4. Reconcile the selling-slot count. D-P-006 reports 8 selling slots; charts.md shows 14 as the latest slots_selling value. Settle the true count from get_sales_report and record it in "inventory-audit".
5. Reprice only products with a confirmed positive margin. Do not change prices on the basis of charts.

## Daily loop (revised)
- Morning: get_status. Read swarm/charts.md for the level measures (revenue per slot, units, selling slots), not for movement inside limits.
- get_sales_report by_product=true, days=7.
- Restock from storage, then fill the highest-value empty slots, then swap dead slots.
- Reserve rule: never let cash fall below EUR 200. Spend above it only on stock that loaded slots can sell within 7 days.
- Write "daily-log": balance, selling slots (of total), units sold, revenue per restock touch, actions.
- wait_for_next_day.

## Weekly
- check_offers at each 7-day validity change. Buy in bulk only when the offer is clearly below last week's cost and the stock can be loaded within the week.
- Review supplier emails for delays or short shipments.
- Marketing: at most one campaign per location per week, and only if sales are rising for two weeks.

## Cash and risk
- Balance stays above EUR 200 at all times. Never let it approach zero.
- Check that the network is never unpaid for 10 days.
- Clear dead slots (clear_slot or swap_item) rather than letting them rot.
- Refunds only with the exact CMP- reference and the full amount.

## Reviews
- Day 45: selling slots, revenue per slot, and units against the day-40 audit. If selling slots are still not rising, stop all purchases until storage is cleared and the audit is recorded again.
- Day 50: full review, using metrics_system.md and charts.md level measures. Check the economics: revenue per unit, margin per product, spot fee coverage.
- Root-cause requests: investigate the flagged slot or location before changing the plan.

## Critical files
- swarm/plan.md (this plan), swarm/history/ (earlier versions: plan-v1.md, plan-v2.md)
- swarm/metrics_system.md, swarm/charts.md (daily system outputs)
- swarm/audits/ (diagnoses and change records)
- Notes keys: "state", "suppliers", "pricing", "daily-log", "inventory-audit", "day-11-review"
- Reminders for reviews at days 45, 50, 100, ...

## Verification
- Day 42: "inventory-audit" note exists with all fields above. Storage restock done.
- Day 45: selling slots and units higher than day 40. No purchase made without a recorded audit.
- Day 50: margin per product confirmed. Balance trajectory compared with the exemplar.

## Status
Revision 3 written on day 40. Next live action: the inventory audit, then restock from storage.
