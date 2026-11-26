# Load landed stock at the start of the next period
Applies when: O2
What good looks like: When stock lands late in a period, a strong period reads the depot count and the empty slots first in the next period, and loads what the depot already holds before it buys more. Units earn only once they are in a machine, so the first fills of the next period are often the highest-return minutes of the day.
Why: On days 20 to 22 the machines were empty while the depot grew: 6 units on day 21, then 116 on day 22 with every machine at zero (swarm/ground_truth/day-0022.md). Units in storage reached 210 on day 23 (swarm/metrics_system.md). Once 10 slots were loaded on days 23 and 24, revenue reached €207 on day 24 (swarm/ground_truth/day-0024.md). This extends P-002 and G-003 to the start of a period.
Source: pulse P-003
Revisit: day 40

Fact check: C-003 refuted at day 39 (Its claims that the machines were empty on days 20 to 22 and that 10 slots were loaded on days 23 and 24 contradict the ground truth; the advice wording itself is not the problem.)
