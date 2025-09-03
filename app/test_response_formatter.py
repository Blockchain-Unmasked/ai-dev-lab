#!/usr/bin/env python3
"""
Test script for Response Formatter
Demonstrates how structured data is preserved for systems while providing user-friendly responses
"""

import sys
import os
import json
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from core.response_formatter import ResponseFormatter

def test_response_formatter():
    """Test the response formatter with structured and natural responses"""
    
    formatter = ResponseFormatter()
    
    # Test structured response
    structured_response = """```structured_response
{
  "greeting": "I understand you're reporting a theft from your Coinbase account. I'm here to help guide you through the necessary steps.",
  "immediate_security_steps": {
    "title": "Immediate Security Steps",
    "steps": [
      {
        "action": "Secure Your Account",
        "details": "Change your Coinbase password and enable 2FA immediately."
      },
      {
        "action": "Document Everything",
        "details": "Gather transaction IDs, wallet addresses, and timestamps."
      }
    ]
  },
  "reporting_structure_explanation": {
    "title": "Three-Tier Reporting Structure",
    "tiers": [
      {
        "name": "Tier 1: Law Enforcement (LEO)",
        "description": "File a police report with your local law enforcement agency."
      },
      {
        "name": "Tier 2: Service Provider (Coinbase)",
        "description": "Report the theft directly to Coinbase support."
      },
      {
        "name": "Tier 3: OCINT Investigation",
        "description": "Comprehensive investigation using specialized tools."
      }
    ]
  },
  "evidence_gathering_guidance": {
    "title": "Evidence Gathering",
    "details": "Collect transaction IDs, wallet addresses, timestamps, and screenshots."
  },
  "realistic_guidance": "Crypto theft recovery is challenging but we'll do everything possible to help."
}
```"""
    
    # Mock structured message context
    structured_message = {
        "message_type": "crypto_theft",
        "urgency_level": "high",
        "extracted_entities": {
            "service_providers": ["Coinbase"],
            "crypto_types": ["BTC"]
        },
        "context_requirements": {
            "required_workflows": ["security_first", "evidence_gathering", "three_tier_reporting"]
        }
    }
    
    print("🧪 Testing Response Formatter - Dual Purpose System")
    print("=" * 60)
    
    # Test formatting
    formatted_result = formatter.format_for_frontend(structured_response, structured_message)
    
    print("\n📱 USER-FRIENDLY RESPONSE:")
    print("-" * 40)
    print(formatted_result["formatted_response"])
    
    print("\n🔧 STRUCTURED DATA FOR SYSTEMS:")
    print("-" * 40)
    print(json.dumps(formatted_result["structured_data"], indent=2))
    
    print("\n📊 SYSTEM METADATA:")
    print("-" * 40)
    print(json.dumps(formatted_result["system_metadata"], indent=2))
    
    print("\n🎯 KEY BENEFITS:")
    print("-" * 40)
    print("✅ User gets clean, readable response")
    print("✅ Systems get structured data for processing")
    print("✅ Metadata enables workflow automation")
    print("✅ Context preserved for follow-up actions")
    
    # Test natural response
    natural_response = "I'm sorry to hear about the theft from your Coinbase account. Let me help you with the next steps."
    
    print("\n\n📝 TESTING NATURAL RESPONSE:")
    print("=" * 60)
    
    natural_result = formatter.format_for_frontend(natural_response, None)
    
    print("\n📱 USER-FRIENDLY RESPONSE:")
    print("-" * 40)
    print(natural_result["formatted_response"])
    
    print("\n🔧 STRUCTURED DATA FOR SYSTEMS:")
    print("-" * 40)
    print("None (natural response)")
    
    print("\n📊 SYSTEM METADATA:")
    print("-" * 40)
    print(json.dumps(natural_result["system_metadata"], indent=2))

if __name__ == "__main__":
    test_response_formatter()
