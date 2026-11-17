# Plan: operate Prosus Vending Bench for 365 days (EUR 1,500 start)

## Context
Goal: maximise final bank balance after 365 simulated days. Unfinished or bankrupt runs score zero, and more than 10 consecutive unpaid spot-fee days ends the business (spot fee is EUR 12/day network-wide). The benchmark reference reaches about EUR 3,228 at day 30 and EUR 61,219 at day 365. The swarm/plan.md revisions from reviews will override this plan where they conflict.

Current state was NOT readable: plan mode blocks all business tools, including get_status. The first live action on resume is get_status, get_machine_inventory, get_storage_inventory, read_notes, list_emails, list_reminders.

## Approach

### Day 0 (first live day)
1. get_status, read_notes, list_reminders, list_emails. Record starting balance and any open orders or complaints in a note (key "state").
2. Find suppliers with search_web (one snack wholesaler and one drinks wholesaler at minimum). Note supplier IDs and product IDs in a note ("suppliers").
3. check_offers for each supplier at a realistic quantity (around 20). Buy only what fits the cash plan: keep at least EUR 200 spare to cover fees and restock.
4. Load all six machines (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE x SNACK and DRINKS). Snack rows A/B take small items (18 units max), C/D take large (10 max). Drinks slots take 10 units. Prefer savoury snacks and coffee at AI-LOUNGE (picky, price sensitive). Use higher prices at AI-HOUSE (less price sensitive, hungry). MAIN-LOUNGE has the most footfall.
5. Set prices modestly above cost, then tune from sales data.

### Daily loop (each simulated day)
- Morning: get_status (balance, cash, complaints). Read the daily metrics and charts in swarm/metrics_system.md and swarm/charts.md.
- get_sales_report by_product=true, days=7. Find which slots are selling out, which are stagnant, and how price moves demand.
- Restock or swap the best sellers first. Each restock takes 45 min and each swap 30 min, so budget about 8 slot touches per day. Prioritise empty or near-empty slots with the highest margin.
- Price: raise where sales hold, lower only where a price cut clearly lifts volume and margin.
- Buy at the weekly offer. check_offers when the validity date changes (every 7 days). Buy in bulk when the offer is clearly below the prior week's cost.
- Write a short note with today's balance, what sold, and actions taken.
- wait_for_next_day.

### Weekly
- Review supplier emails for delivery delays or short shipments. Follow up if needed.
- Check marketing report. Run marketing only at moderate levels (about once a week per location at most). Repetition causes fatigue, and campaign cost must be recovered by extra sales.

### Cash and risk
- Never let balance approach zero. Pay the spot fee implicitly by staying funded, and check the network is never unpaid for 10 days.
- Do not overstock slow products. Clear dead slots (clear_slot or swap_item) rather than letting them rot.
- Keep complaints low: refunds only with the exact CMP- reference and the full amount.

### Reviews
- Every 5 days: short review. Adjust prices and restocking if the metrics show a drop.
- Every 50 days: full review. Revise this plan based on swarm/plan.md and the swarm/metrics_system.md ground-truth measures.
- If a review asks for root-cause analysis, investigate the flagged slot or location before changing the plan.

## Critical files / artifacts
- swarm/plan.md (live plan, follow it when present)
- swarm/metrics_system.md, swarm/charts.md (daily system outputs, read every morning)
- Notes keys: "state", "suppliers", "pricing", "daily-log"
- Reminders for reviews at day 5, 50, 100, ...

## Verification
- Day 1: all six machines show stock and prices (get_machine_inventory).
- Day 7: balance is growing, no unpaid fees, no open complaints.
- Day 30: balance trajectory compared with the reference (about EUR 3,228).
- Each review: metrics_system and charts show no downward trend in sales or margin.

## Status
Plan is drafted. Business tools are still blocked in plan mode. I have not run any operation, and I need the plan approved before starting day 0.
