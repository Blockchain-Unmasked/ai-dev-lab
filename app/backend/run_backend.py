#!/usr/bin/env python3
"""
Backend Launcher Script
Fixes relative import issues by setting up proper Python path
"""

import sys
import os
from pathlib import Path

# Get the backend directory path
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

# Set environment variables
os.environ['PYTHONPATH'] = str(backend_dir)

try:
    # Import the app
    from main import app
    print("✅ Backend imports successful!")
    
    # Start the server
    import uvicorn
    print("🚀 Starting FastAPI backend server...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting backend: {e}")
    sys.exit(1)
