#!/usr/bin/env python3
"""
Website Audit MCP Server for AI/DEV Lab
Provides website auditing capabilities for the blockchainunmasked.com project
FOLLOWS APP MCP SERVER RULES: Limited scope, application-specific, sandboxed
"""

import json
import logging
import asyncio
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebsiteAuditMCPServer:
    """Website Audit MCP Server with limited scope and sandboxed access"""
    
    def __init__(self):
        self.server = Server("ai-dev-lab-website-audit")
        self.access_level = "application_scope"
        self.scope = "single_application"
        self.security_level = "sandboxed"
        self.app_root = Path(__file__).parent.parent.parent
        self.audit_data_dir = self.app_root / "audit-data"
        self.screenshots_dir = self.audit_data_dir / "screenshots"
        self.content_dir = self.audit_data_dir / "content"
        self.setup_directories()
        self.setup_capabilities()
        self.setup_handlers()
        
    def setup_directories(self):
        """Setup audit data directories within app scope"""
        try:
            self.audit_data_dir.mkdir(exist_ok=True)
            self.screenshots_dir.mkdir(exist_ok=True)
            self.content_dir.mkdir(exist_ok=True)
            logger.info("✅ Audit directories created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create audit directories: {e}")
    
    def setup_capabilities(self):
        """Setup server capabilities - LIMITED SCOPE ONLY"""
        self.server.capabilities = {
            "tools": [
                Tool(
                    name="audit_webpage",
                    description="Audit a single webpage for content and structure",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "audit_type": {"type": "string", "enum": ["content", "structure", "performance", "full"]},
                            "save_to_archive": {"type": "boolean"}
                        },
                        "required": ["url"]
                    }
                ),
                Tool(
                    name="audit_website_structure",
                    description="Analyze website structure and navigation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "base_url": {"type": "string"},
                            "max_depth": {"type": "number"},
                            "include_external": {"type": "boolean"}
                        },
                        "required": ["base_url"]
                    }
                ),
                Tool(
                    name="extract_page_content",
                    description="Extract and structure page content for archival",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "content_type": {"type": "string", "enum": ["text", "html", "metadata", "all"]},
                            "extraction_rules": {"type": "object"}
                        },
                        "required": ["url"]
                    }
                ),
                Tool(
                    name="analyze_page_performance",
                    description="Analyze page performance metrics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "metrics": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["url"]
                    }
                ),
                Tool(
                    name="save_audit_data",
                    description="Save audit data to local archive",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "data_type": {"type": "string", "enum": ["content", "screenshot", "metadata", "performance"]},
                            "data": {"type": "object"},
                            "filename": {"type": "string"}
                        },
                        "required": ["data_type", "data"]
                    }
                ),
                Tool(
                    name="get_audit_summary",
                    description="Get summary of all audit data collected",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "summary_type": {"type": "string", "enum": ["overview", "detailed", "statistics"]}
                        }
                    }
                ),
                Tool(
                    name="health",
                    description="Health check endpoint - always succeeds",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ],
            "resources": [
                Resource(
                    uri="audit://data-overview",
                    name="Audit Data Overview",
                    description="Overview of collected audit data",
                    mimeType="application/json"
                ),
                Resource(
                    uri="audit://content-archive",
                    name="Content Archive",
                    description="Archived website content",
                    mimeType="application/json"
                ),
                Resource(
                    uri="audit://screenshots",
                    name="Screenshots Archive",
                    description="Archived website screenshots",
                    mimeType="application/json"
                ),
                Resource(
                    uri="audit://performance-data",
                    name="Performance Data",
                    description="Website performance metrics",
                    mimeType="application/json"
                )
            ]
        }
    
    def setup_handlers(self):
        """Setup server event handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            return self.server.capabilities["tools"]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
            logger.info(f"Website Audit Tool called: {name} with args: {arguments}")
            
            if name == "audit_webpage":
                return await self.audit_webpage(arguments)
            elif name == "audit_website_structure":
                return await self.audit_website_structure(arguments)
            elif name == "extract_page_content":
                return await self.extract_page_content(arguments)
            elif name == "analyze_page_performance":
                return await self.analyze_page_performance(arguments)
            elif name == "save_audit_data":
                return await self.save_audit_data(arguments)
            elif name == "get_audit_summary":
                return await self.get_audit_summary(arguments)
            elif name == "health":
                return {"ok": True, "server": "ai-dev-lab-website-audit", "time": datetime.now().isoformat()}
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            return self.server.capabilities["resources"]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            if uri == "audit://data-overview":
                return self.get_audit_data_overview()
            elif uri == "audit://content-archive":
                return self.get_content_archive()
            elif uri == "audit://screenshots":
                return self.get_screenshots_archive()
            elif uri == "audit://performance-data":
                return self.get_performance_data()
            else:
                raise ValueError(f"Unknown resource: {uri}")
    
    async def audit_webpage(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Audit a single webpage for content and structure"""
        url = args["url"]
        audit_type = args.get("audit_type", "full")
        save_to_archive = args.get("save_to_archive", True)
        
        try:
            # Validate URL is within allowed scope (blockchainunmasked.com)
            if not self._is_allowed_url(url):
                return {"success": False, "error": "URL not in allowed scope for this app server"}
            
            audit_results = {
                "url": url,
                "audit_type": audit_type,
                "timestamp": self._get_timestamp(),
                "results": {}
            }
            
            # Perform content audit
            if audit_type in ["content", "full"]:
                content_audit = await self._audit_page_content(url)
                audit_results["results"]["content"] = content_audit
            
            # Perform structure audit
            if audit_type in ["structure", "full"]:
                structure_audit = await self._audit_page_structure(url)
                audit_results["results"]["structure"] = structure_audit
            
            # Perform performance audit
            if audit_type in ["performance", "full"]:
                performance_audit = await self._audit_page_performance(url)
                audit_results["results"]["performance"] = performance_audit
            
            # Save to archive if requested
            if save_to_archive:
                await self._save_audit_results(url, audit_results)
            
            return {"success": True, "audit_results": audit_results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def audit_website_structure(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze website structure and navigation"""
        base_url = args["base_url"]
        max_depth = args.get("max_depth", 3)
        include_external = args.get("include_external", False)
        
        try:
            # Validate base URL
            if not self._is_allowed_url(base_url):
                return {"success": False, "error": "Base URL not in allowed scope for this app server"}
            
            # This would typically call the Lab MCP server for actual crawling
            # App servers cannot perform system operations directly
            structure_analysis = {
                "base_url": base_url,
                "max_depth": max_depth,
                "include_external": include_external,
                "note": "This app server cannot perform crawling directly. Use Lab MCP server for actual crawling.",
                "timestamp": self._get_timestamp()
            }
            
            return {"success": True, "structure_analysis": structure_analysis}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def extract_page_content(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and structure page content for archival"""
        url = args["url"]
        content_type = args.get("content_type", "all")
        extraction_rules = args.get("extraction_rules", {})
        
        try:
            # Validate URL
            if not self._is_allowed_url(url):
                return {"success": False, "error": "URL not in allowed scope for this app server"}
            
            # This would typically call the Lab MCP server for actual extraction
            # App servers cannot perform network operations directly
            content_extraction = {
                "url": url,
                "content_type": content_type,
                "extraction_rules": extraction_rules,
                "note": "This app server cannot perform content extraction directly. Use Lab MCP server for actual extraction.",
                "timestamp": self._get_timestamp()
            }
            
            return {"success": True, "content_extraction": content_extraction}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def analyze_page_performance(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze page performance metrics"""
        url = args["url"]
        metrics = args.get("metrics", ["load_time", "status_code", "content_size"])
        
        try:
            # Validate URL
            if not self._is_allowed_url(url):
                return {"success": False, "error": "URL not in allowed scope for this app server"}
            
            # This would typically call the Lab MCP server for actual performance analysis
            # App servers cannot perform network operations directly
            performance_analysis = {
                "url": url,
                "requested_metrics": metrics,
                "note": "This app server cannot perform performance analysis directly. Use Lab MCP server for actual analysis.",
                "timestamp": self._get_timestamp()
            }
            
            return {"success": True, "performance_analysis": performance_analysis}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def save_audit_data(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Save audit data to local archive"""
        data_type = args["data_type"]
        data = args["data"]
        filename = args.get("filename", f"{data_type}_{self._get_timestamp()}.json")
        
        try:
            # Ensure filename is safe and within app scope
            safe_filename = self._sanitize_filename(filename)
            file_path = self.audit_data_dir / safe_filename
            
            # Save data to file
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            return {
                "success": True,
                "data_type": data_type,
                "filename": safe_filename,
                "file_path": str(file_path),
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_audit_summary(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get summary of all audit data collected"""
        summary_type = args.get("summary_type", "overview")
        
        try:
            summary = {
                "summary_type": summary_type,
                "timestamp": self._get_timestamp(),
                "data_directory": str(self.audit_data_dir),
                "total_files": len(list(self.audit_data_dir.rglob("*"))),
                "content_files": len(list(self.content_dir.rglob("*"))) if self.content_dir.exists() else 0,
                "screenshot_files": len(list(self.screenshots_dir.rglob("*"))) if self.screenshots_dir.exists() else 0
            }
            
            if summary_type == "detailed":
                summary["file_list"] = self._get_file_list()
            elif summary_type == "statistics":
                summary["statistics"] = self._get_audit_statistics()
            
            return {"success": True, "summary": summary}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_audit_data_overview(self) -> str:
        """Get overview of audit data"""
        try:
            overview = {
                "total_audits": 0,
                "content_audits": 0,
                "performance_audits": 0,
                "structure_audits": 0,
                "last_audit": None,
                "data_directory": str(self.audit_data_dir)
            }
            return json.dumps(overview, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
    
    def get_content_archive(self) -> str:
        """Get content archive information"""
        try:
            content_info = {
                "archive_location": str(self.content_dir),
                "total_files": len(list(self.content_dir.rglob("*"))) if self.content_dir.exists() else 0,
                "file_types": ["json", "html", "txt"],
                "last_updated": self._get_timestamp()
            }
            return json.dumps(content_info, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
    
    def get_screenshots_archive(self) -> str:
        """Get screenshots archive information"""
        try:
            screenshots_info = {
                "archive_location": str(self.screenshots_dir),
                "total_files": len(list(self.screenshots_dir.rglob("*"))) if self.screenshots_dir.exists() else 0,
                "file_types": ["png", "jpg", "jpeg"],
                "last_updated": self._get_timestamp()
            }
            return json.dumps(screenshots_info, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
    
    def get_performance_data(self) -> str:
        """Get performance data information"""
        try:
            performance_info = {
                "data_location": str(self.audit_data_dir),
                "metrics_collected": ["load_time", "status_code", "content_size"],
                "total_records": 0,
                "last_updated": self._get_timestamp()
            }
            return json.dumps(performance_info, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
    
    # Helper methods - LIMITED SCOPE ONLY
    def _is_allowed_url(self, url: str) -> bool:
        """Check if URL is within allowed scope for this app server"""
        allowed_domains = [
            "blockchainunmasked.com",
            "www.blockchainunmasked.com"
        ]
        
        for domain in allowed_domains:
            if domain in url:
                return True
        return False
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe storage"""
        # Remove or replace unsafe characters
        safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
        # Ensure it doesn't start with a dot or contain path separators
        safe_filename = safe_filename.lstrip('.').replace('/', '_').replace('\\', '_')
        return safe_filename
    
    async def _audit_page_content(self, url: str) -> Dict[str, Any]:
        """Audit page content (placeholder - would call Lab MCP server)"""
        return {
            "content_audit": "Content audit would be performed by Lab MCP server",
            "url": url,
            "timestamp": self._get_timestamp()
        }
    
    async def _audit_page_structure(self, url: str) -> Dict[str, Any]:
        """Audit page structure (placeholder - would call Lab MCP server)"""
        return {
            "structure_audit": "Structure audit would be performed by Lab MCP server",
            "url": url,
            "timestamp": self._get_timestamp()
        }
    
    async def _audit_page_performance(self, url: str) -> Dict[str, Any]:
        """Audit page performance (placeholder - would call Lab MCP server)"""
        return {
            "performance_audit": "Performance audit would be performed by Lab MCP server",
            "url": url,
            "timestamp": self._get_timestamp()
        }
    
    async def _save_audit_results(self, url: str, results: Dict[str, Any]) -> bool:
        """Save audit results to local archive"""
        try:
            safe_filename = f"audit_{self._sanitize_filename(url)}_{self._get_timestamp()}.json"
            file_path = self.audit_data_dir / safe_filename
            
            with open(file_path, 'w') as f:
                json.dump(results, f, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Failed to save audit results: {e}")
            return False
    
    def _get_file_list(self) -> List[str]:
        """Get list of files in audit data directory"""
        try:
            files = []
            for file_path in self.audit_data_dir.rglob("*"):
                if file_path.is_file():
                    files.append(str(file_path.relative_to(self.audit_data_dir)))
            return files
        except Exception as e:
            logger.error(f"Failed to get file list: {e}")
            return []
    
    def _get_audit_statistics(self) -> Dict[str, Any]:
        """Get audit statistics"""
        try:
            stats = {
                "total_files": len(list(self.audit_data_dir.rglob("*"))),
                "json_files": len(list(self.audit_data_dir.rglob("*.json"))),
                "html_files": len(list(self.audit_data_dir.rglob("*.html"))),
                "text_files": len(list(self.audit_data_dir.rglob("*.txt"))),
                "image_files": len(list(self.audit_data_dir.rglob("*.png"))) + len(list(self.audit_data_dir.rglob("*.jpg")))
            }
            return stats
        except Exception as e:
            logger.error(f"Failed to get audit statistics: {e}")
            return {"error": str(e)}

async def main():
    """Main server function"""
    audit_server = WebsiteAuditMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await audit_server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ai-dev-lab-website-audit",
                server_version="1.0.0",
                capabilities=audit_server.server.capabilities
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
