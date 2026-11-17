# Plan: Operate Prosus Vending Bench for 365 days

## Context
Goal: maximise bank balance at day 365 from EUR 1,500. Unfinished or bankrupt runs score zero, so survival comes first: never let the business sit more than 10 consecutive unpaid days (spot fee EUR 12/day network-wide). Benchmark to beat: roughly EUR 3,228 at day 30 and EUR 61,219 at day 365.

Constraints found in the briefing:
- Plan mode blocked all vending tools, so the workspace is empty and no live state was read. Current stock, prices, suppliers and balance are unknown until day 1.
- 8-hour working day. Restock takes 45 min, swap 30 min, price change/status a few minutes. Realistically 6–10 machine trips per day, so batch restocks and prefer swap_item over clear+restock.
- Six machines (3 locations x SNACK/DRINKS), 72 slots. Snack rows A/B take small items (18 units), C/D large (10). Drinks slots hold 10.
- Duplicate products across slots share demand, so extra slots add capacity, not customers. Do not fill every slot with the same product for no gain.
- Cash is banked overnight; card takings settle a day later; open complaints hurt reputation.

## Approach

### Day 0 (first morning, 09:00)
1. get_status, get_machine_inventory (all), get_storage_inventory, get_marketing_report, list_emails, list_reminders, read_notes. Write a note with the starting state.
2. search_web for wholesalers of snacks and drinks in Amsterdam. Email 2–3 for catalogues and terms. Record supplier IDs in notes.
3. check_offers on each supplier before any order. Prices refresh weekly, so note the validity date.
4. Stock a balanced first load: savoury snacks and coffee/soft drinks suited to AI-LOUNGE (picky, price sensitive), larger quantities for AI-HOUSE (hungry, less price sensitive), and the highest-footfall MAIN-LOUNGE. Keep margins healthy and avoid tying up cash in slow sellers.
5. Set prices modestly above cost. Confirm every loaded slot has a price, since unpriced stock sells nothing.

### Daily loop (each day)
1. get_status first. Check balance, complaints, open orders, and whether any machine is empty or near empty.
2. get_sales_report (by_product, last few days) to see what sells and at what price. Use it to adjust prices and mix. Price response is the main lever, so test small price moves and read the effect next day.
3. Plan the day's trips: restock or swap only where stock is low and the product sells. Batch by location to save travel time.
4. Order from suppliers on the weekly offer cycle. Buy the next week's core products when the offer is good, and avoid buying slow movers.
5. Marketing: only moderate use, roughly one campaign per location per week at most, and rotate channels. Repetition causes fatigue, and cross-channel spam reduces traffic. Check get_marketing_report before spending. Run it only when the sales uplift clearly beats the cost.
6. Write end-of-day notes (state, decisions, prices, supplier IDs and terms) and set reminders for weekly offer changes and cash checks.
7. wait_for_next_day, then read the result: sales, deliveries, supplier replies, review outputs.

### Monitoring and reviews (from the system)
- Every day: read swarm/metrics_system.md and swarm/charts.md, and check for anomalies (balance trend, stockouts, margin per product).
- Every 5 days: short review. Act on any warning in swarm/plan.md.
- Every 50 days: full review. When a review asks what went wrong, diagnose from sales and inventory data before changing the plan, then revise swarm/plan.md.
- Always follow the current swarm/plan.md when it differs from this file.

## Risks and guards
- Bankruptcy: keep cash above roughly EUR 200 and the spot fee paid every day. Stop discretionary spending (marketing, bulk buys) if the balance falls.
- Stockouts: a slot with stock but no price sells nothing, and an empty slot loses sales. Check every machine at least every few days.
- Supplier risk: delays, short shipments and closures. Keep 2 suppliers for core lines and verify deliveries in the depot.
- Overstock: depot cash is not money. Buy in volumes that sell within about a week for perishable-like items.
- Complaints: resolve promptly with send_payment using the exact CMP- reference and the full amount. Unmatched payments are lost, so never guess the reference.
- Marketing overspend: costs are immediate, so log each campaign and its traffic effect in notes.

## Verification
- Each day, reconcile balance change against sales minus purchases minus spot fee and marketing.
- Track gap versus the benchmark (EUR 3,228 at day 30; EUR 61,219 at day 365) in the day's notes.
- Confirm the plan and notes are updated after each review.

## Open questions for the user
- None blocking. Operating decisions will be made from live data on day 0, since plan mode prevented reading the state.
