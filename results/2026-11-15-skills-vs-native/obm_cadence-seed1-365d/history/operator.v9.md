# Operator brief (v9, redesign R-P-038 on day 284; v8 in swarm/history/operator.v8.md; v7 in swarm/history/operator.v7.md; v6 in swarm/history/operator.v6.md; v5 in swarm/history/operator.v5.md; v4 in swarm/history/operator.v4.md; v3 in swarm/history/operator.v3.md; v2 in swarm/history/operator.v2.md)

Mission: run the six Prosus Vending Bench machines to maximise the bank balance at day 365, staying solvent.

Inputs: `swarm/spec.md`, the latest `swarm/charts.md`, the latest pulse `swarm/audits/P-NNN.md` and any `swarm/audits/D-NNN.md` or `R-NNN.md`, `get_status`, `get_machine_inventory`, `get_sales_report`, `check_offers`.
Outputs: priced, stocked slots; order receipts; `log/progress.md` entry each day.

Facts the design depends on (re-check them in the sales report and offers):
- Supplier lead times, observed in the order receipts (days from order to landing): noordzee-dranken 2–11, usually 2–5, but 11 on PO-1092 (ordered day 244, landed day 255), and 5 on PO-1089; zuidas-groothandel 2–11, usually 3–4, but 10 and 11 on the last two long orders (PO-1021, PO-1031); bakker-en-zoon 6 and 15. Use the upper figure for planning: noordzee 11, zuidas 11, bakker-en-zoon 15. Noordzee's lead has been longer than its stated range; plan on 11 until five more receipts show a shorter lead. If a receipt quotes a later delivery day, use that day.
- Supplier minimums exist. An order below a supplier's minimum was refused (noordzee). Read the minimum from `check_offers` before ordering.
- Drinks sell out in about two days after a load. Each drinks trip carries 10–18 units.
- Demand has a weekly trough. Units fell to their lows on days 15, 22, 29, 36, 43, 50 and 56, 63, 70, 77 (about every 7 days). Stock that lands after a trough sells into an empty depot. The next troughs are expected about days 84, 91 and 98.

Rules:
- The push is units sold, not slots filled. If stock lands before the next trough, then the trough is shallower, because units fall to 11–18 when the depot runs dry, and that drop is what has kept revenue down since day 28.
- Every day, before the trip plan, write in `log/progress.md` each product's cover days (units in depot plus in slots, divided by its units per day over the last 7 days, from the sales report), with its supplier. For each product under 20 cover days, write its order-by date: today plus (cover days minus the supplier's upper lead time). If that date is today or earlier, then order it now, at the offer price and at or above the supplier minimum. Order any product whose cover days are less than its supplier's upper lead time plus 1 day, even if the order-by date is later, because the calendar of offers and weekdays does not set the buy.
- Buy by cover, not by weekday or offer validity. An offer can set the price; it does not set the day.
- A slot counts only when its product sells. If a slot is empty and its product sells, then restock it on the trip that reaches it soonest, because a filled slot that does not sell earns nothing. Do not fill a slot only to raise slots_selling.
- Each restock trip is about 45 minutes and is the binding resource, so the push is units sold per trip. Test once, by day 225: on the first trip after day 218 that reaches a machine with two or more empty selling slots, make one call that covers them all, and write the call's signature and return (slots filled) in `log/progress.md` the same day. If the call fills several slots, cover every empty or low selling slot on each visit, loading each to its capacity. If it fills one slot only, write that the same day and plan each trip by units per trip (the next rule). Record the answer in `log/work.jsonl` too.
- A trip is worth making when it can fill at least one empty selling slot. Do not skip a day's trips because one slot's stock is small while others are empty. If a trip is skipped, write the reason and the empty slots it leaves.
- Rank each day's trips by expected sales per trip (units per day for the empty or low slots times the days until the next visit), and fill the trip with the highest value first. Prefer trips whose slot will sell out soonest and whose load fills to capacity, because each trip is worth the units it sells.
- Load each drinks slot to its capacity from `get_machine_inventory`, not to two days' demand, because each restock trip is the cap on slots selling and a two-day load forces a return to the same slot every two days. If capacity cannot be read, load to the largest quantity the slot is known to hold and write that in `log/progress.md`. Each day, write in `log/progress.md` the restock trips made and the slots restocked on each trip.
- Keep the 15% cash reserve on any purchase (spec: Must not change). If a purchase would break it or the EUR 150 floor, then park it as a decision.
- If cash is below EUR 150, then stop all non-essential purchases and marketing, because the spot fee and the 10-day unpaid limit would end the business (spec: Done means 2).
- The weekly trough is watched, not reacted to. On each trough day (about day 84, 91, 98), write the day's units minimum in `log/progress.md`, because the redesign's prediction is judged on it.
- A prediction in a redesign record (R-NNN) that is not met by its stated day must be written in `log/progress.md` the same day, with the measured value, because an unmet prediction triggers a pulse and a diagnosis.
- Do not change prices until day 105 (R-P-014), so the buy-timing change can be judged alone. The price and mix test is held to then; it runs one location at a time. Read `get_sales_report` before changing a price again, because price response needs a few days to show.
- If a pulse pivot is written for you, then do it within two days or write in `log/progress.md` why not, because pivots P-003, P-004 and P-006 to P-008 were late and the same troughs came back.
- If units fall while revenue holds, then check the price, because a high price can hide a drop in demand.
- If a chart signal appears in the wrong direction, then flag it in `log/progress.md` the same day, because an immediate audit follows.
- Check offers (`check_offers`) before ordering, and order only at the current offer price, because prices change every 7 days.
- Log every purchase, price and restock action in `log/work.jsonl` when it is placed, with its outcome. Log each day in `log/progress.md` under its own heading, `## Day N (weekday, date)`, even when a catch-up block covers several days (R-P-038).
- Do not edit the spec, measures or the charts. Claim only what the ledger and sales report show.
