#!/usr/bin/env python3
"""
Test script for Gemini API key validation
"""

import os
import requests
from dotenv import load_dotenv


def test_gemini_api():
    """Test the Gemini API connection"""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return False
    
    print(f"🔑 API Key loaded: {api_key[:8]}...{api_key[-4:]}")
    
    # Test API endpoint - using current model
    url = ("https://generativelanguage.googleapis.com/v1beta/"
           "models/gemini-1.5-pro:generateContent")
    
    # Use API key as query parameter instead of Authorization header
    url_with_key = f"{url}?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": ("Hello! This is a test message from AI/DEV Lab. "
                         "Please respond with 'API connection successful!'")
            }]
        }]
    }
    
    try:
        print("🔄 Testing API connection...")
        response = requests.post(url_with_key, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API connection successful!")
            response_text = (result.get('candidates', [{}])[0]
                           .get('content', {}).get('parts', [{}])[0]
                           .get('text', 'No text in response'))
            print(f"📝 Response: {response_text}")
            return True
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
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

if __name__ == "__main__":
    print("🧪 Testing Gemini API Configuration")
    print("=" * 50)
    
    # Test API key format
    format_ok = test_api_key_format()
    print()
    
    # Test API connection
    if format_ok:
        connection_ok = test_gemini_api()
        print()
        
        if connection_ok:
            print("🎉 All tests passed! Your Gemini API key is working correctly.")
        else:
            print("💥 API connection test failed. Please check your API key and internet connection.")
    else:
        print("💥 API key format test failed. Please check your .env file.")
    
    print("=" * 50)
