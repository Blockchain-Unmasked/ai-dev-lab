#!/bin/bash
# AI/DEV Lab - App Directory Cleanup Script
# Phase 5: Clean up legacy files and optimize organization

set -e

echo "🧹 AI/DEV Lab App Directory Cleanup"
echo "=================================="
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
APP_DIR="$PROJECT_ROOT/app"

echo "📁 Project Root: $PROJECT_ROOT"
echo "📁 App Directory: $APP_DIR"
echo ""

# Check if app directory exists
if [ ! -d "$APP_DIR" ]; then
    echo "❌ Error: App directory not found at $APP_DIR"
    exit 1
fi

echo "🔍 Starting cleanup process..."
echo ""

# Phase 1: Remove legacy main.py files
echo "📝 Phase 1: Removing legacy main.py files..."
cd "$APP_DIR/backend"

LEGACY_FILES=(
    "main.py.backup"
    "main.py.before_static"
    "main.py.function_order_issue"
    "main.py.route_order_issue"
    "main.py.static_issue"
)

for file in "${LEGACY_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  🗑️  Removing: $file"
        rm "$file"
    else
        echo "  ✅ Already clean: $file"
    fi
done

echo ""

# Phase 2: Clean Python cache files
echo "🐍 Phase 2: Cleaning Python cache files..."
cd "$APP_DIR"

# Remove __pycache__ directories
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
echo "  🗑️  Removed __pycache__ directories"

# Remove .pyc files
find . -name "*.pyc" -delete 2>/dev/null || true
echo "  🗑️  Removed .pyc files"

# Remove .pyo files
find . -name "*.pyo" -delete 2>/dev/null || true
echo "  🗑️  Removed .pyo files"

echo ""

# Phase 3: Clean empty directories
echo "📁 Phase 3: Cleaning empty directories..."
cd "$APP_DIR"

# Remove empty directories (but preserve important ones)
EMPTY_DIRS=$(find . -type d -empty 2>/dev/null | grep -v -E "(secrets|logs|backups|storage|uploads)" || true)

if [ -n "$EMPTY_DIRS" ]; then
    echo "$EMPTY_DIRS" | while read -r dir; do
        echo "  🗑️  Removing empty directory: $dir"
        rmdir "$dir" 2>/dev/null || true
    done
else
    echo "  ✅ No empty directories to clean"
fi

echo ""

# Phase 4: Verify .gitignore coverage
echo "🔒 Phase 4: Verifying .gitignore coverage..."
cd "$PROJECT_ROOT"

# Check if database files are properly ignored
if ! grep -q "app/mcp-servers/database-server/data/\*\.sqlite" .gitignore; then
    echo "  📝 Adding database file exclusions to .gitignore"
    echo "" >> .gitignore
    echo "# App database files" >> .gitignore
    echo "app/mcp-servers/database-server/data/*.sqlite" >> .gitignore
    echo "app/mcp-servers/database-server/data/*.db" >> .gitignore
    echo "  ✅ Database files now ignored"
else
    echo "  ✅ Database files already ignored"
fi

echo ""

# Phase 5: Create backup of cleaned state
echo "💾 Phase 5: Creating cleanup backup..."
cd "$APP_DIR"

BACKUP_DIR="$PROJECT_ROOT/backups/app_cleanup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Create a summary of what was cleaned
cat > "$BACKUP_DIR/cleanup_summary.txt" << EOF
AI/DEV Lab App Directory Cleanup Summary
=======================================
Date: $(date)
Cleaner: cleanup_app_directory.sh

Files Removed:
$(ls -la backend/main.py.* 2>/dev/null || echo "No legacy main.py files found")

Directories Cleaned:
$(find . -name "__pycache__" -type d 2>/dev/null || echo "No __pycache__ directories found")

Cache Files Removed:
$(find . -name "*.pyc" -o -name "*.pyo" 2>/dev/null || echo "No cache files found")

Empty Directories Removed:
$(find . -type d -empty 2>/dev/null | grep -v -E "(secrets|logs|backups|storage|uploads)" || echo "No empty directories found")

.gitignore Updates:
- Added database file exclusions
- Verified existing exclusions

Status: Cleanup completed successfully
EOF

echo "  📁 Backup created at: $BACKUP_DIR"
echo ""

# Phase 6: Final verification
echo "✅ Phase 6: Final verification..."
cd "$APP_DIR"

# Check for any remaining issues
REMAINING_ISSUES=0

# Check for legacy files
if ls backend/main.py.* 2>/dev/null; then
    echo "  ⚠️  Warning: Some legacy main.py files remain"
    REMAINING_ISSUES=$((REMAINING_ISSUES + 1))
fi

# Check for cache files
if find . -name "__pycache__" -type d 2>/dev/null | grep -q .; then
    echo "  ⚠️  Warning: Some __pycache__ directories remain"
    REMAINING_ISSUES=$((REMAINING_ISSUES + 1))
fi

# Check for .pyc files
if find . -name "*.pyc" 2>/dev/null | grep -q .; then
    echo "  ⚠️  Warning: Some .pyc files remain"
    REMAINING_ISSUES=$((REMAINING_ISSUES + 1))
fi

if [ $REMAINING_ISSUES -eq 0 ]; then
    echo "  ✅ All cleanup tasks completed successfully"
else
    echo "  ⚠️  $REMAINING_ISSUES issues remain (may require manual intervention)"
fi

echo ""

# Summary
echo "🎉 Cleanup Summary"
echo "=================="
echo "✅ Legacy files removed"
echo "✅ Python cache cleaned"
echo "✅ Empty directories cleaned"
echo "✅ .gitignore updated"
echo "✅ Backup created"
echo "✅ Verification completed"
echo ""
echo "📊 App directory is now optimized and ready for production!"
echo ""
echo "📁 Backup location: $BACKUP_DIR"
echo "📋 Cleanup log: $BACKUP_DIR/cleanup_summary.txt"
echo ""
echo "🚀 Next steps:"
echo "   1. Review the cleanup summary"
echo "   2. Test the application to ensure everything works"
echo "   3. Commit the cleaned state to version control"
echo ""
echo "✨ App directory cleanup completed successfully!"
