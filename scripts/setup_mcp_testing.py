#!/usr/bin/env python3
"""
Setup script for MCP testing environment
Installs required dependencies and prepares testing tools
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up MCP testing environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Install MCP Python SDK
    if not run_command(
        "pip install mcp", 
        "Installing MCP Python SDK"
    ):
        print("❌ Failed to install MCP SDK")
        sys.exit(1)
    
    # Install additional testing dependencies
    dependencies = [
        "aiohttp",
        "asyncio-mqtt", 
        "websockets",
        "PyYAML"  # For Cursor rules verification
    ]
    
    for dep in dependencies:
        if not run_command(
            f"pip install {dep}", 
            f"Installing {dep}"
        ):
            print(f"⚠️  Warning: Failed to install {dep}")
    
    # Create test directories
    test_dirs = [
        "test_results",
        "logs/mcp_tests"
    ]
    
    for test_dir in test_dirs:
        Path(test_dir).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {test_dir}")
    
    # Check MCP server availability
    print("\n🔍 Checking MCP server availability...")
    
    lab_server = Path("mcp-server/server.py")
    if lab_server.exists():
        print(f"✅ Lab server found: {lab_server}")
    else:
        print(f"⚠️  Lab server not found: {lab_server}")
    
    app_servers = [
        "app-demo-server",
        "database-server",
        "website-audit", 
        "content-archive"
    ]
    
    for app_server in app_servers:
        server_path = Path(f"app/mcp-servers/{app_server}/server.py")
        if server_path.exists():
            print(f"✅ App server found: {app_server}")
        else:
            print(f"⚠️  App server not found: {app_server}")
    
    print("\n🎯 Setup complete! You can now run:")
    print("   python scripts/mcp_conformance_test_suite.py --all")


if __name__ == "__main__":
    main()
