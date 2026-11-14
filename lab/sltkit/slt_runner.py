#!/usr/bin/env python3
"""sqllogictest runner for a Python engine.

The engine is a module `engine` exposing `Database()` with `execute(sql) -> list of tuples` (rows; [] for statements).
Errors are signalled by raising any exception. Follows sqllogictest.c / slt_sqlite.c: we are database "sqlite".

usage: python slt_runner.py [--engine-dir DIR] [--max-records N] [--timeout S] [--json OUT] FILE...
Prints one line per failing record: "FAILED <file>:<line>" and a summary.
"""
import argparse, hashlib, importlib, json, math, re, signal, sys, time
from pathlib import Path

class Timeout(Exception): pass
def _alarm(*a): raise Timeout()

def fmt(v, t):
    if v is None: return "NULL"
    if t == "T":
        if isinstance(v, float):
            s = "%.15g" % v
            if re.fullmatch(r"-?\d+", s): s += ".0"
        else:
            s = str(v)
        if s == "": return "(empty)"
        return "".join(c if " " <= c <= "~" else "@" for c in s)
    if t == "I":
        if isinstance(v, bool): return str(int(v))
        if isinstance(v, int): return str(v)
        if isinstance(v, float): return str(int(v)) if math.isfinite(v) else "0"
        m = re.match(r"\s*[-+]?\d+", str(v)); return str(int(m.group(0))) if m else "0"
    if t == "R":
        if isinstance(v, (int, float)): return "%.3f" % v
        m = re.match(r"\s*[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?", str(v)); return "%.3f" % (float(m.group(0)) if m else 0.0)
    raise ValueError("bad type " + t)

def parse(path):
    lines = Path(path).read_text(errors="replace").split("\n"); i = 0; recs = []
    while i < len(lines):
        if not lines[i].strip() or lines[i].startswith("#"): i += 1; continue
        start = i + 1; conds = []
        while lines[i].split()[0] in ("skipif", "onlyif"):
            conds.append(lines[i].split()[:2]); i += 1
        tok = lines[i].split(); i += 1
        body = []
        while i < len(lines) and lines[i].strip() and lines[i] != "----":
            body.append(lines[i]); i += 1
        exp = None
        if i < len(lines) and lines[i] == "----":
            i += 1; exp = []
            while i < len(lines) and lines[i].strip():
                exp.append(lines[i]); i += 1
        recs.append({"line": start, "conds": conds, "tok": tok, "sql": "\n".join(body), "exp": exp})
    return recs

def skipped(conds):
    for kind, db in conds:
        m = db.lower() == "sqlite"
        if (kind == "skipif" and m) or (kind == "onlyif" and not m): return True
    return False

def run_file(path, Database, max_records=None, timeout=5.0, deadline=None):
    out = {"file": str(path), "queries": 0, "passed": 0, "statements": 0, "statements_ok": 0, "failures": []}
    try:
        db = Database()
    except Exception as e:
        out["failures"].append((0, "Database() failed: " + repr(e)[:200])); return out
    labels = {}; n = 0
    for r in parse(path):
        if r["tok"][0] == "halt" and not skipped(r["conds"]): break
        if r["tok"][0] == "hash-threshold" or skipped(r["conds"]): continue
        if r["tok"][0] not in ("statement", "query"): continue
        n += 1
        if max_records and n > max_records: break
        if deadline and time.time() > deadline:
            out["failures"].append((r["line"], "file time limit")); break
        signal.setitimer(signal.ITIMER_REAL, timeout)
        err = res = None
        try:
            res = db.execute(r["sql"])
        except Timeout:
            err = "timeout"
        except BaseException as e:
            err = repr(e)[:200]
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
        if r["tok"][0] == "statement":
            out["statements"] += 1
            want_err = r["tok"][1] == "error"
            if (err is not None) == want_err: out["statements_ok"] += 1
            else: out["failures"].append((r["line"], f"statement {'should fail' if want_err else 'failed: ' + str(err)}"))
            continue
        out["queries"] += 1
        types, sortm = r["tok"][1], (r["tok"][2] if len(r["tok"]) > 2 else "nosort")
        label = r["tok"][3] if len(r["tok"]) > 3 else None
        if err is not None:
            out["failures"].append((r["line"], "query error: " + str(err))); continue
        try:
            rows = [tuple(x) for x in (res or [])]
            if any(len(x) != len(types) for x in rows): raise ValueError(f"wrong column count: want {len(types)}")
            vals = [[fmt(v, types[j]) for j, v in enumerate(x)] for x in rows]
        except Exception as e:
            out["failures"].append((r["line"], "bad result: " + repr(e)[:150])); continue
        if sortm == "rowsort": vals.sort()
        flat = [v for x in vals for v in x]
        if sortm == "valuesort": flat.sort()
        h = hashlib.md5("".join(v + "\n" for v in flat).encode()).hexdigest()
        exp = r["exp"] or []
        m = re.match(r"(\d+) values hashing to ([0-9a-f]{32})", exp[0]) if exp else None
        if m: ok = int(m.group(1)) == len(flat) and m.group(2) == h
        elif exp: ok = [e.strip() for e in exp] == flat
        elif label and label in labels: ok = labels[label] == h
        else: ok = len(flat) == 0
        if label and ok: labels.setdefault(label, h)
        if ok: out["passed"] += 1
        else: out["failures"].append((r["line"], "wrong result"))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+"); ap.add_argument("--engine-dir", default=".")
    ap.add_argument("--max-records", type=int, default=None); ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--file-time", type=float, default=600.0); ap.add_argument("--json", default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    sys.modules["sqlite3"] = None; sys.modules["_sqlite3"] = None
    sys.path.insert(0, str(Path(a.engine_dir).resolve()))
    signal.signal(signal.SIGALRM, _alarm)
    Database = importlib.import_module("engine").Database
    tot = {"queries": 0, "passed": 0, "statements": 0, "statements_ok": 0}; results = []
    for f in a.files:
        o = run_file(f, Database, a.max_records, a.timeout, time.time() + a.file_time); results.append(o)
        for k in tot: tot[k] += o[k]
        if not a.quiet:
            for line, why in o["failures"]: print(f"FAILED {f}:{line} {why}")
    if a.json: Path(a.json).write_text(json.dumps({"total": tot, "files": results}))
    q = tot["queries"]
    print(f"{tot['passed']}/{q} queries passed, {tot['statements_ok']}/{tot['statements']} statements ok")
    sys.exit(0 if tot["passed"] == q and tot["statements_ok"] == tot["statements"] else 1)

if __name__ == "__main__":
    main()
