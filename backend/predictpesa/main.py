"""
PredictPesa FastAPI Application Entry Point.

This module initializes the FastAPI application with all necessary middleware,
routers, and configuration for the PredictPesa prediction market platform.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

from predictpesa.api.v1 import api_router
from predictpesa.core.config import settings
from predictpesa.core.database import init_db, close_db
from predictpesa.core.logging import setup_logging
from predictpesa.core.redis import init_redis, close_redis
from predictpesa.middleware.auth import AuthMiddleware
from predictpesa.middleware.rate_limit import RateLimitMiddleware
from predictpesa.middleware.request_id import RequestIDMiddleware

# Prometheus metrics
REQUEST_COUNT = Counter(
    "predictpesa_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"]
)

REQUEST_DURATION = Histogram(
    "predictpesa_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

logger = structlog.get_logger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware for collecting Prometheus metrics."""
    
    async def dispatch(self, request: Request, call_next):
        """Process request and collect metrics."""
        method = request.method
        path = request.url.path
        
        # Start timer
        with REQUEST_DURATION.labels(method=method, endpoint=path).time():
            response = await call_next(request)
        
        # Count requests
        REQUEST_COUNT.labels(
            method=method,
            endpoint=path,
            status_code=response.status_code
        ).inc()
        
        return response


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    logger.info("Starting PredictPesa application", version=settings.app_version)
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Initialize Redis
    await init_redis()
    logger.info("Redis initialized")
    
    # TODO: Initialize Hedera client
    # TODO: Initialize AI services
    # TODO: Initialize background tasks
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down PredictPesa application")
    
    # Close database connections
    await close_db()
    logger.info("Database connections closed")
    
    # Close Redis connections
    await close_redis()
    logger.info("Redis connections closed")
    
    logger.info("Application shutdown complete")


def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    # Setup logging
    setup_logging()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
    )
    
    # Add middleware (order matters!)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    
    # Trusted host middleware (security)
    if settings.is_production:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["predictpesa.com", "*.predictpesa.com"]
        )
    
    # Custom middleware
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(AuthMiddleware)
    
    # Metrics middleware (if enabled)
    if settings.prometheus_enabled:
        app.add_middleware(MetricsMiddleware)
    
    # Include API routers
    app.include_router(api_router, prefix="/api/v1")
    
    # Health check endpoints
    @app.get("/health")
    async def health_check():
        """Basic health check endpoint."""
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment
        }
    
    @app.get("/health/detailed")
    async def detailed_health_check():
        """Detailed health check with dependencies."""
        # TODO: Add database, Redis, Hedera network checks
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "dependencies": {
                "database": "healthy",
                "redis": "healthy",
                "hedera": "healthy"
            }
        }
    
    # Metrics endpoint
    if settings.prometheus_enabled:
        @app.get("/metrics")
        async def metrics():
            """Prometheus metrics endpoint."""
            return Response(
                generate_latest(),
                media_type="text/plain"
            )
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler for unhandled errors."""
        logger.error(
            "Unhandled exception",
            exc_info=exc,
            path=request.url.path,
            method=request.method
        )
        
        if settings.debug:
            # In debug mode, show the actual error
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "detail": str(exc),
                    "type": type(exc).__name__
                }
            )
        else:
            # In production, hide error details
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "message": "An unexpected error occurred"
                }
            )
    
    return app


# Create the application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "predictpesa.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        workers=1 if settings.reload else settings.workers,
        log_level=settings.log_level.lower(),
        access_log=True,
    )
