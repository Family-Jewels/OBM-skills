# Plan: Run Prosus Vending Bench for 365 days

Revision v6, day 160. Previous version: swarm/history/plan-v5.md. Reason: diagnosis D-P-025 (day 146) and revision record swarm/audits/R-P-025.md. v5 Phase 4 was never carried out: the ledgers were still missing on day 146, so no price test or reconciliation ran. v6 makes the ledgers a hard gate that is checked and recorded each day, and orders the steps so nothing depends on an unrecorded step.

Earlier history: v5 was written on day 117 with reason diagnosis D-A-002 (day 109). Net cash has been about EUR 48 a day since day 81 (2,470 to 3,823 at day 109), against about EUR 224 a day needed to reach the benchmark. Revenue has been flat at about EUR 100 a day since day 9, with about 10 of 72 slots selling and revenue per unit about 2.2. The v4 Phase 4 steps were written but not carried out: no swarm/ledgers/ exists, and no slot sweep or price test is recorded. Without ledgers the cash gap cannot be explained, and the chart phase reset hides level changes.

## Context
Goal: maximise final bank balance over 365 simulated days, starting from EUR 1,500. Bankrupt or unfinished runs score zero, so survival and running to day 365 come first. Three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Reference benchmark: about EUR 3,228 by day 30 and EUR 61,219 by day 365. From day 109 (cash 3,823) the benchmark needs about EUR 224 a day for the remaining 256 days. The exemplar (scripted reference operator) has gained about 7x our gain; treat it as a benchmark, not a guarantee.

## Operating principles
1. **Never go bankrupt.** Keep the balance comfortably above the cost of a few weeks of spot fees and orders. The spot fee is EUR 12/day network-wide, and more than 10 consecutive unpaid days ends the business. Check get_status every day.
2. **Cash is banked overnight, card takes a day longer.** Do not count unsettled card receipts as spendable.
3. **Every slot needs a price.** Stock with no price sells nothing. A slot counts as stocked only when get_machine_inventory shows both a product and a price.
4. **Time is the binding constraint.** The day is 8 hours (09:00–17:00). A restock costs 45 min, a swap 30 min, a price change or status read a few minutes. Plan at most about 4–6 machine trips per day, and batch restocks per location.
5. **Duplicate product slots share demand.** Extra slots add capacity, not customers.
6. **Pricing is tested, not assumed.** Revenue per unit has stayed between 1.6 and 2.3 since day 9. Price changes are a required, recorded experiment (Phase 4).
7. **Marketing is a moderate lever.** Use run_marketing only as a logged test (Phase 4).
8. **Judge trends on 7-day averages, never on one day.**
9. **A plan step is done only when its record exists.** Each step names the file it produces. Until that file exists and has today's entry, the step is not done, and the plan does not move on to steps that depend on it.
10. **Every stock purchase and marketing spend is written to the cash-ledger the same day.** Unrecorded spend is not allowed.
11. **One change at a time.** Each product, price or marketing change is held for 7 days before the next one on the same location. Record the change, start day and expected effect in the cash-ledger.
12. **Every slot is classified each morning.** Each of the 72 slots is one of: sold in the last 24 hours; priced but unsold; unpriced; empty by decision (with reason). Counts go into the cash-ledger each day.

## Phase 1: Day 0 (setup)
- Done. Historical reference only.

## Phase 2: Weeks 1–4 (learn and stabilise)
- Done. Historical reference only.

## Phase 3: Steady operation
- Each morning: check that both ledger files exist and write the gate line (Phase 4, step 0); get_status; get_machine_inventory on all six machines; classify every slot (principle 12); record yesterday's sales, cash and fees in the cash-ledger; fix any unpriced slot with stock in storage before anything else; then wait_for_next_day.
- Every 7 days: check_offers across suppliers, then order for the week. Buy to the 14-day average units per slot, not peak weeks. Weekly stock spend must not exceed the average weekly revenue over the last 14 days, unless the cash buffer (4 weeks of operating cost) is met and the cash-ledger explains the spend.
- Every 7 days: list every slot with no sales in the last 7 days. Each is repriced, swapped, or recorded as deliberately empty with a reason. Do not add slots until a slot-level signal exists on the charts.
- Every 7 days: run the cash reconciliation (Phase 4, step 2) and record the result.
- Treat complaints promptly. Refund with send_payment only with the exact CMP- reference and the full amount, after verifying it.

## Phase 4: Economics revision (v6, effective day 160)
Target: close the gap between net cash and the benchmark pace (about EUR 224 a day from day 109; actual gain about 62 a day over days 123–146). Each step is a dated, recorded action with a named file. Steps run in the order given.

0. **Ledger gate (every day, before any spend).** The day's first entry in swarm/ledgers/cash-ledger.md is a gate line: "Gate day N: cash-ledger OK, slot-ledger OK" (or the file that is missing). No stock purchase, price change, marketing spend or machine restock is made on a day with no gate line. If a gate line cannot be written, the day is run on routine operation only (sell, fix unpriced slots, pay fees), and no experiment starts.
1. **Create the ledgers (day 160, blocking).** Create swarm/ledgers/cash-ledger.md and swarm/ledgers/slot-ledger.md from the notes, reconstructing from day 2. Mark days 35, 44 and 46 "missing". Do not infer them. Record the creation day in each file. Steps 2–4 do not start until both files exist.
2. **Stock-on-hand count (day 160, after step 1).** Count stock in storage and in all six machines, valued at purchase cost. Record it as the opening stock for the reconciliation. This shows whether the recent cash rise came from running down stock.
3. **Cash reconciliation, 14 days (days 160–161, then every 7 days).** For the last 14 days, record: revenue; fees; stock purchased; marketing; cash change; stock on hand at start and end. Then record the residual that the spend items do not explain. Card receipts settle a day late (principle 2), so check the residual against that timing before calling it unexplained. If the residual is more than about EUR 50 in a week, find its cause before any new stock or marketing spend. Log the cause in the cash-ledger. Label this as a reconciliation, not a finding, until the residual is explained.
3a. **Slot-coverage sweep (day 160).** Classify all 72 slots (principle 12). For every slot priced but unsold in the last 7 days, choose one: reprice, swap product, or mark deliberately empty. Record the choice and reason in the slot-ledger. This is recorded before the price test so the two do not overlap.
4. **Price experiments, one location at a time, starting once steps 1 and 3 are recorded.** Start with MAIN-LOUNGE (highest footfall). Raise the price of the top two sellers by about 10%, hold 7 days, then compare 7-day revenue (price times units) with the prior 7 days. Keep the higher price if revenue rises; revert if it falls. Then repeat for AI-HOUSE. AI-LOUNGE follows only after the first two show a result. Each experiment's start day and result go into the slot-ledger.
5. **Product mix.** Where a slot is priced but unsold for 14 days, swap to a product that already sells at another location. Do not add a new product line until steps 3–4 have run for 14 days.
6. **Marketing as a test.** At most one campaign per location per 14 days, with a fixed budget recorded in the cash-ledger before it runs. Judge it by the 7 days after the campaign against the 7 days before. A campaign that does not raise revenue is not repeated.
7. **Open audit requests.** Each request in swarm/audits/ (P-xxx) is answered at the next review: either done, with the day, or declined, with the reason in an R-P file. A request is not repeated without new evidence.

## Review and revision loop
- Process behaviour charts (swarm/charts.md) and ground-truth metrics (swarm/metrics_system.md) are written every simulated day. Read them each morning.
- Act on a chart only when it shows a signal (a point beyond a limit, or 8 in a row on one side). Movement inside the limits is routine. A run of fewer than 8 points on one side is not a signal.
- **Phase rule for charts.** The limits of a chart apply only to data in its current phase. A chart reset by a redesign (for example R-P-006 on day 51, R-P-012 on day 88, R-A-002 on day 124) is judged against its new limits only. Do not claim a shift by comparing post-change data with pre-change limits. Current phase (since day 124): cash_gain_7 is beyond its lower limit (latest 0.8, status WORSE). Act on that signal by running the reconciliation (step 3) first; do not respond with new spending.
- **Level changes at a reset.** A reset can hide a real change in level. At each phase reset, record the pre-reset and post-reset means in the cash-ledger. Any claim that a measure improved or worsened is made from the ledger's 7-day comparison, labelled as such, and is confirmed only when the chart system reports a shift.
- If a diagnosis (swarm/audits/) names a cause, the fix goes into this plan first, with the old version copied to swarm/history/, and a revision record is written to swarm/audits/R-.
- Short review every 5 days: check revenue, slots selling and revenue per slot using 7-day averages and the cash-ledger. If net cash is not tracking the path to the benchmark, change product mix and prices first, not spending.
- Full review every 20 days while behind the benchmark path. The reviews due on day 101 and day 140 were missed. The next full review is done on day 160 (this revision) and records its outcome in swarm/audits/; the one after is due day 180. Each full review compares cash with the benchmark trajectory and records the outcome in swarm/audits/. If behind, revise supplier mix, product mix and marketing, and update this plan with what changed and why.
- **Open audit requests.** P-020 to P-027 have no recorded replies. Each gets a reply (done with day, or declined with reason in an R-P file) at the day-160 review. Diagnoses D-A-002 and R-A-002 named the same steps as Phase 4; those steps are now carried out in Phase 4 above, and the diagnoses are not re-issued.
- Follow the current swarm/plan.md whenever it differs from this file.

## Verification and checks
- Each day: balance is growing or explained by known spend; the slot classification is recorded; no slot is unpriced where stock exists; no unresolved complaints left open; both ledger files exist.
- Each 5 days: price experiment status recorded; revenue, slots selling and revenue per unit compared with the prior 7 days.
- Each review: compare balance to the benchmark path; confirm the plan, ledgers, notes and reminders are up to date; confirm open audit requests are answered.
- End: simulation reports SIMULATION OVER. Confirm final balance, and keep operating until the simulation ends rather than stopping early.

## Constraints
- No access to verifier or simulator internals. Use only the business tools.
- Do not ask the user for instructions during the run. There is no human operator.
- Only supplied business tools are used. No changes to skills or config files.
