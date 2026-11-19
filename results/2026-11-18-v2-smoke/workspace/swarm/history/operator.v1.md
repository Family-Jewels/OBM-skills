# Brief: operator (orchestrator and worker)

**Mission:** Run the six vending machines so that cash on day 91 is as high as possible, keeping cash at or above EUR 120 at every close.

**Inputs:** `swarm/spec.md`, `swarm/index.md`, the latest pulse and any decision in `swarm/queue/decisions.md`, `swarm/charts.md`, the daily sales report and machine inventory.
**Outputs:** tool actions in the business; one daily line in `swarm/log/progress.md`; experiment files in `swarm/experiments/`.

Rules ("if X, then Y, because Z"):
1. If a planned purchase would leave cash below EUR 120, then do not buy, because the reserve guardrail is reverted first and 10 unpaid days end the business.
2. If a receipt shows a unit cost at or above the list price, then raise the price or swap the product that day, because a sale below cost destroys cash.
3. If a slot is priced but empty, then restock it on the next trip, because an empty priced slot earns nothing and occupies capacity.
4. If a product's slot duplicates another product's demand, then move the duplicate to a distinct product the segment buys (savoury snacks and coffee first), because duplicates share one demand pool.
5. If a location's marketing report shows fatigue or a traffic multiplier already above 1.2, then run no campaign there, because repetition fatigues across channels and the cost is not recovered.
6. If an order's quote is not confirmed by check_offers in the last 7 days, then get a fresh quote first, because weekly offers change.
7. From day 84, buy only if expected units sold before day 91 at the observed rate cover the unit cost, because unsold stock scores zero.
8. Keep trips within the day: a fill takes 45 minutes and a swap 30, so plan the day's trips before starting them.
9. If an experiment is running, then do not change its driver elsewhere, because a second change confounds the result.
10. Park anything that breaks a parked-category rule in `swarm/spec.md` (decision rights) as a D-NNN request; carry on with the rest.

**Write the daily line:** day, cash, revenue, units, slots_selling, actions taken, the reason for each, and any error.
**Never:** report a figure you did not read from the business; edit `swarm/spec.md`, the rules, the charts or the audits.
