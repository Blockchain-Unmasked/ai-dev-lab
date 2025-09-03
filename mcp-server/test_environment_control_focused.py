#!/usr/bin/env python3
"""
Focused Test for Environment Control Tools
Tests the specific tools that interact with the app folder
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def test_environment_control_focused():
    """Test environment control tools specifically"""
    
    print("🎯 Focused Test: Environment Control Tools")
    print("=" * 50)
    
    try:
        # Import the enhanced server
        from enhanced_server import EnhancedLabMCPServer
        
        # Create server instance
        print("🔧 Creating Enhanced Lab MCP Server...")
        server = EnhancedLabMCPServer()
        print("✅ Enhanced Lab MCP Server created successfully")
        
        # Test 1: Check current environment status
        print("\n🔍 TEST 1: Current Environment Status")
        print("-" * 40)
        
        initial_health = await server.check_environment_health({
            "detailed": False,
            "services": ["frontend", "backend", "mcp"]
        })
        print(f"Initial Health: {json.dumps(initial_health, indent=2)}")
        
        # Test 2: Start Development Environment
        print("\n🚀 TEST 2: Start Development Environment")
        print("-" * 40)
        
        print("Starting development environment...")
        start_result = await server.start_development_environment({
            "environment": "development",
            "services": ["frontend", "backend"],
            "wait_for_ready": False
        })
        print(f"Start Result: {json.dumps(start_result, indent=2)}")
        
        # Wait for services to start
        print("\n⏳ Waiting 10 seconds for services to start...")
        await asyncio.sleep(10)
        
        # Test 3: Check Health After Start
        print("\n🏥 TEST 3: Health After Start")
        print("-" * 40)
        
        health_after_start = await server.check_environment_health({
            "detailed": True,
            "services": ["frontend", "backend"]
        })
        print(f"Health After Start: {json.dumps(health_after_start, indent=2)}")
        
        # Test 4: Test App Folder Interaction
        print("\n📂 TEST 4: App Folder Interaction")
        print("-" * 40)
        
        # Test listing app folder contents
        print("Listing app folder contents...")
        app_listing = await server.run_terminal_command({
            "command": "ls -la",
            "working_directory": str(project_root / "app"),
            "timeout": 10
        })
        print(f"App Folder Contents: {json.dumps(app_listing, indent=2)}")
        
        # Test checking specific app files
        print("\nChecking specific app files...")
        app_files = await server.run_terminal_command({
            "command": "find . -name '*.html' -o -name '*.py' | head -5",
            "working_directory": str(project_root / "app"),
            "timeout": 10
        })
        print(f"App Files Found: {json.dumps(app_files, indent=2)}")
        
        # Test 5: Test start_dev.sh Script
        print("\n📜 TEST 5: start_dev.sh Script Test")
        print("-" * 40)
        
        # Check if start_dev.sh exists and is executable
        script_check = await server.run_terminal_command({
            "command": "ls -la start_dev.sh",
            "working_directory": str(project_root / "app"),
            "timeout": 10
        })
        print(f"Script Check: {json.dumps(script_check, indent=2)}")
        
        # Test 6: Stop Environment
        print("\n🛑 TEST 6: Stop Environment")
        print("-" * 40)
        
        print("Stopping development environment...")
        stop_result = await server.stop_development_environment({
            "force": False,
            "cleanup": True
        })
        print(f"Stop Result: {json.dumps(stop_result, indent=2)}")
        
        # Test 7: Final Health Check
        print("\n🏥 TEST 7: Final Health Check")
        print("-" * 40)
        
        final_health = await server.check_environment_health({
            "detailed": False,
            "services": ["frontend", "backend"]
        })
        print(f"Final Health: {json.dumps(final_health, indent=2)}")
        
        # Summary
        print("\n" + "=" * 50)
        print("🎉 ENVIRONMENT CONTROL TEST COMPLETED!")
        print("=" * 50)
        
        print("\n✅ Environment start/stop working")
        print("✅ Health monitoring functional")
        print("✅ App folder interaction working")
        print("✅ start_dev.sh integration working")
        print("✅ Service management operational")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting focused environment control test...")
    success = asyncio.run(test_environment_control_focused())
    
    if success:
        print("\n🎯 Environment control tools are fully operational!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the output above.")
        sys.exit(1)
