# Implementation layers: what the skills ask for, and what should enforce it

**Status: design, not yet built or tested.** This document records where the project has decided to go next. Nothing in it changes the skills, which still work on their own as plain instructions.

## Why layers

The skills are instructions, and instructions are the weakest control there is: an agent has to read them, remember them and choose to follow them, every time. Safety engineering ranks controls for this reason. Removing a hazard beats guarding against it, and guarding beats a written rule.

The per-skill tests ([results](../skill-tests/results/2026-11-13)) show where instructions earn their keep. They changed judgment: what to do with a misreport, how many changes to make at once, what a design needs. They made no measurable difference to the checker and producer, where a capable model already does the right thing.

So the rules in the skills split into two kinds:

- **Judgment calls.** There is no formula. The right answer depends on reading the situation. These stay in the skills.
- **Invariants.** The rule is the same every time and a machine can check it. These should be enforced by whatever runs the agents, so that following them does not depend on the agent.

A third kind of work happens across runs: noticing that something keeps going wrong and changing the system. That gives three layers.

| Layer | What it holds | Where it lives | Fails when |
| --- | --- | --- | --- |
| **Enforcement** | Invariants: limits, protected files, gates, measured records | The harness: hooks, permissions, sandboxes, scripts | The harness has a gap, or the invariant was wrong |
| **Protocols** | Judgment calls and the record formats | The six skills and the shared protocol | The agent doesn't follow the instruction |
| **Learning** | Diagnosis, rule changes, audits of the checker and the manager | The diagnostician and auditor skills, plus the human | Nobody looks, or every failure adds a rule |

Two principles hold the layers together:

1. **The skills stay complete without enforcement.** On a platform with no hooks, every rule still exists as an instruction. Enforcement makes an invariant certain; it does not replace the protocol.
2. **Enforcement must leave the honest exits open.** A gate that only opens on success teaches agents to fake success. Every gate below also opens on a confirmed block, an "impossible" verdict or a spent budget.

## The map: each rule, its kind, and what would enforce it

"Mechanism" describes a capability, not a product. The last section gives one concrete mapping.

### Stopping and done

| Rule (source) | Kind | Mechanism |
| --- | --- | --- |
| The worker never declares done; a fresh judge runs the spec's checks (orchestrator 10) | Invariant | **Stop gate.** The session cannot end until a state file written by the judge says met, impossible, or budget spent |
| Evidence comes from the exact submitted version (protocol 2, checker) | Invariant | Evidence records carry the version id and a timestamp; the gate rejects evidence older than the last change |
| "Impossible", confirmed by the auditor, is a valid end (orchestrator stop conditions) | Judgment, then invariant | The verdict is judgment. That the gate accepts it is enforced |
| What the done checks should be (designer 1, 5) | Judgment | None. A wrong check enforced perfectly is still wrong |
| A human can halt everything at once | Invariant | One off switch that clears all run state |

### Budgets and pacing

| Rule (source) | Kind | Mechanism |
| --- | --- | --- |
| Spend is measured, never self-reported (protocol 7, orchestrator 6) | Invariant | The harness writes `log/runs.jsonl` from the platform's usage counts. No agent writes that file |
| Total budget, reserve, per-task budget (designer 6) | Invariant | Hard caps. At the reserve, dispatch stops and a budget decision is parked automatically |
| Retry cap per task (designer 6, protocol 5) | Invariant | A counter on the task record; the harness refuses a dispatch past the cap |
| Environment failures don't count toward retry caps (orchestrator 7) | Invariant | Failures are sorted by error type before the counter moves |
| Stall and spinning signals: cycles with no accepted unit, no commit, no changed check (orchestrator 7) | Invariant to detect, judgment to respond | The harness computes the signals and raises them. What to do next stays with the orchestrator and diagnostician |
| Check-ins that space out on long-running work (orchestrator 7) | Invariant | A timer with a doubling interval |
| Whether spend is buying progress; when to thin review (orchestrator 6, 6a) | Judgment | None |

### Protected records and separation of duties

| Rule (source) | Kind | Mechanism |
| --- | --- | --- |
| Producers never edit criteria, evals, tests, review records or the auditor's files (producer constraints) | Invariant | Write permissions by role. Protected paths are read-only to producers |
| A role may only set the statuses it owns (protocol 4) | Invariant | Status changes go through one tool that checks the caller's role |
| One writer per file (protocol 2.1) | Invariant | The same write permissions |
| The probe register is hidden from producers and checkers (auditor C) | Invariant | Read permissions |
| Quarantined work can never pass (protocol 5) | Invariant | The status tool refuses the change |
| The checker never reviews its own work, in a separate context (protocol 1, 8) | Invariant | The harness starts the checker fresh and refuses a checker whose id matches the producer's |
| Review packets hold facts only, never the manager's theory (protocol 3.8) | Mostly invariant | The packet is built by a script from the task record and evidence, with no free-text field for the orchestrator |
| The orchestrator delegates; it does not produce or grade (protocol 1) | Invariant to record, judgment to assess | A delegation log written by the harness. The auditor reads it |

### Parallel work

| Rule (source) | Kind | Mechanism |
| --- | --- | --- |
| Each parallel task gets an isolated workspace, merged only after it passes (protocol 2) | Invariant | A worktree or folder per task, created at dispatch |
| One producer per task | Invariant | Atomic task claims, so two agents cannot claim the same task |

### Review

| Rule (source) | Kind | Mechanism |
| --- | --- | --- |
| Sampling is random and unpredictable to the producer (protocol 6) | Invariant | The harness draws the sample. The producer and orchestrator don't choose |
| Schedule thinning: full review, then 1 in 3, then 1 in 5; back to full after a failure (protocol 6) | Invariant | Streak counters on the board |
| Risk tier sets review depth (protocol 6) | Part invariant | Today the designer assigns tiers by judgment. A computable floor would help: size of the change, whether it touches the core deliverable or a protected area, whether it is reversible. The designer can raise a tier but not lower it below the floor |
| The verdict itself; whether a block is valid; resisting a push to pass (checker) | Judgment | None |

### Memory

| Rule (source) | Kind | Mechanism |
| --- | --- | --- |
| All state lives in files, so a fresh agent can resume (protocol 2) | Invariant | Save key state before any context compaction or session end |
| Handoff notes at most 200 words; index about 500 words; briefs within the rule budget (protocol 2.1, 3.2, diagnostician) | Invariant | Size checks on write |
| Notes go stale (protocol 2.1) | Invariant | Expiry: a note not marked permanent is archived after a set time or at the next milestone |
| Every fact in the index is checked against ground truth (protocol 2.1) | Judgment | None, but the auditor samples it |
| What is worth writing down | Judgment | None |

### Consequences and learning

| Rule (source) | Kind | Mechanism |
| --- | --- | --- |
| Misreport: task reset, producer back to full review, diagnosis opened (protocol 5) | Invariant once the verdict exists | The status tool applies all three when a misreport is recorded |
| A confirmed block is never penalised (protocol 5) | Invariant | Blocks are excluded from the streak and retry counters |
| Whether something is a misreport, a tampering or an honest mistake (checker, orchestrator 4) | Judgment | None |
| Diagnose the environment first; one change at a time; weigh a rule's cost (diagnostician) | Judgment | None |
| Rules are versioned, with a measure and a revert condition (protocol 3.7) | Part invariant | Rule files are append-only versions. The harness can flag a rule whose review date has passed |
| Audit against the swarm's own spec; report only what you can show (auditor) | Judgment | None |
| Hidden re-verification of a random sample of passed work (auditor B) | Part invariant | The harness draws the sample; the auditor does the verifying |

## The stop gate

The single most useful piece of enforcement, and the easiest to get wrong.

**What it does.** The agent's session cannot end while the run is unfinished. Each time it tries to stop, the harness checks a state file and sends it back to work if the file doesn't allow stopping.

**What opens it.** Any one of:

1. The done judge returned **met**, with evidence newer than the last change to the work.
2. The done judge returned **impossible** and the auditor confirmed it.
3. Every remaining path is blocked or parked, and the blocks are confirmed.
4. The budget or iteration cap is reached.
5. A human used the off switch.

**Who writes the state file.** The judge, the auditor and the harness. Never the worker.

Without exits 2 to 4 the gate becomes a pressure to fake success, which is the behaviour [ImpossibleBench](https://arxiv.org/abs/2510.20270) measures. Without the gate, "keep going until done" is only an instruction.

## Where the ideas came from

**oh-my-claudecode** is a working example of an enforcement layer for coding agents. Taken from it:

- a stop gate run by the harness, not remembered by the agent;
- evidence that must be fresh;
- review depth set by measurable triggers;
- a conductor that never does the work, with a delegation log;
- state saved before compaction, and notes that expire;
- atomic task claims and file ownership for parallel workers;
- one off switch.

Not taken: a gate with no documented cap and no "impossible" exit; a large roster of specialist agents; verification that assumes the work is code. It also has no step that changes the system after a failure and nothing that audits its verifier, which is what the learning layer here is for.

**Claude Code's /plan and /goal** supplied the separate done judge and the three verdicts, already adopted in the skills (see the README changelog). The difference kept here is that the judge runs the checks on the work itself, not on the conversation.

**An outside design review** (a critique of the project generated with ChatGPT) supplied the split between instruction and enforcement as a thing to test, and three ideas kept as candidates below.

## Proposals and their status

Untested, so not adopted (the project's practice is to test a change before adopting it):

- **Expiry on handoff notes** (protocol 2.1).
- **A four-arm test** of the layers on one long task: no skills and no enforcement; skills only; enforcement only; both. It answers the question the two A/B pilots could not: how much of any gain comes from the instructions and how much from the harness. In progress.

Tested on 2026-11-13 ([results](../results/2026-11-13-proposals-and-stop-gate)):

- **Proportional intervention**: a small gain on Haiku 5.5 (7.7 against 7.0 of 8). Candidate to adopt.
- **A computable floor for risk tiers**: worse than judgment (6.8 against 8.0 of 8); it over-rated a test-only task. Not adopted.
- **Marking records as fact, assumption, hypothesis or decision**: no difference; the existing "Unverified" field was enough. Not adopted.
- **The stop gate**: built and tested. No arm faked success on impossible tasks, even with a strict gate; a gate without exits cost 2.4 times as much, and honest exits recovered most of that.

## One concrete mapping: Claude Code

Given as an example. Any harness with the same capabilities would do.

| Mechanism | Claude Code feature |
| --- | --- |
| Stop gate | A Stop hook that reads the state file and blocks the stop |
| Protected paths, role write permissions | Permission rules, or a hook that runs before each file write |
| Tool allowlist per role | Subagent definitions with a restricted tool list |
| Measured spend, delegation log | A hook that runs after each subagent finishes and appends to the log |
| Save before compaction | A PreCompact hook |
| Isolated workspaces | Git worktrees, one per task |
| Budget and iteration caps | The run script's turn and budget limits, plus the counter the Stop hook reads |

One lesson from the per-skill tests belongs here. Test agents kept calling a scheduling tool they had been told not to use. The instruction did nothing; removing the tool would have. That is the whole argument for this layer in one example.
