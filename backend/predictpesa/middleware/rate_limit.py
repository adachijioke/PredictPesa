"""
Rate limiting middleware for PredictPesa.
Protects against abuse and ensures fair usage.
"""

import structlog
from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from predictpesa.core.config import settings
from predictpesa.core.redis import rate_limiter

logger = structlog.get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting requests."""
    
    def __init__(self, app, requests_per_minute: int = None, burst: int = None):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute or settings.rate_limit_requests_per_minute
        self.burst = burst or settings.rate_limit_burst
    
    async def dispatch(self, request: Request, call_next):
        """Process request and apply rate limiting."""
        
        # Skip rate limiting for health checks and metrics
        if self._is_exempt_path(request.url.path):
            return await call_next(request)
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Check rate limit
        is_allowed, remaining = await self._check_rate_limit(client_id, request)
        
        if not is_allowed:
            logger.warning(
                "Rate limit exceeded",
                client_id=client_id,
                path=request.url.path,
                method=request.method
            )
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
                headers={
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": "60",
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = "60"
        
        return response
    
    def _is_exempt_path(self, path: str) -> bool:
        """Check if path is exempt from rate limiting."""
        exempt_paths = {
            "/health",
            "/health/detailed",
            "/metrics",
        }
        return path in exempt_paths
    
    def _get_client_id(self, request: Request) -> str:
        """
        Get client identifier for rate limiting.
        
        Uses user ID if authenticated, otherwise IP address.
        """
        # Try to get user ID from request state (set by auth middleware)
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"
        
        # Fall back to IP address
        client_ip = self._get_client_ip(request)
        return f"ip:{client_ip}"
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        # Check for forwarded headers (behind proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP in the chain
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fall back to direct connection
        return request.client.host if request.client else "unknown"
    
    async def _check_rate_limit(self, client_id: str, request: Request) -> tuple[bool, int]:
        """
        Check if request is within rate limit.
        
        Args:
            client_id: Client identifier
            request: HTTP request
            
        Returns:
            Tuple of (is_allowed, remaining_requests)
        """
        # Different limits for different endpoints
        limit, window = self._get_limits_for_path(request.url.path, request.method)
        
        # Use Redis rate limiter
        rate_limit_key = f"rate_limit:{client_id}:{request.url.path}"
        
        try:
            is_allowed, remaining = await rate_limiter.is_allowed(
                rate_limit_key,
                limit,
                window
            )
            return is_allowed, remaining
        except Exception as e:
            logger.error("Rate limit check failed", error=str(e))
            # Fail open - allow request if Redis is down
            return True, limit
    
    def _get_limits_for_path(self, path: str, method: str) -> tuple[int, int]:
        """
        Get rate limits for specific path and method.
        
        Args:
            path: Request path
            method: HTTP method
            
        Returns:
            Tuple of (requests_limit, window_seconds)
        """
        # Default limits
        default_limit = self.requests_per_minute
        window = 60  # 1 minute
        
        # Stricter limits for write operations
        if method in ["POST", "PUT", "DELETE"]:
            # Market creation and staking limits
            if "/markets/create" in path:
                return 5, window  # 5 markets per minute
            elif "/stakes/create" in path:
                return 10, window  # 10 stakes per minute
            elif "/auth/" in path:
                return 5, window  # 5 auth attempts per minute
            else:
                return default_limit // 2, window  # Half the default for other writes
        
        # More lenient for read operations
        elif method == "GET":
            if "/markets/" in path:
                return default_limit * 2, window  # Double for market queries
            else:
                return default_limit, window
        
        return default_limit, window
