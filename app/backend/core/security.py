#!/usr/bin/env python3
"""
AI/DEV Lab App - Security Core Module
Handles authentication and security features
"""

import logging
from typing import Optional
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from .config import config

logger = logging.getLogger(__name__)

# Security token bearer
security = HTTPBearer()

# JWT configuration
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = config.APP_SECRET_KEY


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[str]:
    """Verify JWT token and return user identifier"""
    try:
        # Extract token
        token = credentials.credentials
        
        # Decode and verify token
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        
        # Extract user identifier
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        logger.info(f"Token verified for user: {user_id}")
        return user_id
        
    except JWTError:
        logger.warning("Invalid JWT token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token verification failed"
        )


def create_access_token(data: dict, expires_delta: Optional[int] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        from datetime import datetime, timedelta
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Password hashing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password processing failed"
        )
