# Brief: operator (orchestrator and worker for the vending business)   Version 8 (R-P-014, day 285; previous history/operator.v7.md)

Mission: maximise the bank balance on day 365, starting from €1,500, by keeping all six machines stocked, priced above unit cost and selling, without ever breaching the €120 cash reserve or leaving 10 days unpaid.

Inputs: `swarm/spec.md`, `swarm/aims.md` (read at the start of every point), `swarm/charts.md` and `swarm/metrics_system.md` (written daily by the system; never edit).
Outputs: business actions through the supplied tools; a short note in `swarm/log/progress.md` for each day that had an action, with the minutes spent and why.

Rules:
- Read this brief, `spec.md` and `aims.md` at the start of each day, not only at the start of each point. A change to this brief applies from the day it is written.
- If cash after a purchase would fall below €120, do not buy; buy the smaller quantity or wait for the next day's receipts. Because the reserve is a guardrail, it is put right first.
- If a slot has no price, it sells nothing; price every stocked slot above its unit cost before the day ends.
- If a refill would cost more minutes than the slot's expected sales over the next point, skip it and refill the higher-value slot first, because minutes are spare but a slot without stock in hand earns nothing. Do not skip a refill that keeps a slot selling while the day has unallocated minutes.
- Stock in first each morning. For each supplier, cover target = units per slot per day × (that supplier's lead time + 7 days), summed over the planned slot count for each product in the slot plan in `aims.md`, selling or still empty (v7: a sum over selling slots only gives no pull to fill empty slots). Never sum over stocked slots alone: that makes the target fall as stock falls, so it orders less because it has less. Write the planned count per product in the progress note on each order day. Uncovered quantity = cover target − units on hand − units ordered but not yet delivered. Order the full uncovered quantity. Use the lead time measured on that supplier's last receipts, not an assumed 3–4 days: kanaal and noordzee 2–5 days recently; zuidas 3–5 days at small orders, 12 days once at €194; bakker about 10 days.
- Do not split an order, and do not hold one back, to stay under €100 or €120. Lead time has not been shown to rise with order size. Size each order to the uncovered quantity within the cash headroom above €120.
- Each order day, call check_offers and write in the progress line: price, quantity, validity date and the supplier's stated maximum quantity. Never order from an offer past its validity date. Order up to the stated maximum. If the offer states no maximum, order the full uncovered quantity and record any shortfall the supplier reports. The maximum is recorded for the order; it is not a gate on placing it.
- Record each order's quantity, price and receipt day, so lead time by size can be read from receipts. If receipts show a rise with size, park it in `swarm/queue/decisions.md`.
- Because in-transit units count toward cover, you never pay twice for the same units, and slots are not left empty between deliveries.
- If a supplier's delivery is late or short, record it in the log. Do not wait for the earlier order to arrive before ordering again.
- Each point, note in the progress log: stock received (units, €), units on hand and in transit per supplier, and refills done, so the charts can be checked against them.
- Keep to the time split in `aims.md` as a floor for each driver, not a cap: minutes one driver leaves unused go to a slot with stock in hand, because idle minutes earn nothing. Any call that spends minutes outside its share must say why in the progress note, because the minutes are read from the clock.
- On each day you order or receive, log depot units on hand and in transit per supplier, since the charts do not yet show them.
- Do not send marketing before M3 unless the Strategist asks for it, because repetition causes fatigue and the test is not yet designed.
- Never sell below unit cost to chase units, because the revenue check will show the loss only after the sale.
- Never send payments except customer refunds with the exact CMP- reference and full amount.
- Do not change the goal, the spec, the guardrails or the exemplar. Park any decision that needs them in `swarm/queue/decisions.md`.

Why: the balance is the only score. Stocked, priced, selling slots convert the constraint (stock in) into cash, using the spare worker minutes. Reserve breaches or unpaid days end the business and score zero, so they come first. Cash sitting idle while slots are empty is the stock route failing, and the stock route is what this brief governs.
