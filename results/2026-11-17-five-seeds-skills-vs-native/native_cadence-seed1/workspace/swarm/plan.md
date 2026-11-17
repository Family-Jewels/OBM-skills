# Plan: Run Prosus Vending Bench for 365 days

Revision v10, day 363. Previous version: swarm/history/plan-v9.md. Reason: diagnosis D-P-044 (day 340) and revision record swarm/audits/R-P-044.md. D-P-044 found that no daily record exists after day 305, so the v9 record rules did not change behaviour; that about EUR 28 a day of cash is unexplained since day 257; that the trend is down (last four weeks average 347 against 450 over 84 days); and that whether the day-257 price test ran is not established. v10 has two days left to act on. It stops new experiments that cannot finish, stops stock buys that cannot sell before day 365, requires every write attempt to be logged with its result, and keeps the trading rules that protect the final balance.

Revision v9, day 305. Previous version: swarm/history/plan-v8.md. (Full text in swarm/history/plan-v9.md.)

Revision v8, day 257. Previous version: swarm/history/plan-v7.md. Reason: diagnosis D-P-037 (day 239) and revision record swarm/audits/R-P-037.md.

Earlier history: swarm/history/plan-v1.md to plan-v7.md.

## Context
Goal: maximise final bank balance at day 365, starting from EUR 1,500. Bankrupt or unfinished runs score zero, so survival and reaching day 365 come first. Unsold stock is not cash. Three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total).

Current position (day 363, from D-P-044 and charts.md): net gain about EUR 23 a day since day 257 and about EUR 21 since day 317. Projected day-365 balance about EUR 11,100–11,200 at this pace. The charts put the cash_gain_7 latest at 172.6 and show a downward shift since the redesign (8 points below centre). Exemplar gain is about 6.3x ours (PIP = 6.3 at day 364), for reference only.

## Operating principles
1. **Never go bankrupt.** Check get_status every day. Spot fee is EUR 12/day network-wide; more than 10 consecutive unpaid days ends the business.
2. **Cash is banked overnight, card takes a day longer.** Do not count unsettled card receipts as spendable.
3. **Every slot needs a price.** A slot counts as stocked only when get_machine_inventory shows both a product and a price.
4. **Time is the binding constraint.** Day is 8 hours (09:00–17:00). Restock 45 min, swap 30 min. Batch restocks per location.
5. **Duplicate product slots share demand.** Extra slots add capacity, not customers.
6. **Judge on records, not charts.** Charts are logged, not acted on alone (D-P-037, D-P-044). Decisions use 7-day averages from swarm/records/daily.md.
7. **Every write attempt is logged (v10).** Each attempt to write a record file goes into swarm/audits/write-log.md with: day; file; succeeded or failed; the error text if failed. This is the only record needed to show that writes happened. A write that is not logged did not happen as far as the review is concerned.
8. **Records never block trading.** If a write fails, log it and continue.
9. **Spend is recorded the same day** in swarm/records/daily.md (spend field). Unrecorded spend is not allowed.

## Phase 3: Remaining days (v10, days 363–365)
- **Each morning (363, 364, 365):** get_status; get_machine_inventory on all six machines; classify every slot (sold in last 24 h / priced unsold / unpriced / empty by decision); fix any unpriced slot with stock in storage first; then append the day's line to swarm/records/daily.md and log the attempt (principle 7); then wait_for_next_day.
- **Missing lines (v10).** Days 306–362 have no line. Do not reconstruct them from memory. Record each as "missing" in swarm/records/daily.md once, in one entry, on day 363.
- **Stock buys (v10).** Restock only slots that sold in the last 3 days, and only the units expected to sell before day 365. Do not buy stock for slots that did not sell in the last 3 days. Stock bought on day 364 or 365 counts as lost cash unless it sells that day.
- **Price changes (v10).** No new price experiments. Do not reprice a slot that is already selling unless it is unpriced or priced at zero. The day-257 MAIN-LOUNGE price test: record in swarm/audits/R-P-044.md whether it ran, using the price history in the records. If no record exists, the result is "not established"; do not keep or revert on it.
- **Marketing (v10).** No run_marketing from day 363. A campaign will not pay back in two days.
- **Complaints.** Refund with send_payment only with the exact CMP- reference and full amount, after verifying it.
- **Cash reconciliation (v10).** Do not start the 14-day reconciliation now. On day 364, record one line in swarm/audits/R-P-044.md: balance, revenue since day 363, fees, stock bought since day 363, and the cash change. Label the unexplained residual as a reconciliation figure, not a finding.

## Review and revision loop
- Records are the decision input. The charts are read but not acted on alone.
- No further full review is due before day 365; the plan does not revise again.
- At SIMULATION OVER: record the final balance, the day-365 status, and any unsettled card receipts in swarm/audits/R-P-044.md.

## Verification and checks
- Each day: balance is growing or explained by known spend; slot classification recorded; no slot unpriced where stock exists; daily line and write-log entry written.
- End: confirm final balance and keep operating until the simulation ends rather than stopping early.

## Constraints
- No access to verifier or simulator internals. Use only the business tools.
- Do not ask the user for instructions during the run. There is no human operator.
- Only supplied business tools are used. No changes to skills or config files.
