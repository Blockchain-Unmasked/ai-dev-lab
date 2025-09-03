#!/usr/bin/env python3
"""
AI/DEV Lab Testing Framework - Test Configuration and Fixtures
Provides comprehensive test setup for maintaining 100/100 scores
"""

import asyncio
import tempfile
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Add app to Python path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set testing environment before importing app
import os
os.environ["APP_ENV"] = "testing"
os.environ["APP_DEBUG"] = "false"

from app.backend.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_config() -> dict:
    """Test configuration overrides."""
    return {
        "APP_ENV": "testing",
        "APP_SECRET_KEY": "test-secret-key-for-testing-only",
        "APP_DEBUG": False,
        "SECURITY_ENABLED": True,
        "CORS_ALLOWED_ORIGINS": ["http://localhost:3000", "http://localhost:8000"],
        "MCP_SERVER_HOST": "localhost",
        "MCP_SERVER_PORT": 8001,
    }


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application."""
    # Override environment variables for testing
    import os
    os.environ["APP_ENV"] = "testing"
    os.environ["APP_DEBUG"] = "false"
    
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client for the FastAPI application."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def auth_headers() -> dict:
    """Provide authentication headers for protected endpoints."""
    # For testing, we'll use a mock JWT token
    # In production, this would be generated through proper authentication
    return {
        "Authorization": "Bearer test-jwt-token-for-testing",
        "Content-Type": "application/json"
    }


@pytest.fixture
def mock_mcp_server():
    """Mock MCP server responses for testing."""
    return {
        "tools": [
            {
                "name": "run_terminal_command",
                "description": "Execute terminal commands",
                "inputSchema": {"type": "object", "properties": {"command": {"type": "string"}}}
            },
            {
                "name": "analyze_chat_conversation",
                "description": "Analyze chat conversations",
                "inputSchema": {"type": "object", "properties": {"conversation": {"type": "array"}}}
            },
            {
                "name": "generate_response_template",
                "description": "Generate response templates",
                "inputSchema": {"type": "object", "properties": {"intent": {"type": "string"}}}
            }
        ],
        "resources": [
            {
                "uri": "app://chat-templates",
                "name": "Chat Response Templates",
                "description": "Available response templates"
            }
        ]
    }


@pytest.fixture
def sample_conversation() -> list:
    """Sample conversation data for testing."""
    return [
        {
            "role": "user",
            "content": "Hello, I need help with my account",
            "timestamp": "2025-08-26T12:00:00Z"
        },
        {
            "role": "assistant",
            "content": "Hello! I'd be happy to help you with your account. What specific issue are you experiencing?",
            "timestamp": "2025-08-26T12:00:01Z"
        },
        {
            "role": "user",
            "content": "I can't log in, it says my password is incorrect",
            "timestamp": "2025-08-26T12:00:05Z"
        }
    ]


@pytest.fixture
def sample_user_data() -> dict:
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "role": "user"
    }


@pytest.fixture
def temp_dir():
    """Create a temporary directory for file operations."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_env_vars(monkeypatch, test_config):
    """Mock environment variables for testing."""
    for key, value in test_config.items():
        monkeypatch.setenv(key, str(value))


@pytest.fixture
def mock_gemini_api(monkeypatch):
    """Mock Gemini API responses for testing."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-pro")
    monkeypatch.setenv("GEMINI_TEMPERATURE", "0.7")


@pytest.fixture
def performance_benchmarks():
    """Performance benchmark thresholds for testing."""
    return {
        "api_response_time": 200,  # milliseconds
        "database_query_time": 100,  # milliseconds
        "page_load_time": 5000,  # milliseconds
        "mcp_tool_response": 1000,  # milliseconds
        "concurrent_users": 100,
        "requests_per_second": 100
    }


@pytest.fixture
def security_test_data():
    """Security test data for vulnerability testing."""
    return {
        "sql_injection": [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "'; INSERT INTO users VALUES ('hacker', 'password'); --"
        ],
        "xss_payloads": [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>"
        ],
        "path_traversal": [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd"
        ]
    }


@pytest.fixture
def ocint_standards():
    """OCINT standards for compliance testing."""
    return {
        "security_score_minimum": 900,
        "code_coverage_minimum": 95,
        "performance_benchmarks": {
            "api_response": 200,
            "database_query": 100,
            "page_load": 5000
        },
        "security_requirements": [
            "authentication_required",
            "authorization_enforced",
            "input_validation",
            "sql_injection_prevention",
            "xss_prevention",
            "csrf_protection"
        ]
    }


# Test markers for categorization
pytest_plugins = [
    "pytest_asyncio",
    "pytest_cov",
    "pytest_html",
    "pytest_benchmark"
]


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )
    config.addinivalue_line(
        "markers", "security: mark test as a security test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "mcp: mark test as an MCP server test"
    )
    config.addinivalue_line(
        "markers", "backend: mark test as a backend test"
    )
    config.addinivalue_line(
        "markers", "frontend: mark test as a frontend test"
    )
    config.addinivalue_line(
        "markers", "critical: mark test as critical (must pass)"
    )
    config.addinivalue_line(
        "markers", "ocint: mark test as OCINT standards compliance"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add backend marker for backend tests
        if "backend" in item.nodeid or "api" in item.nodeid or "database" in item.nodeid:
            item.add_marker(pytest.mark.backend)
        
        # Add frontend marker for frontend tests
        if "frontend" in item.nodeid or "component" in item.nodeid or "ui" in item.nodeid:
            item.add_marker(pytest.mark.frontend)
        
        # Add MCP marker for MCP tests
        if "mcp" in item.nodeid or "mcp_server" in item.nodeid:
            item.add_marker(pytest.mark.mcp)
        
        # Add security marker for security tests
        if "security" in item.nodeid or "auth" in item.nodeid or "validation" in item.nodeid:
            item.add_marker(pytest.mark.security)
        
        # Add performance marker for performance tests
        if "performance" in item.nodeid or "benchmark" in item.nodeid or "load" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        
        # Add critical marker for critical tests
        if "health" in item.nodeid or "status" in item.nodeid:
            item.add_marker(pytest.mark.critical)
