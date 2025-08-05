"""User schemas for PredictPesa."""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    country_code: Optional[str] = Field(None, min_length=2, max_length=2)


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response."""
    
    id: UUID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    country_code: Optional[str]
    role: str
    is_verified: bool
    is_active: bool
    
    class Config:
        from_attributes = True
