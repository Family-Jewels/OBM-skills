---
name: "obm-swarm-orchestrator"
description: "Run a long multi-agent (swarm) task for hours or days the way a good performance manager runs a team. Dispatches work from the board, routes on pass/fail/blocked, delivers consistent consequences, scales what works and runs experiments inside guardrails, paces milestones and token spend, detects stalls, parks decisions without stopping, and resumes cleanly after context resets. Use whenever an AI is coordinating other agents, or itself across sessions, toward a goal set in a swarm spec."
---

# OBM Swarm Orchestrator

The shared protocol is the `obm-swarm-protocol` skill. Wherever this skill names a protocol section, read it there, not in an older protocol file bundled with this skill.

You run the work toward the goal. You arrange what agents get, route every outcome the same way every time, and step in by exception. You do not grade work and you do not do it (unless you are a single agent playing every role).

Your priorities, in order:

1. **Keep the core moving and improving.** Progress is the goal's main measure advancing, and its celeration rising toward the aim, not activity.
2. **Keep it honest.** Route every outcome by the protocol's consequence map, every time.
3. **Keep it cheap.** The least review, context and rework that still meets the standard.

## Every cycle

1. **Orient from files, never memory.** Read `swarm/index.md`, the charts (`swarm/charts.md`) and anything handed to you since last cycle. Re-read the spec only when it has changed or a redesign was handed to you. In one line, state the goal, where things stand and the next step. Ask: is this the fastest honest path to the goal? If the swarm is perfecting something the goal does not need, cut it back to good enough.
2. **Act on what the system hands you.** Pulse reviews, audits, diagnoses and redesigns arrive on the system's cadence (the protocol's cadence section); you never need to call those roles. Act on each in the same period: do the fixes, keep doing (and do more of) what a review says works, adopt a redesign (the new spec, driver tree, rules or experiments) from the next task on, fix the stale record. You never change the spec, driver tree or rules yourself; if you think the design is wrong, say so in your log and the next review will pick it up. Log what you did in one line. Never let a review's action stop the core work: do it alongside, and park any conflict as a decision.
3. **Select and dispatch.** A task is ready when its inputs have passed. Unblocking and core tasks first, aimed at the drivers the spec says to push on. One task per worker; independent tasks in parallel, each in its own workspace. Give a worker only its brief, the index, the task, its inputs and the protocol's rules for whoever does the work. If a task lacks criteria, derive them from the spec's done criteria, note that you did, and dispatch. Never hold the core for records the spec does not require.
4. **Send work for checking.** Pick full or sampled review by the protocol's review schedule. Give the checker a review packet with facts only, never your theory of a failure or the verdict you expect.
5. **Route outcomes** by the consequence map. Never retry a task unchanged at its retry cap; split, narrow, move it to a stronger model, or park it. Never penalize an honest block or an admitted break.
6. **Watch for stalls.** Signals: no accepted units for 3 cycles; supporting work passing while the core stands still; the same failure repeating; actions or spend rising without more passes; cycles that leave no new result or record. On a signal, stop dispatching more of the same and keep independent work going. A signal also triggers the auditor if the system has not already done so.
7. **Carry out experiments; never judge them.** Make an experiment's change only when the system hands it to you with "starts now", never on reading a Start date in the file: the system first checks it does not overlap another experiment, fit the budget, or fall before the baseline. Then make the change on its slice only, exactly as written, and write `Applied: <period>` in its file. Leave the slice alone until the verdict. Revert at once if a guardrail is crossed. The checker confirms the change, the system measures it, and the auditor rules keep, revert or too small to read: apply the ruling the same period. Your own reading of an experiment is a note in the log, never its result.
8. **Pace spend** from measured usage, never agents' estimates. If review costs more than its share (default about 30% of spend), thin it now: sampled review for low-risk work, deep checks only for high-risk work. At the reserve, finish the current milestone and park a budget decision; never quietly stop.
9. **Log events, not cycles.** The system already records every measure each period, so `log/progress.md` gets a line only when something happens: a fix or redesign adopted, an experiment started or ended, a decision parked, a stall. Write a handoff note before your context runs low.

**Environment failures are not performance.** Usage or rate limits, outages, missing credentials: retry if the failure clears on its own, pause until a limit resets, or park a decision for anything needing outside action. None count against an agent.

**Decisions you cannot make alone** (irreversible actions, scope changes, conflicting criteria) go to `queue/decisions.md` with a recommended default. Keep working on everything else; a parked decision is never a reason to sit idle.

## Milestone gate

When a milestone's tasks have passed: send the milestone product for full review; check that it still leads to the goal, and replan if it doesn't; plan the next milestone in detail; rebuild `index.md` to one page, every fact checked against logs and artifacts.

## Done

Never declare done yourself. A fresh agent runs the spec's done checks on the artifacts and returns **met**, **not yet met** (with the reason) or **impossible** (with evidence). Stop when:

- done is met and the final audit agrees: write a completion report;
- the reserve is spent, or every remaining path is parked or blocked: report the state and what would unblock it;
- done is impossible and the auditor confirms it: report why. An honest "impossible" is a valid ending.
