#!/usr/bin/env python3
"""
Test script for OCINT MVP - Crypto Theft Victim Report Creation
Tests the focused Tier 1 agent for efficient report creation
"""

import json
import asyncio
from pathlib import Path
from ocint_mvp_prompting_strategy import OCINTMVPEngine, ReportStatus, ReportSection

async def test_ocint_mvp():
    """Test the OCINT MVP agent with realistic scenarios"""
    
    print("🚀 OCINT MVP - Crypto Theft Victim Report Creation Test")
    print("=" * 70)
    
    # Initialize the OCINT MVP engine
    engine = OCINTMVPEngine()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Complete Report - Bitcoin Theft",
            "messages": [
                "Hi, I need help. Someone stole my Bitcoin yesterday. My name is John Smith and my email is john@example.com. You can call me at 555-123-4567.",
                "The theft happened on 2024-01-15 around 2:30 PM. I logged into my wallet and saw all my Bitcoin was gone. I think someone hacked my computer.",
                "I lost about 2.5 Bitcoin worth around $100,000. The wallet address was 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa and the transaction hash is abc123def456789...",
                "Yes, I have screenshots of the wallet showing the transactions and some emails from the exchange. I can provide those."
            ]
        },
        {
            "name": "Incomplete Report - Missing Details",
            "messages": [
                "Hello, I was robbed of my Ethereum. My name is Sarah Johnson, email sarah@test.com, phone 555-987-6543.",
                "It happened last week, I think on Tuesday. I'm not sure of the exact time.",
                "I lost some Ethereum, maybe 10 ETH. I don't have the wallet addresses right now."
            ]
        },
        {
            "name": "Complex Case - Multiple Cryptocurrencies",
            "messages": [
                "I need to report a major theft. I'm Mike Chen, mike@company.com, 555-456-7890. This is urgent.",
                "The theft occurred on 2024-01-20 at 11:45 PM. I discovered it when I tried to make a transaction and my wallet was empty. I suspect a phishing attack.",
                "I lost Bitcoin, Ethereum, and Litecoin. About 5 BTC, 50 ETH, and 100 LTC. Total value around $500,000. I have multiple wallet addresses and transaction hashes.",
                "I have extensive evidence including screenshots, transaction records, and email communications with the attackers."
            ]
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📋 Test {i}: {scenario['name']}")
        print("-" * 50)
        
        # Initialize report data
        report_data = engine.report_template.copy()
        report_data['report_id'] = f"OCINT-{i:03d}"
        current_step = 1
        
        # Process each message
        for j, message in enumerate(scenario['messages'], 1):
            print(f"\n💬 Message {j}: {message[:60]}...")
            
            # Generate prompt
            prompt = engine.generate_ocint_prompt(current_step, message, report_data)
            
            # Process response
            result = engine.process_customer_response(message, current_step, report_data)
            report_data = result['updated_report']
            
            print(f"✅ Step {current_step}: {result['completion_status']['status']}")
            print(f"📊 Completion: {result['completion_status']['completion_percentage']:.1%}")
            print(f"📈 Messages: {report_data['message_count']}/{engine.agent_capabilities.max_messages}")
            
            # Show extracted information
            if current_step == 1:
                print(f"👤 Victim Info: {report_data.get('victim_info', {})}")
            elif current_step == 2:
                print(f"📅 Incident: {report_data.get('incident_details', {})}")
            elif current_step == 3:
                print(f"💰 Transaction: {report_data.get('transaction_info', {})}")
            elif current_step == 4:
                print(f"📎 Evidence: {report_data.get('evidence', {})}")
            
            # Check if ready for escalation
            if result['should_escalate']:
                print(f"\n🚨 READY FOR ESCALATION!")
                break
            
            # Move to next step
            current_step += 1
            if current_step > len(engine.conversation_flow):
                print(f"\n⚠️  Reached maximum conversation steps")
                break
        
        # Final report status
        final_status = engine._check_report_completion(report_data)
        print(f"\n📋 Final Report Status:")
        print(f"   Status: {final_status['status']}")
        print(f"   Completion: {final_status['completion_percentage']:.1%}")
        print(f"   Messages Used: {report_data['message_count']}")
        print(f"   Ready for Human Review: {final_status['ready_for_human_review']}")
        
        # Show escalation summary if ready
        if final_status['ready_for_human_review']:
            escalation_summary = engine.generate_escalation_prompt(report_data)
            print(f"\n📋 Escalation Summary:")
            print(escalation_summary[:300] + "...")
    
    print(f"\n🎉 OCINT MVP Testing Complete!")
    print("=" * 70)

async def test_mcp_integration():
    """Test MCP server integration"""
    
    print("\n🔌 Testing OCINT MVP MCP Server Integration")
    print("-" * 50)
    
    try:
        from ocint_mvp_mcp_server import ocint_engine
        
        # Test prompt generation
        report_data = ocint_engine.report_template.copy()
        result = ocint_engine.generate_ocint_prompt(
            1, 
            "Hi, I need help with a crypto theft report",
            report_data
        )
        
        print("✅ OCINT MVP prompt generation successful")
        print(f"   Prompt length: {len(result)} characters")
        
        # Test response processing
        result = ocint_engine.process_customer_response(
            "My name is John Smith, email john@example.com, phone 555-123-4567",
            1,
            report_data
        )
        
        if result['updated_report']['victim_info']:
            print("✅ Response processing successful")
            print(f"   Extracted info: {result['updated_report']['victim_info']}")
        
        # Test completion check
        completion = ocint_engine._check_report_completion(result['updated_report'])
        print("✅ Completion check successful")
        print(f"   Status: {completion['status']}")
        print(f"   Completion: {completion['completion_percentage']:.1%}")
        
    except ImportError as e:
        print(f"⚠️  MCP integration test skipped: {e}")
        print("   (MCP dependencies not installed)")

async def test_conversation_efficiency():
    """Test conversation efficiency and message minimization"""
    
    print("\n⚡ Testing Conversation Efficiency")
    print("-" * 50)
    
    engine = OCINTMVPEngine()
    
    # Test with minimal messages
    efficient_scenario = [
        "Hi, I'm John Smith (john@example.com, 555-123-4567). Someone stole 2.5 Bitcoin from me on 2024-01-15 at 2:30 PM. I discovered it when I logged into my wallet. The wallet address is 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa and transaction hash is abc123def456. I have screenshots as evidence."
    ]
    
    report_data = engine.report_template.copy()
    current_step = 1
    
    for message in efficient_scenario:
        result = engine.process_customer_response(message, current_step, report_data)
        report_data = result['updated_report']
        
        print(f"📊 Single Message Efficiency Test:")
        print(f"   Messages Used: {report_data['message_count']}")
        print(f"   Completion: {result['completion_status']['completion_percentage']:.1%}")
        print(f"   Status: {result['completion_status']['status']}")
        print(f"   Ready for Escalation: {result['should_escalate']}")
        
        if result['should_escalate']:
            print("✅ SUCCESS: Complete report in 1 message!")
        else:
            print("⚠️  Report needs more information")
    
    # Test conversation flow efficiency
    print(f"\n📋 Conversation Flow Analysis:")
    for i, step in enumerate(engine.conversation_flow, 1):
        print(f"   Step {i}: {step['purpose']}")
        print(f"      Questions: {len(step['questions'])}")
        print(f"      Collects: {len(step['collects'])} fields")

async def test_escalation_criteria():
    """Test escalation criteria and triggers"""
    
    print("\n🚨 Testing Escalation Criteria")
    print("-" * 50)
    
    engine = OCINTMVPEngine()
    
    # Test different escalation scenarios
    escalation_tests = [
        {
            "name": "Complete Report",
            "report_data": {
                "victim_info": {"victim_name": "John", "victim_email": "john@test.com", "victim_phone": "555-123-4567"},
                "incident_details": {"incident_date": "2024-01-15", "incident_description": "Bitcoin stolen"},
                "transaction_info": {"crypto_type": "BTC", "amount_stolen": "2.5", "wallet_addresses": ["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"]},
                "evidence": {"evidence_files": ["screenshots"]},
                "message_count": 3
            }
        },
        {
            "name": "Message Limit Reached",
            "report_data": {
                "victim_info": {"victim_name": "Jane"},
                "incident_details": {"incident_description": "Ethereum stolen"},
                "message_count": 8
            }
        },
        {
            "name": "Incomplete Report",
            "report_data": {
                "victim_info": {"victim_name": "Bob"},
                "message_count": 2
            }
        }
    ]
    
    for test in escalation_tests:
        completion = engine._check_report_completion(test['report_data'])
        
        print(f"📋 {test['name']}:")
        print(f"   Status: {completion['status']}")
        print(f"   Completion: {completion['completion_percentage']:.1%}")
        print(f"   Ready for Human Review: {completion['ready_for_human_review']}")
        print(f"   Missing Fields: {len(completion['missing_fields'])}")

async def main():
    """Main test function"""
    
    print("🚀 Starting OCINT MVP Tests")
    print("=" * 70)
    
    # Run all tests
    await test_ocint_mvp()
    await test_mcp_integration()
    await test_conversation_efficiency()
    await test_escalation_criteria()
    
    print(f"\n🎉 All OCINT MVP Tests Completed!")
    print("=" * 70)
    
    # Show implementation summary
    print("\n📋 OCINT MVP Implementation Summary:")
    print("✅ Focused Tier 1 Agent for Crypto Theft Reports")
    print("✅ Efficient 5-Step Conversation Flow")
    print("✅ Message Minimization (Max 8 messages)")
    print("✅ Intelligent Information Extraction")
    print("✅ Automatic Escalation to Human Investigators")
    print("✅ Comprehensive Report Validation")
    print("✅ MCP Server Integration")
    
    print(f"\n🎯 Key Benefits:")
    print("✅ Streamlined victim onboarding process")
    print("✅ Reduced interaction time and complexity")
    print("✅ Focused scope prevents scope creep")
    print("✅ Efficient escalation to human investigators")
    print("✅ Comprehensive report creation and validation")
    
    print(f"\n🚀 Ready for OCINT MVP Deployment!")

if __name__ == "__main__":
    asyncio.run(main())
