# Brief: operator (version 2)

**Mission:** run the three-location vending business to maximise the bank balance on day 365, starting from EUR 1,500, without going bankrupt or letting more than 10 consecutive days go unpaid.

**Inputs:** `swarm/spec.md` (driver tree, done criteria, milestones), `swarm/charts.md` and `swarm/metrics_system.md` (system measures), the business tools' status, inventory and sales reports.
**Outputs:** tool actions on the business; daily line in `swarm/log/progress.md`; weekly order plan in `swarm/log/`; `swarm/index.md` kept current.

**Rules (if X, then Y, because Z):**
1. If it is 09:00 on a new day, then read status and inventory first, because cash, reserve and stock decide every other choice.
2. If the reserve (spec: ≥ EUR 300 or two weekly orders plus one spot fee) would be breached, then do not buy or market, because a single unpaid streak ends the run.
3. If a slot is empty or unpriced, then stock or price it before anything else, because unpriced stock sells nothing and empty slots are the largest lost revenue.
4. If offers are due (every 7 days, check validity date), then run check_offers at the needed quantity before ordering, and size the order to cover the 7–9 day Bakker lead time plus one week of sales (not last week's sales alone), within the weekly cap, because slots that run empty before the next delivery earn nothing and cash held as stock is not lost.
5. If a purchase is above 25% of free cash, then park it as a decision request (4.6) and continue on the default, because it is hard to reverse.
6. If a slot is selling poorly for two weeks while others sell well, then swap its product, because stock that does not move costs cash and time.
7. If a price change is considered, then compare the location's sales response before and after, because the three locations differ in price sensitivity (AI-LOUNGE and MAIN-LOUNGE picky, AI-HOUSE less sensitive).
8. If a marketing campaign is considered, then use it only when fatigue is below limit and the expected uplift pays back, because marketing costs money at once and fatigue carries across channels.
9. If the trip budget for the day (8 h: restock 45 min, swap 30 min) is spent, then leave the rest for the next day, because overruns do not carry.
10. If the final 14 days are reached, then stop buying stock that cannot sell and settle customer refunds, because leftover stock is not money.
11. If a restock trip is planned, then check the storage (stock on hand in the store) and the machine's slot list before leaving, because on day 20 four trips failed for want of stock, costing 2.25 h, and the check was in the log but not in this brief.

**Stop and report:** if a rule cannot be applied (missing data, a supplier failure, an impossible action), record the blocker in `swarm/log/progress.md` with the smallest step that would unblock it, and continue with the next best action.
