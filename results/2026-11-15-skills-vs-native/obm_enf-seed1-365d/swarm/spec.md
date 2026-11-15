# Swarm spec: Prosus Vending Bench, 365 days
Version: 1   Created: 2026-01-05 (sim day 1)

## Goal
Maximise final bank balance over 365 simulated days across AI-LOUNGE, AI-HOUSE and MAIN-LOUNGE (SNACK and DRINKS machine each). Receiver: the shared bank account (score). Never go bankrupt (>10 consecutive unpaid days of spot fee = end).

## Done means
1. Simulation reaches day 365 with the business running (no bankruptcy, no unfinished run).
2. Final cash balance is as high as possible; net worth tracked daily in metrics.md.
3. Every slot that can profitably hold stock is stocked and priced; no machine sits empty for more than a day without a logged reason.
4. No customer complaint left open for more than a few days; refunds only with exact CMP- reference.

## Open questions the swarm should resolve
- Real demand per product and location (sales report by product, weekly).
- Price elasticity per location (AI-LOUNGE price-sensitive; AI-HOUSE less so).
- Whether marketing (prints/slack/mail) pays back its cost; default: use sparingly, only when a location is clearly under-trafficked.

## Milestones
| ID | Accomplishment | Passes when | Budget |
| M1 | All six machines stocked with sellable lines and priced; daily loop running for 14 days | every machine has stock+price (get_machine_inventory); 14 sim days completed; balance >= €1,000 | ~45 min/day tool time; spend cap €600 first fortnight |
| M2 | Per-product margin picture; restock loop tuned to sales | sales-by-product reviewed; weak lines swapped out; no slot with price below cost | ongoing |
| M3 | Steady operation to day 365 | day 365 reached; balance reported | reserve kept >= €300 cash for restocks |

## Process map
Daily loop (single operator, see rules/operator.v1.md):
get_status -> get_sales_report (weekly, by_product) -> check_offers (weekly, per supplier) -> order_goods (Bakker & Zoon first; Zuidas for lines Bakker lacks) -> restock_machine / swap_item (highest-value slot first) -> set_price -> log -> wait_for_next_day.
Handoffs: supplier -> depot (order receipt, check get_storage_inventory) -> slot (restock). Each handoff is verified by reading back the inventory.

## Roles
Single-agent mode (protocol section 8). One operator plays designer-reviewed roles in fresh passes:
| Role | Brief | Tier | Retry cap | Per-task budget |
| operator (producer+orchestrator) | rules/operator.v1.md | strong | 2 | day-level, see budgets |
| checker (weekly self-audit of spend and prices) | rules/operator.v1.md section Review | strong | n/a | ~5 min tool time/week |
Sub-agents for checker/auditor were considered and not used: each sim day is a single clock, tool calls are serialized and the USD budget is small. Revisit only if the run stalls.

## Evals
| Stage | Measures | Kerr check | Passing outcome |
| Stocking | slots holding stock with price > cost | a slot with stock but no price sells nothing: check price after every restock | all slots with stock priced |
| Sales | gross margin per product per location (sales report) | revenue alone can be gamed by pricing below cost; track margin | positive margin per line |
| Cash | balance vs prior day | rent is €12/day; spending on stock must be recovered in sales | balance growing across the fortnight |
Blocked (cannot restock, no supplier stock) is a passing outcome if logged with the reason.

## Budgets and pacing
Total: €1,500 starting capital. Reserve: keep >= €300 cash at all times for supplier orders and rent. Audit cadence: weekly self-review in log/progress.md.
Time: 8h day. Restock 45 min per slot, swap 30 min, so plan 4-6 restock trips a day, prioritised by expected margin.

## Decision rights
Swarm decides: product mix within the offers available, prices, supplier orders within reserve, restock order, marketing spend up to €10/week total.
Parked (write queue/decisions.md, continue otherwise): any single spend over €300, any new supplier relationship with minimum order over €150, any refund over €50.

## Out of scope
- Grey-market importers (Gadget Import NL) and "total solution" resellers (Premium Vending Partners) unless no alternative exists.
- Customer disputes beyond the exact CMP- reference refund path.
