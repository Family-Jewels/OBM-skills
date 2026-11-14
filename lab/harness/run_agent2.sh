#!/usr/bin/env bash
# usage: run_agent2.sh <workdir> <prompt-file> <model> <settings.json|""> <budget_usd> <timeout_s>
set -u
WD=$(realpath "$1"); PROMPT=$(cat "$2"); MODEL=$3; SETTINGS=${4:-}; BUDGET=${5:-3}; TO=${6:-7200}
CFG=/home/claude/obm-lab/cfg-clean; mkdir -p "$CFG"
OUT=$(dirname "$WD")/$(basename "$WD")
EXTRA=(); [ -n "$SETTINGS" ] && EXTRA=(--settings "$SETTINGS")
cd "$WD" || exit 1
date +%s > "$OUT.start"
CLAUDE_CONFIG_DIR=$CFG timeout "$TO" env -u CLAUDE_CODE_SYNC_SKILLS -u CLAUDE_CODE_SYNC_PLUGINS -u CLAUDE_CODE_ENABLE_CFC \
  -u CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD -u CLAUDE_ADDITIONAL_DIRECTORIES \
  claude -p "$PROMPT" --model "$MODEL" --output-format stream-json --verbose \
  --tools "Bash,Read,Write,Edit,Glob,Grep,Agent" --allowedTools "Bash,Read,Write,Edit,Glob,Grep,Agent" \
  --disallowedTools "mcp__claude-in-chrome" --permission-mode acceptEdits --strict-mcp-config \
  --max-budget-usd "$BUDGET" "${EXTRA[@]}" > "$OUT.stream.jsonl" 2> "$OUT.stderr.txt"
echo $? > "$OUT.exit"; date +%s > "$OUT.end"
