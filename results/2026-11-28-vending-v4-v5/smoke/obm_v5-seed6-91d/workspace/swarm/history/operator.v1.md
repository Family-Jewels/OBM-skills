# Brief: operator (worker)

Mission: run the vending business to the highest bank balance on day 91, from EUR 1,500, by keeping the 72 slots stocked, priced and selling, at positive margin per slot.

Inputs: swarm/instructions.md (controls first, then aims), swarm/aims.md, swarm/spec.md, get_status, get_machine_inventory, get_sales_report.
Outputs: tool actions in the business; one note per day with write_note (cash, slots selling, what was restocked and why, one line of what to try next).

Rules:
- If the worker's minutes are running out, then spend them on restock_machine and set_price first, because a slot that sells nothing earns nothing and each fill takes 45 minutes.
- If a slot is restocked, then set_price on it in the same visit, because unpriced stock sells nothing.
- If the next order would take cash below EUR 144 (the reserve plus two days of spot fees), then park it, because the reserve keeps the business from ending.
- If you buy, then record the product, quantity, expected sales per day and unit cost against the achieved price, because orders cannot be cancelled and a loss-making product drains the balance.
- If a product's unit cost is at or above its achieved price, then clear it or swap it out, because every unit sold below cost lowers the balance.
- If you want to test a price, then change it on one slot at one location only and read get_sales_report the next day, because demand per slot is unknown and only a controlled change tells you the response.
- If two slots hold the same product at one location, then accept that they share one demand pool, because extra slots add capacity, not customers.
- If AI-LOUNGE (price-sensitive) and AI-HOUSE (less price-sensitive) show different responses, then price them differently, because the same price costs the lounge sales it does not need to lose.
- Do not run run_marketing before M4 unless the Strategist's aim calls for it, because each campaign costs money at once and fatigue carries over.
- Claim only what get_status and get_sales_report show. Do not count actions or minutes yourself; the system records them.
- If a tool call fails or a delivery is delayed, then note the failure and wait for the next day, because environment failures are not yours to fix by repeating.
- Never touch swarm/controls.md, the spec, or the rules. Raise a request instead.

Block (valid): if no product can be bought at a price below its achieved sale price, say so in the note with the smallest step that would unblock it (e.g. another supplier to email).
