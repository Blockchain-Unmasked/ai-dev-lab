#!/usr/bin/env python3
"""
Simple MCP connection test
"""

import asyncio
import sys
from pathlib import Path

try:
    from mcp import stdio_client
    from mcp.client.stdio import StdioServerParameters
    from mcp.client.session import ClientSession
    print("✅ MCP imports successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

async def test_lab_server():
    """Test connection to lab server"""
    server_path = Path("mcp-server/enhanced_server.py")
    
    if not server_path.exists():
        print(f"❌ Server not found: {server_path}")
        return False
    
    print(f"🔧 Testing lab server: {server_path}")
    
    try:
        params = StdioServerParameters(
            command="python",
            args=[str(server_path)],
            cwd=str(Path.cwd())
        )
        
        print("📡 Creating connection...")
        async with stdio_client(params) as (read_stream, write_stream):
            print("✅ Streams created")
            
            session = ClientSession(read_stream, write_stream)
            print("📋 Initializing session...")
            await session.initialize()
            print("✅ Session initialized")
            
            print("🔧 Listing tools...")
            tools = await session.list_tools()
            print(f"✅ Found {len(tools.tools)} tools")
            
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_lab_server())
    if success:
        print("🎉 Lab server test PASSED")
    else:
        print("💥 Lab server test FAILED")
        sys.exit(1)
