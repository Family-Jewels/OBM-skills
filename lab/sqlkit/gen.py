#!/usr/bin/env python3
"""Generate SQL test cases with SQLite as the oracle.

Each case: {"id", "category", "setup": [sql...], "query": sql, "ordered": bool, "expected": [[...], ...]}
Expected rows come from Python's sqlite3. Values are restricted so the spec's semantics equal SQLite's.
usage: gen.py <seed> <n_per_category> <out.jsonl>
"""
import json, random, sqlite3, sys

def rows_t1(r):
    out = []
    for i in range(1, r.randint(14, 22) + 1):
        a = r.choice([None] + list(range(-5, 30)))
        b = r.choice([None, "apple", "Banana", "cherry", "date", "Elder", "fig", "grape", "kiwi", "lemon", "Mango", "apple pie", "berry", ""])
        c = r.choice([None, round(r.uniform(-50, 200), 2), float(r.randint(0, 9)), 0.5, 2.25])
        g = r.choice(["n", "s", "e", "w"])
        out.append((i, a, b, c, g))
    return out

def rows_t2(r):
    out = []
    for i in range(1, r.randint(10, 16) + 1):
        out.append((i, r.choice([None] + list(range(1, 25))), r.choice(["red", "blue", "green", None, "Blue"]), r.randint(-3, 12)))
    return out

def lit(v):
    if v is None: return "NULL"
    if isinstance(v, str): return "'" + v.replace("'", "''") + "'"
    return repr(v)

def setup_sql(r):
    t1, t2 = rows_t1(r), rows_t2(r)
    s = ["CREATE TABLE t1 (id INTEGER, a INTEGER, b TEXT, c REAL, g TEXT)",
         "CREATE TABLE t2 (id INTEGER, t1_id INTEGER, color TEXT, qty INTEGER)"]
    s.append("INSERT INTO t1 VALUES " + ", ".join("(" + ", ".join(lit(v) for v in row) + ")" for row in t1))
    s.append("INSERT INTO t2 VALUES " + ", ".join("(" + ", ".join(lit(v) for v in row) + ")" for row in t2))
    return s

COLS1 = ["a", "b", "c", "g"]
def pred(r, depth=0):
    kind = r.choice(["cmp", "cmp", "null", "in", "between", "like", "bool"] if depth < 2 else ["cmp", "null"])
    if kind == "cmp":
        col = r.choice(["a", "c", "b"])
        op = r.choice(["=", "<>", "<", "<=", ">", ">=", "!="])
        v = r.randint(-5, 30) if col == "a" else (round(r.uniform(-20, 150), 1) if col == "c" else r.choice(["apple", "cherry", "fig", "Mango", "kiwi"]))
        return f"{col} {op} {lit(v)}"
    if kind == "null": return f"{r.choice(COLS1)} IS {r.choice(['', 'NOT '])}NULL"
    if kind == "in": return f"a {r.choice(['', 'NOT '])}IN ({', '.join(str(r.randint(-5, 30)) for _ in range(r.randint(1, 4)))})"
    if kind == "between":
        lo = r.randint(-5, 15); return f"a {r.choice(['', 'NOT '])}BETWEEN {lo} AND {lo + r.randint(0, 15)}"
    if kind == "like": return f"b {r.choice(['', 'NOT '])}LIKE {lit(r.choice(['a%', '%e', '%an%', '_i%', 'APPLE%', '%', 'm_ngo']))}"
    return f"({pred(r, depth + 1)} {r.choice(['AND', 'OR'])} {'NOT ' if r.random() < 0.2 else ''}{pred(r, depth + 1)})"

def num(r, depth=0):
    k = r.choice(["arith", "arith", "func", "case", "col", "lit"] if depth < 2 else ["col", "lit"])
    if k == "col": return r.choice(["a", "c", "id"])
    if k == "lit": return str(r.choice([0, 1, 2, 3, 7, -4, 2.5, 10]))
    if k == "arith": return f"({num(r, depth + 1)} {r.choice(['+', '-', '*', '/', '%'])} {num(r, depth + 1)})"
    if k == "func": return r.choice(["abs(a)", "length(b)", "coalesce(a, 0)", "abs(c)", "coalesce(c, a, -1)"])
    return f"CASE WHEN {pred(r, 2)} THEN {num(r, 2)} ELSE {r.choice(['0', 'c', 'NULL'])} END"

def text(r):
    return r.choice(["(b || '-x')", "upper(b)", "lower(b)", "coalesce(b, 'none')", "(g || b)", "CASE WHEN a > 10 THEN 'big' WHEN a IS NULL THEN 'none' ELSE 'small' END"])

def expr(r, depth=0):
    return num(r) if r.random() < 0.7 else text(r)

def q_select(r):
    cols = ", ".join(r.sample(["id", "a", "b", "c", "g"], r.randint(1, 4)))
    return f"SELECT {cols} FROM t1 WHERE {pred(r)}", False

def q_expr(r):
    return f"SELECT id, {expr(r)}, {expr(r)} FROM t1", False

def q_null(r):
    return r.choice([
        f"SELECT id FROM t1 WHERE NOT ({pred(r, 1)})",
        f"SELECT id, a = {r.randint(0, 9)}, a IS NULL, coalesce(a, c, 0) FROM t1",
        f"SELECT id, a + c, a > c, b || 'z' FROM t1 WHERE id <= {r.randint(5, 20)}",
        f"SELECT id FROM t1 WHERE a IN ({r.randint(0, 9)}, NULL)",
        f"SELECT id FROM t1 WHERE a NOT IN ({r.randint(0, 9)}, NULL)"]), False

def q_order(r):
    keys = r.sample(["a", "b", "c", "g"], r.randint(1, 3))
    ob = ", ".join(f"{k} {r.choice(['ASC', 'DESC', ''])}".strip() for k in keys) + ", id"
    lim = r.choice(["", f" LIMIT {r.randint(0, 8)}", f" LIMIT {r.randint(1, 6)} OFFSET {r.randint(0, 6)}"])
    return f"SELECT id, {', '.join(keys)} FROM t1 ORDER BY {ob}{lim}", True

def q_agg(r):
    aggs = r.sample(["COUNT(*)", "COUNT(a)", "COUNT(b)", "SUM(a)", "SUM(c)", "AVG(a)", "MIN(a)", "MAX(a)", "MIN(b)", "MAX(c)", "COUNT(DISTINCT g)", "SUM(qty)"[:0] or "AVG(c)"], r.randint(1, 4))
    w = f" WHERE {pred(r)}" if r.random() < 0.6 else ""
    return f"SELECT {', '.join(aggs)} FROM t1{w}", False

def q_group(r):
    aggs = ", ".join(r.sample(["COUNT(*)", "SUM(a)", "AVG(c)", "MIN(b)", "MAX(a)", "COUNT(c)"], r.randint(1, 3)))
    hv = r.choice(["", " HAVING COUNT(*) > 1", f" HAVING SUM(a) > {r.randint(0, 40)}", " HAVING MAX(a) IS NOT NULL"])
    key = r.choice(["g", "a % 3", "b IS NULL", "g, a > 10"])
    order = r.random() < 0.5
    sql = f"SELECT {key}, {aggs} FROM t1 GROUP BY {key}{hv}"
    if order: sql += f" ORDER BY {key.split(',')[0]}"
    return sql, False  # grouped order compared as multiset unless ORDER BY fully determines it

def q_distinct(r):
    cols = ", ".join(r.sample(["g", "a % 4", "b IS NULL", "upper(substr(b, 1, 1))"[:0] or "length(b)"], r.randint(1, 2)))
    return f"SELECT DISTINCT {cols} FROM t1", False

def q_join(r):
    jt = r.choice(["JOIN", "INNER JOIN", "LEFT JOIN"])
    cols = r.choice(["t1.id, t2.id", "t1.id, t2.color, t2.qty", "t1.b, t2.qty", "t1.id, t2.id, t1.a + t2.qty"])
    w = r.choice(["", f" WHERE t2.qty > {r.randint(0, 8)}", " WHERE t2.color IS NULL", f" WHERE t1.a < {r.randint(0, 20)}"])
    on = r.choice(["t1.id = t2.t1_id", "t1.a = t2.qty", "t1.id = t2.t1_id AND t2.qty > 2"])
    return f"SELECT {cols} FROM t1 {jt} t2 ON {on}{w}", False

def q_joinagg(r):
    return r.choice([
        "SELECT t1.g, COUNT(t2.id), SUM(t2.qty) FROM t1 LEFT JOIN t2 ON t1.id = t2.t1_id GROUP BY t1.g",
        f"SELECT t2.color, COUNT(*) FROM t1 JOIN t2 ON t1.id = t2.t1_id WHERE t1.a > {r.randint(-5, 10)} GROUP BY t2.color",
        "SELECT t1.id, COUNT(t2.id) FROM t1 LEFT JOIN t2 ON t1.id = t2.t1_id GROUP BY t1.id HAVING COUNT(t2.id) >= 1"]), False

def q_sub(r):
    return r.choice([
        f"SELECT id FROM t1 WHERE id IN (SELECT t1_id FROM t2 WHERE qty > {r.randint(0, 10)})",
        f"SELECT id FROM t1 WHERE id NOT IN (SELECT t1_id FROM t2 WHERE t1_id IS NOT NULL AND qty < {r.randint(0, 10)})",
        "SELECT id, a FROM t1 WHERE a > (SELECT AVG(a) FROM t1)",
        "SELECT id FROM t1 WHERE c = (SELECT MAX(c) FROM t1)",
        f"SELECT COUNT(*) FROM t1 WHERE a < (SELECT MIN(qty) FROM t2 WHERE qty > {r.randint(0, 5)})"]), False

def q_dml(r):
    stmts = r.choice([
        [f"UPDATE t1 SET a = a + {r.randint(1, 5)} WHERE {pred(r)}"],
        [f"DELETE FROM t1 WHERE {pred(r)}"],
        [f"UPDATE t1 SET b = 'zz', c = NULL WHERE a > {r.randint(0, 20)}", f"DELETE FROM t2 WHERE qty < {r.randint(0, 6)}"],
        [f"INSERT INTO t1 (id, a, g) VALUES (100, {r.randint(-5, 20)}, 'x'), (101, NULL, 'x')"]])
    return stmts, "SELECT id, a, b, c, g FROM t1 ORDER BY id", True

CATS = {"select_where": q_select, "expressions": q_expr, "null_logic": q_null, "order_limit": q_order, "aggregates": q_agg,
        "group_by": q_group, "distinct": q_distinct, "joins": q_join, "join_aggregates": q_joinagg, "subqueries": q_sub}

def norm(v):
    return v

def make(seed, n, out):
    r = random.Random(seed); cases = []
    for cat in list(CATS) + ["dml"]:
        k = 0
        while k < n:
            setup = setup_sql(r)
            if cat == "dml":
                extra, q, ordered = q_dml(r); setup = setup + extra
            else:
                q, ordered = CATS[cat](r)
            con = sqlite3.connect(":memory:")
            try:
                for s in setup: con.execute(s)
                rows = [list(x) for x in con.execute(q).fetchall()]
            except sqlite3.Error:
                continue
            cases.append({"id": f"{cat}-{seed}-{k}", "category": cat, "setup": setup, "query": q, "ordered": ordered, "expected": rows})
            k += 1
    with open(out, "w") as f:
        for c in cases: f.write(json.dumps(c) + "\n")
    print(len(cases), "cases ->", out)

if __name__ == "__main__":
    make(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
