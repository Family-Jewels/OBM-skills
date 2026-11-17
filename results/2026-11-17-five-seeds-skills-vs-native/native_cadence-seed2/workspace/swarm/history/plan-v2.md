# Plan: operate Prosus Vending Bench for 365 days (EUR 1,500 start)

Revision 2 (day 11). Supersedes the day-0 plan kept in swarm/history/plan-v1.md. The swarm is already live (day 8 of trading), so the "approve before day 0" step is removed.

## Context
Goal: maximise final bank balance after 365 simulated days. Unfinished or bankrupt runs score zero. More than 10 consecutive unpaid spot-fee days ends the business (spot fee is EUR 12/day network-wide). Reference: about EUR 3,228 at day 30, EUR 61,219 at day 365. At day 11 the swarm holds about EUR 1,215 cash against an exemplar at about EUR 2,134 (swarm/charts.md).

Diagnosis (swarm/audits/D-P-001.md): sales are very low (10 units total on day 8, 4 slots selling), and most capital is idle (cash about EUR 1,000 above the EUR 200 reserve). The likely cause, not verified, is that stock bought before day 2 was not loaded until about day 6. Machine and storage inventory must be checked before deciding anything else.

## Immediate actions (days 11 to 13)
1. Inventory audit first. Run get_machine_inventory and get_storage_inventory. Record in note "inventory-audit": units bought vs units loaded, per machine and per slot, and any empty or unpriced slots.
2. Load stock. Fill every empty or near-empty slot in all six machines (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE SNACK and DRINKS) from storage, or buy and load if storage is short. Target every slot stocked by the end of day 12.
3. Deploy idle cash. Keep EUR 200 reserve. Spend the rest on check_offers stock for the best-margin products, sized to the slots that will be filled. Do not buy for slots that cannot be loaded that day (45 min per restock, about 8 touches per day).
4. Compare with the exemplar. Count selling slots each day against the exemplar trajectory in charts.md. Target at least 12 selling slots by day 14.
5. Write a note "day-11-review" with the audit results. If the audit shows stock was not loaded, record that as the cause in D-P-001 follow-up.

## Daily loop (revised)
- Morning: get_status, then read swarm/metrics_system.md and swarm/charts.md. Do not react to movements inside the chart limits. Limits are computed by the system, not by agents.
- get_sales_report by_product=true, days=7. Check selling slots against the count above.
- Restock empty slots first (highest margin), then swap dead slots, then reprice.
- Reserve rule: never let cash fall below EUR 200. Spend above it only on stock that a loaded slot can sell within 7 days.
- Write the daily note ("daily-log"): balance, selling slots, units sold, actions.
- wait_for_next_day.

## Weekly
- check_offers at each 7-day validity change. Buy in bulk only when the offer is clearly below last week's cost.
- Review supplier emails for delays or short shipments.
- Marketing: at most one campaign per location per week, and only if sales are rising.

## Cash and risk
- Balance stays above EUR 200 at all times. Never let it approach zero.
- Check that the network is never unpaid for 10 days.
- Clear dead slots (clear_slot or swap_item) rather than letting them rot.
- Refunds only with the exact CMP- reference and the full amount.

## Reviews
- Day 16 (5 days after this revision): check selling slots, units, and revenue per slot against charts.md. If selling slots are still below 8, stop repricing and return to the stock audit.
- Day 50: full review, using metrics_system.md and charts.md ground-truth measures.
- Root-cause requests: investigate the flagged slot or location before changing the plan.

## Critical files
- swarm/plan.md (this plan), swarm/history/ (earlier versions)
- swarm/metrics_system.md, swarm/charts.md (daily system outputs, read every morning)
- swarm/audits/ (diagnoses and change records)
- Notes keys: "state", "suppliers", "pricing", "daily-log", "inventory-audit", "day-11-review"
- Reminders for reviews at days 16, 50, 100, ...

## Verification
- Day 12: all six machines show stock and prices (get_machine_inventory). Inventory audit note exists.
- Day 14: at least 12 selling slots; cash at or above reserve with spending matched to stocked slots.
- Day 16: sales per day trending up, not flat. Balance growing faster than the day-11 rate.
- Day 30: balance trajectory compared with the reference (about EUR 3,228).

## Status
Revision 2 written on day 11. Next live action: the inventory audit above.
