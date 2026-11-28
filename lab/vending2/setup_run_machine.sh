#!/bin/bash
# Lay out a run machine the way run_arms2.py expects it, from this repo checkout. Idempotent: safe to run before every batch,
# and it refreshes the lab and skills copies so a run never uses stale code.
#   /home/claude/bench-src/vending-bench   Prosus Vending Bench v3.0.0, pinned to the commit the v4/v5 plan uses
#   /home/claude/vb-venv                   the simulator's Python (3.12, as in its Dockerfile)
#   /home/claude/obm-lab                   this repo's lab/, plus an empty cfg-clean/ (each run gets a fresh copy of it)
#   /home/claude/obm-skills/skills         this repo's skills/
# usage: lab/vending2/setup_run_machine.sh
set -euo pipefail
REPO=$(cd "$(dirname "$0")/../.." && pwd)
BENCH=/home/claude/bench-src/vending-bench
PIN=08c5a42a24bedf40fbabee03748ac77ad0e600df   # vending-bench HEAD on 2026-11-28; task.toml version 3.0.0

if [ ! -d "$BENCH/.git" ]; then
  mkdir -p "$(dirname "$BENCH")"
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/ProsusAI/vending-bench "$BENCH"
fi
if [ "$(git -C "$BENCH" rev-parse HEAD)" != "$PIN" ]; then
  git -C "$BENCH" fetch --depth 1 origin "$PIN" && git -C "$BENCH" checkout -q "$PIN"
fi
grep -q 'version = "3.0.0"' "$BENCH/tasks/vending-bench/task.toml" || { echo "vending-bench is not version 3.0.0" >&2; exit 1; }

PYV=$(command -v python3.12 || command -v python3)
[ -x /home/claude/vb-venv/bin/python ] || "$PYV" -m venv /home/claude/vb-venv
/home/claude/vb-venv/bin/pip install -q -r "$BENCH/tasks/vending-bench/environment/sim-server/requirements.txt"

mkdir -p /home/claude/obm-lab /home/claude/obm-skills
for d in "$REPO"/lab/*; do                      # refresh every lab folder; cfg-clean and run outputs are left alone
  rm -rf "/home/claude/obm-lab/$(basename "$d")"
  cp -a "$d" /home/claude/obm-lab/
done
mkdir -p /home/claude/obm-lab/cfg-clean
find /home/claude/obm-lab -name __pycache__ -prune -exec rm -rf {} +
rm -rf /home/claude/obm-skills/skills && cp -a "$REPO/skills" /home/claude/obm-skills/skills

/home/claude/vb-venv/bin/python -c "import fastmcp" 2>/dev/null
echo "run machine ready: vending-bench $(git -C "$BENCH" rev-parse --short HEAD), lab and skills from $(git -C "$REPO" rev-parse --short HEAD)"
