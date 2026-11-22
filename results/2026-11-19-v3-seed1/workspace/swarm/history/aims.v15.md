As of day 210 (after S-010), for point 31: days 211–217. Record: audits/AS-010.md. Supersedes the point-30 aims (history/aims.v14.md). Design change needed: no (see AS-010).

**Constraint: worker time (480 min a day), 91% used.** Output per minute is the limit. The largest gap is stocked-but-not-selling: slots selling depends on pricing and converting stock, not only on fill count.

| Driver | Now (day 210) | Stretch aim, point 31 | Priority | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg | 25.0 (own best 29) | ≥ 30 | 1 | cash ≥ 120 at every close; no stocked slot left unpriced |
| Slots stocked at day end, median | 56 (of 72) | ≥ 60 | 1, leads slots selling | depot read before each fill; no fill without product in the depot |
| Units, 7-period avg | 92.9 (own best 125.3) | ≥ 120 | 2, follows slots | never sell below unit cost |
| Stocked slots with no price, at close | not yet logged (charted from get_machine_inventory) | 0 at every close | 1, process | a stocked slot unpriced past the next working day is a missed day in the pulse |

Unit cost is not pushed this point (it is moving the wrong way, x1.08; goes to the auditor).

**Capacity split (480 min, 09:00–17:00):**
- Fills 380 min (79%): depot read first; only products the depot holds; after that machine's pricing.
- Pricing block 60 min (13%): right after the order step; every stocked slot with no price. First claim on the gap.
- Orders 32 min (7%): order step by 10:00; commit idle cash above 240 within the best quote.
- Reserve 8 min (2%): runs past 16:30.
- Marketing 0.

**Test this point:** one restock call for several empty slots of one machine, only where the depot holds the product. Log minutes per call and slots per call. The point-28 result is still not in the record; it is logged this point. Aims 1 and 2 depend on it: if one call fills one slot at 45 min, they are out of reach at this capacity and the next pulse says Diagnosis needed: yes.

**Guardrails (standing rules stand):**
- Cash ≥ 120 after each order and at every close.
- No fill without a depot read. A failed fill costs 45 min.
- The pricing block runs first every working day; never skip a stocked slot's price to make room for a fill.
- Order step by 10:00. If missed, fills run only for products with depot cover of at least 5 days, and the miss is logged. Stop fills near 16:30.
- No order above 40% of cash; no order above the lowest same-week quote.
- If reads or pricing run over, cut optional reads first, then quote-check extras; never a set_price on a stocked slot, a fill or the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Log for the next point:** slots restocked per call, minutes per restock call, fills per working day, depot cover per product, slots emptied per day, stocked-but-unpriced slots at each close.
