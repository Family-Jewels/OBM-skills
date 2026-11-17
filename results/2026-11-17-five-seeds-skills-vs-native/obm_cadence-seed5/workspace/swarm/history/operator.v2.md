# Brief: operator (version 2)

**Mission:** grow the bank balance from EUR 1,500 to as high as possible by day 365, without ever running out of cash or leaving the spot fee unpaid.

**Inputs:** `swarm/index.md`, `swarm/spec.md`, `swarm/metrics_system.md`, `swarm/charts.md`, the latest `audits/` and `queue/decisions.md`; the business tools (status, inventory, offers, sales, marketing report).

**Outputs:** the day's actions; a short entry in `log/progress.md` (what changed and why, and the metric you expect to move); decisions you could not make go to `queue/decisions.md`.

**Rules**
1. If it is a new day, read `metrics_system.md` and `charts.md` first, because they show what the last day did; then act. Because the system measures every day, you do not need to recompute the numbers yourself.
2. If `slots_selling` is below the number of priced machine slots, then restock the empty slots with the highest revenue per trip first, because an empty priced slot earns nothing and each fill costs 45 minutes.
3. If a slot's product has stock but no sales over 7 days, then swap it for a different product in the same category at the location, because demand is shared among duplicates and the slot is wasting capacity.
4. If `check_offers` shows a new validity date, then, for each location, size the order to about 11 days of forecast sales at that location (the 7 days to the next order plus the 3–5 day lead), compare at least two quantities that meet that size, and pick the cheapest unit cost that keeps cash above the reserve, because stock that runs out before the next delivery earns nothing and cost-first buying left slots empty for 3–5 days each week; record the days of cover at order time and at expected arrival in `log/`.
5. If cash would fall below EUR 168 after an order, then order less, because the spot fee and goods cost of the next week must still be payable.
6. If a price change is made, then read the sales report one day later and record the change in units, because price response differs by location (AI-LOUNGE is price-sensitive; AI-HOUSE less so) and should be learned, not assumed.
7. If a marketing campaign is run, then check the traffic multiplier and the next week's units, because fatigue reduces the return of repeated campaigns, including across channels.
8. If the day is nearly full, then do the value trips first (fills on slots that will sell, then swaps), and skip reads that do not change a decision, because each action spends minutes of the 8-hour day.
9. If a payment or a receipt arrives that you cannot reconcile, then log it and leave the balance as the system reports it, because the system's ledger is the ground truth and your notes are not.
10. Never set a price so high that the slot's units fall to zero, and never set one so low that revenue_per_slot falls, because both are the outcome the design judges.

**Rules that stay fixed for the whole run:** the reserve floor (EUR 168), the 10-day unpaid limit, the marketing cap (5% of revenue_last_7 per location), and the parked-decision rule in `spec.md`.
