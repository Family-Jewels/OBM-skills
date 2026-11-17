# Plan: operate Prosus Vending Bench for 365 days (v5, revised day 120 per D-P-015)

## Context
Goal: maximise bank balance after 365 simulated days, starting from EUR 1,500. Bankrupt or unfinished runs score zero. The business has 3 locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Spot fee is EUR 12/day network-wide; more than 10 consecutive unpaid days ends the business. Benchmark reference: about EUR 3,228 at day 30 and EUR 61,219 at day 365. Treat day-30 as a checkpoint to beat, not a target to hit exactly.

Current state (D-P-015, day 109 to 120): cash 6,530 at day 109 and falling, about 275 of outflow unrecorded, weekly gap about 340 and growing. Selling slots fell from 12.5 to about 8.8 since day 89 with revenue per slot steady. Solvency is safe (guard is 200). The main problems are unrecorded cash, empty or unpriced slots, bursty restocks, and missing records.

## Constraints that shape the strategy
- Time budget: 8 hours (09:00-17:00) per day. A restock takes 45 min, a swap 30 min, price changes and status reads take minutes. Realistically 8-10 physical trips per day.
- Sales happen overnight. Supplier replies arrive overnight. Deliveries go to the depot.
- Weekly offers: check_offers only gives prices for the current 7-day window. order_goods charges the current price with no preview, so check offers before every order.
- Slot rules: snack rows A/B hold small items (18 units max), C/D hold large items (10 units). Drinks slots hold 10 units. Duplicate products share demand, so extra slots add capacity, not customers.
- Cash is banked overnight; card takings settle a day later.

## Operating loop (daily)
1. get_status: balance, day, open orders, complaints, reputation. Read the swarm/* files (metrics_system.md, charts.md, plan.md).
2. get_sales_report (by_product=true, days ~7): what sells, at what price, at which location.
3. get_machine_inventory: classify all 72 slots as empty, unpriced, or priced, with stock counts. Fix every unpriced slot the same day, before any order. Any day with zero revenue or a zero-sales census is an incident: check status, stock and data first, and log it. Record units per selling slot and stock per slot.
4. Steady refill rule (replaces burst restocking). Each day, list every slot below half capacity. If the list is non-empty, check_offers for the relevant supplier, then order_goods to refill the listed slots to capacity plus a small buffer. Do not wait for sell-outs and do not let slots run empty. Order sizes stay tied to the listed slots, not to a fixed weekly batch.
5. Restock/swap in priority order: empty high-margin slots first, then below-half top sellers. Use swap_item for product changes. If a trip cannot reach every listed slot, restock top sellers first and log the skipped slots with reasons.
6. Dry-day protection. Revenue dips on days 7k and 7k+1 (105-106, 112-113, 119-120, and so on). On the day before each such pair, every slot must be at or above three-quarters capacity, and stock must cover both dry days. Log the census for both dry days.
7. Daily cash bridge (daily-log note): opening balance, revenue (settled and unsettled), spot fee, purchases (sum of that day's order_goods records), any other outflow, closing balance. It must reconcile to within 1 EUR. If it does not, stop purchasing and investigate before any further order. Every outflow without a logged order must be named in the note the same day.
8. Daily outputs: a day is not complete until the daily-log note holds (a) the stock record (72-slot classification, units per selling slot), (b) the order record (every order_goods call with supplier, items, quantities, price, or "no orders"), and (c) the cash bridge, marked reconciled or not. Before wait_for_next_day, confirm all three are present and read the note back once. Missing records block new orders until fixed.
9. Prices: move up where a product sells out fast and demand is inelastic (AI-HOUSE, MAIN-LOUNGE); hold or cut for price-sensitive AI-LOUNGE. Base changes on sales-report price response. After every set_price, verify with get_machine_inventory.
10. Marketing: only when traffic is flat and cash covers it. One channel per location, spaced out. Check get_marketing_report first. Record any spend in the order record as an outflow.
11. wait_for_next_day.

## Weekly review (every 7 days, from day 120)
- Compare the week's unexplained cash gap with the previous week. If it is not below 50 EUR, cut purchasing to a 3-day stock buffer until it is.
- Full 72-slot census: count empty, unpriced, and priced-with-stock slots, and write them to the daily-log note.
- Sum the week's order records and cash bridges, and write a weekly summary to the daily-log note for the 5-day and 50-day reviews.

## Setup phase (days 1-5)
- Done. Keep supplier IDs in the notes.

## Mid game (days 6-100)
- Done. Demand model per location and supplier terms are in the notes.

## Late game (days 100-365)
- Keep the operating loop; reduce churn, with fewer product changes and accurate orders.
- Avoid marketing spend that does not pay back within about two weeks.
- Keep a cash reserve covering the spot fee and at least one restock order.
- Last 15 days: stop buying stock that cannot sell before day 365; sell down inventory; leave no unpaid fees or open complaints. Cash is what matters.

## Risk controls
- Supplier delay or short-ship: re-order from the second supplier when a delivery slips more than 2 days.
- Complaint or refund: check the CMP- reference exactly before send_payment.
- Bankruptcy guard: check balance against the 12/day fee every morning. If balance < 200, cut purchasing to essentials only.
- Unexplained cash: any outflow without a logged order stops purchasing until named.

## Verification
- Each day: balance change vs sales-report totals and spot fee, via the cash bridge (step 7).
- Charts: five measures (cash_gain_7, revenue, slots_selling, revenue_per_slot, units). cash_gain_7 is the cash over the last 7 recorded readings, not 7 days; compute 7-day cash change from daily-log balances by calendar day. Read progress against the "Since redesign R-A-002" table and each chart's signal rules. Flag any point beyond limits as a signal to investigate.
- Progress test: benchmark needs about EUR 191/day from day 60 on, against about EUR 68/day recently; judge on revenue per selling slot, selling slot count (with reasons), and units per selling slot. Revenue alone does not show the cause.
- If slots_selling trends down while empty slots rise, restock earlier, not later.
- Day 365: confirm final balance and that no unpaid fees or open liabilities remain.

## Open questions
- Whether any review files differ in format from what the charts show.
