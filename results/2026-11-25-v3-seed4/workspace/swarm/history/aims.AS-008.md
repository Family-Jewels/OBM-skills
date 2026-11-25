# Aims: day 183, point 27 (days 183-189) (AS-008, after Strategist S-008). Previous: history/aims.AS-007.md

**Constraint:** stock in (spec 1a1b). Worker time is idle, not short: the system clock's 7-day median is 25 of 480 minutes a day (latest day 410). The minutes are not turning into stocked slots (median 6 of 72 at day end, aim 20).

**Stretch aims, point 27 (days 183-189).** The S-008 aims, values unchanged, moved from point 26 (point 26 ended at day 182, before this update). Judged on the spec's measures at day 189.

| Driver (spec term) | Now (charts, day 182) | Aim, point 27 | Share of capacity | Guardrail |
| --- | --- | --- | --- | --- |
| Worker time (1e; system clock) | 7-day median 25 min a day; latest 410 | 7-day median at least 360 min a day (ceiling 432) | All 480 min a day | Unallocated and review at least 48 min a day, not spent |
| Stock in (1a1b; slots stocked at day end) | Median 6, latest 11, of 72; receipts, depot stock and in-transit not charted | 7-day median of slots stocked at day end at least 20 (own best 14.29) | 60%: 288 min a day | Cash ≥ 120 after each payment; order within the supplier's stated maximum (record any shortfall); no stock held beyond lead time plus one cycle; unit cost < price |
| Refills (1a1a; slots with stock in hand only) | Not charted; log and clock disagree (D-P-012) | Use minutes not taken by stock in | 15%: 72 min a day | No refill on a slot with no stock in hand |
| Pricing and mix (1a2, 1a2b) | Revenue per slot latest 6.73 (7-period) | 7-period average at least 9.54 (own best), held | 10%: 48 min a day | Margin > 0; cut price only where revenue per slot shows it pays |
| Status reads and swaps (1a1) | Not aimed by S-008; follows stock in | Read only | 5%: 24 min a day | One swap is 30 min (spec); 24 min does not cover one |

Unallocated and review: 10%, 48 min a day (guardrail). Split total: 288 + 72 + 48 + 24 + 48 = 480.

Top measure, cash: read, not pushed. Point 26 floor 8,441.88, aim 48,708.40 (charts, day 182); cash 5,297.87.

**Standing guardrails (spec v4):** cash ≥ 120 every day; no product sold below unit cost; no marketing before M3; no send_payment outside a customer refund.

**Notes:**
- Stock in first each morning. Order the full uncovered quantity, cover summed over selling slots, with check_offers on each order day (operator brief v6, R-P-013).
- Diagnosis D-P-013 is open. Before relying on a minutes figure, confirm the operator's run status and tool access.
- Report stock on hand, in transit and receipts in each progress note until the system charts them (spec open question 9).
- Minutes are judged on the system clock only (D-P-012).
- Minutes per stock-in call are not measured yet, so the 288-minute share is provisional. Log them from the action log.
- At day 189, if the clock median is under 120 minutes a day, or stocked slots stay under 14 after minutes are spent, the next aim update must end `Design change needed: yes`.
