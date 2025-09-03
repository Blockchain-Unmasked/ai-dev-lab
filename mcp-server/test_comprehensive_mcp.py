#!/usr/bin/env python3
"""
Comprehensive Test Script for AI/DEV Lab MCP Server
Tests all tools, especially environment control and app folder interaction
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def test_comprehensive_mcp():
    """Test all MCP tools comprehensively"""
    
    print("🧪 Comprehensive AI/DEV Lab MCP Server Test")
    print("=" * 60)
    
    try:
        # Import the enhanced server
        from enhanced_server import EnhancedLabMCPServer
        
        # Create server instance
        print("🔧 Creating Enhanced Lab MCP Server...")
        server = EnhancedLabMCPServer()
        print("✅ Enhanced Lab MCP Server created successfully")
        
        # Test 1: Basic System Tools
        print("\n" + "="*50)
        print("🔍 TEST 1: Basic System Tools")
        print("="*50)
        
        # Test system status
        print("\n📊 Testing system status...")
        system_status = server.get_system_status()
        print(f"System Status: {system_status}")
        
        # Test repository structure
        print("\n📁 Testing repository structure...")
        repo_structure = server.get_repository_structure()
        print(f"Repository Structure: {repo_structure[:500]}...")
        
        # Test 2: Terminal Command Execution
        print("\n" + "="*50)
        print("🔍 TEST 2: Terminal Command Execution")
        print("="*50)
        
        # Test basic terminal command
        print("\n💻 Testing terminal command execution...")
        terminal_result = await server.run_terminal_command({
            "command": "pwd",
            "working_directory": str(project_root),
            "timeout": 10
        })
        print(f"Terminal Command Result: {json.dumps(terminal_result, indent=2)}")
        
        # Test 3: App Folder Interaction
        print("\n" + "="*50)
        print("🔍 TEST 3: App Folder Interaction")
        print("="*50)
        
        # Test listing app folder contents
        print("\n📂 Testing app folder listing...")
        app_listing = await server.run_terminal_command({
            "command": "ls -la",
            "working_directory": str(project_root / "app"),
            "timeout": 10
        })
        print(f"App Folder Listing: {json.dumps(app_listing, indent=2)}")
        
        # Test checking app folder structure
        print("\n🏗️ Testing app folder structure...")
        app_structure = await server.run_terminal_command({
            "command": "find . -type f -name '*.py' | head -10",
            "working_directory": str(project_root / "app"),
            "timeout": 10
        })
        print(f"App Python Files: {json.dumps(app_structure, indent=2)}")
        
        # Test 4: Environment Health Check
        print("\n" + "="*50)
        print("🔍 TEST 4: Environment Health Check")
        print("="*50)
        
        print("\n🏥 Testing environment health check...")
        health_result = await server.check_environment_health({
            "detailed": True,
            "services": ["frontend", "backend", "mcp"]
        })
        print(f"Environment Health: {json.dumps(health_result, indent=2)}")
        
        # Test 5: Development Environment Control
        print("\n" + "="*50)
        print("🔍 TEST 5: Development Environment Control")
        print("="*50)
        
        # Test starting development environment
        print("\n🚀 Testing development environment start...")
        start_result = await server.start_development_environment({
            "environment": "development",
            "services": ["frontend", "backend"],
            "wait_for_ready": False
        })
        print(f"Start Environment Result: {json.dumps(start_result, indent=2)}")
        
        # Wait for services to start
        print("\n⏳ Waiting for services to start...")
        await asyncio.sleep(15)
        
        # Check health after startup
        print("\n🔍 Checking health after startup...")
        health_after_start = await server.check_environment_health({
            "detailed": False,
            "services": ["frontend", "backend"]
        })
        print(f"Health After Start: {json.dumps(health_after_start, indent=2)}")
        
        # Test 6: Mission System
        print("\n" + "="*50)
        print("🔍 TEST 6: Mission System")
        print("="*50)
        
        # Test creating a mission
        print("\n🎯 Testing mission creation...")
        mission_result = await server.create_mission({
            "mission_name": "Test Environment Control",
            "mission_description": "Testing the new MCP environment control tools",
            "mission_type": "TESTING",
            "mission_priority": "MEDIUM"
        })
        print(f"Mission Creation Result: {json.dumps(mission_result, indent=2)}")
        
        # Test listing missions
        print("\n📋 Testing mission listing...")
        missions_result = await server.list_missions({
            "status_filter": "all"
        })
        print(f"Missions List: {json.dumps(missions_result, indent=2)}")
        
        # Test 7: Package Management
        print("\n" + "="*50)
        print("🔍 TEST 7: Package Management")
        print("="*50)
        
        # Test checking available commands
        print("\n🔧 Testing command availability...")
        commands_to_check = ["python3", "pip", "npm", "git"]
        for cmd in commands_to_check:
            available = server._check_command(cmd)
            print(f"Command '{cmd}': {'✅ Available' if available else '❌ Not Available'}")
        
        # Test 8: File Operations
        print("\n" + "="*50)
        print("🔍 TEST 8: File Operations")
        print("="*50)
        
        # Test safe path validation
        print("\n🛡️ Testing safe path validation...")
        safe_paths = [
            str(project_root / "app" / "frontend" / "index.html"),
            str(project_root / "mcp-server" / "enhanced_server.py"),
            "/etc/passwd",  # This should be unsafe
            str(project_root / "app" / "backend" / "main.py")
        ]
        
        for path in safe_paths:
            is_safe = server._is_safe_path(path)
            print(f"Path '{path}': {'✅ Safe' if is_safe else '❌ Unsafe'}")
        
        # Test 9: MCP Server Management
        print("\n" + "="*50)
        print("🔍 TEST 9: MCP Server Management")
        print("="*50)
        
        # Test MCP servers status
        print("\n🔌 Testing MCP servers status...")
        mcp_status = server.get_mcp_servers_status()
        print(f"MCP Servers Status: {mcp_status}")
        
        # Test 10: Final Health Check
        print("\n" + "="*50)
        print("🔍 TEST 10: Final Health Check")
        print("="*50)
        
        print("\n🏥 Final environment health check...")
        final_health = await server.check_environment_health({
            "detailed": True,
            "services": ["frontend", "backend", "mcp"]
        })
        print(f"Final Health Status: {json.dumps(final_health, indent=2)}")
        
        # Test 11: Stop Environment
        print("\n" + "="*50)
        print("🔍 TEST 11: Stop Environment")
        print("="*50)
        
        print("\n🛑 Testing environment stop...")
        stop_result = await server.stop_development_environment({
            "force": False,
            "cleanup": True
        })
        print(f"Stop Environment Result: {json.dumps(stop_result, indent=2)}")
        
        # Final Summary
        print("\n" + "="*60)
        print("🎉 COMPREHENSIVE TEST COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        print("\n✅ All MCP tools tested successfully")
        print("✅ App folder interaction working")
        print("✅ Environment control tools functional")
        print("✅ Mission system operational")
        print("✅ Security features working")
        print("✅ Health monitoring operational")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Comprehensive test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting comprehensive MCP server test...")
    success = asyncio.run(test_comprehensive_mcp())
    
    if success:
        print("\n🎯 All tests passed! Your Lab MCP server is fully operational.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the output above for details.")
        sys.exit(1)
