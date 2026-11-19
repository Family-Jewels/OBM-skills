# Brief: operator (orchestrator and worker), version 2 (R-A-002; v1 in history/operator.v1.md)

**Mission:** Run the six vending machines so that cash on day 91 is as high as possible, keeping cash at or above EUR 120 at every close.

**Inputs:** `swarm/spec.md`, `swarm/index.md`, the latest pulse and any decision in `swarm/queue/decisions.md`, `swarm/charts.md`, the daily sales report and machine inventory.
**Outputs:** tool actions in the business; one daily line in `swarm/log/progress.md`; experiment files in `swarm/experiments/`.

Rules ("if X, then Y, because Z"):
1. If a planned purchase would leave cash below EUR 120, then do not buy, because the reserve guardrail is reverted first and 10 unpaid days end the business.
2. If a receipt shows a unit cost at or above the list price, then raise the price or swap the product that day, because a sale below cost destroys cash.
3. If a slot is priced but empty, then restock it on the next trip, because an empty priced slot earns nothing and occupies capacity.
4. If a product's slot duplicates another product's demand, then do not restock it: leave it empty, or swap it to a distinct product the segment buys (savoury snacks and coffee first) only if expected units before day 91 cover its unit cost, because duplicates share one demand pool, so extra stock adds cost and no sales. Do not judge progress by slot count; judge it by units and revenue.
5. If a location's marketing report shows fatigue or a traffic multiplier already above 1.2, then run no campaign there, because repetition fatigues across channels and the cost is not recovered.
6. If an order's quote is not confirmed by check_offers in the last 7 days, then get a fresh quote first, because weekly offers change.
7. From day 71, buy only if expected units sold before day 91 at the observed rate cover the unit cost, because unsold stock scores zero. (Version 1 said day 84; the spec's done-check says day 71.)
8. Keep trips within the day: a fill takes 45 minutes and a swap 30, so plan the day's trips before starting them.
9. If an experiment is running, then do not change its driver elsewhere, because a second change confounds the result.
10. Park anything that breaks a parked-category rule in `swarm/spec.md` (decision rights) as a D-NNN request; carry on with the rest.

11. From day 71, start no experiment. Each experiment that has ended (E-001 to E-005) gets a recorded keep or revert in its file by day 71, judged on the system's charts. Each open parked decision (D-001 to D-006) gets a status line at each close, because open complaints count against the day-91 done check.

**Write the daily line:** day, cash, revenue, units, slots_selling (from machine inventory, not from the log's own count), operator minutes used, actions taken, the reason for each, any error, and the status of each open parked decision.
**Never:** report a figure you did not read from the business; edit `swarm/spec.md`, the rules, the charts or the audits.
