# Day 46 (Thu 19 Feb 2026) day log

- Open balance 2888.84. Sales day 45: 53 units, EUR 155.95. (1-day report on day 46: crisps 25, oat 13, nuts 7, cola 5, sparkling 2, energy 1.)
- P-007 correction: the 9-slot price pass runs before any trip that would pass 216 restock minutes. Days 42 and 43 skipped it (restock stopped at 180 min on each, so no trip passed 216, but the pass was not run before the day's fills). Today the pass ran first.
- Reads: get_sales_report (1 day), get_machine_inventory.
- Price pass (9 slots, about 45 min): AI-HOUSE crisps C1 3.30 -> 3.50; MAIN crisps C1 3.60 -> 3.80; AI-LOUNGE crisps C1 3.50 -> 3.70; AI-HOUSE oat A2 2.75 -> 2.95; AI-LOUNGE nuts A1 2.00 -> 2.10; MAIN stroopwafel A2 1.65 -> 1.75; AI-LOUNGE sparkling A1 1.75 (held); AI-HOUSE energy B1 3.00 (held); MAIN energy C2 2.95 (held).
- Swap check: no product with zero sales in 7 days (choco and stroopwafel show zero yesterday only because they were out of stock). No swap.
- Fills (4, 180 min; a 5th trip would take the day past 216): cola 10 at AI-HOUSE A1; cola 10 at MAIN B1; sparkling 10 at AI-HOUSE A3; sparkling 10 at MAIN C1.
- Orders: PO-1015 (zuidas) paid 180.40, due day 48: crisps 60 @1.96 and oat-latte 40 @1.57. Quote row in swarm/log/T-0002.md (day 46, valid_through_day 49, later than today). Balance after order 2708.44.
- Depot (estimate): oat ~1, crisps 0 (next supply: none until a new order), energy ~4, stroopwafel 0, choco 0, nuts ~4, cola ~20, sparkling ~40. PO-1014 (choco 80, energy 60, stroopwafel 60) due day 47. Oat and crisps need a new order (check zuidas before ordering; valid_through_day must be later than the order day).
