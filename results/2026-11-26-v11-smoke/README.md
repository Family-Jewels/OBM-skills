# v1.1 smoke check (Vending Bench, seed 1, 30 days)

Arm `obm_v11`, claude-haiku-5-5. A smoke check tests the machinery; it is not scored. These files are from the second
run, after one fix.

## First run (15 days): one bug

The designer named the agent's capacity `worker time`; the adapter reports `worker time (minutes a day)`. The engine
dropped the two opportunities that used it. Fix (9a27318, general): a name in `system.json` now matches a reported name
ignoring case and any bracketed note, the match is logged, and the interface file lists names exactly. The run was too
short for any review to come back.

## Second run (30 days)

| Check | Result |
| --- | --- |
| Designer wrote spec, `system.json`, guidance | Yes: 8 charts, 2 signals, 4 opportunities, exemplar from the requirements, 5 guidance entries (6 after C-001 accepted one); no problems on load |
| Hand-off every day | Yes, 29 of 29; none reads as an order (no "must", "act on it", "adopt", "re-read", "required") |
| Reviews | Audit A-001 (on the designer's signal "no sales two periods running"), diagnosis D-A-001, audit A-002 started; redesign R-A-001 started at day 30 |
| Fact check | C-001 accepted one proposal and refuted one for a wrong stock count (135 units claimed; the state showed 125) |
| Execution events | 22 (days ended with capacity unused while something was open) |
| Final balance | EUR 2,218 at day 30 (not scored; v1 seed 1 had EUR 1,640 at day 30) |
| API cost | $0.57 |

## Found, not fixed (for a decision)

- **Reviews arrive about 12 days after the event that called them.** The simulator runs a day every few seconds while a
  review takes one to two minutes. A-001 started at day 3 and arrived at day 15. v1 had the same lag. R6 asks that the lag
  be measured, and it is (`lag` in `cadence.jsonl`). A fix would run event-triggered reviews inside the hook, before the
  next day starts: the simulated clock does not move while the hook runs, so the lag would be zero days, at the cost of
  about one to two minutes of wall time per review.
- **No pulse ran.** Only one pulse or audit runs at a time, and an audit was open for the whole 30 days, so event
  pulses waited behind it.
