#!/usr/bin/env python3
"""
AI/DEV Lab App - Static Asset Routes
Handles serving of frontend assets (CSS, JS, images)
"""

import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

# Create static router
static_router = APIRouter(prefix="/static", tags=["static"])

# Frontend directory path
FRONTEND_DIR = "/Users/hazael/Code/ai-dev-lab/app/frontend"

# MIME type mapping
MIME_TYPES = {
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.html': 'text/html',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.ico': 'image/x-icon',
    '.svg': 'image/svg+xml',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.eot': 'application/vnd.ms-fontobject'
}

@static_router.get("/{file_path:path}")
async def serve_static_file(file_path: str):
    """Serve static files from the frontend directory"""
    try:
        # Construct full file path
        full_path = os.path.join(FRONTEND_DIR, file_path)
        
        # Security: Prevent directory traversal
        if not os.path.abspath(full_path).startswith(FRONTEND_DIR):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Check if file exists
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Determine MIME type
        file_ext = Path(full_path).suffix.lower()
        content_type = MIME_TYPES.get(file_ext, 'application/octet-stream')
        
        # Read and return file
        with open(full_path, 'rb') as f:
            content = f.read()
        
        return Response(content=content, media_type=content_type)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving file: {str(e)}")

@static_router.get("/")
async def list_static_files():
    """List available static files (for debugging)"""
    try:
        files = []
        for root, dirs, filenames in os.walk(FRONTEND_DIR):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), FRONTEND_DIR)
                files.append(rel_path)
        
        return {"available_files": files, "total_count": len(files)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")
