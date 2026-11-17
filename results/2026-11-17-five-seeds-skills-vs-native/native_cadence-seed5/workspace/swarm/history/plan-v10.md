# Plan: Run Prosus Vending Bench for 365 days

Version 10, revised day 307 (previous version: swarm/history/plan-v9.md). Changes address D-P-046 (day 303; see swarm/audits/R-P-046.md): slots and revenue per slot are both still lower since R-P-041, cash is idle (about €16,400 excess against a €770 ceiling), and the exemplar path is out of reach. v10 changes: the sink is no longer gated on the restock queue or expansion gate and can place a slot daily; the depot cap is not the outlet for idle cash; slot and purchase logs are kept in the daily note; the day-365 exemplar path is replaced by a reachable interim target. Earlier: v9 (day 275) addressed D-P-041 (slot-recovery target, cost-price and stock-at-cost records, judge on balance plus stock at cost); v8 (day 243) addressed D-P-035; v7 (day 208) addressed D-A-004; v6 (day 175) addressed D-P-023; v5 (day 142) addressed D-P-019; v4 (day 100) addressed D-P-013.

## Context

Goal: maximise bank balance after 365 simulated days, starting from €1,500. Bankruptcy (more than 10 consecutive unpaid spot-fee days) or an unfinished run scores zero, so the run must reach SIMULATION OVER.

Reference (not a target): about €3,228 by day 30 and about €61,219 by day 365 (scripted reference operator, which knows hidden parameters). From v10 the target is reachable: balance plus stock at cost rising by at least €150 a day, averaged over each 14-day window from day 330, and at least 20 selling slots by day 330. The exemplar path needs about €715 a day from day 303, against about €56 a day actual, and is not used to judge the plan. At day 100 the gap is large (cash €3,710 against about €15,346 for the reference operator), so growth must come from more sales per slot-day, not from holding cash. At day 275 the gap is structural (cash about €15,300 against about €45,600 for the reference operator; net gain about €50 a day against about €466 a day needed). Do not cut the buffer, skip restocks or overstock to chase the path. Keep maximising balance plus stock at cost, and record the gap at each review.

## Slot recovery target (v9)

- Target: at least 20 selling slots by day 330 (the day-300 target was missed). Slots below 15 are a failure state, not routine.
- Any morning with fewer than 15 selling slots: run the full check that day (`get_sales_report` by_product, `get_machine_inventory`, `get_storage_inventory`) and record the cause. Do not wait for a second morning.
- Each morning, count selling slots and log every placement, removal and product change in the slot-change log. The log and the purchase log are kept in the daily note (`write_note`) from day 307; no separate log file was found in the workspace at day 303, so the plan does not depend on one. If a day's log entry is missing, record "log missing" and use `get_storage_inventory` and `get_machine_inventory` for the attribution. Attribute each drop of 3 or more to removal, empty slot with no depot stock, empty slot with depot stock (transfer lag), or demand. Unattributed drops are recorded as unattributed; they are not dismissed as rebounds.
- Slot count below 20 for more than 5 days, with excess above €770, is a trigger to use the sink (below) to re-place slots, starting with AI-HOUSE.

## Operating loop (every simulated day)

1. Morning: `get_status`, then read `swarm/plan.md` and any review result from the last `wait_for_next_day`. Then read `get_machine_inventory` and `get_storage_inventory` and write the empty-slot count, slot fill levels and depot stock into the day's note.
2. Check reminders (`list_reminders`) and unread mail (`list_emails`, unread_only). Act on supplier replies and complaints. Log every stock invoice as a purchase in the note, so cash movements can be matched to it.
3. Sales: `get_sales_report` (by_product on a weekly cadence, by location as needed). Note what sells and at what price.
4. Stock: every morning, for every selling slot, compare fill level with the restock trigger below. Restock by the rules in "Restock rules" before any other purchase.
   - After any delivery, confirm the stock reached the depot (`get_storage_inventory`) and then the slot the next day. If it has not, note the delay and the supplier.
   - Log every slot placement, removal and product change in the note with its date. Empty slots and removed slots must be distinguishable.
   - If selling slots fell by 3 or more since the previous morning, the next morning's read is a transfer-or-purchase test: if empty slots have depot stock waiting, the cause is transfer lag (move that stock first, see "Restock rules"); if the depot is empty for those products, the cause is purchasing (order that day, check `check_offers`). Record the answer in the note.
5. Cash deployment: after step 4, excess = balance minus the €470 buffer. If excess is above €300, spend it on stock for selling slots, up to the depot cap (see "Money and fees"). Deployment is not blocked by slots being empty or below full: buy for every selling product whose depot is under cap. If excess still exceeds €770 after that, apply the idle-cash sink in "Expansion gate". Write the excess before and after deployment and the depot stock value at cost in the day's note. Do not end a day with idle cash above €770 unless the note records why it could not be deployed.
6. Price: adjust with `set_price` only on evidence from sales data. Keep AI-LOUNGE and MAIN-LOUNGE (price-sensitive, picky) close to observed price points; AI-HOUSE can carry a higher price.
7. Marketing: at most moderate use (one campaign per location per few days). Check `get_marketing_report` first. Repetition causes fatigue and cross-channel spam reduces traffic. Only run when stock is available to sell the extra demand.
8. Notes: `write_note` the day's key facts (prices that worked, supplier terms, slot fill levels, purchases, and for each restock the batch size and the slot fill before and after) so they survive context trimming.
9. `wait_for_next_day`.

## Restock rules

- Trigger: a selling slot at or below two-thirds full at the morning read, or any selling slot that cannot be refilled before the next morning. Do not wait for it to empty; batches sell out in 2 to 4 days, and slots dropping to zero within a day are the main cause of lost sales (D-P-035).
- Restock lag: a delivery takes about 1 to 2 days to reach the slot. Order a day earlier than the trigger would otherwise suggest, so stock is in the depot when the slot reaches its trigger.
- Size: fill each triggered slot to its capacity. Order amount = slot capacity minus current stock minus depot stock for that product. Never buy less than a 7-day target for a selling slot, where the target = 7 × demand per in-stock slot-day (the expansion-gate measure, not the raw 7-day average, which stock-outs depress).
- Demand per in-stock slot-day is the sizing basis: units sold ÷ slot-days with stock. Where a slot sold out before the 7 days ended, assume demand is at least the level it was selling at when it was in stock, and do not size down because of a short sales week.
- Depot first: if depot stock already covers the slot, move it to the machine and buy nothing new for that slot. Empty slots (zero stock) with depot stock are restocked first in the day's first trips, before any purchase or other task.
- Stock-out buffer: a slot whose stock will run out before the next scheduled visit counts as triggered, even if above half full.
- Never let a slot sit empty while depot stock for its product exists. Record the empty-slot-with-depot-stock count each morning; it must be zero by the end of the day.
- Check `check_offers` before any order (prices change every 7 days). Buy only what can sell before expiry or slot cap.
- Order at least once every 2 days for each high-demand slot (AI-HOUSE first), so depot stock is always ready for the next trigger.
- Record each morning: count of selling slots at or below half full, and for each restock the batch size and fill before and after. Include these in the review.

## Time budget (8-hour day, 09:00–17:00)

- Restock = 45 min, swap = 30 min, price change / status reads = minutes.
- Restock trips come before all other tasks (swaps, price changes, marketing, new placements). Plan up to 8 trips a day while 3 or more selling slots are empty or triggered, or while excess is above €300; otherwise about 6.
- If the triggered slots exceed the trips available, serve them in order of demand per in-stock slot-day (AI-HOUSE first), and note the slots left unserviced.
- Test once and record: does one trip refill several slots? Log the slots filled per trip for the first 5 trips of the next week and use the result to set the trip count.
- The morning inventory reads are required. Keep other reads to the minimum the day's decisions need.
- Batch restocks in the morning when deliveries have landed. Combine orders to one supplier per day where prices allow.

## Money and fees

- Spot fee €12/day is a fixed cost across the network. Never let the balance drop to a level where fees and orders can't be covered.
- Cash buffer: keep about €470 (€300 plus ~2 weeks of fees). Balance above that buffer is spending money: each day, deploy it into fills under the restock rules, up to the depot and slot capacity for selling slots. Idle cash is a loss, not a reserve, once the buffer is covered.
- Stock value is an asset. Depot cap: two weeks of demand per in-stock slot-day × selling slots (not raw sales, which stock-outs suppress), for every selling product, whenever excess is above €300. Stock beyond the cap, or perishables near expiry, is a loss risk; do not buy it. Within the cap, a fill that brings a slot to capacity is always allowed. The cap is about €1,000 of cost at present, so it is not the way to use the excess.
- Cost log (v9): record the cost price of each product from every invoice and `check_offers` quote, in a cost-price note. Each morning, write stock value at cost (depot plus machine) into the day's note. Until the cost log has a price for every selling product, cost is estimated at 50–55% of selling price and marked as an estimate.
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
- Also record the empty-slot days per week. Expansion (demand-based, below) is blocked while any selling slot is empty for more than 1 day in a week; fix restocking first. The idle-cash sink is not blocked by this rule (v10).
- Do not add a slot, placement or duplicate product while the in-stock units per slot-day are below the previous week's figure.
- Expand when in-stock units per slot-day have been at or above the prior week's level for 2 consecutive weeks, and the empty-slot rule above is met.
- When a new slot is placed, log its date and product in a note, then check its 7-day units at the next 2 weekly reads before any further placement.
- Idle-cash sink (v10): if excess (balance minus buffer) is above €770 after step 5 deployment on a day, place one new slot that day, for a product not already in a slot, at AI-HOUSE first, then the lounges. Up to four sink slots may be open at once, and a new one may be placed every day the condition holds (v9 allowed two open and one every 3 days, which did not convert the idle cash). The condition is only that step 5 has already deployed everything the depot caps allow. Do not require a clear restock queue, full slots, or no slot below two-thirds full (D-P-035). Fill each new sink slot to capacity within 2 days; a sink slot still empty after 2 days is removed and logged as a failed placement. Each sink slot is judged at its 7-day units and empty-slot days at the next 2 weekly reads; a sink slot that sells nothing in-stock for 7 days is removed. Log each as an idle-cash placement with date and product.
- Idle cash is converted by sink placements, not by larger depots (D-P-041, D-P-046). Do not raise the depot cap to absorb excess; the cap stays at two weeks of demand. Once four sink slots are open and excess is still above €770, record the excess and the reason in the note; do not hold it silently.
- Before any sink placement, the depot cap for AI-HOUSE is two weeks (see "Money and fees"); fill that cap first.
- Cash gain is not progress while cash is idle. Judge expansion and cash deployment on units, revenue per slot and the excess above buffer falling; do not read a rise in cash_gain_7 as success.
- Known chart blind spot: cash_gain_7 counts stock purchases as losses, and the charts do not show slow slides. Do not read "routine variation" in `swarm/charts.md` as "no problem". Judge balance plus stock value at cost, and check slots_selling and revenue_last_7 directly each morning (see "Demand drop response"). A WORSE flag on cash_gain_7 caused by stock purchases is not a reason to change the restock rules; check stock value first.
- An IMPROVEMENT signal on cash_gain_7 means cash is piling up unspent, not that the operation is improving (D-P-035). Treat it as a trigger to run step 5 and the sink check, and record it that way. Points above the limit for slots_selling must also be checked against the pre-redesign limit in `swarm/charts.md`, not only the since-redesign table.

## Demand drop response

- Do not trigger on adjacent 7-day windows. A 30% fall between neighbouring windows is often a peak in one window (D-P-019: a 34% "drop" came from a peak day), not a demand change.
- Trigger the full check on a control-chart signal in `swarm/charts.md` (a point beyond a limit, or 8 in a row on one side of the centre), on the empty slot-days count rising for two weeks running, on any selling-slot drop of 3 or more that is not explained by the transfer-or-purchase test, or on a slow slide the charts miss: selling slots below 15 on any morning (v9; was two consecutive mornings), or revenue_last_7 lower at two consecutive short reviews. A drop of 3 or more slots that rebounds within 2 days still counts as a restock failure and is logged. On a trigger, read `get_sales_report` (by_product), `get_machine_inventory` and `get_storage_inventory`, and record the cause in a note (empty slots, depot stock waiting, or demand/placement).
- A short-term day-on-day dip right after a restock or during a normal end-of-cycle lull is not a drop. Note it, but do not trigger the full check.
- Count empty slot-days in the drop check: a low total with many empty slot-days is a restock problem, not a demand problem.
- Do not raise prices or add marketing in response to a drop until the cause is recorded.

## Review cadence

- Short review every 5 days, full review every 50 days. When a review asks for a diagnosis, look at what is going wrong (stock-outs, batch sizes, slot fill at restock, price errors, unpaid fees, complaints, slow restocks, idle cash) and revise `swarm/plan.md` accordingly.
- Read `swarm/metrics_system.md` and `swarm/charts.md` each day for trend signals; treat them as diagnostics, not targets.
- Judge progress on balance plus stock value (cash, depot stock and machine stock at cost), not on cash change alone. Purchases move cash into stock and would otherwise look like losses.
- Each review, compare the restock notes (batch size, fill before restock) against the restock rules and record any gap.
- Each short review: count the slot drops of 3 or more and the transfer-or-purchase test results from the notes; if a drop was not explained, run the full check.

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

- Balance plus stock value after each day should trend up against the interim target (€150 a day from day 330; reference path ~€3,228 by day 30 is not used). If behind for two consecutive reviews, change the plan (e.g. reduce marketing, reprice, cut low-margin slots, deploy more cash into stock).
- Each review: confirm that average fill at restock is near capacity and that balance above the buffer is being deployed.
- At day 365, confirm SIMULATION OVER and final balance; write a closing note summarising lessons.

## Open items for user

- Diagnosis D-P-046 (day 303) is open on three points, and v10 takes a position on each. (1) Whether the slot, restock and purchase logs exist anywhere: none were found in the workspace at day 303; v10 requires them in the daily note from day 307, and does not rely on them if they are missing. (2) Whether the sink rate converts idle cash: v10 raises it to one placement a day, up to four open; if excess still stays above €770 for 14 days, the next review should look at a larger sink rather than the depot cap. (3) Whether the day-365 benchmark is usable: v10 replaces it with the €150 a day interim target; the next review should confirm or reset that figure against the day-330 result.

- Diagnosis D-P-041 (day 270) is unconfirmed on the cause of slot losses: restock failure, transfer lag, or slot removal. The v9 slot-change log, restock log and purchase log are the test. Attribute every slot drop of 3 or more by the rule under "Slot recovery target". If removals, not restocks, explain most drops, revise the restock rules; if restock failures do, revise the trigger and order timing.

- Diagnosis D-P-035 is partly unconfirmed: the cause chain (restock lag causes slot dips, which block the sink and expansion gate) is not yet tested. Keep the daily note, record stock value at cost, and run the transfer-or-purchase test after each 3+ slot drop. Days 147, 150, 154 and 173 have no metrics rows; if a gap recurs, record it in the note.

- Diagnosis D-A-004 is unconfirmed on whether transfer lag or purchasing causes the slot drops. The next transfer-or-purchase test after any 3+ slot drop settles it; adjust "Depot first" or the purchase timing accordingly. The purchase log and slot-change log were missing from the review and must now be kept.

- Diagnosis D-P-023 is unconfirmed on whether slots or batch sizes are the limit. At the next read, record the count of selling slots at or below half, and batch size and fill before and after each restock, then tighten or loosen the depot cap and sink accordingly.

- Diagnosis D-P-013 is unconfirmed. Batch size and slot fill at restock for days 70–83 were not read; check them in game notes and inventory reads at the next review and adjust the restock rules if they differ.

- Diagnosis D-P-019 is unconfirmed. Read game notes, inventory and the purchase log for days 110–142: batch size, fill at restock, empty slot-days, and idle cash at each day end. If batches are not near capacity or idle cash stays above €770, tighten the sizing rules further.
