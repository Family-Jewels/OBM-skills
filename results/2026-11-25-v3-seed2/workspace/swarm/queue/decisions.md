# Parked decisions (operator)

Customer claims: policy = refund the slot's price for the item claimed (no record of a failed vend, double charge or expired item beyond one vend). Claims above one vend price cannot be matched; they stay open.

| Ref | Customer | Claimed | Paid | Still open | Note |
|---|---|---|---|---|---|
| CMP-001 | Daan Smit | €7.46 (AI-LOUNGE:SNACK:A1 gummy €1.50) | €1.50 (D13) | €5.96 | open |
| CMP-002 | Chloe Martin | €6.12 double charge | €2.50 (D42) | €3.62 | open |
| CMP-003 | Sanne Willems | €13.44 out-of-date (MAIN SNACK C2 tortilla €3.00) | €3.00 (D44) | €10.44 | open; tortilla not restocked |
| CMP-004 | Chloe Martin | €20.73 wrong item (AI-HOUSE SNACK B2 stroop €1.50) | €1.50 (D49) | €19.23 | open |
| CMP-005 | Priya Nair | €20.93 out-of-date (AI-HOUSE SNACK C1 crisps €2.50) | €2.50 (D53) | €18.43 | open; check stock age |
| CMP-006 | Priya Nair | €23.79 failed vend (AI-LOUNGE DRINKS A3 cola €2.00) | €2.00 (D55) | €21.79 | open |
| CMP-007 | Lars Jansen | €3.09 wrong item (AI-HOUSE DRINKS A1 energy €2.50) | €2.50 (D60) | €0.59 | open |
| CMP-008 | Sanne Willems | €8.27 failed vend (MAIN DRINKS A1 sparkling €1.50) | €1.50 (D81) | €6.77 | open |
| CMP-009 | Daan Smit | €6.03 failed vend (AI-HOUSE SNACK C1 crisps €2.50) | €2.50 (D91) | €3.53 | open |
| CMP-010 | Fatima El Amrani | €8.53 wrong item (AI-LOUNGE SNACK B1 nuts €2.00) | €2.00 (D92) | €6.53 | open |
| CMP-011 | Daan Smit | €20.84 failed vend (AI-LOUNGE SNACK C1 crisps €2.50) | €2.50 (D96) | €18.34 | open |
| CMP-012 | Daan Smit | €5.89 wrong item (AI-LOUNGE DRINKS B1 energy €2.50) | €2.50 (D101) | €3.39 | open |
| CMP-013 | Tom de Boer | €5.01 out-of-date (AI-HOUSE DRINKS A1 energy €2.50) | €2.50 (D109) | €2.51 | open |
| CMP-014 | Priya Nair | €21.92 double charge | €2.50 (D131) | €19.42 | open |

Total still open (approx.): €171.

Decision needed (operator default): keep the slot-price refund policy; do not pay claims above one vend price. Check stock age on crisps/energy (out-of-date claims CMP-003, 005, 013) and rotate older stock first.
