#!/usr/bin/env python3
"""
Test script for App-Specific SAP system
Demonstrates how the app SAP integrates with MCP context and structured messaging
"""

import sys
import os
import json
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from core.message_parser import MessageParser
from core.app_sap_loader import AppSAPLoader

def test_app_sap_system():
    """Test the App SAP system with MCP integration"""
    
    # Initialize the components
    message_parser = MessageParser()
    app_sap_loader = AppSAPLoader()
    
    # Test messages
    test_messages = [
        "Hi id like help reporting a theft from my coinbase account",
        "My Bitcoin wallet was hacked and I lost 2 BTC yesterday",
        "I need help with my account login",
        "Someone stole my ETH from my MetaMask wallet"
    ]
    
    print("🧪 Testing App-Specific SAP System with MCP Integration")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: {message}")
        print("-" * 50)
        
        # Parse the message
        structured_message = message_parser.parse_message(message)
        
        # Mock MCP context
        mcp_context = {
            "status": "active",
            "available_tools": ["crypto_analysis", "evidence_processing", "report_generation", "context_management"],
            "session_id": f"session_{structured_message.get('message_id', 'unknown')}",
            "integration_level": "standard"
        }
        
        # Generate app-specific prompt
        app_prompt = app_sap_loader.generate_app_prompt(
            user_message=message,
            structured_message=structured_message,
            mcp_context=mcp_context
        )
        
        # Display key information
        print(f"Message Type: {structured_message['message_type']}")
        print(f"Urgency Level: {structured_message['urgency_level']}")
        print(f"Primary Intent: {structured_message['intent_analysis']['primary_intent']}")
        print(f"Emotional State: {structured_message['intent_analysis']['emotional_state']}")
        
        # Show MCP integration
        print(f"MCP Status: {mcp_context['status']}")
        print(f"Available Tools: {', '.join(mcp_context['available_tools'])}")
        
        # Show three-tier analysis if applicable
        three_tier = structured_message.get('three_tier_analysis')
        if three_tier:
            print("Three-Tier Analysis:")
            print(f"  Is Crypto Theft: {three_tier['is_crypto_theft']}")
            print(f"  Service Provider: {three_tier['tier_2_service_provider']}")
            print(f"  Evidence Status: {three_tier['evidence_status']}")
        
        # Show response guidance
        guidance = structured_message['response_guidance']
        print("Response Guidance:")
        print(f"  Type: {guidance['response_type']}")
        print(f"  Tone: {guidance['tone_guidance']}")
        print(f"  Length: {guidance['length_guidance']}")
        
        # Show required workflows
        workflows = structured_message['context_requirements']['required_workflows']
        if workflows:
            print(f"  Required Workflows: {workflows}")
        
        print(f"  Processing Time: {structured_message['metadata']['processing_time_ms']}ms")
        
        # Show prompt length
        print(f"Generated Prompt Length: {len(app_prompt)} characters")
    
    print("\n" + "=" * 60)
    print("✅ App SAP System Test Complete!")
    
    # Show full prompt example for crypto theft
    print("\n📋 Full App SAP Prompt Example (Crypto Theft):")
    print("=" * 60)
    example_message = "My Bitcoin wallet was hacked and I lost 2 BTC yesterday"
    example_parsed = message_parser.parse_message(example_message)
    example_mcp_context = {
        "status": "active",
        "available_tools": ["crypto_analysis", "evidence_processing", "report_generation"],
        "session_id": "session_example_12345",
        "integration_level": "standard"
    }
    example_prompt = app_sap_loader.generate_app_prompt(
        user_message=example_message,
        structured_message=example_parsed,
        mcp_context=example_mcp_context
    )
    print(example_prompt)

if __name__ == "__main__":
    test_app_sap_system()
