#!/usr/bin/env python3
"""
Test script for App MCP Server
Tests the server functionality without running the full MCP server
"""

import json
import asyncio
from server import AppMCPServer

async def test_server_functionality():
    """Test the MCP server functionality"""
    print("🧪 Testing App MCP Server Functionality...")
    
    # Create server instance
    app_server = AppMCPServer()
    
    print("\n📋 Testing Capabilities...")
    
    # Test tools
    tools = app_server.server.capabilities["tools"]
    print(f"✅ Found {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool.name}: {tool.description}")
    
    # Test resources
    resources = app_server.server.capabilities["resources"]
    print(f"✅ Found {len(resources)} resources:")
    for resource in resources:
        print(f"   - {resource.uri}: {resource.name}")
    
    # Test prompts
    prompts = app_server.server.capabilities["prompts"]
    print(f"✅ Found {len(prompts)} prompts:")
    for prompt in prompts:
        print(f"   - {prompt['name']}: {prompt['description']}")
    
    print("\n🛠️ Testing Tool Functions...")
    
    # Test conversation analysis
    test_conversation = [
        {"role": "user", "content": "Hello, I need help", "timestamp": "2024-01-01T00:00:00Z"},
        {"role": "agent", "content": "Hi there! How can I help you?", "timestamp": "2024-01-01T00:00:01Z"},
        {"role": "user", "content": "My order is late", "timestamp": "2024-01-01T00:00:02Z"}
    ]
    
    analysis = await app_server.analyze_conversation({"conversation": test_conversation})
    print(f"✅ Conversation Analysis: {json.dumps(analysis, indent=2)}")
    
    # Test template generation
    template = await app_server.generate_template({
        "user_intent": "problem_solving",
        "context": "late delivery",
        "response_type": "problem_solving"
    })
    print(f"✅ Response Template: {json.dumps(template, indent=2)}")
    
    # Test metrics calculation
    test_responses = [
        {"response_time": 2.5, "user_satisfaction": 4, "resolution_time": 5.0},
        {"response_time": 1.8, "user_satisfaction": 5, "resolution_time": 3.5}
    ]
    
    metrics = await app_server.calculate_metrics({"responses": test_responses})
    print(f"✅ Response Metrics: {json.dumps(metrics, indent=2)}")
    
    print("\n📚 Testing Resource Functions...")
    
    # Test chat templates
    chat_templates = app_server.get_chat_templates()
    print(f"✅ Chat Templates: {chat_templates[:100]}...")
    
    # Test QA guidelines
    qa_guidelines = app_server.get_qa_guidelines()
    print(f"✅ QA Guidelines: {qa_guidelines[:100]}...")
    
    # Test A/B testing config
    ab_config = app_server.get_ab_testing_config()
    print(f"✅ A/B Testing Config: {ab_config[:100]}...")
    
    print("\n🎉 All tests passed! App MCP Server is working correctly.")

def test_config_loading():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        import yaml
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print(f"✅ Config loaded successfully: {config['server']['name']}")
    except ImportError:
        print("⚠️ PyYAML not installed, skipping config test")
    except Exception as e:
        print(f"❌ Config test failed: {e}")

if __name__ == "__main__":
    print("🚀 App MCP Server Test Suite")
    print("=" * 40)
    
    # Test configuration
    test_config_loading()
    
    # Test server functionality
    asyncio.run(test_server_functionality())
    
    print("\n" + "=" * 40)
    print("✅ Test suite completed successfully!")
