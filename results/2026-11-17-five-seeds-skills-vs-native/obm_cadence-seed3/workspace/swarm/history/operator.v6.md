# Brief: operator (version 6)

Mission: maximise the bank balance on day 365 from €1,500 by stocking, pricing and funding the six machines well, on cash and not on revenue.

Read first: `swarm/index.md`, `swarm/charts.md`, `swarm/spec.md` (driver tree, done means, decision rights).

Rules, with reasons:
- Keep cash above €300 on every day, because a streak of unpaid fee days ends the business and the reserve is the only buffer. If an order would break it, order less.
- Check check_offers the same day before every order, because order_goods pays the current price immediately and there is no preview or cancel.
- Stock every profitable slot first, because empty slots earn nothing and it is the cheapest lever. Use the in-stock signal (once the system records it) to see where customers asked for something we did not have.
- Order to a cover target, never to empty, because quotes said about 2 days, deliveries took 2 to 11 (zuidas, bakker), and the last five took 3 to 4 days; every order so far was placed only after its SKU ran out, so the depot ran dry and the machines stood empty while orders were in transit (D-P-029). Before each order, in this order:
  (a) read the depot stock of the SKU and the stock in its slots;
  (b) from get_sales_report for the last 7 days, take the SKU's units per day;
  (c) cover days = (depot stock + slot stock) ÷ units per day;
  (d) lead time used = the longest of the last five deliveries for that supplier in `log/progress.md` (dated order to arrival), not its quoted days;
  (e) order so that cover after delivery is at least lead time used + 1 day, quantity from check_offers at that quantity, within the reserve.
  Trigger: place the reorder when cover falls to lead time + 1 day, not when stock reaches zero. Log one line per order: `ORDER <PO> <supplier> <SKU> | depot | slot | units/day | cover before | lead time used | cover after`. If the €300 reserve cannot fund the target, order what it allows, write the shortfall in the log and at the next pulse; do not skip the order.
- Change one SKU's price at a time, by no more than ±25%, and read the response on the sales report a week later, because several changes at once hide which one worked.
- Never sell a SKU below its unit cost, because revenue that loses money lowers the final cash.
- Run marketing only where the previous campaign paid back within 14 days (C5). Repetition creates fatigue across channels.
- Clear any slot with no sale for 21 days, because stock held is cash not yet earned.
- Plan each day's restock trips from the machines' current state, not from the sales report alone: before the first trip, read the stock of every slot in the active rotation (one read pass), and read get_sales_report for the last 7 days to rank them by units sold per day. Visit the high-demand slots that are empty or near-empty and in stock at the depot first, because a hot slot empties in about two days. Then fill the rest, each visited slot to its full capacity from depot stock where the depot allows (v6: not a partial load of about 10 per SKU), because a partial load sells out in about two days and the slot stands empty until the next trip; the depot counts and the order rule still apply first. Reason: D-P-025 found trips going out without a current view of which slots were empty, so visits found full slots or missing SKUs.
- Keep the active restock rotation to about 16 slots, the number the day's trips can keep full (each selling slot needs a reload every 2 to 3 days). Do not add a slot to the rotation while it is at 16. Slots outside the rotation are not restocked; they leave the rotation only when they sell out or hit the 21-day rule, never cleared early just to free a trip. Guard: every machine keeps at least one stocked selling slot in SNACK and in DRINKS (M1), and no location goes unstocked for more than 2 days (parked). Reason: D-P-025 found about 42 assigned slots against 8 to 10 trips a day, so most slots stood empty while trips went to full ones.
- At each restock visit, read the slot's stock and log how many of the slots visited were empty at the moment of the visit (for example "AI-HOUSE SNACK: 4 visited, 2 empty"). This is the only stock-out signal until the system records it. Log it as an operator count; never report it as the in-stock fraction, which stays uncharted until the system measures it.
- (v6) For each SKU loaded at a visit, log loaded units, and at that slot's next read log units found. The difference, less units recorded sold between the two reads (from get_sales_report), is the unexplained loss for that slot. Log it as an operator count on the visit's line. Do not guess its cause in the log; write "unexplained" and the figures. Reason: D-P-036 found stock vanishing between loads and reads with nothing in the records to explain it, so no one could see where it went. This is the interim instrument until D-007 is answered (spec C9).
- Write a log entry every day, even on a day with no action: cash at close, slots visited, empty count, next action. A missing day cannot be checked at the pulse, so the record gap in days is watched.
- Spend trips on a clear return: a restock takes 45 minutes and a swap 30, so plan the day's trips before starting the first one. Reads and price changes cost minutes. The rotation read before planning and the restock-visit read are always taken, because the trip plan depends on them; other reads are taken only when you will act on them.
- In the last 30 days, buy only what will sell before day 365, and stop marketing unless it pays back before the end.
- Park decisions listed under "Parked" in the spec in `queue/decisions.md`, with a default; keep working meanwhile.
- Do not look for the verifier, simulator internals or any hidden parameter. Learn from `get_sales_report` only.

Outputs: daily entry in `log/progress.md` (what was done, cash at close, any decision parked). Update `index.md` at each weekly review. Each weekly review states the offers used and the checks C2 to C7 status.

If a tool call fails, retry at most twice, then record it as an environment failure and move on. Do not count it against a strategy.
