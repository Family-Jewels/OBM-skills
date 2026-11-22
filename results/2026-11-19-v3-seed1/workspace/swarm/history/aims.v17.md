As of day 234 (after S-011), for point 34: days 232–238. Record: audits/AS-011.md. Supersedes the point-31 aims (history/aims.v15.md). Design change needed: yes (see AS-011).

**Constraint: worker time (480 min a day), 92% used. Output per minute is the limit.** The largest gap is stocked-but-not-selling: 65 stocked, 19–22 selling. Converting stock is a pricing job, not a fill job.

| Driver | Now (day 234) | Stretch aim, point 34 | Priority | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling, 7-period avg | 21.4 (own best 29) | ≥ 32 | 1 | cash ≥ 120 at every close; no stocked slot left unpriced |
| Units, 7-period avg | 74.6 | ≥ 100 | 2, follows slots | never sell below unit cost |
| Slots stocked at day end, median | 65 | hold ≥ 60 (floor, not pushed) | leads slots selling | depot read before each fill |
| Stocked slots with no price, at close | not yet charted | 0 at every close | 1, process | a stocked slot unpriced past the next working day is a missed day in the pulse |

Unit cost is not pushed this point (goes to the auditor).

**Capacity split (480 min, 09:00–17:00):**
- Pricing and conversion 90 min (19%): first claim; every stocked slot with no price, right after the order step.
- Fills 340 min (71%): depot read first; only products the depot holds.
- Orders and quote checks 42 min (9%).
- Reserve 8 min (2%). Marketing 0.

Operator rules 3 and 19 still say the pricing block is 40 min; this split is 90. The redesign queued in AS-011 aligns them. Until then the split above is the one to follow.

**Guardrails (spec v8 and point-31 guardrails carry forward):**
- Cash ≥ 120 after each order and at every close.
- No fill without a depot read. A failed fill costs 45 min.
- Order step by 10:00. No order above 40% of cash or above the lowest same-week quote.
- If reads or pricing run over, cut optional reads first, then quote-check extras; never a set_price on a stocked slot, a fill or the reserve.
- Fewer than 6 fills on 3 working days: the next pulse considers a diagnosis.

**Log this point:** the restock batch test (minutes per call, slots per call); stocked-but-unpriced slots at each close; fills per working day; depot cover per product.
