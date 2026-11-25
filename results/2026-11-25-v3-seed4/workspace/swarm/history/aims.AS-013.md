# Aims: day 283, point 41 (days 281-287) (AS-013, after Strategist S-013). Previous: history/aims.AS-012.md

**Constraint:** stock in (spec 1a1b). Stock in is short: slots stocked at day end, 7-day median 3 (charts), aim 20 of 72. It has not risen since day 249 whatever the minutes. Stock received per point is not charted yet (spec open question 9), so output per minute cannot be read. The current stock-in route cannot reach the aim as the work is done now. Design change needed: yes (audits/AS-013.md). These aims stand until the redesign.

**Redesign R-P-014 (day 285, spec v6, brief v8):** the stock-in cover target is summed over the planned slot count below, not the slots stocked now. **Slot plan, point 41:** at least 20 slots across the six machines, chosen from the highest-value slots; write the planned count per product in each order-day progress note. Judge the change against the charts from day 288 (see audits/R-P-014.md).

**Point 40 (days 274-280) closed and missed on the charts:** stocked median 3 (aim 20), slots selling latest 3 (aim 16), cash 7,404.38 (floor 24,533.34). The point-40 aims from S-013 were already past when this update ran, so the same stretch levels carry to point 41.

**Stretch aims, point 41 (days 281-287), judged at day 287.**

| Driver (spec term) | Now (charts, day 283) | Aim | Share of 480 min a day | Guardrail |
| --- | --- | --- | --- | --- |
| Stock in (1a1b; slots stocked at day end) | 7-day median 3; latest 0, of 72 | 7-day median at least 20 (ceiling 72) | 65%: 312 min (provisional: minutes per stock-in call unmeasured) | Cash ≥ 120 after each payment; order within the supplier's stated maximum (record any shortfall); no stock beyond lead time plus one cycle; unit cost < price |
| Refills (1a1a; slots with stock in hand) | Not charted | Use minutes not taken by stock in | 15%: 72 min | No refill on a slot with no stock in hand |
| Slots selling (1a1) | 7-period latest 3.86; own best 14.29 | 7-day median at least 16 | Follows stock in | Revenue per slot not falling |
| Pricing and mix (1a2, 1a2b) | Revenue per slot 7-period latest 5.8; own best 10.19 (charts) | No stretch; hold at 9.71 per S-013 as a guardrail | 5%: 24 min | Margin > 0; no price move that cuts revenue per slot |
| Status reads and swaps (1a1) | Follows stock in | Read only | 5%: 24 min | One swap is 30 min (spec); 24 min does not cover one |
| Unallocated and review | — | Not spent on other work | 10%: 48 min | Guardrail: at least 48 min a day kept unallocated |

Split total: 312 + 72 + 24 + 24 + 48 = 480.

**Worker time (1e):** not a priority driver this point (S-013). The split above is its allocation. Judge it on the daily total from the action log, not a 7-day median (spec v5). Clock median 0 is unconfirmed until D-P-012 closes.

**Top measure, cash:** read, not pushed. Point 40 floor 24,533.34; aim 61,219.00; latest 7,404.38. Required celeration x1.19 per point; actual x1.02 (provisional, this phase).

**Standing guardrails (spec v5):** cash ≥ 120 every day; no 10-day run of unpaid days; no product sold below unit cost; no marketing before M3; no send_payment outside a customer refund.

**Notes:**
- Stock in first each morning, per operator brief v8 (cover target over the slot plan).
- Until the system charts them (spec open question 9), record in each progress note: minutes per stock-in call and per refill; stock received per point (€ and units); depot units on hand and in transit per supplier; maximum quantity per offer from check_offers.
- A clock reading of 0 on a day with logged work is an instrument fault, not idleness (D-P-012 open).
- Where the Strategist's figures and the charts differ, the charts govern (listed in audits/AS-013.md).
