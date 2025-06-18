#\!/usr/bin/env bash
set -euo pipefail
TASK="${TASK:-}"
TIMEOUT="${TIMEOUT:-900}"   # 15-min default watchdog

if [[ -z "$TASK" ]]; then
  echo "Usage: TASK=\"<instruction>\" $0" >&2
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/../../" && pwd)"
cd "$REPO_ROOT"
echo "🛠  Engineer executing: $TASK"

# Watchdog: kill if Claude hangs longer than $TIMEOUT
timeout "$TIMEOUT" claude /task "$TASK" || {
  echo "❌  Engineer timed out after $TIMEOUT s" >&2
  exit 124
}
