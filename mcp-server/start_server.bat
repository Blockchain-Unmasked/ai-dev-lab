@echo off
REM AI/DEV Lab MCP Server Startup Script (Windows)
REM Starts the MCP server with proper environment configuration

echo 🚀 Starting AI/DEV Lab MCP Server...
echo 📁 Project Root: %~dp0..
echo 🔒 Security Mode: Guardian Enabled
echo 📡 Transport: STDIO (Local Development)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is required but not installed
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Check Python version (3.7+ required for dataclasses)
for /f "tokens=2" %%i in ('python -c "import sys; print(sys.version.split()[0])" 2^>nul') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% detected

REM Set environment variables
set AI_DEV_PROJECT_ROOT=%~dp0..
set AI_DEV_MCP_MODE=development
set AI_DEV_GUARDIAN_CONFIG=%AI_DEV_PROJECT_ROOT%\mcp-server\guardian_config.yaml

REM Create log directory if it doesn't exist
if not exist "logs" mkdir logs

REM Start the MCP server
echo 🔧 Starting MCP server...
echo 📝 Logs will be written to: logs\mcp_server.log
echo ⏹️  Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
python server.py > logs\mcp_server.log 2>&1

pause
