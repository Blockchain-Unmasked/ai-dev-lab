#!/bin/bash
# AI/DEV Lab App - Server Startup Script

echo "🚀 Starting AI/DEV Lab App Server..."

# Activate virtual environment
source venv/bin/activate

# Start the server
python3 -m uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload
