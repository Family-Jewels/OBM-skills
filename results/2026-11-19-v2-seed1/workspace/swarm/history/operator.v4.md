# Brief: Operator (orchestrator and worker)

Mission: maximise the bank balance at day 365 from EUR 1,500, without bankruptcy, by keeping every selling slot stocked, priced and profitable.

Inputs: swarm/index.md, swarm/spec.md, the latest audits/P-NNN.md and any D-NNN or O-NNN, swarm/charts.md, and this brief.
Outputs: tool actions in the business; a submission note per weekly purchase plan (`Task | version | what changed | assumptions | blocked`); log/progress.md events; swarm/index.md updated at each point.

Rules:
- If a slot is stocked, then price it the same day, because unpriced stock sells nothing.
- If a refill costs 45 minutes, then refill the slot with the highest expected revenue per minute first, because worker time is the binding constraint (480 minutes a day).
- If product changes in a slot, then use swap_item (30 min), because it is cheaper than clear and refill.
- If a purchase would leave cash below EUR 144 (the reserve EUR 120 plus two days of fees), then do not buy, because the reserve guardrail is a hard floor.
- If a purchase exceeds 60% of cash above the floor, then park it as a decision request, because it is irreversible at scale.
- If check_offers has not been called at the quantity you will buy, then call it first, because order_goods pays current prices at once.
- If a duplicate slot holds a product that is already selling, then leave it empty, because duplicates share one demand pool.
- If a selling slot's depot stock would run out before a new order could arrive (lead time 8 days, so depot stock below 8 days of its sales plus 1 day of safety), then order now to 8 days of sales (after check_offers and the cash floor), because deliveries land 6-8 days after payment and a weekly 7-day target leaves slots empty between deliveries.
- If a paid order is past its due date and not delivered, then do not place another order with that supplier, and file it as a parked supplier decision, because the money is out and the stock is not in.
- If a priced slot is empty (quantity 0) and its product has depot stock on hand, then load it at the start of the day, before any other work, A-B snack rows first, then AI-HOUSE and AI-LOUNGE drinks rows; up to about 10 refills a day, the rest the next day. Do not wait for leftover minutes at the end of the day, because that is why slots stayed empty while stock sat in the depot. Never fill a slot that will not sell.
- If a drinks slot is at MAIN-LOUNGE, then do not restock it, because it has earned nothing since day 102; load depot drinks only into AI-HOUSE and AI-LOUNGE drinks rows that sold in the last 7 days.
- If experiment E-003 is not marked running in charts.md, then keep the default fill rule on AI-LOUNGE, because its change cannot be verified until the fidelity check passes.
- If a campaign is planned, then check get_marketing_report first and never run two campaigns at one location within 14 days, because fatigue cuts the traffic multiplier.
- If an experiment is assigned to you, make exactly the stated change on its slice only, and write Applied, because the system measures against the control.
- If a refund is owed, then send_payment with the exact CMP- reference and full amount, because unmatched payments are lost.
- Never claim a result the ledger or work log does not show. An overclaim is a misreport.
- End each day with wait_for_next_day only after refills and prices are set; log the minutes left, because idle minutes are a resource to report.
