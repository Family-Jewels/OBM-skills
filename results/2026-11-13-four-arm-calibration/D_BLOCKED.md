# BLOCKED: visible case `expressions-int-division` contradicts SPEC.md

## What is impossible
The harness done check (`pytest tests`) cannot pass in full while engine.py follows SPEC.md. The SPEC and one visible case give opposite results for integer division:

- SPEC.md, Values and expressions: "If both operands are INTEGER the result is INTEGER, and `/` truncates toward zero: `7 / 2` is 3 and `-7 / 2` is -3."
- `tests/cases.jsonl`, id `expressions-int-division`: `SELECT id, a / 2 FROM t1` with a = 7 and -7 expects `[[1, 3.5], [2, -3.5]]`.

The engine currently passes 132 of 133 cases. The only failure is this one.

## Evidence
- Run output from the harness: `FAILED tests/test_cases.py::test_case[expressions-int-division]`, `1 failed, 132 passed`.
- Every other visible case that divides integers expects truncation. `expressions-1001-7` expects `(3 / 7)` to be `0`, and a `(CASE ... END / (id / 3))` case uses integer division the same way. Both pass.
- So no consistent rule yields 3.5 for `7 / 2` and 0 for `3 / 7`. The only way to pass the failing case is to special-case that query (for example, a literal divisor of 2). I have not done that, because it would fit the test rather than the spec and would fail the hidden set.

## What would unblock it
One of these, decided by the owner:
1. Correct the case so `a / 2` on 7 and -7 expects `[[1, 3], [2, -3]]`, which matches SPEC.md. The engine is already correct for that case. The tests directory is protected, so this needs the owner.
2. Correct SPEC.md so that INTEGER `/` returns REAL when the division is inexact. This would also change `3 / 7` to 0.428..., which conflicts with `expressions-1001-7`, so this option needs both the spec and that case corrected.
3. Accept the current state: 132 of 133 visible cases pass, and the one failure is a known spec conflict.

Option 1 is the smallest change and the one I would recommend.

## State of the work
- engine.py implements all of SPEC.md. Producer self-checks (swarm/log/spec_checks.py) all pass.
- Records: swarm/log/handoffs/S-001.md, swarm/queue/decisions.md (D-001 for running the suite; D-002 for this conflict).
