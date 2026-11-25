# Aims: day 223, point 32 (days 218-224) (AS-010, after Strategist S-010). Previous: history/aims.AS-009.md

**Constraint:** stock in (spec 1a1b). Worker time is not the binding limit: 480 min a day is available and most of it is unused. Stock in is short (7-day median 8 stocked at day end, aim 20). The current stock-in route cannot close the gap on any minute count (see audits/AS-010.md). Design change needed: the route changes at the next redesign; these aims stand until then.

**Stretch aims, point 32 (days 218-224), judged at day 224.**

| Driver (spec term) | Now (charts, day 223) | Aim | Share of 480 min a day | Guardrail |
| --- | --- | --- | --- | --- |
| Stock in (1a1b; slots stocked at day end) | 7-day median 8; latest 5, of 72 | 7-day median at least 20 (ceiling 72) | 60%: 288 min (provisional: minutes per stock-in call unmeasured) | Cash ≥ 120 after each payment; order within the supplier's stated maximum (record any shortfall); no stock beyond lead time plus one cycle; unit cost < price |
| Worker time (1e; system clock) | 7-day median 65; latest 0 (S-010 quotes 265) | 7-day median at least 360 min a day (ceiling 432), once D-P-012 is closed | All 480 | Unallocated and review at least 48 min, not spent |
| Refills (1a1a; slots with stock in hand) | Not charted | Use minutes not taken by stock in | 20%: 96 min | No refill on a slot with no stock in hand |
| Slots selling (1a1) | Latest 5; 7-period 9.71 | 7-day median at least 14 (own best 14.29) | Follows stock in | Revenue per slot not falling |
| Pricing and mix (1a2, 1a2b) | Revenue per slot 5.88 (latest 7-period) | 7-period average at least 9.54 (own best), held | 5%: 24 min | Margin > 0; cut price only where revenue per slot shows it pays |
| Status reads and swaps (1a1) | Follows stock in | Read only | 5%: 24 min | One swap is 30 min (spec); 24 min does not cover one |

Unallocated and review: 10%, 48 min a day (guardrail). Split total: 288 + 96 + 24 + 24 + 48 = 480.

Top measure, cash: read, not pushed. Point 31 floor 12,356.90, aim 61,219.00; latest 6,263.78 (point 31), 6,440.34 (day 223).

**Standing guardrails (spec v4):** cash ≥ 120 every day; no product sold below unit cost; no marketing before M3; no send_payment outside a customer refund.

**Notes:**
- Stock in first each morning, per operator brief v6 (R-P-013), unchanged.
- Record minutes per stock-in call and per refill in each progress note until D-P-012 closes.
- Report stock on hand, in transit and receipts in each progress note until the system charts them (spec open question 9).
- Judge the worker-time aim against the action log as well as the clock until D-P-012 closes; a clock reading of 0 on a day with logged work is an instrument fault, not idleness.
