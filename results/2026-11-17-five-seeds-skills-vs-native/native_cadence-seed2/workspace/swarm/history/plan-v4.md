# Plan: operate Prosus Vending Bench for 365 days (EUR 1,500 start)

Revision 4 (day 81). Supersedes revision 3 kept in swarm/history/plan-v3.md. Written in response to swarm/audits/D-P-011.md, recorded in swarm/audits/R-P-011.md.

## Context
Goal: maximise final bank balance after 365 simulated days. Unfinished or bankrupt runs score zero. More than 10 consecutive unpaid spot-fee days ends the business (spot fee is EUR 12/day network-wide). Reference at day 81: exemplar cash about EUR 12,056 vs swarm about EUR 3,339 (swarm/charts.md, PIP 5.7).

Diagnosis (swarm/audits/D-P-011.md): revenue is not weakening; the "weakening" reading came from endpoints. Volume is capped by stocked selling slots, and revenue per stocked slot is steady at about 8-12. The likely limit is restock throughput (about 8 touches per day). Cash is not binding: about EUR 2,676 sits above the EUR 200 reserve. Unit economics are positive (about EUR 2.10 revenue per unit against about EUR 0.73 cost, approximate).

## Measures
- Judge trends on 14-day means of selling slots and units, never on single days or endpoints.
- Revenue above its upper limit since day 46 is a recorded shift. Note it; do not change the plan on it alone.
- Selling-slot counts of 8 (day 35) and 14 (day 40) both match their dates. No reconciliation needed.

## Gate: inventory audit (today, day 81)
Confirm note "inventory-audit" exists and is current. If not, write it before any purchase. Record:
- total slots per machine and stocked slots per machine (sizes the restock backlog);
- units bought vs loaded vs sold, per machine and slot;
- stock in machines vs storage;
- unit margin per product, from get_sales_report by_product=true, days=14.

Check for notes "day-50-review" and "daily-log". If they are missing, say so in the audit; do not assume them.

## Restock throughput (the constraint)
1. Each day, rank the roughly 8 restock touches by expected revenue per touch: recent units per slot times about EUR 2.10 per unit.
2. Fill empty high-value slots first, from storage where possible. Then near-empty slots. Swap or clear dead slots last.
3. Do not buy for slots that cannot be touched within 7 days.

## Purchasing
- Keep the EUR 200 reserve. Above it, buy to fill the slots in today's and the next 7 days' restock plan.
- Cash is not the constraint, so do not hold back purchases that the restock plan can use. Do not buy stock that will sit in storage beyond 7 days.
- Reprice only products with a confirmed positive margin.

## Daily loop
- Morning: get_status. Read swarm/charts.md level measures (selling slots, units, revenue per slot).
- get_sales_report by_product=true, days=7.
- Rank and perform restock touches (see above). Buy only per the purchasing rule.
- Write "daily-log": balance, selling slots (of total), units sold, revenue per restock touch, actions.
- wait_for_next_day.

## Weekly
- check_offers at each 7-day validity change. Buy in bulk only when the offer is clearly below last week's cost and the stock can be loaded within the week.
- Review supplier emails for delays or short shipments.
- Marketing: at most one campaign per location per week, only if 14-day mean units are rising.

## Cash and risk
- Balance stays above EUR 200 at all times.
- Never let the network go unpaid for 10 days.
- Clear dead slots rather than letting them rot.
- Refunds only with the exact CMP- reference and the full amount.

## Reviews
- Day 90: 14-day means of selling slots and units against days 67-81. If selling slots are flat or falling, record the restock-touch ranking and its results in an audit before changing anything else.
- Day 100: full review, using metrics_system.md and charts.md level measures. Check revenue per unit, margin per product, and the exemplar gap.
- Root-cause requests: investigate the flagged slot or location before changing the plan.

## Critical files
- swarm/plan.md (this plan), swarm/history/ (earlier versions: plan-v1.md, plan-v2.md, plan-v3.md)
- swarm/metrics_system.md, swarm/charts.md (daily system outputs)
- swarm/audits/ (diagnoses and change records: D-P-006, R-P-006, D-P-011, R-P-011)
- Notes keys: "state", "suppliers", "pricing", "daily-log", "inventory-audit", "day-11-review"
- Reminders for reviews at days 90, 100, ...

## Verification
- Day 81: "inventory-audit" note exists with all fields above, including total slots per machine.
- Day 90: 14-day mean selling slots and units higher than days 67-81, or the restock ranking is recorded as failing.
- Day 100: margin per product confirmed. Gap to exemplar compared with day 81 (PIP 5.7).

## Status
Revision 4 written on day 81. Next live action: the inventory audit, then the ranked restock touches for today.
