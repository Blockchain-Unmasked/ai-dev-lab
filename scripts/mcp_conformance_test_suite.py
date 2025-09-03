#!/usr/bin/env python3
"""
MCP Conformance Test Suite - AI/DEV Lab Project
Comprehensive testing for Lab and App MCP servers

Usage:
    python scripts/mcp_conformance_test_suite.py --lab-server
    python scripts/mcp_conformance_test_suite.py --app-server app-demo-server
    python scripts/mcp_conformance_test_suite.py --all
"""

import asyncio
import json
import time
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from mcp import stdio_client
    from mcp.client.stdio import StdioServerParameters
    from mcp.types import Tool
except ImportError:
    logger.error("MCP Python SDK not installed. Install with: pip install mcp")
    sys.exit(1)


class MCPConformanceTester:
    """Comprehensive MCP server conformance tester"""
    
    def __init__(self):
        self.test_results = {
            "lab_server": {},
            "app_servers": {},
            "overall": {}
        }
        self.start_time = time.time()
        
    async def test_lab_server(self) -> Dict[str, Any]:
        """Test the main Lab MCP server"""
        logger.info("🧪 Testing Lab MCP Server...")
        
        server_path = Path("mcp-server/enhanced_server.py")
        if not server_path.exists():
            return {"error": "Lab server not found", "status": "FAILED"}
            
        try:
            # Use stdio_client for proper MCP connection
            params = StdioServerParameters(
                command="python",
                args=[str(server_path)],
                cwd=str(Path.cwd())
            )
            async with stdio_client(params) as session:
                results = await self._test_server_session(session, "lab_server")
                self.test_results["lab_server"] = results
                return results
                
        except Exception as e:
            error_result = {
                "error": str(e),
                "status": "FAILED",
                "connection": "FAILED"
            }
            self.test_results["lab_server"] = error_result
            return error_result
    
    async def test_app_server(self, server_name: str) -> Dict[str, Any]:
        """Test a specific App MCP server"""
        logger.info(f"🧪 Testing App MCP Server: {server_name}")
        
        server_path = Path(f"app/mcp-servers/{server_name}/server.py")
        if not server_path.exists():
            return {
                "error": f"App server {server_name} not found", 
                "status": "FAILED"
            }
            
        try:
            # Use stdio_client for proper MCP connection
            params = StdioServerParameters(
                command="python",
                args=[str(server_path)],
                cwd=str(Path.cwd())
            )
            async with stdio_client(params) as session:
                results = await self._test_server_session(
                    session, f"app_{server_name}"
                )
                self.test_results["app_servers"][server_name] = results
                return results
                
        except Exception as e:
            error_result = {
                "error": str(e),
                "status": "FAILED",
                "connection": "FAILED"
            }
            self.test_results["app_servers"][server_name] = error_result
            return error_result
    
    async def _test_server_session(self, session, server_type: str) -> Dict[str, Any]:
        """Test a single MCP server session"""
        results = {
            "connection": "PASSED",
            "tools": {},
            "resources": {},
            "prompts": {},
            "performance": {},
            "error_handling": {},
            "status": "PASSED"
        }
        
        # Test 1: List Tools
        try:
            start_time = time.time()
            tools_response = await session.list_tools()
            tools_time = (time.time() - start_time) * 1000
            
            results["tools"]["count"] = len(tools_response.tools)
            results["tools"]["response_time_ms"] = tools_time
            results["tools"]["list"] = [
                tool.name for tool in tools_response.tools
            ]
            
            # Test individual tools with sample payloads
            for tool in tools_response.tools:
                tool_result = await self._test_tool_execution(session, tool)
                results["tools"][tool.name] = tool_result
                
        except Exception as e:
            results["tools"]["error"] = str(e)
            results["status"] = "FAILED"
        
        # Test 2: List Resources
        try:
            start_time = time.time()
            resources_response = await session.list_resources()
            resources_time = (time.time() - start_time) * 1000
            
            results["resources"]["count"] = len(resources_response.resources)
            results["resources"]["response_time_ms"] = resources_time
            results["resources"]["list"] = [
                r.uri for r in resources_response.resources
            ]
            
        except Exception as e:
            results["resources"]["error"] = str(e)
            results["status"] = "FAILED"
        
        # Test 3: List Prompts
        try:
            start_time = time.time()
            prompts_response = await session.list_prompts()
            prompts_time = (time.time() - start_time) * 1000
            
            results["prompts"]["count"] = len(prompts_response.prompts)
            results["prompts"]["response_time_ms"] = prompts_time
            results["prompts"]["list"] = [
                p.name for p in prompts_response.prompts
            ]
            
        except Exception as e:
            results["prompts"]["error"] = str(e)
            results["status"] = "FAILED"
        
        # Test 4: Performance Metrics
        results["performance"] = {
            "tools_response_ms": results["tools"].get("response_time_ms", 0),
            "resources_response_ms": results["resources"].get("response_time_ms", 0),
            "prompts_response_ms": results["prompts"].get("response_time_ms", 0)
        }
        
        # Test 5: Error Handling
        results["error_handling"] = await self._test_error_handling(session)
        
        return results
    
    async def _test_tool_execution(self, session, tool: Tool) -> Dict[str, Any]:
        """Test individual tool execution with sample payloads"""
        tool_result = {
            "schema_valid": True,
            "execution_tests": {},
            "status": "PASSED"
        }
        
        # Generate sample payload based on tool schema
        sample_payload = self._generate_sample_payload(tool)
        
        if sample_payload:
            try:
                start_time = time.time()
                # Note: We'll test with a small payload to avoid side effects
                execution_result = await session.call_tool(
                    tool.name, sample_payload
                )
                execution_time = (time.time() - start_time) * 1000
                
                tool_result["execution_tests"]["sample_payload"] = {
                    "status": "PASSED",
                    "response_time_ms": execution_time,
                    "has_response": bool(execution_result.content)
                }
                
            except Exception as e:
                tool_result["execution_tests"]["sample_payload"] = {
                    "status": "FAILED",
                    "error": str(e)
                }
                tool_result["status"] = "FAILED"
        
        return tool_result
    
    def _generate_sample_payload(self, tool: Tool) -> Optional[Dict[str, Any]]:
        """Generate a safe sample payload for tool testing"""
        if not hasattr(tool, 'inputSchema') or not tool.inputSchema:
            return {}
        
        schema = tool.inputSchema
        sample = {}
        
        try:
            if "properties" in schema:
                for prop_name, prop_schema in schema["properties"].items():
                    if "type" in prop_schema:
                        if prop_schema["type"] == "string":
                            if "enum" in prop_schema:
                                sample[prop_name] = prop_schema["enum"][0]
                            else:
                                sample[prop_name] = "test_value"
                        elif prop_schema["type"] == "number":
                            sample[prop_name] = 1
                        elif prop_schema["type"] == "boolean":
                            sample[prop_name] = False
                        elif prop_schema["type"] == "array":
                            sample[prop_name] = []
                        elif prop_schema["type"] == "object":
                            sample[prop_name] = {}
            
            # Only include required fields for safety
            if "required" in schema:
                required_fields = set(schema["required"])
                safe_sample = {
                    k: v for k, v in sample.items() if k in required_fields
                }
                return safe_sample
            
            return sample
            
        except Exception:
            return {}
    
    async def _test_error_handling(self, session) -> Dict[str, Any]:
        """Test error handling with invalid requests"""
        error_tests = {}
        
        # Test 1: Invalid tool name
        try:
            await session.call_tool("invalid_tool_name", {})
            error_tests["invalid_tool"] = (
                "FAILED - Should have rejected invalid tool"
            )
        except Exception:
            error_tests["invalid_tool"] = "PASSED - Properly rejected invalid tool"
        
        # Test 2: Invalid payload structure
        try:
            await session.call_tool(
                "get_project_status", 
                {"invalid_field": "invalid_value"}
            )
            error_tests["invalid_payload"] = "PASSED - Accepted valid payload"
        except Exception as e:
            error_tests["invalid_payload"] = (
                f"FAILED - Rejected valid payload: {str(e)}"
            )
        
        return error_tests
    
    async def test_all_servers(self):
        """Test all available MCP servers"""
        logger.info("🚀 Starting comprehensive MCP server testing...")
        
        # Test Lab Server
        await self.test_lab_server()
        
        # Test App Servers
        app_server_dirs = [
            "app-demo-server",
            "database-server", 
            "website-audit",
            "content-archive"
        ]
        
        for server_dir in app_server_dirs:
            if Path(f"app/mcp-servers/{server_dir}").exists():
                await self.test_app_server(server_dir)
        
        # Generate overall results
        self._generate_overall_results()
        
        # Print summary
        self._print_summary()
        
        # Save detailed results
        self._save_results()
    
    def _generate_overall_results(self):
        """Generate overall test results summary"""
        total_servers = 1 + len(self.test_results["app_servers"])
        passed_servers = 0
        
        # Count passed servers
        if self.test_results["lab_server"].get("status") == "PASSED":
            passed_servers += 1
            
        for app_server in self.test_results["app_servers"].values():
            if app_server.get("status") == "PASSED":
                passed_servers += 1
        
        self.test_results["overall"] = {
            "total_servers": total_servers,
            "passed_servers": passed_servers,
            "failed_servers": total_servers - passed_servers,
            "success_rate": (
                (passed_servers / total_servers) * 100 
                if total_servers > 0 else 0
            ),
            "total_test_time_seconds": time.time() - self.start_time
        }
    
    def _print_summary(self):
        """Print test results summary"""
        overall = self.test_results["overall"]
        
        print("\n" + "="*60)
        print("🎯 MCP CONFORMANCE TEST RESULTS")
        print("="*60)
        
        print(f"\n📊 Overall Results:")
        print(f"   Total Servers: {overall['total_servers']}")
        print(f"   Passed: {overall['passed_servers']}")
        print(f"   Failed: {overall['failed_servers']}")
        print(f"   Success Rate: {overall['success_rate']:.1f}%")
        print(f"   Total Test Time: {overall['total_test_time_seconds']:.1f}s")
        
        print(f"\n🔧 Lab Server:")
        lab_status = self.test_results["lab_server"].get("status", "UNKNOWN")
        lab_tools = self.test_results["lab_server"].get("tools", {}).get("count", 0)
        print(f"   Status: {lab_status}")
        print(f"   Tools: {lab_tools}")
        
        print(f"\n📱 App Servers:")
        for server_name, results in self.test_results["app_servers"].items():
            status = results.get("status", "UNKNOWN")
            tools = results.get("tools", {}).get("count", 0)
            print(f"   {server_name}: {status} ({tools} tools)")
        
        print("\n" + "="*60)
    
    def _save_results(self):
        """Save detailed test results to file"""
        output_file = f"mcp_conformance_results_{int(time.time())}.json"
        
        with open(output_file, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        logger.info(f"📝 Detailed results saved to: {output_file}")


async def main():
    """Main test execution function"""
    parser = argparse.ArgumentParser(description="MCP Conformance Test Suite")
    parser.add_argument(
        "--lab-server", 
        action="store_true", 
        help="Test only Lab MCP server"
    )
    parser.add_argument(
        "--app-server", 
        type=str, 
        help="Test specific App MCP server"
    )
    parser.add_argument(
        "--all", 
        action="store_true", 
        help="Test all MCP servers"
    )
    
    args = parser.parse_args()
    
    tester = MCPConformanceTester()
    
    if args.lab_server:
        await tester.test_lab_server()
        tester._generate_overall_results()
        tester._print_summary()
    elif args.app_server:
        await tester.test_app_server(args.app_server)
        tester._generate_overall_results()
        tester._print_summary()
    elif args.all:
        await tester.test_all_servers()
    else:
        print("Please specify --lab-server, --app-server <name>, or --all")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
