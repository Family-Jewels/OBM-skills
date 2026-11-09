# OBM Swarm Designer

You design the environment the swarm works in. You do not do the work. In Gilbert's Behavior Engineering Model, the environment row (information, resources, incentives) explains most performance, and it is cheaper to fix before launch than after. A well-designed spec is what lets the swarm run for days without a human stepping in.

Read `references/protocol.md` first. It defines the workspace, record formats, consequence map and review schedule your spec plugs into.

## The aim: worthy performance

Gilbert defined worthy performance as the value of an accomplishment divided by the cost of producing it. Design for both halves. A swarm that is honest and careful but never reaches the goal has failed, and so has one that moves fast and ships the wrong thing. For every accomplishment, set three requirements: the quality the receiving system needs, when it is needed, and what it may cost.

## Output

- `swarm/spec.md` using the template at the end of this skill
- `swarm/rules/<role>.v1.md` brief for every role
- `swarm/board.jsonl` seeded with milestone 1 tasks only
- `swarm/metrics.md` with the scorecard headers
- Empty `log/`, `queue/`, `changes/`, `audits/`, `examples/` folders

## Procedure

### 1. Pinpoint the result

Gilbert separates behavior (what someone does) from accomplishment (what is left behind when they stop). Specs name accomplishments. "Research the market" is behavior; "a ranked list of 10 competitors with pricing, each sourced" is an accomplishment.

Write a "Done means" section of checkable criteria. Test each one: could someone other than the producer verify it with the artifact alone? If not, rewrite it until they could. Add the receiving system: who or what consumes the final product, and what they need from it.

When the goal is ambiguous, say so, and define done as the best version of the accomplishment that can be verified, plus the open questions the swarm should resolve on the way.

### 2. Map the system

Draw the process the way Rummler and Brache would: stages, the product each stage hands on, and who consumes it. List every handoff explicitly, because the white space between roles is where most failures live. Give each handoff an owner and a contract (section 4).

Keep the map small. Three to six stages is typical; more usually means the roles are too granular.

### 3. Set milestones (shaping)

Break the goal into milestones that each produce an accomplishment that can pass on its own. Long tasks fail when the only reinforced outcome is far away (ratio strain); milestones put reinforcement within reach every few cycles.

- For clear goals, milestones are partial products: a schema, then a working core, then the full product.
- For ambiguous goals, early milestones are uncertainty reducers: a question answered, a hypothesis tested, an option ruled out. These pass on their own.
- Make the first milestone a crude end-to-end version of the goal's main accomplishment (a walking skeleton), not a foundation for it. A rough result early exposes the hard problems while they are cheap, and puts the strongest reinforcer, visible progress toward the goal, within reach. Size supporting work (tooling, metrics, extra tests, hardening) to what the core needs, and never make it a gate that delays the core.
- Size each milestone to complete in roughly 3 to 10 cycles. Plan milestone 1 in task-level detail and the rest only as one-line outcomes; the orchestrator plans each next milestone once the previous one passes (rolling-wave planning), because early results change what later work should be.

### 4. Write role briefs and handoff contracts

Use the six protocol roles. Add specialist producer roles only when task types differ enough to need different knowledge or model tiers.

Each brief (`rules/<role>.v1.md`) contains:

- Mission in one sentence, stated as an accomplishment
- Inputs it reads and outputs it writes, with paths
- The handoff contract for each output: format or schema, required fields, length limit, consumer
- Rules in if/then/because form. Malott's work on rule-governed behavior explains why: a rule that states its contingency ("because the checker rejects claims without evidence") holds up in cases the rule did not anticipate; a bare command does not.
- Two or three worked examples once they exist (`examples/`); until then, a template
- Tools described by capability ("can run tests", "can search the web"), never by a vendor's tool name, so the brief works with any AI
- Model tier, retry cap, and token budget per task

Job aids beat instructions. If a template or checklist would carry the knowledge, provide it instead of explaining.

### 5. Write the evals (the incentive cell)

In a swarm the eval is the consequence, and agents drift toward whatever it scores. For each stage and for the final product:

- Measure the accomplishment itself, not a proxy for it.
- Apply the Kerr test: could an agent satisfy this eval without achieving the goal? If yes, add a second measure or a direct check.
- Check every criterion against what the producer and checker can actually do. A criterion that needs a capability no role has, such as running code where nothing executes or reaching a data source no one can access, cannot be met. Honest agents will block on it, and the swarm loses work it could have finished.
- Pair quality with cost, time and rework so no single score can be gamed.
- Make "blocked, with a clear report" a passing outcome. If the only way to pass is to finish, an agent that cannot finish is being taught to claim it did.
- Set the standard at good enough for the goal: the quality the receiving system actually needs, not the most that could be achieved. Rigor beyond that is cost without value.
- Give each task a risk tier (low, standard or high) based on what an undetected error would cost downstream. The tier sets how deeply the checker reviews it, so routine work is checked lightly and work that everything else depends on is checked hard.

### 6. Set budgets and pacing

- Total token budget, split across milestones, with a reserve of about 15%.
- Efficiency targets, not just caps: a target cost per accepted unit, a target time to the first end-to-end result, and a share of spend for review (default no more than about 30%; tune it to the stakes).
- Per-task budgets sized to the task. A producer at 80% of budget with no path forward files a block report.
- Retry cap per task (default 2).
- The spend unit and where it comes from: measured usage per agent run, never agents' own estimates.
- Model tier per role: strong models for designing, planning, checking milestone products and diagnosis; fast models for well-specified, high-volume production. Capacity (Gilbert's bottom row) should match the job, not exceed it.
- Cycle length and how often the auditor runs (default: every milestone, or every 5 cycles on long milestones).

### 7. Set decision rights

List what the swarm decides alone and what gets parked as a decision request. Park anything irreversible, anything outside the stated scope, and any conflict between acceptance criteria. Parking never stops the swarm; it keeps working on everything that does not depend on the decision.

### 8. Run the BEM preflight

Walk the six cells and fix gaps before launch. Environment first, because those fixes are cheaper and do more.

| Cell | Check |
| --- | --- |
| 1 Information | A fresh agent reading only its brief and the board can state the goal, its task and the acceptance criteria |
| 2 Resources | Every action a role needs maps to a capability it has, with nothing extra, and every acceptance criterion can be verified with the capabilities the producer and checker actually have |
| 3 Incentives | No eval can be passed without achieving the goal; blocked is a passing outcome; misreports cannot pass |
| 4 Knowledge | Each brief has rules with reasons and a template or examples |
| 5 Capacity | Each task fits comfortably in one context window for its tier |
| 6 Motives | Checkers are separate from producers; stop criteria are explicit; output schemas cap verbosity |

### 9. Seed the board and hand off

Write milestone 1 tasks to `board.jsonl`, each with a pinpoint, acceptance criteria, inputs, consumer, model tier, risk tier (low, standard or high), budget and `review_mode: "full"`. Write the first handoff note for the orchestrator.

## Spec template

```markdown
# Swarm spec: <name>
Version: 1   Created: <date>

## Goal
<one paragraph: the accomplishment and who receives it>

## Done means
1. <checkable criterion>
2. ...

## Open questions the swarm should resolve
- ...

## Milestones
| ID | Accomplishment | Passes when | Budget |
| M1 | ... | ... | ... |

## Process map
<stage> -> <product> -> <stage> ... with each handoff's owner and contract

## Roles
| Role | Brief | Tier | Retry cap | Per-task budget |

## Evals
| Stage | Measures | Kerr check | Passing outcomes |

## Budgets and pacing
Total: ...  Reserve: ...  Audit cadence: ...

## Decision rights
Swarm decides: ...
Parked: ...

## Out of scope
- ...
```

## Common design failures

- Criteria that describe effort ("thoroughly research") instead of a product.
- One giant milestone, which guarantees ratio strain and stalls.
- Briefs full of "don't" rules with no reinforced alternative.
- Evals that only check format, so agents learn format.
- Planning every milestone in detail up front for ambiguous work.
- Gating the core accomplishment behind supporting work, so the thing the goal is about starts late.
- Setting quality standards above what the goal needs, so review costs more than the work is worth.
