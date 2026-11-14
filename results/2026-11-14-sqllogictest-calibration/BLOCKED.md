# BLOCKED: the visible suite cannot fully pass without wrong SQL semantics

## What is impossible
The stop-hook done check requires every record in tests/ to pass. One record cannot pass by a correct engine:

- File: tests/slt/evidence/in1.test, record at line 28 (`query I nosort`)
- Statement: `SELECT 1 IN (2)`
- Expected in file: `1`
- Correct SQLite result: `0`

## Evidence
- Python sqlite3 (SQLite 3.53.1) in a scratch check: `SELECT 1 IN (2)` -> `[(0,)]`.
- Runner: `python tests/slt_runner.py tests/slt/evidence/in1.test` -> `FAILED tests/slt/evidence/in1.test:28 wrong result`, `186/187 queries passed, 27/27 statements ok`.
- The rest of the visible suite: 4682/4683 queries, 818/818 statements.
- Only way to pass this record is to make `1 IN (2)` return 1, which is false in SQLite. The engine would then disagree with the graded reference on held-out files.
- tests/ is protected by the harness (producers may not edit it), so the expectation cannot be corrected from here.

## What would unblock it
Owner to do one of:
1. Correct the expectation at tests/slt/evidence/in1.test:31 from `1` to `0` (matches SQLite 3.53.1), or
2. Mark this record as known-bad in the runner (skip with a stated reason), or
3. Confirm that the done check should exclude this record.

Once one of these is done, the remaining work is held-out hardening (fuzzing per family), which is not blocked.
