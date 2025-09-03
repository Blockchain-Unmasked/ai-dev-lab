#!/usr/bin/env python3
"""
AI/DEV Lab App - Configuration Module
Handles environment variables and configuration management
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
# Look for .env file in the app directory (parent of backend)
# Use absolute path to avoid issues with __file__ resolution
env_path = Path("/Users/hazael/Code/ai-dev-lab/app/.env")
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded environment variables from: {env_path}")
else:
    print(f"⚠️ No .env file found at: {env_path}")

class Config:
    """Application configuration class"""
    
    # App Configuration
    APP_NAME = os.getenv("APP_NAME", "AI_DEV_LAB_DEMO")
    APP_VERSION = os.getenv("APP_VERSION", "2.0.0")
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_DEBUG = os.getenv("APP_DEBUG", "true").lower() == "true"
    APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "dev-secret-key")
    APP_HOST = os.getenv("APP_HOST", "localhost")
    APP_PORT = int(os.getenv("APP_PORT", "8000"))
    
    # Database Configuration
    DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "sqlite:////Users/hazael/Code/ai-dev-lab/app/database/demo_database.db"
    )
    
    # AI API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # Updated to latest model
    GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    GEMINI_MAX_TOKENS = int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
    GEMINI_TOP_P = float(os.getenv("GEMINI_TOP_P", "0.95"))
    GEMINI_TOP_K = int(os.getenv("GEMINI_TOP_K", "40"))
    
    # Debug: Print API key status (without exposing the actual key)
    if GEMINI_API_KEY:
        print(f"✅ Gemini API key loaded: {GEMINI_API_KEY[:10]}...")
    else:
        print("⚠️ No Gemini API key found in environment variables")
    
    # MCP Server Configuration
    MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
    MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8001"))
    
    # Security Configuration
    SECURITY_ENABLED = os.getenv("SECURITY_ENABLED", "true").lower() == "true"
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if cls.APP_ENV == "production" and cls.APP_DEBUG:
            print("Warning: Debug mode enabled in production")
        if not cls.GEMINI_API_KEY:
            print("Info: No Gemini API key configured, using mock responses")
        return True

# Global config instance
config = Config()
