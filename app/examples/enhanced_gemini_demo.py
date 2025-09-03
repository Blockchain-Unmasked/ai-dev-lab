#!/usr/bin/env python3
"""
Enhanced Gemini API Demo
Demonstrates all the new features of the latest Gemini API implementation
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent.parent
sys.path.insert(0, str(app_dir))

from backend.core.gemini_client import (
    EnhancedGeminiClient, 
    TaskType, 
    ModelType,
    GenerationConfig,
    SafetySettings
)

async def demo_basic_content_generation():
    """Demonstrate basic content generation with different models"""
    print("🚀 Demo: Basic Content Generation")
    print("-" * 50)
    
    client = EnhancedGeminiClient()
    
    # Test different task types
    tasks = [
        (TaskType.CHAT, "Hello! How are you today?"),
        (TaskType.ANALYSIS, "Analyze the benefits of using AI in software development."),
        (TaskType.CODE_GENERATION, "Write a Python function to calculate fibonacci numbers."),
        (TaskType.HIGH_FREQUENCY, "What is 2+2?")
    ]
    
    for task_type, prompt in tasks:
        print(f"\n📝 Task: {task_type.value}")
        print(f"Prompt: {prompt}")
        
        response = await client.generate_content(
            prompt=prompt,
            task_type=task_type
        )
        
        if response.get("success"):
            print(f"✅ Model: {response.get('model', 'Unknown')}")
            print(f"Response: {response.get('text', 'No response')[:200]}...")
        else:
            print(f"❌ Error: {response.get('error', 'Unknown error')}")

async def demo_structured_output():
    """Demonstrate structured JSON output"""
    print("\n\n🎯 Demo: Structured Output")
    print("-" * 50)
    
    client = EnhancedGeminiClient()
    
    # Define schema for customer support response
    schema = {
        "type": "object",
        "properties": {
            "response": {"type": "string"},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "category": {"type": "string", "enum": ["technical", "billing", "general", "escalation"]},
            "suggestions": {
                "type": "array",
                "items": {"type": "string"},
                "maxItems": 3
            },
            "escalation_needed": {"type": "boolean"},
            "next_steps": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["response", "confidence", "category"]
    }
    
    customer_message = "I'm having trouble logging into my account. I keep getting an error message."
    
    print(f"Customer Message: {customer_message}")
    
    prompt = f"""Analyze this customer support message and provide a structured response:

Customer Message: "{customer_message}"

Provide a JSON response with:
- response: Your helpful response to the customer
- confidence: Your confidence level (0.0 to 1.0)
- category: The type of issue (technical, billing, general, escalation)
- suggestions: 2-3 helpful suggestions
- escalation_needed: Whether this needs human intervention
- next_steps: Recommended next steps for the customer"""

    response = await client.generate_structured_output(
        prompt=prompt,
        schema=schema,
        task_type=TaskType.STRUCTURED_OUTPUT
    )
    
    if response.get("success"):
        print("✅ Structured Response Generated:")
        structured_data = response.get("structured_data", {})
        print(json.dumps(structured_data, indent=2))
    else:
        print(f"❌ Error: {response.get('error', 'Unknown error')}")

async def demo_model_selection():
    """Demonstrate intelligent model selection"""
    print("\n\n🤖 Demo: Intelligent Model Selection")
    print("-" * 50)
    
    client = EnhancedGeminiClient()
    
    # Show available models
    models = client.get_available_models()
    print("Available Models:")
    for model in models:
        print(f"  - {model['name']}: {model['description']}")
    
    # Test model selection for different content lengths
    test_cases = [
        ("Short question", "What is Python?", 20),
        ("Medium analysis", "Explain the benefits of microservices architecture in detail.", 100),
        ("Long content", "A" * 1000 + " - Please analyze this long content.", 1000)
    ]
    
    for description, content, length in test_cases:
        print(f"\n📊 {description} (Length: {length} chars)")
        selected_model = client.select_model(TaskType.ANALYSIS, length)
        print(f"Selected Model: {selected_model}")

async def demo_custom_generation_config():
    """Demonstrate custom generation configuration"""
    print("\n\n⚙️ Demo: Custom Generation Configuration")
    print("-" * 50)
    
    client = EnhancedGeminiClient()
    
    # Create custom config for creative writing
    creative_config = GenerationConfig(
        temperature=0.9,  # More creative
        max_output_tokens=500,
        top_p=0.95,
        top_k=40
    )
    
    # Create custom config for technical analysis
    technical_config = GenerationConfig(
        temperature=0.3,  # More focused
        max_output_tokens=1000,
        top_p=0.8,
        top_k=20
    )
    
    creative_prompt = "Write a short creative story about a robot learning to paint."
    technical_prompt = "Explain the technical implementation of a REST API with authentication."
    
    print("🎨 Creative Writing (High Temperature):")
    response = await client.generate_content(
        prompt=creative_prompt,
        task_type=TaskType.CHAT,
        generation_config=creative_config
    )
    
    if response.get("success"):
        print(f"Response: {response.get('text', 'No response')[:200]}...")
    
    print("\n🔧 Technical Analysis (Low Temperature):")
    response = await client.generate_content(
        prompt=technical_prompt,
        task_type=TaskType.ANALYSIS,
        generation_config=technical_config
    )
    
    if response.get("success"):
        print(f"Response: {response.get('text', 'No response')[:200]}...")

async def demo_safety_settings():
    """Demonstrate custom safety settings"""
    print("\n\n🛡️ Demo: Custom Safety Settings")
    print("-" * 50)
    
    client = EnhancedGeminiClient()
    
    # Create strict safety settings
    strict_safety = SafetySettings(
        harassment_threshold="BLOCK_LOW_AND_ABOVE",
        hate_speech_threshold="BLOCK_LOW_AND_ABOVE",
        sexually_explicit_threshold="BLOCK_LOW_AND_ABOVE",
        dangerous_content_threshold="BLOCK_LOW_AND_ABOVE"
    )
    
    # Create moderate safety settings
    moderate_safety = SafetySettings(
        harassment_threshold="BLOCK_MEDIUM_AND_ABOVE",
        hate_speech_threshold="BLOCK_MEDIUM_AND_ABOVE",
        sexually_explicit_threshold="BLOCK_MEDIUM_AND_ABOVE",
        dangerous_content_threshold="BLOCK_MEDIUM_AND_ABOVE"
    )
    
    test_prompt = "Write a professional email about a project update."
    
    print("🔒 Strict Safety Settings:")
    response = await client.generate_content(
        prompt=test_prompt,
        task_type=TaskType.CHAT,
        safety_settings=strict_safety
    )
    
    if response.get("success"):
        print(f"Response: {response.get('text', 'No response')[:200]}...")
        safety_ratings = response.get("safety_ratings", [])
        if safety_ratings:
            print(f"Safety Ratings: {len(safety_ratings)} categories checked")

async def demo_error_handling():
    """Demonstrate error handling and fallback"""
    print("\n\n🚨 Demo: Error Handling")
    print("-" * 50)
    
    client = EnhancedGeminiClient()
    
    # Test with invalid input
    print("Testing with empty prompt:")
    response = await client.generate_content(
        prompt="",
        task_type=TaskType.CHAT
    )
    
    if not response.get("success"):
        print(f"✅ Properly handled empty prompt: {response.get('error', 'Unknown error')}")
    
    # Test with very long prompt
    print("\nTesting with very long prompt:")
    long_prompt = "A" * 100000  # Very long prompt
    response = await client.generate_content(
        prompt=long_prompt,
        task_type=TaskType.ANALYSIS
    )
    
    if response.get("success"):
        print("✅ Handled long prompt successfully")
    else:
        print(f"⚠️ Long prompt handling: {response.get('error', 'Unknown error')}")

async def main():
    """Run all demos"""
    print("🎉 Enhanced Gemini API Demo")
    print("=" * 60)
    print("This demo showcases the latest Gemini API features:")
    print("- New genai.Client() pattern")
    print("- Structured JSON output")
    print("- Intelligent model selection")
    print("- Custom generation configuration")
    print("- Enhanced safety settings")
    print("- Multimodal processing capabilities")
    print("=" * 60)
    
    try:
        await demo_basic_content_generation()
        await demo_structured_output()
        await demo_model_selection()
        await demo_custom_generation_config()
        await demo_safety_settings()
        await demo_error_handling()
        
        print("\n\n🎊 Demo Complete!")
        print("All enhanced Gemini API features have been demonstrated.")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Make sure your GEMINI_API_KEY is configured in the .env file")

if __name__ == "__main__":
    asyncio.run(main())
