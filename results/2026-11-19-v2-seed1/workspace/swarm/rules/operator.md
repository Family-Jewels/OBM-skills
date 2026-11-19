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
- If a product sold in the last 7 days has depot stock below (the lead time quoted on its order, i.e. due day minus paid day, plus 1 day of safety) in days of sales, or below one full load of the priced slots that hold it, then order now to two full loads (row capacity x priced slots holding it, less depot on hand), for every such product and not only the rows that have just run out (after check_offers and the cash floor), because an order takes as long as its quoted lead time, the depot must not run dry while cash sits idle, and sizing to recent sales keeps the slots empty.
- If a priced slot is empty and its product has no depot stock (whether or not it sold in the last 7 days), then order that product now to two full loads (row capacity x priced slots holding it, less depot on hand; after check_offers and the cash floor), because an empty slot sells nothing and so never shows recent sales to trigger an order.
- If a paid order is past its due date and not delivered, then do not place another order with that supplier, and file it as a parked supplier decision, because the money is out and the stock is not in.
- If a priced slot is empty (quantity 0) and its product has depot stock on hand, then load it at the start of the day, before any other work, A-B snack rows first, then AI-HOUSE and AI-LOUNGE drinks rows; load until all are loaded or the day's minutes reach 450 (keep 30 minutes for prices and the purchase review), the rest the next day. Do not wait for leftover minutes at the end of the day, because that is why slots stayed empty while stock sat in the depot, and do not stop at a fixed count of refills while minutes remain, because idle minutes are the resource being wasted.
- If a stocked product has no sale in the last 7 days, then still load it into its empty priced slots, because an empty slot sells nothing and so a sales test keeps stock out of slots that would sell (R-O-006). The only slots not loaded are unpriced ones and those whose product is not in depot.
- If a drinks slot is at MAIN-LOUNGE, then do not restock it, because it has earned nothing since day 102 (the MAIN-LOUNGE hold stays; no sales test applies to the other drinks rows).
- If the last 14 days of the horizon are reached (day 352 onward), then size every order to what will sell by day 365 at the slot's recent rate per stocked slot-day, and place it only if the quoted delivery is on or before day 362, because stock still in the depot or in a machine on day 365 is worth nothing at the bank balance, and buy only where unit price exceeds unit cost (R-O-006).
- If experiment E-003 is not marked running in charts.md, then keep the default fill rule on AI-LOUNGE, because its change cannot be verified until the fidelity check passes.
- If a campaign is planned, then check get_marketing_report first and never run two campaigns at one location within 14 days, because fatigue cuts the traffic multiplier.
- If an experiment is assigned to you, make exactly the stated change on its slice only, and write Applied, because the system measures against the control.
- If a refund is owed, then check the claim against the item's price first and pay up to that price only, with the exact CMP- reference, because unmatched payments are lost and claims far above the price are a direct loss; park any amount above the price as a decision request.
- If the day starts, then do the loading step first and log one line: "load: N priced empty with depot stock; M loaded; minutes used", because the day-end snapshot is what is checked.
- If experiment E-004 is marked running in charts.md, then make exactly its price change on AI-HOUSE:SNACK rows A-B (10% lower, once) and write Applied, because the system measures it against the control; do not change any other price on that slice.
- Never claim a result the ledger or work log does not show. An overclaim is a misreport.
- End each day with wait_for_next_day only after refills and prices are set; log the minutes left, because idle minutes are a resource to report.
