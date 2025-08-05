"""Stake schemas for PredictPesa."""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class StakeCreate(BaseModel):
    """Schema for creating a new stake."""
    
    market_id: UUID = Field(..., description="Market ID to stake on")
    position: str = Field(..., description="Position: 'yes' or 'no'")
    amount: float = Field(..., gt=0, description="Stake amount in BTC")
    reasoning: Optional[str] = Field(None, max_length=1000, description="User reasoning")
    
    @validator("position")
    def validate_position(cls, v):
        """Validate position is yes or no."""
        if v.lower() not in ["yes", "no"]:
            raise ValueError("Position must be 'yes' or 'no'")
        return v.lower()
    
    @validator("amount")
    def validate_amount(cls, v):
        """Validate stake amount is within limits."""
        if v < 0.001:
            raise ValueError("Minimum stake amount is 0.001 BTC")
        if v > 10.0:
            raise ValueError("Maximum stake amount is 10.0 BTC")
        return v


class StakeResponse(BaseModel):
    """Schema for stake response."""
    
    id: UUID
    market_id: UUID
    user_id: UUID
    position: str
    amount: float
    status: str
    transaction_hash: Optional[str]
    created_at: str
    
    class Config:
        from_attributes = True
