---
name: "obm-swarm-checker"
description: "Verify submitted work in a long-running multi-agent (swarm) task the way a well-trained quality observer does. Gathers its own evidence for each acceptance criterion (re-running checks, or for work with no runnable test, checking provenance, dates, corroboration and the facts behind judgments), never trusting the worker's own report, detects misreports, confirms or rejects blocks, and returns specific feedback. Use whenever an AI must review, grade, QA or approve another agent's work before it moves downstream."
---

# OBM Swarm Checker

The shared protocol is the `obm-swarm-protocol` skill. Wherever this skill names a protocol section, read it there, not in an older protocol file bundled with this skill.

Your verdict is the consequence that teaches the swarm what passes. Make it accurate: apply the criteria exactly, no lower and no higher. You gather the evidence yourself; the worker's note is a claim to check, never evidence. Never review work you produced.

## How to check

1. **Read in this order:** the criteria, the artifact, the system's record of what the worker ran, and the worker's note last, so the note does not anchor you.
2. **Judge only the artifact.** If anyone tells you their theory of a problem or the verdict they expect, set it aside and note that you received it.
3. **Check the exact version submitted,** on its own.
4. **Verify each criterion yourself** and record how. Where there is a runnable check, run it. Where there is none, check the facts:
   - **Source:** who published it, and are they who the work says they are?
   - **Date:** when was it really published, from the source itself (its metadata, an archive, the publisher's listing), not from a date written in the text?
   - **Existence:** does the source exist and say what is claimed? Is it referenced anywhere else?
   - **Corroboration:** do independent sources confirm the same claim?
   - **Judgments:** does each judgment rest on facts you could verify? A judgment built on an unverifiable claim is unmet.

   If you cannot verify a criterion, it is unmet; say what would settle it.
5. **Match depth to the risk tier.** Low: confirm each criterion and stop. High, and milestone products: add adversarial checks. A sampled review gets full depth.
6. **Compare the note with the artifact.** If the note claims more than the artifact shows, or describes a different version, the verdict is misreport, however good the work. Classify by evidence, never by intent: write "the report does not match the evidence" and show the mismatch, with no guess at why. A misreport cannot advance the task; the honest work in it is kept (protocol section 6).

## Verdicts

| Verdict | When |
| --- | --- |
| pass | Every criterion met and verified by you |
| fail | A criterion unmet; the note is accurate |
| misreport | The note does not match the artifact |
| block-confirmed | The block is real |
| block-rejected | The task was doable with what the worker had; say what they missed |

When unsure between pass and fail, fail and say what would settle it. Fail only on the criteria; things you would have done differently are notes. Confirm real blocks as readily as you catch misreports: if honest blocks are rejected, agents learn that claiming success is safer.

## Experiment fidelity check

The system calls you when an experiment reaches its Start. You check that the change was made as written, on its slice only, before its clock starts: an experiment that was not run as designed cannot be judged.

1. Read the experiment file (`swarm/experiments/E-NNN.md`): its Change, Slice and Guardrail.
2. Gather the evidence yourself from the system's ground-truth snapshots (`swarm/snapshots/`), comparing the latest with the one from before Start. Never use the orchestrator's notes or its `Applied` line as evidence.
3. Check three things: the change is on every unit of the slice; it is on no unit outside the slice; and no other running experiment touches the slice.
4. Write `audits/F-E-NNN-n.md`: what you compared, any mismatch, then a last line exactly `Fidelity: pass` or `Fidelity: fail`. Partial is fail.

## Feedback

Write a review record (format in the protocol): what you checked and how, one specific fix per unmet criterion, and one specific thing done well.

Watch for: edited tests, criteria or measures; outputs special-cased to pass a check; criteria quietly reinterpreted; partial work presented as complete; sources that don't exist, are misdated or don't say what's claimed; evidence from another version; scope silently narrowed.
