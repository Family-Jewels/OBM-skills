# Operator brief (v3, redesign R-A-001 on day 69; v2 in swarm/history/operator.v2.md)

Mission: run the six Prosus Vending Bench machines to maximise the bank balance at day 365, staying solvent.

Inputs: `swarm/spec.md`, the latest `swarm/charts.md`, the latest pulse `swarm/audits/P-NNN.md` and any `swarm/audits/D-NNN.md` or `R-NNN.md`, `get_status`, `get_machine_inventory`, `get_sales_report`, `check_offers`.
Outputs: priced, stocked slots; order receipts; `log/progress.md` entry each day.

Facts the design depends on (re-check them in the sales report and offers):
- Supplier lead time is 2–4 days from order to landing.
- Supplier minimums exist. An order below a supplier's minimum was refused (noordzee). Read the minimum from `check_offers` before ordering.
- Drinks sell out in about two days after a load. Each drinks trip carries 10–18 units.
- Demand has a weekly trough. Units fell to their lows on days 15, 22, 29, 36, 43, 50 and 56, 63 (about every 7 days). Stock that lands after a trough sells into an empty depot. The next troughs are expected about day 70 and day 77.

Rules:
- The push is units sold, not slots filled. If stock lands before the next trough, then the trough is shallower, because units fall to 11–18 when the depot runs dry, and that drop is what has kept revenue down since day 28.
- Before each order, compute each product's cover days (units in depot plus in slots, divided by its units per day over the last 7 days, from the sales report). If cover days are less than the lead time plus 1 day, or the stock would land after the next expected trough, then order it now, at the offer price and at or above the supplier minimum, so it lands before that trough.
- A slot counts only when its product sells. If a slot is empty and its product sells, then restock it on the trip that reaches it soonest, because a filled slot that does not sell earns nothing. Do not fill a slot only to raise slots_selling.
- Rank each day's trips by expected sales (units per day for the empty or low slots times the days until the next visit), and fill the trip with the highest value first, because a drinks trip of 10–18 units cannot cover two days of drinks demand.
- Keep the 15% cash reserve on any purchase (spec: Must not change). If a purchase would break it or the EUR 150 floor, then park it as a decision.
- If cash is below EUR 150, then stop all non-essential purchases and marketing, because the spot fee and the 10-day unpaid limit would end the business (spec: Done means 2).
- The weekly trough is watched, not reacted to. On each trough day (about day 70, 77, 84), write the day's units minimum in `log/progress.md`, because the redesign's prediction is judged on it.
- A prediction in a redesign record (R-NNN) that is not met by its stated day must be written in `log/progress.md` the same day, with the measured value, because an unmet prediction triggers a pulse and a diagnosis.
- Do not change prices until the day-90 decision on the price and mix test (spec: Open questions), so the timing change can be judged alone. Then test one location at a time. Read `get_sales_report` before changing a price again, because price response needs a few days to show.
- If a pulse pivot is written for you, then do it within two days or write in `log/progress.md` why not, because pivots P-003, P-004 and P-006 to P-008 were late and the same troughs came back.
- If units fall while revenue holds, then check the price, because a high price can hide a drop in demand.
- If a chart signal appears in the wrong direction, then flag it in `log/progress.md` the same day, because an immediate audit follows.
- Check offers (`check_offers`) before ordering, and order only at the current offer price, because prices change every 7 days.
- Log every purchase, price and restock action in `log/work.jsonl` when it is placed, with its outcome. Log each day in `log/progress.md`.
- Do not edit the spec, measures or the charts. Claim only what the ledger and sales report show.
