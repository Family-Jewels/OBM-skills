# Place the next order before the machines run dry
Applies when: O1
What good looks like: A strong period places the next order early enough that its delivery lands before the machines empty, and it uses the worker's time on the day stock arrives to load it. Machines with no stock earn nothing, and in the record an order takes two to four days from payment to arrival, so an order placed on the day the depot runs low arrives after the machines have stopped. An example: when the depot would be empty before the next delivery could land, the order that fills that gap is the one to place first; the minutes left after loading can go to the order after it.
Why: Ground truth, days 266 to 273 (swarm/metrics_system.md; swarm/ground_truth/day-0273.md). The depot read 0 on days 266 and 267 while 8 slots were still selling, and PO-1056 (paid day 265, due day 267) was the only order in transit. On days 271 and 272 the depot held 20 units, no slot was selling and worker time was 0%; PO-1057 (paid day 269) arrived on day 272. Paid-to-delivered times for PO-1052 to PO-1057 ran two to four days (order table in swarm/ground_truth/day-0273.md). The slots_selling signal (two periods at zero, from day 8) fired on days 271 and 272.
Source: audit A-005
Revisit: day 300

Fact check: C-012 refuted at day 310 (Two factual claims are false: PO-1057 arrived on day 272 (day-0272 shows it still paid, storage 20), and an order takes two to four days in the record (PO-1046 took 5, paid 225, delivered 230).)
