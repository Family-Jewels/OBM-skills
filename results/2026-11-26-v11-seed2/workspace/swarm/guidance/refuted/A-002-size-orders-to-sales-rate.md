# Size the next order to the sales rate of the stocked slots
Applies when: O2
Revises: G-003
What good looks like: Before it places an order, a strong period divides the depot count by what its stocked slots have sold per day over the last few weeks (the sales report gives both figures). That gives the days of stock already held. An order sized to a few days of that rate keeps the depot close to what the machines can sell. For example, 259 units in the depot against about 30 units sold a day is roughly eight days of stock; a strong period in that position loads what it holds onto the empty slots, then orders for the days ahead.
Why: On day 60 the depot held 259 units (swarm/charts.md; swarm/ground_truth/day-0060.md). Orders PO-1013 to PO-1017 delivered about 870 units in days 51 to 59 by order line, while the stocked slots sold 619 units over days 41 to 60. The depot rose from 15 units on day 41 to 259 on day 60, beyond the chart's upper limit of 222.5. At paid unit costs the 259 units are about EUR 198 of cash not yet earning. G-003 already names this problem; this example gives the sales-rate reference that the advice leaves out.
Source: audit A-002
Revisit: day 90

Fact check: C-007 refuted at day 94 (the claim that PO-1013 to PO-1017 delivered about 870 units in days 51 to 59 is false; days 51 to 59 saw 445 units delivered (PO-1013 day 51, PO-1017 day 58, PO-1016 day 59). The 867 figure is the five orders combined, including PO-1014 (day 43) and PO-1015 (day 49).)
