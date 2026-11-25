# Aims: day 50, point 8 (AS-002, after Strategist S-002). Previous: history/aims.v1.md

**Constraint:** stock on hand for stocked slots. Worker time is not the limit (295 of 480 min used on day 50; 7-day median 120). Cash is not binding (2,240 vs 120 reserve). The depot runs empty and deliveries slip, so stocked slots cannot be filled as fast as minutes allow.

**Stretch aims, point 8 (days 50-56).** S-002's aims ran to day 49 and have lapsed (16 stocked and selling by day 49: not met, 7 selling on day 50). Carried forward to the next point:
1. slots_selling: 16 stocked, priced and selling by day 56 (own best 14.29; standing aim 24).
2. Stock received: enough to cover lead time plus one cycle for those slots, ordered only for the uncovered quantity. The unit count is set once the supplier maximum order quantity is recorded (spec open question 7). Not yet charted.
3. revenue_per_slot: 7.89 on the 7-day average (carried forward, not lowered).
4. Top measure, cash: the aim line charted for day 56; the floor line is the minimum. Unit cost is not a priority until it has 6 points.

**Worker time, per day (480) and per point (3,360), per spec Resources:**

| Driver | Share | Per day | Per point |
| --- | --- | --- | --- |
| Refills (1a1, 45 min each; about 45 a point) | 60% | 288 min | 2,016 min |
| Pricing and mix (1a2) | 15% | 72 min | 504 min |
| Buying and offers (1b, stock received 1a1b) | 10% | 48 min | 336 min |
| Status reads and swaps | 5% | 24 min | 168 min |
| Unallocated and review | 10% | 48 min | 336 min |

Refills take first claim. Idle minutes are expected while stock is the limit; do not spend them without stock to put in a slot.

**Guardrails (from spec):**
- Cash ≥ 120 every day. A purchase that would breach it waits (parked if it is a single large purchase).
- Unallocated and review ≥ 10% of each point.
- Order only the uncovered quantity: cover for lead time plus one cycle, minus units on hand, minus units in transit. Record the supplier's maximum order quantity before sizing any order above the current €60-90 lots.
- Never order from an offer past its 7-day validity.
- Margin per unit > 0; no product sold below unit cost.
- Price cut only if revenue per slot shows it pays.
- No marketing before M3.

**Stock is not yet reachable by this split alone (see AS-002).** The redesign that changes the stock-in route is queued. Until it lands, keep the split and report stock on hand and deliveries at each pulse.
