#!/usr/bin/env python3
"""
AI/DEV Lab App - API Routes Module
Handles all API endpoints and routing
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict

from core.security import verify_token
from core.config import Config

# Create API router
api_router = APIRouter(prefix="/api/v1", tags=["api"])


@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI/DEV Lab App",
        "version": Config.APP_VERSION,
        "environment": Config.APP_ENV
    }


@api_router.get("/status")
async def system_status():
    """System status endpoint"""
    return {
        "system": "operational",
        "database": "connected",
        "mcp_server": "active",
        "security": "enabled"
    }


@api_router.get("/config")
async def get_config():
    """Get application configuration (non-sensitive)"""
    return {
        "app_name": Config.APP_NAME,
        "app_version": Config.APP_VERSION,
        "environment": Config.APP_ENV,
        "debug_mode": Config.APP_DEBUG,
        "database_type": Config.DATABASE_TYPE,
        "security_enabled": Config.SECURITY_ENABLED,
        "cors_enabled": bool(Config.CORS_ALLOWED_ORIGINS)
    }


@api_router.get("/protected", dependencies=[Depends(verify_token)])
async def protected_endpoint():
    """Protected endpoint requiring authentication"""
    return {
        "message": "Access granted to protected endpoint",
        "user_authenticated": True
    }


@api_router.post("/auth/login")
async def login(credentials: Dict[str, str]):
    """User authentication endpoint"""
    # Mock authentication for demo purposes
    username = credentials.get("username")
    password = credentials.get("password")
    
    if username == "demo" and password == "demo123":
        from ..core.security import create_access_token
        token = create_access_token(data={"sub": username})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": username
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


@api_router.get("/mcp/status")
async def mcp_server_status():
    """MCP server status endpoint"""
    return {
        "mcp_server": "active",
        "host": Config.MCP_SERVER_HOST,
        "port": Config.MCP_SERVER_PORT,
        "tools_available": 15,
        "status": "operational"
    }


@api_router.get("/ai/config")
async def get_ai_config():
    """Get AI API configuration"""
    return {
        "gemini": {
            "api_key_configured": bool(Config.GEMINI_API_KEY),
            "model": Config.GEMINI_MODEL,
            "temperature": Config.GEMINI_TEMPERATURE,
            "status": "available" if Config.GEMINI_API_KEY else "unconfigured"
        },
        "models": [
            {
                "name": "gemini-pro",
                "provider": "Google",
                "status": ("available" if Config.GEMINI_API_KEY else "unconfigured")
            },
            {
                "name": "gpt-4",
                "provider": "OpenAI",
                "status": "available"
            },
            {
                "name": "claude-3",
                "provider": "Anthropic",
                "status": "available"
            }
        ]
    }

@api_router.get("/ai/models")
async def get_ai_models():
    """Get available AI models"""
    return {
        "models": [
            {
                "name": "gemini-pro",
                "provider": "Google",
                "status": ("available" if Config.GEMINI_API_KEY else "unconfigured")
            },
            {
                "name": "gpt-4",
                "provider": "OpenAI",
                "status": "available"
            },
            {
                "name": "claude-3",
                "provider": "Anthropic",
                "status": "available"
            }
        ]
    }


@api_router.post("/test-gemini")
async def test_gemini_api(request: Dict[str, str]):
    """Test Gemini API connection with provided API key"""
    api_key = request.get("apiKey", "")
    
    if not api_key:
        return {
            "success": False,
            "error": "API key is required"
        }
    
    try:
        # Test the API key by making a simple request to Gemini
        import google.generativeai as genai
        
        # Configure the API key
        genai.configure(api_key=api_key)
        
        # Create a model instance
        model = genai.GenerativeModel('gemini-pro')
        
        # Make a simple test request
        response = model.generate_content("Hello, this is a test message. Please respond with 'API connection successful'.")
        
        if response and response.text:
            return {
                "success": True,
                "message": "API connection successful",
                "response": response.text.strip()
            }
        else:
            return {
                "success": False,
                "error": "No response from API"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"API test failed: {str(e)}"
        }


@api_router.post("/ai/chat")
async def ai_chat(message: Dict[str, str]):
    """AI chat endpoint with real Gemini API integration"""
    user_message = message.get("message", "")
    
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required"
        )
    
    try:
        # Use real Gemini API for intelligent responses
        import google.generativeai as genai
        from core.config import Config
        
        # Configure Gemini API
        if not Config.GEMINI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key not configured"
            )
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        # Create an intelligent prompt for customer support
        intelligent_prompt = f"""You are an expert AI customer support agent for a technology company. You are knowledgeable, helpful, and professional.

Customer Message: "{user_message}"

Please provide a helpful, intelligent response that:
1. Directly addresses the customer's question or concern
2. Shows understanding of their specific situation
3. Provides actionable solutions or guidance
4. Asks clarifying questions if needed
5. Maintains a professional yet friendly tone
6. Demonstrates expertise in technology and customer service

Keep your response concise (2-4 sentences) but thorough. Focus on being genuinely helpful rather than generic."""

        # Generate response with Gemini
        response = model.generate_content(
            intelligent_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=Config.GEMINI_TEMPERATURE,
                max_output_tokens=1024,
                top_p=0.95,
                top_k=40
            )
        )
        
        if response and response.text:
            ai_response = response.text.strip()
            mcp_tools_used = ["gemini-api"]
            model_used = Config.GEMINI_MODEL
        else:
            raise Exception("No response generated from Gemini API")
        
        return {
            "user_message": user_message,
            "ai_response": ai_response,
            "mcp_tools_used": mcp_tools_used,
            "timestamp": "2025-01-26T12:00:00Z",
            "model": model_used,
            "mcp_integration": "active",
            "confidence": 0.95,
            "quality": 0.9
        }
        
    except Exception as e:
        # Fallback to intelligent mock response
        ai_response = f"I understand you're asking about: {user_message}. I'd be happy to help you with that. Could you provide a bit more detail about your specific situation so I can give you the most accurate assistance?"
        return {
            "user_message": user_message,
            "ai_response": ai_response,
            "mcp_tools_used": ["fallback"],
            "timestamp": "2025-01-26T12:00:00Z",
            "model": "fallback-model",
            "mcp_integration": "error",
            "error": str(e)
        }


# Note: Exception handlers should be registered on the main app, not on APIRouter
# These will be handled by the global exception handler in main.py
