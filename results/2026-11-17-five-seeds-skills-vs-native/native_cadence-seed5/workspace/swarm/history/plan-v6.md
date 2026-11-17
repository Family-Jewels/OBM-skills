# Plan: Run Prosus Vending Bench for 365 days

Version 6, revised day 175 (previous version: swarm/history/plan-v5.md). Changes address D-P-023: 93% of cash sat idle above the buffer, and the plan had no working sink for it once slots were full (depot cap too small, expansion gate too strict). Earlier: v5 (day 142) addressed D-P-019; v4 (day 100) addressed D-P-013.

## Context

Goal: maximise bank balance after 365 simulated days, starting from €1,500. Bankruptcy (more than 10 consecutive unpaid spot-fee days) or an unfinished run scores zero, so the run must reach SIMULATION OVER.

Benchmark to beat or match: about €3,228 by day 30 and about €61,219 by day 365 (scripted reference operator, which knows hidden parameters). Those are the trajectory targets. At day 100 the gap is large (cash €3,710 against about €15,346 for the reference operator), so growth must come from more sales per slot-day, not from holding cash.

## Operating loop (every simulated day)

1. Morning: `get_status`, then read `swarm/plan.md` and any review result from the last `wait_for_next_day`. Then read `get_machine_inventory` and `get_storage_inventory` and write the empty-slot count, slot fill levels and depot stock into the day's note.
2. Check reminders (`list_reminders`) and unread mail (`list_emails`, unread_only). Act on supplier replies and complaints. Log every stock invoice as a purchase in the note, so cash movements can be matched to it.
3. Sales: `get_sales_report` (by_product on a weekly cadence, by location as needed). Note what sells and at what price.
4. Stock: every morning, for every selling slot, compare fill level with the restock trigger below. Restock by the rules in "Restock rules" before any other purchase.
   - After any delivery, confirm the stock reached the depot (`get_storage_inventory`) and then the slot the next day. If it has not, note the delay and the supplier.
5. Cash deployment: after step 4, excess = balance minus the €470 buffer. If excess is above €300, spend it on stock for selling slots, up to the depot cap (see "Money and fees"). If excess still exceeds €770 after that and every selling slot is full, apply the idle-cash sink in "Expansion gate". Write the excess before and after deployment in the day's note. Do not end a day with idle cash above €770 unless the note records why it could not be deployed.
6. Price: adjust with `set_price` only on evidence from sales data. Keep AI-LOUNGE and MAIN-LOUNGE (price-sensitive, picky) close to observed price points; AI-HOUSE can carry a higher price.
7. Marketing: at most moderate use (one campaign per location per few days). Check `get_marketing_report` first. Repetition causes fatigue and cross-channel spam reduces traffic. Only run when stock is available to sell the extra demand.
8. Notes: `write_note` the day's key facts (prices that worked, supplier terms, slot fill levels, purchases, and for each restock the batch size and the slot fill before and after) so they survive context trimming.
9. `wait_for_next_day`.

## Restock rules

- Trigger: a selling slot at or below half full at the morning read. Do not wait for it to empty; batches sell out in 2 to 4 days.
- Size: fill each triggered slot to its capacity. Order amount = slot capacity minus current stock minus depot stock for that product. Never buy less than a 7-day target for a selling slot, where the target = 7 × demand per in-stock slot-day (the expansion-gate measure, not the raw 7-day average, which stock-outs depress).
- Demand per in-stock slot-day is the sizing basis: units sold ÷ slot-days with stock. Where a slot sold out before the 7 days ended, assume demand is at least the level it was selling at when it was in stock, and do not size down because of a short sales week.
- Depot first: if depot stock already covers the slot, move it to the machine and buy nothing new for that slot.
- Check `check_offers` before any order (prices change every 7 days). Buy only what can sell before expiry or slot cap.
- Order at least once every 2 days for each high-demand slot (AI-HOUSE first), so depot stock is always ready for the next trigger.
- Record each morning: count of selling slots at or below half full, and for each restock the batch size and fill before and after. Include these in the review.

## Time budget (8-hour day, 09:00–17:00)

- Restock = 45 min, swap = 30 min, price change / status reads = minutes.
- Plan at most ~6 machine trips per day. Prioritise: empty or half-empty slots that sell, then low high-margin slots.
- The morning inventory reads are required. Keep other reads to the minimum the day's decisions need.
- Batch restocks in the morning when deliveries have landed. Combine orders to one supplier per day where prices allow.

## Money and fees

- Spot fee €12/day is a fixed cost across the network. Never let the balance drop to a level where fees and orders can't be covered.
- Cash buffer: keep about €470 (€300 plus ~2 weeks of fees). Balance above that buffer is spending money: each day, deploy it into fills under the restock rules, up to the depot and slot capacity for selling slots. Idle cash is a loss, not a reserve, once the buffer is covered.
- Stock value is an asset. Keep depot stock to about one week of demand per in-stock slot-day × selling slots (not raw sales, which stock-outs suppress). While the idle-cash condition in "Expansion gate" holds, raise the cap to two weeks for the top-demand products (AI-HOUSE first). Stock beyond the cap, or perishables near expiry, is a loss risk; do not buy it. Within the cap, a fill that brings a slot to capacity is always allowed.
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
- Idle-cash sink: if excess (balance minus buffer) has stayed above €770 at three consecutive day-ends, every selling slot is full at each of those morning reads, and no selling slot has been at or below half full that week, you may place one new slot for a product not already in a slot, at AI-HOUSE first. The two-weeks-running rule does not apply to this exception. Do not place a second such slot until the first passes its check above. Log it as an idle-cash placement.
- Cash gain is not progress while cash is idle. Judge expansion and cash deployment on units, revenue per slot and the excess above buffer falling; do not read a rise in cash_gain_7 as success.

## Demand drop response

- Do not trigger on adjacent 7-day windows. A 30% fall between neighbouring windows is often a peak in one window (D-P-019: a 34% "drop" came from a peak day), not a demand change.
- Trigger the full check only on a control-chart signal in `swarm/charts.md` (a point beyond a limit, or 8 in a row on one side of the centre), or on the empty slot-days count rising for two weeks running. On a trigger, read `get_sales_report` (by_product), `get_machine_inventory` and `get_storage_inventory`, and record the cause in a note (empty slots, depot stock waiting, or demand/placement).
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

- Diagnosis D-P-023 is unconfirmed on whether slots or batch sizes are the limit. At the next read, record the count of selling slots at or below half, and batch size and fill before and after each restock, then tighten or loosen the depot cap and sink accordingly.

- Diagnosis D-P-013 is unconfirmed. Batch size and slot fill at restock for days 70–83 were not read; check them in game notes and inventory reads at the next review and adjust the restock rules if they differ.
- Diagnosis D-P-019 is unconfirmed. Read game notes, inventory and the purchase log for days 110–142: batch size, fill at restock, empty slot-days, and idle cash at each day end. If batches are not near capacity or idle cash stays above €770, tighten the sizing rules further.
