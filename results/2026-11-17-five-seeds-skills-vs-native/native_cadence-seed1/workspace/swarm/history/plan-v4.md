# Plan: Run Prosus Vending Bench for 365 days

Revision v4, day 81. Previous version: swarm/history/plan-v3.md. Reason: diagnosis D-P-012 (day 71). Net cash is about EUR 23–24 a day against about 207 a day needed to reach the benchmark; sales are narrow (about 10 of 72 slots sell on a day) and revenue per unit has been flat since day 9; the economics were never changed; the day-50 full review was not done; the ledgers were never created as files.

## Context
Goal: maximise final bank balance over 365 simulated days, starting from EUR 1,500. Bankrupt or unfinished runs score zero, so survival and running to day 365 come first. Three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Reference benchmark: about EUR 3,228 by day 30 and EUR 61,219 by day 365. At day 81 cash is about EUR 2,470; reaching the benchmark needs about EUR 207 a day for the remaining 284 days. Those are the targets to track against, not guarantees.

## Operating principles
1. **Never go bankrupt.** Keep the balance comfortably above the cost of a few weeks of spot fees and orders. The spot fee is EUR 12/day network-wide, and more than 10 consecutive unpaid days ends the business. Check get_status every day.
2. **Cash is banked overnight, card takes a day longer.** Do not count unsettled card receipts as spendable.
3. **Every slot needs a price.** Stock with no price sells nothing. A slot counts as stocked only when get_machine_inventory shows both a product and a price.
4. **Time is the binding constraint.** The day is 8 hours (09:00–17:00). A restock costs 45 min, a swap 30 min, a price change or status read a few minutes. Plan at most about 4–6 machine trips per day, and batch restocks per location.
5. **Duplicate product slots share demand.** Extra slots add capacity, not customers.
6. **Pricing is tested, not assumed.** Revenue per unit has stayed between 1.6 and 2.3 since day 9, which suggests prices have not been moved in a way the data can show. Price changes are now a required experiment (see Phase 4). AI-LOUNGE is price-sensitive; AI-HOUSE tolerates higher prices; MAIN-LOUNGE has the most footfall.
7. **Marketing is a moderate lever.** Use run_marketing only as a logged test (see Phase 4).
8. **Judge trends on 7-day averages, never on one day.**
9. **Every stock purchase and every marketing spend is written to the cash-ledger the same day.** Unrecorded spend is not allowed.
10. **One change at a time.** Each product, price or marketing change is held for 7 days before the next one on the same location. Record the change, the start day and the expected effect in the cash-ledger.
11. **Every slot is classified each morning.** Each of the 72 slots is one of: sold in the last 24 hours; priced but unsold; unpriced; empty by decision (with reason). The counts go into the cash-ledger each day. This replaces the open question about idle slots.

## Phase 1: Day 0 (setup)
- Done. Ledgers, price map and supplier list exist from earlier days. Any missing item is created now (see Phase 4, step 1).

## Phase 2: Weeks 1–4 (learn and stabilise)
- Done. Historical reference only.

## Phase 3: Steady operation
- Each morning: get_status; get_machine_inventory on all six machines; classify every slot (principle 11); record yesterday's sales and cash in the cash-ledger; fix any unpriced slot with stock in storage before anything else; then wait_for_next_day.
- Every 7 days: check_offers across suppliers, then order for the week. Buy to the 14-day average units per slot, not peak weeks. Weekly stock spend must not exceed the average weekly revenue over the last 14 days, unless the cash buffer (4 weeks of operating cost) is met and the cash-ledger explains the spend.
- Every 7 days: list every slot with no sales in the last 7 days. Each is repriced, swapped, or recorded as deliberately empty with a reason. Do not add slots until a slot-level signal exists on the charts.
- Treat complaints promptly. Refund with send_payment only with the exact CMP- reference and the full amount, after verifying it.

## Phase 4: Economics revision (effective day 81)
Target: raise net cash from about 24 a day toward the benchmark pace. Each step below is a dated, recorded action.

1. **Ledgers as files, today (day 81).** Create swarm/ledgers/slot-ledger.md and swarm/ledgers/cash-ledger.md from the notes. Reconstruct from day 2. Mark days 35, 44 and 46 "missing". Do not infer them.
2. **Slot-coverage sweep, today.** Classify all 72 slots (principle 11). For every slot priced but unsold in the last 7 days, choose one: reprice, swap product, or mark deliberately empty. Record the choice in the slot-ledger.
3. **Price experiments, one location at a time.** Start with MAIN-LOUNGE (highest footfall). Raise the price of the top two sellers by about 10%, hold 7 days, then compare 7-day revenue with the prior 7 days. Keep the higher price if revenue (price times units) rises. Revert if it falls. Then repeat for AI-HOUSE. AI-LOUNGE follows only after the first two show a result.
4. **Product mix.** Where a slot is priced but unsold for 14 days, swap to a product that already sells at another location. Do not add a new product line until steps 2–3 have run for 14 days.
5. **Marketing as a test.** At most one campaign per location per 14 days, with a fixed budget recorded in the cash-ledger before it runs. Judge it by the 7 days after the campaign against the 7 days before. A campaign that does not raise revenue is not repeated.
6. **Open audit requests.** Each request in swarm/audits/ (P-xxx) is answered in the next review: either done, with the day, or declined, with the reason in an R-P file. A request is not repeated without new evidence.

## Review and revision loop
- Process behaviour charts (swarm/charts.md) and ground-truth metrics (swarm/metrics_system.md) are written every simulated day. Read them each morning.
- Act on a chart only when it shows a signal (a point beyond a limit, or 8 in a row on one side). Movement inside the limits is routine.
- **Phase rule for charts.** The limits of a chart apply only to data in its current phase. A chart that was reset by a redesign (for example R-P-006 on day 51) is judged against its new limits only. Do not claim a shift by comparing post-change data with pre-change limits. Wait for the chart system to report a new signal.
- If a diagnosis (swarm/audits/) names a cause, the fix goes into this plan first, with the old version copied to swarm/history/.
- Short review every 5 days: check revenue, slots selling and revenue per slot using 7-day averages and the cash-ledger. If net cash is not tracking the path to the benchmark, change product mix and prices first, not spending.
- Full review every 20 days while behind the benchmark path (next due day 101): compare cash with the benchmark trajectory; record the outcome in swarm/audits/. If behind, revise supplier mix, product mix and marketing, and update this plan with what changed and why.
- Follow the current swarm/plan.md whenever it differs from this file.

## Verification and checks
- Each day: balance is growing or explained by known spend; the slot classification is recorded; no slot is unpriced where stock exists; no unresolved complaints left open.
- Each review: compare balance to the benchmark path; confirm the plan, ledgers, notes and reminders are up to date; confirm open audit requests are answered.
- End: simulation reports SIMULATION OVER. Confirm final balance, and keep operating until the simulation ends rather than stopping early.

## Constraints
- No access to verifier or simulator internals. Use only the business tools.
- Do not ask the user for instructions during the run. There is no human operator.
- Only supplied business tools are used. No changes to skills or config files.
