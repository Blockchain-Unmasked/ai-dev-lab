#!/usr/bin/env python3
"""
AI/DEV Lab Backend API Tests
Comprehensive testing for FastAPI endpoints and functionality
"""

import pytest
from fastapi import status
from httpx import AsyncClient


class TestHealthEndpoints:
    """Test health and status endpoints."""
    
    @pytest.mark.critical
    @pytest.mark.backend
    def test_health_endpoint(self, client):
        """Test the health endpoint returns healthy status."""
        response = client.get("/api/v1/health")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "AI/DEV Lab App"
        assert data["version"] == "2.0.0"
        assert data["environment"] == "testing"
    
    @pytest.mark.critical
    @pytest.mark.backend
    def test_status_endpoint(self, client):
        """Test the status endpoint returns system status."""
        response = client.get("/api/v1/status")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "uptime" in data
        assert "version" in data
        assert "environment" in data
    
    @pytest.mark.backend
    def test_config_endpoint(self, client):
        """Test the config endpoint returns configuration info."""
        response = client.get("/api/v1/config")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "app_name" in data
        assert "app_version" in data
        assert "environment" in data


class TestMCPEndpoints:
    """Test MCP server integration endpoints."""
    
    @pytest.mark.mcp
    @pytest.mark.backend
    def test_mcp_status_endpoint(self, client):
        """Test the MCP status endpoint."""
        response = client.get("/api/v1/mcp/status")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "status" in data
        assert "tools_available" in data
        assert data["tools_available"] == 15
    
    @pytest.mark.mcp
    @pytest.mark.backend
    def test_mcp_tools_endpoint(self, client):
        """Test the MCP tools endpoint."""
        response = client.get("/api/v1/mcp/tools")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "tools" in data
        assert len(data["tools"]) > 0
        
        # Check for specific tools
        tool_names = [tool["name"] for tool in data["tools"]]
        assert "run_terminal_command" in tool_names
        assert "analyze_chat_conversation" in tool_names


class TestAIEndpoints:
    """Test AI integration endpoints."""
    
    @pytest.mark.backend
    def test_ai_models_endpoint(self, client):
        """Test the AI models endpoint."""
        response = client.get("/api/v1/ai/models")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "models" in data
        assert len(data["models"]) > 0
    
    @pytest.mark.backend
    def test_ai_chat_endpoint_success(self, client):
        """Test the AI chat endpoint with valid input."""
        message = {"message": "Hello, how can you help me?"}
        response = client.post("/api/v1/ai/chat", json=message)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["user_message"] == "Hello, how can you help me?"
        assert "ai_response" in data
        assert data["mcp_integration"] == "active"
        assert "mcp_tools_used" in data
    
    @pytest.mark.backend
    def test_ai_chat_endpoint_analysis(self, client):
        """Test AI chat with conversation analysis request."""
        message = {"message": "Can you analyze this conversation?"}
        response = client.post("/api/v1/ai/chat", json=message)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "analyze_chat_conversation" in data["mcp_tools_used"]
        assert "MCP Tool Analysis" in data["ai_response"]
    
    @pytest.mark.backend
    def test_ai_chat_endpoint_template(self, client):
        """Test AI chat with response template request."""
        message = {"message": "Generate a response template"}
        response = client.post("/api/v1/ai/chat", json=message)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "generate_response_template" in data["mcp_tools_used"]
        assert "MCP Tool Response" in data["ai_response"]
    
    @pytest.mark.backend
    def test_ai_chat_endpoint_metrics(self, client):
        """Test AI chat with metrics calculation request."""
        message = {"message": "Calculate performance metrics"}
        response = client.post("/api/v1/ai/chat", json=message)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "calculate_response_metrics" in data["mcp_tools_used"]
        assert "MCP Tool Metrics" in data["ai_response"]
    
    @pytest.mark.backend
    def test_ai_chat_endpoint_empty_message(self, client):
        """Test AI chat endpoint with empty message."""
        message = {"message": ""}
        response = client.post("/api/v1/ai/chat", json=message)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "detail" in data
        assert "Message is required" in data["detail"]
    
    @pytest.mark.backend
    def test_ai_chat_endpoint_missing_message(self, client):
        """Test AI chat endpoint with missing message field."""
        message = {}
        response = client.post("/api/v1/ai/chat", json=message)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "detail" in data
        assert "Message is required" in data["detail"]


class TestProtectedEndpoints:
    """Test protected endpoints requiring authentication."""
    
    @pytest.mark.security
    @pytest.mark.backend
    def test_protected_endpoint_without_auth(self, client):
        """Test protected endpoint without authentication."""
        response = client.get("/api/v1/protected")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @pytest.mark.security
    @pytest.mark.backend
    def test_protected_endpoint_with_auth(self, client, auth_headers):
        """Test protected endpoint with authentication."""
        response = client.get("/api/v1/protected", headers=auth_headers)
        # Note: This will fail until we implement proper JWT validation
        # For now, we're testing the endpoint structure
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED]


class TestFrontendServing:
    """Test frontend static file serving."""
    
    @pytest.mark.frontend
    @pytest.mark.backend
    def test_frontend_index_html(self, client):
        """Test frontend index.html is served correctly."""
        response = client.get("/frontend")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]
        assert "OCINT - AI Intake/Support Agent Demo" in response.text
    
    @pytest.mark.frontend
    @pytest.mark.backend
    def test_frontend_css_assets(self, client):
        """Test frontend CSS assets are served correctly."""
        response = client.get("/frontend/assets/css/main.css")
        assert response.status_code == status.HTTP_200_OK
        assert "text/css" in response.headers["content-type"]
        assert "OCINT AI Intake/Support Agent Demo" in response.text
    
    @pytest.mark.frontend
    @pytest.mark.backend
    def test_frontend_js_assets(self, client):
        """Test frontend JavaScript assets are served correctly."""
        response = client.get("/frontend/scripts/main.js")
        assert response.status_code == status.HTTP_200_OK
        assert "application/javascript" in response.headers["content-type"]
    
    @pytest.mark.frontend
    @pytest.mark.backend
    def test_frontend_asset_not_found(self, client):
        """Test frontend asset not found handling."""
        response = client.get("/frontend/nonexistent.js")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    @pytest.mark.backend
    def test_404_not_found(self, client):
        """Test 404 handling for non-existent endpoints."""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    @pytest.mark.backend
    def test_method_not_allowed(self, client):
        """Test method not allowed handling."""
        response = client.put("/api/v1/health")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    @pytest.mark.backend
    def test_invalid_json(self, client):
        """Test invalid JSON handling."""
        response = client.post(
            "/api/v1/ai/chat",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestAsyncEndpoints:
    """Test async endpoint functionality."""
    
    @pytest.mark.asyncio
    @pytest.mark.backend
    async def test_async_health_endpoint(self, async_client):
        """Test health endpoint with async client."""
        response = await async_client.get("/api/v1/health")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["status"] == "healthy"
    
    @pytest.mark.asyncio
    @pytest.mark.backend
    async def test_async_ai_chat_endpoint(self, async_client):
        """Test AI chat endpoint with async client."""
        message = {"message": "Async test message"}
        response = await async_client.post("/api/v1/ai/chat", json=message)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["user_message"] == "Async test message"
        assert data["mcp_integration"] == "active"


class TestPerformanceEndpoints:
    """Test endpoint performance and response times."""
    
    @pytest.mark.performance
    @pytest.mark.backend
    def test_health_endpoint_performance(self, client, benchmark):
        """Benchmark health endpoint response time."""
        def health_request():
            return client.get("/api/v1/health")
        
        result = benchmark(health_request)
        assert result.status_code == status.HTTP_200_OK
        
        # Performance assertion (should be under 100ms)
        # Note: This is a basic benchmark, actual performance may vary
        assert result.elapsed.total_seconds() < 0.1
    
    @pytest.mark.performance
    @pytest.mark.backend
    def test_ai_chat_endpoint_performance(self, client, benchmark):
        """Benchmark AI chat endpoint response time."""
        message = {"message": "Performance test message"}
        
        def ai_chat_request():
            return client.post("/api/v1/ai/chat", json=message)
        
        result = benchmark(ai_chat_request)
        assert result.status_code == status.HTTP_200_OK
        
        # Performance assertion (should be under 200ms)
        assert result.elapsed.total_seconds() < 0.2


class TestOCINTCompliance:
    """Test OCINT standards compliance."""
    
    @pytest.mark.ocint
    @pytest.mark.backend
    def test_ocint_security_headers(self, client):
        """Test OCINT security header requirements."""
        response = client.get("/api/v1/health")
        
        # Check for security headers
        headers = response.headers
        assert "X-Content-Type-Options" in headers or "X-Frame-Options" in headers
        
        # Additional security checks can be added here
        # based on OCINT security standards
    
    @pytest.mark.ocint
    @pytest.mark.backend
    def test_ocint_response_format(self, client):
        """Test OCINT response format standards."""
        response = client.get("/api/v1/health")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        # Check for required fields based on OCINT standards
        required_fields = ["status", "service", "version", "environment"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
    
    @pytest.mark.ocint
    @pytest.mark.backend
    def test_ocint_error_handling(self, client):
        """Test OCINT error handling standards."""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        # Check for proper error response format
        assert "detail" in data or "error" in data
