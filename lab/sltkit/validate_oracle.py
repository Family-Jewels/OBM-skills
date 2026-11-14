import sqlite3, sys, signal, time, json
sys.path.insert(0, "/home/claude/obm-lab/slt")
import slt_runner as R
class Database:
    def __init__(self): self.c = sqlite3.connect(":memory:", isolation_level=None)
    def execute(self, sql): return self.c.execute(sql).fetchall()
signal.signal(signal.SIGALRM, R._alarm)
tot = [0, 0, 0, 0]
for f in sys.argv[1:]:
    t = time.time(); o = R.run_file(f, Database, None, 30)
    tot[0] += o["passed"]; tot[1] += o["queries"]; tot[2] += o["statements_ok"]; tot[3] += o["statements"]
    print(f"{o['passed']}/{o['queries']} q, {o['statements_ok']}/{o['statements']} st, {time.time()-t:.1f}s  {f}  {o['failures'][:3]}")
print("TOTAL", tot)
