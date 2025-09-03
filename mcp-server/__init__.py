"""
AI/DEV Lab MCP Server Package

This package provides Model Context Protocol (MCP) servers for the AI/DEV Lab,
enabling AI agents to interact with the development environment through
standardized tools and resources.
"""

__version__ = "1.0.0"
__author__ = "AI/DEV Lab Team"
__description__ = "MCP servers for AI/DEV Lab development environment"

# Import main server classes
from .server import LabMCPServer
from .enhanced_server import EnhancedLabMCPServer
from .http_server import MCPHTTPServer

__all__ = [
    "LabMCPServer",
    "EnhancedLabMCPServer", 
    "MCPHTTPServer"
]
