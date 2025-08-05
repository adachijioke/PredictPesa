"""API v1 package."""

from fastapi import APIRouter

from predictpesa.api.v1.endpoints import (
    auth,
    users,
    markets,
    stakes,
    oracle,
    defi,
    health
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(markets.router, prefix="/markets", tags=["Markets"])
api_router.include_router(stakes.router, prefix="/stakes", tags=["Stakes"])
api_router.include_router(oracle.router, prefix="/oracle", tags=["Oracle"])
api_router.include_router(defi.router, prefix="/defi", tags=["DeFi"])

__all__ = ["api_router"]
