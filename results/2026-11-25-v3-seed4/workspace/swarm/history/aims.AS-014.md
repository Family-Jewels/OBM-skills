# Aims: day 315, point 46 (days 316-322) (AS-014, after Strategist S-014). Previous: history/aims.AS-013.md

**Constraint:** stock in (spec 1a1b). Slots stocked at day end: latest 1, 7-day median 1 of 72 (charts), aim 20. Not risen since day 249. Stock received per point, depot units and the supplier maximum from check_offers are still not charted (spec open questions 7 and 9), and the worker clock reads 0 while the log shows work (D-P-012 open), so output per minute and capacity cannot be read. R-P-014 has run two points with no shift yet on the charts.

Capacity is not the limit: worker time is unused on the clock, and cash is about 7,490 above the €120 reserve. The stock-in route is the limit.

**Stretch aims, point 46 (days 316-322), judged at day 322.** The S-014 levels carry forward unchanged.

| Driver (spec term) | Now (charts, day 315) | Aim | Share of 480 min a day | Guardrail |
| --- | --- | --- | --- | --- |
| Stock in (1a1b; slots stocked at day end) | Latest 1; 7-day median 1; ceiling 72 | 7-day median at least 20 | 75%: 360 min, first claim each morning | Cash ≥ 120 after each payment; order within check_offers maximum (record any shortfall); cover target = planned slots per product × (lead time + 7 days); no stock beyond lead time plus one cycle; unit cost < price |
| Slots selling (1a1) | Latest 1 slot selling; own best 14.29 | 7-day median at least 16 | Follows stock in | Revenue per slot not falling |
| Worker time (1e) | Clock median 0 (unconfirmed, D-P-012) | Action-log daily total at least 400 min on 5 of 7 days; log within 10% of clock | The whole split below | A 0 clock reading on a day with logged work is an instrument fault |
| Refills (1a1a) | Not charted | Use minutes not taken by stock in | 5%: 24 min | Refill only a slot with stock in hand. A refill is 45 min, so 24 min covers none: see note 2 |
| Pricing and mix (1a2, 1a2b) | Revenue per slot latest 5.97; own best 10.19 | Hold at 9.71 (S-013); no stretch | 5%: 24 min | Margin > 0; no price move that cuts revenue per slot |
| Status reads and swaps (1a1) | Follows stock in | Read only | 5%: 24 min | A swap is 30 min; 24 min covers none |
| Unallocated and review | — | Not spent on other work | 10%: 48 min | At least 48 min a day kept unallocated |

Split total: 360 + 24 + 24 + 24 + 48 = 480 min a day.

**Top measure, cash:** read, not pushed. Floor line 35,910.99 and aim line 61,219.00 (charts, point 45); latest 7,609.48.

**Standing guardrails (spec v5):** cash ≥ 120 every day; no 10-day run of unpaid days; no product sold below unit cost; no marketing before M3; no send_payment outside a customer refund.

**Notes:**
1. Slot plan, point 46: at least 20 slots across the six machines, highest-value slots first, as in point 41. Write the planned count per product in each order-day progress note (spec open question 12).
2. Refill and swap work does not fit the 24-minute shares. When a refill or swap is needed, it is done after the day's stock in, from the stock-in share, and only while stock in is complete for the day. Strategist to confirm (AS-014).
3. Until the system charts them, record in each progress note: minutes per stock-in call and per refill; stock received per point (€ and units); depot units on hand and in transit per supplier; maximum quantity per offer from check_offers.
4. Where the Strategist's figures and the charts differ, the charts govern. Point 45 (days 309-315) closed with no aims of its own; point 44's window (S-014) closed before this update.
