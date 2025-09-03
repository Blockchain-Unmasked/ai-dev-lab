#!/usr/bin/env python3
"""
AI/DEV Lab - Cursor MCP Connection Verification
Verifies that Cursor IDE can connect to and use the MCP server.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

def test_mcp_server_connection():
    """Test MCP server connection and basic functionality."""
    print("🔌 Testing MCP Server Connection for Cursor IDE...")
    
    try:
        # Start MCP server
        print("  🚀 Starting MCP server...")
        server_process = subprocess.Popen(
            [sys.executable, "mcp-server/server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Test initialize request
        print("  🔧 Testing MCP initialize...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {
                    "name": "cursor-ide",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send initialize request
        server_process.stdin.write(json.dumps(init_request) + "\n")
        server_process.stdin.flush()
        
        # Read response from stdout instead of stdin
        response = server_process.stdout.readline()
        if response:
            try:
                response_data = json.loads(response)
                if "result" in response_data:
                    print("  ✅ MCP initialize successful")
                    print(f"     Server: {response_data['result'].get('serverInfo', {}).get('name', 'Unknown')}")
                    print(f"     Version: {response_data['result'].get('serverInfo', {}).get('version', 'Unknown')}")
                else:
                    print("  ❌ MCP initialize failed")
                    print(f"     Error: {response_data.get('error', 'Unknown error')}")
            except json.JSONDecodeError:
                print("  ❌ Invalid JSON response from MCP server")
        else:
            print("  ❌ No response from MCP server")
        
        # Test tools/list request
        print("  🛠️  Testing MCP tools list...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        server_process.stdin.write(json.dumps(tools_request) + "\n")
        server_process.stdin.flush()
        
        response = server_process.stdout.readline()
        if response:
            try:
                response_data = json.loads(response)
                if "result" in response_data:
                    tools = response_data["result"].get("tools", [])
                    print(f"  ✅ MCP tools list successful - {len(tools)} tools available")
                    for tool in tools:
                        print(f"     - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
                else:
                    print("  ❌ MCP tools list failed")
            except json.JSONDecodeError:
                print("  ❌ Invalid JSON response for tools list")
        else:
            print("  ❌ No response for tools list")
        
        # Test resources/list request
        print("  📚 Testing MCP resources list...")
        resources_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list"
        }
        
        server_process.stdin.write(json.dumps(resources_request) + "\n")
        server_process.stdin.flush()
        
        response = server_process.stdout.readline()
        if response:
            try:
                response_data = json.loads(response)
                if "result" in response_data:
                    resources = response_data["result"].get("resources", [])
                    print(f"  ✅ MCP resources list successful - {len(resources)} resources available")
                    for resource in resources:
                        print(f"     - {resource.get('name', 'Unknown')}: {resource.get('description', 'No description')}")
                else:
                    print("  ❌ MCP resources list failed")
            except json.JSONDecodeError:
                print("  ❌ Invalid JSON response for resources list")
        else:
            print("  ❌ No response for resources list")
        
        # Cleanup
        server_process.terminate()
        server_process.wait()
        
        print("  ✅ MCP server connection test completed successfully")
        return True
        
    except Exception as e:
        print(f"  ❌ MCP server connection test failed: {e}")
        return False

def test_cursor_configuration():
    """Test Cursor IDE configuration for MCP integration."""
    print("\n🔧 Testing Cursor IDE MCP Configuration...")
    
    cursor_mcp_config = Path(".cursor/mcp.json")
    if not cursor_mcp_config.exists():
        print("  ❌ Cursor MCP configuration file missing")
        return False
    
    try:
        with open(cursor_mcp_config, 'r') as f:
            config = json.load(f)
        
        # Check required configuration
        required_keys = ["mcpServers", "cursorIntegration"]
        for key in required_keys:
            if key not in config:
                print(f"  ❌ Missing required configuration key: {key}")
                return False
        
        # Check MCP server configuration
        mcp_servers = config.get("mcpServers", {})
        if "ai-dev-lab" not in mcp_servers:
            print("  ❌ AI/DEV Lab MCP server not configured")
            return False

        server_config = mcp_servers["ai-dev-lab"]
        required_server_keys = ["command", "args", "cwd"]
        for key in required_server_keys:
            if key not in server_config:
                print(f"  ❌ Missing server configuration key: {key}")
                return False
        
        print("  ✅ Cursor MCP configuration is valid")
        print(f"     Server: {server_config.get('description', 'Unknown')}")
        print(f"     Command: {' '.join(server_config.get('args', []))}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading Cursor MCP configuration: {e}")
        return False

def main():
    """Main verification process."""
    print("🧪 AI/DEV Lab - Cursor MCP Connection Verification")
    print("=" * 60)
    
    # Test Cursor configuration
    config_ok = test_cursor_configuration()
    
    # Test MCP server connection
    connection_ok = test_mcp_server_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 VERIFICATION SUMMARY")
    print("=" * 60)
    
    print(f"Cursor Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"MCP Server Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    
    if config_ok and connection_ok:
        print("\n🎉 ALL VERIFICATIONS PASSED!")
        print("🚀 Cursor IDE is fully configured and ready to use MCP server.")
        print("💡 You can now:")
        print("   - Use AI tools through MCP server integration")
        print("   - Switch between Free and Enterprise modes")
        print("   - Leverage Guardian security for safe AI operations")
        print("   - Build your web app with AI assistance")
        return True
    else:
        print("\n❌ SOME VERIFICATIONS FAILED.")
        print("🔧 Please review the configuration and try again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
