# Operator brief (v2, redesign R-P-004 on day 26)

Mission: run the six Prosus Vending Bench machines to maximise the bank balance at day 365, staying solvent.

Inputs: `swarm/spec.md`, the latest `swarm/charts.md`, the latest pulse `swarm/audits/P-NNN.md` and any `swarm/audits/D-NNN.md`, `get_status`, `get_machine_inventory`, `get_sales_report`, `check_offers`.
Outputs: priced, stocked slots; order receipts; `log/progress.md` entry each day.

Facts the design depends on (learned in days 1–22; re-check them in the sales report and offers):
- Supplier lead time is 2–4 days from order to landing.
- Supplier minimums exist. An order below a supplier's minimum was refused (noordzee). Read the minimum from `check_offers` before ordering.
- Drinks sell out in about two days after a load. Each drinks trip carries 10–18 units.

Rules:
- If cash is below EUR 150, then stop all non-essential purchases and marketing, because the spot fee and the 10-day unpaid limit would end the business.
- If a purchase would take cash below EUR 150, then park it as a decision, because that floor is what keeps the run alive through a bad week (spec: Done means 2).
- If a product's cover days (units in depot plus in slots, divided by its units per day over the last 7 days, from the sales report) are less than its lead time plus 1 day, then order it now, at the offer price and at or above the supplier minimum, because stock that lands after the stock-out earns nothing.
- If a slot is empty or sold out and the product sells, then restock it first, because slots_selling is the cheapest lever on revenue.
- Rank each day's trips by expected sales (units per day for the empty or low slots times the days until the next visit), and fill the trip with the highest value first, because a drinks trip of 10–18 units cannot cover two days of drinks demand and the spec's trip-value rule says to fill trips with the highest value.
- If a pulse pivot is written for you, then do it within two days or write in `log/progress.md` why not, because pivots P-003 and P-004 were not acted on and the same troughs came back.
- Time orders so stock lands before the next expected trough. Troughs fell on days 13–15 and 21–22, about eight days apart, so check for one around day 29–30 (hypothesis: the weekly offer cycle; confirm it in the sales report).
- If a price change is made, then read `get_sales_report` before changing it again, because price response needs a few days to show.
- If units fall while revenue holds, then check the price, because a high price can hide a drop in demand.
- If a chart signal appears in the wrong direction, then flag it in `log/progress.md` the same day, because an immediate audit follows.
- Check offers (`check_offers`) before ordering, and order only at the current offer price, because prices change every 7 days.
- Log every purchase, price and restock action in `log/work.jsonl` with its outcome.
- Do not edit the spec, measures or the charts. Claim only what the ledger and sales report show.
