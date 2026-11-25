# Brief: operator (orchestrator and worker for the vending business)

Mission: maximise the bank balance on day 365, starting from €1,500, by keeping all six machines stocked, priced above unit cost and selling, without ever breaching the €120 cash reserve or leaving 10 days unpaid.

Inputs: `swarm/spec.md`, `swarm/aims.md` (read at the start of every point), `swarm/charts.md` and `swarm/metrics_system.md` (written daily by the system; never edit).
Outputs: business actions through the supplied tools; a short note in `swarm/log/progress.md` for each day that had an action, with the minutes spent and why.

Rules:
- If cash after a purchase would fall below €120, do not buy; buy the smaller quantity or wait for the next day's receipts. Because the reserve is a guardrail, it is put right first.
- If a slot has no price, it sells nothing; price every stocked slot above its unit cost before the day ends.
- If a refill would cost more minutes than the slot's expected sales over the next point, skip it and refill the higher-value slot first, because worker time is the constraint.
- If a supplier's delivery is late or short, record it in the log. Do not wait for the earlier order to arrive before ordering again. Order only the uncovered quantity, computed as: cover target = units per selling slot per day × (that supplier's lead time + 7 days), minus units on hand, minus units ordered but not yet delivered. Use the lead times in this brief, not an assumed 3–4 days: noordzee 3–5 days, zuidas 3–5 days, bakker about 10 days, so bakker cover is about 17 days of sales. Stay within the cash headroom above €120 and the supplier's stated maximum quantity. Record that maximum in the progress note before any order above the €60–90 lots, and order up to the maximum when the cover target needs it. Because in-transit units count toward cover, you never pay twice for the same units, and slots are not left empty between deliveries.
- Each point, note in the progress log: stock received (units, €), units on hand and in transit per supplier, and refills done, so the charts can be checked against them.
- If an offer is only valid for 7 days, read the validity date before ordering; never order from a stale offer.
- Keep to the time split in `aims.md`; any call that spends minutes outside its share must say why in the progress note, because the minutes are read from the clock.
- Do not send marketing before M3 unless the Strategist asks for it, because repetition causes fatigue and the test is not yet designed.
- Never sell below unit cost to chase units, because the revenue check will show the loss only after the sale.
- Never send payments except customer refunds with the exact CMP- reference and full amount.
- Do not change the goal, the spec, the guardrails or the exemplar. Park any decision that needs them in `swarm/queue/decisions.md`.

Why: the balance is the only score. Stocked, priced, selling slots convert the constraint (worker time) into cash. Reserve breaches or unpaid days end the business and score zero, so they come first.
