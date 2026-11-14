import json, random, shutil, sys
from pathlib import Path
sys.path.insert(0, "/home/claude/obm-lab/slt"); import slt_runner as R
SRC = Path("/home/claude/slt-src/sqllogictest/test"); LAB = Path("/home/claude/obm-lab")
KIT = LAB / "sltkit/kit"; HID = LAB / "keys/slt_hidden"
def truncate(src, dst, n):
    lines = src.read_text(errors="replace").split("\n"); recs = R.parse(src)
    real = [r for r in recs if r["tok"][0] in ("statement", "query")]
    cut = len(lines) if len(real) <= n else real[n]["line"] - 1
    while cut > 0 and real and len(real) > n and lines[cut - 1].split() and lines[cut - 1].split()[0] in ("skipif", "onlyif"): cut -= 1
    dst.parent.mkdir(parents=True, exist_ok=True); dst.write_text("\n".join(lines[:cut]).rstrip() + "\n")
VIS = ["select1.test", "select2.test", "evidence/in1.test", "evidence/slt_lang_createview.test", "evidence/slt_lang_update.test",
       "evidence/slt_lang_replace.test", "evidence/slt_lang_droptable.test",
       "index/between/10/slt_good_0.test", "index/commute/10/slt_good_0.test", "index/delete/10/slt_good_0.test",
       "index/in/10/slt_good_0.test", "index/orderby/10/slt_good_0.test", "index/orderby_nosort/10/slt_good_0.test",
       "index/random/10/slt_good_0.test", "index/view/10/slt_good_1.test",
       "random/aggregates/slt_good_0.test", "random/expr/slt_good_0.test", "random/groupby/slt_good_0.test", "random/select/slt_good_0.test"]
rnd = random.Random(2026)
def pick(d, k, exclude):
    fs = sorted(p.relative_to(SRC).as_posix() for p in (SRC / d).glob("*.test")); fs = [f for f in fs if f not in exclude]
    return rnd.sample(fs, min(k, len(fs)))
HIDDEN = ["select3.test", "select4.test", "select5.test", "evidence/in2.test", "evidence/slt_lang_dropview.test",
          "evidence/slt_lang_dropindex.test", "evidence/slt_lang_reindex.test", "evidence/slt_lang_createtrigger.test", "evidence/slt_lang_droptrigger.test"]
for fam in ["between", "commute", "delete", "in", "orderby", "orderby_nosort", "random", "view"]:
    HIDDEN += pick(f"index/{fam}/10", 2, VIS) + pick(f"index/{fam}/100", 1, VIS)
for fam in ["aggregates", "expr", "groupby", "select"]:
    HIDDEN += pick(f"random/{fam}", 3, VIS)
shutil.rmtree(KIT, ignore_errors=True); shutil.rmtree(HID, ignore_errors=True)
for f in VIS: truncate(SRC / f, KIT / "tests/slt" / f, 400)
for f in HIDDEN: truncate(SRC / f, HID / f, 1000)
p = KIT / "tests/slt/evidence/in1.test"; t = p.read_text()
old = "query I nosort\nSELECT 1 IN (2)\n----\n0\n"; assert t.count(old) == 1; p.write_text(t.replace(old, "query I nosort\nSELECT 1 IN (2)\n----\n1\n"))
shutil.copy(LAB / "slt/slt_runner.py", KIT / "tests/slt_runner.py")
json.dump({"visible": VIS, "hidden": HIDDEN}, open(LAB / "keys/slt_split.json", "w"), indent=1)
print(len(VIS), "visible;", len(HIDDEN), "hidden")
