"""
Authentication middleware for PredictPesa.
Handles JWT token validation and user context.
"""

from typing import Optional

import jwt
import structlog
from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from predictpesa.core.config import settings
from predictpesa.core.redis import cache

logger = structlog.get_logger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for handling authentication."""
    
    # Routes that don't require authentication
    EXEMPT_PATHS = {
        "/",
        "/health",
        "/health/detailed",
        "/metrics",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/auth/register",
        "/api/v1/auth/login",
        "/api/v1/markets/",  # Public market listing
    }
    
    async def dispatch(self, request: Request, call_next):
        """Process request and handle authentication."""
        
        # Skip authentication for exempt paths
        if self._is_exempt_path(request.url.path):
            return await call_next(request)
        
        # Extract and validate token
        token = self._extract_token(request)
        if token:
            user_data = await self._validate_token(token)
            if user_data:
                # Add user data to request state
                request.state.user = user_data
                request.state.user_id = user_data.get("user_id")
            else:
                # Invalid token
                return self._unauthorized_response()
        else:
            # No token provided for protected route
            if self._requires_auth(request.url.path):
                return self._unauthorized_response()
        
        return await call_next(request)
    
    def _is_exempt_path(self, path: str) -> bool:
        """Check if path is exempt from authentication."""
        # Exact match
        if path in self.EXEMPT_PATHS:
            return True
        
        # Pattern matching for dynamic routes
        exempt_patterns = [
            "/api/v1/markets/",  # Allow GET requests to list markets
        ]
        
        for pattern in exempt_patterns:
            if path.startswith(pattern):
                return True
        
        return False
    
    def _requires_auth(self, path: str) -> bool:
        """Check if path requires authentication."""
        # All API routes require auth except exempt ones
        return path.startswith("/api/v1/")
    
    def _extract_token(self, request: Request) -> Optional[str]:
        """Extract JWT token from request headers."""
        authorization = request.headers.get("Authorization")
        if not authorization:
            return None
        
        try:
            scheme, token = authorization.split(" ", 1)
            if scheme.lower() != "bearer":
                return None
            return token
        except ValueError:
            return None
    
    async def _validate_token(self, token: str) -> Optional[dict]:
        """
        Validate JWT token and return user data.
        
        Args:
            token: JWT token string
            
        Returns:
            User data dict or None if invalid
        """
        try:
            # Check if token is blacklisted (logout)
            blacklist_key = f"blacklist:{token}"
            if await cache.exists(blacklist_key):
                logger.warning("Blacklisted token used", token_hash=hash(token))
                return None
            
            # Decode and validate token
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            
            # Extract user data
            user_id = payload.get("sub")
            if not user_id:
                return None
            
            # Check token expiration
            exp = payload.get("exp")
            if not exp:
                return None
            
            # Cache user data for performance
            cache_key = f"user:{user_id}"
            user_data = await cache.get(cache_key)
            
            if not user_data:
                # In a real implementation, fetch from database
                user_data = {
                    "user_id": user_id,
                    "email": payload.get("email"),
                    "role": payload.get("role", "user"),
                    "is_verified": payload.get("is_verified", False),
                }
                # Cache for 5 minutes
                await cache.set(cache_key, user_data, expire=300)
            
            return user_data
            
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token used")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning("Invalid token used", error=str(e))
            return None
        except Exception as e:
            logger.error("Token validation error", error=str(e))
            return None
    
    def _unauthorized_response(self):
        """Return unauthorized response."""
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
