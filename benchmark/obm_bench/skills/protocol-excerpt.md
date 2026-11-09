# OBM Swarm Protocol (excerpt used in this benchmark)

### 3.3 Evidence block (attached to every submission)

```
Task: T-0042
Claim per criterion:
  1. <criterion> : <met / not met> : <evidence: test output, diff, source, artifact path> : <how to verify in one step>
  2. ...
Known gaps: <anything incomplete, uncertain or assumed>
Constraint breaks: <none, or what happened>
```

A claim with no evidence is treated as not met.

### 3.4 Review record

```
Task: T-0042  Reviewer: checker  Mode: full
Verdict: pass | fail | misreport | block-confirmed | block-rejected
Criteria:
  1. <criterion> : met/unmet : <what was checked> : <how>
Correspondence: report matches artifact? yes/no (details)
Feedback: <one specific, criterion-referenced fix per unmet criterion>
Done well: <one specific thing, for the worked-example pool>
```

### 3.5 Blocked report (a valid outcome, not a failure)

```
Task: T-0042
Type: missing information | missing resource | ambiguous criteria | impossible as specified | budget exhausted
Tried: <what was attempted>
Smallest unblocking step: <the one thing that would let work resume>
Proposed narrower task: <a subproblem that can pass on its own>
```

## 5. Consequence map

Consequences must be immediate, certain and identical every time. Inconsistent consequences are the fastest way to teach a swarm the wrong lesson (Daniels: consequences that are immediate and certain control behavior; delayed or uncertain ones barely do).

| Outcome | Consequence |
| --- | --- |
| Passed | Moves downstream at once. Counts toward the producer's pass streak. Strong examples are promoted to `examples/`. |
| Failed | Returned once with specific feedback. At the retry cap, escalated (split, narrow or replan), never retried a third time unchanged. |
| Blocked (confirmed) | Counted as a valid outcome. Routed to split, reassign, park or diagnose. Never penalized. |
| Misreport | The costliest outcome. Task reset, producer returns to full review, diagnostician opens a rule review. |
| Constraint break | Output quarantined and never passes, however good. Logged as data about the environment. |
| Honest report of one's own constraint break | Output still quarantined, but no further consequence. Concealment is the outcome to make impossible, not admission. |

Rewarding A while hoping for B (Kerr, 1975) is the failure this table exists to prevent. If a misreport or a rule-break can ever pass, the swarm is being trained to misreport and break rules.
