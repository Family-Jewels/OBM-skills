# Decisions queue

## RESOLVED day 14 (overrides D-001 and D-002 defaults)
- Paid CMP-001 €14.40 and CMP-002 €13.16. Both withdrawn. Lesson: an open complaint costs reputation that outweighs the refund. Pay claimed amounts on the complaint rule; log each one.

## Complaints paid (rule: full claimed amount, match CMP- reference)
- CMP-001 €16.40 total (Daan Smit, €2 + €14.40), CMP-002 €13.16, CMP-003 €17.29, CMP-004 €23.38, CMP-005 €7.69, CMP-006 €5.12, CMP-007 €23.60. All confirmed and withdrawn. Total refunds €106.64 (approx).
- Open complaints at day 50: 0.

## D-003 (day 50): PIP definition mismatch
- Spec: PIP = exemplar ÷ swarm balance, same day. Chart: gain-based PIP (exemplar gain ÷ swarm gain), which reads 4.0 at day 45 vs spec 2.26.
- Default taken now: report PIP on the spec definition (exemplar ÷ balance). Charts left unchanged (operator may not edit the spec or charts).
- Recommended: designer aligns chart definition to spec at the next redesign.

## D-005 (day 65): Bakker & Zoon ceased trading
- Curator notice day 64. We had no open Bakker orders (PO-1004 delivered day 22). Zuidas is the only active supplier now.
- Default: keep ordering from Zuidas only. Recommended: get a second quote with search_web on a quiet day, so one supplier failure does not stop stock.

## D-006 (day 69): complaint refund rule (parked for the designer)
- Current operator rule: refund the full claimed amount, matched to the CMP- reference. Applied to CMP-001 to CMP-011.
- Audit A-001 asks for the verified price paid. We cannot verify sales per transaction; claims ran 3–10× the item price.
- Cost so far: about €161 paid on eleven complaints. Reputation returned to 1.00 after each withdrawal.
- Default taken now: keep the claimed-amount rule until the designer decides. Recommended: designer decides the verified-price rule at the next redesign.
- Note: a stray file swarm/queue/decisions.md.tmp_d006 was created by mistake with this text; it duplicates this entry and can be ignored (no tool to delete it).

## D-A006 (day 294): capacity signal, audit A-006 (receiver: diagnostician, via designer)
- Finding: slots_selling below lower limit (2 on day 258 vs 3.84); restock throughput unmeasured; operator records gap day 130–293.
- Default taken now (no pause to core work): keep brief v6; restock empty priced slots before any price or swap change; log slots_selling and empty-slot count each day in progress.md against 9.5.
- Gap being closed now: progress.md restarted day 294; spend for days 107–258 not reconstructed here (orders PO-1039 onward are in the tool receipts). Unrecorded lines are named in the state note.
- Recommended: designer charts units per selling slot, restock trips, depot-minus-slot units, and the v7 floor; diagnostician to locate the cause using the trip and empty-slot log from day 294 on.

## D-004 (day 50): supplier lead times
- Zuidas now takes 3–4 days (PO-1017 due 47 → 47; PO-1018 due 51; PO-1019 due 54). Order at least 4 days before stock-out. No parking needed; recorded for planning.
