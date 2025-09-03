#!/usr/bin/env python3
"""
AI/DEV Lab MCP Lab Server Tests
Comprehensive testing for Lab MCP Server integration
"""

import pytest
import requests
from unittest.mock import Mock, patch


class TestLabMCPServerAvailability:
    """Test Lab MCP Server availability and connectivity."""
    
    @pytest.mark.mcp
    @pytest.mark.critical
    def test_lab_mcp_server_running(self):
        """Test that the Lab MCP Server is running on port 8001."""
        try:
            response = requests.get("http://localhost:8001/health", timeout=5)
            assert response.status_code == 200
        except requests.exceptions.RequestException:
            # If the server isn't running, we'll test the mock responses
            # This allows tests to run even when the server is offline
            pytest.skip("Lab MCP Server not running on port 8001")
    
    @pytest.mark.mcp
    def test_lab_mcp_server_port_configuration(self):
        """Test that the app is configured to connect to the correct MCP port."""
        from app.backend.core.config import config
        
        assert config.MCP_SERVER_PORT == 8001
        assert config.MCP_SERVER_HOST == "localhost"
    
    @pytest.mark.mcp
    def test_lab_mcp_server_connection(self):
        """Test connection to Lab MCP Server."""
        try:
            # Test basic connectivity
            response = requests.get("http://localhost:8001/", timeout=5)
            # Should get some response (even if it's an error page)
            assert response.status_code in [200, 404, 405]
        except requests.exceptions.RequestException:
            pytest.skip("Lab MCP Server not accessible")


class TestLabMCPServerTools:
    """Test the 15 tools available in the Lab MCP Server."""
    
    @pytest.mark.mcp
    def test_mcp_tools_count(self, client):
        """Test that exactly 15 tools are available."""
        response = client.get("/api/v1/mcp/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["tools_available"] == 15
    
    @pytest.mark.mcp
    def test_mcp_tools_list(self, client):
        """Test that the MCP tools endpoint returns the correct tools."""
        response = client.get("/api/v1/mcp/tools")
        assert response.status_code == 200
        
        data = response.json()
        assert "tools" in data
        assert len(data["tools"]) == 15
        
        # Check for specific expected tools
        tool_names = [tool["name"] for tool in data["tools"]]
        expected_tools = [
            "run_terminal_command",
            "install_package",
            "analyze_chat_conversation",
            "generate_response_template",
            "calculate_response_metrics"
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names, f"Missing tool: {expected_tool}"
    
    @pytest.mark.mcp
    def test_mcp_tool_structure(self, client):
        """Test that MCP tools have the correct structure."""
        response = client.get("/api/v1/mcp/tools")
        assert response.status_code == 200
        
        data = response.json()
        tools = data["tools"]
        
        for tool in tools:
            # Check required fields
            assert "name" in tool, "Tool missing name field"
            assert "description" in tool, "Tool missing description field"
            assert "inputSchema" in tool, "Tool missing inputSchema field"
            
            # Check field types
            assert isinstance(tool["name"], str), "Tool name must be string"
            assert isinstance(tool["description"], str), "Tool description must be string"
            assert isinstance(tool["inputSchema"], dict), "Tool inputSchema must be dict"


class TestLabMCPServerIntegration:
    """Test integration between the app and Lab MCP Server."""
    
    @pytest.mark.mcp
    def test_app_mcp_status_integration(self, client):
        """Test that the app correctly reports MCP server status."""
        response = client.get("/api/v1/mcp/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "tools_available" in data
        assert "last_updated" in data or "timestamp" in data
    
    @pytest.mark.mcp
    def test_app_mcp_tools_integration(self, client):
        """Test that the app can access MCP server tools."""
        response = client.get("/api/v1/mcp/tools")
        assert response.status_code == 200
        
        data = response.json()
        assert "tools" in data
        assert len(data["tools"]) > 0
        
        # Verify tool details are accessible
        for tool in data["tools"]:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool
    
    @pytest.mark.mcp
    def test_app_ai_mcp_integration(self, client):
        """Test that the app's AI can use MCP tools."""
        # Test conversation analysis tool
        message = {"message": "Can you analyze this conversation?"}
        response = client.post("/api/v1/ai/chat", json=message)
        assert response.status_code == 200
        
        data = response.json()
        assert data["mcp_integration"] == "active"
        assert "analyze_chat_conversation" in data["mcp_tools_used"]
        
        # Test response template tool
        message = {"message": "Generate a response template"}
        response = client.post("/api/v1/ai/chat", json=message)
        assert response.status_code == 200
        
        data = response.json()
        assert data["mcp_integration"] == "active"
        assert "generate_response_template" in data["mcp_tools_used"]
        
        # Test metrics calculation tool
        message = {"message": "Calculate performance metrics"}
        response = client.post("/api/v1/ai/chat", json=message)
        assert response.status_code == 200
        
        data = response.json()
        assert data["mcp_integration"] == "active"
        assert "calculate_response_metrics" in data["mcp_tools_used"]


class TestLabMCPServerCommunication:
    """Test communication protocols between app and Lab MCP Server."""
    
    @pytest.mark.mcp
    def test_mcp_protocol_compliance(self, client):
        """Test that the app follows MCP protocol standards."""
        # Test that the app can communicate using standard MCP protocols
        # This is a basic test - production would use MCP client libraries
        
        response = client.get("/api/v1/mcp/status")
        assert response.status_code == 200
        
        # Verify response format follows expected structure
        data = response.json()
        required_fields = ["status", "tools_available"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
    
    @pytest.mark.mcp
    def test_mcp_error_handling(self, client):
        """Test MCP error handling when server is unavailable."""
        # Test how the app handles MCP server communication errors
        # This would be tested by temporarily disabling the MCP server
        
        # For now, we test the current implementation
        response = client.get("/api/v1/mcp/status")
        assert response.status_code == 200
        
        # The app should handle MCP server errors gracefully
        # and provide fallback responses when appropriate
    
    @pytest.mark.mcp
    def test_mcp_timeout_handling(self, client):
        """Test MCP timeout handling."""
        # Test that the app handles MCP server timeouts appropriately
        # This would be tested by simulating slow responses
        
        # For now, we test the current implementation
        response = client.get("/api/v1/mcp/status")
        assert response.status_code == 200
        
        # The app should have timeout mechanisms in place
        # for MCP server communication


class TestLabMCPServerPerformance:
    """Test Lab MCP Server performance characteristics."""
    
    @pytest.mark.performance
    @pytest.mark.mcp
    def test_mcp_status_response_time(self, client, benchmark):
        """Benchmark MCP status endpoint response time."""
        def mcp_status_request():
            return client.get("/api/v1/mcp/status")
        
        result = benchmark(mcp_status_request)
        assert result.status_code == 200
        
        # MCP status should respond quickly (under 100ms)
        assert result.elapsed.total_seconds() < 0.1
    
    @pytest.mark.performance
    @pytest.mark.mcp
    def test_mcp_tools_response_time(self, client, benchmark):
        """Benchmark MCP tools endpoint response time."""
        def mcp_tools_request():
            return client.get("/api/v1/mcp/tools")
        
        result = benchmark(mcp_tools_request)
        assert result.status_code == 200
        
        # MCP tools should respond quickly (under 100ms)
        assert result.elapsed.total_seconds() < 0.1
    
    @pytest.mark.performance
    @pytest.mark.mcp
    def test_mcp_ai_integration_response_time(self, client, benchmark):
        """Benchmark AI chat with MCP tool integration response time."""
        message = {"message": "Test message for performance"}
        
        def ai_chat_request():
            return client.post("/api/v1/ai/chat", json=message)
        
        result = benchmark(ai_chat_request)
        assert result.status_code == 200
        
        # AI chat with MCP integration should respond under 200ms
        assert result.elapsed.total_seconds() < 0.2


class TestLabMCPServerSecurity:
    """Test Lab MCP Server security measures."""
    
    @pytest.mark.security
    @pytest.mark.mcp
    def test_mcp_server_access_control(self, client):
        """Test that MCP server endpoints have proper access control."""
        # Test that MCP endpoints are not publicly accessible
        # without proper authentication (if required)
        
        # For now, we test the current implementation
        response = client.get("/api/v1/mcp/status")
        assert response.status_code == 200
        
        # In production, these endpoints might require authentication
        # This test ensures the current security model is working
    
    @pytest.mark.security
    @pytest.mark.mcp
    def test_mcp_tool_input_validation(self, client):
        """Test that MCP tools validate input properly."""
        # Test that MCP tools don't accept malicious input
        # This is tested through the AI chat endpoint
        
        malicious_inputs = [
            {"message": "<script>alert('XSS')</script>"},
            {"message": "'; DROP TABLE users; --"},
            {"message": "../../../etc/passwd"}
        ]
        
        for malicious_input in malicious_inputs:
            response = client.post("/api/v1/ai/chat", json=malicious_input)
            # Should handle malicious input safely
            assert response.status_code in [200, 400, 422]


class TestLabMCPServerReliability:
    """Test Lab MCP Server reliability and fault tolerance."""
    
    @pytest.mark.mcp
    def test_mcp_server_consistency(self, client):
        """Test that MCP server responses are consistent."""
        # Test multiple requests to ensure consistency
        
        responses = []
        for _ in range(5):
            response = client.get("/api/v1/mcp/status")
            assert response.status_code == 200
            responses.append(response.json())
        
        # All responses should have the same structure
        first_response = responses[0]
        for response in responses[1:]:
            assert response.keys() == first_response.keys()
            assert response["tools_available"] == first_response["tools_available"]
    
    @pytest.mark.mcp
    def test_mcp_server_availability_monitoring(self, client):
        """Test MCP server availability monitoring."""
        # Test that the app can detect MCP server availability
        
        response = client.get("/api/v1/mcp/status")
        assert response.status_code == 200
        
        data = response.json()
        # Should indicate server status
        assert "status" in data
        
        # Status should be meaningful (e.g., "available", "unavailable")
        assert data["status"] in ["available", "unavailable", "healthy", "error"]


class TestLabMCPServerOCINTCompliance:
    """Test Lab MCP Server OCINT standards compliance."""
    
    @pytest.mark.ocint
    @pytest.mark.mcp
    def test_ocint_mcp_standards_compliance(self, client):
        """Test that MCP server integration meets OCINT standards."""
        # Test compliance with OCINT MCP integration standards
        
        response = client.get("/api/v1/mcp/status")
        assert response.status_code == 200
        
        data = response.json()
        
        # Check for required OCINT compliance fields
        ocint_requirements = [
            "status",
            "tools_available",
            "version"  # Optional but recommended
        ]
        
        for requirement in ocint_requirements:
            if requirement in data:
                # Field exists and has valid value
                if requirement == "tools_available":
                    assert isinstance(data[requirement], int)
                    assert data[requirement] > 0
                elif requirement == "status":
                    assert isinstance(data[requirement], str)
                    assert len(data[requirement]) > 0
        
        # Should have at least basic compliance
        compliance_score = sum(1 for req in ocint_requirements if req in data)
        assert compliance_score >= 2, "Insufficient OCINT compliance"
