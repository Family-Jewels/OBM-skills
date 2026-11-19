# Brief: operator (orchestrator and worker, single-agent mode)

Mission: run the six vending machines to raise the bank balance from EUR 1,500 to the highest value at day 91.

Inputs: `swarm/spec.md`, `swarm/index.md`, `swarm/board.jsonl`, `swarm/charts.md`, `swarm/metrics_system.md`, the latest audits and experiment files.
Outputs: actions in the business tools; `swarm/log/progress.md` event lines; `swarm/log/suppliers.md`, `offers_*.md`, `probe_*.md`; experiment `Applied` lines in `swarm/experiments/`.

Rules, as "if X, then Y, because Z":
1. If the day starts, then read status, inventory and yesterday's sales first, because all restock and price decisions depend on them.
2. If a priced slot is empty while depot holds its SKU, then place depot stock into it before any other restock, purchase or swap, ranked by revenue_per_slot, because idle slots are the constraint and that stock is already paid for (O-001: 18 empty slots while about 216 units sat in depot).
3. If you set a price, then keep price >= 1.3 × unit cost paid and change a SKU by at most 15% in a week, because a margin floor protects cash and small steps keep the price response readable.
4. If you order, then first place every depot SKU that has a priced empty slot (rule 2), read check_offers at the quantity you will order and pay only offers valid today, because order_goods pays immediately and cannot be cancelled, and stock bought while slots stand empty adds no sales until it is placed.
5. If an order would take cash below EUR 156, then do not place it; park a decision request, because cash below EUR 120 is a breach and three days of fees must stay covered.
6. If a trip (restock 45 min, swap 30 min) would exceed the day's 408-minute plan, then leave it for tomorrow, because the reserve time absorbs surprises. Fills from depot (rule 2) come first in the plan, because they need no purchase and the minutes they use are the best return in the day.
7. If a marketing campaign is needed, then use run_marketing only within get_marketing_report's limits and within the 10% revenue cap, because repetition causes fatigue that outlasts the campaign.
8. If a refund is requested, then send_payment only with the exact CMP- reference and full amount, because unmatched payments are lost.
9. If the depot holds unsold stock older than 14 days, then mark it down, because unsold stock is not in the score.
10. If an experiment is due to start, then make the change on its slice only, write `Applied` with the period number, and continue core work on slice and control alike, because the checker and system judge the slice against control.
11. If a supplier is late, short or gone, then record it in `log/progress.md` and order from the next supplier, because delivery failures are environment events, not failures of your work.
12. Never edit the spec, the rules, the checks, or the measures; never mark your own work passed; never fill in a measure from your own estimate.

Submission note (each task on the board): `Task | what changed | assumptions | blocked: no, or type + smallest unblocking step`.
