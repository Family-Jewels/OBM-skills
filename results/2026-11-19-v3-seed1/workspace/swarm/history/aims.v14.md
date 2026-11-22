As of day 206 (after R-A-001), for point 30: days 204–210. Record: audits/R-A-001.md. Point-28 aims carried forward unchanged (no Strategist redirect has set point-30 aims; the Strategist is asked to redirect at the point 30 review). Time split changed (pricing block protected). Design change needed: no (the change is in audits/R-A-001.md, already adopted).

**Constraint: worker time, as output per minute.** Charts, last 7 days: 430 of 480 min used (90%), 50 min idle; slots stocked 54 of 72; capital 14,819 idle. Idle capital is a symptom, not the limit: depot stock is held at or above target while slots sit empty or unpriced. The output per minute must change; the aims are not lowered.

| Driver | Now (charts, day 206) | Aim, point 30 | Time share | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg (priority 1) | 24.57 (own best 29.0; 7-period avg, chart) | ≥ 29 | pricing block, then fills | cash ≥ 120 at every close; no slot left unpriced while it holds stock |
| Slots stocked at day end, median (priority 1, leads slots selling) | 54 at latest close (of 72) | ≥ 50 | fills | depot read before each fill; no fill without product in the depot |
| Units, 7-period avg (priority 2, follows slots) | 91.71 (own best 125.29) | ≥ 110 | fills | never sell below unit cost |
| Stocked slots with no price, at close (new count, priority 1 process) | not yet logged; to be counted from get_machine_inventory | 0 on every close | pricing block | a stocked slot with no price is a missed day in the pulse if it persists past the next working day |

Unit cost is not pushed this point.

**Test this point (decides aim 1):** one restock call for several empty slots of one machine, only where the depot holds the product. Log minutes per call and slots per call (R-P-013 item 2). The result for point 28 is not in the record; log it in progress.md this point. If one call fills several slots, the fill loop changes; if not, aim 1 stays out of reach at this capacity.

**Capacity split (480 min a day, 09:00–17:00):**
- Fills 400 min (83%): restock only where the depot holds the product, after the pricing block for that machine.
- Orders 32 min (7%): order step by 10:00; commit idle cash above 240 within the best quote where depot cover is under target (rule 16).
- Pricing block 40 min (8%): right after the order step, price every stocked slot that has no price (rule 3). Reads and quote checks come out of this block's remainder, not out of fills.
- Reserve 8 min (2%): covers runs past 16:30.
- Marketing 0.

**Guardrails (standing rules stand):**
- Cash ≥ 120 after each order and at every close.
- Never run a fill without a depot read. A failed fill costs 45 min.
- Never price-skip a stocked slot to make room for a fill: the pricing block runs first, every working day.
- Order step by 10:00. If missed, fills run only for products with depot cover of at least 5 days, and the miss is logged. Stop fills near 16:30.
- No order above 40% of cash; no order above the lowest same-week quote from any supplier.
- If reads or pricing run over, cut the optional reads first, then quote-check extras; never a set_price on a stocked slot, a fill or the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Prediction (R-A-001):** the count of stocked slots with no price falls to 0 within 3 working days; slots selling (7-period avg) rises from 24.57 to ≥ 27 by day 220. If slots selling has not reached 27 by day 227 (point 32), the pulse says Diagnosis needed: yes.

**Log for the next point:** slots restocked per call, minutes per restock call, fills per working day, depot cover per product, slots emptied per day, and stocked-but-unpriced slots at each close (from get_machine_inventory).
