#!/usr/bin/env python3
"""
AI/DEV Lab App - Logging Core Module
Handles structured logging configuration
"""

import logging
import sys
from typing import Dict, Any
import structlog

from .config import config


def setup_logging():
    """Setup structured logging configuration"""
    
    # Configure standard logging
    logging.basicConfig(
        level=(logging.DEBUG if config.APP_DEBUG else logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log")
        ]
    )
    
    # Configure structlog for structured logging
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Set log levels for external libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    # Log configuration
    logger = structlog.get_logger()
    logger.info(
        "Logging system initialized",
        environment=config.APP_ENV,
        debug_mode=config.APP_DEBUG,
        log_level=("DEBUG" if config.APP_DEBUG else "INFO")
    )


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get structured logger instance"""
    return structlog.get_logger(name)


def log_request(request_data: Dict[str, Any], logger: structlog.BoundLogger = None):
    """Log HTTP request data"""
    if logger is None:
        logger = get_logger()
    
    logger.info(
        "HTTP Request",
        method=request_data.get("method"),
        path=request_data.get("path"),
        headers=request_data.get("headers"),
        query_params=request_data.get(
            "query_params"
        ),
        client_ip=request_data.get("client_ip")
    )


def log_response(response_data: Dict[str, Any], logger: structlog.BoundLogger = None):
    """Log HTTP response data"""
    if logger is None:
        logger = get_logger()
    
    logger.info(
        "HTTP Response",
        status_code=response_data.get("status_code"),
        response_time=response_data.get("response_time"),
        response_size=response_data.get("response_size")
    )
