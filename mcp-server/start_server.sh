#!/bin/bash
# AI/DEV Lab MCP Server Startup Script
# Starts the MCP server with proper environment configuration

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting AI/DEV Lab MCP Server..."
echo "📁 Project Root: $PROJECT_ROOT"
echo "🔒 Security Mode: Guardian Enabled"
echo "📡 Transport: STDIO (Local Development)"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    exit 1
fi

# Check Python version (3.7+ required for dataclasses)
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo "❌ Error: Python 3.7+ is required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Set environment variables
export AI_DEV_PROJECT_ROOT="$PROJECT_ROOT"
export AI_DEV_MCP_MODE="development"
export AI_DEV_GUARDIAN_CONFIG="$PROJECT_ROOT/mcp-server/guardian_config.yaml"

# Create log directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/logs"

# Start the MCP server
echo "🔧 Starting MCP server..."
echo "📝 Logs will be written to: $SCRIPT_DIR/logs/mcp_server.log"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

cd "$SCRIPT_DIR"
python3 server.py 2>&1 | tee "logs/mcp_server.log"
