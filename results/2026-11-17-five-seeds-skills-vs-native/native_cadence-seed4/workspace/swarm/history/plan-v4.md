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
3. get_machine_inventory: classify every one of the 72 slots each day as empty, unpriced, or priced, with its stock count. Record the counts in the daily-log note. Unpriced stock sells nothing, so fix those first. Empty slots count against revenue on every day they stay empty. Also record units sold per selling slot (units sold / slots with stock and a price) and stock per slot. Track these, not the raw count of selling slots: a higher slot count with thin stock earns less. Selling slots have fallen from about 15.5 to about 12 since day 52 while revenue per selling slot is unchanged, so the cause is which slots stop selling. Do not assume thin stock: for each non-selling slot, record whether it is empty, unpriced, or priced with stock. Only empty slots call for restocking; priced slots with stock call for a check of price and demand, not a refill.
4. Procurement is triggered by slot depletion, not by a fixed weekly cycle. When a slot's stock falls below about half its capacity (raised from a third, because top slots sell about 5 units a day and a slot at a third runs dry within a day or two), or a product sells out, check_offers for the relevant supplier and order_goods for what the depleted slots need to refill to capacity, plus a small buffer. Check offers before every order. Keep order sizes to what slots can hold plus a small buffer to avoid tying up cash in depot stock.
5. Restock/swap in priority order: empty high-margin slots first, then low-stock top sellers. Time restocks to when slots are running low, so that stock is not bunched into bursts with dry gaps between them. Use swap_item when changing product (30 min vs 45 min + clear). If a restock trip cannot reach every slot below half capacity, restock the top sellers first and log the slots skipped.
5a. Daily cash bridge, written to the daily-log note: opening balance, revenue (sales report, settled and unsettled), spot fee, purchases (the sum of that day's order_goods records), closing balance. The bridge must reconcile to the balance; if it does not, investigate before the next day's orders. Also reconcile over each 7-day window: about 740 of cash went out over days 60-76 that no record explained, so any outflow not matched by a logged order must be named and written down.
5b. Checked daily outputs. A day is not complete until three records are written to the daily-log note: (a) the stock record (per-slot counts and the 72-slot classification from step 3, with units per selling slot), (b) the order record (every order_goods call with its supplier, items, quantities, and price, or "no orders"), and (c) the cash bridge from step 5a, marked reconciled or not. Before wait_for_next_day, check that all three exist for the day and that the bridge reconciles. Missing or unreconciled records are an open issue to fix first.
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
- After each day: compare balance change with sales-report totals and the spot fee, using the cash bridge in step 5a.
- Charts: there are five measures (cash_gain_7, revenue, slots_selling, revenue_per_slot, units). Do not assume cash_gain_7 is a 7-day change; D-P-001 found it equals cash(t) minus cash(t-9) at day 12. Check the definition before reading it. D-P-007 found the chart limits are pre-redesign and overlap in places, so read progress against the "Since redesign R-P-001" table and the charts' own signal rules, not the headline table alone. Flag any point beyond the pre-redesign limits (for example the day-30 revenue point) as a signal to investigate, not as routine variation.
- Cash_gain_7 is the cash over the last 7 recorded readings, not 7 days, and missing rows stretch it. Compute 7-day cash change from the daily-log balances by calendar day instead.
- Weekly low: revenue on days 7k and 7k+1 (e.g. 42-43, 49-50, 70-71) averaged about 45, against about 150 on other days. Days 77-78 are the next pair. Log for each of those days the offers checked, orders placed, restock trips, and the slot census. Do not move the restock schedule until days 77-78 are read.
- Days 77 and 78, before sales: take the full 72-slot census (empty / unpriced / priced, with stock) and save it to the daily-log note, then check whether revenue on those days is low again.
- Progress test: the benchmark needs about EUR 191/day from day 60 onward, against about EUR 68/day recently; PIP is about 2.7. Judge progress on revenue per selling slot, selling slot count (with the reason for each non-selling slot), and units per selling slot. Revenue alone does not show whether stock, price, or footfall is the cause.
- Records: after writing the three daily records (step 5b), read the daily-log note back once to confirm they are stored there. If they are stored elsewhere, say so in the daily-log note so the system can find them.
- Slot count: if slots_selling trends down while empty slots rise, restock earlier, not later.
- Check swarm/metrics_system.md and swarm/charts.md each day for drift from the plan.
- At day 30: compare balance to the benchmark (about EUR 3,228). If behind, review pricing, stock-outs, and marketing use.
- At day 365: confirm final balance and that no unpaid fees or open liabilities remain.

## Open questions (to resolve once live state is readable)
- Current inventory, prices, and whether any slots are unpriced.
- Which suppliers exist and their weekly offer cycle.
- Whether the swarm review files are present and what format they take.
