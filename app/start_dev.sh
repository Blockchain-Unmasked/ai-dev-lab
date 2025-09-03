#!/bin/bash
# AI/DEV Lab Web Application - Development Startup Script
# Following OCINT architecture standards and development practices

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting AI/DEV Lab Web Application (Development Mode)"
echo "📁 Project Root: $PROJECT_ROOT"
echo "🏗️  Architecture: OCINT Standards Compliant"
echo "🔒 Security: Guardian MCP + OCINT Standards"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python version (3.13+ required per OCINT standards)
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 13 ]); then
    echo "❌ Error: Python 3.13+ is required per OCINT standards (found $PYTHON_VERSION)"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected (OCINT compliant)"

# Check Node.js version (18+ required for frontend build tools)
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is required for frontend build tools"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2)
NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)

if [ "$NODE_MAJOR" -lt 18 ]; then
    echo "❌ Error: Node.js 18+ is required (found $NODE_VERSION)"
    exit 1
fi

echo "✅ Node.js $NODE_VERSION detected"

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "🔧 Setting up Python virtual environment..."
    cd backend
    python3 -m venv venv
    echo "✅ Virtual environment created"
    cd ..
else
    echo "✅ Virtual environment exists"
fi

# Activate virtual environment and install dependencies
echo "📦 Installing Python dependencies..."
cd backend
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Python dependencies installed"
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
echo "✅ Frontend dependencies installed"
cd ..

# Set environment variables
export AI_DEV_PROJECT_ROOT="$PROJECT_ROOT"
export AI_DEV_MCP_MODE="development"
export AI_DEV_GUARDIAN_CONFIG="$PROJECT_ROOT/mcp-server/guardian_config.yaml"
export PYTHONPATH="$PROJECT_ROOT/app/backend:$PYTHONPATH"

# Clean up any existing processes
echo "🧹 Cleaning up any existing development processes..."
pkill -f "uvicorn.*8000" > /dev/null 2>&1 || true
pkill -f "uvicorn.*8001" > /dev/null 2>&1 || true
pkill -f "http.server.*3000" > /dev/null 2>&1 || true
sleep 2

echo ""
echo "🎯 Starting development servers..."
echo ""

# Start backend server
echo "🔧 Starting FastAPI backend server..."
cd backend
source venv/bin/activate

# Use the existing working simple startup script
# Check if port 8000 is already in use
if lsof -i :8000 > /dev/null 2>&1; then
    echo "    ⚠️  Port 8000 is already in use. Stopping existing process..."
    lsof -ti :8000 | xargs kill -9 > /dev/null 2>&1
    sleep 2
fi

echo "    🚀 Starting backend using working simple startup script..."
cd backend
python start_simple.py &
BACKEND_PID=$!
cd ..

# Wait for services to start
echo ""
echo "⏳ Waiting for services to start up..."
sleep 5

# Health check
echo ""
echo "🔍 **Health Check Status**"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend (8000):     HEALTHY"
else
    echo "❌ Backend (8000):     STARTING..."
fi

# Check frontend
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend (3000):    HEALTHY"
else
    echo "❌ Frontend (3000):    STARTING..."
fi

# Check Lab MCP server
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Lab MCP (8001):     HEALTHY"
else
    echo "❌ Lab MCP (8001):     STARTING..."
fi

echo ""
echo "💡 **Note**: stdio-based MCP servers run in background"
echo "   Use 'ps aux | grep -E \"(app-demo|database-server)\"' to check"
echo ""

# Start frontend development server (simple HTTP server for now)
echo "🌐 Starting frontend development server..."
cd frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!
cd ..

# Start MCP servers for the app
echo "🔌 Starting MCP servers for app agents..."

# Start app-demo-server (stdio-based)
echo "  📱 Starting app-demo-server..."
cd mcp-servers/app-demo-server
if [ ! -f "venv/bin/activate" ]; then
    echo "    📦 Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "    📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "    🚀 Starting app-demo-server (stdio-based)..."
python3 server.py &
APP_DEMO_PID=$!
cd ../..

# Start database-server (stdio-based)
echo "  🗄️  Starting database-server..."
cd mcp-servers/database-server
if [ ! -f "venv/bin/activate" ]; then
    echo "    📦 Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "    📦 Installing dependencies..."
# Create requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "mcp>=1.0.0" > requirements.txt
    echo "asyncio" >> requirements.txt
    echo "typing-extensions>=4.0.0" >> requirements.txt
fi
pip install -r requirements.txt > /dev/null 2>&1
echo "    🚀 Starting database-server (stdio-based)..."
python3 server.py &
DATABASE_PID=$!
cd ../..

# Start main Lab MCP server (HTTP-based on port 8001)
echo "  🔧 Starting main Lab MCP server (port 8001)..."
cd ../mcp-server
if [ ! -f "venv/bin/activate" ]; then
    echo "    📦 Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "    📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Check if port 8001 is already in use
if lsof -i :8001 > /dev/null 2>&1; then
    echo "    ⚠️  Port 8001 is already in use. Stopping existing process..."
    lsof -ti :8001 | xargs kill -9 > /dev/null 2>&1
    sleep 2
fi

echo "    🚀 Starting Lab MCP server on port 8001..."
python3 -m uvicorn http_server:app --host 0.0.0.0 --port 8001 --reload &
LAB_MCP_PID=$!
cd ../app

echo ""
echo "✅ Development servers started!"
echo ""
echo "🚀 **Service Endpoints**"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Frontend:        http://localhost:3000"
echo "🔧 Backend:         http://localhost:8000"
echo "📚 API Docs:        http://localhost:8000/docs"
echo "🔒 Health Check:    http://localhost:8000/health"
echo ""
echo "🔌 **MCP Servers**"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Lab MCP Server:  http://localhost:8001 (HTTP)"
echo "📱 App Demo Server: stdio://app/mcp-servers/app-demo-server"
echo "🗄️  Database Server: stdio://app/mcp-servers/database-server"
echo ""
echo "📊 **Process IDs**"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Backend:     PID $BACKEND_PID"
echo "Frontend:    PID $FRONTEND_PID"
echo "Lab MCP:     PID $LAB_MCP_PID"
echo "App Demo:    PID $APP_DEMO_PID"
echo "Database:    PID $DATABASE_PID"
echo ""
echo "⏹️  Press Ctrl+C to stop all servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down development servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    kill $APP_DEMO_PID 2>/dev/null || true
    kill $DATABASE_PID 2>/dev/null || true
    kill $LAB_MCP_PID 2>/dev/null || true
    echo "✅ All servers stopped"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
