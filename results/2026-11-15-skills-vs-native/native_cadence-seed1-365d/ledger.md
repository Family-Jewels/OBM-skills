# Operator ledger (days 0-42)

Opening cash €1,500. Spot fee €12/day. Complaints settled by full claim amount (partial payments do not close them).

## Purchases (order_goods, cash out on order day)
| Order | Day | Supplier | Paid | Delivered |
|---|---|---|---|---|
| PO-1001 | 1 | Bakker | 212.40 | d7 |
| PO-1002 | 1 | Zuidas | 122.00 | d5 |
| PO-1003 | 1 | Noordzee | 104.40 | d6 |
| PO-1004 | 11 | Zuidas | 149.16 | d14 |
| PO-1005 | 12 | Bakker | 142.30 | d15 |
| PO-1006 | 12 | Noordzee | 100.40 | d16 |
| PO-1007 | 17 | Zuidas | 154.90 | d21 |
| PO-1008 | 17 | Bakker | 126.90 | d28 |
| PO-1009 | 21 | Noordzee | 90.50 | d23 |
| PO-1010 | 21 | Zuidas | 117.40 | d24 |
| PO-1011 | 24 | Zuidas | 79.40 | d27 |
| PO-1012 | 30 | Bakker | 147.60 | d35 |
| PO-1013 | 30 | Zuidas | 147.00 | d33 |
| PO-1014 | 33 | Noordzee | 96.60 | d38 |
| PO-1015 | 35 | Zuidas | 216.60 | d38 |
| PO-1016 | 41 | Bakker | 185.60 | d52 (due) |
| PO-1017 | 41 | Zuidas | 77.40 | d43 (due) |

Total purchases paid to date: about €2,170.

## Customer complaints (all closed by paying the full claim)
| Ref | Day | Paid |
|---|---|---|
| CMP-001 | 8 | 16.40 |
| CMP-002 | 12 | 13.16 |
| CMP-003 | 21 | 17.29 |
| CMP-004 | 26 | 23.38 |
| CMP-005 | 29 | 7.69 |
| CMP-006 | 36 | 5.12 |
| CMP-007 | 40 | 23.60 |

## Reconciliation of early outflows
- Day 1-2: 1500 -> 1049.20 = 450.80 = PO-1001 + PO-1002 + PO-1003 (438.80) + spot fees 2 days (12.00). Fully explained.
- Day 6-7 stall: stock in transit (deliveries d5-d7); loaded d6 onward.
- Day 30-31 dip: PO-1012 and PO-1013 paid on day 30 (294.60). Explained.
- Day 33-34: PO-1014 (96.60) paid day 33. Explained.

## Sales (gross revenue per day, from sales report)
d6 €28.10 (14u), d7 €33.50, d8 €162.30, d9 €150.10, d10 €208.00, d11 €126.10, d12 €148.40, d13 €27.20, d14 €22.90, d15 €159.00, d16 €261.50, d17 €178.90, d18 €90.70, d19 €38.90, d20 €28.50, d21 €14.80, d22 €107.70, d23 €145.10, d24 €136.70, d25 €166.20, d26 €139.30, d27 €28.10, d28 €21.60, d29 €268.80, d30 €141.20, d31 €81.30, d32 €20.00, d33 €33.40, d34 €37.70, d35 €32.30, d36 €304.90, d37 €173.10, d38 €79.90, d39 €115.60, d40 €138.90, d41 €29.00.

## Days 42-51 (added d51)
- Orders: PO-1017 Zuidas 77.40 (d41, delivered d43, confirmed). PO-1018 Zuidas 164.70 (d45, delivered d49). PO-1019 Zuidas 117.60 (d47, due d51, not yet received at d51 09:25). PO-1016 Bakker 185.60 (d41, due d52).
- Complaints: CMP-007 paid 23.60 (d41).
- Marketing (run_marketing, cash out): d19 mail MAIN 2.00 + slack AI-HOUSE 1.00; d29 slack MAIN 1.00 + mail AI-LOUNGE 2.00; d46 slack AI-HOUSE 1.00 + slack MAIN 1.00.
- Sales (gross): d43 (Mon) 74u/€150.70; d44 78u/€188.10; d45 47u/€97.80; d46 41u/€74.20; d47 22u/€41.60; d48 5u/€9.70; d49 5u/€8.70; d50 67u/€130.10.
- Cash d51: €2,734.80.
- Note on earlier review gaps: sales list above is keyed by the sales-report date (day of report), so d43 row is the sale of the previous day. Spot fees 12/day are assumed paid each day.

## Days 52-69 (added d69)
- Orders: PO-1016 Bakker 185.60 (d41; delivered d52). PO-1019 Zuidas 117.60 (d47; delivered d51). PO-1020 Noordzee 115.20 (d55; delivered d59). PO-1021 Zuidas 98.10 (d55; delivered d59). PO-1022 Zuidas 182.40 (d61; delivered d65). PO-1023 Zuidas 207.90 (d67; due d71). PO-1024 Noordzee 104.40 (d68; due d72).
- Bakker & Zoon Distributie went out of business (notice d64). No further Bakker orders. Replacement sourcing: Zuidas and Noordzee.
- Complaints: CMP-008 22.75 (d54, Tom de Boer); CMP-009 13.89 (d65, Chloe Martin); CMP-010 15.28 (d68, Lars Jansen).
- Marketing: d55 slack AI-LOUNGE 1.00.
- Sales (gross, by report day): d52 64u/€123.10; d53 70u/€171.40; d54 75u/€181.00; d55 42u/€104.70; d56 8u/€17.90; d57 5u/€12.10; d58 57u/€129.90; d59 69u/€166.90; d60 23u/€41.00; d61 68u/€138.40; d62 44u/€85.70; d63 10u/€20.30; d64 6u/€12.20; d65 39u/€79.80; d66 55u/€115.10; d67 30u/€69.00; d68 43u/€117.80; d69 48u/€120.30.
- Cash: d51 €2,734.80; d54 €3,155.00 (before CMP-008); d60 €3,412.25; d65 €3,475.55; d69 €3,476.68.
- Machine-level note: MAIN-LOUNGE empties within 1-2 days; weekend sales collapse when machines run dry (d56, d63-64).

## Days 70-94 (added d94)
- Orders: PO-1023 Zuidas 207.90 (d67; delivered d71). PO-1024 Noordzee 104.40 (d68; delivered d72). PO-1025 Noordzee 98.70 (d74; delivered d76). PO-1026 Zuidas 254.00 (d75; delivered d79). PO-1027 Zuidas 187.10 (d81; delivered d85). PO-1028 Zuidas 117.60 (d82; delivered d85). PO-1029 Zuidas 176.00 (d88; delivered d91). PO-1030 Noordzee 95.80 (d89; delivered d91). PO-1031 Zuidas 162.60 (d93; due d96).
- Complaints: CMP-010 15.28 (d68); CMP-011 23.89 (d75). Both closed by full claim.
- Marketing: none since d55.
- Sales (gross, by report day): d70 14u/€33.70; d71 9u/€23.90; d72 23u/€49.70; d73 58u/€120.80; d74 58u/€112.10; d75 63u/€111.40; d76 49u/€98.50; d77 7u/€13.30; d78 15u/€28.70; d79 59u/€109.80; d80 66u/€126.30; d81 76u/€187.30; d82 46u/€121.80; d83 45u/€107.80; d84 10u/€23.80; d85 8u/€18.90; d86 36u/€79.60; d87 68u/€150.70; d88 84u/€183.20; d89 86u/€180.80; d90 48u/€94.40; d91 6u/€11.20; d92 5u/€9.60; d93 50u/€117.40.
- Cash: d69 €3,476.68; d75 €3,767.98 (before CMP-011); d81 €3,913.09; d87 €4,077.19; d94 €4,317.99.
- Reconciliation: each cash movement from d70 onward matches a logged order, complaint, or fee. Earlier "unexplained" alerts were stale reads of the reports and do not reflect real outflows.

## Cash
d42 balance €2,483.90 (opening €1,500). d51 balance €2,734.80. d69 balance €3,476.68. d94 balance €4,317.99.

## Stock constraints (learned)
- A restock fills one slot and takes 45 minutes; about 6-7 slots can be refilled per day.
- Weekend (Sat/Sun) sales are roughly 15-20 units per day; Monday is strongest.
- Supplier lead times: Noordzee 2-5 days, Zuidas 3-5 days, Bakker 4-17 days. Zuidas has a €75 minimum order.
