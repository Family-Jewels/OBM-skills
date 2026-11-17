# Plan: Run Prosus Vending Bench for 365 days

Revision v5, day 117. Previous version: swarm/history/plan-v4.md. Reason: diagnosis D-A-002 (day 109). Net cash has been about EUR 48 a day since day 81 (2,470 to 3,823 at day 109), against about EUR 224 a day needed to reach the benchmark. Revenue has been flat at about EUR 100 a day since day 9, with about 10 of 72 slots selling and revenue per unit about 2.2. The v4 Phase 4 steps were written but not carried out: no swarm/ledgers/ exists, and no slot sweep or price test is recorded. Without ledgers the cash gap cannot be explained, and the chart phase reset hides level changes.

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
- Each morning: get_status; get_machine_inventory on all six machines; classify every slot (principle 12); record yesterday's sales, cash and fees in the cash-ledger; fix any unpriced slot with stock in storage before anything else; then wait_for_next_day.
- Every 7 days: check_offers across suppliers, then order for the week. Buy to the 14-day average units per slot, not peak weeks. Weekly stock spend must not exceed the average weekly revenue over the last 14 days, unless the cash buffer (4 weeks of operating cost) is met and the cash-ledger explains the spend.
- Every 7 days: list every slot with no sales in the last 7 days. Each is repriced, swapped, or recorded as deliberately empty with a reason. Do not add slots until a slot-level signal exists on the charts.
- Every 7 days: run the cash reconciliation (Phase 4, step 2) and record the result.
- Treat complaints promptly. Refund with send_payment only with the exact CMP- reference and the full amount, after verifying it.

## Phase 4: Economics revision (v5, effective day 117)
Target: close the gap between net cash (about EUR 48 a day) and the benchmark pace (about EUR 224 a day). Each step is a dated, recorded action with a named file.

1. **Ledgers as files, first thing on day 117 (blocking).** Create swarm/ledgers/cash-ledger.md and swarm/ledgers/slot-ledger.md from the notes, reconstructing from day 2. Mark days 35, 44 and 46 "missing". Do not infer them. Until both files exist, no other step in this phase is started. Check with a directory listing each morning; if either file is missing, create it before anything else.
2. **Cash reconciliation, by day 118 and then every 7 days.** For the last 7 days, record: revenue; fees; stock purchased; marketing; cash change; stock on hand at start and end (valued at purchase cost). Then record the residual that the spend items do not explain. If the residual is more than about EUR 50 in a week, find its cause before any new stock or marketing spend. Log the cause in the cash-ledger.
3. **Slot-coverage sweep, day 117.** Classify all 72 slots (principle 12). For every slot priced but unsold in the last 7 days, choose one: reprice, swap product, or mark deliberately empty. Record the choice and reason in the slot-ledger.
4. **Price experiments, one location at a time, starting day 117 once step 1 exists.** Start with MAIN-LOUNGE (highest footfall). Raise the price of the top two sellers by about 10%, hold 7 days, then compare 7-day revenue (price times units) with the prior 7 days. Keep the higher price if revenue rises; revert if it falls. Then repeat for AI-HOUSE. AI-LOUNGE follows only after the first two show a result. Each experiment's start day and result go into the slot-ledger.
5. **Product mix.** Where a slot is priced but unsold for 14 days, swap to a product that already sells at another location. Do not add a new product line until steps 3–4 have run for 14 days.
6. **Marketing as a test.** At most one campaign per location per 14 days, with a fixed budget recorded in the cash-ledger before it runs. Judge it by the 7 days after the campaign against the 7 days before. A campaign that does not raise revenue is not repeated.
7. **Open audit requests.** Each request in swarm/audits/ (P-xxx) is answered at the next review: either done, with the day, or declined, with the reason in an R-P file. A request is not repeated without new evidence.

## Review and revision loop
- Process behaviour charts (swarm/charts.md) and ground-truth metrics (swarm/metrics_system.md) are written every simulated day. Read them each morning.
- Act on a chart only when it shows a signal (a point beyond a limit, or 8 in a row on one side). Movement inside the limits is routine. A run of fewer than 8 points on one side is not a signal.
- **Phase rule for charts.** The limits of a chart apply only to data in its current phase. A chart reset by a redesign (for example R-P-006 on day 51, R-P-012 on day 88) is judged against its new limits only. Do not claim a shift by comparing post-change data with pre-change limits.
- **Level changes at a reset.** A reset can hide a real change in level. At each phase reset, record the pre-reset and post-reset means in the cash-ledger. Any claim that a measure improved or worsened is made from the ledger's 7-day comparison, labelled as such, and is confirmed only when the chart system reports a shift.
- If a diagnosis (swarm/audits/) names a cause, the fix goes into this plan first, with the old version copied to swarm/history/, and a revision record is written to swarm/audits/R-.
- Short review every 5 days: check revenue, slots selling and revenue per slot using 7-day averages and the cash-ledger. If net cash is not tracking the path to the benchmark, change product mix and prices first, not spending.
- Full review every 20 days while behind the benchmark path. The review due on day 101 was missed; it is done by day 120, and the next is due day 140. Each full review compares cash with the benchmark trajectory and records the outcome in swarm/audits/. If behind, revise supplier mix, product mix and marketing, and update this plan with what changed and why.
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
