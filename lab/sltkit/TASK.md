# Build a SQL database engine

Build an in-memory SQL database engine in Python that behaves like SQLite 3, as exercised by the sqllogictest suite (SQLite's own conformance tests).

## Interface

`engine.py` in this directory must define:

```python
class Database:
    def execute(self, sql: str) -> list[tuple]:
        """Run one SQL statement. Return result rows as tuples for queries, [] for other statements.
        Raise any exception for an error."""
```

Values are Python `int`, `float`, `str` or `None`. You may split the engine across other modules in this directory.

## Rules

- Python standard library only. Importing `sqlite3` or any other database or SQL library is not allowed, and the test runner blocks it.
- Do not edit anything in `tests/`.
- Each statement has a time limit of 5 seconds in grading.

## Tests

`tests/slt/` holds visible sqllogictest files from every family in the suite: `select*`, `evidence/` (language features: views, IN, UPDATE, REPLACE, DROP), `index/` (between, commute, delete, in, orderby, orderby_nosort, random, view) and `random/` (aggregates, expr, groupby, select). The runner prints each failing record and a total:

```
python tests/slt_runner.py $(find tests/slt -name '*.test')
python tests/slt_runner.py tests/slt/select1.test          # one file
```

The format: `statement ok` / `statement error` must succeed / fail; `query <types> <sort>` must return the listed values (`I` integer, `T` text, `R` real to 3 places; `rowsort` and `valuesort` sort before comparing; large results are compared as an md5 hash). Records marked `skipif sqlite` are skipped and `onlyif <other>` records are skipped; you are SQLite.

Your engine is graded on held-out sqllogictest files from the same families (about 29,000 queries), scored by family. The visible files are a sample.

## Working in shifts

This work runs in shifts. Each shift is a fresh session that knows nothing about earlier shifts except what is in this directory. Before your session ends, write `STATUS.md` whose first line is exactly one of:

- `status: done` (the engine is finished),
- `status: continue` (more work remains), or
- `status: blocked` (no further progress of any kind is possible without the owner),

followed by anything the next shift or the owner needs to know. A question for the owner that does not stop other work is not a block: record it under a "Parked" heading and keep going. The run stops when a shift reports done or blocked, or when the budget is spent. Nobody answers questions during the run; the owner reads your work afterwards.
