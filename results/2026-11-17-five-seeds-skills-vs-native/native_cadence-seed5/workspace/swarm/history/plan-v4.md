# Plan: Run Prosus Vending Bench for 365 days

Version 4, revised day 100 (previous version: swarm/history/plan-v3.md). Changes address D-P-013: batches sized for about 3 days instead of the 7-day cycle, restocks not triggered by slot level, cash above the buffer left idle, and stock-outs that keep the expansion gate shut.

## Context

Goal: maximise bank balance after 365 simulated days, starting from €1,500. Bankruptcy (more than 10 consecutive unpaid spot-fee days) or an unfinished run scores zero, so the run must reach SIMULATION OVER.

Benchmark to beat or match: about €3,228 by day 30 and about €61,219 by day 365 (scripted reference operator, which knows hidden parameters). Those are the trajectory targets. At day 100 the gap is large (cash €3,710 against about €15,346 for the reference operator), so growth must come from more sales per slot-day, not from holding cash.

## Operating loop (every simulated day)

1. Morning: `get_status`, then read `swarm/plan.md` and any review result from the last `wait_for_next_day`. Then read `get_machine_inventory` and `get_storage_inventory` and write the empty-slot count, slot fill levels and depot stock into the day's note.
2. Check reminders (`list_reminders`) and unread mail (`list_emails`, unread_only). Act on supplier replies and complaints. Log every stock invoice as a purchase in the note, so cash movements can be matched to it.
3. Sales: `get_sales_report` (by_product on a weekly cadence, by location as needed). Note what sells and at what price.
4. Stock: every morning, for every selling slot, compare fill level with the restock trigger below. Restock by the rules in "Restock rules" before any other purchase.
   - After any delivery, confirm the stock reached the depot (`get_storage_inventory`) and then the slot the next day. If it has not, note the delay and the supplier.
5. Cash deployment: after step 4, if balance is above the buffer, spend the excess on stock for selling slots (see "Money and fees"). Do not end a day with idle cash above the buffer while any selling slot is below full.
6. Price: adjust with `set_price` only on evidence from sales data. Keep AI-LOUNGE and MAIN-LOUNGE (price-sensitive, picky) close to observed price points; AI-HOUSE can carry a higher price.
7. Marketing: at most moderate use (one campaign per location per few days). Check `get_marketing_report` first. Repetition causes fatigue and cross-channel spam reduces traffic. Only run when stock is available to sell the extra demand.
8. Notes: `write_note` the day's key facts (prices that worked, supplier terms, slot fill levels, purchases, and for each restock the batch size and the slot fill before and after) so they survive context trimming.
9. `wait_for_next_day`.

## Restock rules

- Trigger: a selling slot at or below half full at the morning read. Do not wait for it to empty; batches sell out in 2 to 4 days.
- Size: fill each triggered slot to its capacity, not to a 3-day quantity. Order amount = slot capacity minus current stock minus depot stock for that product. A 7-day target (7-day average units per slot times 7) is the floor; never buy less than that for a selling slot.
- Depot first: if depot stock already covers the slot, move it to the machine and buy nothing new for that slot.
- Check `check_offers` before any order (prices change every 7 days). Buy only what can sell before expiry or slot cap.
- Order at least once every 2 days for each high-demand slot (AI-HOUSE first), so depot stock is always ready for the next trigger.

## Time budget (8-hour day, 09:00–17:00)

- Restock = 45 min, swap = 30 min, price change / status reads = minutes.
- Plan at most ~6 machine trips per day. Prioritise: empty or half-empty slots that sell, then low high-margin slots.
- The morning inventory reads are required. Keep other reads to the minimum the day's decisions need.
- Batch restocks in the morning when deliveries have landed. Combine orders to one supplier per day where prices allow.

## Money and fees

- Spot fee €12/day is a fixed cost across the network. Never let the balance drop to a level where fees and orders can't be covered.
- Cash buffer: keep about €470 (€300 plus ~2 weeks of fees). Balance above that buffer is spending money: each day, deploy it into fills under the restock rules, up to the depot and slot capacity for selling slots.
- Stock value is an asset. Keep depot stock to about one week of forecast sales (7-day units per slot times slots). Stock beyond that, or perishables near expiry, is a loss risk; do not buy it.
- Pay order invoices from balance; check balance before ordering. A stock purchase is inventory, not a loss.
- Cash is banked overnight; card takings settle a day later. Don't mistake unsettled card money for cash on hand.
- Refunds only via `send_payment` with the exact CMP- reference and full amount. Reference must match a complaint or invoice; a wrong reference loses money. Resolve complaints promptly to protect reputation.

## Suppliers and sourcing

- Week 1: `search_web` for wholesalers in Amsterdam (snacks and drinks, small and large product rows). Shortlist 2–3 suppliers. Email for catalogue and ask for volume or trade terms. Do not place large first orders until catalogue replies are read (replies arrive overnight).
- Use `check_offers` per supplier at the quantity you intend to buy; buy at the best current price.
- Keep at least two suppliers per category to limit damage from delays, short-shipment or a supplier going out of business. Check arrivals in the depot via `get_storage_inventory`.
- Track each supplier's delivery reliability in a note.

## Pricing and product mix

- Learn with `get_sales_report` (by_product) before changing price. Make small price moves (5–10%) and watch the response for at least 2–3 days before the next move.
- AI-LOUNGE and MAIN-LOUNGE: savoury snacks and coffee/drinks sell best; avoid over-pricing.
- AI-HOUSE: hungrier customers, tolerate higher prices and sell more volume; prioritise stock depth there.
- Avoid duplicate-product slots unless demand justifies them; extra slots add capacity, not customers.

## Expansion gate (new slots and duplicate products)

- Measure demand per in-stock slot-day: units sold divided by the number of slot-days a slot had stock (exclude days the slot was empty). Stock-outs hide demand, so the raw 7-day average understates it and must not decide expansion on its own.
- Also record the empty-slot days per week. Expansion is blocked while any selling slot is empty for more than 1 day in a week; fix restocking first.
- Do not add a slot, placement or duplicate product while the in-stock units per slot-day are below the previous week's figure.
- Expand when in-stock units per slot-day have been at or above the prior week's level for 2 consecutive weeks, and the empty-slot rule above is met.
- When a new slot is placed, log its date and product in a note, then check its 7-day units at the next 2 weekly reads before any further placement.

## Demand drop response

- Judge drops on weekly totals: if this 7-day unit total is more than 30% below the prior 7-day total, the same day read `get_sales_report` (by_product), `get_machine_inventory` and `get_storage_inventory`. Record the cause in a note (empty slots, depot stock waiting, or demand/placement).
- A short-term day-on-day dip right after a restock or during a normal end-of-cycle lull is not a drop. Note it, but do not trigger the full check.
- Count empty slot-days in the drop check: a low total with many empty slot-days is a restock problem, not a demand problem.
- Do not raise prices or add marketing in response to a drop until the cause is recorded.

## Review cadence

- Short review every 5 days, full review every 50 days. When a review asks for a diagnosis, look at what is going wrong (stock-outs, batch sizes, slot fill at restock, price errors, unpaid fees, complaints, slow restocks, idle cash) and revise `swarm/plan.md` accordingly.
- Read `swarm/metrics_system.md` and `swarm/charts.md` each day for trend signals; treat them as diagnostics, not targets.
- Judge progress on balance plus stock value (cash, depot stock and machine stock at cost), not on cash change alone. Purchases move cash into stock and would otherwise look like losses.
- Each review, compare the restock notes (batch size, fill before restock) against the restock rules and record any gap.

## Risks to monitor

- Stock-outs (empty slots = zero sales), especially in the days after a batch sells out.
- Undersized batches: restocks that do not fill the slot to capacity.
- Overstock / perishables aging in depot (wasted cash).
- Idle cash above the buffer (growth lost).
- Price spirals (price too high for picky customers, or too low to cover cost).
- Bankruptcy from unpaid fees if cash runs thin.
- Unresolved complaints lowering reputation.
- Marketing fatigue reducing traffic after repeated campaigns.

## Verification (per day, and end of run)

- Balance plus stock value after each day should trend up against the benchmark path (~€3,228 by day 30). If behind for two consecutive reviews, change the plan (e.g. reduce marketing, reprice, cut low-margin slots, deploy more cash into stock).
- Each review: confirm that average fill at restock is near capacity and that balance above the buffer is being deployed.
- At day 365, confirm SIMULATION OVER and final balance; write a closing note summarising lessons.

## Open items for user

- Diagnosis D-P-013 is unconfirmed. Batch size and slot fill at restock for days 70–83 were not read; check them in game notes and inventory reads at the next review and adjust the restock rules if they differ.
