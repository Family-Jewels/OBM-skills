# Index (operator). Rebuilt day 109 after full audit A-002 (as of day 86). Spec v3 and operator rules v3 (R-P-012, adopted day 102).

Goal: cash on day 365 from €1,500 across AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE (SNACK + DRINKS each).

## Status update (day 289, Tue 20 Oct 2026; per A-006 actions)
- Cash at open day 289: €12,944.17. Reserve met every day.
- C4 on sales records (revenue last 7 days ÷ same 7 days 30 days earlier): day 288 = €395.50 ÷ €432.50 = 0.91 (days 282–288 vs 252–258). Earlier audit read 0.52 at day 240 and 0.59 at day 272 on a different basis; the basis must be confirmed by the owner/measurement owner.
- Open orders: none (PO-1091 arrived day 287: protein 60, energy 60).
- Refunds: CMP-024 (€24.03), CMP-025 (€12.48), CMP-026 (€3.81) paid item-price then balance (closed).
- Per-visit loss log: started day 289 (loaded, empty, sold by get_sales_report; see day289_log).
- D-008 (stock loss) status: revised — MAIN sells out quickly (volume 1.8× in the demand multipliers), so the 'loss' may be sales; to be confirmed by the per-visit log. D-007 open (122+ days).

## Status update (day 255, Wed 16 Sep 2026; per A-005 action 2)
- Cash at open day 255: €12,616.19. Reserve €300 met every day. Refunds to date: CMP-022 (€17.42) and CMP-023 (€16.83), each item price then balance.
- Rules in force: operator v5 (cover rule, ORDER line per order, C8); spec v6 (cover_days, C8). Redesign R-P-029 adopted day 237.
- Suppliers: zuidas-groothandel active (lead used 4 days = longest of the last five deliveries). noordzee-dranken: not used since PO-1063. bakker removed.
- Open orders: PO-1084 energy 80 (arrived day 254); PO-1085 protein 50 (due day 257).
- Empty-count proxy (operator): day 253 AI-HOUSE 8 of 9 rotation slots empty; MAIN-LOUNGE 15 of 16 empty; day 246 AI-LOUNGE 16 of 16 empty. Unexplained stock loss in machines (see day244_log, day253_log): recorded sales do not match loaded stock.
- C4 (growth) on cash: €11,109.84 (day 192) → €12,150 (day 240) → €12,616 (day 255). Positive, slow.
- Open decisions: D-001, D-002, D-003, D-005, D-006, D-007 (defaults in use). Anomaly (stock loss) and CMP-022/023 flagged for owner review.
- Denominator: 42 assigned slots against 72 physical slots; still unexplained (A-004 F).

## Status update (day 203, Sun 26 Jul 2026; per A-004 action 2)
- Cash at open day 203: €11,460.84 (day 202 close). Reserve €300 met every day since day 109.
- Rotation (operator rules v4, ~16 slots): energy AI-LOUNGE/AI-HOUSE/MAIN DRINKS B2/B3; crisps AI-HOUSE and MAIN C1/C2; stroopwafel AI-HOUSE A1/A2 and MAIN A1; protein AI-HOUSE B3 and MAIN A3; choco AI-HOUSE B1 and MAIN B1.
- Open orders: PO-1068 (zuidas energy 60, crisps 40, due day 203); PO-1069 (zuidas protein 60, due day 204).
- Depot day 203 (09:25): cola 130, crisps 7 (loaded to MAIN C1), energy 50 (30 after day-203 loads), gummy 4, nuts 24, oat 24, protein 24, sparkling 80, stroopwafel 84 (after MAIN A1 load 66). Choco 0.
- Empty-count proxy (operator, not in-stock fraction): day 203 MAIN-LOUNGE read: rotation SNACK slots A1, A3, B1, C1, C2 all empty (5 of 5); DRINKS B2 empty, B3 6 units. Reloaded day 203.
- Denominator: 42 assigned slots (rotation plus parked) against 72 physical slots; no explanation in the swarm files (A-004 F).
- D-007 written to queue/decisions.md day 203 (late; due day 150). Defaults in use.

## Status (day 109, Thu 23 Apr 2026)
- Cash at open €5,390.19. Reserve €300: met every day (lowest close in the run €1,073.70 day 8; none below €300 since). No unpaid fee days.
- Empty-slot count (operator proxy, not in-stock fraction): 33 of 42 at day 108 read; the chart does not carry it.
- Complaints (all closed): CMP-001 to CMP-011. Refunds to date ≈ €150 (see progress.md). Each paid at item price first, balance to close (D-001/D-003 default; owner review open).
- Log: daily entries in log/progress.md through day 81 (catch-up), then per-day entries in write_note keys day82_log … day108_log. Gap days 96–97 not written.

## Suppliers (status day 109)
| supplier | status | items | realised lead (order → arrival) | cover rule |
| --- | --- | --- | --- | --- |
| zuidas-groothandel | active | crisps, energy, choco, protein, nuts, stroopwafel, cola, sparkling, oat, gummy, dropjes, mint | 2,2,2,3,2,2,11,10,4,4,4 (PO-1002..1016); 4 (PO-1025, 1026), 4 (PO-1032), 7 (PO-1033) | 12 days |
| noordzee-dranken | active | energy, sparkling, cola, oat | 2, 4, 3 (PO-1034) | 4 days |
| bakker-en-zoon-distributie | INSOLVENT day 52 (MSG-0033). Removed. | — | 10, 11 | — |
| kanaal-cash-carry, premium-vend, gadget-import | not used | — | — | — |

## Open orders (day 109)
- None. PO-1033 (zuidas, due day 107) arrived overnight 107→108 and is being loaded (energy 120, crisps 100, choco 60, nuts 40, protein 60, oat 40, cola 40, sparkling 40, stroopwafel 40).
- PO-1034 (noordzee: energy 60, oat 40) arrived day 103.

## Reorder points (A-002 action 1; written from day-108 reads; applied from the day-110 order)
Order when depot plus on-order falls below the trigger. Trigger = 7-day sales rate × 12 days (zuidas lead) plus a 7-day interval. Load target: 18 per small slot, 10 per large slot.
- Energy: 104 units/7 days ≈ 15/day. Trigger ≈ 180. Order to 180+ on the next check.
- Choco: 46/7 ≈ 7/day. Trigger ≈ 84.
- Protein: 52/7 ≈ 7/day. Trigger ≈ 84.
- Crisps: 66/7 ≈ 9/day. Trigger ≈ 108.
- Stroopwafel: 31/7 ≈ 4.5/day. Trigger ≈ 54.
- Oat: 27/7 ≈ 4/day. Trigger ≈ 48. Cola: 30/7 ≈ 4/day. Trigger ≈ 48.
- Nuts: 13/7 ≈ 2/day. Trigger ≈ 24. Sparkling: 14/7 ≈ 2/day. Trigger ≈ 24.
- Gummy, mint, dropjes: low demand; hold at most one slot each; no reorder beyond current depot.

## Price state (per SKU)
- Crisps €2.40 (6 slots). Energy €2.50 (9 slots). Oat €2.50. Cola €2.00. Sparkling €1.80. Protein €2.00. Choco €2.00. Nuts €2.20. Stroopwafel €1.80 (AI-LOUNGE A2, AI-HOUSE A1/A2, MAIN A1). Gummy €1.60. Dropjes €1.50 (AI-LOUNGE A1). Mint €1.50 (AI-HOUSE A3, MAIN A2).

## Checks (day 109)
- C2 (fee never unpaid ≥3 days): met.
- C3 (cash ≥ €300 each day): met.
- C4 (growth, read at day 120): pending.
- C5 (marketing pays): no marketing run.
- C6 (service): no open complaints; refund default (D-001/D-003) continues until the owner decides (D-005).
- C7 (stock turning): mint slots (AI-HOUSE A3, MAIN A2) show low sales; review at day 110 under the 21-day rule.

## Open items
- D-001, D-002, D-003 open with the owner (see queue/decisions.md). D-005 added on day 109 with defaults.
- Run budget: the spec (about USD 2) and the session figure differ. The session figure governs for this run (about USD 33 left at day 109). Flagged in D-005.
- Instrumentation (in-stock fraction, 7-day COGS) still not provided (D-002).

## Next
- Day 110: zuidas check_offers, then order by the reorder points above (energy, choco, protein, stroopwafel first). Log cover figures.
- Trips by 7-day ranking each morning; log empty counts per visit.
- Day 109–110: stroopwafel into MAIN A1, AI-HOUSE A1, AI-LOUNGE A2; crisps into empty C slots.
