# Swarm index (orchestrator working file, one page)

Goal: maximise bank balance at day 365 from EUR 1,500 (spec: swarm/spec.md). Reserve EUR 168. Unpaid fee limit 10 days.

## Status (as of day 357, Sun 27 Dec 2026) — updated day 357 (A-007 records pass)
- Balance 13,304.00 at 09:00 day 357; net worth about 13,450 (day 357 stock included). Reputation 0.96; open complaint CMP-022 (EUR 12.94) parked (reputation at or above 0.85).
- Design in force: spec v9, operator v9 (R-P-039, adopted day 321; revert test day 330 count recorded in queue/decisions.md: 27 of 36 priced slots empty). Next redesign: none before day 334 per R-P-039 spacing; none adopted since.
- Open orders: none in transit at day 357 (PO-1097 nuts 40, crisps 30 arrived 356/357 and are loaded).
- Stock: energy 16 (depot), cola 35, gummy 5; nuts and crisps loaded day 357 across the three locations.
- Records: unit_costs.md extended to PO-1097 (summary block, day 357); swarm/log/progress.md synced to day 316; log/progress.md current to day 357; timelog.md has rows to day 294 (fill counts later in log/progress.md).
- Remaining: 8 days. Ordering only what can sell by day 365.

## Status (superseded: as of day 280, Sun 11 Oct 2026) — updated day 280 (A-006 records pass)
- Balance 10,302.60 at 09:00 day 280 (sales day 279: 38 units, EUR 70.20; the week before had 136 and 144 unit days). Reputation 0.96 after payments on day 259 (0.84 before). Open complaint CMP-018 (Chloe Martin, 4.34): parked (reputation at or above 0.85).
- Open orders: PO-1069 (nuts 40, gummy 40, crisps 50, energy 46, cola 40; due 282), PO-1070 (nuts 40, gummy 30, energy 20, cola 30, crisps 30; due 284). Offers valid through day 280 (zuidas); new check_offers due from day 281.
- Cover (A-006 action 1, from day 280): logged per location in log/progress.md. Several locations sat under 8 days for crisps, nuts, energy and cola between days 273 and 282; each cycle's lead time (3 to 4 days) produced a 1 to 3 day gap.
- Time log started at swarm/log/timelog.md (days 254 to 280 approximate; from day 280 daily). M4 miss and M5 pace miss to queue/decisions.md. T-002 reopened on board.jsonl.
- Earlier day-242 status (superseded): Balance 8,684.07 at 09:00 day 242. Open complaints then CMP-014/015/016, all paid day 259.
- Operator rule 2 = v6 (R-P-024, day 217): restock empty priced slots by revenue per trip, fill to cap, MAIN first; zero count and depot units logged at 09:00 and close. R-P-024 revert test sent to designer (decisions.md, day 242); v6 kept until designer rules.
- Rule 11 cover floor 8 days per operator v5 text (R-A-003). Cover at order logged for PO-1053 (cola 0, energy about 0 days).
- A-005 (full audit as of day 217) open items: PIP definition (chart is gain-based, spec is cash-based), 11-day sizing, stock-out chart, T-002 reopen, daily time log (kept in log/progress.md), M4 miss to be recorded.
- Records status: unit_costs.md has PO-1047 to PO-1053. progress.md current to day 242. The day 227 to 229 entries flagged by A-005 are held in the swarm log until the ledger reaches them (none added by the orchestrator in this pass).

## Status (superseded: as of day 195, Sat 18 Jul 2026)
- Cash 7,360.74 (balance day 195). Open order: PO-1043 (nuts 50, gummy 40; due day 196). Reputation 0.92 (day 182); CMP-010 and CMP-011 parked.
- Operator rule 2 back to v4 text (revenue per trip) from day 186 under the R-P-021 revert condition (decisions.md). Rule 11 cover floor per operator v5 text (R-A-003). A-004 action 1 (restore v3 on disk) still a conflict in decisions.md.
- Pulses P-022 (day 183) and P-023 (day 188): cash_gain_7 below pre-redesign limit since R-P-021; diagnosis needed (started by the system). Cash-based PIP 4.3 (spec definition) used.
- Cash-by-day checkpoints: day 183 7,028; day 188 7,126; day 195 7,361.
- Earlier status (superseded, day 183):
- Cash 6,875.14 after PO-1040 (balance 7,028.04 before order); reputation 0.92; open complaints CMP-010 (EUR 3.60) and CMP-011 (EUR 16.35), both parked under the complaint rule (decisions.md).
- Spec v5 and operator v5 in force since day 177 (R-P-021: fills by units lost per hour; zero counts at 09:00 and close). Operator rule 11 = v5 text (R-A-003 floor 8 days, depot + machine + in-transit). The day-167 v3 revert note is superseded. Conflict with A-004 action 1 (revert on disk) parked in decisions.md, with the R-P-021 position as default.
- Open orders: PO-1039 (energy 40, nuts 60, cola 40, gummy 40; due 184); PO-1040 (crisps 30, choco 60, dropjes 40, sparkling 30; paid 152.90; due 187).
- Pace: cash 6,875 vs spec pace line about 10,400: below pace since day 90; flagged to designer (P-020, P-021, A-004).
- Milestone M3 (day 90) missed and recorded.
- Next: day 184 PO-1039 arrival: fill nuts/gummy/cola/energy MAIN first; swap MAIN DRINKS A2 (currently 1 sparkling, mistakenly loaded day 180) to energy. Day 185: R-P-021 test (zero count 14 or fewer; cash_gain_7 above 289.85). Check offers again on day 189.

## Status (superseded: as of day 100, Tue 14 Apr 2026)
- Cash 2,904.62 (balance day 100). Reputation 1.00. Weekly zuidas orders: PO-1023 (day 91, arrived 95), PO-1024 (day 97, due 101, EUR 311.60). Next check_offers ~day 104.
- Pace: spec pace line ~5,850 at day 97 (P-011); PIP both definitions until designer settles: cash-based (spec) ~5.0 at day 97; gain-based (chart) ~9.2. Both above 2.
- Diagnosis of P-011 requested by the system (in progress; handoff pending). R-001 open with designer.
- Empty-slot state day 100: AI-HOUSE snacks nearly all empty (choco, gummy, nuts/crisps partially refilled); choco and gummy restock on day 101 from PO-1024.
- Log sync: swarm/log/progress.md still ends at day 61; workspace log/progress.md is current to day 100 and is the detailed record (backfill into swarm log pending).

## Status (superseded: as of day 61, Fri 06 Mar 2026)
- Cash 2,032.72 (balance at open day 61). Pace line ~3,600 at day 60: we are well behind (PIP ~2.9 by spec definition, A-001).
- Machines: stock arriving from PO-1018 (zuidas, due day 61: energy 40, cola 30, choco 30, gummy 30, nuts 40, sparkling 30, crisps 30, dropjes 20). Fills on arrival.
- Reputation 0.84 on day 60 after four complaints; all four refunded day 60 and withdrawn (see swarm/queue/decisions.md, complaints_policy note).
- Open decisions: D-002 (missed M2), D-005 (ordering cadence: revert to one zuidas order per week, covering ~10-11 days of stock), D-006 (designer requests from A-001).
- Diagnosis: A-001 requested a diagnosis (top sellers ran out days 32-39). Waiting for D-diagnosis and redesign.

## Suppliers
- zuidas-groothandel: default. Lead 3-4 days (PO-1001 1->4, PO-1003 6->8, PO-1004 8->11, PO-1005 10->14, PO-1006 13->16, PO-1007 15->18, PO-1008 17->21, PO-1009 22->24, PO-1010 26->28, PO-1011/12 30->33, PO-1013 35->39, PO-1014 36->39, PO-1015 42->45, PO-1016 46->49, PO-1017 52->56, PO-1018 59->61). Min order 75.
- bakker-en-zoon: 20-day lead observed (PO-1002 day 6 -> day 26). Avoid for urgent stock.
- noordzee-dranken, kanaal-cash-carry: not used. premium-vending-partners: avoid.

## Products and current best slot per product (price at last set)
- energy: MAIN:DRINKS:A2 (2.20), HOUSE:DRINKS:B1 (2.00), LOUNGE:DRINKS:B1 (2.10)
- cola: MAIN:DRINKS:A1 (2.00), HOUSE:DRINKS:A1 (2.00), LOUNGE:DRINKS:A1 (1.80)
- sparkling: MAIN:DRINKS:B1 (1.60), HOUSE:DRINKS:A2 (1.60), LOUNGE:DRINKS:A2 (1.50)
- oat latte: LOUNGE:DRINKS:A3 (2.30)
- choco: HOUSE:SNACK:A1 (1.80), MAIN:SNACK:A1 (1.60), LOUNGE:SNACK:A1 (1.50)
- crisps: HOUSE:SNACK:C1 (2.50), MAIN:SNACK:C1 (2.50), LOUNGE:SNACK:C1 (2.30)
- nuts: HOUSE:SNACK:B1 (2.40), MAIN:SNACK:B1 (2.40), LOUNGE:SNACK:B2 (2.20)
- gummy: HOUSE:SNACK:A2 (1.80), MAIN:SNACK:B2 (1.80)
- dropjes: MAIN:SNACK:A2 (1.60), LOUNGE:SNACK:B1 (1.40)
- stroopwafel: HOUSE:SNACK:B2 (1.60)
- tortilla: LOUNGE:SNACK:C2 (3.20)
- oatmeal: HOUSE:SNACK:B3 (2.40)
- protein bar: MAIN:SNACK:A3 (2.60)
- mint: LOUNGE:SNACK:A2 (1.80), MAIN:SNACK:B3 (1.80)

## Measurement gaps (instrumentation)
- Daily time log: swarm/log/timelog.md (days 1-5 only; resumed from day 61 as minutes per action in log/progress.md).
- Unit costs per receipt: swarm/log/unit_costs.md (stops at PO-1006; PO-1007 to PO-1018 are in the progress log with unit prices).

## Operating rules in force
1. Restock every empty slot the same day from depot stock; allocate depot stock across machines before the first fill; do not fill fewer than ~8 units unless the slot is otherwise empty.
2. One zuidas order per week (D-005) on the check_offers validity date, plus cover-floor orders (operator rule 11, floor 6 days on depot stock, v3 text) when a location's product falls below floor. Sized ~11 days of sales.
3. Complaints: park unverified claims while reputation is at or above 0.85; pay exactly as claimed only while reputation is below 0.85 (EXCEPTION day 142, decisions.md). Log each in swarm/queue/decisions.md.
4. Marketing: slack EUR 1 only where the location has at least 3 products in stock.
