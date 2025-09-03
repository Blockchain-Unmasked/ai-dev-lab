#!/usr/bin/env python3
"""
Test script for Chat Flow Manager
Demonstrates step-by-step user guidance for crypto theft scenarios
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

def test_chat_flow():
    """Test the step-by-step chat flow system"""
    
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
    
    print("🧪 Testing Step-by-Step Chat Flow System")
    print("=" * 60)
    
    # Test crypto theft scenario
    test_messages = [
        "Hi id like help reporting a theft from my coinbase account",
        "I've secured my account and changed my password",
        "Yes, I have the transaction details ready",
        "I'd like to go through each reporting step"
    ]
    
    print("\n📱 CRYPTO THEFT SCENARIO - Step by Step:")
    print("=" * 60)
    
    # Track conversation context
    conversation_context = {"message_type": "crypto_theft", "current_step": 1}
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n👤 User Message {i}: {message}")
        print("-" * 40)
        
        # Parse the message
        structured_message = message_parser.parse_message(message)
        
        # Override message type to maintain conversation context for step-by-step flow
        if conversation_context["message_type"] == "crypto_theft":
            structured_message["message_type"] = "crypto_theft"
            # Update step based on user message content
            if "secured" in message.lower() or "changed password" in message.lower():
                conversation_context["current_step"] = 2
            elif "transaction details" in message.lower() or "evidence" in message.lower() or "ready" in message.lower():
                conversation_context["current_step"] = 3
            elif "reporting step" in message.lower() or "each step" in message.lower():
                conversation_context["current_step"] = 3
            # Don't reset step for continuation messages
            elif any(phrase in message.lower() for phrase in ["go through", "walk through", "explain", "tell me about"]):
                # Keep current step for explanation requests
                pass
        
        # Debug output (commented out for clean output)
        # print(f"🔍 Parsed Message Type: {structured_message.get('message_type', 'unknown')}")
        # print(f"🔍 Urgency Level: {structured_message.get('urgency_level', 'unknown')}")
        # print(f"🔍 Current Step: {conversation_context['current_step']}")
        
        # Format using step-by-step flow
        formatted_result = response_formatter.format_for_frontend("", structured_message)
        
        print(f"🤖 AI Response:")
        print(formatted_result["formatted_response"])
        
        # Show step metadata
        metadata = formatted_result["system_metadata"]
        print(f"\n📊 Step Info: {metadata.get('step_number', 0)}/{metadata.get('total_steps', 0)} - {metadata.get('flow_type', 'unknown')}")
    
    print("\n" + "=" * 60)
    print("✅ Step-by-Step Chat Flow Test Complete!")
    
    # Test flow summary
    print("\n📋 FLOW SUMMARY:")
    print("=" * 60)
    flow_summary = chat_flow_manager.get_flow_summary("crypto_theft")
    print(f"Total Steps: {flow_summary['total_steps']}")
    for step in flow_summary['steps']:
        print(f"  Step {step['step']}: {step['title']} ({step['actions_count']} actions)")

if __name__ == "__main__":
    test_chat_flow()
