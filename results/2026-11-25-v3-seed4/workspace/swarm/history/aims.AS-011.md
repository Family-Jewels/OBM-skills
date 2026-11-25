# Aims: day 246, point 36 (days 246-252) (AS-011, after Strategist S-011). Previous: history/aims.AS-010.md

**Constraint:** stock in (spec 1a1b). Worker time is spare: most of the 480 min a day is unused. Stock in is short (aim 20 slots stocked; charts show 2 at day end, 7-day median 4, of 72). Stock in did not follow more minutes (S-011: held at 13 on 270 min). The current stock-in route cannot close the gap on any minute count. Design change needed: yes (see audits/AS-011.md). These aims stand until the redesign.

**Stretch aims, point 36 (days 246-252), judged at day 252.** Carried forward unchanged from S-011 (written for point 35, days 239-245, now ended); the Strategist sets any new values.

| Driver (spec term) | Now (charts, day 246) | Aim | Share of 480 min a day | Guardrail |
| --- | --- | --- | --- | --- |
| Stock in (1a1b; slots stocked at day end) | 7-day median 4; latest 2, of 72 | 7-day median at least 20 (ceiling 72) | 60%: 288 min (provisional: minutes per stock-in call unmeasured) | Cash ≥ 120 after each payment; order within the supplier's stated maximum (record any shortfall); no stock beyond lead time plus one cycle; unit cost < price |
| Worker time (1e; clock and action log) | Clock 7-day median 0 (D-P-012 open); S-011 quotes 270 | Daily total at least 400 min a day (ceiling 432 after the 10% reserve) | All 480 | Unallocated and review at least 48 min, not spent |
| Refills (1a1a; slots with stock in hand) | Not charted | Use minutes not taken by stock in | 20%: 96 min | No refill on a slot with no stock in hand |
| Slots selling (1a1) | Latest 3; 7-period 9.29 | 7-day median at least 16 (own best 14.29: a stretch) | Follows stock in | Revenue per slot not falling |
| Pricing and mix (1a2, 1a2b) | Revenue per slot 7.95 (latest 7-period) | Hold at own best 9.54 as a guardrail | 5%: 24 min | Margin > 0; cut price only where revenue per slot shows it pays |
| Status reads and swaps (1a1) | Follows stock in | Read only | 5%: 24 min | One swap is 30 min (spec); 24 min does not cover one |

Unallocated and review: 10%, 48 min a day (guardrail). Split total: 288 + 96 + 24 + 24 + 48 = 480.

Top measure, cash: read, not pushed. Point 35 floor 16,760.47, aim 61,219.00; latest 7,071.07 (point 35), 7,066.23 (day 246).

**Standing guardrails (spec v5):** cash ≥ 120 every day; no product sold below unit cost; no marketing before M3; no send_payment outside a customer refund.

**Notes:**
- Stock in first each morning, per operator brief v6 (R-P-013), unchanged.
- Record minutes per stock-in call and per refill, and stock received per point, in each progress note until D-P-012 closes and the system charts them.
- Report stock on hand, in transit and receipts in each progress note (spec open question 9).
- Judge the worker-time aim against the action log as well as the clock until D-P-012 closes; a clock reading of 0 on a day with logged work is an instrument fault, not idleness.
- The baseline figures in S-011 (stock in median 13, slots selling 12.71 and 16, worker time median 270) do not match the system charts. Judge against the charts; the Strategist is asked to reconcile (audits/AS-011.md).
