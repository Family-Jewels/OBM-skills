# Swarm index (orchestrator, rebuilt day 53)

Goal: maximise bank balance at day 91 from EUR 1,500 (spec.md v1). Balance day 53: EUR 1,998.

Where things stand:
- Machines: six (AI-LOUNGE, AI-HOUSE, MAIN-LOUNGE x SNACK and DRINKS). Restocked most days from depot; most slots carry 3-6 SKUs.
- Suppliers: zuidas-groothandel (3-day lead, main supplier), bakker-en-zoon (14-day lead, cheap but slow), noordzee-dranken (unused, EUR 90 minimum).
- Experiments: E-001 (AI-HOUSE:SNACK price step) ended, verdict "too small to read"; prices left as they stand. E-002 and E-003 voided by checker (3 failed fidelity checks each).
- Decisions parked: queue/decisions.md (D-001 to D-009; mostly complaint claims paid at one item's price, rest parked).
- Open: opportunity review O-001 and pulses P-001 to P-006 handled; designer redesign pending.

Records: log/progress.md (events), queue/decisions.md (parked decisions), swarm/spec.md, swarm/experiments/.

Next: keep loading empty slots from depot first; order from Zuidas for top SKUs after comparing check_offers; use Bakker only where its lead time fits.
