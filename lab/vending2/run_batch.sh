#!/bin/bash
# Drives the v4/v5 plan with no one watching: the smoke stage, then, only if every smoke check passes, the seed stage.
# Each tick of seed_batch.py files what finished and starts the next run (one at a time); this loop waits for that run,
# then ticks again. Each run starts only when the usage window refreshes: until then the loop exits, writing the time to
# /home/claude/runs/next_start, and a scheduled task the session sets for that time starts it again. Every filed run is committed and pushed at once,
# because the container is ephemeral. Starting it twice is harmless: the second copy exits.
#   usage: setsid nohup lab/vending2/run_batch.sh >/dev/null 2>&1 &      log: /home/claude/runs/batch.log
REPO=$(cd "$(dirname "$0")/../.." && pwd); cd "$REPO" || exit 1
B=results/2026-11-28-vending-v4-v5; LOG=/home/claude/runs/batch.log; PIDF=/home/claude/runs/batch.pid
BRANCH=claude/blissful-keller-ldige3
mkdir -p /home/claude/runs
if [ -f "$PIDF" ] && kill -0 "$(cat "$PIDF")" 2>/dev/null; then echo "$(date -u +%FT%TZ) already running" >> "$LOG"; exit 0; fi
echo $$ > "$PIDF"
say() { echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }
alive() { local s; s=$(ps -o stat= -p "$1" 2>/dev/null); [ -n "$s" ] && [ "${s:0:1}" != "Z" ]; }
push() {  # commit and push whatever was filed
  git add "$B" 2>/dev/null
  git diff --cached --quiet && return 0
  git commit -q -m "Vending v4/v5 batch: $1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01LAiU7vYJef3zv522k7gEpP" || return 0
  for i in 1 2 3 4; do
    git push -q origin "$BRANCH" && { say "pushed: $1"; return 0; }
    git fetch -q origin "$BRANCH" && git merge -q --no-edit FETCH_HEAD; sleep $((2 ** i))
  done
  say "push failed (kept locally): $1"
}
stage() {  # run one stage of seed_batch to completion; its settings come in as VAR=value arguments
  while true; do
    out=$(env "$@" python3 -I lab/vending2/seed_batch.py tick 2>>"$LOG")
    say "tick: $out"
    act=$(python3 -I -c 'import json,sys; print(json.loads(sys.argv[1]).get("action",""))' "$out" 2>/dev/null)
    push "$(python3 -I -c 'import json,sys; d=json.loads(sys.argv[1]); print(d.get("action"), d.get("started") or d.get("run") or "", "filed:", " ".join(f["run"] for f in d.get("filed", [])) or "-")' "$out" 2>/dev/null)"
    case "$act" in
      started|resumed|running)
        pid=$(python3 -I -c 'import json,sys; print(json.loads(sys.argv[1]).get("pid",""))' "$out")
        while alive "$pid"; do sleep 30; done ;;
      waiting)  # until the usage window refreshes. A sleeping loop dies with the container, so the loop exits and a
                # scheduled task that the session sets for that time starts it again (starting it early is harmless)
        when=$(python3 -I -c 'import json,sys; print(json.loads(sys.argv[1])["resume_after_utc"])' "$out")
        echo "$when" > /home/claude/runs/next_start
        say "waiting for the usage window to refresh at $when: the loop exits; a scheduled task starts it again then"
        rm -f "$PIDF"; exit 0 ;;
      complete) return 0 ;;
      *) say "unexpected tick output; retrying in 5 minutes"; sleep 300 ;;
    esac
  done
}
say "batch loop started (pid $$) at $(git rev-parse --short HEAD)"
stage SEED_BATCH_RUNS=/home/claude/runs/smoke2 SEED_BATCH_OUT="$REPO/$B/smoke" SEED_BATCH_DAYS=91 SEED_BATCH_ORDER=obm_v4:6,obm_v5:6
python3 -I "$B/smoke_check.py" "$B/smoke/obm_v4-seed6-91d" "$B/smoke/obm_v5-seed6-91d" > "$B/smoke/CHECK.md" 2>&1
if grep -q "FAIL" "$B/smoke/CHECK.md"; then
  say "a smoke check failed: stopping before any seed (see $B/smoke/CHECK.md)"; push "smoke check failed; seeds not started"; rm -f "$PIDF"; exit 1
fi
push "smoke checks passed; seeds start"
stage SEED_BATCH_RUNS=/home/claude/runs/seeds SEED_BATCH_OUT="$REPO/$B"
python3 -I "$B/evaluate.py" > "$B/EVALUATION.md" 2>&1
push "seed batch complete; decision rules computed"
say "batch complete"; rm -f "$PIDF"
