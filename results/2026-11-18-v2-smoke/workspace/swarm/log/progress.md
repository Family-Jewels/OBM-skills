# Operator progress log (events and daily lines)

## Milestones
- T-001 baseline: day 1, cash 1500, 72 slots empty and unpriced, storage empty.
- T-002 suppliers: bakker-en-zoon, kanaal-cash-carry, zuidas-groothandel quoted (day 1; kanaal and bakker re-quoted day 8, valid to day 14). Noordzee emailed day 1; no usable reply.
- M1 (crude end-to-end): all six machines have a selling slot by day 6-7. Met on day 7 (sales day 6).

## Orders
- PO-1001 bakker-en-zoon, day 1, paid 189.60, due day 15, arrives overnight day 15->16 (cola 40, oat-latte 30, crisps 40, nuts 30, choco 30, stroopwafel 30). Cost recorded per receipt.
- PO-1002 kanaal-cash-carry, day 1, paid 154.40, due day 5, arrived day 5->6 (sparkling 60 @0.49, gummy 30 @0.62, crisps 40 @1.93, dropjes 40 @0.73).
- PO-1003 kanaal-cash-carry, day 8, paid 124.10, due day 11, arrived day 11->12 (cola 30 @1.17, energy 20 @1.60, stroopwafel 20 @0.80, mint 20 @0.95, nuts 20 @1.10).

## Experiments
- E-001 started day 8 (price test). Test slots +10%: AI-LOUNGE:SNACK:A1 gummy 1.80->1.98; AI-HOUSE:SNACK:A1 dropjes 1.80->1.98; MAIN-LOUNGE:SNACK:A1 gummy 1.80->1.98. Baseline held: crisps C1 2.50 at all sites, sparkling 1.80. Half split approximated (one slot per site). Ends day 28.

## Events
- Day 6: stocked six machines (first fills); spot fees accrue 12/day.
- Day 8: P-001 pulse received (no signal). Idle: 63 of 72 slots not selling. Action: keep reserve, fill idle slots, log E-001.
- Day 12: stocked cola (3 drinks machines), nuts (AI-LOUNGE B1), stroopwafel (AI-HOUSE B1), mint (MAIN-LOUNGE B1), energy (AI-HOUSE and MAIN-LOUNGE A3). Prices: cola 2.00, nuts 2.20, stroopwafel 1.60, mint 1.50, energy 2.50.
- Pending: bakker deliveries day 16 (crisps 40 needed at AI-HOUSE and AI-LOUNGE C1, oat latte, choco). Gummy and crisps depot empty.

## Orders (continued)
- PO-1004 kanaal-cash-carry, day 13 (Saturday), paid 126.40, delivery day 26 (gummy 30 @0.71, energy 20 @1.60, cola 30 @1.17, stroopwafel 20 @0.80, nuts 20 @1.10). Lead time 13 days vs 3 days on PO-1003: do not order from kanaal at weekends.
- PO-1005 zuidas-groothandel, day 14 (Sunday), paid 80.80, delivered day 18 (energy 30 @1.29, cola 30 @0.95, mint 20 @0.68). Lead 4 days.
- PO-1006 zuidas-groothandel, day 17, paid 134.80, due day 20 (energy 40 @1.29, cola 30 @0.95, gummy 30 @0.51, sparkling 20 @0.51, protein bar 20 @1.46).

## Experiments (correction, pulse P-002)
- E-001 deviation: the spec asks for +10% on half the selling slots at each site. Only 3 slots were selling per site at day 8, so the test used one slot per site (gummy at AI-LOUNGE and MAIN-LOUNGE, dropjes at AI-HOUSE). Baseline: crisps C1 2.50, sparkling 1.80, everything else as set. Result written at day 28.

## Events (continued)
- Day 16: stock-outs found (MAIN and AI-HOUSE drinks empty; most crisps slots empty). Restocked crisps x3, cola x2, sparkling x2, stroopwafel, choco MAIN B2.
- Day 17: P-002 pulse received (no signal; 6 selling slots on the chart vs about 19 in this log, reconciled below). Action: idle cash used for PO-1006; oat latte x3 drinks B1 (2.50), stroopwafel AI-LOUNGE B2 (1.60), nuts MAIN B3 (2.20), choco AI-HOUSE B2 (1.80).

## Daily lines
- Day 18: cash 1150.40. Units day 17: 67 (EUR 133.40). Stock-outs on most drinks slots; restocked cola x2, sparkling MAIN A1, crisps MAIN C1, nuts AI-HOUSE B3.
- Day 19: cash 1283.30 (PO-1005 arrived). Units day 18: 65 (EUR 140.10). Energy x3 drinks A3 (2.50), cola AI-HOUSE A2, mint MAIN B1. PO-1007 zuidas (crisps 40, nuts 30) due day 29 (Friday order, 10-day lead).
- Day 20: cash 1282.10. Units day 19: 46 (EUR 100.40). No trips (no stock on hand).
- Day 21: cash 1343.00 (PO-1006 arrived). Units day 20: 16 (EUR 34.10). Restocked sparkling x2, gummy x2, protein AI-HOUSE A2, energy duplicates AI-HOUSE B2 and MAIN B2, cola duplicates AI-LOUNGE B2 and MAIN C1. PO-1008 zuidas placed (77.70, due 24).
- Day 22: cash 1296.98. Units day 21: 18 (EUR 37.66). Energy AI-LOUNGE B3, MAIN C2; cola AI-HOUSE C1.
- Day 23: cash 1244.44 after PO-1009 (108.50). Units day 22: 75 (EUR 160.08).
- Day 24: cash 1364.20. Units day 23: 36 (EUR 75.66). Stock-outs: almost every slot empty. Only cola reloaded (AI-LOUNGE A2, AI-HOUSE A2). PO-1008 and PO-1009 arrive day 25 (due day N arrives N+1).

- Day 25: cash 1424.38. Units day 24: 29 (EUR 62.74). PO-1008 arrived; restocked stroop, choco, gummy, dropjes, mint. PO-1010 zuidas placed (93.50, due 35, 10-day lead).
- Day 26: cash 1412.66. Units day 25: 73 (EUR 133.02). PO-1009 arrived; energy x3, oat x2, sparkling x2, cola x2.
- Day 27: cash 1548.90 (PO-1004 arrived). Units day 26: 97 (EUR 205.08). Stroop, nuts, energy x2, cola, gummy.
- Day 28: cash 1700.74. Units day 27: 33 (EUR 69.54). E-001 closed (inconclusive, kept 1.98). CMP-001 refund 1.50 paid, rest parked as D-001.
- Day 29: cash 1623.68 after PO-1011 (kanaal, 127.50, due day 40). Units day 28: 24 (EUR 50.44). E-002 started.
- Day 30: cash 1684.90. Units day 29: 66 (EUR 141.14). PO-1007 arrived (crisps 40, nuts 30). Restocked crisps AI-LOUNGE/AI-HOUSE/MAIN C1, nuts AI-HOUSE B3 (18) and MAIN B3 (12). Price moves (decision, within decision rights, from full audit A-001 and opportunity review O-001): energy 2.50 -> 2.75 at all three drinks A3/B2/B3/C2 slots; cola 2.00 -> 2.20 at all six cola slots. Watch units and revenue for 7 days.
- Audit actions (A-001, P-001..P-003): reconciled slot count (8 selling on day 24 by inventory), daily lines filled days 12-30, E-001 result and deviation written, E-002 start rule written, decision file created (D-001).

- Day 31: cash 1834.12 (morning). Units day 30: 81 (EUR 177.54). CMP-002 refund 1.98 (D-002). PO-1012 zuidas (60 energy etc.) and PO-1013 bakker (40 each, crisps, nuts, choco, stroop, cola, oat) placed, cash 1415.94 after.
- Day 32: cash 1543.02 (morning). Units day 31: 33 (EUR 65.36). CMP-003 refund 3.92 (withdrawn).
- Day 33: cash 1584.66. Units day 32: 16 (EUR 31.48). Crisps AI-LOUNGE C1 reloaded.
- Day 34: cash 1605.84. Units day 33: 15 (EUR 33.08). PO-1012 arrived; energy x3 drinks A3, gummy x2, sparkling x2, dropjes, mint. CMP-004 refund 1.60 (D-003).
- Day 35: cash 1625.35. Units day 34: 11 (EUR 24.99). Sparkling MAIN A1, energy AI-HOUSE B2, MAIN B2.
- Day 36: cash 1629.56. Units day 35: 13 (EUR 29.68). PO-1010 arrived (stroop 40, gummy 40, dropjes 30, choco 30). Restocked stroop x2, choco x2, dropjes, protein, mint, energy AI-LOUNGE B3. PO-1014 zuidas placed 114.60 (due 38).
- Day 37: cash 1586.51. Units day 36: 93 (EUR 186.89). PO-1013 bakker arrived. E-005 full-depth loads (cola x3, oat x3); nuts AI-LOUNGE B1; crisps AI-HOUSE C1, MAIN C1.
- Day 38: cash 1837.52. Units day 37: 158 (EUR 346.36). CMP-005 (Sanne Willems, claims 16.55, failed vend at MAIN C1): refunded 2.50 slot price; rest parked (D-004). Stroop MAIN A3 (new, 1.60), gummy AI-HOUSE A3, crisps AI-LOUNGE C1, cola AI-HOUSE C1. PO-1014 due 38 (arrives 39).
- Price hold: no price changes from day 31 until E-002 closes (day 49), per P-004.

- Day 39: cash 2076.27 (morning). Units day 38: 90 (EUR 186.17). PO-1014 arrived; energy x5 and cola x3 loaded; PO-1015 zuidas placed (97.00, due 42).
- Day 40: cash 2158.17. Units day 39: 56 (EUR 121.14). PO-1011 kanaal due 40 (arrived 41). PO-1016 bakker placed (144.70, due 47). Snack reloads: choco, stroop, nuts AI-HOUSE; sparkling AI-LOUNGE A1; cola AI-HOUSE A2; oat AI-LOUNGE B1.
- Day 41: cash 2119.00. Units day 40: 77 (EUR 169.73). No trips (calls ran into day 42; see note).
- Day 42: cash 2245.33. Units day 41: 15 (EUR 33.63). Loaded MAIN-LOUNGE empty row set (energy, sparkling, cola, gummy, dropjes, choco, stroop), AI-HOUSE dropjes and cola, AI-LOUNGE gummy A3 (1.98). PO-1015 due 42. M3 (60 slots by day 42) missed (about 35-40 selling).
- Day 43: cash 1963.66 after PO-1017 (311.60, due 45). Units day 42: 27 (EUR 56.19). Energy x6 drinks slots (10/10 where stock allowed), sparkling AI-HOUSE A1, protein AI-HOUSE A2.
- Day 44: cash 2041.97. Units day 43: 100 (EUR 203.09). Cola AI-LOUNGE A2, B2. Cola ran out in depot.
- Day 45: cash 2253.18. Units day 44: 88 (EUR 199.66). Depot energy 32, sparkling 50, dropjes 28, protein 26, gummy 20. Loaded energy AI-HOUSE B3 (new, 2.75), energy MAIN B3 (new, 2.75), protein MAIN B1 (new, 2.50).
- P-004/P-005 items: full-depth restocks kept; idle cash deployed through PO-1015, PO-1016, PO-1017. Slot count: system figure 10 (chart) vs 13 (resource table); the orchestrator count on day 45 is about 40 priced slots with stock (from loads). Reconciliation request left to the system (spec open question 7).
- E-001 is recorded KEEP but untested (flagged for the day-49 review).

## Slot count reconciliation (P-003 request)
- Counted from machine inventory at 11:30 day 24: slots with stock > 0 and a price = 8 (AI-LOUNGE: gummy A1, sparkling A1, cola B2, energy B3; AI-HOUSE: protein A2; MAIN-LOUNGE: gummy A1, mint B1, energy C2). Earlier counts of 19 and 27 were wrong (they counted slots that had sold out). The system figure of 9 on day 21 is consistent with stock-outs.
- M2 (36 selling by day 21) is missed. Binding constraint is supply in the depot and trip time, not demand: the machines sell out in about one day.
- Day 12: cash 1120.14. Units day 11: 12 (EUR 22.68). Selling slots (count of priced slots with stock) approx 19.
- Day 13: cash 1023.22 after PO-1004. Units day 12: 68 (EUR 141.84).
- Day 14: cash 1055.38 after PO-1005. Units day 13: 10 (EUR 17.98).
- Day 15: cash 1051.88. Units day 14: 5 (EUR 8.10).
- Day 16: cash 1062.66. Units day 15: 19 (EUR 34.06). Stock-outs on most drinks slots found in the morning.
- Day 17: cash 1131.04 (open). Units day 16: 93 (EUR 188.26). Cash after PO-1006 996.24 at 09:55; the slot count after today's fills is about 27.
- Slots-selling reconciliation: the chart read 6 on day 14 because most drinks and snack slots had run dry; the log count is the priced slots with stock. Use the log count (approx) until the day-21 full audit confirms it.
- Duplicate-slot sharing: not yet confirmed by a sales-report test; each product so far has at most one slot per machine, so the sharing rule is untested. Confirm by day 21.
