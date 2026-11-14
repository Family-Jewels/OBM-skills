#!/usr/bin/env bash
# Run one isolated headless agent.
# usage: run_agent.sh <workdir> <prompt-file> <model> [settings.json] [max_budget_usd]
# Writes <workdir>/../<name>.result.json (final JSON) and <name>.stream.jsonl (full transcript).
set -u
WD=$(realpath "$1"); PROMPT=$(cat "$2"); MODEL=$3; SETTINGS=${4:-}; BUDGET=${5:-3}
CFG=/home/claude/obm-lab/cfg-clean; mkdir -p "$CFG"
OUT=$(dirname "$WD")/$(basename "$WD")
EXTRA=(); [ -n "$SETTINGS" ] && EXTRA=(--settings "$SETTINGS")
cd "$WD" || exit 1
CLAUDE_CONFIG_DIR=$CFG env -u CLAUDE_CODE_SYNC_SKILLS -u CLAUDE_CODE_SYNC_PLUGINS -u CLAUDE_CODE_ENABLE_CFC \
  -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD -u CLAUDE_ADDITIONAL_DIRECTORIES \
  claude -p "$PROMPT" --model "$MODEL" --output-format stream-json --verbose \
  --tools "Bash,Read,Write,Edit,Glob,Grep" --allowedTools "Bash,Read,Write,Edit,Glob,Grep" \
  --disallowedTools "mcp__claude-in-chrome" --permission-mode acceptEdits --strict-mcp-config \
  --max-budget-usd "$BUDGET" "${EXTRA[@]}" > "$OUT.stream.jsonl" 2> "$OUT.stderr.txt"
tail -n 1 "$OUT.stream.jsonl" > "$OUT.result.json"
