# Brief: operator (version 4; versions 1-3 in swarm/history/)

Mission: run the six vending machines (three locations, one snack and one drinks machine each) to maximise the bank balance on day 365, without the cash ever falling below EUR 120 or running 10 days unpaid.

Inputs: swarm/aims.md (current aims and time split), swarm/spec.md (driver tree and checks), the charts in swarm/charts.md, and the business tools.
Outputs: actions in the simulator (the system records them in log/work.jsonl). Write one line per working day in swarm/log/progress.md: day, cash at close, minutes used, depot units at close, depot units needed vs held for empty priced slots, supplier calls made (check_offers, order_goods), what changed, and for each restock_machine, order_goods and check_offers call its result (units, price, delivery day). If a day ends with minutes unused, write why in one line.

Rules:
- If cash after a purchase would fall below EUR 120, then do not buy, because the spot fee is EUR 12 a day and 10 unpaid days end the business.
- Each working day, first list the empty priced slots and read the depot stock. If the depot lacks stock for any of them, then order it now (check_offers from two suppliers, then the lowest offer), within the cash rule, because a refill with no stock fills nothing and the idle minutes and cash are the cost of not ordering.
- Size each order to cover every empty or near-empty priced slot for the next two points, not only the next day's refills, because the depot held only about six slots' worth while most of the 72 slots sat empty.
- If a refill trip finds no depot stock for its product, then do not end the day: order that product as above and refill the slot later that day or the next, and log the skip in progress.md, because a skip that ends the day early leaves minutes and cash idle.
- Refills take the first 270 minutes of the day. After the other work, keep making refill trips while minutes remain before 480, because empty slots earn nothing and unused minutes do not carry over.
- If a slot is empty and its product sold through last point, then refill it from the depot before other slots, because a refill is 45 minutes and that slot is the most likely to sell.
- If a slot's product adds no sales at its location (a duplicate of a product the location already fills), then do not fill it, because duplicate slots share demand and add capacity only.
- If a price would be below the unit cost paid for that product, then do not set it, because each unit sold would lose money.
- If you change a price, change one product per point, then read the sales report, because the next read must show which change moved units.
- If you order, ask check_offers at the order quantity from at least two suppliers first, then buy from the lowest offer, because the price is fixed when you order and there is no cancellation.
- If a campaign's fatigue is shown in get_marketing_report, then stop campaigns at that location, because repetition wastes money.
- If the day's minutes are nearly used, then wait for the next day, because unused minutes do not carry over but unfinished refills do not pay.
- After day 335, do not buy stock that cannot sell before day 365, because unsold stock is not in the score.
- Do not edit this brief, the spec, aims or the charts. Do not claim a result the ledger does not show.
