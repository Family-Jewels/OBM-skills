# Plan: Run Prosus Vending Bench for 365 days

Version 3, revised day 59 (previous version: swarm/history/plan-v2.md). Changes address D-P-007: a weekly restock cycle that leaves machines near empty, idle cash, and controls that block growth.

## Context

Goal: maximise bank balance after 365 simulated days, starting from €1,500. Bankruptcy (more than 10 consecutive unpaid spot-fee days) or an unfinished run scores zero, so the run must reach SIMULATION OVER.

Benchmark to beat or match: about €3,228 by day 30 and about €61,219 by day 365 (scripted reference operator, which knows hidden parameters). Those are the trajectory targets. Growth comes from compounding: cash above the buffer should go into stock that sells, and the network should expand only when sales data supports it.

## Operating loop (every simulated day)

1. Morning: `get_status`, then read `swarm/plan.md` and any review result from the last `wait_for_next_day`. Then read `get_machine_inventory` and `get_storage_inventory` and write the empty-slot count, slot fill levels and depot stock into the day's note.
2. Check reminders (`list_reminders`) and unread mail (`list_emails`, unread_only). Act on supplier replies and complaints. Log every stock invoice as a purchase in the note, so cash movements can be matched to it.
3. Sales: `get_sales_report` (by_product on a weekly cadence, by location as needed). Note what sells and at what price.
4. Stock: check every selling slot's fill level every 2 to 3 days, not only when it runs out. Restock when a selling slot is at or below half full, or when the next 3 days' units would empty it. Because batches sell out in 2 to 4 days, buy enough depth to cover the 7-day offer cycle. If depot stock already covers the slot, move it to the machine first and buy nothing new. Check `check_offers` before any order (prices change every 7 days). Buy only what can sell before expiry or slot cap.
   - After any delivery, confirm the stock reached the depot (`get_storage_inventory`) and then the slot the next day. If it has not, note the delay and the supplier.
5. Price: adjust with `set_price` only on evidence from sales data. Keep AI-LOUNGE and MAIN-LOUNGE (price-sensitive, picky) close to observed price points; AI-HOUSE can carry a higher price.
6. Marketing: at most moderate use (one campaign per location per few days). Check `get_marketing_report` first. Repetition causes fatigue and cross-channel spam reduces traffic. Only run when stock is available to sell the extra demand.
7. Notes: `write_note` the day's key facts (prices that worked, supplier terms, slot fill levels, purchases) so they survive context trimming.
8. `wait_for_next_day`.

## Time budget (8-hour day, 09:00–17:00)

- Restock = 45 min, swap = 30 min, price change / status reads = minutes.
- Plan at most ~6 machine trips per day. Prioritise: empty slots that sell, then low high-margin slots.
- The morning inventory reads are required. Keep other reads to the minimum the day's decisions need.
- Batch restocks in the morning when deliveries have landed.

## Money and fees

- Spot fee €12/day is a fixed cost across the network. Never let the balance drop to a level where fees and orders can't be covered.
- Cash buffer: keep about €470 (€300 plus ~2 weeks of fees). Cash above that buffer should be deployed into stock for slots that sell, not left idle. Idle cash earns nothing.
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

- Measure units per slot on 7-day totals (7-day sum divided by slots and 7), not single days, because the offer cycle makes daily figures swing.
- Do not add a slot, placement or duplicate product while the 7-day units per slot are below the previous 7-day figure.
- Expand when the 7-day units per slot have been at or above the prior week's level for 2 consecutive weeks, and the empty slots already in use are restocked.
- When a new slot is placed, log its date and product in a note, then check its 7-day units at the next 2 weekly reads before any further placement.

## Demand drop response

- Judge drops on weekly totals: if this 7-day unit total is more than 30% below the prior 7-day total, the same day read `get_sales_report` (by_product), `get_machine_inventory` and `get_storage_inventory`. Record the cause in a note (empty slots, depot stock waiting, or demand/placement).
- A short-term day-on-day dip right after a restock or during a normal end-of-cycle lull is not a drop. Note it, but do not trigger the full check.
- Do not raise prices or add marketing in response to a drop until the cause is recorded.

## Review cadence

- Short review every 5 days, full review every 50 days. When a review asks for a diagnosis, look at what is going wrong (stock-outs, price errors, unpaid fees, complaints, slow restocks, idle cash) and revise `swarm/plan.md` accordingly.
- Read `swarm/metrics_system.md` and `swarm/charts.md` each day for trend signals; treat them as diagnostics, not targets.
- Judge progress on balance plus stock value (cash, depot stock and machine stock at cost), not on cash change alone. Purchases move cash into stock and would otherwise look like losses.

## Risks to monitor

- Stock-outs (empty slots = zero sales), especially in the days after a batch sells out.
- Overstock / perishables aging in depot (wasted cash).
- Idle cash above the buffer (growth lost).
- Price spirals (price too high for picky customers, or too low to cover cost).
- Bankruptcy from unpaid fees if cash runs thin.
- Unresolved complaints lowering reputation.
- Marketing fatigue reducing traffic after repeated campaigns.

## Verification (per day, and end of run)

- Balance plus stock value after each day should trend up against the benchmark path (~€3,228 by day 30). If behind for two consecutive reviews, change the plan (e.g. reduce marketing, reprice, cut low-margin slots, deploy more cash into stock).
- At day 365, confirm SIMULATION OVER and final balance; write a closing note summarising lessons.

## Open items for user

- None blocking. Operate under this version from the next day.
