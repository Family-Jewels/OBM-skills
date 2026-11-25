# Aims: day 350, point 51 (days 351-357) (AS-015, after Strategist S-015). Previous: history/aims.AS-014.md

**Constraint:** stock in (spec 1a1b). Slots stocked at day end: latest 1, 7-day median 2 of 72 (charts), aim 24 (S-015). Stock received per point, depot units and the supplier maximum from check_offers are still not charted (spec open questions 7 and 9). The worker clock (system ground truth) reads a 7-day median of 0 with 5 of 7 days unused; the action log is not confirmed against it (D-P-012 open).

Capacity is not the limit. The stock-in route is.

**Stretch aims, point 51 (days 351-357), judged at day 357.** The S-015 levels carry forward unchanged. Their window (days 337-343) closed before this update, so they apply from the next point.

| Driver (spec term) | Now (charts, day 350) | Aim | Share of 480 min a day | Guardrail |
| --- | --- | --- | --- | --- |
| Stock in (1a1b; slots stocked at day end) | Latest 1; 7-day median 2; ceiling 72 | 7-day median at least 24 | 75%: 360 min, first claim each morning | Cash ≥ 120 after each payment; order within check_offers maximum (record any shortfall); cover target = planned slots per product × (lead time + 7 days); no stock beyond lead time plus one cycle; unit cost < price |
| Slots selling (1a1) | Latest 2 selling (control chart; 3.0 in own-best table); own best 14.29 | 7-day median at least 16 | Follows stock in | Revenue per slot not falling (celeration /1.09, wrong way) |
| Worker time (1e) | Clock 7-day median 0; 5 of 7 days unused | Clock at least 360 min a day on 5 of 7 days; action log within 10% of clock | The whole split below | A 0 clock reading on a day with logged work is an instrument fault (D-P-012) |
| Refills (1a1a) | Not charted | Use minutes not taken by stock in | 5%: 24 min | Refill only a slot with stock in hand. A refill is 45 min, so 24 min covers none: see note 2 |
| Pricing and mix (1a2, 1a2b) | Revenue per slot 6.36 (7-period latest); own best 10.19 | Hold at 9.71 (S-013); no stretch | 5%: 24 min | Margin > 0; no price move that cuts revenue per slot |
| Status reads and swaps (1a1) | Follows stock in | Read only | 5%: 24 min | A swap is 30 min; 24 min covers none |
| Unallocated and review | — | Not spent on other work | 10%: 48 min | At least 48 min a day kept unallocated |

Split total: 360 + 24 + 24 + 24 + 48 = 480 min a day.

**Top measure, cash:** read, not pushed. Latest point 50 (days 344-350): 7,701.97. Floor line 52,565.16; aim line 61,219.00 (charts). Required celeration from here is x2.82 per point against x1.00 now. The goal and the 61,219 aim stand.

**Standing guardrails (spec v6):** cash ≥ 120 every day; no 10-day run of unpaid days; no product sold below unit cost; marketing only within limits and only as the spec allows; no send_payment outside a customer refund; no send_payment to unmatched references.

**Notes:**
1. Slot plan, point 51: at least 24 slots across the six machines, highest-value slots first. Write the planned count per product in each order-day progress note (spec open question 12).
2. Refill and swap work does not fit the 24-minute shares (a refill is 45 min, a swap 30 min). When one is needed, do it after the day's stock in, from the stock-in share, and only while stock in is complete for the day. Strategist to confirm (AS-014 note 2 carries forward). This conflict is the subject of AS-015's design-change flag.
3. Until the system charts them, record in each progress note: minutes per stock-in call and per refill; stock received per point (€ and units); depot units on hand and in transit per supplier; maximum quantity per offer from check_offers.
4. Where the Strategist's figures and the charts differ, the charts govern. S-015 reported a clock median of 25 minutes at day 336; the system chart now reads 0 for the last 7 days. The charts are used.
