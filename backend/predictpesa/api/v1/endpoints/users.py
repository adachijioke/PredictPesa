"""User management endpoints."""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from predictpesa.api.deps import get_current_user, get_db
from predictpesa.models.user import User

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.get("/me")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile."""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role.value if current_user.role else "user",
        "is_verified": current_user.is_verified,
        "is_active": current_user.is_active,
    }


@router.put("/me")
async def update_user_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user profile."""
    logger.info("Profile update", user_id=current_user.id)
    
    # In a real implementation, update user in database
    return {"message": "Profile updated successfully"}


@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user statistics."""
    return {
        "total_stakes": 0,
        "total_winnings": 0.0,
        "success_rate": 0.0,
        "markets_created": 0,
        "reputation_score": 0
    }
