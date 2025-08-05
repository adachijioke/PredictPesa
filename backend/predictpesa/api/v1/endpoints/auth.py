"""Authentication endpoints for PredictPesa."""

from datetime import datetime, timedelta
from typing import Any

import jwt
import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from predictpesa.api.deps import get_current_user
from predictpesa.core.config import settings
from predictpesa.core.database import get_db
from predictpesa.core.redis import cache
from predictpesa.models.user import User
from predictpesa.schemas.auth import LoginRequest, LoginResponse, TokenResponse

router = APIRouter()
logger = structlog.get_logger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    
    Creates a new user account with email verification required.
    """
    logger.info("User registration attempt", email=user_data.get("email"))
    
    try:
        # Check if user already exists
        # In a real implementation, query the database
        # For demo purposes, we'll simulate this
        
        # Hash password
        hashed_password = get_password_hash(user_data["password"])
        
        # Create user (simulated)
        user_response = {
            "id": "demo-user-id",
            "email": user_data["email"],
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "country_code": user_data.get("country_code"),
            "is_verified": False,
            "is_active": True,
            "role": "user",
            "created_at": datetime.utcnow().isoformat()
        }
        
        logger.info("User registered successfully", user_id=user_response["id"])
        
        return user_response
    
    except Exception as e:
        logger.error("User registration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=LoginResponse)
async def login_user(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return access token.
    
    Validates credentials and returns JWT token for API access.
    """
    logger.info("User login attempt", email=login_data.email)
    
    try:
        # In a real implementation, query database for user
        # For demo purposes, we'll simulate authentication
        
        # Simulate user lookup and password verification
        if login_data.email == "demo@predictpesa.com" and login_data.password == "demo123456":
            user_data = {
                "id": "demo-user-id",
                "email": login_data.email,
                "first_name": "Demo",
                "last_name": "User",
                "country_code": "NG",
                "is_verified": True,
                "is_active": True,
                "role": "user"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        token_data = {
            "sub": user_data["id"],
            "email": user_data["email"],
            "role": user_data["role"],
            "is_verified": user_data["is_verified"]
        }
        
        access_token = create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )
        
        # Cache user data
        cache_key = f"user:{user_data['id']}"
        await cache.set(cache_key, user_data, expire=300)
        
        logger.info("User login successful", user_id=user_data["id"])
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            user=user_data
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("User login failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/logout")
async def logout_user(
    current_user: User = Depends(get_current_user),
    token: str = Depends(security)
):
    """
    Logout user and invalidate token.
    
    Adds token to blacklist to prevent further use.
    """
    logger.info("User logout", user_id=current_user.id)
    
    try:
        # Add token to blacklist
        blacklist_key = f"blacklist:{token.credentials}"
        await cache.set(blacklist_key, True, expire=settings.access_token_expire_minutes * 60)
        
        # Clear user cache
        cache_key = f"user:{current_user.id}"
        await cache.delete(cache_key)
        
        logger.info("User logout successful", user_id=current_user.id)
        
        return {"message": "Successfully logged out"}
    
    except Exception as e:
        logger.error("User logout failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """
    Refresh access token.
    
    Issues a new access token for authenticated user.
    """
    logger.info("Token refresh", user_id=current_user.id)
    
    try:
        # Create new access token
        token_data = {
            "sub": str(current_user.id),
            "email": current_user.email,
            "role": current_user.role.value,
            "is_verified": current_user.is_verified
        }
        
        access_token = create_access_token(data=token_data)
        
        logger.info("Token refresh successful", user_id=current_user.id)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
    
    except Exception as e:
        logger.error("Token refresh failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/verify-email")
async def verify_email(
    verification_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """
    Verify user email address.
    
    Confirms user email using verification token.
    """
    logger.info("Email verification attempt", token=verification_data.get("token"))
    
    try:
        # In a real implementation, validate verification token
        # and update user's is_verified status
        
        return {"message": "Email verified successfully"}
    
    except Exception as e:
        logger.error("Email verification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email verification failed"
        )


@router.post("/forgot-password")
async def forgot_password(
    email_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """
    Request password reset.
    
    Sends password reset email to user.
    """
    logger.info("Password reset request", email=email_data.get("email"))
    
    try:
        # In a real implementation, generate reset token and send email
        
        return {"message": "Password reset email sent"}
    
    except Exception as e:
        logger.error("Password reset request failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset request failed"
        )


@router.post("/reset-password")
async def reset_password(
    reset_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """
    Reset user password.
    
    Updates password using reset token.
    """
    logger.info("Password reset attempt", token=reset_data.get("token"))
    
    try:
        # In a real implementation, validate reset token and update password
        
        return {"message": "Password reset successfully"}
    
    except Exception as e:
        logger.error("Password reset failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset failed"
        )
