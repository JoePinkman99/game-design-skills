#!/bin/sh
# Install the game-analysis + game-redesign Claude Code skills for this user.
# Replaces existing copies of these two skill folders, if present.
set -e

SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${HOME}/.claude/skills"

command -v python3 >/dev/null 2>&1 || {
  echo "ERROR: python3 not found on PATH — required by matrix_analysis.py" >&2
  exit 1
}

mkdir -p "$DEST"
rm -rf "$DEST/game-analysis" "$DEST/game-redesign"
cp -R "$SRC/game-analysis" "$DEST/"
cp -R "$SRC/game-redesign" "$DEST/"

echo "Installed:"
ls "$DEST/game-analysis" "$DEST/game-redesign"

echo ""
echo "Smoke test (matrix script on classic RPS):"
TMP="$(mktemp /tmp/skill-smoke.XXXXXX.json)"
printf '{"nodes":["Rock","Paper","Scissors"],"matrix":[[0,-1,1],[1,0,-1],[-1,1,0]]}' > "$TMP"
python3 "$DEST/game-analysis/scripts/matrix_analysis.py" "$TMP" | head -6
rm -f "$TMP"

echo ""
echo "OK — start a NEW Claude Code session so the skills register."
