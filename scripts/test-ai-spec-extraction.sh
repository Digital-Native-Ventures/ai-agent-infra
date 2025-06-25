#!/usr/bin/env bash
set -euo pipefail

ISSUE_ID="${1:-871}"
REPO="${GITHUB_REPOSITORY:-Digital-Native-Ventures/alfred-agent-platform-v2}"

echo "🔍 Testing AI-Spec extraction for issue #$ISSUE_ID..."

# Extract AI-Spec using the same method as engineer-run.sh
AI_SPEC=$(gh issue view "$ISSUE_ID" --repo "$REPO" --comments | awk '/^### AI-Spec/{flag=1; ai_spec=""} flag{ai_spec=ai_spec"\n"$0} /^--$/{if(flag) {last_spec=ai_spec; flag=0}} END{print last_spec}')

if [[ -z "$AI_SPEC" ]]; then
  echo "❌ No AI-Spec found"
  exit 1
fi

echo "✅ Found AI-Spec:"
echo "---"
echo "$AI_SPEC"
echo "---"

# Count lines and characters
LINE_COUNT=$(echo "$AI_SPEC" | wc -l)
CHAR_COUNT=$(echo "$AI_SPEC" | wc -c)

echo ""
echo "📊 Stats:"
echo "  - Lines: $LINE_COUNT"
echo "  - Characters: $CHAR_COUNT"