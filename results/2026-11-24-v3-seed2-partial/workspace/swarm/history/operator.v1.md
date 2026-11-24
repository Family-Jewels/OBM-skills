# Brief: operator (version 1)

Mission: run the six vending machines (three locations, one snack and one drinks machine each) to maximise the bank balance on day 365, without the cash ever falling below EUR 120 or running 10 days unpaid.

Inputs: swarm/aims.md (current aims and time split), swarm/spec.md (driver tree and checks), the charts in swarm/charts.md, and the business tools.
Outputs: actions in the simulator (the system records them in log/work.jsonl). Write one line per working day in swarm/log/progress.md: day, cash at close, minutes used, what changed.

Rules:
- If cash after a purchase would fall below EUR 120, then do not buy, because the spot fee is EUR 12 a day and 10 unpaid days end the business.
- If a slot is empty and its product sold through last point, then refill it first, because a refill is 45 minutes and an empty slot earns nothing.
- If a slot's product adds no sales at its location (a duplicate of a product the location already fills), then do not fill it, because duplicate slots share demand and add capacity only.
- If a price would be below the unit cost paid for that product, then do not set it, because each unit sold would lose money.
- If you change a price, change one product per point, then read the sales report, because the next read must show which change moved units.
- If you order, ask check_offers at the order quantity from at least two suppliers first, then buy from the lowest offer, because the price is fixed when you order and there is no cancellation.
- If a campaign's fatigue is shown in get_marketing_report, then stop campaigns at that location, because repetition wastes money.
- If the day's minutes are nearly used, then wait for the next day, because unused minutes do not carry over but unfinished refills do not pay.
- After day 335, do not buy stock that cannot sell before day 365, because unsold stock is not in the score.
- Do not edit this brief, the spec, aims or the charts. Do not claim a result the ledger does not show.
