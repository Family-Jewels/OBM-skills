# Match a stock order to the loading time it needs
Applies when: O2
Revises: G-007
What good looks like: When stock is already waiting in the depot, a strong period loads that stock into the machines before it places a large new order, and sizes the order to what the coming days' worker time can load. Before ordering, it reads the depot count and the number of empty slots together, as the clearing example above does. A delivery that lands while the depot is full can then be placed over the following days rather than left in storage.
Why: PO-1014 delivered 322 units on day 43, when the depot held 15. The depot stood at 332 on day 44 and 216 on day 45, beyond the chart's upper limit of 164.9 (swarm/charts.md; swarm/ground_truth/latest.md). Capacity used was 2%, 6% and 0% on days 41 to 43 (swarm/charts.md). Revenue over the last 7 days fell from 672 on day 30 to 328 on day 45 (swarm/metrics_system.md).
Source: pulse P-005
Revisit: day 60

Fact check: C-006 refuted at day 63 (All ground-truth figures match (PO-1014 322 units delivered day 43 with 15 in depot; storage 332 day 44, 216 day 45; capacity 2/6/0% days 41–43; revenue_last_7 672 day 30 to 328 day 45), but the 164.9 upper limit is not in ground truth and recomputed XmR limits are 181 (days 2–43) or 206 (days 2–59).)
