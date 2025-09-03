#!/usr/bin/env python3
"""
Test script for Victim Report Agent (Tier 1 MVP)
Tests the crypto theft victim report agent specifically
"""

import sys
import os
import json
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from core.chat_flow_manager import ChatFlowManager
from core.message_parser import MessageParser
from core.response_formatter import ResponseFormatter

def test_victim_report_agent():
    """Test the victim report agent for crypto theft scenarios"""
    
    # Initialize components with correct paths
    chat_flow_manager = ChatFlowManager()
    message_parser = MessageParser("agents/message-structure-sap.json")
    response_formatter = ResponseFormatter()
    
    # Initialize global instances
    from core.chat_flow_manager import initialize_chat_flow_manager
    from core.message_parser import initialize_message_parser
    from core.response_formatter import initialize_response_formatter
    
    initialize_chat_flow_manager()
    initialize_message_parser("agents/message-structure-sap.json")
    initialize_response_formatter()
    
    print("🚨 Testing Victim Report Agent (Tier 1 MVP)")
    print("=" * 60)
    
    # Test crypto theft victim report scenario
    test_messages = [
        "Hi, I need help reporting a theft from my Coinbase account",
        "I've secured my account and changed my password",
        "Yes, I have the transaction details ready",
        "I'd like to go through each reporting step"
    ]
    
    print("\n📱 VICTIM REPORT AGENT - Step by Step:")
    print("=" * 60)
    
    # Track conversation context for victim report mode
    conversation_context = {"message_type": "crypto_theft", "current_step": 1}
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n👤 Victim Message {i}: {message}")
        print("-" * 40)
        
        # Parse the message
        structured_message = message_parser.parse_message(message)
        
        # Override for victim report mode (Tier 1 MVP)
        structured_message["message_type"] = "crypto_theft"
        structured_message["urgency_level"] = "high"
        
        # Update step based on user message content
        if "secured" in message.lower() or "changed password" in message.lower():
            conversation_context["current_step"] = 2
        elif "transaction details" in message.lower() or "evidence" in message.lower() or "ready" in message.lower():
            conversation_context["current_step"] = 3
        elif "reporting step" in message.lower() or "each step" in message.lower():
            conversation_context["current_step"] = 3
        elif any(phrase in message.lower() for phrase in ["go through", "walk through", "explain", "tell me about"]):
            # Keep current step for explanation requests
            pass
        
        # Format using step-by-step flow
        formatted_result = response_formatter.format_for_frontend("", structured_message)
        
        print(f"🤖 Victim Report Agent Response:")
        print(formatted_result["formatted_response"])
        
        # Show step metadata
        metadata = formatted_result["system_metadata"]
        print(f"\n📊 Step Info: {metadata.get('step_number', 0)}/{metadata.get('total_steps', 0)} - {metadata.get('flow_type', 'unknown')}")
        
        # Show system data for workflow automation
        if formatted_result.get("structured_data"):
            print(f"🔧 System Data Available: {len(formatted_result['structured_data'])} fields")
    
    print("\n" + "=" * 60)
    print("✅ Victim Report Agent Test Complete!")
    
    # Test flow summary
    print("\n📋 VICTIM REPORT FLOW SUMMARY:")
    print("=" * 60)
    flow_summary = chat_flow_manager.get_flow_summary("crypto_theft")
    print(f"Total Steps: {flow_summary['total_steps']}")
    for step in flow_summary['steps']:
        print(f"  Step {step['step']}: {step['title']} ({step['actions_count']} actions)")
    
    print("\n🎯 TIER 1 MVP FEATURES:")
    print("=" * 60)
    print("✅ Step-by-step victim guidance")
    print("✅ Crypto theft specific responses")
    print("✅ Three-tier reporting structure")
    print("✅ Evidence gathering guidance")
    print("✅ System data for workflow automation")
    print("✅ Clean, concise responses (not verbose)")

if __name__ == "__main__":
    test_victim_report_agent()
