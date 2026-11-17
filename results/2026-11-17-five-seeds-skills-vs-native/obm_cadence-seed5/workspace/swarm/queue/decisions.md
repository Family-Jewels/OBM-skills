# Parked decisions

## A-007 response (day 357, orchestrator)
- Action 1 (cover check on due-day mornings): applied from day 321 on; due-day mornings with an order not yet in depot counted as zero (days 330, 337, 344, 351 and 356 checked). Not every day logged per location (gap acknowledged).
- Action 2 (records): unit_costs.md extended to PO-1097 (PO-1056 to 1070 by reference to the progress log); index.md status at day 357; swarm log synced to day 316; timelog rows to day 294 (fill counts for 295 to 357 are in log/progress.md, not re-keyed).
- Action 3 (designer package, one request): units per selling slot down since day 287; one-day-late delivery on PO-1073 to PO-1097; PIP basis still open since day 216; cover, units-per-slot and unsold-inventory charts still not delivered; label fix on charts.md. No new redesign requested before day 334; end of run is day 365 (8 days left), so the designer's changes can no longer pay back much.
- End-of-run rule (orchestrator): from day 357 only stock that can sell by day 365 is ordered; unsold stock is not a money asset.

## CMP-023 (day 360, Daan Smit, EUR 24.39) and CMP-022 (EUR 12.94): parked, reputation 0.92 (day 360)
- Reputation 0.92 at or above 0.85 → both parked. If reputation falls below 0.85 before day 365, pay both as claimed (day-142 exception) using the complaint emails' CMP references.

## CMP-022 (day 335, Lars Jansen, EUR 12.94): parked, reputation 0.96 (day 335)
- Complaint rule: reputation at or above 0.85 → park unverified claim. Reputation 0.96 → parked. Open: CMP-022 only. Pay as claimed if reputation drops below 0.85 (day-142 exception).

## R-P-039 revert test count, day 330 (orchestrator; for the designer's revert check)
- Priced slot count at 09:25 to 11:30, day 330 (6 machines, 36 priced slots): empty 27 of 36. Breakdown: MAIN snack 8 of 8 empty; HOUSE snack 5 of 7; LOUNGE snack 5 of 7; MAIN drinks 2 of 4; HOUSE drinks 4 of 5; LOUNGE drinks 3 of 5.
- Depot at 11:55 day 330: cola 10, gummy 3, nothing else (nuts 0, crisps 0, energy 0). PO-1088 (nuts 70) and PO-1089 (energy 60) due 330 not yet in depot; PO-1090 (crisps 60, gummy 50, cola 60; EUR 199.20) ordered 330 at 12:20, due 333.
- Fact for the designer: the empties are a depot-stock gap (no crisps order landed between 326 and 333; no gummy or cola in transit after 325 until 330), not a rule-11 read error in the orchestrator's cover count. The count is above 15 of 30; the R-P-039 revert test (3 or more counts above 15 in days 318 to 330) needs the day 318 to 329 counts, which are not all in the log. Orchestrator has not reverted; it reports the count only.
- Order-timing lapses logged: energy cover below 8 from day 327 (ordered 327 16:10, PO-1089); crisps below 8 from 326 (ordered 330, PO-1090, due 333).

## Pulse P-038 (day 302, read day 305): cash_gain_7 label and PIP basis (designer)
- P-038 says cash_gain_7 is labelled "shift down" while its since-mean (550.2) sits above the prior upper limit (525.53). Orchestrator cannot resolve the label; asks designer to correct the label in charts.md.
- PIP: chart gain-based 4.9 vs spec cash-based 4.4 at day 302. Still unresolved (open since day 262). Designer to settle with the next redesign.
- Diagnosis flagged "yes" by P-038: passed to designer; no operator action beyond the pivots (fills first, zero count logged, per-location cover daily).
- Orchestrator: swarm/log/progress.md synced through day 302 (done day 302; includes R-A-006 adoption on day 287).

## CMP-020 (day 303, Priya Nair, EUR 15.67): parked, reputation 0.88 (day 303)
- Same complaint rule as CMP-019. Reputation 0.88 is at or above 0.85: parked. Open parked claims: CMP-018 (4.34), CMP-019 (17.47), CMP-020 (15.67), total EUR 37.48. Reputation fell 0.96 → 0.92 → 0.88 over days 298 to 303 with three claims; if it drops below 0.85, pay all three as claimed (day-142 exception).

## CMP-019 (day 302, Fatima El Amrani, EUR 17.47) and CMP-018: parked, reputation 0.92 (day 302)
- Complaint rule (spec, R-001 open): reputation at or above 0.85 → park unverified claim. Reputation 0.92 → CMP-019 parked; CMP-018 (EUR 4.34) still parked. No payment made.
- Default if reputation falls below 0.85: pay exactly as claimed under the reference (CMP-019 / CMP-018), per the day-142 exception. Check get_status each morning.
- Orchestrator note, day 302: the parked claims total EUR 21.81, below 0.1% of balance. Payment or not does not change the outcome; the park rule is kept.

## A-006 records and projection, day 280 (orchestrator; designer diagnosis in progress)
- M4 miss (by day 180: each marketing spend tied to a measured uplift): no marketing was run in this run after day 1 (traffic 1.0 at all three locations, marketing report day 241); the milestone's test is therefore not met as written, recorded here.
- M5 pace miss (by day 270: cash at or above about 26,500; fill trips at or near cap): cash 10,302 at day 280 against the pace line of about 26,500 at day 270 (about 24,000 at day 259 by the spec's 0.88%/day); fill trips were at cap on working days but stock-outs left machines empty for 1 to 3 days each order cycle.
- Projection at the recent rate (about 30 to 60 net per day since day 254): about 16,000 to 18,000 at day 365 against 61,219 at the exemplar. Goal and exemplar are for the human to revisit; not changed here.
- Designer items from A-006 still open: per-location days-of-cover trigger (operator v7 now logs per location), lead-time overrun, PIP basis (cash, spec v7), chart label errors, missing ground-truth rows (days 1, 152, 243, 244, 247, 248, 263 in metrics_system.md), R-001 complaint rule.

## CMP-018 (day 269, Chloe Martin, EUR 4.34, out-of-date stock): parked, reputation 0.96 (day 270)
- Complaint rule: reputation at or above 0.85, so parked unverified. Pay as claimed if reputation falls below 0.85 (day-142 exception).

## Label and PIP-basis conflicts in charts.md, day 268 (pulse P-033 pivot 3): designer to correct at next redesign check
- Since-R-A-005 table: revenue and units means sit well above centre but read "no shift yet"; revenue_per_slot and cash_gain_7 read "beyond upper limit" while inside it. Orchestrator cannot verify without point data.
- PIP: chart 5.1 (gain basis) vs spec 4.5 (cash basis, 43,735 ÷ 9,717 at day 264). Spec line 46 says cash basis. Recommend the cash basis on both chart and spec.
- Orchestrator log: swarm/log/progress.md synced to day 268 (days 254 to 268 added). The R-A-003 day-161 outcome is not in the orchestrator log; the designer holds it.

## PIP definition and chart arithmetic, day 262 (pulse P-032 pivot 3): designer to settle
- Chart states PIP 5.3 on day 259; its own inputs (42,869.61 ÷ 9,347.67) give 4.6. P-029 and P-031 flagged the same mismatch (5.3 vs 4.66).
- Spec v7 defines PIP as the cash ratio (spec line 46). The chart is gain-based. Recommend: one definition (cash ratio), restated on the chart from day 262.
- Operator holds R-A-005 (spec v7, operator v7) until its predicted-shift date in audits/R-A-005.md. Orchestrator recommendation: no change before day 262 revert check.
- Interim cover practice (orchestrator, logged in log/progress.md): 09:00 cover per product at each location; order when network cover is below 8 days; size to 11 days; EUR 75 zuidas minimum has forced 2 to 3 times target on small lines (day 256).

## R-P-024 revert test sent to designer, day 242 (A-005 action 1): designer to rule revert or redesign
- Numbers as audited: units per selling slot 3.3 on days 217 to 226 against the 4.0 revert line; revenue mean 83.6 and 78.2 (prediction was at least 110 by day 226).
- Orchestrator recommendation: revert to v5 (or redesign), since the R-P-024 revert line is met. v6 stays in force until the designer rules.
- Operator practice in the meantime: zero count and depot units logged at 09:00 and close; cover logged at order and arrival; MAIN first; fill to cap while the depot holds stock.
- Cover on days 239 to 242: cola and energy at 0 depot stock on day 239 (PO-1053 ordered, delivered day 242). Choco and crisps at 0 depot stock day 236 to 240 (PO-1052 due 240, delivered 241, one day late).

## CMP-016 (day 229, Daan Smit, EUR 9.00): parked, reputation 0.88 (day 230)
- Not one purchase (highest single item EUR 3.20). Default: do not pay; refund only a verified single item at its slot price with reference CMP-016.
- Open complaints day 230: CMP-014 (8.04), CMP-015 (15.94), CMP-016 (9.00); total EUR 32.98. If reputation falls below 0.85, the day-142 exception (pay exactly as claimed) would apply to all three.

## CMP-015 (day 226, Chloe Martin, EUR 15.94): parked, reputation 0.92 (day 227)
- Claim: asks EUR 15.94, reference CMP-015 (as listed in status day 227). Not one purchase: highest single item price is EUR 3.20 (tortilla, AI-LOUNGE C2, currently out of stock).
- Default (complaint rule, reputation 0.92 >= 0.85): do not pay. If a single-item fault is verified, refund that item's slot price with reference CMP-015.
- Open with CMP-014 (Tom de Boer, EUR 8.04, parked day 218). If reputation falls below 0.85, the day-142 exception would apply to both (total about EUR 24).

## R-P-024 prediction check, day 226 (operator reading; designer to decide revert or keep)
- Prediction (R-P-024): revenue mean over days 207-226 at least EUR 110 (against 82.6 since R-P-021); stock-out slot-days falling by a third; cover 8-11 on 80% of days; units per selling slot at least 4.5.
- Operator reading from the sales reports in the log: daily revenue, days 207-226, mean about EUR 78 (20 values, range 9.8 to 170.7). Prediction NOT met on revenue.
- Zero-stock count (09:00/09:25 logs): 25-26 of 30 (days 214-217), 17 of 30 (day 223). Falling since day 217, which is in the prediction's direction.
- Units per selling slot: not computed by the operator (needs the chart); designer to read it from charts.md.
- Operator action: rule 2 v6 kept in force (no revert made by the operator). Revert conditions in R-P-024 are for the designer or the system to confirm from charts.md.

## CMP-014 (day 217, Tom de Boer, "double charged", EUR 8.04): parked, reputation 0.96
- Claim: double charge, asks EUR 8.04, reference CMP-014 (as listed in status day 218). Same customer as CMP-006 (day 132, EUR 23.10, parked then).
- Why parked (complaint rule, reputation 0.96 >= 0.85): EUR 8.04 is more than the price of one item at any slot (highest single price EUR 3.20 for tortilla at AI-LOUNGE; energy 2.20-2.10 at MAIN and AI-LOUNGE); no transaction record visible.
- Default: do not pay. If a duplicate charge is verified, refund one item at its slot price with reference CMP-014.

## PIP mismatch flagged to designer, day 216 (P-027 and P-028 pivot 3)
- Chart PIP (gain-based) does not match its own inputs: P-028 gives 5.4 charted vs 4.5 from cash (35,079.77 / 7,714.07 at day 214). P-027 gives 5.2 charted vs 4.4 (34,214 / 7,735, day 209). Both definitions are above 2 in every case.
- Operator asks the designer to fix one definition (spec: cash / cash) and recheck the chart's arithmetic.
- Swarm log sync: swarm/log/progress.md now covers days 154-214 (added day 215), so the 16-day gap cited in P-028 is closed.

## Second supplier for nuts and gummy, day 213 (operator action; designer to note)
- Trigger: zuidas PO-1047 (nuts 60, gummy 60, crisps 40; paid 182.00 on day 210) shows delivery day 221 (11 days; usual 3-5). Zuidas reply (day 212) gave no ETA.
- Action: kanaal-cash-carry (not used before; valid through 217; minimum order EUR 120): nuts 80 @0.95 and gummy 60 @0.80 (cost about 124). Its nuts price is 5% below zuidas' current price; its lead time is not yet known.
- Designer to decide: keep kanaal-cash-carry as a second supplier for nuts and gummy (if its lead time is 3-5 days), or cancel the zuidas PO-1047 nuts/gummy lines on the next contact (order cannot be cancelled by the tools; the goods will arrive day 221).

## CLOSED day 208: v3 cover-revert conflict (A-004 action 1 vs R-P-021), per P-026 pivot 1
- Operator state now: operator rule 2 = v4 text (revenue per trip, from day 186); operator rule 11 = v5 text (R-A-003 cover floor 8, depot + machine + in-transit); spec v5 rows stay in the spec. v3 is NOT restored on disk. This is the record the operator runs.
- Designer to align spec v5 and operator text on one version (rule 2) when the P-024 / D-P-024 redesign comes.
- Price and marketing moves held (P-026 pivot 3), except the day-203 crisps price test at AI-LOUNGE (2.60), which stays until the diagnosis returns.

## EXCEPTION applied day 199: CMP-010, CMP-011, CMP-012, CMP-013 paid in full as claimed (EUR 57.57)
- Trigger: reputation 0.84 on day 199 (below 0.85; 0.88 on day 198), so the day-142 exception applies: pay exactly as claimed while reputation is below 0.85.
- Payments (all confirmed by the system; complaints withdrawn): CMP-010 Daan Smit EUR 3.60; CMP-011 Sanne Willems EUR 16.35; CMP-012 Priya Nair EUR 22.51; CMP-013 Sanne Willems EUR 15.11 (AI-HOUSE:SNACK:B1, "machine ate my money", reported day 198).
- Balance after: 7,386.87.
- Designer note: the four claims were each several times the item price; the reputation drop (1.00 to 0.84 since day 150s) cost more demand than the refunds. R-001 (complaint rule) still needs a settled rule; this exception is the operator's current standing rule until then.

## CMP-012 (day 197, Priya Nair, "wrong item dispensed", AI-LOUNGE:SNACK:A1; EUR 22.51)
- Claim: wrong item from AI-LOUNGE A1 (chocolate bar, EUR 1.50); asks EUR 22.51, reference CMP-012. Same customer as CMP-005 and CMP-007.
- Why parked (complaint rule, reputation 0.88 >= 0.85): EUR 22.51 is about fifteen times the slot price; not one purchase; no transaction record visible.
- Default: do not pay. If a wrong-item dispense is verified, refund one item at EUR 1.50 with reference CMP-012.
- Risk noted: reputation 0.88 (day 198); CMP-010 (3.60), CMP-011 (16.35) and CMP-012 (22.51) open. If reputation falls below 0.85, the day-142 exception (pay exactly as claimed) would apply to all three (total about EUR 42.46). Designer to settle R-001 before that happens.

## REVERT of R-P-021 fill-order change, day 186 (operator position; designer to confirm)
- R-P-021 revert condition (its own text): zero-stock count still 14 or more by day 185, or cash_gain_7 below 289.85 for 2 pulses in a row.
- Day 186 09:25 count (operator, full inventory read): 21 of 30 priced slots empty (AI-LOUNGE 5 of 11; AI-HOUSE 9 of 9; MAIN 7 of 10). Day 185 was higher (about 22 by close of 184). Cash_gain_7 below its limit at P-022 (252.5 against 289.85).
- Action: operator rule 2 returned to v4 text (restock empty slots by highest revenue per trip first). Zero counts still logged at 09:00 and close (A-004 action 2). Spec v5 rows left as they are until the designer decides.
- Conflict kept open: A-004 action 1 (restore spec v3 and operator v3) is still parked; R-A-003 (cover floor 8 days) stays in force until the designer decides.
- Designer to decide: whether the revert of rule 2 is the redesign, and what the diagnosis (P-022 request) should test first.

## CONFLICT day 183: A-004 action 1 (restore spec v3 / operator v3 on disk) vs R-P-021 (keep R-A-003)
- A-004 (delivered day 183, as of day 167) asks the orchestrator to restore spec v3 and operator v3 now, since R-A-003's revert test is met.
- R-P-021 (adopted day 177, later) keeps R-A-003 for now: reverting would reopen the late-order gap and confound the day-185 test of the fill-order change. Spec v5 and operator v5 (rule 2 only) are in force.
- Operator position: follow the adopted redesign (R-P-021 / operator v5). Operator rule 11 is therefore the v5 text (floor 8 days; depot + machine + in-transit). My day-167 note operator_rule11_revert_day167 is superseded by this entry.
- Recommended default for the designer: keep R-A-003 until the day-185 test (zero-stock count 14 or fewer, cash_gain_7 above 289.85), then decide revert or keep on the data. Do not revert on disk in the meantime.
- Other A-004 actions taken by the operator: receipts PO-1036 to PO-1039 added to unit_costs.md; index.md updated to day 183; fill order by units lost per hour; zero counts logged at 09:00.

## CMP-011 (day 172, Sanne Willems, "out of date stock", MAIN-LOUNGE:DRINKS:A2; EUR 16.35)
- Claim: past-date item from MAIN DRINKS A2 (energy at EUR 2.20); asks EUR 16.35, reference CMP-011. Same customer as CMP-009 (day 141, EUR 18.53, parked).
- Why parked (complaint rule, reputation 0.92 >= 0.85): EUR 16.35 is about seven times the slot price; not one purchase; expiry not visible to the operator.
- Default: do not pay. If a past-date item is verified, refund one item at EUR 2.20 with reference CMP-011.
- Pattern: three "out of date stock" claims (CMP-009, CMP-010, CMP-011) each for several times the item price. Designer to consider whether stock age can be tracked (loaded date) to test these.

## CMP-010 (day 162, Daan Smit, "out of date stock", MAIN-LOUNGE:SNACK:C1; EUR 3.60)
- Claim: past-date crisps bag from MAIN C1; asks EUR 3.60, reference CMP-010. Same customer as CMP-003 (day 59) and CMP-005 neighbour pattern.
- Why parked (complaint rule, reputation 0.96 >= 0.85): EUR 3.60 is not one purchase at the slot price (crisps EUR 2.50 at MAIN C1). Expiry is not visible in the machine data. No transaction record visible.
- Default: do not pay. If a past-date item is verified, refund one item at EUR 2.50 with reference CMP-010.
- Note: MAIN C1 crisps were loaded from depot on day 161 (stock dates not visible to operator).

## EXCEPTION day 142: complaints CMP-005 to CMP-009 paid in full (EUR 77.63) while reputation < 0.85
- Trigger: reputation fell 1.00 -> 0.92 (day 135) -> 0.80 (day 142) with five open complaints. Sales report day 141: reputation demand multiplier 0.84 (about 16% lower demand; 128 units sold that day).
- Action: paid each claim exactly as claimed under its reference (CMP-005 3.46, CMP-006 23.10, CMP-007 15.20, CMP-008 17.34, CMP-009 18.53); the system confirmed each refund and withdrew each complaint. Balance after: 4,676.14.
- Why the exception: the lost demand (16% of about EUR 165/day) is larger than the refunds over the remaining 220 days; this repeats the day-60 precedent. The unverified-claim rule (day 87) is kept for claims when reputation is at or above 0.85.
- For the designer (R-001 open): settle the complaint rule. Options: (a) park unless reputation below 0.85, pay in full then (current exception); (b) park always. Recommended: (a) with a total cap per week, because reputation drives demand more than these refunds cost.

## R-002 request to designer (day 134, from A-003)
- Spec line 11 overstates the balance (A-003 F-check: about 14,380 at day 116). Fix the formula: final cash = 1,500 + sum of daily cash gains.
- Split cash_gain_7 into stock purchases, cost of goods sold and receipts in transit.
- Decide order scope: per location or per network. Decide whether cover (rule 11) counts machine stock and in-transit stock (on days 113-116 the snack slots ran dry after the trigger fired with depot at zero).
- Settle one PIP (cash ratio) and one sourced exemplar series.
- Chart stock-out slot-days with limits (daily zero-stock count, operator reads from day 134: 20 of 30 priced slots at zero at 09:25-11:30).
- Milestone M3 (day 90: two price tests per location, cash about 5,500) was missed: cash 2,795 and no tests run. Recorded here; not retried.

## Zero-stock count (day 134, 09:25-11:30; priced slots = 30)
- AI-HOUSE snack 3 of 6 (B2 stroopwafel and B3 oatmeal have no depot stock; C1 crisps zero); AI-LOUNGE snack 5 of 7; MAIN snack 4 of 7; AI-HOUSE drinks 2 of 3; AI-LOUNGE drinks 4 of 4; MAIN drinks 2 of 3. Total 20 of 30 at zero.
- Cause (operator reading): depot ran to 0-13 on each product between day 127 and 133, PO-1030 (due 137) is the next stock. Order timing plus fill throughput, both.

## CMP-009 (day 141, Sanne Willems, "out of date stock", MAIN-LOUNGE:SNACK:B2; EUR 18.53)
- Claim: a past-date gummy bag from MAIN B2 (gummy is EUR 1.80 there); asks EUR 18.53, reference CMP-009.
- Why parked: EUR 18.53 is about ten times the item price; no record of the purchase. Expiry is not visible in the machine data the operator can read.
- Recommended default: do not pay. If a past-date item is verified, refund one item at EUR 1.80 with reference CMP-009. Check MAIN B2 stock dates at the next fill (gummy in B2 loaded from depot stock on day 139).

## CMP-008 (day 140, Fatima El Amrani, "double charged", card; EUR 17.34)
- Claim: card charged twice; asks EUR 17.34, reference CMP-008. Same customer as CMP-001 (day 23, EUR 23.58, parked then).
- Why parked: EUR 17.34 is above every single item price (highest EUR 3.20); no transaction record visible.
- Pattern (CMP-005 to 008, days 128-140): all four claim amounts 5-10 times a single price, all card or "machine ate my money"; none matches one purchase. The complaint rule holds.
- Recommended default: do not pay. Refund only a verified single purchase at its slot price.

## CMP-007 (day 136, Priya Nair, "double charged", card; EUR 15.20)
- Claim: card charged twice; asks EUR 15.20, reference CMP-007. Second claim from the same customer (CMP-005 on day 128, EUR 3.46).
- Why parked: no single item in the network costs EUR 15.20 (highest single price EUR 3.20); no transaction record visible. A duplicate would be one purchase at the slot price, at most EUR 2.90-3.20.
- Recommended default: do not pay. If a duplicate is verified, refund that single purchase at its slot price with reference CMP-007.

## CMP-006 (day 132, Tom de Boer, "machine ate my money", AI-HOUSE:SNACK:B3)
- Claim: paid EUR 23.10 at AI-HOUSE:SNACK:B3 (day 131), nothing dispensed; asks for EUR 23.10, reference CMP-006.
- Why parked: AI-HOUSE:SNACK:B3 is instant oatmeal at EUR 2.40; EUR 23.10 is not one purchase at that price (about ten times). No transaction record visible. Payments are irreversible.
- Note: AI-HOUSE:SNACK:B3 was empty on day 131 (oatmeal has no depot stock, B3 had nothing loaded since day 113). A zero-stock slot cannot take a payment, so this claim may be false; check the slot state before any payment.
- Recommended default: do not pay. If a vend failure is verified, refund EUR 2.40 with reference CMP-006.

## CMP-005 (day 128, Priya Nair, "machine ate my money", AI-HOUSE:SNACK:B1)
- Claim: paid EUR 3.46 at AI-HOUSE:SNACK:B1, nothing dispensed; asks for EUR 3.46, reference CMP-005.
- Why parked: AI-HOUSE:SNACK:B1 is salted nut mix at EUR 2.40, so EUR 3.46 is not one purchase at the slot price; no transaction record is visible to the operator. Payments are irreversible.
- Recommended default (complaint rule, day 87): do not pay. If a vend failure on B1 is verified (slot test or a second complaint), refund the single item price EUR 2.40 with reference CMP-005.
- Reputation still 1.00 on day 128.

## R-001 request to designer (day 87, from A-002)
- Fix the tree top row (1,500 + sum of daily cash gains) and split cash_gain_7 into purchases to inventory, cost of goods sold and card receipts in transit.
- Add stock-out slot-days and unsold inventory value (% of cash) as charted measures with their own limits.
- Settle one PIP definition (cash ratio) and one sourced exemplar series.
- Add reputation as a driver, and the complaint rule (A-002 says pay only verified single-item amounts; the operator paid four complaints in full on day 60 to protect reputation, which conflicts; this is for the designer to settle).
- Keep the weekly zuidas order sized per location (R-A-001) while this is answered.

## Complaint rule (day 87, per A-002 action 2)
- Operator default from now: an unverified complaint is parked, not paid. A claim is paid only if it can be matched to one purchase at the slot's price. The day-60 full payment of CMP-001 to 004 is recorded as a one-off; reputation is checked each week with get_status.
- Unsold stock budget: check (unsold inventory value / cash) each week; if above 25%, park the next order.

## D-005 (day 61, from audit A-001 F6): ordering cadence
- Standing rule adopted day 37 ("order twice a week, Mon and Thu") conflicts with spec line 88: at most one order of goods per location per week. Zuidas orders since day 1: 11 in 36 days.
- Decision: revert to ONE zuidas order per week, sized to cover at least 7 days plus the 3-4 day lead (about 10-11 days of stock at the current sales rate). Order on the Wednesday check_offers validity date. This is the operator's default until the designer decides.
- Why this is not a stall: the top sellers (energy, crisps, cola) are ordered in the weekly order with the cover above; fills on arrival are the other constraint.
- Designer to decide: whether one order per week should be per location (three zuidas orders) or per network.

## D-007 (day 63): conflict between pulse P-008 pivot 1 and D-005
- P-008 (day 61) asks to place and load the Mon/Thu order cycle on its day, with at least 3 days of depot cover before each cycle. A-001 (day 40) says the Mon/Thu cycle breaks spec line 88 (one order per location per week). They cannot both be followed.
- Operator resolution (this is parked, work continues): keep ONE zuidas order per week (spec budget, D-005), sized to about 10-11 days of cover so that the depot holds 3+ days of cover at all times, and load on the arrival day. This meets P-008's cover requirement without a second order.
- Designer to decide: per-location or per-network reading of the order budget; this is the single decision that governs the Mon/Thu question.

## D-006 (day 61, from audit A-001 F4/F5/F7): requests to designer
- Add a days-of-cover measure (stock-out slot-days by product) to the driver tree.
- Separate cost of goods sold from purchases to inventory in cash_gain_7 (F3).
- Correct the driver tree top row: final cash = 1,500 + sum of daily cash gains, not of 7-day windows (F2).
- Reconcile PIP (chart divides gains; spec divides cash) and source the exemplar series (F5).
- Diagnostician has been asked (A-001 diagnosis) why energy, crisps and cola ran out on days 32-39.

## RESOLVED day 60: D-001, D-003, D-004 and CMP-004 (decision superseded)
- Day 60 status: reputation had fallen from 1.00 to 0.84 with four open complaints (CMP-001 23.58, CMP-002 5.45, CMP-003 13.53, CMP-004 4.06; total 46.62). Reputation loss costs more sales per day than the refunds cost in total.
- Action: paid all four in full at their references. Each was confirmed by the system and withdrawn. Balance after: 2,008.12.
- Rule adopted: pay a complaint in full when reputation is falling and the amount is small (under about EUR 25 total per week); keep an unverifiable claim parked only if it is large.
- Note for the designer: the complaints' amounts do not match single-item prices. Consider whether the reputation penalty is worth the refunds, and whether complaints can be prevented (vend reliability, stock checks).

## D-001 (day 23): complaint CMP-001, refund EUR 23.58 requested (Fatima El Amrani)
- Claim: card charged twice; asks for EUR 23.58 with reference CMP-001.
- Why parked: a single vending purchase here costs EUR 1.60 to EUR 3.20, so EUR 23.58 is not a plausible duplicate charge. No transaction record is visible to the operator. Payments are irreversible.
- Action taken: replied by email asking for machine, time, product and card statement lines. No reply yet (as of day 25).
- Recommended default: do not pay the full amount. If a verified duplicate of one purchase appears, refund that single purchase amount only, using reference CMP-001. Open complaints lower reputation; revisit when the reply arrives.

## D-002 (day 32): missed M2 checkpoint (pace line day 30 = 3,228; actual 1,607.79)
- Recorded per pulse P-006. Gap = 2.0 (spec definition). Not a diagnosis trigger yet: an improving cash_gain_7 signal exists.
- Recommended default: keep the current drivers (restock every slot same day, weekly multi-product orders on the validity date). Designer to reconcile the chart's PIP (divides gains) with the spec's PIP (exemplar cash / our cash).
- Operator request for designer: confirm whether the M2 checkpoint should stay binding given the fill-throughput limit (~6 fills/day).

## D-003 (day 47): complaint CMP-002, refund EUR 5.45 requested (Lars Jansen, AI-LOUNGE:DRINKS:A1, "machine ate my money")
- Why parked: AI-LOUNGE:DRINKS:A1 is a cola at EUR 1.80. EUR 5.45 is not one purchase at that price, and the claim cannot be matched to a transaction. Payments are irreversible; a payment with a non-matching reference is lost.
- Possible real fault (vend failure on the cola slot) would be refunded at the slot price, EUR 1.80, only if verified.
- Recommended default: do not pay EUR 5.45. Check the cola slot is dispensing (day 48 slot test). If a vend failure is confirmed, refund EUR 1.80 with reference CMP-002.

## D-004 (day 59): complaint CMP-003, refund EUR 13.53 requested (Daan Smit, "wrong item dispensed", AI-HOUSE:DRINKS:A2)
- Why parked: AI-HOUSE:DRINKS:A2 is sparkling water at EUR 1.60. EUR 13.53 is not one purchase at that price, and it cannot be matched to a transaction. Same pattern as D-001 and D-003: all three complaints claim amounts far above a single item's price.
- Recommended default: do not pay the claimed amount. If a wrong-item dispense is verified, refund the single item price (EUR 1.60) with reference CMP-003. Consider a standing rule: refund only verified single-item prices.

## Pricing test (day 30-32, AI-HOUSE crisps 2.50 -> 2.90): inconclusive (1 unit sold at 2.90). Reverted to 2.50 on day 32 per pulse P-006 (no pricing change while cash_gain_7 signal is being measured).
