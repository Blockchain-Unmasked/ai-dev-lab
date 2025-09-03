#!/bin/bash
# Safety Scan Script for AI/DEV Lab
# Performs comprehensive security and safety checks

set -e

echo "🔒 AI/DEV Lab Safety Scan"
echo "========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "PASS")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "FAIL")
            echo -e "${RED}❌ $message${NC}"
            ;;
        "WARN")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
    esac
}

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d ".cursor" ]; then
    print_status "FAIL" "Not in AI/DEV Lab root directory"
    exit 1
fi

print_status "PASS" "Running in correct directory"

# Check for unwanted files
echo ""
echo "📁 Checking for unwanted files..."

# Check for venv directories (excluding system typeshed)
venv_count=$(find . -name "venv" -type d -not -path "*/.venv/lib/python*/site-packages/mypy/typeshed/stdlib/venv" | wc -l)
if [ $venv_count -gt 0 ]; then
    print_status "FAIL" "Found $venv_count venv directories (should be removed)"
    find . -name "venv" -type d -not -path "*/.venv/lib/python*/site-packages/mypy/typeshed/stdlib/venv"
else
    print_status "PASS" "No venv directories found"
fi

# Check for database files
db_count=$(find . -name "*.db" -type f | wc -l)
if [ $db_count -gt 0 ]; then
    print_status "WARN" "Found $db_count database files (should be in .gitignore)"
    find . -name "*.db" -type f
else
    print_status "PASS" "No database files found"
fi

# Check for log files in wrong locations
log_count=$(find . -maxdepth 1 -name "*.log" -type f | wc -l)
if [ $log_count -gt 0 ]; then
    print_status "WARN" "Found $log_count log files in root (should be in sandbox/)"
    find . -maxdepth 1 -name "*.log" -type f
else
    print_status "PASS" "No log files in root directory"
fi

# Check directory structure
echo ""
echo "🏗️  Checking directory structure..."

required_dirs=(".cursor" "mcp-server" "meta" "docs" "sandbox" "scripts" "references" "tests" "missions")
missing_dirs=()

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        print_status "PASS" "Directory $dir exists"
    else
        print_status "FAIL" "Directory $dir is missing"
        missing_dirs+=("$dir")
    fi
done

# Check .gitignore
echo ""
echo "📝 Checking .gitignore configuration..."

if [ -f ".gitignore" ]; then
    print_status "PASS" ".gitignore file exists"
    
    # Check for important exclusions
    if grep -q "venv/" .gitignore; then
        print_status "PASS" "venv/ is in .gitignore"
    else
        print_status "FAIL" "venv/ is not in .gitignore"
    fi
    
    if grep -q "*.db" .gitignore; then
        print_status "PASS" "*.db is in .gitignore"
    else
        print_status "FAIL" "*.db is not in .gitignore"
    fi
    
    if grep -q "logs/" .gitignore; then
        print_status "PASS" "logs/ is in .gitignore"
    else
        print_status "FAIL" "logs/ is not in .gitignore"
    fi
else
    print_status "FAIL" ".gitignore file is missing"
fi

# Check guardian configuration
echo ""
echo "🛡️  Checking guardian configuration..."

if [ -f "mcp-server/guardian_config.yaml" ]; then
    print_status "PASS" "Guardian config file exists"
    
    # Run Python guardian test if available
    if [ -f "scripts/test_guardian.py" ]; then
        echo "Running guardian tests..."
        if python3 scripts/test_guardian.py; then
            print_status "PASS" "Guardian tests passed"
        else
            print_status "FAIL" "Guardian tests failed"
        fi
    else
        print_status "WARN" "Guardian test script not found"
    fi
else
    print_status "FAIL" "Guardian config file is missing"
fi

# Summary
echo ""
echo "📊 Safety Scan Summary"
echo "======================"

if [ ${#missing_dirs[@]} -eq 0 ] && [ $venv_count -eq 0 ]; then
    print_status "PASS" "Safety scan completed successfully"
    echo ""
    echo "🎉 Repository structure is clean and secure!"
    exit 0
else
    print_status "FAIL" "Safety scan found issues that need attention"
    echo ""
    echo "🔧 Please address the issues above before proceeding"
    exit 1
fi
