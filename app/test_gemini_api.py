#!/usr/bin/env python3
"""
Enhanced test script for Gemini API validation with new features
"""

import os
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the app directory to the Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

# Load environment variables
load_dotenv()

async def test_enhanced_gemini_api():
    """Test the enhanced Gemini API client"""
    
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return False
    
    print(f"🔑 API Key loaded: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        # Import the enhanced Gemini client
        from backend.core.gemini_client import EnhancedGeminiClient, TaskType
        
        # Create client
        client = EnhancedGeminiClient(api_key=api_key)
        print("✅ Enhanced Gemini client initialized")
        
        # Test basic content generation
        print("🔄 Testing basic content generation...")
        response = await client.generate_content(
            prompt="Hello! This is a test message from AI/DEV Lab. Please respond with 'API connection successful!' and mention which model you are.",
            task_type=TaskType.CHAT
        )
        
        if response.get("success"):
            print("✅ Basic content generation successful!")
            print(f"📝 Response: {response.get('text', 'No text')}")
            print(f"🤖 Model: {response.get('model', 'Unknown')}")
        else:
            print(f"❌ Basic content generation failed: {response.get('error', 'Unknown error')}")
            return False
        
        # Test structured output
        print("\n🔄 Testing structured output...")
        schema = {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "model_info": {"type": "string"},
                "capabilities": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["status", "model_info"]
        }
        
        structured_response = await client.generate_structured_output(
            prompt="Provide information about your current status and capabilities in JSON format.",
            schema=schema,
            task_type=TaskType.STRUCTURED_OUTPUT
        )
        
        if structured_response.get("success"):
            print("✅ Structured output generation successful!")
            print(f"📊 Structured data: {structured_response.get('structured_data', {})}")
        else:
            print(f"❌ Structured output failed: {structured_response.get('error', 'Unknown error')}")
        
        # Test model selection
        print("\n🔄 Testing model selection...")
        models = client.get_available_models()
        print(f"📋 Available models: {len(models)}")
        for model in models:
            print(f"  - {model['name']}: {model['description']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running from the app directory")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False




def test_api_key_format():
    """Test if the API key format is correct"""
    
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ No API key found")
        return False
    
    # Check if it looks like a valid Google API key
    if api_key.startswith('AIza') and len(api_key) == 39:
        print("✅ API key format looks correct (39 characters, starts with 'AIza')")
        return True
    else:
        print(f"⚠️  API key format may be incorrect: {len(api_key)} characters, starts with '{api_key[:4]}'")
        return False

async def main():
    """Main test function"""
    print("🧪 Testing Enhanced Gemini API Configuration")
    print("=" * 60)
    
    # Test API key format
    format_ok = test_api_key_format()
    print()
    
    if format_ok:
        # Test enhanced API client
        print("🚀 Testing Enhanced Gemini API Client...")
        enhanced_ok = await test_enhanced_gemini_api()
        print()
        
        if enhanced_ok:
            print("🎉 Enhanced API tests passed! Your Gemini API key is working with the new features.")
        else:
            print("💥 Enhanced API test failed. Please check your API key and internet connection.")
    else:
        print("💥 API key format test failed. Please check your .env file.")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
