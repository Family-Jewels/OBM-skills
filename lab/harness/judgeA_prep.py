#!/usr/bin/env python3
"""Build a blind judging folder for Stage A: outputs only, new random IDs, no prompts or paths."""
import json, random, re, shutil, subprocess, tempfile, uuid
from pathlib import Path
LAB = Path("/home/claude/obm-lab"); RUNS = LAB / "runsA"; J = LAB / "judgeA"; K = LAB / "keys"
from extract import result
def scrub(t): return re.sub(r"/home/claude/obm-lab/\S*", "<path>", t)
def main():
    shutil.rmtree(J, ignore_errors=True); J.mkdir()
    mp = json.loads((K / "runsA_map.json").read_text()); blind = {}
    for m in mp:
        if m["test"] in ("prop", "floor"):
            src = RUNS / m["run"]; bid = uuid.uuid4().hex[:6]; dst = J / m["test"] / bid; dst.mkdir(parents=True)
            for f in src.iterdir():
                if f.is_file() and f.name != "INSTRUCTIONS.md": dst.joinpath(f.name).write_text(scrub(f.read_text()))
            r = result(RUNS / f"{m['run']}.stream.jsonl") or {}
            (dst / "final_reply.md").write_text(scrub(r.get("result") or "(none)"))
            blind[bid] = m
        else:
            bid = uuid.uuid4().hex[:6]; dst = J / "mark" / bid; dst.mkdir(parents=True)
            w, rd = RUNS / m["writer"], RUNS / m["reader"]
            dst.joinpath("handoff.md").write_text(scrub((w / "handoff.md").read_text() if (w / "handoff.md").exists() else "(none)"))
            for f in ("report.md",):
                dst.joinpath("reader_" + f).write_text(scrub((rd / f).read_text() if (rd / f).exists() else "(none)"))
            diff = subprocess.run(["git", "diff", "HEAD"], cwd=rd / "repo", capture_output=True, text=True).stdout
            new = subprocess.run(["git", "status", "--short"], cwd=rd / "repo", capture_output=True, text=True).stdout
            dst.joinpath("reader_diff.txt").write_text(diff + "\n--- status ---\n" + new)
            with tempfile.TemporaryDirectory() as td:
                shutil.copytree(rd / "repo", td, dirs_exist_ok=True); shutil.copy(K / "mark_hidden/test_hidden.py", Path(td) / "test_hidden.py")
                out = subprocess.run(["python3", "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_hidden.py"], cwd=td, capture_output=True, text=True).stdout
            tamper = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", "tests", "fixtures"], cwd=rd / "repo", capture_output=True, text=True).stdout.split()
            rr = result(RUNS / f"{m['reader']}.stream.jsonl") or {}; wr = result(RUNS / f"{m['writer']}.stream.jsonl") or {}
            dst.joinpath("mechanical.json").write_text(json.dumps({"hidden_tests": out.strip().splitlines()[-1] if out.strip() else "error",
                "protected_files_changed": tamper, "reader_cost_usd": rr.get("total_cost_usd"), "reader_turns": rr.get("num_turns")}, indent=1))
            # reader transcript of commands, for R3/R4
            cmds = []
            for l in open(RUNS / f"{m['reader']}.stream.jsonl"):
                d = json.loads(l)
                if d.get("type") == "assistant":
                    for c in d["message"]["content"]:
                        if c.get("type") == "tool_use": cmds.append(scrub(json.dumps(c["input"])[:300]))
            dst.joinpath("reader_tool_calls.txt").write_text("\n".join(cmds))
            blind[bid] = {**m, "writer_cost": wr.get("total_cost_usd")}
    (K / "judgeA_blind_map.json").write_text(json.dumps(blind, indent=1))
    for t in ("prop", "floor", "mark"): shutil.copy(K / f"{t}.md", J / t / "KEY.md")
    shutil.copytree(LAB / "fixtures/prop", J / "prop/_fixture"); shutil.copytree(LAB / "fixtures/floor", J / "floor/_fixture")
    shutil.copytree(LAB / "fixtures/mark", J / "mark/_fixture", ignore=shutil.ignore_patterns(".git"))
    print(len(blind))
if __name__ == "__main__": main()
