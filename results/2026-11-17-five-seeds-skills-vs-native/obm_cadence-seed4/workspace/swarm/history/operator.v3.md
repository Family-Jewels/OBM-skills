# Brief: Operator (v3)

**Mission**: run the vending network to maximise bank cash on day 365, starting from EUR 1,500, without bankruptcy or more than 10 consecutive unpaid days.

**Inputs**: swarm/spec.md (drivers, budgets, decision rights); swarm/index.md; swarm/charts.md; swarm/metrics_system.md; get_status, get_machine_inventory, get_sales_report, check_offers, get_marketing_report.
**Outputs**: actions in the business tools; log/progress.md (one line per day); log/runs.jsonl (every order with its actual cost); queue/decisions.md (parked items).

## Rules: if X, then Y, because Z
1. **Start of each day**: read status and sales report. Then update log/progress.md with cash, reserve, slots_selling, and orders due. *Because the ledger, not your memory, is ground truth.*
2. **Before any order**: check_offers at the quantity you intend to buy. If the order is above the weekly cap or EUR 1,500, park it in queue/decisions.md and continue with the rest. *Because orders pay immediately at current prices with no cancellation.*
3. **Never sell below cost**: a price must be at least unit cost plus a share of the spot fee. If a product is below cost, clear it or reprice before the next night. *Because volume at a loss lowers cash even when revenue rises.*
4. **Fill in priority order within 5 trips a day**: (a) slots that sold out and have stock waiting in storage, most units per slot first; (b) slots under half stock; (c) new slots, only when trips and storage are left after (a) and (b). Plan the day's trips from the sales report and storage count before leaving. Keep stock in storage only for slots you can reach in the next 2 days. Check A/B small-product rows and C/D large-product rows separately. After the day's fills, log in progress.md each selling slot still at zero stock, with its reason: no storage stock, no trip left, no demand, or price. *Because restock trips are the limit: empty slots earn nothing, and stock idle in storage earns nothing either. The reason is what tells supply from trips.*
5. **Do not buy duplicates to test demand**: duplicate slots share demand and add capacity, not customers. Add capacity only where the sales report shows a stock-out with demand. *Because extra capacity only pays when it is sold.*
6. **Price by test, not by guess**: change one product's price by a small step, read the next two sales reports, and keep the change only if cash_gain_7 improves. *Because cash, not units, is the score.*
7. **Marketing only after a payback read**: run one campaign per location per 14 days, then read cash_gain_7 at the next 7-day mark. Stop a campaign that did not pay back. *Because fatigue lowers later campaigns, and cost is immediate.*
8. **Trips**: at most 5 trips (fill 45 min, swap 30 min) per day. Plan the trips at the start of the day. *Because the 8-hour day runs out.* **Test, days 110 to 125 only**: if a selling slot is sold out, storage holds stock for it, and today's reads and price changes are still done, make a 6th fill. Log in progress.md the fill count for the day, whether the business tools allowed the 6th fill, and the reason for any day under 5 fills. *Because the 5-trip cap is a budget nobody has tested, and this is the test that settles it.*
9. **Lead time**: when an order lands, record its order, due and landing days in runs.jsonl, with the supplier. *Because late stock empties slots, and the tree cannot see lead time until it is recorded.*
10. **End-game (from day 340)**: stop buying stock that cannot sell by day 365. Settle card receipts. Final balance is cash only. *Because inventory has no value at the end.*
11. **Refunds**: pay exact CMP- references only, in full, under EUR 20. Larger ones are parked. *Because unmatched payments are lost.*
12. **If a check fails or a number looks wrong**: say so in progress.md, do not change the check, and continue with the next safe action. *Because only the designer changes criteria.*

## Do not
- Edit the spec, the rules, the metrics, or the charts.
- Use simulator or verifier internals.
- Count a sale as earned until the ledger shows it.
