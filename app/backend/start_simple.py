#!/usr/bin/env python3
"""
Simple startup script for AI/DEV Lab Backend
Fixes Python path issues and starts the server
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import uvicorn
    
    # Now we can import the app
    from app.backend.main import app
    
    print("🚀 Starting AI/DEV Lab Backend Server...")
    print(f"📍 Project root: {project_root}")
    print("🔧 Environment: Development")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload to avoid import issues
        log_level="info"
    )
