#!/usr/bin/env bash
set -euo pipefail

echo "→ Creating target folders (safe if exist)…"
mkdir -p docs meta sandbox/logs test_results/mcp

echo "→ Moving root stragglers…"
# Docs vs meta vs sandbox
[ -f AGENTS.md ] && git mv -f AGENTS.md docs/ 2>/dev/null || mv -f AGENTS.md docs/ 2>/dev/null || true
[ -f ai-dev-tree.txt ] && git mv -f ai-dev-tree.txt sandbox/ 2>/dev/null || mv -f ai-dev-tree.txt sandbox/ 2>/dev/null || true
[ -f organization_validation_report.json ] && \
  (git mv -f organization_validation_report.json sandbox/ 2>/dev/null || mv -f organization_validation_report.json sandbox/) || true
[ -f phase-cleanup-tree.txt ] && \
  (git mv -f phase-cleanup-tree.txt sandbox/ 2>/dev/null || mv -f phase-cleanup-tree.txt sandbox/) || true

echo "→ Collecting scattered logs into sandbox/logs…"
# app/backend logs
[ -f app/backend/app.log ] && (git mv -f app/backend/app.log sandbox/logs/ 2>/dev/null || mv -f app/backend/app.log sandbox/logs/) || true
[ -f app/backend/backend.log ] && (git mv -f app/backend/backend.log sandbox/logs/ 2>/dev/null || mv -f app/backend/backend.log sandbox/logs/) || true
# mcp-server logs
[ -f mcp-server/mcp_server.log ] && (git mv -f mcp-server/mcp_server.log sandbox/logs/ 2>/dev/null || mv -f mcp-server/mcp_server.log sandbox/logs/) || true
# tests/app.log
[ -f tests/app.log ] && (git mv -f tests/app.log sandbox/logs/ 2>/dev/null || mv -f tests/app.log sandbox/logs/) || true

echo "→ Removing system/temp files…"
find . -name ".DS_Store" -type f -delete || true
# Remove empty .benchmarks dir if present
[ -d .benchmarks ] && rmdir .benchmarks 2>/dev/null || true

echo "→ Ensuring .gitignore has the right exclusions…"
# Append only missing entries
touch .gitignore
IGNORE_BLOCK=$(cat <<'EOF'
# Node
node_modules/
npm-debug.log*
yarn-error.log*
pnpm-lock.yaml

# Python
.venv/
venv/
__pycache__/
*.pyc

# Env & secrets
.env
app/**/secrets/
app/**/secrets.*.json
mcp-server/**/secrets/
secrets/
*.key
*.pem

# Artifacts & logs
*.db
*.log
logs/
sandbox/logs/
test_results/
coverage/
EOF
)
# Add lines if not already present
while IFS= read -r line; do
  [ -z "$line" ] && continue
  grep -qxF "$line" .gitignore || echo "$line" >> .gitignore
done <<< "$IGNORE_BLOCK"

echo "→ Initialize Git if needed…"
if [ ! -d .git ]; then
  git init
  git add .gitignore >/dev/null 2>&1 || true
  git commit -m "chore(repo): init repo and enforce ignores" >/dev/null 2>&1 || true
fi

echo "→ Purging accidentally tracked heavy/ephemeral stuff (only if tracked)…"
if [ -d .git ]; then
  git rm -r --cached node_modules 2>/dev/null || true
  git rm -r --cached .venv 2>/dev/null || true
  git rm -r --cached logs 2>/dev/null || true
  git rm -r --cached test_results 2>/dev/null || true
  # Any tracked DBs/logs anywhere
  git ls-files -z | xargs -0 -n1 | grep -E '\.db$|\.log$' | xargs -I{} git rm --cached "{}" 2>/dev/null || true
  git add -A
  git commit -m "chore(repo): move stragglers, centralize logs, enforce ignores" 2>/dev/null || true
fi

echo "→ Verification:"
echo "  - node_modules tracked? (should be 0): $(git ls-files node_modules 2>/dev/null | wc -l || echo 'n/a')"
echo "  - .venv tracked? (should be 0): $(git ls-files .venv 2>/dev/null | wc -l || echo 'n/a')"
echo "  - Any tracked .log/.db files? (should be 0): $(git ls-files | grep -E '\.log$|\.db$' | wc -l || echo 'n/a')"

echo "→ Top-level overview (3 levels, noise ignored):"
tree -L 3 -I 'node_modules|.venv|venv|__pycache__|.git'
