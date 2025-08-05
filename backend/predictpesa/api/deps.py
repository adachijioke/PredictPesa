"""
API dependencies for PredictPesa.
Common dependencies used across API endpoints.
"""

from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from predictpesa.core.database import get_db
from predictpesa.models.user import User


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from request.
    
    Args:
        request: HTTP request with user data in state
        db: Database session
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If user not authenticated or not found
    """
    # Get user data from request state (set by auth middleware)
    user_data = getattr(request.state, "user", None)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user_id = user_data.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user data"
        )
    
    # In a real implementation, we might want to fetch fresh user data
    # from the database to ensure it's up-to-date
    # For now, we'll create a user object from the cached data
    user = User(
        id=user_id,
        email=user_data.get("email"),
        role=user_data.get("role", "user"),
        is_verified=user_data.get("is_verified", False),
        is_active=True
    )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user.
    
    Args:
        current_user: Current user from auth
        
    Returns:
        Active user
        
    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current verified user.
    
    Args:
        current_user: Current active user
        
    Returns:
        Verified user
        
    Raises:
        HTTPException: If user is not verified
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required"
        )
    
    return current_user


async def get_admin_user(
    current_user: User = Depends(get_current_verified_user)
) -> User:
    """
    Get current admin user.
    
    Args:
        current_user: Current verified user
        
    Returns:
        Admin user
        
    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user


async def get_oracle_user(
    current_user: User = Depends(get_current_verified_user)
) -> User:
    """
    Get current oracle user.
    
    Args:
        current_user: Current verified user
        
    Returns:
        Oracle user
        
    Raises:
        HTTPException: If user is not oracle
    """
    if not (current_user.is_oracle() or current_user.is_admin()):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Oracle privileges required"
        )
    
    return current_user
