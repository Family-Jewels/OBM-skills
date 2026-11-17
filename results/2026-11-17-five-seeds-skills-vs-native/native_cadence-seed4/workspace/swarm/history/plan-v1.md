# Plan: operate Prosus Vending Bench for 365 days

## Context
Goal: maximise bank balance after 365 simulated days, starting from EUR 1,500. Bankrupt or unfinished runs score zero. The business has 3 locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Spot fee is EUR 12/day network-wide; more than 10 consecutive unpaid days ends the business. Benchmark reference: about EUR 3,228 at day 30 and EUR 61,219 at day 365. Treat day-30 as a checkpoint to beat, not a target to hit exactly.

I could not read live state in plan mode (vending tools are blocked), so the first operating step is to read it. This plan is written from the briefing alone.

## Constraints that shape the strategy
- Time budget: 8 hours (09:00-17:00) per day. A restock takes 45 min, a swap 30 min, price changes and status reads take minutes. Realistically 8-10 physical trips per day, so restock in large batches and avoid churn.
- Sales happen overnight. Supplier replies arrive overnight. Deliveries go to the depot.
- Weekly offers: check_offers only gives prices for the current 7-day window. order_goods charges the current price with no preview, so check offers before every order.
- Slot rules: snack rows A/B hold small items (18 units max), C/D hold large items (10 units). Drinks slots hold 10 units. Duplicate products share demand, so extra slots add capacity, not customers. Do not fill many slots with the same product unless capacity is the bottleneck.
- Cash is banked overnight; card takings settle a day later. Keep cash flowing; watch the balance against the spot fee.

## Operating loop (daily)
1. get_status: balance, day, open orders, complaints, reputation. Read the morning briefing and swarm/* files the system writes (metrics_system.md, charts.md, plan.md). Follow the current swarm/plan.md.
2. get_sales_report (by_product=true, days ~7) to see what sells, at what price, and at which location. Compare with stock levels.
3. get_machine_inventory: find empty or low slots and slots with no price (unpriced stock sells nothing).
4. Procurement, once per week (or when a supplier is low): check_offers for each supplier on the relevant product list, then order_goods for the best-value items. Keep order sizes to what slots can hold plus a small buffer to avoid tying up cash in depot stock.
5. Restock/swap in priority order: empty high-margin slots first, then low-stock top sellers. Use swap_item when changing product (30 min vs 45 min + clear).
6. Prices: move slightly up when a product sells out fast and demand is inelastic (AI-HOUSE, MAIN-LOUNGE); hold or move down for price-sensitive AI-LOUNGE picky customers. Adjust based on sales-report price response, not guesses.
7. Marketing: only when a location's traffic is flat and cash can cover it. Use run_marketing moderately (one channel per location, spaced out) to avoid fatigue. Check get_marketing_report first for costs and limits. Stop if campaign cost exceeds expected margin over the next week.
8. Write a short note each day (write_note key "daily-log") with balance, actions, and any open issues. Set reminders for: weekly offer renewal, supplier replies expected, spot fee checks.
9. wait_for_next_day.

## Setup phase (days 1-5)
- Read status, machine inventory, storage, marketing report, and notes.
- search_web for wholesalers: one snack supplier (savoury preference at AI-LOUNGE; coffee and drinks), one drinks supplier. Email for catalogue and terms; ask for volume discounts. Record supplier IDs in a note.
- Initial stock: fill all 6 machines with a diversified mix, preferring high-margin savoury snacks and coffee/drinks for AI-LOUNGE. Price at a modest markup and let the sales report guide later changes.
- Confirm the EUR 12/day spot fee is covered from sales each day. Never let the balance fall into a state that risks 10 unpaid days.

## Mid game (days 6-100)
- Build a demand model per location: which products sell, at what price, and how footfall changes by day of week and season (sales report weather/seasonal hints).
- Shift shelf space toward top margin-per-slot products. Drop any product with sustained near-zero sales.
- Negotiate better terms with suppliers when the volume grows. Use email for structured requests; use order_goods for actual purchases.
- Use the 5-day short review and 50-day full review: when the system asks, diagnose what is wrong (stock-outs, price errors, unpriced slots, complaints, cash leakage) and revise this plan.

## Late game (days 100-365)
- Keep the operating loop, but reduce churn: fewer product changes, larger but accurate orders.
- Avoid marketing spend that does not pay back within about two weeks.
- Keep a cash reserve large enough to cover the spot fee and at least one restock order.
- Last 15 days: stop buying stock that cannot sell before day 365; sell down inventory; do not leave unpaid fees or open complaints. Inventory is not part of the score, so cash is what matters.

## Risk controls
- Supplier delay or short-ship: keep a second supplier identified; re-order from the alternative when a delivery slips more than 2 days.
- Complaint or refund: check the CMP- reference exactly before send_payment; payments with mismatched references are lost.
- Bankruptcy guard: check balance against the 12/day fee every morning. If balance < 200, cut purchasing to essentials only.
- Price errors: after every set_price, verify with get_machine_inventory.

## Verification
- After each day: compare balance change with sales-report totals and the spot fee.
- Check swarm/metrics_system.md and swarm/charts.md each day for drift from the plan.
- At day 30: compare balance to the benchmark (about EUR 3,228). If behind, review pricing, stock-outs, and marketing use.
- At day 365: confirm final balance and that no unpaid fees or open liabilities remain.

## Open questions (to resolve once live state is readable)
- Current inventory, prices, and whether any slots are unpriced.
- Which suppliers exist and their weekly offer cycle.
- Whether the swarm review files are present and what format they take.
