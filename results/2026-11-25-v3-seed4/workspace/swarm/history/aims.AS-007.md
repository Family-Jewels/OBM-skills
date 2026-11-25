# Aims: day 163, point 24 (days 162-168) (AS-007, after Strategist S-007). Previous: history/aims.AS-006.md

**Constraint:** worker time. The system clock shows a 7-day median of 0 of 480 minutes a day (5 of 7 days unused). Stocked slots at day end: latest 5, median 2, against an aim of 14. Idle minutes go to stock in first.

**Stretch aims, point 24 (days 162-168).** The S-007 aims, values unchanged, moved to the current point. Judged on the spec's measures at day 168.

| Driver | Now (charts) | Aim, point 24 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| Worker time used (system clock) | 7-day median 0 min a day | 7-day median at least 240 min a day | 50% stock in (240 min); 25% refills (120); 10% pricing and mix (48); 5% status reads and swaps (24); 10% unallocated and review (48) | Unallocated and review at least 48 min a day, not spent |
| Stock in (1a1b; slots stocked at day end) | Latest 5, median 2 of 72; receipts and depot stock not charted | At least 14 slots stocked at day end, 7-day median | 50%: 240 min a day | Cash ≥ 120 after each payment; order within the supplier's stated maximum (record any shortfall); no stock held beyond lead time plus one cycle; unit cost < price |
| Refills (1a1a; slots with stock in hand only) | Clock 0 min; log and clock disagree (D-P-012) | Use all minutes not taken by stock in | 25%: 120 min a day | No refill on a slot with no stock in hand |
| Pricing and mix (1a2) | Revenue per slot latest 6.16; 7-period average 6.24 | 7-period average at least 9.54 (own best), held | 10%: 48 min a day | Margin > 0; cut price only where revenue per slot shows it pays |
| Slots selling (1a1) | Latest 9; 7-period average 5.43 | 14 (own best 14.29), held | follows stock in and refills | Selling slots must have stock on hand |

Top measure, cash: read the floor and aim lines at point 24 (point 23: floor 6,717, aim 30,835). Not pushed directly.

**Standing guardrails (spec v4):** cash ≥ 120 every day; no product sold below unit cost; no marketing before M3; no send_payment outside a customer refund.

**Notes:**
- Stock in first each morning. Size each order to the full cover gap for its supplier (operator brief v5, R-P-012).
- Place each delivery in its machines the day it lands.
- Report stock on hand, in transit and receipts in each progress note until the system charts them.
- Minutes are judged on the system clock, the spec's ground truth. The log's refill count does not count toward an aim until the clock and log are reconciled (D-P-012).
- The minutes per stock-in call are not yet measured (spec open question 3), so the 240-minute share is provisional.
- If at day 168 the clock median is under 120 minutes a day, or stocked slots stay under 14 with minutes spent, the next aim update needs a design change.
