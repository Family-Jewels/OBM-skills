# Plan: operate Prosus Vending Bench for 365 days (v9, revised day 313 per D-P-029)

## Context
Goal: maximise bank balance after 365 simulated days, starting from EUR 1,500. Bankrupt or unfinished runs score zero. The business has 3 locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Spot fee is EUR 12/day network-wide; more than 10 consecutive unpaid days ends the business. Benchmark reference: about EUR 3,228 at day 30 and EUR 61,219 at day 365. Treat day-30 as a checkpoint to beat, not a target to hit exactly.

Current state (D-A-006, day 206; charts at day 216): revenue has collapsed (about 39 a day over days 189-206, down 79% in 7 days). Selling slots have stayed at 2-10 since day 135 (7 at day 206) against 13-19 before. Days 201-204 had zero sales while cash fell by the spot fee only. Non-fee outflow of about 0.8 per unit sold has no order records. Cash 10,543 at day 216, solvency safe (about 850 days of fee). Working diagnosis: stock is not reaching priced, selling slots, and purchasing continued without records. Slot-level cause not yet confirmed: no 72-slot census exists.

## Revision v9 (day 313): what changed and why
Diagnosis D-P-029: the v8 freeze did not stop the leak. Cash over days 279-313 still runs 340-410 below the sales-based figure, and revenue fell from 525 (day 302) to 262 (day 313). Selling slots have been mostly 3-9 since day 296. The plan's phase was dated day 228, but charts.md has measured the redesign phase since day 292, so the chart limits in v8 were wrong. The benchmark pace (about 950/day from day 313) is no longer a planning target; the plan now targets the measured gap. v9 changes:
- Phase fixed to day 292. Judge slots_selling against its current-phase centre (5.2, limits -0.96 to 11.36), not 3.4.
- Freeze is checked daily, not assumed: any order_goods record dated after day 278 is logged in the daily note with its cash effect. If the day's bridge gap exceeds 1 EUR, purchasing stays frozen regardless of other gates.
- The freeze items (a)-(d) are the first work of each day until all are written. The 72-slot census is saved under swarm/ as a dated file before any other action.
- Name the day-247 (-230) and day-261 (-214) outflows from records, or mark them unknown with the EUR amount.
- Any day with the bridge unreconciled stops all purchasing, including the step 5 exception.

## Revision v8 (day 278): what changed and why
Diagnosis D-P-027: cash is nearly flat (+73 over days 230-254), about 350-450 of unnamed outflow over those days (1.0-1.3 per unit sold, gate 1.0; one drop of about -230 on day 247), and selling slots fell from 16 to 0-10. The v7 gates needed census and cash-bridge records that were never written, so they never closed and orders kept going. The charts also missed a signal: slots_selling sat above its post-redesign centre (3.4) for 8 readings (days 237-244), because charts.md judged it against pre-redesign limits. v8 freezes orders until the records exist, and fixes the chart comparison in the signal rules.

## Revision v7 (day 216): what changed and why
Purchasing ran ahead of evidence. The gates in steps 4, 5 and 10 existed but were not enforced, so orders kept going with no census and no records. v7 makes the census and records a precondition for ordering, not a logging duty after it.

## Constraints that shape the strategy
- Time budget: 8 hours (09:00-17:00) per day. A restock takes 45 min, a swap 30 min, price changes and status reads take minutes. Realistically 8-10 physical trips per day.
- Sales happen overnight. Supplier replies arrive overnight. Deliveries go to the depot.
- Weekly offers: check_offers only gives prices for the current 7-day window. order_goods charges the current price with no preview, so check offers before every order.
- Slot rules: snack rows A/B hold small items (18 units max), C/D hold large items (10 units). Drinks slots hold 10 units. Duplicate products share demand, so extra slots add capacity, not customers.
- Cash is banked overnight; card takings settle a day later.

## Operating loop (daily)
1. get_status: balance, day, open orders, complaints, reputation. Read the swarm/* files (metrics_system.md, charts.md, plan.md).
2. get_sales_report (by_product=true, days ~7): what sells, at what price, at which location.
3. get_machine_inventory: classify all 72 slots as empty, unpriced, or priced-with-stock, with stock counts. Fix every unpriced slot the same day, before any order. Any day with zero revenue or a zero-sales census is an incident: check status, stock and data first, and log it. Record units per selling slot and stock per slot.
4. Restock-landing check (new). Every slot restocked in the last 2 days must be priced-with-stock in today's census. Any restocked slot that is empty or unpriced is a stop-order incident: fix it (set_price, or swap_item if the product is wrong) before any order_goods call. Log the slot IDs checked.
5. Order gate (closed by default; frozen from day 278, see Freeze). Before any order_goods call, all of the following must be true today, and each must be written in the daily-log note first: (i) the 72-slot census in step 3 is complete; (ii) the restock-landing check in step 4 passed; (iii) the cash bridge for the previous day reconciled within 1 EUR; (iv) purchases per unit sold over the last 7 days is 1.0 or below, computed from the order and sales records. If any item is missing or false, place no order. The only exception is filling empty high-margin slots that today's census confirms as priced. Record the ratio in the order record.
6. Steady refill rule (suspended during the freeze). Each day, list every slot below half capacity that the census confirms as priced and has sold in the last 7 days. If the list is non-empty and the order gate is open, check_offers for the relevant supplier, then order_goods to refill the listed slots to capacity plus a small buffer. Do not refill empty, unpriced, or non-selling slots; fix or log them first. Do not wait for sell-outs and do not let confirmed selling slots run empty. Order sizes stay tied to the listed slots, not to a fixed weekly batch.
6a. Delivery trace (new). Each delivery is traced to slot IDs in the next day's census. Any delivered product not found in a priced slot after 2 days is untraced stock: it blocks orders until located, and the location is logged.
7. Restock/swap in priority order: empty high-margin slots first, then below-half top sellers. Use swap_item for product changes. If a trip cannot reach every listed slot, restock top sellers first and log the skipped slots with reasons. Check each restocked slot's price on the same trip with get_machine_inventory.
8. Dry-day protection. Revenue dips on days 7k and 7k+1 (105-106, 112-113, 119-120, and so on). On the day before each such pair, every slot must be at or above three-quarters capacity, and stock must cover both dry days. Log the census for both dry days. Do not use dry-day protection as a reason to place orders the order gate has closed.
9. Daily cash bridge (daily-log note): opening balance, revenue (settled and unsettled), spot fee, purchases (sum of that day's order_goods records), any other outflow, closing balance. It must reconcile to within 1 EUR. If it does not, stop purchasing and investigate before any further order. Every outflow without a logged order must be named in the note the same day.
10. Daily outputs: a day is not complete until the daily-log note holds (a) the stock record (72-slot classification, units per selling slot, restock-landing check), (b) the order record (every order_goods call with supplier, items, quantities, price, purchases-per-unit ratio, or "no orders"), and (c) the cash bridge, marked reconciled or not. Before wait_for_next_day, confirm all three are present and read the note back once. Missing records block all orders that day and the next, until fixed. Write the records before ordering, not after.
11. Prices: move up where a product sells out fast and demand is inelastic (AI-HOUSE, MAIN-LOUNGE); hold or cut for price-sensitive AI-LOUNGE. Base changes on sales-report price response. After every set_price, verify with get_machine_inventory.
12. Marketing: only when traffic is flat and cash covers it. One channel per location, spaced out. Check get_marketing_report first. Record any spend in the order record as an outflow. Do not spend on marketing while the order gate is closed, during the freeze, or while the restock-landing check failed.
13. wait_for_next_day.

## Freeze (from day 278, D-P-027)
- No order_goods calls, no marketing spend, and no steady refill (step 6) until all four are true and written to the daily-log note:
  (a) a full 72-slot census saved as a dated file under swarm/ (not only in the log);
  (b) the day-247 outflow (about -230) and the unnamed outflow of days 231-278 are named from records, or marked unknown with the gap in EUR;
  (c) the daily cash bridge reconciles for the last 3 days;
  (d) the census shows at least 12 priced-with-stock selling slots.
- Permitted during the freeze: census, fixing unpriced slots, set_price, swap_item, and moving stock already on hand. Each action is logged with slot IDs.
- Missing records stay missing. Do not reconstruct orders or census from memory; mark them unknown.
- Diagnosis gaps: the freeze replaces the step 5 exception.

## Signal response (new)
- Chart comparison: judge slots_selling, revenue, revenue_per_slot, units and cash_gain_7 against the limits of the current phase (since day 292, the centres and limits in the main table of charts.md), not the pre-redesign limits. Read the "before" table as history only.
- slots_selling above the current-phase centre (5.2) for 8 readings in a row is a signal, even inside the limits. Respond as for WORSE: full census and restock-landing check, no order.
- slots_selling flagged WORSE on charts.md: the next action is a full 72-slot census and a restock-landing check, not a larger order. Log the census in the daily-log note.
- Purchases-per-unit above 1.0 for 3 days running: order gate stays closed until the ratio is back under 1.0 and the census shows at least 12 priced-with-stock selling slots.
- Units per day below 40 for 7 days with the order gate open: stop ordering, run a full census, and write a diagnosis note (D-level) before the next order.
- Any zero-sales day, or slots_selling at or below 7 on two days in a row: freeze all orders, run a full census and delivery trace, and write a diagnosis note before any order. Restart only when the census shows at least 12 priced-with-stock selling slots.
- Two days in a row with an unreconciled cash bridge: freeze orders, and name every outflow from the order records for days 175-216 before any further purchase.

## Weekly review (every 7 days, from day 120)
- Compare the week's unexplained cash gap with the previous week. If it is not below 50 EUR, cut purchasing to a 3-day stock buffer until it is.
- Full 72-slot census: count empty, unpriced, and priced-with-stock slots, and write them to the daily-log note.
- Sum the week's order records and cash bridges, and write a weekly summary to the daily-log note, including the purchases-per-unit ratio, for the 5-day and 50-day reviews.

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
- Unexplained cash: any outflow without a logged order stops purchasing until named, the same day it is found. A freeze lasts until the bridge reconciles.
- Diagnosis gaps: a 72-slot census and a cash bridge for days 175-216 are required to settle D-A-006. Until both exist, purchases are limited to the step 5 exception. Under v8, the freeze (above) overrides that exception.

## Verification
- Each day: balance change vs sales-report totals and spot fee, via the cash bridge (step 9).
- Charts: five measures (cash_gain_7, revenue, slots_selling, revenue_per_slot, units). cash_gain_7 is the cash over the last 7 recorded readings, not 7 days; compute 7-day cash change from daily-log balances by calendar day. Read progress against the "Since redesign" table and each chart's signal rules. Flag any point beyond limits as a signal to investigate.
- Progress test: benchmark needs about EUR 191/day from day 60 on, against about EUR 68/day recently; judge on revenue per selling slot, selling slot count (with reasons), units per selling slot, and purchases per unit sold. Revenue alone does not show the cause.
- If slots_selling trends down while empty slots rise, restock earlier, not later, but only into slots the restock-landing check confirms as priced.
- Day 365: confirm final balance and that no unpaid fees or open liabilities remain.

## Open questions
- Cause of the day-247 outflow (about -230) and of the 0.8-1.3 per unit outflow: not known; no records in the workspace (D-P-027).
- Whether slots are empty or unreachable after restocks: not confirmed; the freeze census (a) should settle it.
- Whether any review files differ in format from what the charts show.
- Whether restocked stock is unpriced or sitting in non-selling slots: the census from days 166-170 under steps 3 and 4 should settle it (D-A-004, "what would settle it").
