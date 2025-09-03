#!/usr/bin/env python3
"""
AI/DEV Lab - Cursor IDE Integration Test Suite
Tests all Cursor IDE integrations including MCP server, dual-mode, and AI features.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List

class CursorIntegrationTester:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.cursor_dir = self.project_root / ".cursor"
        self.mcp_dir = self.project_root / "mcp-server"
        self.app_dir = self.project_root / "app"
        
    def test_cursor_configuration(self) -> bool:
        """Test Cursor IDE configuration files."""
        print("🔧 Testing Cursor IDE Configuration...")
        
        required_files = [
            ".cursor/environment.json",
            ".cursor/mcp.json", 
            ".cursor/settings.json",
            ".cursor/rules/free_mode.mdc",
            ".cursor/rules/enterprise_mode.mdc"
        ]
        
        all_exist = True
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} - MISSING")
                all_exist = False
        
        return all_exist
    
    def test_mcp_server_config(self) -> bool:
        """Test MCP server configuration."""
        print("\n🔌 Testing MCP Server Configuration...")
        
        # Test MCP server files
        mcp_files = [
            "mcp-server/server.py",
            "mcp-server/config.yaml",
            "mcp-server/guardian_config.yaml"
        ]
        
        all_exist = True
        for file_path in mcp_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} - MISSING")
                all_exist = False
        
        # Test MCP server functionality
        try:
            result = subprocess.run(
                [sys.executable, "scripts/test_mcp_server.py"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30
            )
            
            if result.returncode == 0:
                print("  ✅ MCP server functionality test passed")
                return all_exist
            else:
                print(f"  ❌ MCP server functionality test failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("  ❌ MCP server test timed out")
            return False
        except Exception as e:
            print(f"  ❌ MCP server test error: {e}")
            return False
    
    def test_web_app_structure(self) -> bool:
        """Test web application structure."""
        print("\n🌐 Testing Web Application Structure...")
        
        required_dirs = [
            "app/frontend",
            "app/backend", 
            "app/shared",
            "app/database",
            "app/deployment",
            "app/docs"
        ]
        
        required_files = [
            "app/README.md",
            "app/ARCHITECTURE_OVERVIEW.md",
            "app/start_dev.sh",
            "app/frontend/index.html",
            "app/backend/main.py",
            "app/backend/requirements.txt"
        ]
        
        all_exist = True
        
        # Test directories
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                print(f"  ✅ {dir_path}/")
            else:
                print(f"  ❌ {dir_path}/ - MISSING")
                all_exist = False
        
        # Test files
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} - MISSING")
                all_exist = False
        
        return all_exist
    
    def test_dual_mode_functionality(self) -> bool:
        """Test dual-mode switching functionality."""
        print("\n🔄 Testing Dual-Mode Functionality...")
        
        try:
            # Test mode switching script
            result = subprocess.run(
                [sys.executable, "scripts/switch_mode.py", "free"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=10
            )
            
            if result.returncode == 0:
                print("  ✅ Mode switching script (free mode)")
            else:
                print(f"  ❌ Mode switching script failed: {result.stderr}")
                return False
            
            # Test enterprise mode
            result = subprocess.run(
                [sys.executable, "scripts/switch_mode.py", "enterprise"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=10
            )
            
            if result.returncode == 0:
                print("  ✅ Mode switching script (enterprise mode)")
                return True
            else:
                print(f"  ❌ Mode switching script failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"  ❌ Mode switching test error: {e}")
            return False
    
    def test_guardian_integration(self) -> bool:
        """Test Guardian security integration."""
        print("\n🔒 Testing Guardian Security Integration...")
        
        guardian_config = self.project_root / "mcp-server/guardian_config.yaml"
        if guardian_config.exists():
            print("  ✅ Guardian configuration file exists")
            
            # Check if Guardian config has required settings
            try:
                with open(guardian_config, 'r') as f:
                    content = f.read()
                    if "security_mode:" in content and "approval_required:" in content:
                        print("  ✅ Guardian security settings configured")
                        return True
                    else:
                        print("  ⚠️  Guardian security settings may be incomplete")
                        return False
            except Exception as e:
                print(f"  ❌ Error reading Guardian config: {e}")
                return False
        else:
            print("  ❌ Guardian configuration file missing")
            return False
    
    def test_cursor_rules(self) -> bool:
        """Test Cursor rules and AI behavior configuration."""
        print("\n📋 Testing Cursor Rules and AI Configuration...")
        
        rules_dir = self.project_root / ".cursor/rules"
        if not rules_dir.exists():
            print("  ❌ Cursor rules directory missing")
            return False
        
        # Check rule files
        rule_files = ["free_mode.mdc", "enterprise_mode.mdc"]
        all_exist = True
        
        for rule_file in rule_files:
            rule_path = rules_dir / rule_file
            if rule_path.exists():
                print(f"  ✅ {rule_file}")
                
                # Check if rules have content
                try:
                    with open(rule_path, 'r') as f:
                        content = f.read()
                        if len(content.strip()) > 100:  # Basic content check
                            print(f"    ✅ {rule_file} has substantial content")
                        else:
                            print(f"    ⚠️  {rule_file} may be incomplete")
                            all_exist = False
                except Exception as e:
                    print(f"    ❌ Error reading {rule_file}: {e}")
                    all_exist = False
            else:
                print(f"  ❌ {rule_file} - MISSING")
                all_exist = False
        
        return all_exist
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run all integration tests."""
        print("🧪 AI/DEV Lab - Cursor IDE Integration Test Suite")
        print("=" * 60)
        
        results = {}
        
        # Run all tests
        results["cursor_config"] = self.test_cursor_configuration()
        results["mcp_server"] = self.test_mcp_server_config()
        results["web_app"] = self.test_web_app_structure()
        results["dual_mode"] = self.test_dual_mode_functionality()
        results["guardian"] = self.test_guardian_integration()
        results["cursor_rules"] = self.test_cursor_rules()
        
        # Calculate overall success
        total_tests = len(results)
        passed_tests = sum(results.values())
        success_rate = (passed_tests / total_tests) * 100
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎯 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nOverall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
        
        if success_rate == 100:
            print("\n🎉 ALL TESTS PASSED! Cursor IDE is fully configured and ready.")
            print("🚀 You can now use all AI/DEV Lab features within Cursor.")
        elif success_rate >= 80:
            print("\n⚠️  MOST TESTS PASSED. Some features may need attention.")
        else:
            print("\n❌ MANY TESTS FAILED. Please review the configuration.")
        
        return results

def main():
    """Main test execution."""
    tester = CursorIntegrationTester()
    results = tester.run_comprehensive_test()
    
    # Exit with appropriate code
    success_rate = (sum(results.values()) / len(results)) * 100
    if success_rate >= 80:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()
