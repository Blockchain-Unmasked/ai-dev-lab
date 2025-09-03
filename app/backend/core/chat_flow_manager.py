#!/usr/bin/env python3
"""
Chat Flow Manager for Step-by-Step User Guidance
Breaks down complex responses into manageable, conversational steps
"""

import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ChatFlowManager:
    """Manages step-by-step chat flow for complex scenarios"""
    
    def __init__(self):
        self.flow_steps = {
            "crypto_theft": [
                {
                    "step": 1,
                    "title": "Immediate Security",
                    "content": "I'm so sorry to hear about the theft from your Coinbase account. This must be really stressful. Let's start by securing your account right away to prevent any further issues.",
                    "actions": [
                        "Change your Coinbase password immediately",
                        "Enable 2FA if not already active",
                        "Check for any unauthorized transactions"
                    ],
                    "next_step_prompt": "Once you've secured your account, let me know and I'll guide you through the next step."
                },
                {
                    "step": 2,
                    "title": "Evidence Gathering",
                    "content": "Great! Now let's gather the evidence we'll need for reporting. This information will be crucial for all the reporting steps.",
                    "actions": [
                        "Screenshot any unauthorized transactions",
                        "Note down transaction IDs and wallet addresses",
                        "Record the exact time and date of the theft"
                    ],
                    "next_step_prompt": "When you have this information ready, let me know and I'll explain the reporting process."
                },
                {
                    "step": 3,
                    "title": "Three-Tier Reporting",
                    "content": "Now I'll explain the three places you need to report this theft. Each serves a different purpose:",
                    "actions": [
                        "1. Local police - for the official crime report",
                        "2. Coinbase support - for their internal investigation", 
                        "3. OCINT investigation - for comprehensive analysis"
                    ],
                    "next_step_prompt": "Would you like me to walk you through each reporting step one by one?"
                }
            ],
            "general_support": [
                {
                    "step": 1,
                    "title": "Understanding Your Issue",
                    "content": "I'm here to help! Let me understand what's going on so I can provide the best assistance.",
                    "actions": [
                        "Describe the specific problem you're experiencing",
                        "Let me know when this started happening",
                        "Share any error messages you've seen"
                    ],
                    "next_step_prompt": "Once I understand the issue better, I'll guide you through the solution."
                }
            ]
        }
    
    def get_step_response(self, message_type: str, step_number: int, user_message: str = "") -> Dict[str, Any]:
        """Get a specific step response"""
        if message_type not in self.flow_steps:
            message_type = "general_support"
        
        steps = self.flow_steps[message_type]
        
        if step_number <= 0 or step_number > len(steps):
            return self._get_completion_response(message_type)
        
        current_step = steps[step_number - 1]
        
        return {
            "step_number": step_number,
            "total_steps": len(steps),
            "title": current_step["title"],
            "content": current_step["content"],
            "actions": current_step["actions"],
            "next_step_prompt": current_step["next_step_prompt"],
            "is_complete": False,
            "flow_type": message_type
        }
    
    def get_next_step(self, message_type: str, current_step: int) -> Dict[str, Any]:
        """Get the next step in the flow"""
        return self.get_step_response(message_type, current_step + 1)
    
    def _get_completion_response(self, message_type: str) -> Dict[str, Any]:
        """Get completion response when all steps are done"""
        if message_type == "crypto_theft":
            return {
                "step_number": 0,
                "total_steps": 0,
                "title": "Investigation Complete",
                "content": "You've completed all the initial steps! I'm here to help with any questions about the reporting process or next steps.",
                "actions": [],
                "next_step_prompt": "Feel free to ask me anything about the investigation or reporting process.",
                "is_complete": True,
                "flow_type": message_type
            }
        else:
            return {
                "step_number": 0,
                "total_steps": 0,
                "title": "Support Complete",
                "content": "I hope I was able to help resolve your issue!",
                "actions": [],
                "next_step_prompt": "Is there anything else I can help you with?",
                "is_complete": True,
                "flow_type": message_type
            }
    
    def should_continue_flow(self, user_message: str, current_step: int, message_type: str) -> bool:
        """Determine if user wants to continue the flow"""
        continue_indicators = [
            "yes", "continue", "next", "ready", "done", "finished", "ok", "okay",
            "let's go", "proceed", "next step", "what's next"
        ]
        
        user_lower = user_message.lower().strip()
        
        # Check for explicit continuation
        if any(indicator in user_lower for indicator in continue_indicators):
            return True
        
        # Check for step completion indicators
        completion_indicators = [
            "i've done", "i did", "completed", "finished", "secured", "changed password",
            "enabled 2fa", "gathered", "have the information", "ready for next"
        ]
        
        if any(indicator in user_lower for indicator in completion_indicators):
            return True
        
        return False
    
    def format_step_response(self, step_data: Dict[str, Any]) -> str:
        """Format step data into a conversational response"""
        response_parts = []
        
        # Add the main content
        response_parts.append(step_data["content"])
        
        # Add actions as a simple list
        if step_data["actions"]:
            response_parts.append("\nHere's what you need to do:")
            for i, action in enumerate(step_data["actions"], 1):
                response_parts.append(f"{i}. {action}")
        
        # Add next step prompt
        if step_data["next_step_prompt"]:
            response_parts.append(f"\n{step_data['next_step_prompt']}")
        
        return "\n".join(response_parts)
    
    def get_flow_summary(self, message_type: str) -> Dict[str, Any]:
        """Get a summary of the entire flow"""
        if message_type not in self.flow_steps:
            return {"total_steps": 0, "steps": []}
        
        steps = self.flow_steps[message_type]
        return {
            "total_steps": len(steps),
            "steps": [
                {
                    "step": step["step"],
                    "title": step["title"],
                    "actions_count": len(step["actions"])
                }
                for step in steps
            ]
        }

# Global chat flow manager instance
chat_flow_manager = None

def initialize_chat_flow_manager():
    """Initialize the global chat flow manager"""
    global chat_flow_manager
    chat_flow_manager = ChatFlowManager()
    return chat_flow_manager

def get_chat_flow_manager() -> Optional[ChatFlowManager]:
    """Get the global chat flow manager instance"""
    return chat_flow_manager
