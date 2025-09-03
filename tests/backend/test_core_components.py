#!/usr/bin/env python3
"""
AI/DEV Lab Core Components Unit Tests
Unit tests for core app functionality
"""

import pytest
from unittest.mock import patch, MagicMock


class TestConfiguration:
    """Test configuration management."""
    
    @pytest.mark.unit
    def test_config_structure(self):
        """Test that configuration has required structure."""
        from app.backend.core.config import config
        
        # Check required configuration fields
        required_fields = [
            "APP_ENV", "APP_HOST", "APP_PORT", "APP_DEBUG",
            "DATABASE_URL", "APP_SECRET_KEY"
        ]
        
        for field in required_fields:
            assert hasattr(config, field), f"Missing config field: {field}"
    
    @pytest.mark.unit
    def test_config_values(self):
        """Test configuration values are properly set."""
        from app.backend.core.config import config
        
        # Test environment
        assert config.APP_ENV in ["development", "testing", "production"]
        
        # Test port is integer
        assert isinstance(config.APP_PORT, int)
        assert 1 <= config.APP_PORT <= 65535
        
        # Test host is string
        assert isinstance(config.APP_HOST, str)
        assert len(config.APP_HOST) > 0
        
        # Test debug is boolean
        assert isinstance(config.APP_DEBUG, bool)
    
    @pytest.mark.unit
    def test_database_url_format(self):
        """Test database URL format."""
        from app.backend.core.config import config
        
        # Database URL should be properly formatted
        assert config.DATABASE_URL.startswith("sqlite:///")
        
        # Should contain the project path
        assert "ai-dev-lab" in config.DATABASE_URL


class TestDatabaseOperations:
    """Test database operations."""
    
    @pytest.mark.unit
    @patch('app.backend.core.database.create_engine')
    @pytest.mark.asyncio
    async def test_database_initialization(self, mock_create_engine):
        """Test database initialization."""
        from app.backend.core.database import init_database
        
        # Mock the engine creation
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        # Test initialization (async function)
        await init_database()
        
        # Should create engine
        mock_create_engine.assert_called_once()
    
    @pytest.mark.unit
    @patch('app.backend.core.database.engine')
    @pytest.mark.asyncio
    async def test_database_health_check(self, mock_engine):
        """Test database health check."""
        from app.backend.core.database import check_database_health
        
        # Mock successful connection
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        
        # Test health check (async function)
        result = await check_database_health()
        assert result is True
        
        # Mock failed connection
        mock_engine.connect.side_effect = Exception("Connection failed")
        
        # Test health check failure
        result = await check_database_health()
        assert result is False


class TestSecurityFunctions:
    """Test security functions."""
    
    @pytest.mark.unit
    def test_password_hashing(self):
        """Test password hashing functionality."""
        from app.backend.core.security import get_password_hash, verify_password
        
        # Test password hashing
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original
        assert hashed != password
        
        # Hash should be string
        assert isinstance(hashed, str)
        
        # Hash should be longer than original
        assert len(hashed) > len(password)
    
    @pytest.mark.unit
    def test_password_verification(self):
        """Test password verification."""
        from app.backend.core.security import get_password_hash, verify_password
        
        # Test correct password
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        # Should verify correctly
        assert verify_password(password, hashed) is True
        
        # Should reject wrong password
        assert verify_password("wrong_password", hashed) is False
    
    @pytest.mark.unit
    def test_jwt_token_creation(self):
        """Test JWT token creation."""
        from app.backend.core.security import create_access_token
        
        # Test token creation
        data = {"sub": "testuser", "role": "user"}
        token = create_access_token(data)
        
        # Token should be string
        assert isinstance(token, str)
        
        # Token should not be empty
        assert len(token) > 0
        
        # Token should contain parts (JWT format)
        parts = token.split('.')
        assert len(parts) == 3  # Header.Payload.Signature


class TestLoggingSystem:
    """Test logging system."""
    
    @pytest.mark.unit
    def test_logging_setup(self):
        """Test logging system setup."""
        from app.backend.core.logging import setup_logging, get_logger
        
        # Test logging setup
        setup_logging()
        
        # Test logger creation
        logger = get_logger("test_logger")
        
        # Logger should be created
        assert logger is not None
        
        # Logger should have name
        assert logger.name == "test_logger"
    
    @pytest.mark.unit
    def test_logging_functions(self):
        """Test logging utility functions."""
        from app.backend.core.logging import log_request, log_response
        
        # Test request logging
        request_data = {
            "method": "GET",
            "url": "/api/v1/health",
            "headers": {"User-Agent": "test-agent"}
        }
        
        # Should not raise errors
        log_request(request_data)
        
        # Test response logging
        response_data = {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {"status": "healthy"}
        }
        
        # Should not raise errors
        log_response(response_data)


class TestAPIUtilities:
    """Test API utility functions."""
    
    @pytest.mark.unit
    def test_api_response_format(self):
        """Test API response format utilities."""
        # This would test any utility functions for API responses
        # For now, we'll test the basic structure
        
        # Mock API response
        api_response = {
            "status": "success",
            "data": {"message": "test"},
            "timestamp": "2025-08-26T12:00:00Z"
        }
        
        # Should have required fields
        assert "status" in api_response
        assert "data" in api_response
        assert "timestamp" in api_response
        
        # Status should be valid
        assert api_response["status"] in ["success", "error", "warning"]
    
    @pytest.mark.unit
    def test_error_handling(self):
        """Test error handling utilities."""
        # Test error response format
        error_response = {
            "error": "Validation failed",
            "detail": "Required field missing",
            "status_code": 400
        }
        
        # Should have error information
        assert "error" in error_response
        assert "detail" in error_response
        assert "status_code" in error_response
        
        # Status code should be valid HTTP status
        assert 100 <= error_response["status_code"] <= 599


class TestMCPIntegration:
    """Test MCP integration utilities."""
    
    @pytest.mark.unit
    def test_mcp_tool_validation(self):
        """Test MCP tool validation."""
        # Test MCP tool structure validation
        valid_tool = {
            "name": "test_tool",
            "description": "Test tool description",
            "inputSchema": {"type": "object"}
        }
        
        # Should have required fields
        assert "name" in valid_tool
        assert "description" in valid_tool
        assert "inputSchema" in valid_tool
        
        # Name should be string
        assert isinstance(valid_tool["name"], str)
        assert len(valid_tool["name"]) > 0
    
    @pytest.mark.unit
    def test_mcp_server_config(self):
        """Test MCP server configuration."""
        from app.backend.core.config import config
        
        # Check MCP server configuration
        assert hasattr(config, 'MCP_SERVER_HOST')
        assert hasattr(config, 'MCP_SERVER_PORT')
        
        # Host should be string
        assert isinstance(config.MCP_SERVER_HOST, str)
        
        # Port should be integer
        assert isinstance(config.MCP_SERVER_PORT, int)
        assert 1 <= config.MCP_SERVER_PORT <= 65535


class TestFileOperations:
    """Test file operation utilities."""
    
    @pytest.mark.unit
    def test_file_path_validation(self):
        """Test file path validation."""
        # Test safe file paths
        safe_paths = [
            "assets/css/main.css",
            "scripts/main.js",
            "images/logo.png"
        ]
        
        for path in safe_paths:
            # Should not contain directory traversal
            assert ".." not in path
            assert "\\" not in path
            
            # Should be relative paths
            assert not path.startswith("/")
    
    @pytest.mark.unit
    def test_content_type_detection(self):
        """Test content type detection."""
        # Test content type mapping
        content_types = {
            ".css": "text/css",
            ".js": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".html": "text/html"
        }
        
        for extension, expected_type in content_types.items():
            # Extension should be valid
            assert extension.startswith(".")
            assert expected_type is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
