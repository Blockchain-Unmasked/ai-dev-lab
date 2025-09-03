#!/usr/bin/env python3
"""
Guardian Security System Test Script
Tests the guardian configuration and security policies for AI/DEV Lab
"""

import yaml
import json
import sys
from pathlib import Path

def test_guardian_config():
    """Test guardian configuration file"""
    config_path = Path("mcp-server/guardian_config.yaml")
    
    if not config_path.exists():
        print("❌ Guardian config file not found")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Test required sections
        required_sections = ['server', 'security', 'approval_gates', 'policies', 'logging']
        for section in required_sections:
            if section not in config:
                print(f"❌ Missing required section: {section}")
                return False
        
        # Test security settings
        if config['security']['security_mode'] != 'strict':
            print("❌ Security mode should be 'strict'")
            return False
        
        if not config['security']['approval_required']:
            print("❌ Approval should be required")
            return False
        
        print("✅ Guardian configuration is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error reading guardian config: {e}")
        return False

def test_project_structure():
    """Test that project structure follows security guidelines"""
    required_dirs = [
        '.cursor',
        'mcp-server',
        'meta',
        'docs',
        'sandbox',
        'scripts',
        'references',
        'tests',
        'missions'
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Missing required directories: {missing_dirs}")
        return False
    
    print("✅ Project structure is valid")
    return True

def test_security_boundaries():
    """Test that security boundaries are properly configured"""
    # Check that venv directories are not tracked (excluding system typeshed)
    venv_dirs = [d for d in Path('.').rglob('venv') 
                 if not str(d).endswith('.venv/lib/python3.13/site-packages/mypy/typeshed/stdlib/venv')]
    if venv_dirs:
        print(f"❌ Found venv directories that should be removed: {venv_dirs}")
        return False
    
    # Check that database files are not tracked
    db_files = list(Path('.').rglob('*.db'))
    if db_files:
        print(f"❌ Found database files that should be ignored: {db_files}")
        return False
    
    print("✅ Security boundaries are properly configured")
    return True

def main():
    """Run all guardian tests"""
    print("🔒 Running Guardian Security Tests...")
    print("=" * 50)
    
    tests = [
        test_guardian_config,
        test_project_structure,
        test_security_boundaries
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All guardian tests passed!")
        return 0
    else:
        print("❌ Some guardian tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
