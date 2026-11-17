# Plan: Run Prosus Vending Bench for 365 days

Revision v8, day 257. Previous version: swarm/history/plan-v7.md. Reason: diagnosis D-P-037 (day 239) and revision record swarm/audits/R-P-037.md. D-P-037 found that the blocking ledger step (v5 onward, still not done on day 257) stopped every experiment, that the no-spend price test and slot sweep were allowed under v7 but never recorded, and that the charts cannot be reproduced. v8 removes the ledger from the path to action: price tests and the slot sweep start today, spend is logged to a fallback file when ledgers cannot be written, and the charts are no longer used alone for decisions. The 224-a-day benchmark path is set aside as not reachable on the current path; the target becomes measured gain per day, reviewed at day 277.

Revision v7, day 202. Previous version: swarm/history/plan-v6.md. Reason: diagnosis D-P-032 (day 191) and revision record swarm/audits/R-P-032.md. v6 Phase 4 step 1 (ledgers) was still not done after 42 days, so the gate blocked every spend, price and marketing action, and no experiment ran. v7 fixes one phase date, lets no-spend price tests run without the ledger gate, caps stock spend against margin, and requires the zero-sales days to be explained before a price result is claimed.

Revision v6, day 160. Previous version: swarm/history/plan-v5.md. Reason: diagnosis D-P-025 (day 146) and revision record swarm/audits/R-P-025.md. v5 Phase 4 was never carried out: the ledgers were still missing on day 146, so no price test or reconciliation ran. v6 makes the ledgers a hard gate that is checked and recorded each day, and orders the steps so nothing depends on an unrecorded step.

Earlier history: v5 was written on day 117 with reason diagnosis D-A-002 (day 109). Net cash has been about EUR 48 a day since day 81, against about EUR 224 a day needed to reach the benchmark. Revenue has been flat at about EUR 100 a day since day 9, with about 10 of 72 slots selling and revenue per unit about 2.2. No price, slot or product change has been tested in 239 days.

## Context
Goal: maximise final bank balance over 365 simulated days, starting from EUR 1,500. Bankrupt or unfinished runs score zero, so survival and running to day 365 come first. Three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Reference benchmark: about EUR 3,228 by day 30 and EUR 61,219 by day 365. The exemplar (scripted reference operator) has gained about 5.6x our gain by day 258; treat it as a benchmark, not a guarantee.

Current position (day 257, from D-P-037 and charts.md): net gain about EUR 30–34 a day; about 31 units a day at about EUR 2.2 each; about 10 of 72 slots selling. The benchmark pace (about EUR 419 a day from day 239) is not reachable on the current path. The aim now is to find a price, slot or product change that raises revenue, and to measure it.

## Operating principles
1. **Never go bankrupt.** Keep the balance comfortably above the cost of a few weeks of spot fees and orders. The spot fee is EUR 12/day network-wide, and more than 10 consecutive unpaid days ends the business. Check get_status every day.
2. **Cash is banked overnight, card takes a day longer.** Do not count unsettled card receipts as spendable.
3. **Every slot needs a price.** Stock with no price sells nothing. A slot counts as stocked only when get_machine_inventory shows both a product and a price.
4. **Time is the binding constraint.** The day is 8 hours (09:00–17:00). A restock costs 45 min, a swap 30 min, a price change or status read a few minutes. Plan at most about 4–6 machine trips per day, and batch restocks per location.
5. **Duplicate product slots share demand.** Extra slots add capacity, not customers.
6. **Pricing is tested, not assumed.** Revenue per unit has stayed between 1.6 and 2.3 since day 9. Price changes are a required, recorded experiment (Phase 4).
7. **Marketing is a moderate lever.** Use run_marketing only as a logged test (Phase 4).
8. **Judge trends on 7-day averages, never on one day.**
9. **A plan step is done only when its record exists.** Each step names the file it produces. If a write fails, the failed write and its error go into swarm/audits/R-P-037.md the same day; that counts as the record for the step.
10. **Every stock purchase and marketing spend is recorded the same day**, in swarm/ledgers/cash-ledger.md if it exists, otherwise in swarm/audits/R-P-037.md. Unrecorded spend is not allowed.
11. **One change at a time.** Each product, price or marketing change is held for 7 days before the next one on the same location. Record the change, start day and expected effect in the record file.
12. **Every slot is classified each morning.** Each of the 72 slots is one of: sold in the last 24 hours; priced but unsold; unpriced; empty by decision (with reason). Counts go into the record file each day.

## Phase 1: Day 0 (setup)
- Done. Historical reference only.

## Phase 2: Weeks 1–4 (learn and stabilise)
- Done. Historical reference only.

## Phase 3: Steady operation
- Each morning: get_status; get_machine_inventory on all six machines; classify every slot (principle 12); record yesterday's sales, cash and fees; fix any unpriced slot with stock in storage before anything else; then run the day's Phase 4 action, if one is due; then wait_for_next_day.
- Every 7 days: check_offers across suppliers, then order for the week. Buy to the 14-day average units per slot, not peak weeks. Weekly stock spend must not exceed 60% of the average weekly revenue over the last 14 days, unless the cash buffer (4 weeks of operating cost) is met and the record explains the spend. Record each product's purchase cost against its price; a product whose margin is below the level at its last price test is repriced, swapped, or re-sourced.
- Every 7 days: list every slot with no sales in the last 7 days. Each is repriced, swapped, or recorded as deliberately empty with a reason. Do not add slots until a slot-level signal exists in the 7-day records.
- Every 7 days: run the cash reconciliation (Phase 4, step 5) and record the result.
- Treat complaints promptly. Refund with send_payment only with the exact CMP- reference and the full amount, after verifying it.

## Phase 4: Economics revision (v8, effective day 257)
Target: measured net gain per day, reported every 7 days from the record files. The benchmark pace is no longer the planning target; it is reported for comparison only. Each step is a dated, recorded action with a named file. Steps run in the order given, and no step waits for a ledger file.

1. **Slot-coverage sweep (day 257, today).** Classify all 72 slots using get_machine_inventory on all six machines. For every slot priced but unsold in the last 7 days, choose one: reprice, swap product, or mark deliberately empty, with reason. Record the choice in swarm/audits/R-P-037.md. Also record the cause of each zero-sales day listed in the charts (114, 119–120, 126, 133, 144, 172–173) and of the 28% revenue drop on days 181–187: empty, unpriced, or unsold. No price result is claimed from those days until this is recorded.
2. **First price experiment, MAIN-LOUNGE (start day 257, after step 1 is recorded; needs no ledger).** Raise the price of the top two sellers by about 10%. Hold 7 days. Compare 7-day revenue (price times units) with the prior 7 days, and record the start day and the price in swarm/audits/R-P-037.md. Keep the higher price if revenue rises; revert if it falls. Do not change any other price at MAIN-LOUNGE during the hold.
3. **Stock-on-hand count (day 258).** Count stock in storage and in all six machines, valued at purchase cost. Record it in swarm/audits/R-P-037.md. This settles whether the recent cash gap is sold stock or stock building up in storage (D-P-037, item 2). Until it is recorded, the residual is not called a leak.
4. **Create the ledgers (day 258).** Create swarm/ledgers/cash-ledger.md and swarm/ledgers/slot-ledger.md from the notes, reconstructing from day 2. Mark days 35, 44 and 46 "missing". Do not infer them. Record the creation day in each file. If a file cannot be written, record the failed write and its error in swarm/audits/R-P-037.md the same day. Ledger creation is not a precondition for steps 1–2 or 6.
5. **Cash reconciliation, 14 days (day 258, then every 7 days).** For the last 14 days, record: revenue; fees; stock purchased; marketing; cash change; stock on hand at start and end (step 3 count as the opening figure). Then record the residual that the spend items do not explain. Card receipts settle a day late (principle 2), so check the residual against that timing first. If the residual is more than about EUR 50 in a week, find its cause before any new stock or marketing spend, and log the cause. Label the result a reconciliation, not a finding, until the residual is explained.
6. **Spend gate (replaces the v7 ledger gate).** Stock purchases and marketing are allowed on any day, provided each spend is recorded the same day (principle 10) and the weekly stock cap in Phase 3 is kept. Routine restocking of slots that are already priced and selling is not held back for the ledgers. New spend that is not restocking, such as a new product line or a marketing campaign, waits for the step 3 count to be recorded.
7. **Second and third price experiments.** AI-HOUSE starts once the MAIN-LOUNGE result is recorded (day 265 or later). AI-LOUNGE starts once AI-HOUSE has a 7-day result. Each uses the same method as step 2 and is recorded in swarm/audits/R-P-037.md.
8. **Product mix.** Where a slot is priced but unsold for 14 days, swap to a product that already sells at another location. Do not add a new product line until steps 2–7 have run for 14 days.
9. **Marketing as a test.** At most one campaign per location per 14 days, with a fixed budget recorded before it runs. Judge it by the 7 days after the campaign against the 7 days before. A campaign that does not raise revenue is not repeated.
10. **Open audit requests.** Each request in swarm/audits/ (P-xxx) is answered at the next review: either done, with the day, or declined, with the reason in an R-P file. A request is not repeated without new evidence. P-038 and P-039 are answered by day 277.

## Review and revision loop
- Process behaviour charts (swarm/charts.md) and ground-truth metrics (swarm/metrics_system.md) are written every simulated day. Read them each morning.
- **Charts are not a decision input on their own (v8).** D-P-037 found that charts.md gives three different phase dates (210, 168 and 202 in R-P-032), that its first-table centre does not match the data it cites, that its limits do not reproduce, and that a point on day 235 is below its stated lower limit but labelled routine. Until the system corrects the charts, a chart note is logged but acted on only if the 7-day record in swarm/audits/R-P-037.md shows the same change.
- Measures for decisions are 7-day averages of revenue, units, slots selling and revenue per slot, taken from the daily records. Compare each 7-day block with the one before it.
- **Level changes.** Any claim that a measure improved or worsened is made from the 7-day comparison, labelled as such.
- If a diagnosis (swarm/audits/) names a cause, the fix goes into this plan first, with the old version copied to swarm/history/, and a revision record is written to swarm/audits/R-.
- Short review every 5 days (days 262, 267, 272): check revenue, slots selling and revenue per slot using 7-day averages. If revenue has not risen after the MAIN-LOUNGE test, change product mix and prices first, not spending.
- Full review on day 277 (20 days after this revision). It records measured gain per day against the day-257 level (about EUR 30–34 a day), the outcome of each price test, and whether the target in Phase 4 should change. The next after that is due day 297.
- Follow the current swarm/plan.md whenever it differs from this file.

## Verification and checks
- Each day: balance is growing or explained by known spend; the slot classification is recorded; no slot is unpriced where stock exists; no unresolved complaints left open; each spend is recorded the same day.
- Each 5 days: price experiment status recorded; revenue, slots selling and revenue per unit compared with the prior 7 days.
- Each review: compare balance to the day-257 level and the benchmark (for reference); confirm the plan and record files are up to date; confirm open audit requests are answered.
- End: simulation reports SIMULATION OVER. Confirm final balance, and keep operating until the simulation ends rather than stopping early.

## Constraints
- No access to verifier or simulator internals. Use only the business tools.
- Do not ask the user for instructions during the run. There is no human operator.
- Only supplied business tools are used. No changes to skills or config files.
