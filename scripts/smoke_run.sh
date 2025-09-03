#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Starting MCP Audit Smoke Test..."

# 0) venv if not active
if [ -z "${VIRTUAL_ENV:-}" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv .venv
  source .venv/bin/activate
  python -m pip install --upgrade pip
fi

# 1) Setup (your script should install any deps)
echo "🔧 Setting up MCP testing environment..."
python scripts/setup_mcp_testing.py

# 2) Verify rules (must pass)
echo "✅ Verifying Cursor rules..."
python scripts/verify_cursor_rules.py

# 3) Conformance test (must pass; writes report)
echo "🧪 Running MCP conformance tests..."
python scripts/mcp_conformance_test_suite.py --all

# 4) Sanity: report exists and contains key sections
REPORT="docs/08-audit/mcp_audit_report.md"
echo "📝 Validating audit report..."

if [ ! -f "$REPORT" ]; then
    echo "FAIL: missing report $REPORT"
    exit 1
fi

# Check for required sections
if ! grep -q "## MCP Conformance" "$REPORT"; then
    echo "FAIL: report missing 'MCP Conformance' section"
    exit 1
fi

if ! grep -q "## Security" "$REPORT"; then
    echo "FAIL: report missing 'Security' section"
    exit 1
fi

if ! grep -q "## Performance" "$REPORT"; then
    echo "FAIL: report missing 'Performance' section"
    exit 1
fi

echo "🎉 OK: Full smoke passed. Report at $REPORT"
echo "📊 Summary: All MCP servers validated, security boundaries enforced, performance metrics recorded"
