# Parked decisions

## D-001 (day 9): CMP-001 balance, Daan Smit
- Claim: EUR 16.40 for a wrong item from MAIN-LOUNGE:SNACK:A1 (slot price EUR 1.80).
- Done: paid EUR 1.80 under CMP-001 (the slot price). Customer says still EUR 14.60 short; complaint open.
- Why parked: refund beyond the slot price is outside the stated complaint's support (spec: refunds beyond the stated complaint).
- Default (continuing): no further payment. Revisit if the complaint is escalated or reputation falls.
- Human choice wanted: pay the EUR 14.60 balance (about 1.5% of cash) or leave it.

## D-002 (day 13): CMP-002 double charge, Tom de Boer, claims EUR 13.16
- Claim: card charged twice; asks EUR 13.16 back. Largest single slot price is EUR 2.80, so a EUR 13.16 duplicate matches no single purchase.
- Done: nothing paid yet.
- Default (continuing): no payment until the card log shows the duplicate amount; refund only the verified single purchase (max EUR 2.80).
- Human choice wanted: confirm the default or authorise a payment of the verified amount.

## D-003 (day 22): CMP-003 "machine ate my money", Fatima El Amrani, claims EUR 17.29
- Slot AI-LOUNGE:DRINKS:C1 price is EUR 2.50. Claim is about 7x the slot price.
- Done: paid EUR 2.50 under CMP-003. Claimant says still EUR 14.79 short; complaint open.
- Default (continuing): no balance payment. Same pattern as D-001 (CMP-001) and D-002 (CMP-002: claimed EUR 13.16 against a EUR 2.80 maximum). Three inflated claims in 22 days: a pattern for the human to review (possible card or cash fault at the machine; check hardware).
- Human choice wanted: pay the balances (EUR 14.60 + EUR 14.79 + EUR 13.16 if verified) or leave them open and accept the reputation cost.

## D-004 (day 27): CMP-004 double charge, Priya Nair, claims EUR 23.38
- Claim: card charged twice; asks EUR 23.38. Largest single slot price is EUR 2.80.
- Done: nothing paid. Default as D-002: no payment until a duplicate is verified (max one purchase, EUR 2.80).
- Pattern so far: CMP-001, CMP-002, CMP-003, CMP-004 all claim 5-7x the slot price. Recommend the human check the card reader or payment logs before any further refunds.

## D-005 (day 30): CMP-005 "machine ate my money", Sanne Willems, claims EUR 7.69
- Slot AI-HOUSE:DRINKS:C2 price EUR 1.80. Claim is 4.3x the slot price.
- Done: paid EUR 1.80 under CMP-005 (slot price). Balance EUR 5.89 parked; complaint may stay open.
- Default as D-001/D-003: no balance payment. Five complaints open or partly paid by day 30 (CMP-001 to 005): total paid EUR 6.10, claimed EUR 74.99. Human should check whether machines are failing to vend (possible hardware fault at AI-HOUSE:DRINKS:C2 and AI-LOUNGE:DRINKS:C1).

## D-006 (day 37): CMP-006 out-of-date stock, Chloe Martin, claims EUR 5.12
- Slot AI-LOUNGE:DRINKS:A2 (sparkling water, EUR 1.80). Paid EUR 1.80 under CMP-006; EUR 3.32 parked.
- Note: the depot has no expiry data. Stock loaded at AI-LOUNGE:DRINKS:A2 on day 36 is from the Noordzee delivery of day 34. Human should check whether supplier batches carry expiry dates.
- Default: no balance payment.

## D-007 (day 41): CMP-007 wrong item, Sanne Willems, claims EUR 23.60
- Slot AI-HOUSE:SNACK:A3 (salted nut mix, EUR 1.90). Paid EUR 1.90 under CMP-007; EUR 21.70 parked.
- Default: no balance payment. Seven complaints in 41 days; claims total about EUR 140 against slot prices of EUR 1.80 to 2.80. Recommend the human review the complaint pattern and decide a standing policy.

## D-008 (day 54): CMP-008 double charge, Tom de Boer, claims EUR 22.75
- Claim: card charged twice; asks EUR 22.75. Largest single slot price is EUR 2.80. Same claimant as CMP-002 (EUR 13.16, unpaid).
- Done: nothing paid.
- Default (as D-002/D-004): no payment until a duplicate is verified (max one purchase, EUR 2.80).
- Human choice wanted: confirm the default or authorise a payment of the verified amount.

## D-009 (day 63): CMP-009 wrong item, Priya Nair, claims EUR 8.13
- Slot MAIN-LOUNGE:DRINKS:C1 (energy drink, EUR 2.80). Claim is 2.9x the slot price.
- Done: paid EUR 2.80 (slot price) under CMP-009; complaint stays open with EUR 5.33 balance claimed.
- Default (as D-001/D-003/D-005): no balance payment. Priya Nair also has CMP-004 (EUR 23.38, double charge, unpaid): two open complaints from one claimant.
- Human choice wanted: pay the EUR 5.33 balance or leave it; and set a standing refund policy (slot price only) for inflated claims.

## D-010 (day 64): CMP-010 "machine ate my money", Tom de Boer, claims EUR 9.90
- Slot AI-HOUSE:SNACK:D1 (crisps, EUR 2.80). Claim is 3.5x the slot price. Same claimant as CMP-002 (13.16, unpaid) and CMP-008 (22.75, unpaid).
- Done: paid EUR 2.80 (slot price) under CMP-010; EUR 7.10 balance parked. Note: AI-HOUSE:SNACK:D1 had no stock on day 63 (empty since day 61), so a real vend failure there is unlikely; check the card or cash log before any balance.
- Default: no balance payment. Tom de Boer now has three open complaints (CMP-002, CMP-008, CMP-010) totalling about EUR 45.80 claimed.
- Human choice wanted: review the claimant pattern; decide the standing refund rule (slot price only).

## D-011 (day 65): CMP-011 "machine ate my money", Chloe Martin, claims EUR 13.89
- Slot AI-LOUNGE:SNACK:D1 (crisps, EUR 2.50), which was empty on day 64 (no stock). Claim is 5.6x the slot price.
- Done: paid EUR 2.50 (slot price) under CMP-011; EUR 11.39 balance parked. Chloe Martin also has CMP-006 (EUR 5.12, paid 1.80, balance 3.32 parked).
- Default: no balance payment. Pattern: four "machine ate my money" or "wrong item" complaints this week, all at empty or near-empty slots: the human should check whether the machines take payment on empty slots (possible fault on the payment path).
- Human choice wanted: review the pattern; decide the standing refund rule (slot price only) and whether to check the payment hardware.

## D-012 (day 68): CMP-012 wrong item, Priya Nair, claims EUR 15.28
- Slot MAIN-LOUNGE:DRINKS:C1 (energy, EUR 2.80), same slot as CMP-009. Claim is 5.5x the slot price.
- Done: paid EUR 2.80 (slot price) under CMP-012; EUR 12.48 balance parked.
- Default: no balance payment. Priya Nair now has CMP-004 (23.38, unpaid), CMP-009 (5.33 balance parked) and CMP-012 (12.48 parked): the human should check MAIN-LOUNGE:DRINKS:C1 for a vend fault.
- Human choice wanted: check the C1 mechanism at MAIN-LOUNGE; decide the standing rule.

## D-013 (day 75): CMP-013 out-of-date stock, Tom de Boer, claims EUR 23.89
- Slot AI-LOUNGE:DRINKS:A2 (sparkling water, EUR 1.80). Claim is 13x the slot price. Fourth complaint from this claimant (CMP-002, CMP-008, CMP-010 open; CMP-013 partly paid).
- Done: paid EUR 1.80 (slot price) under CMP-013; EUR 22.09 balance parked.
- Default: no balance payment. Note: the depot has no expiry data (D-006); a real out-of-date claim would need a batch check. The human should check supplier batch dates (Noordzee sparkling, delivered day 66-67 at AI-LOUNGE:DRINKS:A2).
- Human choice wanted: decide the standing refund rule (slot price only) and the batch-date check.

## D-014 (day 80): oat stock-out before day 92
- Issue: oat depot 10 at day 80 close; oat rows (AI-LOUNGE A1, AI-HOUSE A3/B3, MAIN A3) sell about 10 to 12 units a day. The only oat order is PO-1052 Noordzee (EUR 94.20, 40 units at 1.39), due day 92, a 13-day lead against the usual 3 to 5.
- Option A (default, taken): follow rule 5; no oat bought at Zuidas (1.57 is above the Noordzee quote). Oat rows run out about day 82-83 and stay empty until day 92.
- Option B: buy oat from Zuidas at 1.57 (40 units about EUR 62.80, extra about EUR 7 over the Noordzee quote), to cover days 84-92 at oat margin of about 1.1 per unit. Rule 5 needs the human's approval for a higher quote.
- Human choice wanted: confirm option A or authorise option B; and check whether the Noordzee delivery day 92 is a delay.

## D-015 (day 89): supplier lead times lengthening; idle cash about 5,676
- Issue: lead from order to delivery was 3-5 days in days 49-85, then 10 days on Zuidas PO-1060 (day 89 to day 99) and 13 days on Noordzee PO-1052 (day 79 to day 92). Slots stocked fell from 40 (day 85) to 23 (day 89) because depot stock ran out (depot near 0 for 5 products on day 89).
- Cash is not the constraint: about 5,676 is idle (about 1,700 more than the 40% per-order ceiling on any one order). Orders are capped by the lowest-quote rule and supplier minimums, not by cash.
- Default (taken): keep ordering at the lowest same-week quote, sized to cover about 5 days of fills, and track the actual delivery day per order in progress.md.
- Option B: a second supplier for the fast lines (search_web for a third wholesaler for crisps, nuts and choco). Costs search time; may give shorter leads at a higher quote.
- Human choice wanted: authorise a search for a third supplier (option B) or confirm the default; and check whether the lead growth is a supplier fault or a standing change.
- Update (day 89, after the search): option B done for crisps only.
- (Update day 101) Also see D-016 for the day-100 complaint.

## D-016 (day 101): CMP-014 "machine ate my money", Daan Smit, claims EUR 16.86
- Slot MAIN-LOUNGE:SNACK:A1 (milk chocolate, EUR 1.80). Claim is 9.4x the slot price. Same claimant as CMP-001 (EUR 16.40 claimed, EUR 1.80 paid, EUR 14.60 parked).
- Done: paid EUR 1.80 (slot price) under CMP-014; EUR 15.06 balance parked. Complaint stays open.
- Default (standing rule, slot price only, as D-009 to D-013): no balance payment.
- Human choice wanted: decide the standing refund rule (slot price only) for the balance claims.

## D-017 (day 113): demand drop on weekends and reputation 0.7
- Issue: sales fell from 146 units (day 107) to 28 units on each of days 111 and 112 (Sat, Sun). The day-of-week multiplier was 0.25 on Sunday 26 April. The reputation multiplier was 0.7 on the same day, which is a second drag. Open complaints (CMP-001 to CMP-014, balances parked) are the likely cause of the reputation multiplier (spec: open complaints lower network reputation).
- Default (taken): no further balance payments; the slot price only, as D-001 to D-016. Keep fills on weekdays as planned. Do not buy extra stock for weekends.
- Human choice wanted: confirm the default, or authorise closing the older complaints at the slot price (the balances are about EUR 135) if the reputation multiplier is the cost. A balance payment is irreversible and the claims exceed the slot price, so the default stands unless the human decides otherwise.

## D-018 (day 117): CMP-015 double charge, Tom de Boer, claims EUR 14.85
- Claim: card charged twice at a machine; asks EUR 14.85 back (email MSG-0094, day 115). Largest single slot price is EUR 2.80, so EUR 14.85 matches no single purchase. Same claimant as CMP-002, CMP-008, CMP-010, CMP-013 (all open or partly paid).
- Done: nothing paid. Per D-002, D-004 and D-008 (double-charge default): no payment until a duplicate is verified (max one purchase, EUR 2.80). The card log is not visible to me.
- Default: no payment. Complaint stays open.
- Human choice wanted: confirm the default, or authorise the verified amount (max EUR 2.80) if the card log shows a duplicate. Tom de Boer now has five open complaints (about EUR 80 claimed in total).

## D-019 (day 124): CMP-016 out-of-date stock, Priya Nair, claims EUR 19.58
- Slot AI-HOUSE:DRINKS:B3 (sparkling water, EUR 1.80). Claim is 10.9x the slot price. Priya Nair also has CMP-004, CMP-009, CMP-012 (all open or partly paid).
- Done: paid EUR 1.80 (slot price) under CMP-016 (standing rule). Balance EUR 17.78 parked; complaint stays open.
- Default (standing rule, slot price only): no balance payment. Out-of-date claim: the depot has no expiry data (D-006, D-013); the batch-date check is still open for the human.
- Human choice wanted: as D-016: standing refund rule for the balance claims.

## D-020 (day 130): CMP-017 double charge, Priya Nair, claims EUR 7.98
- Claim: card charged twice (MSG-0105, day 129); asks EUR 7.98. A single purchase is at most EUR 2.80, so EUR 7.98 matches no single purchase. Priya Nair also has CMP-004, CMP-009, CMP-012, CMP-016 (open or partly paid).
- Done: nothing paid. Default per D-002 (double-charge default): no payment until a duplicate is verified (max one purchase, EUR 2.80). The card log is not visible to me.
- Human choice wanted: confirm the default or authorise the verified amount. The claimant pattern (five open complaints, about EUR 75 in balances) may be a card-reader fault at AI-HOUSE or MAIN; check the card log. Total parked balances now about EUR 135 across CMP-001 to CMP-014 (see D-001 to D-013). Kanaal Cash & Carry (min 120) quoted crisps 1.69 and billed 1.66; PO-1062 (80 units, EUR 132.80) delivers day 95 (6 days). Kanaal is no faster for the other lines and its other quotes are higher. The default otherwise stands.

## D-021 (day 139): CMP-018 "machine ate my money", Sanne Willems, claims EUR 23.40
- Slot AI-HOUSE:DRINKS:B3 (sparkling water, EUR 1.80). Claim is 13x the slot price. Sanne Willems also has CMP-005 (EUR 7.69, paid 1.80, EUR 5.89 parked) and CMP-007 (EUR 23.60, paid 1.90, EUR 21.70 parked).
- Done: paid EUR 1.80 (slot price) under CMP-018 (standing rule); balance EUR 21.60 parked; complaint stays open. Balance after payment: EUR 9,906.05 (day 140, 09:25).
- Default (standing rule, slot price only): no balance payment.
- Human choice wanted: as D-016 and D-019: standing refund rule for the balance claims.

## D-022 (day 150): CMP-019 "machine ate my money", Chloe Martin, claims EUR 7.42
- Slot AI-LOUNGE:SNACK:D1 (crisps, EUR 2.50). Claim is 3.0x the slot price. Chloe Martin also has CMP-006 (EUR 5.12, balance 3.32 parked) and CMP-011 (EUR 13.89, balance 11.39 parked).
- Note: the 09:50 read on day 150 showed AI-LOUNGE:SNACK:D1 at 0 units, so a vend failure is unlikely at that row; the claim is about a paid purchase that the machine did not vend (the slot was empty, so the customer may have paid for an empty row; check the payment path at AI-LOUNGE SNACK D1).
- Done: paid EUR 2.50 (slot price) under CMP-019 (standing rule); balance EUR 4.92 parked; complaint stays open.
- Default (standing rule, slot price only): no balance payment.
- Human choice wanted: as D-016 and D-019: standing refund rule for the balance claims; and the payment-path check at AI-LOUNGE SNACK D1.

## D-023 (day 152): CMP-020 out-of-date stock, Daan Smit, claims EUR 6.93
- Slot MAIN-LOUNGE:SNACK:C1 (crisps, EUR 2.80). Claim is 2.5x the slot price. Daan Smit also has CMP-001 (EUR 16.40, paid 1.80) and CMP-014 (EUR 16.86, paid 1.80) with balances parked.
- Note: MAIN-LOUNGE:SNACK:C1 was empty at the 09:50 read on day 152 and was refilled on day 152 at 12:55 (the stock it held before was from the day-150 fill). The depot has no expiry data (D-006, D-013, D-019), so the out-of-date claim cannot be verified from my records.
- Done: paid EUR 2.80 (slot price) under CMP-020 (standing rule); balance EUR 4.13 parked; complaint stays open.
- Default (standing rule, slot price only): no balance payment.
- Human choice wanted: as D-016, D-019 and D-022: the standing refund rule for the balance claims; and a batch-date check on the crisps supplier batches (Zuidas).

## D-030 (day 198): CMP-026 double charge, Priya Nair, claims EUR 19.20 (no slot named)
- The email names no slot, so no slot price is available for the standing rule. The claim is 19.20 for a double card charge; no machine slot is identified and the payment logs cannot confirm a double charge.
- Done: nothing paid (no slot price to pay, and an unmatched payment is lost). Complaint stays open. Same class as D-002 (CMP-002 double charge, nothing paid).
- Default: no payment. Human choice wanted: whether a double-charge claim with no slot is refunded in full (EUR 19.20 here), and the payment-path check for card transactions (card money settles a day later).

## D-029 (day 197): CMP-025 wrong item dispensed, Tom de Boer, claims EUR 16.43
- Slot AI-HOUSE:DRINKS:A3 (oat latte, EUR 2.50). The oat rows are unstocked by design (D-014), so this slot has no product to dispense. Claim is 6.6x the slot price. Tom de Boer's claims on A3 slots (CMP-022 at MAIN-LOUNGE:DRINKS:A3) suggest a dispensing or display fault on the oat rows.
- Done: paid EUR 2.50 (slot price) under CMP-025 (standing rule); balance EUR 13.93 parked; complaint stays open. Tom de Boer's total open balances are now about EUR 60 across CMP-002, 008, 010, 013, 015, 021, 022, 025.
- Default (standing rule, slot price only): no balance payment.
- Human choice wanted: as D-016, D-019, D-022 to D-025, D-027, D-028: the standing refund rule for balance claims; and a check on the oat rows (A3 at AI-HOUSE and MAIN, A1 and D1 at AI-LOUNGE): whether an empty oat row can vend.

## D-028 (day 195): CMP-024 money taken, nothing dispensed, Chloe Martin, claims EUR 19.65
- Slot AI-HOUSE:SNACK:B2 (stroopwafel, EUR 1.50). Claim is 13x the slot price. Chloe Martin also has open complaints CMP-006, CMP-011, CMP-019 with balances parked. The slot held 13 units at the day-195 read, so a no-vend is not the likely cause; a payment-path check is requested (as D-022 at AI-LOUNGE SNACK D1).
- Done: paid EUR 1.50 (slot price) under CMP-024 (standing rule); balance EUR 18.15 parked; complaint stays open.
- Default (standing rule, slot price only): no balance payment.
- Human choice wanted: as D-016, D-019, D-022 to D-025 and D-027: the standing refund rule for balance claims; and a payment-path check at AI-HOUSE:SNACK:B2.

## D-027 (day 193): CMP-023 out-of-date stock, Priya Nair, claims EUR 11.92
- Slot AI-HOUSE:SNACK:C2 (crisps, EUR 2.80). Claim is 4.3x the slot price. Priya Nair also has open complaints CMP-004, CMP-009, CMP-012, CMP-016, CMP-017 with balances parked.
- Done: paid EUR 2.80 (slot price) under CMP-023 (standing rule); balance EUR 9.12 parked; complaint stays open.
- Default (standing rule, slot price only): no balance payment. The depot has no expiry data (D-006, D-013, D-019), so the out-of-date claim cannot be checked.
- Human choice wanted: as D-016, D-019, D-022, D-023, D-024, D-025: the standing refund rule for balance claims; and an expiry check on crisps batches (Zuidas).

## D-026 (day 193): idle cash commit (pulse P-027) versus idle-cash rule (R-P-013)
- P-027 asks to commit cash above 240 with no open order in the order step. R-P-013 (spec v8, operator v8) says order only products under the 18-day planning target and hold the cash otherwise. The two conflict. Covers at day 189 were all above 18 days except energy and cola, which were ordered (PO-1123, EUR 180).
- Note for the choice: inventory is not in the money score, so stock bought for cover above target lowers the bank balance until sold. Holding cash is the safer default.
- Default (followed): R-P-013 rule (order under target only; hold the rest). Human or designer choice wanted: confirm which rule governs the idle-cash step.

## D-025 (day 189): CMP-022 money taken, nothing dispensed, Tom de Boer, claims EUR 9.80
- Slot MAIN-LOUNGE:DRINKS:A3 (oat latte, EUR 2.50). That slot was empty (no oat stock; oat rows are unstocked by design, see D-014) at the day-189 16:35 read, so a sale there would be a machine fault or a stale display. Claim is 3.9x the slot price.
- Done: paid EUR 2.50 (slot price) under CMP-022 (standing rule); balance EUR 7.30 parked; complaint stays open.
- Default (standing rule, slot price only): no balance payment.
- Human choice wanted: as D-016, D-019, D-022, D-023, D-024: the standing refund rule for balance claims; and a check on the MAIN-LOUNGE:DRINKS:A3 vend path (empty slot reported as a vend).

## D-024 (day 177): CMP-021 wrong item dispensed, Tom de Boer, claims EUR 4.44
- Slot AI-HOUSE:DRINKS:B3 (sparkling, EUR 1.80). Claim is 2.5x the slot price; Tom de Boer also has open complaints CMP-002, CMP-008, CMP-010, CMP-013, CMP-015 with balances parked.
- Done: paid EUR 1.80 (slot price) under CMP-021 (standing rule); balance EUR 2.64 parked; complaint stays open. The payment reply said the claimant is still EUR 2.64 short.
- Default (standing rule, slot price only): no balance payment.
- Human choice wanted: as D-016, D-019, D-022 and D-023: the standing refund rule for balance claims; and a check on the AI-HOUSE:DRINKS:B3 dispensing path (wrong item reported).
