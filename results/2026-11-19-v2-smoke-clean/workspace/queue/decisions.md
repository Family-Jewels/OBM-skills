# Parked decisions

## D-005 (day 32): CMP-003 claim EUR 3.92 vs slot price EUR 2.50 (out-of-date crisps, MAIN-LOUNGE:SNACK:C1)
- Paid EUR 2.50 (one item) under CMP-003. Balance of claim parked. Pattern: three out-of-date claims (CMP-001/002/003) all over the single-item price; the crisps lot is the oldest stock (PO-1001, delivered d15). Recommended: check date stock on crisps; consider rotating oldest crisps out. Decision for operator review.

## D-007 (day 38): CMP-005 double-charge claim EUR 16.55
- Paid EUR 2.50 (highest single-item price in the network) under CMP-005; remainder EUR 14.05 parked. Claim cannot be matched to any transaction; no double charge is visible in the sales data. Recommended: no further payment without a matching transaction.

## D-008 (day 46): CMP-006 double-charge claim EUR 24.48
- Paid EUR 2.50 under CMP-006; remainder EUR 21.98 parked. Same as D-007. Six complaints so far (CMP-001..006), all claims 6-10x the item price. Recommend the designer review complaint policy; no further payments beyond one item without a transaction match.

## D-013 (day 80): CMP-009 "wrong item" claim EUR 15.33 vs slot price EUR 2.00 (MAIN-LOUNGE:DRINKS:B2)
- Paid EUR 2.00 under CMP-009; remainder EUR 13.33 parked. Same policy as D-003..D-010.

## D-012 (day 76): oat price to EUR 2.10 (second cost-guardrail correction, disclosed)
- PO-1019 (d75, delivery d77) bought oat at EUR 1.57 per unit. Guardrail (unit cost <= 0.75 x price) needs price >= 2.10. Raised all six oat slots to 2.10 (+10.5%, within the 15% weekly limit): AI-LOUNGE A2, A3, B1, B2 (E-005 slice), AI-HOUSE A3 and MAIN A3 (control). I should have checked oat cost before buying at 1.57 (cf. D-011). Designer/auditor to note: E-005 slice price moved twice (1.80 to 1.90 on d66, to 2.10 on d76).

## D-011 (day 66): oat price move on E-005 slice (disclosed)
- To meet the cost guardrail (unit cost 1.41 must be <= 0.75 x price), I raised oat-latte to EUR 1.90 in AI-LOUNGE:DRINKS:B2 (slice, E-005's changed slot), AI-HOUSE:DRINKS:A3 and MAIN-LOUNGE:DRINKS:A3 (control). The slice price change is a second lever on E-005 and may confound it. Designer/auditor to decide whether E-005 needs a re-read or restart. I have not judged the experiment.

## D-010 (day 63): CMP-008 double-charge claim EUR 23.96
- Paid EUR 2.50 under CMP-008; remainder EUR 21.46 parked. Same policy as D-007/D-008. Eight complaints so far; all unmatched.

## D-009 (day 52): CMP-007 "wrong item" claim EUR 12.43 vs slot price EUR 1.50 (AI-LOUNGE:SNACK:B1)
- Paid EUR 1.50 under CMP-007; remainder parked. Note: AI-LOUNGE:SNACK:B1 was empty at d49 and reloaded after; a wrong-item dispense is possible if a slot held a leftover SKU. Check B1 contents on the next visit.

## D-006 (day 34): CMP-004 claim EUR 23.81 vs slot price EUR 2.50 (MAIN-LOUNGE:SNACK:C1, "machine ate my money")
- Paid EUR 2.50 under CMP-004. Balance parked. Note: C1 (crisps, MAIN) has now two complaints (CMP-003, CMP-004). Recommend checking C1 vend mechanism / stock (large-item row) and its date stock.

## D-004 (day 31): CMP-002 claim EUR 21.42 vs slot price EUR 1.50
- Daan Smit says an item from AI-HOUSE:DRINKS:A1 was past its date; claims EUR 21.42. Paid EUR 1.50 (one item's price) under CMP-002. Same reasoning as D-003. Stock is fresh (Zuidas PO-1005/1007); no date-expiry in the machines' data. Recommended default: no further payment without evidence.

## D-003 (day 28): CMP-001 refund claim EUR 23.08 vs slot price EUR 1.80
- Claimant Priya Nair says she paid EUR 23.08 at MAIN-LOUNGE:DRINKS:A3 (price EUR 1.80) and got nothing.
- Paid EUR 1.80 under CMP-001 (one vend's worth). Complaint stays open (claimant still EUR 21.28 short).
- Recommended default: do not pay the balance without a receipt or matching transaction; the claim does not match the machine's price. Revisit if the sales ledger shows a larger failed vend.

**Update d23: checker voided E-002 and E-003 after three failed fidelity checks (F-E-002-3, F-E-003-3). Neither experiment will run; D-001 and D-002 are closed as moot unless the designer re-issues them. Applied lines stay blank.** Note for designer: E-002 needs marketing in the ground-truth snapshot; E-003 needs its baseline to match the Start (coffee already in MAIN-LOUNGE:DRINKS:A3 since d17).

## D-001 (day 15): E-002 print campaign cannot run within its guardrail yet
- Experiment E-002 Start is point 3 (day 15). Its change is one moderate print campaign per point at AI-LOUNGE (print cost EUR 8).
- Guardrail: marketing spend on the slice <= 10% of AI-LOUNGE's last-7-day revenue. Last 7 days AI-LOUNGE revenue = EUR 54.50, so the cap is EUR 5.45. One print (EUR 8) breaches it.
- Applied is not written. The campaign is not run. Experiment clock has not started.
- Recommended default: wait until AI-LOUNGE 7-day revenue reaches EUR 80+ (cap >= EUR 8), then run the first print on the day that holds, and write Applied with that day. Alternative: the designer or auditor re-states the guardrail for an EUR 80 print when revenue is low. Not my call to change the guardrail.
- Update d22: the E-002 print campaign is still parked under the same guardrail (AI-LOUNGE 7-day revenue still below EUR 80).

## D-002 (day 22): E-003 swap cannot be made as written
- E-003 Start is point 4 (day 22). Change: two of ten MAIN-LOUNGE:DRINKS slots to the coffee SKU.
- Current state: MAIN-LOUNGE:DRINKS:A3 already holds oat-latte (loaded d17, before Start, so the baseline is already partly changed). Other drink slots B1-D3 are empty. Depot holds no oat-latte (all 30 from PO-1001 loaded). The only available supplier for oat-latte is zuidas-groothandel at 1.57; a unit price of 1.57 requires a sell price of at least 2.04 to meet the 1.3x guardrail.
- Applied is not written. The swap is not made.
- Recommended default: the designer re-states E-003 against the actual baseline (e.g., one slot becomes coffee, or the machine is restocked to 10 slots with coffee on both slots from day 22). Alternatively: order 20 oat-latte from zuidas (EUR ~31) and set the second slot to 2.10 when it is loaded, then write Applied. I will not make a price change that confounds the mix lever without a decision.
- Note: the checker's F-E-002-1 still open. Reply through the record, not by breaching the guardrail.
