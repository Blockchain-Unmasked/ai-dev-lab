#!/usr/bin/env python3
"""
Simple MCP connection test to debug the connection issue
"""

import asyncio
import sys
from pathlib import Path

try:
    from mcp import stdio_client
    from mcp.client.stdio import StdioServerParameters
    from mcp.client.session import ClientSession
    print("✅ MCP stdio_client imported successfully")
except ImportError as e:
    print(f"❌ Failed to import MCP: {e}")
    sys.exit(1)

async def test_connection():
    """Test basic MCP connection"""
    server_path = Path("mcp-server/enhanced_server.py")
    
    if not server_path.exists():
        print(f"❌ Server not found: {server_path}")
        return
    
    print(f"🔧 Testing connection to: {server_path}")
    
    try:
        # Test the connection
        params = StdioServerParameters(
            command="python",
            args=[str(server_path)],
            cwd=str(Path.cwd())
        )
        async with stdio_client(params) as (read_stream, write_stream):
            print("✅ Connection established successfully")
            print(f"Read stream type: {type(read_stream)}")
            print(f"Write stream type: {type(write_stream)}")
            
            # Create a client session
            session = ClientSession(read_stream, write_stream)
            await session.initialize()
            
            # Try to list tools
            try:
                tools = await session.list_tools()
                print(f"✅ Tools listed successfully: {len(tools.tools)} tools")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
            except Exception as e:
                print(f"❌ Failed to list tools: {e}")
                print(f"Available methods: {[m for m in dir(session) if not m.startswith('_')]}")
                
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
