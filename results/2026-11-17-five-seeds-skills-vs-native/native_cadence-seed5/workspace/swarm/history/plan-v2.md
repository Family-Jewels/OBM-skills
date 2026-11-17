# Plan: Run Prosus Vending Bench for 365 days

Version 2, revised day 12 (previous version: swarm/history/plan-v1.md). Changes address D-P-001: slow opening stock, day-7 volume drop, and slots added ahead of demand.

## Context

Goal: maximise bank balance after 365 simulated days, starting from €1,500. Bankruptcy (more than 10 consecutive unpaid spot-fee days) or an unfinished run scores zero, so the run must reach SIMULATION OVER.

Benchmark to beat or match: about €3,228 by day 30 and about €61,219 by day 365 (scripted reference operator, which knows hidden parameters). Those are the trajectory targets. Growth comes from compounding: early cash should go into stock that sells, and the network should expand only when sales data supports it.

Limits of this plan: in plan mode the game tools (get_status, get_machine_inventory, read_notes, etc.) are blocked, so I have not yet seen live state. Day 1 begins with the reads listed below. The workspace is empty, so swarm/plan.md, swarm/metrics_system.md and swarm/charts.md do not exist yet; the system creates them.

## Operating loop (every simulated day)

1. Morning: `get_status`, then read `swarm/plan.md` and any review result from the last `wait_for_next_day`. Follow the current plan file over this one once it exists. Then read `get_machine_inventory` and `get_storage_inventory` and write the empty-slot count and depot stock into the day's note.
2. Check reminders (`list_reminders`) and unread mail (`list_emails`, unread_only). Act on supplier replies and complaints.
3. Sales: `get_sales_report` (by_product on a weekly cadence, by location as needed). Note what sells and at what price.
4. Stock: restock before a selling slot runs out, not after. Trigger a restock when a selling slot is at or below half full, or when the day's units would empty it. If depot stock already covers the slot, move it to the machine first and buy nothing new. Check weekly offers with `check_offers` before any order (prices change every 7 days). Buy only what can sell before expiry or slot cap.
   - After any delivery, confirm the stock reached the depot (`get_storage_inventory`) and then the slot the next day. If it has not, note the delay and the supplier.
5. Price: adjust with `set_price` only on evidence from sales data. Keep AI-LOUNGE and MAIN-LOUNGE (price-sensitive, picky) close to observed price points; AI-HOUSE can carry a higher price.
6. Marketing: at most moderate use (one campaign per location per few days). Check `get_marketing_report` first. Repetition causes fatigue and cross-channel spam reduces traffic. Only run when stock is available to sell the extra demand.
7. Notes: `write_note` the day's key facts (prices that worked, supplier terms, slot fill levels) so they survive context trimming.
8. `wait_for_next_day`.

## Time budget (8-hour day, 09:00–17:00)

- Restock = 45 min, swap = 30 min, price change / status reads = minutes.
- Plan at most ~6 machine trips per day. Prioritise: empty slots that sell, then low high-margin slots.
- The morning inventory reads are required. Keep other reads to the minimum the day's decisions need.
- Batch restocks in the morning when deliveries have landed.

## Money and fees

- Spot fee €12/day is a fixed cost across the network. Never let the balance drop to a level where fees and orders can't be covered.
- Pay order invoices from balance; check balance before ordering. Keep a cash buffer of at least ~€300 plus ~2 weeks of fees.
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

- Do not add a slot, placement or duplicate product while units per slot are falling or below the level of the last stable period.
- Expand only when units per slot have held for 5 consecutive days at or above the prior level, and the empty slots already in use are restocked.
- When a new slot is placed, log its date and product in a note, then check its units on each of the next 3 days before any further placement.

## Demand drop response

- If units fall more than 30% day on day, the same day read `get_sales_report` (by_product), `get_machine_inventory` and `get_storage_inventory`. Record the cause in a note (empty slots, depot stock waiting, or demand/placement).
- Do not raise prices or add marketing in response to a drop until the cause is recorded.

## Review cadence

- Short review every 5 days, full review every 50 days. When a review asks for a diagnosis, look at what is going wrong (stock-outs, price errors, unpaid fees, complaints, slow restocks) and revise `swarm/plan.md` accordingly.
- Read `swarm/metrics_system.md` and `swarm/charts.md` each day for trend signals; treat them as diagnostics, not targets.

## Risks to monitor

- Stock-outs (empty slots = zero sales).
- Overstock / perishables aging in depot (wasted cash).
- Price spirals (price too high for picky customers, or too low to cover cost).
- Bankruptcy from unpaid fees if cash runs thin.
- Unresolved complaints lowering reputation.
- Marketing fatigue reducing traffic after repeated campaigns.

## Verification (per day, and end of run)

- Balance after each day should trend up against the benchmark path (~€3,228 by day 30). If behind for two consecutive reviews, change the plan (e.g. reduce marketing, reprice, cut low-margin slots).
- At day 365, confirm SIMULATION OVER and final balance; write a closing note summarising lessons.

## Open items for user

- None blocking. Proceed to operate once plan mode is exited; the day-1 reads will refine the stock and pricing choices above.
