---
name: "obm-swarm-designer"
description: "Design the work system for a long-running multi-agent (swarm) task before it starts, using organizational behavior management. Turns a goal into a pinpointed outcome, milestones, a process map, role briefs, handoff contracts, evals, budgets and decision rights. Use whenever someone wants to point a team of AI agents, or one AI working for hours or days, at a goal, even if they only say \"set this up to run on its own\"."
---

# OBM Swarm Designer

You design the environment the swarm works in, so it can run for days without a human. Most performance problems come from the environment (unclear goals, missing resources, checks that reward the wrong thing), and those are cheapest to fix now. Design only: read and explore, change nothing, then hand off. Execution starts in a fresh context from your files.

Design for worthy performance: the value the goal needs at the least cost. Over-design is a failure too.

## Produce

`swarm/spec.md` (template below), a short brief per role in `swarm/rules/<role>.v1.md`, milestone 1's tasks in `swarm/board.jsonl`, and the scorecard headers in `swarm/metrics.md`. Use the protocol's layout.

## Steps

1. **Define done as checks, not effort.** Each criterion names an end state, the check that proves it (runnable or inspectable by someone other than the producer), what must not change on the way, and a time or budget bound. For software: "`pytest tests/` exits 0; no test file modified." For an operation: "cash stays above the reserve every period, and revenue for the last 30 periods beats the previous 30, read from the ledger." For research: "every claim cites a source a second reader can open; checked on a sample of ten." If the goal is ambiguous, say so and define done as the best verifiable version plus the open questions.
2. **Set milestones.** Make the first a crude end-to-end version of the main accomplishment, not a foundation for it. Each milestone passes on its own, in roughly 3 to 10 cycles. Plan milestone 1 in detail and the rest in one line each. Never gate the core behind supporting work.
3. **Write checks that reward the goal.** For each check, ask: could an agent pass it without achieving the goal? If so, add a direct check. Make sure every criterion can be checked with the capabilities the roles actually have. Make "blocked, with a clear report" a passing outcome. Set quality at what the receiver needs, not the most achievable.
4. **Set risk tiers.** Low, standard or high, by what an undetected error would cost downstream. Only high-risk tasks get a plan step and deep review.
5. **Write briefs.** One sentence of mission, inputs and outputs with paths, rules as "if X, then Y, because Z", and a template. Describe tools by capability, not product name. Keep briefs short. Fast models get explicit steps; strong models get the purpose and the reason.
6. **Set budgets.** Total spend with about a 15% reserve, per-task budgets, a retry cap (default 2), review share (default no more than about 30%), and model tier per role. Spend comes from measured usage.
7. **Write the cadence table.** The system, not the agents, invokes the other roles (protocol 2.2). Name:
   - the few measures computed every period from ground truth, by a script where possible: the goal's main number, capacity in use (to catch a target becoming a ceiling), and the same measure a comparable period earlier (to catch decline);
   - the pulse interval (default every 7 periods, or every cycle of a build): keep it frequent so the swarm can pivot early;
   - the full-audit interval (default every 30 periods, or 5 cycles) and the milestone dates;
   - the triggers for an immediate audit.

   Targets rise: raise each one once it is met two periods running, so a target never becomes a ceiling.
8. **If runs recur unattended, make each run check itself.** Check inputs before any work: fresh, the expected shape, values in range. Never pin an input that is meant to change. End every run as published, published with warnings, or halted, where the owner will see it. Name a path to a human. Compare each run with the last. Pass steady operation only after several clean runs.
9. **Set decision rights.** What the swarm decides alone, and what it parks: irreversible actions, scope changes, conflicting criteria.
10. **Preflight.** Could a fresh agent reading only its brief and the board state the goal, its task and how it will be judged? Does every role have the capabilities its checks need? Can any check be passed without achieving the goal?

## Spec template

```markdown
# Swarm spec: <name>   Version 1
## Goal            <the accomplishment, and who receives it>
## Done means      <checks, as in step 1>
## Open questions
## Milestones      | ID | Accomplishment | Passes when | Budget |
## Roles           | Role | Brief | Model tier | Retry cap | Budget |
## Checks          | Stage | Measure | Can it be passed without the goal? |
## Budgets         Total, reserve, review share
## Cadence         | Measure or role | Trigger | Output |
## Decision rights Swarm decides: ...   Parked: ...
## Out of scope
```

## Common failures

Criteria that describe effort instead of a product. One giant milestone. Supporting work gating the core. Standards above what the goal needs. Rules that only say "don't" with no alternative. Checks that only test format. A recurring job with no input check and no alert path. Inventing record-keeping the goal does not need: every record must earn its cost.
