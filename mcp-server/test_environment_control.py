#!/usr/bin/env python3
"""
Test script for the new environment control tools in the Enhanced Lab MCP Server
"""

import asyncio
import json
from pathlib import Path
import sys

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def test_environment_control():
    """Test the new environment control tools"""
    
    print("🧪 Testing AI/DEV Lab Environment Control Tools")
    print("=" * 60)
    
    try:
        # Import the enhanced server
        from mcp_server.enhanced_server import EnhancedLabMCPServer
        
        # Create server instance
        server = EnhancedLabMCPServer()
        
        print("✅ Enhanced Lab MCP Server created successfully")
        
        # Test health check
        print("\n🔍 Testing environment health check...")
        health_result = await server.check_environment_health({
            "detailed": True,
            "services": ["frontend", "backend", "mcp"]
        })
        
        print(f"Health Check Result: {json.dumps(health_result, indent=2)}")
        
        # Test starting development environment
        print("\n🚀 Testing development environment start...")
        start_result = await server.start_development_environment({
            "environment": "development",
            "services": ["frontend", "backend"],
            "wait_for_ready": False
        })
        
        print(f"Start Result: {json.dumps(start_result, indent=2)}")
        
        # Wait a bit and check health again
        print("\n⏳ Waiting for services to start...")
        await asyncio.sleep(10)
        
        health_result_after = await server.check_environment_health({
            "detailed": False,
            "services": ["frontend", "backend"]
        })
        
        print(f"Health After Start: {json.dumps(health_result_after, indent=2)}")
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_environment_control())
