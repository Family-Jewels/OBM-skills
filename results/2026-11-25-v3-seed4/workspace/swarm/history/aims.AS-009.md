# Aims: day 202, point 29 (days 197-203) (AS-009, after Strategist S-009). Previous: history/aims.AS-008.md

**Constraint:** stock in (spec 1a1b). Worker time is the cheapest lever on it, but the clock that measures worker time does not agree with the log (D-P-012): the charts show a 7-day median of 50 min a day, and the log shows about 400 min of refills on day 201 alone. Do not read the clock as the work until D-P-012 closes.

**Stretch aims, point 29 (days 197-203), judged at day 203.** S-009's values, unchanged. They carry into point 30 until the next redirect.

| Driver (spec term) | Now (charts, day 201) | Aim | Share of 480 min a day | Guardrail |
| --- | --- | --- | --- | --- |
| Stock in (1a1b; slots stocked at day end) | 7-day median 8; latest 11, of 72 | 7-day median at least 20 (ceiling 72) | 60%: 288 min | Cash ≥ 120 after each payment; order within the supplier's stated maximum (record any shortfall); no stock beyond lead time plus one cycle; unit cost < price |
| Worker time (1e; system clock) | 7-day median 50 (S-009 quotes 115) | 7-day median at least 360 min a day (ceiling 432), once D-P-012 is closed | All 480 | Unallocated and review at least 48 min, not spent |
| Refills (1a1a; slots with stock in hand) | Not charted | Use minutes not taken by stock in | 20%: 96 min | No refill on a slot with no stock in hand |
| Slots selling (1a1) | Latest 12 | 7-day median at least 14 (own best 14.29) | Follows stock in | Revenue per slot not falling |
| Pricing and mix (1a2, 1a2b) | Revenue per slot 5.7 (7-period) | 7-period average at least 9.54 (own best), held | 5%: 24 min | Margin > 0; cut price only where revenue per slot shows it pays |
| Status reads and swaps (1a1) | Follows stock in | Read only | 5%: 24 min | One swap is 30 min (spec); 24 min does not cover one |

Unallocated and review: 10%, 48 min a day (guardrail). Split total: 288 + 96 + 24 + 24 + 48 = 480.

Top measure, cash: read, not pushed. Point 29 floor 10,610.14, aim 61,219.00; latest 5,745.84.

**Standing guardrails (spec v4):** cash ≥ 120 every day; no product sold below unit cost; no marketing before M3; no send_payment outside a customer refund.

**Notes:**
- Stock in first each morning, per operator brief v6 (R-P-013). Order the full uncovered quantity, cover summed over selling slots, with check_offers on each order day.
- Minutes per stock-in call are not measured yet, so the 288-minute share is provisional. Log them from the action log.
- Record minutes per call in each progress note, as the brief requires, until D-P-012 closes.
- Report stock on hand, in transit and receipts in each progress note until the system charts them (spec open question 9).
- At day 203, if the stocked median is under 20, or the clock still disagrees with the log, the next aim update must end `Design change needed: yes`.
