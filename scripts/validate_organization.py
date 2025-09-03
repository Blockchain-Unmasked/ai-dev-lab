#!/usr/bin/env python3
"""
Repository Organization Validation Script
Validates that all files are properly organized and accessible
"""

import os
import json


def validate_directory_structure():
    """Validate the main directory structure"""
    print("🔍 Validating Directory Structure...")
    
    expected_dirs = [
        'docs',
        'projects', 
        'meta',
        'mcp-server',
        'app',
        'missions',
        'input',
        'scripts'
    ]
    
    missing_dirs = []
    for dir_name in expected_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    else:
        print("✅ All expected directories found")
        return True

def validate_docs_organization():
    """Validate docs directory organization"""
    print("\n📚 Validating Documentation Organization...")
    
    docs_subdirs = [
        'architecture',
        'setup', 
        'security',
        'missions',
        'cursor-integration',
        'research',
        'mcp-servers'
    ]
    
    missing_subdirs = []
    for subdir in docs_subdirs:
        if not os.path.exists(f"docs/{subdir}"):
            missing_subdirs.append(subdir)
    
    if missing_subdirs:
        print(f"❌ Missing docs subdirectories: {missing_subdirs}")
        return False
    else:
        print("✅ All docs subdirectories found")
        return True

def validate_projects_organization():
    """Validate projects directory organization"""
    print("\n🚀 Validating Projects Organization...")
    
    project_dirs = [
        'blockchainunmasked-audit',
        'enterprise-research'
    ]
    
    missing_projects = []
    for project in project_dirs:
        if not os.path.exists(f"projects/{project}"):
            missing_projects.append(project)
    
    if missing_projects:
        print(f"❌ Missing project directories: {missing_projects}")
        return False
    else:
        print("✅ All project directories found")
        return True

def validate_meta_organization():
    """Validate meta directory organization"""
    print("\n🧩 Validating Meta Documentation Organization...")
    
    meta_subdirs = [
        'decisions',
        'features',
        'checklists', 
        'schemas',
        'templates'
    ]
    
    missing_subdirs = []
    for subdir in meta_subdirs:
        if not os.path.exists(f"meta/{subdir}"):
            missing_subdirs.append(subdir)
    
    if missing_subdirs:
        print(f"❌ Missing meta subdirectories: {missing_subdirs}")
        return False
    else:
        print("✅ All meta subdirectories found")
        return True

def validate_index_files():
    """Validate that index files exist and are accessible"""
    print("\n📖 Validating Index Files...")
    
    index_files = [
        'docs/README.md',
        'projects/README.md', 
        'meta/README.md'
    ]
    
    missing_files = []
    for file_path in index_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing index files: {missing_files}")
        return False
    else:
        print("✅ All index files found")
        return True

def validate_root_cleanup():
    """Validate that root directory is properly cleaned up"""
    print("\n🧹 Validating Root Directory Cleanup...")
    
    # Count markdown files in root
    root_md_files = [f for f in os.listdir('.') if f.endswith('.md')]
    
    # Should only have a few essential files
    expected_root_files = [
        'README.md',
        'PROJECT_RENAME_SUMMARY.md', 
        'REPOSITORY_CLEANUP_AND_ORGANIZATION_SUMMARY.md'
    ]
    
    unexpected_files = [f for f in root_md_files if f not in expected_root_files]
    
    if unexpected_files:
        print(f"⚠️  Unexpected markdown files in root: {unexpected_files}")
        return False
    else:
        print("✅ Root directory properly cleaned up")
        return True

def validate_file_accessibility():
    """Validate that key files are accessible and readable"""
    print("\n🔓 Validating File Accessibility...")
    
    test_files = [
        'docs/README.md',
        'projects/README.md',
        'meta/README.md',
        'docs/architecture/MCP_SERVER_ARCHITECTURE_RULES.md',
        'projects/blockchainunmasked-audit/BLOCKCHAINUNMASKED_AUDIT_PRD.md'
    ]
    
    inaccessible_files = []
    for file_path in test_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) < 100:  # Basic content validation
                    inaccessible_files.append(f"{file_path} (too short)")
        except Exception as e:
            inaccessible_files.append(f"{file_path} ({str(e)})")
    
    if inaccessible_files:
        print(f"❌ Inaccessible files: {inaccessible_files}")
        return False
    else:
        print("✅ All test files accessible and readable")
        return True

def generate_organization_report():
    """Generate a comprehensive organization report"""
    print("\n📊 Generating Organization Report...")
    
    report = {
        "validation_date": "2025-08-26",
        "status": "Validating...",
        "directory_structure": validate_directory_structure(),
        "docs_organization": validate_docs_organization(),
        "projects_organization": validate_projects_organization(),
        "meta_organization": validate_meta_organization(),
        "index_files": validate_index_files(),
        "root_cleanup": validate_root_cleanup(),
        "file_accessibility": validate_file_accessibility()
    }
    
    # Determine overall status
    all_passed = all(report.values())
    report["status"] = "✅ PASSED" if all_passed else "❌ FAILED"
    
    # Save report
    with open('organization_validation_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📋 Organization Report: {report['status']}")
    print("📄 Report saved to: organization_validation_report.json")
    
    return report

def main():
    """Main validation function"""
    print("🏗️ AI/DEV Lab Repository Organization Validation")
    print("=" * 50)
    
    report = generate_organization_report()
    
    print("\n📈 Validation Summary:")
    print(f"✅ Directory Structure: {'PASS' if report['directory_structure'] else 'FAIL'}")
    print(f"✅ Documentation Organization: {'PASS' if report['docs_organization'] else 'FAIL'}")
    print(f"✅ Projects Organization: {'PASS' if report['projects_organization'] else 'FAIL'}")
    print(f"✅ Meta Documentation: {'PASS' if report['meta_organization'] else 'FAIL'}")
    print(f"✅ Index Files: {'PASS' if report['index_files'] else 'FAIL'}")
    print(f"✅ Root Cleanup: {'PASS' if report['root_cleanup'] else 'FAIL'}")
    print(f"✅ File Accessibility: {'PASS' if report['file_accessibility'] else 'FAIL'}")
    
    if report['status'] == "✅ PASSED":
        print("\n🎉 All validations passed! Repository is properly organized.")
    else:
        print("\n⚠️  Some validations failed. Please review the issues above.")
    
    return report['status'] == "✅ PASSED"

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
