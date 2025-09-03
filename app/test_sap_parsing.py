#!/usr/bin/env python3
"""
Test script for SAP message parsing system
Demonstrates how user messages are structured into comprehensive JSON format
"""

import sys
import os
import json
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from core.message_parser import MessageParser

def test_message_parsing():
    """Test the SAP message parsing system with various scenarios"""
    
    # Initialize the message parser
    parser = MessageParser()
    
    # Test messages
    test_messages = [
        "Hi id like help reporting a theft from my coinbase account",
        "My Bitcoin wallet was hacked and I lost 2 BTC yesterday",
        "I need help with my account login",
        "There's a bug in the system that's causing errors",
        "How much does your service cost?",
        "I'm having trouble with my MetaMask wallet - someone stole my ETH"
    ]
    
    print("🧪 Testing SAP Message Parsing System")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: {message}")
        print("-" * 40)
        
        # Parse the message
        structured_message = parser.parse_message(message)
        
        # Display key information
        print(f"Message Type: {structured_message['message_type']}")
        print(f"Urgency Level: {structured_message['urgency_level']}")
        print(f"Primary Intent: {structured_message['intent_analysis']['primary_intent']}")
        print(f"Emotional State: {structured_message['intent_analysis']['emotional_state']}")
        
        # Show extracted entities
        entities = structured_message['extracted_entities']
        if any(entities.values()):
            print("Extracted Entities:")
            for entity_type, values in entities.items():
                if values:
                    print(f"  {entity_type}: {values}")
        
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
    
    print("\n" + "=" * 50)
    print("✅ SAP Message Parsing Test Complete!")
    
    # Show full JSON structure for one example
    print("\n📋 Full JSON Structure Example:")
    print("=" * 50)
    example_message = "My Bitcoin wallet was hacked and I lost 2 BTC yesterday"
    example_parsed = parser.parse_message(example_message)
    print(json.dumps(example_parsed, indent=2))

if __name__ == "__main__":
    test_message_parsing()
