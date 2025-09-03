#!/usr/bin/env python3
"""
AI/DEV Lab MCP Server - HTTP Interface
Provides HTTP access to MCP tools and resources for app integration
"""

import json
import logging
from typing import Any, Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from server import AIDevLabMCPServer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI/DEV Lab MCP Server",
    description="HTTP interface for MCP tools and resources",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP server
mcp_server = AIDevLabMCPServer()

# Pydantic models for requests
class ToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any] = {}

class ResourceReadRequest(BaseModel):
    uri: str

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI/DEV Lab MCP Server",
        "version": "1.0.0",
        "tools_available": len(mcp_server.capabilities["tools"]),
        "resources_available": len(mcp_server.capabilities["resources"])
    }

# MCP tools endpoint
@app.get("/tools")
async def list_tools():
    """List all available MCP tools"""
    try:
        result = mcp_server.handle_tools_list()
        return result
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# MCP tool call endpoint
@app.post("/tools/call")
async def call_tool(request: ToolCallRequest):
    """Execute an MCP tool"""
    try:
        result = mcp_server.handle_tools_call(request.name, request.arguments)
        return {
            "tool": request.name,
            "arguments": request.arguments,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error calling tool {request.name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# MCP resources endpoint
@app.get("/resources")
async def list_resources():
    """List all available MCP resources"""
    try:
        result = mcp_server.handle_resources_list()
        return result
    except Exception as e:
        logger.error(f"Error listing resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# MCP resource read endpoint
@app.post("/resources/read")
async def read_resource(request: ResourceReadRequest):
    """Read an MCP resource"""
    try:
        result = mcp_server.handle_resources_read(request.uri)
        return result
    except Exception as e:
        logger.error(f"Error reading resource {request.uri}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# MCP prompts endpoint
@app.get("/prompts")
async def list_prompts():
    """List all available MCP prompts"""
    try:
        result = mcp_server.handle_prompts_list()
        return result
    except Exception as e:
        logger.error(f"Error listing prompts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Server info endpoint
@app.get("/info")
async def server_info():
    """Get server information and capabilities"""
    return {
        "server_name": mcp_server.server_name,
        "version": mcp_server.version,
        "capabilities": {
            "tools_count": len(mcp_server.capabilities["tools"]),
            "resources_count": len(mcp_server.capabilities["resources"]),
            "prompts_count": len(mcp_server.capabilities["prompts"])
        }
    }

if __name__ == "__main__":
    logger.info("Starting AI/DEV Lab MCP HTTP Server on port 8001")
    uvicorn.run(
        "http_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
