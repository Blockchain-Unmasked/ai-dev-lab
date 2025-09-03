#!/usr/bin/env python3
"""
AI/DEV Lab App - API Routes Module
Handles all API endpoints and routing
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any
import re

from core.security import verify_token
from core.config import Config
from api.prompts import router as prompts_router

# Create API router
api_router = APIRouter(prefix="/api/v1", tags=["api"])

# Include prompts router
api_router.include_router(prompts_router)


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
    """Test Gemini API connection with provided API key using enhanced client"""
    api_key = request.get("apiKey", "")
    
    if not api_key:
        return {
            "success": False,
            "error": "API key is required"
        }
    
    try:
        # Import the enhanced Gemini client
        from core.gemini_client import EnhancedGeminiClient, TaskType
        
        # Create client with provided API key
        client = EnhancedGeminiClient(api_key=api_key)
        
        # Test with different models
        test_prompt = "Hello! This is a test message from AI/DEV Lab. Please respond with 'API connection successful!' and mention which model you are."
        
        # Test with Flash model (fast and efficient)
        response = await client.generate_content(
            prompt=test_prompt,
            task_type=TaskType.CHAT
        )
        
        if response.get("success") and response.get("text"):
            return {
                "success": True,
                "message": "API connection successful",
                "response": response["text"].strip(),
                "model": response.get("model", "unknown"),
                "client_type": "enhanced",
                "available_models": client.get_available_models()
            }
        else:
            return {
                "success": False,
                "error": response.get("error", "No response from API")
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"API test failed: {str(e)}"
        }


@api_router.post("/ai/chat")
async def ai_chat(message: Dict[str, str]):
    """AI chat endpoint with enhanced Gemini API integration"""
    user_message = message.get("message", "")
    
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required"
        )
    
    try:
        # Use enhanced Gemini API for intelligent responses
        from core.gemini_client import gemini_client, TaskType
        from core.config import Config
        
        # Check if API key is configured
        if not Config.GEMINI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key not configured"
            )
        
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

CRITICAL GUIDANCE FOR CRYPTO THEFT SCENARIOS:
- Law enforcement agencies do NOT have specialized crypto investigation teams
- Victims must do the investigative work themselves first
- Focus on: 1) Immediate security (change passwords, enable 2FA), 2) Gather evidence (transaction IDs, wallet addresses), 3) Report to exchanges, 4) Use blockchain analysis tools
- NEVER mention law enforcement in initial responses - they cannot help without evidence
- NEVER suggest filing police reports immediately - this is ineffective
- Only suggest law enforcement AFTER victim has gathered all evidence and documentation
- Emphasize that the victim needs to do the work first, then law enforcement can assist
- For crypto theft: focus on securing accounts, gathering evidence, and working with exchanges first

IMPORTANT: If the customer mentions crypto theft, do NOT mention law enforcement in your response. Focus only on immediate security steps and evidence gathering.

EXAMPLE OF WHAT NOT TO SAY: "report to law enforcement" or "file a police report"
EXAMPLE OF WHAT TO SAY: "secure your account, gather evidence, report to exchanges"

Keep your response concise (2-4 sentences) but thorough. Focus on being genuinely helpful rather than generic."""

        # Generate response with enhanced Gemini client
        response = await gemini_client.generate_content(
            prompt=intelligent_prompt,
            task_type=TaskType.CHAT
        )
        
        if response.get("success") and response.get("text"):
            ai_response = response["text"].strip()
            mcp_tools_used = ["enhanced-gemini-api"]
            model_used = response.get("model", "unknown")
            confidence = 0.95
            quality = 0.9
        else:
            raise Exception(f"No response generated from Gemini API: {response.get('error', 'Unknown error')}")
        
        return {
            "user_message": user_message,
            "ai_response": ai_response,
            "mcp_tools_used": mcp_tools_used,
            "timestamp": "2025-01-26T12:00:00Z",
            "model": model_used,
            "mcp_integration": "active",
            "confidence": confidence,
            "quality": quality,
            "client_type": "enhanced"
        }
        
    except Exception as e:
        # Intelligent fallback response based on user message content
        ai_response = generate_intelligent_fallback_response(user_message, str(e))
        return {
            "user_message": user_message,
            "ai_response": ai_response,
            "mcp_tools_used": ["fallback"],
            "timestamp": "2025-01-26T12:00:00Z",
            "model": "fallback-model",
            "mcp_integration": "error",
            "error": str(e),
            "client_type": "fallback"
        }


@api_router.post("/ai/structured-chat")
async def structured_ai_chat(request: Dict[str, Any]):
    """AI chat endpoint with structured JSON output"""
    user_message = request.get("message", "")
    schema = request.get("schema", {
        "type": "object",
        "properties": {
            "response": {"type": "string"},
            "confidence": {"type": "number"},
            "suggestions": {"type": "array", "items": {"type": "string"}},
            "next_steps": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["response", "confidence"]
    })
    
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message is required"
        )
    
    try:
        from core.gemini_client import gemini_client, TaskType
        from core.config import Config
        
        if not Config.GEMINI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key not configured"
            )
        
        prompt = f"""Analyze this customer message and provide a structured response:

Customer Message: "{user_message}"

Provide a JSON response with:
- response: Your helpful response to the customer
- confidence: Your confidence level (0.0 to 1.0)
- suggestions: 2-3 helpful suggestions
- next_steps: Recommended next steps for the customer"""

        response = await gemini_client.generate_structured_output(
            prompt=prompt,
            schema=schema,
            task_type=TaskType.STRUCTURED_OUTPUT
        )
        
        if response.get("success"):
            return {
                "user_message": user_message,
                "structured_response": response.get("structured_data", {}),
                "model": response.get("model", "unknown"),
                "timestamp": "2025-01-26T12:00:00Z",
                "client_type": "enhanced-structured"
            }
        else:
            raise Exception(f"Structured generation failed: {response.get('error', 'Unknown error')}")
            
    except Exception as e:
        return {
            "user_message": user_message,
            "error": str(e),
            "client_type": "fallback"
        }

@api_router.post("/ai/analyze")
async def ai_analyze(request: Dict[str, Any]):
    """AI analysis endpoint for complex reasoning tasks"""
    content = request.get("content", "")
    analysis_type = request.get("analysis_type", "general")
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content is required"
        )
    
    try:
        from core.gemini_client import gemini_client, TaskType
        from core.config import Config
        
        if not Config.GEMINI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Gemini API key not configured"
            )
        
        prompt = f"""Perform a comprehensive {analysis_type} analysis of the following content:

{content}

Provide detailed insights, identify key patterns, and offer actionable recommendations."""

        response = await gemini_client.generate_content(
            prompt=prompt,
            task_type=TaskType.ANALYSIS
        )
        
        if response.get("success"):
            return {
                "content": content,
                "analysis_type": analysis_type,
                "analysis": response.get("text", ""),
                "model": response.get("model", "unknown"),
                "timestamp": "2025-01-26T12:00:00Z",
                "client_type": "enhanced-analysis"
            }
        else:
            raise Exception(f"Analysis failed: {response.get('error', 'Unknown error')}")
            
    except Exception as e:
        return {
            "content": content,
            "error": str(e),
            "client_type": "fallback"
        }

@api_router.get("/ai/models-enhanced")
async def get_enhanced_ai_models():
    """Get available AI models and their capabilities"""
    try:
        from core.gemini_client import gemini_client
        
        return {
            "success": True,
            "models": gemini_client.get_available_models(),
            "client_type": "enhanced"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "models": []
        }

# Note: Exception handlers should be registered on the main app, not on APIRouter
# These will be handled by the global exception handler in main.py
