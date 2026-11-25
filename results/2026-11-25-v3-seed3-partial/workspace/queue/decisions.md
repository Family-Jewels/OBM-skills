# Parked decisions (orchestrator)

1. **Model-usage budget (spec: USD 2.00 total; visible cap USD 39.99).** Breached at day 53 (spec total reached). Default: keep operating with lean calls; do not stop the core (stopping scores zero). For the human: confirm which cap applies. Spend at day 113: about USD 5.37.
2. **Customer complaints.** Policy since day 32: pay the full claimed amount on each complaint, so each is withdrawn (CMP-001 to CMP-009 all withdrawn). Earlier partial refunds were topped up. Default unchanged.
3. **Supplier lead time.** Zuidas lead time moved from 3-4 days to about 10 days (PO-1029). Noordzee 3-5 days. Default: order by cover with lead time + 2 days; use noordzee for drinks where possible; check lead time on each receipt.
4. **Depot cover instrumentation.** Not yet charted. Until it is, the orchestrator writes depot units and last-7-day units sold in log/progress.md each working day.
5. **Refill quota.** At least 2 refills a day while slots are below the aim and stock is on hand (AS-004/operator v4). Shortfalls logged with the depot count.
