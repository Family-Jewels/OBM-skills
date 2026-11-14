# Mini SQL engine

Build an in-memory SQL engine in Python, in `engine.py`, using only the standard library. Importing `sqlite3` or any other database or SQL library is not allowed.

```python
from engine import Database
db = Database()
db.execute("CREATE TABLE t (id INTEGER, name TEXT)")   # returns []
db.execute("INSERT INTO t VALUES (1, 'a'), (2, NULL)") # returns []
db.execute("SELECT id FROM t WHERE name IS NULL")      # returns [(2,)]
```

`execute` takes one statement (no trailing semicolon needed) and returns a list of tuples for SELECT, and `[]` for anything else. Keywords are case-insensitive; identifiers are lowercase in the tests.

## Statements

- `CREATE TABLE name (col TYPE, ...)` with types INTEGER, TEXT, REAL.
- `INSERT INTO name VALUES (...), (...)` and `INSERT INTO name (col, ...) VALUES (...)`. Columns not listed are NULL.
- `UPDATE name SET col = expr, ... [WHERE cond]`
- `DELETE FROM name [WHERE cond]`
- `SELECT [DISTINCT] items FROM table [[INNER | LEFT] JOIN table ON cond] [WHERE cond] [GROUP BY exprs [HAVING cond]] [ORDER BY expr [ASC|DESC], ...] [LIMIT n [OFFSET m]]`. `JOIN` alone means INNER JOIN. Columns may be qualified (`t1.id`). At most one join per query.

## Values and expressions

- Values are INTEGER, REAL, TEXT or NULL. Literals: integers, decimals, single-quoted strings (`''` is an escaped quote), NULL.
- Unary minus (`-4`, `-a`). Arithmetic `+ - * / %`. If both operands are INTEGER the result is INTEGER, and `/` truncates toward zero: `7 / 2` is 3 and `-7 / 2` is -3. If either is REAL the result is REAL: `7 / 2.0` is 3.5. `%` truncates both operands to integers first, takes the sign of the left operand (`-7 % 3` is -1), and returns REAL if either operand was REAL. Division or `%` by zero gives NULL.
- `||` concatenates text.
- Comparison `= <> != < <= > >=`. Numbers compare numerically (INTEGER with REAL too). Text compares by Unicode code point, so `'B' < 'a'`. Comparisons give 1 or 0, or NULL if either side is NULL.
- `AND`, `OR`, `NOT` use three-valued logic: `NULL AND 0` is 0, `NULL OR 1` is 1, otherwise NULL propagates. A WHERE or HAVING condition keeps a row only when it is true (non-zero, not NULL).
- `x IS NULL`, `x IS NOT NULL` (always 1 or 0).
- `x [NOT] IN (v, ...)` and `x [NOT] IN (SELECT ...)`: true if equal to any value; otherwise NULL if the list holds a NULL or x is NULL, else false.
- `x [NOT] BETWEEN lo AND hi` means `x >= lo AND x <= hi`.
- `x [NOT] LIKE pattern`: `%` matches any run of characters, `_` exactly one; ASCII letters match case-insensitively.
- `CASE WHEN cond THEN v [WHEN ...] [ELSE v] END`; no ELSE means NULL.
- Scalar subquery `(SELECT ...)` returning one column: its first row's value, or NULL if it has no rows.
- Functions: `abs(x)`, `length(text)`, `upper(text)`, `lower(text)`, `coalesce(x, y, ...)` (first non-NULL). Any NULL argument gives NULL except in coalesce.

## Aggregates and grouping

- `COUNT(*)`, `COUNT(x)` (non-NULL values), `COUNT(DISTINCT x)`, `SUM(x)`, `AVG(x)`, `MIN(x)`, `MAX(x)`.
- SUM of INTEGER values is INTEGER; if any value is REAL it is REAL. AVG is always REAL. SUM, AVG, MIN and MAX ignore NULLs and return NULL when there are no non-NULL values; COUNT returns 0.
- MIN and MAX use the comparison rules above.
- Without GROUP BY, a query with aggregates returns exactly one row, even over no rows.
- With GROUP BY, one row per distinct group key (NULLs form one group). GROUP BY may use expressions, and select items may repeat them.

## Ordering and output

- Without ORDER BY, row order is not significant (tests compare as a multiset).
- ORDER BY sorts by each key in turn. NULL sorts before every other value in ascending order and after them in descending order. ORDER BY may use any expression over the row, including a select item's expression.
- `LIMIT n OFFSET m` applies after sorting.
- DISTINCT removes duplicate result rows (NULLs are equal to each other for this purpose).
- `LEFT JOIN`: rows of the left table with no match appear once, with NULL for every column of the right table.

## Tests

`tests/` holds the visible test cases (`tests/cases.jsonl`) and a runner: `python -m pytest tests -q`. Each case gives setup statements, a query and the expected rows. Numbers compare with a tolerance of 1e-9, and an INTEGER equals a REAL of the same value. Your engine is also graded on a larger hidden set of cases of the same kinds. Do not edit anything in `tests/`.
