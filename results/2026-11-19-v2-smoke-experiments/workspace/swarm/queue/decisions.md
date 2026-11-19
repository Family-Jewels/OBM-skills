# Decision requests (parked, default applied, work continues)

## D-001 (day 31): refund for CMP-001 (Daan Smit, out-of-date item, claim EUR 21.42)
- Context: one dropjes pack at MAIN-LOUNGE:SNACK:A1 (shelf price 1.80) claimed as out of date; claim asks EUR 21.42.
- Default applied: paid EUR 1.80 under CMP-001 (item price). The customer says this is short by EUR 19.62 and the complaint stays open.
- Why parked: refunds are irreversible and the claim is far above the item value. Human or designer to rule if the balance should change.
- Action taken: rotate MAIN-LOUNGE:SNACK:A1 stock oldest-first; check dropjes stock age on reload.

## D-003 (day 35): refund for CMP-003 (Fatima El Amrani, "machine ate my money")
- Context: claims EUR 23.81 paid at AI-LOUNGE:SNACK:A2 (dropjes, shelf price 1.80) with no vend.
- Default applied (same policy as D-001): paid EUR 1.80 under CMP-003, the slot's item price. The claim is far above any single vend. Parked for the human or designer to rule.
- Action to check: whether a card/cash payment was taken without vend; no machine fault is visible in the ledger.

## D-004 (day 38): refund for CMP-004 (Sanne Willems again, double charge claim EUR 16.55)
- Context: same customer as CMP-002 (day 32, EUR 3.92, settled). New claim EUR 16.55 for a duplicate card charge.
- Default applied: paid EUR 3.00 (the highest single vend price in the network) under CMP-004. A duplicate charge is one vend. Parked for the human or designer to rule.
- Note: repeat claims from the same customer; check the card ledger if it recurs.

## D-005 (day 40): settle open complaints CMP-001, CMP-003, CMP-004 in full
- Context: reputation fell 1.00 -> 0.88 with three complaints open. Full balances: 19.62, 22.01, 13.55 (total 55.18) brought each claim to its requested amount.
- Decision (changes the D-001/D-003/D-004 default): paid the full balance on each, so all three are withdrawn. The cost is about EUR 55, small against the sales lost if reputation keeps falling over the remaining 51 days.
- Parked for the human/designer to review. Expect future claims to be settled at the requested amount if they are specific and the reputation is below 0.95.

## D-006 (day 63): settle CMP-006 (Lars Jansen, "machine ate my money", claim EUR 23.96) in full
- Context: same pattern as CMP-001/003/005. Reputation is 0.96 and the complaint pattern repeats every ~10 days. Full settlement under D-005 keeps reputation near 1.00. Each claim is ~EUR 20-24; the sales lost to a lower reputation over the remaining 28 days would be larger.
- Decision: paid EUR 23.96 under CMP-006. Parked for the human/designer to review. If a future claim is above EUR 30, or the reputation is above 0.98 and the claim is a single vend, revisit.

## D-007 (day 80): CMP-007 (Chloe Martin, wrong item, claim EUR 15.33, AI-HOUSE:DRINKS:A2 cola 2.00)
- Per A-002 item 3: future claims settle at the item price (default), not the full claim, pending a human ruling on D-005/D-006.
- Paid EUR 2.00 (the slot's price) under CMP-007. The claim stays open unless the customer accepts; reputation to be watched.

## D-002 (day 32): refund for CMP-002 (Sanne Willems, double charge)
- Context: card charged twice; claim EUR 3.92 for the duplicate.
- Default applied: paid EUR 3.92 under CMP-002. Customer confirmed and withdrew the complaint.
