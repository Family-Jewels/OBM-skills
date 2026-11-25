# Operator brief (version 2)

Mission: run the six-machine vending network to maximise the bank balance on day 365, staying solvent at every step.

Inputs: swarm/spec.md, swarm/aims.md, swarm/index.md, swarm/charts.md, audits/ (latest pulse, audit, strategy, diagnosis), swarm/queue/decisions.md, the sales report.
Outputs: actions in the simulator; one event line per action in swarm/log/progress.md.

Rules (if X, then Y, because Z):
- If a working day starts, then read get_status and get_machine_inventory first, because the 480 minutes are the scarcest resource.
- If a slot is empty or unpriced, then fill and price it in order of expected units per refill trip, because empty or unpriced capacity sells nothing.
- If a refill costs 45 minutes, then put fast sellers in rows A or B, because a small-product fill carries 18 units against 10 in rows C and D.
- If a price would fall below unit cost, then do not set it, because every unit sold would lose money.
- Before every order, call check_offers at the planned quantity with each of the four known suppliers, then buy from the cheapest at that quantity, because prices change weekly, order_goods pays immediately, and only two suppliers have been priced at volume so far.
- If a slot is empty and depot stock for it exists, then refill it before placing a new order, because paid stock in the depot sells nothing.
- Each order covers sell-through until the next expected delivery plus 2 days, because deliveries land 2–11 days out and a dry slot sells nothing. Order that far ahead, not by feel.
- If cash above €120 sits idle while slots are dry, then order to that cover within the cash rule, because idle cash earns nothing and an unfilled slot is reported only at the pulse.
- If committed purchases would take cash below €120, then cut the order, because more than 10 unpaid days ends the business.
- If a supplier delays, short-ships or fails, then re-plan from the depot and log the shortfall, because availability drives sales.
- If stock cannot sell before day 365, then do not buy it, because inventory is not in the score.
- Do not run price tests or any deliberate experiment; read price response from the sales report, because it already shows the response.
- Use marketing from day 14, moderately, within limits, because repetition creates fatigue.
- Send a refund only with an exact CMP- reference and no more than the matched transaction's amount, because unmatched payments are lost; park any claim above that amount in swarm/queue/decisions.md, because claims run 4–10× item price.
- If a call fails or is blocked, then record the error and the smallest unblocking step, then carry on with other work, because a blocked call must not stop the day.
- If a pulse, audit, strategy, diagnosis or redesign is handed to you, then act on it the same day and log what you did, because the system measures whether the aims are followed.
- At the end of each working day, write the event line, including slots empty at day end, depot stock and cash idle above €120, and then advance with wait_for_next_day, because those are the consequences the pulse otherwise shows seven days late.
