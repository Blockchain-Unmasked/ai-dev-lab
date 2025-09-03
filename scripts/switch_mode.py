#!/usr/bin/env python3
"""
AI/DEV Lab - Cursor Mode Switching Utility
Allows users to switch between Free and Enterprise modes
"""

import json
import os
import sys
from pathlib import Path
from typing import Literal

ModeType = Literal["free", "enterprise"]

class CursorModeSwitcher:
    """Utility for switching between Cursor modes"""
    
    def __init__(self):
        self.project_root = Path.home() / "Code" / "ai-dev-lab"
        self.cursor_dir = self.project_root / ".cursor"
        self.environment_file = self.cursor_dir / "environment.json"
        self.rules_dir = self.cursor_dir / "rules"
        
    def get_current_mode(self) -> ModeType:
        """Get the current active mode"""
        if not self.environment_file.exists():
            return "free"
        
        try:
            with open(self.environment_file, 'r') as f:
                config = json.load(f)
            
            # Check if enterprise mode is active
            if config.get("cursor_settings", {}).get("dual_mode") == "enabled":
                # Check which mode is currently active
                if config.get("cursor_settings", {}).get("current_mode") == "enterprise":
                    return "enterprise"
                else:
                    return "free"
            else:
                return "free"
        except Exception as e:
            print(f"Error reading current mode: {e}")
            return "free"
    
    def switch_mode(self, target_mode: ModeType) -> bool:
        """Switch to the specified mode"""
        if not self.environment_file.exists():
            print("❌ Cursor environment file not found")
            return False
        
        try:
            # Read current configuration
            with open(self.environment_file, 'r') as f:
                config = json.load(f)
            
            # Update mode settings
            if "cursor_settings" not in config:
                config["cursor_settings"] = {}
            
            config["cursor_settings"]["current_mode"] = target_mode
            
            # Update mode-specific settings
            if target_mode == "enterprise":
                config["cursor_settings"]["background_agents"] = "enabled_with_approval"
                config["cursor_settings"]["max_context_length"] = "1M"
                config["cursor_settings"]["mcp_tools"] = "full"
                config["cursor_settings"]["approval_required"] = "comprehensive"
                print("🚀 Switching to Enterprise Mode - Full capabilities enabled")
            else:
                config["cursor_settings"]["background_agents"] = "disabled"
                config["cursor_settings"]["max_context_length"] = "100K"
                config["cursor_settings"]["mcp_tools"] = "limited"
                config["cursor_settings"]["approval_required"] = "minimal"
                print("⚡ Switching to Free Mode - Efficient, focused operations")
            
            # Write updated configuration
            with open(self.environment_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Update mode indicator in environment
            os.environ["CURSOR_MODE"] = target_mode.upper()
            
            print(f"✅ Successfully switched to {target_mode.title()} Mode")
            return True
            
        except Exception as e:
            print(f"❌ Error switching modes: {e}")
            return False
    
    def show_mode_info(self, mode: ModeType):
        """Display information about the specified mode"""
        if mode == "enterprise":
            print("""
🚀 Enterprise Mode - Full Capabilities
=====================================
• Background agents enabled (with approval)
• Large context windows (up to 1M tokens)
• Full MCP tool access
• Comprehensive approval workflows
• Advanced security features
• Team collaboration support

Perfect for:
- Complex architectural decisions
- Large-scale refactoring
- Background agent operations
- Comprehensive security reviews
- Team collaboration features
""")
        else:
            print("""
⚡ Free Mode - Efficient Operations
==================================
• Concise, focused responses
• Limited context usage (100K tokens)
• Essential MCP tools only
• Minimal approval requirements
• Fast, efficient operations
• Resource-optimized

Perfect for:
- Quick questions and clarifications
- Simple file edits and modifications
- Basic code reviews
- Documentation updates
- Simple configuration changes
""")
    
    def list_available_modes(self):
        """List all available modes with descriptions"""
        print("""
🎯 Available Cursor Modes
=========================

1. Free Mode (⚡)
   - Efficient, focused operations
   - Limited resource usage
   - Quick tasks and simple operations
   - No background agents

2. Enterprise Mode (🚀)
   - Comprehensive, thorough assistance
   - Full capabilities and features
   - Background agent support
   - Advanced security and compliance

Current Mode: {current_mode}
""".format(current_mode=self.get_current_mode().title()))
    
    def run_interactive(self):
        """Run the mode switcher interactively"""
        print("🎯 AI/DEV Lab - Cursor Mode Switcher")
        print("=" * 50)
        
        current_mode = self.get_current_mode()
        print(f"Current Mode: {current_mode.title()}")
        print()
        
        while True:
            print("Options:")
            print("1. Switch to Free Mode")
            print("2. Switch to Enterprise Mode")
            print("3. Show current mode info")
            print("4. List all modes")
            print("5. Exit")
            print()
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                if current_mode == "free":
                    print("Already in Free Mode")
                else:
                    self.switch_mode("free")
                    current_mode = "free"
            elif choice == "2":
                if current_mode == "enterprise":
                    print("Already in Enterprise Mode")
                else:
                    self.switch_mode("enterprise")
                    current_mode = "enterprise"
            elif choice == "3":
                self.show_mode_info(current_mode)
            elif choice == "4":
                self.list_available_modes()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
            
            print()

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line mode
        switcher = CursorModeSwitcher()
        target_mode = sys.argv[1].lower()
        
        if target_mode in ["free", "enterprise"]:
            switcher.switch_mode(target_mode)
        else:
            print("❌ Invalid mode. Use 'free' or 'enterprise'")
            print("Usage: python switch_mode.py [free|enterprise]")
    else:
        # Interactive mode
        switcher = CursorModeSwitcher()
        switcher.run_interactive()

if __name__ == "__main__":
    main()
