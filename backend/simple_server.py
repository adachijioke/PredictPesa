#!/usr/bin/env python3
"""
Simple test server for PredictPesa without database dependencies.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from predictpesa.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to PredictPesa API",
        "version": settings.app_version,
        "status": "running",
        "environment": settings.environment
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "PredictPesa Backend",
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug
    }

@app.get("/api/v1/markets")
async def get_markets():
    """Get markets endpoint (mock data)."""
    return {
        "markets": [
            {
                "id": "1",
                "title": "Test Market",
                "description": "A test prediction market",
                "category": "technology",
                "status": "active",
                "yes_probability": 0.65,
                "no_probability": 0.35
            }
        ],
        "total": 1
    }

@app.get("/api/v1/ai/analyze")
async def ai_analyze():
    """AI analysis endpoint (mock)."""
    return {
        "analysis": "Market conditions are favorable",
        "confidence": 0.85,
        "recommendation": "Consider staking on YES outcome"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Simple PredictPesa Server...")
    print(f"📖 API docs: http://localhost:8001/docs")
    print(f"🔍 Health check: http://localhost:8001/health")
    
    uvicorn.run(
        "simple_server:app",
        host=settings.host,
        port=8001,
        reload=settings.reload,
        log_level="info"
    )
