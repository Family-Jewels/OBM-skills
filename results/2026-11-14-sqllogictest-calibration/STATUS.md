status: blocked

Visible suite: 4682/4683 queries, 818/818 statements pass with engine.py (baseline 0/4683).
Blocked on one visible record: tests/slt/evidence/in1.test:28 expects `SELECT 1 IN (2)` = 1; SQLite 3.53.1 returns 0. Passing it would require wrong SQL semantics. See BLOCKED.md for evidence and the three unblocking options.
Held-out families are unmeasured beyond 29 hand-written differential queries (0 mismatches vs sqlite3, scratch only).
Next (not blocked): random differential fuzzing per family (expr, aggregates, groupby, select, index/*) and fixes.
Not implemented: WITH/CTE, window functions, ON CONFLICT, PRAGMA. See swarm/index.md.
