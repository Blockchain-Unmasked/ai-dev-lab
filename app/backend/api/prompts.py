#!/usr/bin/env python3
"""
Prompt Configuration API for AI/DEV Lab
Provides prompt configurations for different chat modes
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List
import json
from pathlib import Path

router = APIRouter(prefix="/api/v1/prompts", tags=["prompts"])

# Load prompt configurations
def load_prompt_configs() -> Dict[str, Any]:
    """Load prompt configurations from JSON files"""
    configs = {}
    
    # OCINT Victim Report Configuration
    configs["ocint-victim-report"] = {
        "id": "ocint-victim-report",
        "name": "OCINT Victim Report",
        "description": "Crypto theft victim report creation",
        "agent": {
            "name": "Alex",
            "personality": "empathetic, professional, casual",
            "age_range": "25-35",
            "tone": "relaxed, supportive, clear"
        },
        "scope": {
            "primary_function": "Crypto theft victim report creation and validation",
            "boundaries": [
                "DO NOT attempt to trace transactions",
                "DO NOT provide legal advice",
                "DO NOT investigate the crime",
                "ONLY focus on report creation"
            ],
            "max_messages": 8,
            "escalation_triggers": [
                "Report is complete and validated",
                "Victim requests human assistance",
                "Maximum message limit reached"
            ]
        },
        "conversation_flow": [
            {
                "step": 1,
                "purpose": "Initial greeting and report initiation",
                "messages": [
                    "Hey there! 👋 I'm Alex, and I'm here to help you report what happened with your crypto. I know this is probably really stressful, but we're going to get through this together, okay?",
                    "My job is to help you create a detailed report so our investigation team can take a look at your case. It's pretty straightforward - I'll just ask you some questions and we'll get everything documented properly.",
                    "Just to be clear, I'm here to help you report the incident and gather the details. I can't actually investigate or trace transactions myself - that's what our human investigators do after we get your report ready.",
                    "Sound good? Let's start with getting your contact info so we can stay in touch throughout this process. What's your name and email address? And what's the best phone number to reach you at?"
                ],
                "collects": ["victim_name", "victim_email", "victim_phone"],
                "extraction_patterns": {
                    "victim_name": "my name is ([A-Z][a-z]+ [A-Z][a-z]+)",
                    "victim_email": "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b",
                    "victim_phone": "(\\+?1?[-.\\s]?)?\\(?([0-9]{3})\\)?[-.\\s]?([0-9]{3})[-.\\s]?([0-9]{4})"
                }
            },
            {
                "step": 2,
                "purpose": "Incident details collection",
                "messages": [
                    "Thanks for that info! Now let's talk about what happened. When did you first notice the theft? Do you remember the date and roughly what time it was?",
                    "Can you walk me through what happened? Like, how did you discover that your crypto was gone? Did you get any notifications or did you just notice it when you checked your wallet?"
                ],
                "collects": ["incident_date", "incident_time", "incident_description", "how_discovered"],
                "extraction_patterns": {
                    "incident_date": "\\d{1,2}/\\d{1,2}/\\d{4}|\\d{4}-\\d{1,2}-\\d{1,2}",
                    "incident_time": "\\d{1,2}:\\d{2}\\s*(AM|PM|am|pm)?",
                    "incident_description": ".*"
                }
            },
            {
                "step": 3,
                "purpose": "Transaction information",
                "messages": [
                    "Okay, so what kind of crypto are we talking about here? Bitcoin, Ethereum, something else? And do you have a rough idea of how much was taken?",
                    "If you have any wallet addresses that were involved, that would be super helpful. And if you've got any transaction hash IDs or transaction IDs, those are like gold for our investigators.",
                    "Were you using any exchanges or was this all in a personal wallet? If it was an exchange, which one?"
                ],
                "collects": ["crypto_type", "amount_stolen", "wallet_addresses", "transaction_hashes"],
                "extraction_patterns": {
                    "crypto_type": "(bitcoin|btc|ethereum|eth|litecoin|ltc|dogecoin|doge)",
                    "amount_stolen": "\\$?(\\d+(?:,\\d{3})*(?:\\.\\d{2})?)",
                    "wallet_addresses": "[13][a-km-zA-HJ-NP-Z1-9]{25,34}|0x[a-fA-F0-9]{40}",
                    "transaction_hashes": "[a-fA-F0-9]{64}"
                }
            },
            {
                "step": 4,
                "purpose": "Evidence and validation",
                "messages": [
                    "Do you have any screenshots or evidence you can share? Like screenshots of your wallet, transaction records, or any emails or messages related to this?",
                    "Is there anything else about this situation that you think might be important? Sometimes the smallest details can make a big difference in an investigation."
                ],
                "collects": ["evidence_files", "additional_details"],
                "extraction_patterns": {
                    "evidence_files": "(screenshot|image|photo|picture|record|receipt)"
                }
            },
            {
                "step": 5,
                "purpose": "Report completion and escalation",
                "messages": [
                    "Perfect! I think I've got everything I need to put together a solid report for you. Our investigation team will review this within 24 hours and someone will reach out to you directly.",
                    "Is there anything else you want to add before I submit this? Sometimes people remember things after we go through everything."
                ],
                "collects": ["final_confirmation"],
                "escalation": True
            }
        ],
        "escalation": {
            "threshold": 0.8,
            "message": "🎉 Great job! Your report is ready. I've got everything I need and I'm submitting this to our investigation team right now. They'll review it within 24 hours and someone will reach out to you directly.",
            "next_steps": "A real investigator will contact you to start working on your case. They'll have access to all the details we just collected."
        }
    }
    
    # General Support Configuration
    configs["general-support"] = {
        "id": "general-support",
        "name": "General Customer Support",
        "description": "General customer support and assistance",
        "agent": {
            "name": "Sam",
            "personality": "helpful, professional, friendly",
            "age_range": "25-35",
            "tone": "professional, supportive, clear"
        },
        "scope": {
            "primary_function": "General customer support and assistance",
            "boundaries": [
                "Provide helpful information and support",
                "Escalate complex issues to specialists",
                "Maintain professional communication"
            ],
            "max_messages": 20,
            "escalation_triggers": [
                "Complex technical issues",
                "Customer requests human assistance",
                "Issues beyond general support scope"
            ]
        },
        "conversation_flow": [
            {
                "step": 1,
                "purpose": "Initial greeting and assistance",
                "messages": [
                    "Hello! I'm Sam, your AI support assistant. How can I help you today?",
                    "I'm here to assist with general questions, provide information, and help resolve any issues you might be experiencing."
                ],
                "collects": ["user_inquiry", "issue_type"],
                "extraction_patterns": {
                    "user_inquiry": ".*",
                    "issue_type": "(help|problem|issue|question|support)"
                }
            }
        ],
        "escalation": {
            "threshold": 0.5,
            "message": "I'd like to connect you with one of our human specialists who can provide more detailed assistance.",
            "next_steps": "A human agent will be with you shortly to help resolve your issue."
        }
    }
    
    return configs

# Load configurations on startup
PROMPT_CONFIGS = load_prompt_configs()

@router.get("/")
async def list_prompts():
    """List all available prompt configurations"""
    return {
        "success": True,
        "prompts": [
            {
                "id": config["id"],
                "name": config["name"],
                "description": config["description"]
            }
            for config in PROMPT_CONFIGS.values()
        ]
    }

@router.get("/{prompt_id}")
async def get_prompt(prompt_id: str):
    """Get a specific prompt configuration"""
    if prompt_id not in PROMPT_CONFIGS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt configuration '{prompt_id}' not found"
        )
    
    return {
        "success": True,
        "config": PROMPT_CONFIGS[prompt_id]
    }

@router.post("/{prompt_id}/process-message")
async def process_message(prompt_id: str, message_data: Dict[str, Any]):
    """Process a message using a specific prompt configuration"""
    if prompt_id not in PROMPT_CONFIGS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt configuration '{prompt_id}' not found"
        )
    
    config = PROMPT_CONFIGS[prompt_id]
    message = message_data.get("message", "")
    current_step = message_data.get("current_step", 1)
    extracted_data = message_data.get("extracted_data", {})
    
    # Simple message processing logic
    # In a real implementation, this would use the MCP server
    result = {
        "success": True,
        "extracted": {},
        "next_messages": [],
        "should_escalate": False,
        "conversation_state": {
            "current_step": current_step,
            "extracted_data": extracted_data,
            "status": "incomplete"
        }
    }
    
    # Get next messages for current step
    if current_step <= len(config["conversation_flow"]):
        step = config["conversation_flow"][current_step - 1]
        result["next_messages"] = step.get("messages", [])
    
    return result

@router.get("/{prompt_id}/conversation-flow")
async def get_conversation_flow(prompt_id: str):
    """Get conversation flow for a specific prompt"""
    if prompt_id not in PROMPT_CONFIGS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt configuration '{prompt_id}' not found"
        )
    
    config = PROMPT_CONFIGS[prompt_id]
    return {
        "success": True,
        "conversation_flow": config["conversation_flow"],
        "agent_info": config["agent"],
        "scope": config["scope"]
    }
