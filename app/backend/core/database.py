#!/usr/bin/env python3
"""
AI/DEV Lab App - Database Core Module
Handles database initialization and connection management
"""

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import config


logger = logging.getLogger(__name__)

# Database engine and session
engine = None
async_session = None

async def init_database():
    """Initialize database connections"""
    global engine, async_session
    
    try:
        if config.DATABASE_TYPE == "sqlite":
            # SQLite database
            database_url = config.DATABASE_URL.replace(
                "sqlite:///", "sqlite:///"
            )
            engine = create_engine(database_url, echo=config.APP_DEBUG)
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("SQLite database connection established")
                
        elif config.DATABASE_TYPE == "postgresql":
            # PostgreSQL database
            database_url = (
                f"postgresql://{config.DATABASE_USER}:"
                f"{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:"
                f"{config.DATABASE_PORT}/{config.DATABASE_NAME}"
            )
            engine = create_engine(database_url, echo=config.APP_DEBUG)
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("PostgreSQL database connection established")
        
        # Create session factory
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        logger.info("Database session factory created")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def close_database():
    """Close database connections"""
    global engine
    
    try:
        if engine:
            engine.dispose()
            logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}")

def get_db_session():
    """Get database session"""
    if not engine:
        raise RuntimeError("Database not initialized")
    return async_session()

# Database health check
async def check_database_health():
    """Check database health status"""
    try:
        if engine:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        return False
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
