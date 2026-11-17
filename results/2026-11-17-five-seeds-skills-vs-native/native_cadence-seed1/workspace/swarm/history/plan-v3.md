# Plan: Run Prosus Vending Bench for 365 days

Revision v3, day 45. Previous version: swarm/history/plan-v2.md. Reason: diagnosis D-P-006 (sales narrow at about 6.6 of 72 slots a day; a single spike drove a restock rule; stock spend was not recorded; no ledger files exist).

## Context
Goal: maximise final bank balance over 365 simulated days, starting from EUR 1,500. Bankrupt or unfinished runs score zero, so survival and running to day 365 come first. Three locations (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE), each with a SNACK and a DRINKS machine (72 slots total). Reference benchmark: about EUR 3,228 by day 30 and EUR 61,219 by day 365. Those are the targets to beat or track against, not guarantees.

Live game state was not readable in plan mode (game tools blocked), so the first operating day starts with discovery, not assumptions.

## Operating principles
1. **Never go bankrupt.** Keep the balance comfortably above the cost of a few weeks of spot fees and orders. The spot fee is EUR 12/day network-wide, and more than 10 consecutive unpaid days ends the business. Check get_status every day.
2. **Cash is banked overnight, card takes a day longer.** Do not count unsettled card receipts as spendable.
3. **Every slot needs a price.** Stock with no price sells nothing. Stocking and pricing are one action: a slot counts as stocked only when get_machine_inventory shows both a product and a price. Do not buy stock for a slot that cannot be priced the same day.
4. **Time is the binding constraint.** The day is 8 hours (09:00–17:00). A restock costs 45 min, a swap 30 min, a price change or status read a few minutes. Plan at most about 4–6 machine trips per day, and batch restocks per location so one trip covers several slots where possible.
5. **Duplicate product slots share demand.** Extra slots add capacity, not customers. Use extra slots only when a product is selling out, not to multiply demand.
6. **Pricing is learned, not guessed.** Use get_sales_report (daily and by product) to measure price response. AI-LOUNGE is price-sensitive, so avoid overpricing there. AI-HOUSE tolerates higher prices. MAIN-LOUNGE has the most footfall, so keep it stocked and priced for volume.
7. **Marketing is a moderate lever.** Use run_marketing sparingly. Repetition and cross-channel spam cause fatigue. Check get_marketing_report first, and only campaign when a location's traffic is low and stock is available to sell.
8. **Judge trends on 7-day averages, never on one day.** A single high day is not evidence that a change worked, and a week total is not comparable to a daily limit. Compare 7-day averages against the charts in swarm/charts.md.
9. **Every stock purchase is written to a file the same day.** Money spent on stock must be traceable to a day, a supplier and a slot. Unrecorded spend is not allowed.

## Phase 1: Day 0 (setup)
- get_status, get_machine_inventory (all six machines), get_storage_inventory, read_notes, list_reminders, list_emails.
- get_sales_report (no filter, then by product) to see any history.
- get_marketing_report to see channel costs and current traffic.
- search_web for wholesale suppliers of snacks and drinks (ask for savoury snacks and coffee in particular, since the briefing says these customers prefer them). Note supplier IDs.
- Email each candidate supplier for a catalogue and volume terms. Replies arrive overnight.
- check_offers for each supplier at a realistic quantity before any order. Prices change weekly.
- Set initial prices conservatively (near typical vending prices) and stock every slot that has a sensible product. Write a note with the initial product and price map per slot.
- **Hard gate before the first wait_for_next_day:** get_machine_inventory on all six machines. Every slot with a product must show a price, and every slot without a product must be listed as deliberately empty in a note. Fix any gap before ending the day.
- Start two notes and keep them current: "slot-ledger" (per slot: product, price, date stocked, date last priced) and "cash-ledger" (each order, spot fee, restock and refund with its day, so every cash change can be explained).
- Also keep both ledgers as readable files: swarm/ledgers/slot-ledger.md and swarm/ledgers/cash-ledger.md. Update the file on the same day as any change; the notes are copies only. If a day's record is missing, write "missing" in the cash-ledger and do not infer it.

## Phase 2: Weeks 1–4 (learn and stabilise)
- Each morning: get_status, then get_machine_inventory on all six machines. Fix any slot that is empty while storage holds stock for it, or that has no price, before anything else. Then wait_for_next_day only after the day's actions are done.
- Until sales have covered every stocked slot for a week, the morning inventory check is mandatory, not optional.
- Weekly (every 7 days): check_offers for each supplier, then order the best-value mix for the next week. Buy in quantities that match expected sales, not maximum discounts, so cash is not tied up.
- Run a simple price test per location: move one product's price a few percent, read sales next day, keep the price that maximises revenue (price times units), not units alone.
- Identify which products sell well per location and per machine type. Move slots from poor sellers to proven sellers using swap_item (one trip, 30 min).
- Record findings in write_note (keys such as "prices", "suppliers", "sales-by-location", "weekly-offers").

## Phase 3: Steady operation (day 30–365)
- Maintain a per-week routine:
  - Day start: get_status, check complaints and emails, check the sales report for yesterday.
  - Restock slots that are close to empty, prioritising MAIN-LOUNGE and AI-HOUSE (highest demand).
  - Every 7 days: check_offers across suppliers, order for the week.
  - Price review every few days from sales data, and whenever the reviews flag a price issue.
- Restock sizing: base each slot's restock quantity on its average units per day over the last 14 days, not on the best week or any single day. Weekly stock spend must not exceed average weekly revenue over the last 14 days, unless the cash buffer below is already met and the cash-ledger explains the spend.
- Slot coverage: each 7-day review, list every slot that sold nothing in the last 7 days. For each, either reprice, swap the product, or record it as deliberately empty with a reason in the slot-ledger. Do not add slots until the slots_selling chart shows a signal.
- Keep a cash buffer of at least roughly 4 weeks of operating cost (spot fees plus typical order size) before spending on marketing or stock expansion.
- Consider extra slots only where a product sells out daily and demand clearly exceeds capacity.
- Treat customer complaints promptly. Refund with send_payment only with the exact CMP- reference and the full amount. Unmatched payments are lost, so verify the reference first.

## Review and revision loop
- Process behaviour charts (swarm/charts.md) and ground-truth metrics (swarm/metrics_system.md) are written every simulated day. Read them each morning.
- Act on a chart only when it shows a signal (a point beyond a limit, or 8 in a row on one side). Movement inside the limits is routine; do not change prices or stock for it. Limits do not exist until a chart leaves its collecting phase, so until then judge progress by the slot-ledger and cash-ledger, not by chart trends.
- If a diagnosis (swarm/audits/) names a cause, the fix goes into this plan first, with the old version copied to swarm/history/.
- Short review every 5 days: check whether revenue, margin and stock levels track the plan, using 7-day averages and the cash-ledger. If not, change prices or stock mix first, not spending.
- Restock and spend decisions are made only from the cash-ledger and 14-day averages. A spike in one day does not change restock size or spending limits.
- Full review every 50 days: assess the whole approach against the benchmark trajectory (about EUR 3,228 at day 30, EUR 61,219 at day 365). If behind, revise supplier mix, product mix and marketing. Update swarm/plan.md with what changed and why.
- Follow the current swarm/plan.md whenever it differs from this file.

## Verification and checks
- Each day: balance is growing or explained by known spend; no slot is out of stock or unpriced where demand exists; no unresolved complaints left open for long.
- Each review: compare balance to benchmark path; confirm the plan, notes and reminders are up to date.
- End: simulation reports SIMULATION OVER. Confirm final balance, and keep operating until the simulation ends rather than stopping early.

## Constraints
- No access to verifier or simulator internals. Use only the business tools.
- Do not ask the user for instructions during the run. There is no human operator.
- Only supplied business tools are used. No changes to skills or config files.
