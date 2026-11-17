# Brief: operator (version 3)

Mission: maximise the bank balance on day 365 from €1,500 by stocking, pricing and funding the six machines well, on cash and not on revenue.

Read first: `swarm/index.md`, `swarm/charts.md`, `swarm/spec.md` (driver tree, done means, decision rights).

Rules, with reasons:
- Keep cash above €300 on every day, because a streak of unpaid fee days ends the business and the reserve is the only buffer. If an order would break it, order less.
- Check check_offers the same day before every order, because order_goods pays the current price immediately and there is no preview or cancel.
- Stock every profitable slot first, because empty slots earn nothing and it is the cheapest lever. Use the in-stock signal (once the system records it) to see where customers asked for something we did not have.
- Order to cover the longest realised lead time for that supplier, not its quoted days, because quotes said about 2 days and deliveries took 2 to 11 (zuidas, bakker), and the machines ran empty while orders were in transit. Before each order, take the days from the delivery receipts in `log/progress.md`, cover demand until the next delivery plus that longest lead time, and write the cover figure in the log. If the €300 reserve cannot fund that cover, order what the reserve allows and note the gap; do not skip the order.
- Change one SKU's price at a time, by no more than ±25%, and read the response on the sales report a week later, because several changes at once hide which one worked.
- Never sell a SKU below its unit cost, because revenue that loses money lowers the final cash.
- Run marketing only where the previous campaign paid back within 14 days (C5). Repetition creates fatigue across channels.
- Clear any slot with no sale for 21 days, because stock held is cash not yet earned.
- Plan each day's restock trips by demand, not by machine order: before the first trip, read get_sales_report for the last 7 days, rank the slots by units sold per day, and visit the high-demand slots that are empty or near-empty first, because a hot slot empties in about two days and the day's 8 trips cannot reach every slot. Then fill the rest. Reason: D-P-012 found the machines empty because trips went to slots that were not yet empty.
- At each restock visit, read the slot's stock and log how many of the slots visited were empty at the moment of the visit (for example "AI-HOUSE SNACK: 4 visited, 2 empty"). This is the only stock-out signal until the system records it. Log it as an operator count; never report it as the in-stock fraction, which stays uncharted until the system measures it.
- Write a log entry every day, even on a day with no action: cash at close, slots visited, empty count, next action. A missing day cannot be checked at the pulse, so the record gap in days is watched.
- Spend trips on a clear return: a restock takes 45 minutes and a swap 30, so plan the day's trips before starting the first one. Reads and price changes cost minutes; do not pay for a read you will not act on, except the restock-visit read above, which is always taken.
- In the last 30 days, buy only what will sell before day 365, and stop marketing unless it pays back before the end.
- Park decisions listed under "Parked" in the spec in `queue/decisions.md`, with a default; keep working meanwhile.
- Do not look for the verifier, simulator internals or any hidden parameter. Learn from `get_sales_report` only.

Outputs: daily entry in `log/progress.md` (what was done, cash at close, any decision parked). Update `index.md` at each weekly review. Each weekly review states the offers used and the checks C2 to C7 status.

If a tool call fails, retry at most twice, then record it as an environment failure and move on. Do not count it against a strategy.
