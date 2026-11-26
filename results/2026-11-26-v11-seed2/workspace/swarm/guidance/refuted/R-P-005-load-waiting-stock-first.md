# Load waiting stock before buying more
Revises: G-004
Applies when: O3
What good looks like: On a day with cash to spare and worker time unused, a strong period looks at the depot before it buys. Stock already waiting there, and empty slots beside it, is the nearest income, and loading costs the same minutes a purchase would. Buying adds to the depot and earns nothing until it is loaded. For example: a day that ends with units waiting in storage and most slots empty can load those fills first, then order only as much as the slots left after loading will take in the next few days. A small price test on one slot remains an option for the minutes left over.
Why: Ground truth on days 41–43, 49–50 and 55–58 shows units waiting in the depot (15, 121 and 53) with worker time under 10% used and most slots empty. Purchases on those days (PO-1014 on day 41, PO-1015 landing on day 49) added to the depot while sales stayed at 1–6 units a day. G-004 as written pointed to buying on the same days. See swarm/audits/D-P-005.md.
Source: diagnosis D-P-005
Revisit: day 100

Fact check: C-008 refuted at day 112 (not advice: it requires loading before buying and caps orders to the slots left after loading; also its claim that sales stayed at 1–6 units a day is false (23 units on day 41).)
