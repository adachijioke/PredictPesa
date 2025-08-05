"""
Request ID middleware for PredictPesa.
Adds unique request IDs for tracing and debugging.
"""

import contextvars
import uuid
from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Context variable for request ID
request_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    'request_id', default=None
)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add unique request IDs to all requests."""
    
    def __init__(self, app, header_name: str = "X-Request-ID"):
        super().__init__(app)
        self.header_name = header_name
    
    async def dispatch(self, request: Request, call_next):
        """Process request and add request ID."""
        
        # Get or generate request ID
        request_id = self._get_or_generate_request_id(request)
        
        # Set in context variable for logging
        request_id_var.set(request_id)
        
        # Add to request state
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add request ID to response headers
        response.headers[self.header_name] = request_id
        
        return response
    
    def _get_or_generate_request_id(self, request: Request) -> str:
        """
        Get request ID from headers or generate a new one.
        
        Args:
            request: HTTP request
            
        Returns:
            Request ID string
        """
        # Check if client provided request ID
        existing_id = request.headers.get(self.header_name)
        if existing_id:
            return existing_id
        
        # Generate new UUID
        return str(uuid.uuid4())


def get_request_id() -> Optional[str]:
    """
    Get current request ID from context.
    
    Returns:
        Request ID or None if not set
    """
    return request_id_var.get()
