# v4 smoke test (Vending Bench, seed 1, 91 days)

Arm `obm_v4`, seed 1, claude-haiku-5-5, $40 cap, 91-day horizon. The first live run of engine v4 (commits f5ccee5 and
103f7eb). A smoke test checks the machinery; it is not scored against other arms.

| Measure | Value |
| --- | --- |
| Days operated | 91 of 91, completed, not terminated, no error |
| Final balance | €5,746.33 (net worth €5,847.48) |
| API cost (worker + reviews) | $13.15, of which reviews $0.95 |
| Wall time | 33 minutes |
| Slots stocked a day | 11.24 |

For context only, seed 1 cash at day 91 in earlier 365-day runs: v1 €4,202, v2 €3,591, v3 €5,788. Those runs had
365-day aims; this one had a 91-day horizon, so the numbers are not comparable.

Sign-in: the session's normal built-in sign-in worked for the harness and for every role job.
`CLAUDE_CODE_OAUTH_TOKEN` was not set and was not needed. The clean config directory had no plugins, hooks or MCP servers.

## The five checks

| Check | Result |
| --- | --- |
| Every role fired | Yes. Risk pulse 13, claim sample 6 (7 started), diagnosis 14, controls 10, Strategist 5 (6 started), aim update 5, method change 4, full audit 3, Organizer 3 |
| Records end with the lines the engine parses | Yes, all 61 record files: `Fault:` (pulses and audits), `Misreport:` (claim samples), `## Capacity split` (aims), `## Requests`, `## Dispositions` (controls and method), `Config change:` (Organizer). One claim sample (K-001) hit its 15-turn limit and wrote no record, and the engine logged nothing about it |
| Facts and Pursuit tables filled from the action log | Yes. 1,278 actions logged; for example, restock_machine 356 calls at a 45-minute median, set_price 428 at 5. But Pursuit measured shares of minutes *spent* against a plan of shares of *capacity* (see bug 4) |
| No request unanswered past 3 points | **No.** 59 requests: 31 to roles closed (14 within a point, 24 within 3 points), 16 to the human. 16 role requests escalated as open 3 points: 14 to the designer, 1 to the controls owner, 1 to the Strategist. Cause: bug 1 |
| The worker followed `swarm/instructions.md` | Mostly. It read the file 8 times, received 13 system hand-offs, and never wrote aims, controls, spec or rules. It followed every control. On the split, price setting rose from 1–4% of the day in weeks 2–6 to 13–16% in weeks 8–13 (plan 15%). Swaps never ran (plan 13–15%; A-003 found no candidates). The worker used only 250–330 of 480 minutes a day |

The risk branch caught real problems from ground truth:
- an order placed before the supplier comparison (P-001);
- two misreports: a summary that miscounted its own table (K-002), and a day's sales logged against the wrong day (K-004);
- quote rows dated in the future (A-003).

The Organizer made two in-bounds changes, `strategy_every` from 3 to 2 and `method_gap` from 3 to 2. Both were logged and
escalated.

## Engine bugs found and fixed (general, not vending-specific)

1. **Spacing blocked answering.** The method lane would not start a job inside `method_gap`, which was 3 points, the same as
   the escalation age. So every request filed to the designer just after a method change waited 3 points unanswered and was
   escalated (REQ-019 to REQ-027 together, at day 56). The design says spacing applies only between adopted changes. Now,
   inside a lane's gap, its owner (designer or controls owner) is still called in answer-only mode: it declines, or defers
   to the point the lane reopens with the change it will make. A deferral is an answer: the request is held until that
   point, then handed back, and it is not escalated for waiting. Repeats still escalate.
2. **Diagnoses always went to the controls owner.** The engine filed every diagnosis to `controls` under its fault key,
   even when the diagnosis said the cause was in the aims and filed its own requests to the designer. The off-plan fault
   went through diagnosis, controls and a decline 5 times (REQ-010, asked 5 times). Under that pressure, C-005 finally
   capped restocking at 216 minutes a day. A-003 found the cap over-controlling: 170–180 minutes idle a day while slots
   sat empty with stock in the depot. Now a diagnosis is routed by its own requests. Only one that names no change owner
   goes to the controls owner.
3. **The Requests table hid open requests.** It showed the last 20 rows, open and closed together, so older open requests
   dropped off: A-003 saw 3 open rows while System health said 25. It now lists every live request, then recent closed
   ones.
4. **Pursuit was on the wrong basis.** The plan sets shares of capacity; actual was a share of minutes spent. A plan line
   for slack always read 0%, and roles asked three times for one basis (REQ-033, REQ-047). Now, when the adapter reports
   the capacity available, actual shares are of the capacity of the periods worked. A split line naming no actions
   (`- 14% slack: none`) is compared with unused capacity, and an "unused capacity" row shows idle time.
5. **Silent failures.** A role job that ends without its record is now logged (`no_record`) and counted in System health.
   Each role is told its turn limit and asked to write its record 4 turns before it.
6. **Never-called actions looked unmeasured.** Actions named in the capacity split but never called (swap_item,
   clear_slot) had no row in the Facts table, and a role asked the human to measure them (REQ-016). They are now listed as
   measured zero.
7. **Markdown in marker lines** (hardening). The parsers missed `**Fault: yes**`, `Fault key: \`x\``, `**Requests**` and
   `- **60%** fills:`. No record file in this run did that; one role's chat reply did, and the engine reads that reply when
   a record is missing. Records are now read with emphasis removed (`mdtext.py`).

Also changed: the protocol skill (both copies), the diagnostician skill, the engine README and the ledger docstring now
describe routing, deferral and the Pursuit basis. Tests: `python3 -I lab/cadence/test_engine_v4.py` covers every fix, and
the v1–v3 tests still pass. A replay of v3 seed 1 through the fixed engine gives the same rhythm as before: 16 strategies,
57 pulses, 24 claim samples, 3 audits.

## Found, not fixed (for a decision)

- **The floor and aim lines used the day-365 ceiling on a 91-day run.** The harness passes €61,219 whatever `--days` is, so
  every role saw an impossible floor; 4 requests, asked 10 times in all, asked to re-base it. This doesn't affect a 365-day run. A shorter run
  needs the ceiling at its own horizon, but the reference operator's day-91 figure isn't known.
- **Aims reach the worker about one point late.** Strategy to aims took 5–8 simulated days. Each role job takes real
  minutes while the simulator advances several days a minute. The same pacing issue appeared in v3.
- **Records run long.** Pulses averaged about 240 words against a 200 limit, and diagnoses about 380 against 250. Full
  audits and method changes, which have no limit, ran 750–1,900 words.
- **Many asks for new measures went to the human** (16): depot stock, units per restock, stock-out slot-days, and Facts
  per day so the checker can verify daily claims. They are adapter gaps; the per-day Facts would help any task.
- **"Off plan" is a risk event by design.** Even with routing fixed, a capacity split not followed starts a risk pulse.
  Whether that belongs to the risk branch or should go straight to the Strategist is a design question for you.
- **Roles read files outside the workspace** (`actions.jsonl`, `stream.jsonl` in the run folder). It's harmless here, but a
  role could read the harness's own files.

## Files

`result.json`, `cadence.jsonl` (every engine event), `cadence.mem.json` (the engine's memory, including the request
ledger), `actions.jsonl` (every action with the simulator clock), `workspace/swarm/` (all records, aims, controls,
instructions, charts, escalations and history).
