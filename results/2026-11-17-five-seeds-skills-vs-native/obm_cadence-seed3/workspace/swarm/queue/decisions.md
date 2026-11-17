# Decisions queue

## D-001 (day 11): refund CMP-001 exceeded the item price — for owner review (already acted)
- Complaint from Fatima El Amrani, day 10, out-of-date stock at MAIN-LOUNGE:DRINKS:A2 (sparkling water, price €1.80).
- Claimed €17.50. I first paid €1.80 (the item's price). The system kept the complaint open for the €15.70 balance, then I paid the €15.70 to close it. Total €17.50 paid, against an item price of €1.80.
- Default I would have chosen: refund the item price and contest the rest. Chosen instead: full claimed amount to close the complaint (C6: no open complaint after 2 days; open complaints lower reputation). Cost to cash: €15.70.
- Owner review: whether to refund the item price only for future claims of this kind. Recommended default for next time: pay the item price, then the claimed amount only if the system still reports the complaint open.
- Also check the expiry of stock: this item reached a customer past its date (depot stock is fresh from 13 Jan supplier deliveries; no expiry date is held in the records). Watch for repeats.

## D-001 update (day 23): the pattern is now four or more claims
- Claims applied the same way (item price first, balance to close): CMP-001 €17.50 (sparkling, €1.80 item), CMP-002 €19.49 (mint, €1.50), CMP-003 €7.40 (mint, €1.50), CMP-005 €24.82 (sparkling, €1.80). Also CMP-004 double charge €5.90 paid in full.
- Total refunds to day 23: €75.11. Claims run 4–13× item price.
- Recommendation for owner: (a) keep closing complaints (open complaints lower reputation), but (b) cut the cause: stock sitting in machines for more than about a week (mint from day 5 and sparkling from day 4 were the first to expire). Operator action now: load about one week's demand per slot and rotate stock.
- Default for next claim of this type unchanged: item price, then claimed amount to close. If the owner prefers item-price-only refunds, the default changes at the next review.

## D-002 (day 48): instrumentation request, for the owner
- Needed: stock-out slot-days per slot per day, and a 7-day COGS total from receipts (spec open question 1). Neither is in the records or the tools available to the operator.
- Default until answered: operator keeps a per-machine empty-slot count at each close (labelled proxy, not in-stock fraction). Not estimated as in-stock.
- Also requested: one basis for PIP. Quote the spec's cash ratio (exemplar cash ÷ swarm cash, same day). Day 36: 2.60. The chart's gain basis is not used for decisions.

## D-003 (day 48): refund rule C6 — decide before day 49 (redesign candidate)
- Open since day 11 (D-001). Refunds to date CMP-001..007 total €111.07 (plus the day-48 record). Each claim is paid at item price first, then the claimed balance to close (system keeps the complaint open until the full amount).
- Default recommended by the diagnosis (D-P-004): pay the item price, and pay the claimed balance only if the owner decides so. Operator continues the current default until the owner answers; the choice changes the cost by about €15–€25 per claim.

## D-005 (day 109): owner decision request, bundled (D-001, D-002, D-003 still open; defaults in use)
- Refund rule (D-001/D-003): pay the item price first, then the balance to close the complaint. Default in use since day 11. Claims since then: CMP-008 (€19.14, paid €1.50 + €17.64), CMP-009 (€6.51, paid €1.80 + €4.71), CMP-010 (€6.03, paid €2.50 + €3.53), CMP-011 (€12.51, paid €2.40 + €10.11). Owner: keep, or pay the item price only? Default: keep until you answer.
- Two "machine ate my money" claims (CMP-009 AI-LOUNGE:SNACK:A2; CMP-011 MAIN-LOUNGE:SNACK:C1) may be a vend fault; I will check those slots on the next visit. Owner: is there a service contact?
- Instrumentation (D-002): in-stock fraction and 7-day COGS are not provided. Default: operator empty-slot count per visit (proxy only).
- Run budget: the spec says about USD 2 left; the session shows about USD 33 left at day 109. Default: the session figure governs; spend about 1% of it per week.
- PIP basis: default is the spec's cash ratio (exemplar cash ÷ swarm cash, same day).
- No decision is blocking trading; all defaults are in use.

## D-006 (day 122): PIP chart value disagrees with its own inputs (measurement owner)
- The pulse reports (P-010 day 64, P-011, P-014, P-015, P-016) quote a PIP on the chart that does not match the chart's own cash inputs. P-016 day 118: chart 3.8, inputs 18,461.46 ÷ 5,928.35 = 3.11.
- Operator basis: spec's cash ratio (exemplar cash ÷ swarm cash, same day). Recomputed at day 122 from the ledger cash: exemplar ~18,461 at day 118 vs swarm 5,928; PIP ≈ 3.1. Default: use this recomputed figure; the chart's figure is not used.
- Owner or designer to fix the chart basis (default: spec's cash ratio).

## D-007 (day 203, logged late; was due day 150 per R-P-025): instrumentation and records request, for the owner
- Requested: (a) in-stock fraction per slot per day (or stock-out slot-days), (b) 7-day COGS from delivery receipts, (c) run-spend ledger, (d) the ledger record for the PIP exemplar.
- Records held by the operator: empty-slot count per restock visit (proxy, not in-stock fraction); sales by product (get_sales_report); delivery receipts in log/progress.md and day-by-day write_note keys.
- Default until answered: operator proxies (empty count per visit, COGS from receipts) are used; no further re-raise in pulses or logs unless the owner asks.
- Also noted (A-004 F): the 42-slot denominator against 72 physical slots is unexplained in the swarm files; operator assigns rotation of ~16 slots under operator rules v4.

## D-008 (day 267): unexplained stock loss in machines, for the owner and the measurement owner
- Observed: slots loaded from the depot read empty within 2–5 days, while get_sales_report recorded fewer units than the stock loaded. Examples: AI-HOUSE A1 stroopwafel 18 (loaded day 253, 0 on day 260); MAIN B2/B3 energy 10 each (loaded day 262, 0 on day 266); AI-HOUSE and MAIN found fully empty on days 244 and 253; AI-LOUNGE empty on day 246 (loaded days 236–241).
- Sales by product over 7 days (day 260 read): energy 68, protein 44, stroopwafel 37, choco 31, crisps 24. Loads over the same period were larger than these units.
- Cause not known from the tools: possible vend fault or unrecorded dispensing (cf. the 'machine ate my money' complaints CMP-009, CMP-011, CMP-023 at AI-LOUNGE DRINKS B3), or a stock-count fault. The operator cannot inspect the machines.
- Operator action in the meantime: smaller loads (10 per slot), one test slot (MAIN DRINKS B2 reloaded day 266) before loading the rest of MAIN. Do not change prices or the rotation.
- Ask: owner or measurement owner to check whether stock is leaving the machines without sales, and to give the in-stock count (D-007). Default: continue at smaller loads; no cash spent beyond the cover rule.
- Complaints this week (refunds paid, item price then balance): CMP-022 (€17.42, wrong item MAIN SNACK B2), CMP-023 (€16.83, machine ate money, AI-LOUNGE DRINKS B3), CMP-024 (€24.03, double charge). Owner review asked: refund of the item price only for the double-charge and money-lost claims.

## D-004 (day 48): parked-decision record — location unstocked for more than 2 days
- Days 34–36: AI-LOUNGE, AI-HOUSE and MAIN were largely empty of energy, crisps and snacks after the depot ran dry (no order was delayed by a choice). This matches the Parked item "leaving a location unstocked for more than 2 days". It was a stock-out, not a decision. Recorded here for the owner; no action pending.
