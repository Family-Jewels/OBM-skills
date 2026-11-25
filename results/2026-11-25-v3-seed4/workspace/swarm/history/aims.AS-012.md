# Aims: day 259, point 38 (days 260-266) (AS-012, after Strategist S-012). Previous: history/aims.AS-011.md

**Constraint:** stock in (spec 1a1b). Worker time is spare: charts show 155 of 480 min a day used (median), 325 idle. Stock in is short: slots stocked at day end, 7-day median 5 (latest 8), aim 20 of 72. More minutes have not lifted it (AS-010, AS-011, AS-012). The current stock-in route cannot reach the aim as the work is done now. Design change needed: yes (audits/AS-012.md). These aims stand until the redesign.

**Point 37 (days 253-259) closes today.** Judged against the charts: missed on stock in, worker time and slots selling. Values below are carried forward unchanged from S-012 (set for point 37); the Strategist sets new values.

**Stretch aims, point 38 (days 260-266), judged at day 266.**

| Driver (spec term) | Now (charts, day 259) | Aim | Share of 480 min a day | Guardrail |
| --- | --- | --- | --- | --- |
| Stock in (1a1b; slots stocked at day end) | 7-day median 5; latest 8, of 72 | 7-day median at least 20 (ceiling 72) | 60%: 288 min (provisional: minutes per stock-in call unmeasured) | Cash ≥ 120 after each payment; order within the supplier's stated maximum (record any shortfall); no stock beyond lead time plus one cycle; unit cost < price |
| Worker time (1e; clock and action log) | Used, 7-day median 155 (clock; D-P-012 open) | Daily total at least 400 min on each day (ceiling 432 after the 10% reserve); clock and action log within 10% of each other | All 480 | Unallocated and review at least 48 min, not spent |
| Refills (1a1a; slots with stock in hand) | Not charted | Use minutes not taken by stock in | 20%: 96 min | No refill on a slot with no stock in hand |
| Slots selling (1a1) | 7-period latest 8.71; own best 14.29 | 7-day median at least 16 | Follows stock in | Revenue per slot not falling |
| Pricing and mix (1a2, 1a2b) | Revenue per slot 7-period latest 9.56 | Hold at own best 9.71 as a guardrail (charts; S-012 wrote 9.54) | 5%: 24 min | Margin > 0; cut price only where revenue per slot shows it pays |
| Status reads and swaps (1a1) | Follows stock in | Read only | 5%: 24 min | One swap is 30 min (spec); 24 min does not cover one |

Unallocated and review: 10%, 48 min a day (guardrail). Split total: 288 + 96 + 24 + 24 + 48 = 480.

Top measure, cash: read, not pushed. Point 37 floor 19,519.75, aim 61,219.00; latest 7,102.67 (day 259). Required celeration x1.15 per point.

**Standing guardrails (spec v5):** cash ≥ 120 every day; no product sold below unit cost; no marketing before M3; no send_payment outside a customer refund.

**Notes:**
- Stock in first each morning, per operator brief v6, unchanged.
- The worker-time aim is judged on the daily total, not a 7-day median (spec v5, R-A-001). S-012 wrote a 7-day median; the spec governs.
- A clock reading of 0 on a day with logged work is an instrument fault, not idleness (D-P-012 open).
- Record minutes per stock-in call and per refill, stock received per point (€ and units), and stock on hand, in transit and receipts in each progress note until the system charts them (spec open question 9).
- Judge against the charts where S-012 and the charts differ (audits/AS-012.md lists them).
