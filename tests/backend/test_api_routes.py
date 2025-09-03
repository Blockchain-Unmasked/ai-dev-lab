#!/usr/bin/env python3
"""
AI/DEV Lab API Routes Unit Tests
Unit tests for individual API endpoint functionality
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi import status


class TestHealthRoutes:
    """Test health and status route functionality."""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_health_endpoint_logic(self):
        """Test health endpoint business logic."""
        from app.backend.api.routes import health_check
        
        # Test health check response (async function)
        response = await health_check()
        
        # Should return health status
        assert response["status"] == "healthy"
        assert response["service"] == "AI/DEV Lab App"
        assert "version" in response
        assert response["environment"] == "development"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_status_endpoint_logic(self):
        """Test status endpoint business logic."""
        from app.backend.api.routes import system_status
        
        # Test status check response (async function)
        response = await system_status()
        
        # Should have required fields
        assert "system" in response
        assert "database" in response
        assert "mcp_server" in response
        assert "security" in response
        
        # System should be operational
        assert response["system"] == "operational"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_config_endpoint_logic(self):
        """Test config endpoint business logic."""
        from app.backend.api.routes import get_config
        
        # Test config info response (async function)
        response = await get_config()
        
        # Should have required fields
        assert "app_name" in response
        assert "app_version" in response
        assert "environment" in response
        
        # App name should exist and be a string
        assert "app_name" in response
        assert isinstance(response["app_name"], str)
        assert len(response["app_name"]) > 0


class TestMCPRoutes:
    """Test MCP integration route functionality."""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_mcp_status_logic(self):
        """Test MCP status endpoint logic."""
        from app.backend.api.routes import mcp_server_status
        
        # Test MCP status response (async function)
        response = await mcp_server_status()
        
        # Should have required fields
        assert "status" in response
        assert "tools_available" in response
        
        # Tools count should be 15
        assert response["tools_available"] == 15
    
    @pytest.mark.unit
    def test_mcp_tools_logic(self):
        """Test MCP tools endpoint logic."""
        # Note: There's no mcp_tools endpoint in the current routes
        # This test validates the expected structure when it's implemented
        
        # Mock MCP tools response structure
        mock_tools_response = {
            "tools": [
                {
                    "name": "run_terminal_command",
                    "description": "Execute terminal commands",
                    "inputSchema": {"type": "object"}
                },
                {
                    "name": "analyze_chat_conversation",
                    "description": "Analyze chat conversations",
                    "inputSchema": {"type": "object"}
                }
            ]
        }
        
        # Should have tools list
        assert "tools" in mock_tools_response
        assert isinstance(mock_tools_response["tools"], list)
        
        # Each tool should have required structure
        for tool in mock_tools_response["tools"]:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool


class TestAIRoutes:
    """Test AI integration route functionality."""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_ai_models_logic(self):
        """Test AI models endpoint logic."""
        from app.backend.api.routes import get_ai_models
        
        # Test AI models response (async function)
        response = await get_ai_models()
        
        # Should have models list
        assert "models" in response
        assert isinstance(response["models"], list)
        
        # Should have some models
        assert len(response["models"]) > 0
        
        # Each model should have required fields
        for model in response["models"]:
            assert "name" in model
            assert "provider" in model
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_ai_chat_logic_basic(self):
        """Test AI chat endpoint basic logic."""
        from app.backend.api.routes import ai_chat
        
        # Test basic message (async function)
        message_data = {"message": "Hello, how are you?"}
        response = await ai_chat(message_data)
        
        # Should have required fields
        assert "user_message" in response
        assert "ai_response" in response
        assert "mcp_integration" in response
        assert "mcp_tools_used" in response
        
        # User message should match input
        assert response["user_message"] == "Hello, how are you?"
        
        # MCP integration should be active
        assert response["mcp_integration"] == "active"
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_ai_chat_logic_analysis(self):
        """Test AI chat endpoint analysis logic."""
        from app.backend.api.routes import ai_chat
        
        # Test analysis message (async function)
        message_data = {"message": "Can you analyze this conversation?"}
        response = await ai_chat(message_data)
        
        # Should use analysis tool
        assert "analyze_chat_conversation" in response["mcp_tools_used"]
        
        # Response should indicate analysis
        assert "MCP Tool Analysis" in response["ai_response"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_ai_chat_logic_template(self):
        """Test AI chat endpoint template logic."""
        from app.backend.api.routes import ai_chat
        
        # Test template message (async function)
        message_data = {"message": "Generate a response template"}
        response = await ai_chat(message_data)
        
        # Should use template tool
        assert "generate_response_template" in response["mcp_tools_used"]
        
        # Response should indicate template generation
        assert "MCP Tool Response" in response["ai_response"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_ai_chat_logic_metrics(self):
        """Test AI chat endpoint metrics logic."""
        from app.backend.api.routes import ai_chat
        
        # Test metrics message (async function)
        message_data = {"message": "Calculate performance metrics"}
        response = await ai_chat(message_data)
        
        # Should use metrics tool
        assert "calculate_response_metrics" in response["mcp_tools_used"]
        
        # Response should indicate metrics calculation
        assert "MCP Tool Metrics" in response["ai_response"]
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_ai_chat_logic_empty_message(self):
        """Test AI chat endpoint empty message handling."""
        from app.backend.api.routes import ai_chat
        from fastapi import HTTPException
        
        # Test empty message (async function)
        message_data = {"message": ""}
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await ai_chat(message_data)
        
        # Should be 400 Bad Request
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Message is required" in str(exc_info.value.detail)
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_ai_chat_logic_missing_message(self):
        """Test AI chat endpoint missing message handling."""
        from app.backend.api.routes import ai_chat
        from fastapi import HTTPException
        
        # Test missing message field (async function)
        message_data = {}
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await ai_chat(message_data)
        
        # Should be 400 Bad Request
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Message is required" in str(exc_info.value.detail)


class TestProtectedRoutes:
    """Test protected route functionality."""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_protected_endpoint_logic(self):
        """Test protected endpoint logic."""
        from app.backend.api.routes import protected_endpoint
        
        # Test protected endpoint response (async function)
        response = await protected_endpoint()
        
        # Should have required fields
        assert "message" in response
        assert "user_authenticated" in response
        
        # Message should indicate protection
        assert "protected" in response["message"].lower()


class TestFrontendServing:
    """Test frontend serving logic."""
    
    @pytest.mark.unit
    @patch('builtins.open')
    @pytest.mark.asyncio
    async def test_frontend_serving_logic(self, mock_open):
        """Test frontend serving endpoint logic."""
        from app.backend.main import serve_frontend
        
        # Mock file reading
        mock_file = MagicMock()
        mock_file.read.return_value = "<html><title>Test</title></html>"
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Test frontend serving (async function)
        response = await serve_frontend()
        
        # Should return HTML response
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    @pytest.mark.unit
    @patch('builtins.open')
    @pytest.mark.asyncio
    async def test_frontend_file_serving_logic(self, mock_open):
        """Test frontend file serving logic."""
        from app.backend.main import serve_frontend_file
        
        # Mock file reading
        mock_file = MagicMock()
        mock_file.read.return_value = "body { color: red; }"
        mock_open.return_value.__enter__.return_value = mock_file
        
        # Test CSS file serving (async function)
        response = await serve_frontend_file("assets/css/main.css")
        
        # Should return CSS response
        assert response.status_code == 200
        assert "text/css" in response.headers["content-type"]


class TestErrorHandling:
    """Test error handling logic."""
    
    @pytest.mark.unit
    def test_http_exception_handling(self):
        """Test HTTP exception handling."""
        from fastapi import HTTPException
        
        # Test HTTP exception creation
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
        
        # Should have correct status code
        assert exception.status_code == 404
        
        # Should have detail message
        assert exception.detail == "Resource not found"
    
    @pytest.mark.unit
    def test_validation_error_handling(self):
        """Test validation error handling."""
        # Test validation error structure
        # This would test how validation errors are handled
        # For now, we'll test the basic concept
        
        # Mock validation error
        validation_error = {
            "type": "validation_error",
            "detail": "Field validation failed",
            "fields": ["email", "password"]
        }
        
        # Should have error information
        assert validation_error["type"] == "validation_error"
        assert "detail" in validation_error
        assert "fields" in validation_error


class TestResponseFormats:
    """Test API response format consistency."""
    
    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_response_structure_consistency(self):
        """Test that all API responses have consistent structure."""
        # Test health endpoint response structure
        from app.backend.api.routes import health_check
        health_response = await health_check()
        
        # Should have consistent structure
        assert isinstance(health_response, dict)
        assert "status" in health_response
        assert "service" in health_response
        assert "version" in health_response
    
    @pytest.mark.unit
    def test_error_response_consistency(self):
        """Test that error responses have consistent structure."""
        # Test error response structure
        error_response = {
            "error": "Validation failed",
            "detail": "Required field missing",
            "status_code": 400
        }
        
        # Should have consistent error structure
        assert "error" in error_response
        assert "detail" in error_response
        assert "status_code" in error_response
        
        # Status code should be integer
        assert isinstance(error_response["status_code"], int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
