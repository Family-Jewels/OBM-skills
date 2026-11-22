As of day 86 (after S-004), for point 13: days 85–91.

**Constraint: worker time, as output per minute.** Median 445 of 480 min used (charts, last 7 days): 93% in use. Stocked slots fell 23 → 20 (S-004); charts show median 26, latest 28. Revenue per slot 7.73 against own best 9.55.

**Stretch aims, point 13 (days 85–91):**

| Driver | Now (day 86 charts) | Stretch aim, end of day 91 | Time share | Guardrail |
| --- | --- | --- | --- | --- |
| Slots selling (priority 1) | 7-period avg 19.47; latest 26; own best 21.86 | 7-period avg ≥ 24 of 72 | fills | cash ≥ 120 at every close; no slot left unpriced while it holds stock |
| Slots stocked at day end (leads slots selling) | median 26 (S-004: 20); latest 28 | median ≥ 30 of 72 | fills | depot read before each fill; no fill without product in the depot |
| Units, 7-period avg (priority 2, via units per fill) | 7-period avg 72.4; own best 82.86 | 7-period avg ≥ 83 | fills | never sell below unit cost |

Unit cost has no aim this point: its level is not charted yet (the designer will chart it).

**Time split (480 min a day, 09:00–17:00), per Strategist S-004:**
- Fills 360 min (75%): restocks only where the depot holds the product. At 45 min per slot this is about 8 restocks a day.
- Orders and sourcing 48 min (10%): placed before the first fill of the day.
- Pricing and reads 48 min (10%): read price response from normal sales reports against revenue per slot. No experiments.
- Reserve 24 min (5%): covers runs past 16:30.
- Marketing 0.

**Guardrails:**
- Order step placed before the first fill. If not placed by 10:00, fills run only for products with depot cover of at least 5 days, and the miss is logged. Stop fills near 16:30.
- Never run a fill without a depot read. A failed fill costs 45 min.
- No order above 40% of cash; no order above the lowest same-week quote from any supplier; cash ≥ 120 after each order.
- Commit idle cash above 240 to stock in the order step, within the best quote.
- If reads or pricing run over, cut pricing, not a fill and not the reserve.
- Fewer than 6 fills on 3 working days, or median stocked below 30 on day 91: the next pulse considers a diagnosis.

Note: the aims above assume 45 min per slot restocked. Whether that holds is not yet charted; see audits/AS-004.md.
