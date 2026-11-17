# Decisions queue

## D-001 (day 30): M1 milestone missed; designer review requested
- Milestone M1 passes when cash >= 3,228 on day 30. Actual: EUR 1,378.16 (day 30). Gap to exemplar path: about 2.3x.
- Cause (operator reading): trip capacity is the binding constraint (5 fills/day x 10 units for large rows; 18 for small A/B rows). Every slot sells out within about 1 to 2 days, so capacity, not price, limits sales. Also stock-outs from thin orders on days 13 to 17, and failed trips on day 21 when storage was not checked.
- Recommended default (operator's, work continues): keep the current cadence, put small-product stock in A/B rows where margin per trip is higher, keep prices at or above cost plus margin, buy weekly from Zuidas (about 2-day delivery). Bakker is unreliable (PO-1004 arrived 14 days late).
- Ask of the designer: confirm the M1 target is reachable under the 5-trip cap, or reset the day-30 checkpoint and the trip plan. Decide whether to add duplicate slots (capacity) where stock-outs are proven, since spec says duplicates add capacity, not customers.
- Default if no reply: continue as above; no change to spec, checks or budgets by the operator.

## D-002 (day 86): day-90 pace checkpoint review (from pulse P-012, day 85)
- Cash at d85 €2,807 (d86 €2,657 after order and fees) against ~5,470 on day 90. Recent pace ~350/week on cash_gain_7; the pace needed is ~€37/day. Gap cannot close by day 90 at current throughput (5 trips/day, about 50 large or 90 small units/day).
- Ask of the designer: review the day-90 checkpoint (reset or keep) and the fill driver (fills per day, storage per slot) given the trip limit. Human decision on reset (see D-001).
- Recommended default: keep the current cadence (twice-weekly Zuidas orders, sold-out-first fills within 5 trips, weekend stock not bought for). No change to spec, checks or budgets by the operator.
- Default if no reply: continue as above.

## D-003 (day 101): supplier lead-time anomaly (Zuidas PO-1031, Bakker PO-1032)
- PO-1031 (Zuidas, cola 40, nuts 30, energy 20, €87.20) quoted delivery day 111 (10 days). Zuidas was 2-4 days in the earlier offer periods; PO-1029 and PO-1030 took 3-4 days. PO-1032 (Bakker, cola 40, crisps 20, €66.00, minimum €60) quoted day 113 (12 days). Bakker was 14 days late on PO-1004 earlier.
- Effect: cola (the high-volume drink) will have no stock in storage from about day 101 to day 111; crisps and energy cover is short until PO-1030 (day 102).
- Ask of the designer: confirm whether lead times are rising (a supplier-side change) or these are single anomalies; review the order-timing driver (lead time per supplier) in the next redesign.
- Recommended default: keep ordering Zuidas for the main lines, use Bakker only for a hedge on the single fastest-selling line, and place orders at least 10 days before a stock-out until a normal lead time is observed. No change to spec or budgets by the operator.
- Addendum (day 135): further anomalies since D-003. PO-1046 (Zuidas, nuts 18, crisps 30, d132) quoted delivery d141, a 9-day lead. Zuidas otherwise ran 4 days (PO-1038 to PO-1045, mostly 1 day late against the due day). Bakker not used since PO-1032. Crisps and nuts out of storage until PO-1047 (crisps 30, d138) and PO-1046 (d141). Input for the next redesign on lead time per supplier.

## D-004 (day 131): pulse P-018 pivot "6th trip whenever a sold-out slot has stock" vs rule 8
- Pulse P-018 (day 128) pivot 2 asks for a 6th fill whenever a sold-out slot has storage stock. Rule 8 allows a 6th fill only on days 110 to 125 (the test window), and the 5-trip cap otherwise.
- Test result so far: the business tools allowed 6 fills on days 117, 118, 119, 124, 125 (no unpaid day, no read or price change skipped). Sold-out slots still waited on storage stock after 5 fills on several days after d125 (e.g. d128: five sold-out slots with no trip left).
- Operator action: rule 8 kept as written (5 trips after d125). Pivot not adopted as a rule change, because only the designer changes rules.
- Ask of the designer: decide whether the 6th fill becomes permanent (with the price, unpaid-day and read checks) or stays a test. Recommended default: keep 5 trips and the test result as the record until the designer decides.
- Default if no reply: continue at 5 trips.

## D-005 (day 154): one consolidated question for the designer, from audit A-003
- Open items, asked once: (a) D-004 (6th fill: now moot since the test ended d125; the 5-trip cap stays); (b) the R-A-002 revert clause (its prediction 11.0 by d125 was not met: 8.1 on d141, 9.38 in the R-P-020 read; the clause needs a clear test); (c) the D-P-020 storage and cover driver: operator now applies rule 13 (6 days of cover at effective lead 5); audit A-003 asks for 7 days cover ordered twice a week. The operator keeps rule 13 as written and records the 7-day suggestion here.
- Test data for (c): operator log shows sold-out selling slots every day from d117; energy sells about 20 a day on hot days against the 12 a day used for cover; crisps about 10; cola about 10; stock-outs fall when cover reaches the 6-day rule (d151 onward: check the next audit).
- Aim: audit A-003 says the 61,219 aim will not be reached on current drivers (about 13,700 projected at day 365). Checkpoint reset (D-001, D-002) stays with the human.
- Charts still missing: fills, sold-out slot-days, storage per sold-out slot, lead time, margin, COGS, marketing, the spec's pace line; PIP basis (cash ratio on a labelled exemplar path).
- Default if no reply: spec v5 and operator rules v4 as written; no rule change by the operator.

## CMP-004 (re-entered from the day-45 D-002 collision, audit A-003 item 3b)
- CMP-004 (day 45 complaint, €16.58) was declined at the time; the complaint policy was changed on day 59 (pay every open CMP- claim in full). The day-45 entry is recorded here under its own number. Complaint rule (written once, applied to every claim): pay the exact CMP- reference in full if under €20, log the claim against the slot price. CMP-011 (day 149, €4.68) was paid under this rule.

## D-006 (day 167): trip-cap conflict raised by pulse P-023 (day 164)
- P-023 says the spec calls the trip cap non-binding (day-125 test), while the log shows five fills every day from d157 to d167, sold-out selling slots left with no trip left, and storage stock waiting in the depot for those slots (e.g. d165 crisps 50 in storage, 0 loaded; d167 cola and crisps stock while sold-out slots had no trip).
- Operator facts: rule 8 (5 trips/day) is kept; the 6th fill test ended d125; the 6th-fill failed call on d159 used a slot's time.
- Ask of the designer: decide whether the trip cap of 5 is the binding driver (and whether rule 8 should lift it), or whether the spec's non-binding statement should be corrected. The operator does not change rule 8 or the spec.
- Recommended default: keep 5 trips and the priority fill order (sold-out with stock first, by margin per trip) until the designer decides.
- Default if no reply: continue at 5 trips.
- Update (day 180): R-P-024 retired the flat cap (spec v6, operator rules v5). The operator now fills while a sold-out slot holds storage stock, until reads and price changes are done or the 8-hour day runs out. Days 180 and 181 ran 8 and 7 fills; the time budget set the stop. D-006 is answered by R-P-024; this entry is closed unless the designer says otherwise.

## D-007 (day 182): pace gap, for the human
- Cash €6,161 at day 182 (after PO-1074/PO-1075 and day-181 sales). Pulse P-026 puts the linear need at about €2,080 a week to reach the 61,219 aim by day 365, against about €250 a week now. Audit A-003 projects about €13,700 at day 365 on the old drivers.
- Ask: confirm whether the 61,219 aim or the day-180 checkpoint (about 12,000) is still the target, or reset it (D-001 and D-002 also wait on this). The operator keeps running the current plan meanwhile.
- Recommended default: keep the current plan (fills while sold-out with stock, six-day cover, check_offers before each order) and reset the checkpoint to the realistic path.
- Default if no reply: continue as above.

## D-008 (day 193): CMP-013 over the €20 limit (park under operator rule 11)
- Claim: Daan Smit, out-of-date item from AI-HOUSE:SNACK:C1 (day 192), refund requested €21.30, reference CMP-013.
- Rule 11 (operator v5) says pay CMP- claims in full only under €20; larger claims are parked. The day-59 complaint policy (D-002, pay every open claim in full) is the older rule. The two conflict at this amount.
- Recommended default: pay the exact CMP-013 amount in full, because the item was out of date (a seller fault), the claim is exact, and the cost is small against reputation. Designer or human to confirm the threshold.
- Default if no reply: park; the operator will not pay until the threshold is settled.

## Update (day 197, per audit A-004)
- D-007 (pace gap, for the human) is still open. A-004 says the 61,219 aim is not reachable at the post-day-180 rate (about 15,000 to 17,000 at day 365). Human to decide whether to reset the checkpoint table and the day-365 expectation. The operator keeps the current plan; no goal change by the operator.
- The 8-hour day question is unanswered: is it a business rule or a self-set budget? It sets the fill ceiling (6 to 8 fills a day). Human or designer to answer before the next redesign. Operator test: log whether a ninth fill fits when reads and price changes finish early.
- D-001 and D-002 (checkpoints) wait on the same human decision as D-007.
- CMP-014 (Tom de Boer, €4.95, wrong item from AI-HOUSE:DRINKS:B1) paid in full on d197 under rule 11 (exact reference; customer withdrew the complaint).
- New (d197): PO-1086 (zuidas, cola 40, crisps 30, oat 25, sparkling 20; paid €133.35) quoted delivery day 208, an 11-day lead, against the 4-day quotes on PO-1084 and PO-1085. Check_offers d197 (valid through d203) was run first. Input for the lead-time-per-supplier question (D-003 addendum). Cola, crisps and oat cover after PO-1085 (due d198) may run short before d208; the operator will consider a second supplier only on a designer or human decision.
- Sales dropped on d196 (18 units, €40.30) against about 75 a day on d193 to d195; reputation fell from 0.96 to 0.92 on d197. Logged for the next read; no rule change.

## D-009 (day 215): CMP-016 over the €20 limit (park under operator rule 11)
- Claim: Chloe Martin, out-of-date item from AI-LOUNGE:SNACK:A1 (milk chocolate line, day 214), refund €21.39, reference CMP-016.
- Same question as D-008 (CMP-013, Daan Smit, €21.30): rule 11 (v5) parks claims of €20 or more; the day-59 policy (pay every open claim) is older. Both are out-of-date stock claims (seller fault).
- Recommended default: pay both in full, exact references, as the day-59 policy says; the designer or human to confirm the threshold. Operator default per rule 11 is to park. Both amounts (€42.69 together) are small against reputation (0.92 on d197).
- Also: the AI-LOUNGE:SNACK:A1 chocolate line is priced at €1.90 with zero stock and no storage stock for it. The operator will not restock it until the human or designer decides whether the line stays in the mix.
- Default if no reply: park; the operator will not pay until the threshold is settled.

## D-010 (day 249): one request to the human, from audit A-005 (8-hour day and checkpoint)
- Question 1, the 8-hour day: is it a business rule or a self-set budget? Reading A: a fixed rule of the business, so each day gives 8 hours: about 9 fills at 45 minutes each, plus reads at 25 minutes. Reading B: a self-set budget that the operator can widen (for example by starting at 09:00 with reads done in parallel, or by shortening the read time). Implication: at 9 fills a day the fill ceiling is about 9 machine loads. Current revenue: 7-day window to d248 €1,059.70 (about €151 a day).
- Question 2, the checkpoint and the aim: the 61,219 aim and the day-180 checkpoint (about 12,000) are not reachable at the current rate. A-005 projects about €15,000 to €17,000 on day 365. Confirm whether the aim is kept or reset, and the day-365 expectation to plan against.
- Cash position: €9,672 at 09:00 on d249; €9,037 on d242 (7-day change +€634.75, after stock purchases of about €640 over the same window). Stock at cost about €306 on d249.
- Footfall test running: mail at MAIN-LOUNGE on d249 (€2.00, traffic multiplier 1.18, 3-day bonus). Payback read due on d256 (14-day sales by slot against the 14 days before).
- Recommended default: keep the current plan (fills to sold-out slots first, 6-day cover, check_offers before each order, one location test per 14 days), and reset the day-365 expectation to the realistic path (about €15,000 to €17,000) pending the human's answer. The operator does not change the 8-hour day or the aim itself.
- Default if no reply: continue as above; no change to the 8-hour day, the aim or the checkpoint by the operator.

## D-011 (day 258): complaint amount to check (CMP-019, rule 11 applied)
- CMP-019 (Priya Nair, out-of-date item from AI-LOUNGE:DRINKS:A1 sparkling, list price €1.60) claimed €14.69 under the exact reference. Rule 11 (under €20, exact reference) was applied: paid €14.69 on d258; the customer withdrew the complaint.
- Flag: €14.69 is about nine times the price of one bottle. Possible that the claim covers more than one unit, or that the claim is inflated. Not verified against the sales ledger (the operator cannot see the purchase record).
- Also: CMP-018 (same customer, double charge, €8.64) was paid in full on d257.
- Recommended default: keep rule 11 as written (pay exact references under €20 in full), and ask the designer whether the claim amount should be checked against a unit price before payment. No action needed from the human unless the amount is shown to be wrong.
