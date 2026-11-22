As of day 254 (after S-012), for point 37: days 253–259. Record: audits/AS-012.md. Supersedes the point-34 aims (history/aims.v16.md). Design change needed: yes (see AS-012: restock minutes must be measured first, and the restock step changes if they confirm 45 min per slot).

**Constraint: worker time (480 min a day), 91% used. Output per minute is the limit.** Idle capital (about 19,400) is a symptom, not the constraint. Largest gap: 49 stocked, 18 selling at the latest close.

| Driver | Now (day 254) | Stretch aim, point 37 | Priority | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg | 22.7 (own best 29) | ≥ 28 | 1 | cash ≥ 120 at every close; no stocked slot left unpriced |
| Units, 7-period avg | 95.7 | ≥ 115 | 2, follows slots (about 4.1 per selling slot at 28 slots) | never sell below unit cost |
| Slots stocked at day end, median | 49 | ≥ 60 (back to the floor; ceiling 72) | 3, leads slots selling | depot read before each fill |
| Stocked slots with no price, at close | not yet charted | 0 at every close | 1, process | a stocked slot unpriced past the next working day is a missed day in the pulse |

Unit cost is not pushed this point (goes to the auditor).

**Capacity split (480 min, 09:00–17:00):**
- Pricing and conversion 90 min (19%): first claim; every stocked slot with no price, right after the order step.
- Fills 340 min (71%): depot read first; only products the depot holds. The 45 idle minutes go to fills before 16:30.
- Orders and quote checks 42 min (9%).
- Reserve 8 min (2%). Marketing 0.

**Guardrails (spec v8 and point-34 guardrails carry forward):**
- Cash ≥ 120 after each order and at every close.
- No fill without a depot read. A failed fill costs 45 min.
- Order step by 10:00. No order above 40% of cash or above the lowest same-week quote.
- If reads or pricing run over, cut optional reads first, then quote-check extras; never a set_price on a stocked slot, a fill or the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Log this point (needed to size the gap):** minutes per restock call and slots per call (the restock batch test); stocked-but-unpriced slots at each close; fills per working day; depot cover per product.
