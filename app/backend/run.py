#!/usr/bin/env python3
"""
AI/DEV Lab App - Server Entry Point
Run this file directly to start the FastAPI server
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Now import the app
from app.backend.main import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting AI/DEV Lab App Server...")
    print(f"📍 Project root: {project_root}")
    print("🔧 Environment: Development")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        "app.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
