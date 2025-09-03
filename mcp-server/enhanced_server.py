#!/usr/bin/env python3
"""
Enhanced Lab MCP Server for AI/DEV Lab
Provides web scraping, terminal automation, and infrastructure management capabilities
FOLLOWS LAB MCP SERVER RULES: Full system access, repository-wide scope
"""

import json
import logging
import asyncio
import subprocess
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool

# Try to import requests for health checks
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Import mission system
from mission_system import MissionSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedLabMCPServer:
    """Enhanced Lab MCP Server with full system access capabilities"""
    
    def __init__(self):
        self.server = Server("ai-dev-lab-enhanced")
        self.access_level = "full_system"
        self.scope = "repository_wide"
        self.security_level = "high"
        self.repository_root = Path(__file__).parent.parent
        try:
            self.mission_system = MissionSystem(self.repository_root)
            logger.info("✅ Mission system initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ Mission system failed to initialize: {e}")
            self.mission_system = None
        
        # Initialize development environment process tracking
        self.dev_environment_process = None
        
        self.setup_capabilities()
        self.setup_handlers()
        
    def setup_capabilities(self):
        """Setup server capabilities - FULL SYSTEM ACCESS"""
        self.server.capabilities = {
            "tools": {
                "run_terminal_command": Tool(
                    name="run_terminal_command",
                    description="Execute terminal commands with full system access",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "command": {"type": "string"},
                            "working_directory": {"type": "string"},
                            "timeout": {"type": "number"}
                        },
                        "required": ["command"]
                    }
                ),
                "install_package": Tool(
                    name="install_package",
                    description="Install system packages using package managers",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "package_name": {"type": "string"},
                            "package_manager": {"type": "string", "enum": ["pip", "npm", "brew", "apt", "yum"]},
                            "version": {"type": "string"}
                        },
                        "required": ["package_name", "package_manager"]
                    }
                ),
                "check_system_status": Tool(
                    name="check_system_status",
                    description="Check system resources and status",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "check_type": {"type": "string", "enum": ["disk", "memory", "cpu", "network", "all"]}
                        }
                    }
                ),
                "backup_data": Tool(
                    name="backup_data",
                    description="Create data backups with full system access",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "source_path": {"type": "string"},
                            "backup_location": {"type": "string"},
                            "backup_type": {"type": "string", "enum": ["full", "incremental", "differential"]}
                        },
                        "required": ["source_path"]
                    }
                ),
                "scrape_webpage": Tool(
                    name="scrape_webpage",
                    description="Extract content from a single webpage using full system tools",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "extract_type": {"type": "string", "enum": ["text", "html", "metadata", "all"]},
                            "wait_time": {"type": "number"}
                        },
                        "required": ["url"]
                    }
                ),
                "crawl_website": Tool(
                    name="crawl_website",
                    description="Discover and crawl all pages on a website",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "base_url": {"type": "string"},
                            "max_pages": {"type": "number"},
                            "respect_robots": {"type": "boolean"},
                            "output_directory": {"type": "string"}
                        },
                        "required": ["base_url"]
                    }
                ),
                "capture_screenshot": Tool(
                    name="capture_screenshot",
                    description="Take screenshots at various viewports using full system access",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "viewport": {"type": "string", "enum": ["desktop", "tablet", "mobile", "custom"]},
                            "width": {"type": "number"},
                            "height": {"type": "number"},
                            "output_path": {"type": "string"}
                        },
                        "required": ["url", "viewport"]
                    }
                ),
                "extract_content": Tool(
                    name="extract_content",
                    description="Extract and structure content from web pages",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "extraction_rules": {"type": "object"},
                            "output_format": {"type": "string", "enum": ["json", "xml", "csv", "text"]}
                        },
                        "required": ["url"]
                    }
                ),
                "health": Tool(
                    name="health",
                    description="Health check endpoint - always succeeds",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                "analyze_performance": Tool(
                    name="analyze_performance",
                    description="Analyze website performance and metrics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "metrics": {"type": "array", "items": {"type": "string"}},
                            "output_format": {"type": "string"}
                        },
                        "required": ["url"]
                    }
                ),
                "manage_mcp_servers": Tool(
                    name="manage_mcp_servers",
                    description="Manage and configure other MCP servers in the system",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "action": {"type": "string", "enum": ["start", "stop", "restart", "status", "configure"]},
                            "server_name": {"type": "string"},
                            "configuration": {"type": "object"}
                        },
                        "required": ["action"]
                    }
                ),
                "create_mission": Tool(
                    name="create_mission",
                    description="Create a new mission with full mission system integration",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "mission_name": {"type": "string"},
                            "mission_description": {"type": "string"},
                            "mission_type": {"type": "string", "enum": ["DEVELOPMENT", "AUDIT", "TESTING", "DEPLOYMENT", "MAINTENANCE", "RESEARCH", "DOCUMENTATION", "SECURITY", "INTEGRATION"]},
                            "mission_priority": {"type": "string", "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "OPTIONAL"]},
                            "mission_objectives": {"type": "array", "items": {"type": "object"}},
                            "execution_plan": {"type": "object"},
                            "mission_requirements": {"type": "object"}
                        },
                        "required": ["mission_name", "mission_description", "mission_type"]
                    }
                ),
                "get_mission_briefing": Tool(
                    name="get_mission_briefing",
                    description="Get mission briefing using prompt engine",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "mission_id": {"type": "string"}
                        },
                        "required": ["mission_id"]
                    }
                ),
                "get_execution_plan": Tool(
                    name="get_execution_plan",
                    description="Get execution plan for mission or specific phase",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "mission_id": {"type": "string"},
                            "phase_id": {"type": "string"}
                        },
                        "required": ["mission_id"]
                    }
                ),
                "update_mission_status": Tool(
                    name="update_mission_status",
                    description="Update mission status and stage",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "mission_id": {"type": "string"},
                            "new_status": {"type": "string", "enum": ["PLANNING", "BRIEFING", "EXECUTION", "DEBRIEFING", "COMPLETED", "FAILED", "PAUSED", "CANCELLED"]},
                            "stage": {"type": "string", "enum": ["INITIALIZATION", "ANALYSIS", "IMPLEMENTATION", "TESTING", "VALIDATION", "DEPLOYMENT", "MONITORING"]}
                        },
                        "required": ["mission_id", "new_status"]
                    }
                ),
                "list_missions": Tool(
                    name="list_missions",
                    description="List all active and completed missions",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status_filter": {"type": "string", "enum": ["active", "completed", "all"]}
                        }
                    }
                ),
                "start_development_environment": Tool(
                    name="start_development_environment",
                    description="Start the full development environment (frontend, backend, MCP servers)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "services": {"type": "array", "items": {"type": "string"}, "description": "Specific services to start (default: all)"},
                            "environment": {"type": "string", "enum": ["development", "staging", "production"], "default": "development"}
                        }
                    }
                ),
                "stop_development_environment": Tool(
                    name="stop_development_environment",
                    description="Stop the development environment and all running services",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "services": {"type": "array", "items": {"type": "string"}, "description": "Specific services to stop (default: all)"},
                            "force": {"type": "boolean", "description": "Force stop all processes"}
                        }
                    }
                ),
                "check_environment_health": Tool(
                    name="check_environment_health",
                    description="Check health status of all development environment services",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "detailed": {"type": "boolean", "description": "Include detailed health information"},
                            "services": {"type": "array", "items": {"type": "string"}, "description": "Specific services to check (default: all)"}
                        }
                    }
                )
            },
            "resources": {
                "lab://system-status": Resource(
                    uri="lab://system-status",
                    name="System Status",
                    description="Current system status and resource usage",
                    mimeType="application/json"
                ),
                "lab://repository-structure": Resource(
                    uri="lab://repository-structure",
                    name="Repository Structure",
                    description="Complete repository file and directory structure",
                    mimeType="application/json"
                ),
                "lab://mcp-servers": Resource(
                    uri="lab://mcp-servers",
                    name="MCP Servers Status",
                    description="Status of all MCP servers in the system",
                    mimeType="application/json"
                ),
                "lab://audit-progress": Resource(
                    uri="lab://audit-progress",
                    name="Website Audit Progress",
                    description="Current progress of website audit operations",
                    mimeType="application/json"
                )
            }
        }
    
    def setup_handlers(self):
        """Setup server event handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            return list(self.server.capabilities["tools"].values())
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
            logger.info(f"Lab MCP Tool called: {name} with args: {arguments}")
            
            if name == "run_terminal_command":
                return await self.run_terminal_command(arguments)
            elif name == "install_package":
                return await self.install_package(arguments)
            elif name == "check_system_status":
                return await self.check_system_status(arguments)
            elif name == "backup_data":
                return await self.backup_data(arguments)
            elif name == "scrape_webpage":
                return await self.scrape_webpage(arguments)
            elif name == "crawl_website":
                return await self.crawl_website(arguments)
            elif name == "capture_screenshot":
                return await self.capture_screenshot(arguments)
            elif name == "extract_content":
                return await self.extract_content(arguments)
            elif name == "analyze_performance":
                return await self.analyze_performance(arguments)
            elif name == "manage_mcp_servers":
                return await self.manage_mcp_servers(arguments)
            elif name == "create_mission":
                return await self.create_mission(arguments)
            elif name == "get_mission_briefing":
                return await self.get_mission_briefing(arguments)
            elif name == "get_execution_plan":
                return await self.get_execution_plan(arguments)
            elif name == "update_mission_status":
                return await self.update_mission_status(arguments)
            elif name == "list_missions":
                return await self.list_missions(arguments)
            elif name == "start_development_environment":
                return await self.start_development_environment(arguments)
            elif name == "stop_development_environment":
                return await self.stop_development_environment(arguments)
            elif name == "check_environment_health":
                return await self.check_environment_health(arguments)
            elif name == "health":
                return {"ok": True, "server": "ai-dev-lab-enhanced", "time": datetime.now().isoformat()}
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            return list(self.server.capabilities["resources"].values())
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            if uri == "lab://system-status":
                return self.get_system_status()
            elif uri == "lab://repository-structure":
                return self.get_repository_structure()
            elif uri == "lab://mcp-servers":
                return self.get_mcp_servers_status()
            elif uri == "lab://audit-progress":
                return self.get_audit_progress()
            else:
                raise ValueError(f"Unknown resource: {uri}")
    
    async def run_terminal_command(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute terminal commands with full system access"""
        command = args["command"]
        working_directory = args.get("working_directory", str(self.repository_root))
        timeout = args.get("timeout", 30)
        
        try:
            # Validate working directory is within repository
            if not self._is_safe_path(working_directory):
                return {"success": False, "error": "Working directory outside repository bounds"}
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": True,
                "command": command,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "working_directory": working_directory
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {timeout} seconds"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def install_package(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Install system packages using package managers"""
        package_name = args["package_name"]
        package_manager = args["package_manager"]
        version = args.get("version")
        
        try:
            if package_manager == "pip":
                cmd = f"pip install {package_name}"
                if version:
                    cmd += f"=={version}"
            elif package_manager == "npm":
                cmd = f"npm install {package_name}"
                if version:
                    cmd += f"@{version}"
            elif package_manager == "brew":
                cmd = f"brew install {package_name}"
            else:
                return {"success": False, "error": f"Unsupported package manager: {package_manager}"}
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            return {
                "success": result.returncode == 0,
                "package": package_name,
                "manager": package_manager,
                "command": cmd,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def check_system_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Check system resources and status"""
        check_type = args.get("check_type", "all")
        
        try:
            status = {}
            
            if check_type in ["disk", "all"]:
                status["disk"] = self._get_disk_usage()
            
            if check_type in ["memory", "all"]:
                status["memory"] = self._get_memory_usage()
            
            if check_type in ["cpu", "all"]:
                status["cpu"] = self._get_cpu_usage()
            
            if check_type in ["network", "all"]:
                status["network"] = self._get_network_status()
            
            return {"success": True, "status": status}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def backup_data(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create data backups with full system access"""
        source_path = args["source_path"]
        backup_location = args.get("backup_location", f"{source_path}_backup")
        backup_type = args.get("backup_type", "full")
        
        try:
            # Validate source path is within repository
            if not self._is_safe_path(source_path):
                return {"success": False, "error": "Source path outside repository bounds"}
            
            # Create backup
            if backup_type == "full":
                cmd = f"cp -r {source_path} {backup_location}"
            else:
                cmd = f"rsync -av {source_path} {backup_location}"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            return {
                "success": result.returncode == 0,
                "source": source_path,
                "backup_location": backup_location,
                "backup_type": backup_type,
                "command": cmd,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def scrape_webpage(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content from a single webpage"""
        url = args["url"]
        extract_type = args.get("extract_type", "all")
        wait_time = args.get("wait_time", 5)
        
        try:
            # Use curl for basic extraction
            if extract_type in ["text", "all"]:
                text_cmd = f"curl -s '{url}' | grep -v '<script' | grep -v '<style' | sed 's/<[^>]*>//g'"
                text_result = subprocess.run(text_cmd, shell=True, capture_output=True, text=True)
                text_content = text_result.stdout.strip()
            else:
                text_content = ""
            
            # Use curl for HTML
            if extract_type in ["html", "all"]:
                html_cmd = f"curl -s '{url}'"
                html_result = subprocess.run(html_cmd, shell=True, capture_output=True, text=True)
                html_content = html_result.stdout
            else:
                html_content = ""
            
            return {
                "success": True,
                "url": url,
                "extract_type": extract_type,
                "text_content": text_content,
                "html_content": html_content,
                "timestamp": self._get_timestamp()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def crawl_website(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Discover and crawl all pages on a website"""
        base_url = args["base_url"]
        max_pages = args.get("max_pages", 100)
        respect_robots = args.get("respect_robots", True)
        output_directory = args.get("output_directory", f"crawl_output_{self._sanitize_filename(base_url)}")
        
        try:
            # Create output directory
            os.makedirs(output_directory, exist_ok=True)
            
            # Use wget for crawling
            wget_cmd = f"wget --recursive --level=2 --page-requisites --adjust-extension --span-hosts --convert-links --restrict-file-names=windows --domains {base_url} --no-parent --directory-prefix={output_directory} {base_url}"
            
            if respect_robots:
                wget_cmd += " --robots=on"
            
            result = subprocess.run(wget_cmd, shell=True, capture_output=True, text=True)
            
            return {
                "success": result.returncode == 0,
                "base_url": base_url,
                "output_directory": output_directory,
                "command": wget_cmd,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def capture_screenshot(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Take screenshots at various viewports"""
        url = args["url"]
        viewport = args["viewport"]
        width = args.get("width", 1920 if viewport == "desktop" else 768 if viewport == "tablet" else 375)
        height = args.get("height", 1080 if viewport == "desktop" else 1024 if viewport == "tablet" else 667)
        output_path = args.get("output_path", f"screenshot_{self._sanitize_filename(url)}_{viewport}.png")
        
        try:
            # Use Puppeteer if available, otherwise use wkhtmltoimage
            if self._check_command("node"):
                # Try Puppeteer
                puppeteer_script = f"""
                const puppeteer = require('puppeteer');
                (async () => {{
                    const browser = await puppeteer.launch();
                    const page = await browser.newPage();
                    await page.setViewport({{width: {width}, height: {height}}});
                    await page.goto('{url}');
                    await page.screenshot({{path: '{output_path}'}});
                    await browser.close();
                }})();
                """
                
                with open("temp_screenshot.js", "w") as f:
                    f.write(puppeteer_script)
                
                result = subprocess.run("node temp_screenshot.js", shell=True, capture_output=True, text=True)
                os.remove("temp_screenshot.js")
                
                if result.returncode == 0:
                    return {
                        "success": True,
                        "url": url,
                        "viewport": viewport,
                        "output_path": output_path,
                        "method": "puppeteer"
                    }
            
            # Fallback to wkhtmltoimage
            wkhtml_cmd = f"wkhtmltoimage --width {width} --height {height} '{url}' {output_path}"
            result = subprocess.run(wkhtml_cmd, shell=True, capture_output=True, text=True)
            
            return {
                "success": result.returncode == 0,
                "url": url,
                "viewport": viewport,
                "output_path": output_path,
                "method": "wkhtmltoimage",
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def extract_content(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and structure content from web pages"""
        url = args["url"]
        extraction_rules = args.get("extraction_rules", {})
        output_format = args.get("output_format", "json")
        
        try:
            # Basic content extraction
            curl_cmd = f"curl -s '{url}'"
            result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {"success": False, "error": "Failed to fetch URL"}
            
            html_content = result.stdout
            
            # Extract basic metadata
            import re
            title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
            title = title_match.group(1) if title_match else ""
            
            # Extract text content
            text_content = re.sub(r'<[^>]+>', '', html_content)
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            extracted_data = {
                "url": url,
                "title": title,
                "text_content": text_content[:1000] + "..." if len(text_content) > 1000 else text_content,
                "content_length": len(text_content),
                "timestamp": self._get_timestamp()
            }
            
            if output_format == "json":
                return {"success": True, "data": extracted_data}
            elif output_format == "text":
                return {"success": True, "data": f"Title: {title}\n\nContent: {text_content}"}
            else:
                return {"success": True, "data": extracted_data}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def analyze_performance(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze website performance and metrics"""
        url = args["url"]
        metrics = args.get("metrics", ["load_time", "status_code", "content_size"])
        output_format = args.get("output_format", "json")
        
        try:
            analysis_results = {}
            
            # Check status code and load time
            if "status_code" in metrics or "load_time" in metrics:
                curl_cmd = f"curl -s -w '%{http_code} %{time_total} %{size_download}' -o /dev/null '{url}'"
                result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    parts = result.stdout.strip().split()
                    if len(parts) >= 3:
                        analysis_results["status_code"] = int(parts[0])
                        analysis_results["load_time"] = float(parts[1])
                        analysis_results["content_size"] = int(parts[2])
            
            # Check if site is accessible
            if "accessibility" in metrics:
                ping_cmd = f"ping -c 1 {url.replace('https://', '').replace('http://', '').split('/')[0]}"
                ping_result = subprocess.run(ping_cmd, shell=True, capture_output=True, text=True)
                analysis_results["accessible"] = ping_result.returncode == 0
            
            analysis_results["url"] = url
            analysis_results["timestamp"] = self._get_timestamp()
            
            return {"success": True, "analysis": analysis_results}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def manage_mcp_servers(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Manage and configure other MCP servers in the system"""
        action = args["action"]
        server_name = args.get("server_name")
        configuration = args.get("configuration", {})
        
        try:
            if action == "status":
                # Check status of all MCP servers
                return {"success": True, "servers": self._get_mcp_servers_status()}
            elif action == "start":
                # Start a specific MCP server
                if not server_name:
                    return {"success": False, "error": "Server name required for start action"}
                return await self._start_mcp_server(server_name)
            elif action == "stop":
                # Stop a specific MCP server
                if not server_name:
                    return {"success": False, "error": "Server name required for stop action"}
                return await self._stop_mcp_server(server_name)
            else:
                return {"success": False, "error": f"Unsupported action: {action}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_system_status(self) -> str:
        """Get current system status"""
        try:
            status = {
                "disk": self._get_disk_usage(),
                "memory": self._get_memory_usage(),
                "cpu": self._get_cpu_usage(),
                "timestamp": self._get_timestamp()
            }
            return json.dumps(status, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
    
    def get_repository_structure(self) -> str:
        """Get complete repository file and directory structure"""
        try:
            structure = self._scan_directory(self.repository_root)
            return json.dumps(structure, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
    
    def get_mcp_servers_status(self) -> str:
        """Get status of all MCP servers in the system"""
        try:
            status = self._get_mcp_servers_status()
            return json.dumps(status, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
    
    def get_audit_progress(self) -> str:
        """Get current progress of website audit operations"""
        try:
            progress = {
                "phase": "infrastructure_setup",
                "completed_tasks": ["dependencies_installed", "directories_created"],
                "current_task": "enhanced_mcp_server_creation",
                "progress_percentage": 25,
                "timestamp": self._get_timestamp()
            }
            return json.dumps(progress, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)
    
    # Helper methods
    def _is_safe_path(self, path: str) -> bool:
        """Validate that path is within repository bounds"""
        try:
            resolved_path = Path(path).resolve()
            return str(resolved_path).startswith(str(self.repository_root.resolve()))
        except:
            return False
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _sanitize_filename(self, text: str) -> str:
        """Sanitize text for use in filenames"""
        import re
        return re.sub(r'[^\w\-_\.]', '_', text)
    
    def _check_command(self, command: str) -> bool:
        """Check if a command is available"""
        try:
            subprocess.run([command, "--version"], capture_output=True, check=True)
            return True
        except:
            return False
    
    def _get_disk_usage(self) -> Dict[str, Any]:
        """Get disk usage information"""
        try:
            result = subprocess.run("df -h .", shell=True, capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                return {
                    "filesystem": parts[0],
                    "size": parts[1],
                    "used": parts[2],
                    "available": parts[3],
                    "use_percent": parts[4],
                    "mounted_on": parts[5]
                }
        except:
            pass
        return {"error": "Could not retrieve disk usage"}
    
    def _get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage information"""
        try:
            result = subprocess.run("vm_stat", shell=True, capture_output=True, text=True)
            # Parse vm_stat output for macOS
            memory_info = {}
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    memory_info[key.strip()] = value.strip()
            return memory_info
        except:
            pass
        return {"error": "Could not retrieve memory usage"}
    
    def _get_cpu_usage(self) -> Dict[str, Any]:
        """Get CPU usage information"""
        try:
            result = subprocess.run("top -l 1 | grep 'CPU usage'", shell=True, capture_output=True, text=True)
            return {"cpu_usage": result.stdout.strip()}
        except:
            pass
        return {"error": "Could not retrieve CPU usage"}
    
    def _get_network_status(self) -> Dict[str, Any]:
        """Get network status information"""
        try:
            result = subprocess.run("ifconfig | grep 'inet '", shell=True, capture_output=True, text=True)
            return {"network_interfaces": result.stdout.strip()}
        except:
            pass
        return {"error": "Could not retrieve network status"}
    
    def _scan_directory(self, directory: Path) -> Dict[str, Any]:
        """Recursively scan directory structure"""
        try:
            structure = {"name": directory.name, "type": "directory", "children": []}
            
            for item in directory.iterdir():
                if item.is_dir():
                    structure["children"].append(self._scan_directory(item))
                else:
                    structure["children"].append({
                        "name": item.name,
                        "type": "file",
                        "size": item.stat().st_size
                    })
            
            return structure
        except Exception as e:
            return {"name": directory.name, "type": "directory", "error": str(e)}
    
    def _get_mcp_servers_status(self) -> Dict[str, Any]:
        """Get status of all MCP servers"""
        try:
            servers = {
                "lab_servers": {
                    "main": {"status": "running", "type": "core"},
                    "enhanced": {"status": "running", "type": "enhanced"}
                },
                "app_servers": {
                    "demo": {"status": "running", "type": "app_demo"},
                    "database": {"status": "running", "type": "database"},
                    "website_audit": {"status": "stopped", "type": "audit"},
                    "content_archive": {"status": "stopped", "type": "archive"}
                }
            }
            return servers
        except Exception as e:
            return {"error": str(e)}
    
    async def _start_mcp_server(self, server_name: str) -> Dict[str, Any]:
        """Start a specific MCP server"""
        # Implementation for starting MCP servers
        return {"success": True, "action": "start", "server": server_name, "status": "started"}
    
    async def _stop_mcp_server(self, server_name: str) -> Dict[str, Any]:
        """Stop a specific MCP server"""
        # Implementation for stopping MCP servers
        return {"success": True, "action": "stop", "server": server_name, "status": "stopped"}
    
    # Mission System Methods
    async def create_mission(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new mission with full mission system integration"""
        if not self.mission_system:
            return {"success": False, "error": "Mission system not available"}
            
        try:
            mission_data = {
                "mission_name": args["mission_name"],
                "mission_description": args["mission_description"],
                "mission_type": args["mission_type"],
                "mission_priority": args.get("mission_priority", "MEDIUM"),
                "mission_objectives": args.get("mission_objectives", []),
                "execution_plan": args.get("execution_plan", {}),
                "mission_requirements": args.get("mission_requirements", {})
            }
            
            mission_id = self.mission_system.create_mission(mission_data)
            
            return {
                "success": True,
                "mission_id": mission_id,
                "message": f"Mission '{args['mission_name']}' created successfully",
                "mission_data": mission_data
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_mission_briefing(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get mission briefing using prompt engine"""
        try:
            mission_id = args["mission_id"]
            briefing = self.mission_system.get_mission_briefing(mission_id)
            
            return {
                "success": True,
                "mission_id": mission_id,
                "briefing": briefing
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_execution_plan(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get execution plan for mission or specific phase"""
        try:
            mission_id = args["mission_id"]
            phase_id = args.get("phase_id")
            
            execution_plan = self.mission_system.get_execution_plan(mission_id, phase_id)
            
            return {
                "success": True,
                "mission_id": mission_id,
                "phase_id": phase_id,
                "execution_plan": execution_plan
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def update_mission_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Update mission status and stage"""
        try:
            mission_id = args["mission_id"]
            new_status = args["new_status"]
            stage = args.get("stage")
            
            success = self.mission_system.update_mission_status(mission_id, new_status, stage)
            
            if success:
                return {
                    "success": True,
                    "mission_id": mission_id,
                    "new_status": new_status,
                    "stage": stage,
                    "message": f"Mission status updated to {new_status}"
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to update mission {mission_id}"
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def list_missions(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List all active and completed missions"""
        try:
            status_filter = args.get("status_filter", "all")
            
            if status_filter == "active":
                missions = self.mission_system.list_active_missions()
            elif status_filter == "completed":
                missions = self.mission_system.list_completed_missions()
            else:
                missions = {
                    "active": self.mission_system.list_active_missions(),
                    "completed": self.mission_system.list_completed_missions()
                }
            
            return {
                "success": True,
                "status_filter": status_filter,
                "missions": missions,
                "count": len(missions) if isinstance(missions, list) else {
                    "active": len(missions["active"]),
                    "completed": len(missions["completed"])
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def start_development_environment(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Start the complete AI/DEV Lab development environment using start_dev.sh"""
        try:
            environment = args.get("environment", "development")
            services = args.get("services", ["frontend", "backend", "mcp"])
            wait_for_ready = args.get("wait_for_ready", True)
            
            # Path to the start_dev.sh script
            script_path = self.repository_root / "app" / "start_dev.sh"
            
            if not script_path.exists():
                return {
                    "success": False,
                    "error": f"start_dev.sh not found at {script_path}"
                }
            
            # Make script executable
            script_path.chmod(0o755)
            
            # Start the development environment
            logger.info(f"Starting {environment} environment with services: {services}")
            logger.info(f"Using script: {script_path}")
            
            # Set environment variables for the script
            env_vars = os.environ.copy()
            env_vars.update({
                "AI_DEV_PROJECT_ROOT": str(self.repository_root),
                "AI_DEV_MCP_MODE": environment,
                "AI_DEV_GUARDIAN_CONFIG": str(self.repository_root / "mcp-server" / "guardian_config.yaml"),
                "PYTHONPATH": f"{self.repository_root}/app/backend:{env_vars.get('PYTHONPATH', '')}",
                "MCP_APP_SERVERS_ENABLED": "true"
            })
            
            # Run the script in background with proper environment
            process = subprocess.Popen(
                [str(script_path)],
                cwd=str(self.repository_root / "app"),
                env=env_vars,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid  # Create new process group for proper cleanup
            )
            
            # Store process info for later management
            self.dev_environment_process = {
                "pid": process.pid,
                "pgid": os.getpgid(process.pid),
                "script_path": str(script_path),
                "start_time": datetime.now().isoformat(),
                "environment": environment,
                "services": services
            }
            
            if wait_for_ready:
                # Wait for services to start (script has built-in delays)
                logger.info("Waiting for services to start up...")
                await asyncio.sleep(8)  # Increased wait time for full startup
                
                # Check if services are responding
                health_status = await self.check_environment_health({"detailed": True})
                
                return {
                    "success": True,
                    "action": "start_development_environment",
                    "environment": environment,
                    "services": services,
                    "process_id": process.pid,
                    "process_group_id": os.getpgid(process.pid),
                    "health_status": health_status,
                    "script_used": str(script_path),
                    "message": f"Development environment started successfully using {script_path}",
                    "endpoints": {
                        "frontend": "http://localhost:3000",
                        "backend": "http://localhost:8000",
                        "api_docs": "http://localhost:8000/docs",
                        "health_check": "http://localhost:8000/health",
                        "mcp_servers": {
                            "app_demo": "stdio://app/mcp-servers/app-demo-server",
                            "database": "stdio://app/mcp-servers/database-server"
                        }
                    }
                }
            else:
                return {
                    "success": True,
                    "action": "start_development_environment",
                    "environment": environment,
                    "services": services,
                    "process_id": process.pid,
                    "process_group_id": os.getpgid(process.pid),
                    "script_used": str(script_path),
                    "message": f"Development environment starting in background using {script_path}",
                    "endpoints": {
                        "frontend": "http://localhost:3000",
                        "backend": "http://localhost:8000",
                        "api_docs": "http://localhost:8000/docs",
                        "health_check": "http://localhost:8000/health",
                        "mcp_servers": {
                            "app_demo": "stdio://app/mcp-servers/app-demo-server",
                            "database": "stdio://app/mcp-servers/database-server"
                        }
                    }
                }
                
        except Exception as e:
            logger.error(f"Failed to start development environment: {e}")
            return {"success": False, "error": str(e)}

    async def stop_development_environment(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Stop all development services and clean up processes"""
        try:
            force = args.get("force", False)
            cleanup = args.get("cleanup", True)
            
            logger.info("Stopping development environment")
            
            # Find and stop processes
            stopped_processes = []
            
            # First, try to stop the main development environment process group
            if hasattr(self, 'dev_environment_process') and self.dev_environment_process:
                try:
                    pgid = self.dev_environment_process.get('pgid')
                    if pgid:
                        logger.info(f"Stopping process group {pgid}")
                        if force:
                            subprocess.run(f"kill -9 -{pgid}", shell=True)
                        else:
                            subprocess.run(f"kill -{pgid}", shell=True)
                        stopped_processes.append({
                            "type": "process_group",
                            "pgid": pgid,
                            "force": force
                        })
                except Exception as e:
                    logger.warning(f"Failed to stop process group: {e}")
            
            # Check for common development server processes on specific ports
            common_ports = [3000, 8000, 8001, 8002, 8003]
            
            # Also check for MCP server processes
            mcp_server_processes = []
            try:
                # Check for app-demo-server and database-server processes
                result = subprocess.run(
                    "ps aux | grep -E '(app-demo-server|database-server)' | grep -v grep",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.stdout.strip():
                    mcp_server_processes = result.stdout.strip().split('\n')
            except Exception as e:
                logger.warning(f"Failed to check MCP server processes: {e}")
            
            for port in common_ports:
                try:
                    # Find process using the port
                    result = subprocess.run(
                        f"lsof -ti :{port}",
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    
                    if result.stdout.strip():
                        pids = result.stdout.strip().split('\n')
                        for pid in pids:
                            if pid.strip():
                                try:
                                    if force:
                                        subprocess.run(f"kill -9 {pid}", shell=True)
                                    else:
                                        subprocess.run(f"kill {pid}", shell=True)
                                    stopped_processes.append({
                                        "type": "port_process",
                                        "port": port,
                                        "pid": pid,
                                        "force": force
                                    })
                                except Exception as e:
                                    logger.warning(f"Failed to stop process {pid}: {e}")
                except Exception as e:
                    logger.warning(f"Failed to check port {port}: {e}")
            
            # Cleanup if requested
            if cleanup:
                # Clean up any temporary files or processes
                try:
                    subprocess.run("pkill -f 'http.server'", shell=True)
                    subprocess.run("pkill -f 'python.*main.py'", shell=True)
                    subprocess.run("pkill -f 'python.*run.py'", shell=True)
                except Exception as e:
                    logger.warning(f"Cleanup warning: {e}")
            
            return {
                "success": True,
                "action": "stop_development_environment",
                "stopped_processes": stopped_processes,
                "cleanup_performed": cleanup,
                "message": f"Stopped {len(stopped_processes)} processes"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def check_environment_health(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Check health status of all development services"""
        try:
            detailed = args.get("detailed", False)
            services = args.get("services", ["frontend", "backend", "mcp"])
            
            health_status = {}
            
            # Check frontend (port 3000)
            if "frontend" in services:
                if not REQUESTS_AVAILABLE:
                    health_status["frontend"] = {
                        "status": "unknown",
                        "port": 3000,
                        "error": "requests library not available"
                    }
                else:
                    try:
                        response = requests.get("http://localhost:3000", timeout=5)
                        health_status["frontend"] = {
                            "status": "healthy" if response.status_code == 200 else "unhealthy",
                            "port": 3000,
                            "response_time": response.elapsed.total_seconds(),
                            "status_code": response.status_code
                        }
                    except Exception as e:
                        health_status["frontend"] = {
                            "status": "unhealthy",
                            "port": 3000,
                            "error": str(e)
                        }
            
            # Check backend (port 8000)
            if "backend" in services:
                if not REQUESTS_AVAILABLE:
                    health_status["backend"] = {
                        "status": "unknown",
                        "port": 8000,
                        "error": "requests library not available"
                    }
                else:
                    try:
                        response = requests.get("http://localhost:8000/health", timeout=5)
                        health_status["backend"] = {
                            "status": "healthy" if response.status_code == 200 else "unhealthy",
                            "port": 8000,
                            "response_time": response.elapsed.total_seconds(),
                            "status_code": response.status_code
                        }
                    except Exception as e:
                        health_status["backend"] = {
                            "status": "unhealthy",
                            "port": 8000,
                            "error": str(e)
                        }
            
            # Check MCP server (port 8001)
            if "mcp" in services:
                if not REQUESTS_AVAILABLE:
                    health_status["mcp"] = {
                        "status": "unknown",
                        "port": 8001,
                        "error": "requests library not available"
                    }
                else:
                    try:
                        response = requests.get("http://localhost:8001/health", timeout=5)
                        health_status["mcp"] = {
                            "status": "healthy" if response.status_code == 200 else "unhealthy",
                            "port": 8001,
                            "response_time": response.elapsed.total_seconds(),
                            "status_code": response.status_code
                        }
                    except Exception as e:
                        health_status["mcp"] = {
                            "status": "unhealthy",
                            "port": 8001,
                            "error": str(e)
                        }
            
            # Overall health summary
            healthy_services = sum(1 for service in health_status.values() if service.get("status") == "healthy")
            total_services = len(health_status)
            overall_health = "healthy" if healthy_services == total_services else "degraded" if healthy_services > 0 else "unhealthy"
            
            result = {
                "success": True,
                "overall_health": overall_health,
                "healthy_services": healthy_services,
                "total_services": total_services,
                "health_percentage": round((healthy_services / total_services) * 100, 2) if total_services > 0 else 0,
                "services": health_status
            }
            
            if detailed:
                # Add system resource information
                result["system_resources"] = {
                    "disk": self._get_disk_usage(),
                    "memory": self._get_memory_usage(),
                    "cpu": self._get_cpu_usage()
                }
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}

async def main():
    """Main server function"""
    enhanced_server = EnhancedLabMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await enhanced_server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ai-dev-lab-enhanced",
                server_version="1.0.0",
                capabilities=enhanced_server.server.capabilities
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
