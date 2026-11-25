# Aims: day 71, point 11 (AS-003, after Strategist S-003). Previous: history/aims.v2.md

**Constraint:** stock on hand for selling slots. Cash is not binding (2,978 vs 120 reserve). Worker time is not binding (7-day median 100 of 480 min used, per the charts). Stock is limited by lead time: larger orders have arrived later (see guardrails).

**Stretch aims, point 11 (days 71-77).** S-003's point-10 aims lapsed on day 70 (slots_selling 7-period average 4.57 against 14). Carried forward, not lowered:
1. slots_selling: 14 on the 7-day average by day 77 (own best 14.29; standing aim 24).
2. revenue_per_slot: 9.54 on the 7-day average (own best; latest 6.28).
3. Stock in: on hand plus in transit covers the selling slots. Cover per slot = units per selling slot per day (about 4.5) × (supplier lead time + 7 days): about 50 units a slot for kanaal, noordzee and zuidas; about 75 for bakker. Report stock on hand, in transit and deliveries per point in the progress note until the system charts them (spec open question 9).
4. Top measure, cash: the charts' aim line (×1.16 a point, about 4,930 by day 77); floor about 2,690. Falling short of the aim triggers nothing.

**Worker time: 480 min a day, 3,360 per point (S-003's split, in minutes):**

| Driver | Share | Per day | Per point |
| --- | --- | --- | --- |
| Buying and offers (1b, stock in 1a1b) | 35% | 168 min | 1,176 min |
| Refills (1a1, 45 min each; only for slots with stock in hand, about 26 a point) | 35% | 168 min | 1,176 min |
| Pricing and mix (1a2, 1a2b) | 10% | 48 min | 336 min |
| Status reads and swaps | 10% | 48 min | 336 min |
| Unallocated and review | 10% | 48 min | 336 min |

Buying takes first claim. Do not spend refill minutes on a slot with no stock in hand.

**Guardrails (spec v3, unchanged):**
- Cash ≥ 120 every day. A purchase that would breach it is parked if it is a single large purchase.
- Unallocated and review ≥ 10% of each point (48 min a day).
- Order to the cover target: target minus on hand minus in transit.
- Keep each supplier order near €90–100 per visit. Orders of about €90 arrived in 3–4 days; PO-1027 (zuidas, €194) is due 12 days after ordering. Record each order's quantity and lead time.
- Noordzee has a €90 minimum per order: check it against the current offer before ordering.
- No order from an offer past its 7-day validity.
- Maximum order quantity: none seen up to 60 units a line (day 71). Record it on each order.
- Margin per unit > 0; no product sold below unit cost.
- Price cut only if revenue per slot shows it pays.
- No marketing before M3.

**Stock is not reachable by this split alone (see AS-003).** A redesign of the stock-in route is queued (earliest point 13, day 85). Until it lands, keep the split and report stock on hand, in transit and deliveries at each pulse.
