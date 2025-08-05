"""Pydantic schemas for market operations."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, validator

from predictpesa.models.market import MarketCategory, MarketStatus, MarketType


class MarketCreate(BaseModel):
    """Schema for creating a new market."""
    
    title: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Market title/question"
    )
    
    description: str = Field(
        ...,
        min_length=20,
        max_length=2000,
        description="Detailed market description"
    )
    
    question: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="The prediction question"
    )
    
    category: MarketCategory = Field(
        ...,
        description="Market category"
    )
    
    market_type: MarketType = Field(
        default=MarketType.BINARY,
        description="Type of market (binary, multiple, scalar)"
    )
    
    end_date: datetime = Field(
        ...,
        description="When the market closes for new stakes"
    )
    
    tags: Optional[List[str]] = Field(
        default=None,
        description="Tags for categorization and search"
    )
    
    country_codes: Optional[List[str]] = Field(
        default=None,
        description="Relevant country codes"
    )
    
    use_ai_processing: bool = Field(
        default=False,
        description="Whether to use AI for market optimization"
    )
    
    allow_early_resolution: bool = Field(
        default=False,
        description="Allow resolution before end date"
    )
    
    @validator("end_date")
    def validate_end_date(cls, v):
        """Validate end date is in the future."""
        if v <= datetime.utcnow():
            raise ValueError("End date must be in the future")
        return v
    
    @validator("tags")
    def validate_tags(cls, v):
        """Validate tags list."""
        if v is not None:
            if len(v) > 10:
                raise ValueError("Maximum 10 tags allowed")
            for tag in v:
                if len(tag) > 50:
                    raise ValueError("Tag length cannot exceed 50 characters")
        return v


class MarketUpdate(BaseModel):
    """Schema for updating a market."""
    
    title: Optional[str] = Field(
        None,
        min_length=10,
        max_length=500
    )
    
    description: Optional[str] = Field(
        None,
        min_length=20,
        max_length=2000
    )
    
    tags: Optional[List[str]] = None
    
    is_featured: Optional[bool] = None
    
    allow_early_resolution: Optional[bool] = None


class MarketResponse(BaseModel):
    """Schema for market response."""
    
    id: UUID
    title: str
    description: str
    question: str
    category: MarketCategory
    market_type: MarketType
    status: MarketStatus
    
    creator_id: UUID
    
    start_date: datetime
    end_date: datetime
    resolution_date: Optional[datetime] = None
    settlement_date: Optional[datetime] = None
    
    # Financial data
    total_stake_amount: float
    yes_stake_amount: float
    no_stake_amount: float
    
    # Statistics
    total_participants: int
    yes_participants: int
    no_participants: int
    
    # Probabilities
    yes_probability: Optional[float] = None
    no_probability: Optional[float] = None
    
    # Resolution
    winning_outcome: Optional[str] = None
    resolution_confidence: Optional[float] = None
    
    # Metadata
    tags: Optional[List[str]] = None
    country_codes: Optional[List[str]] = None
    
    # AI data
    ai_generated: bool
    ai_confidence: Optional[float] = None
    
    # Features
    is_featured: bool
    is_trending: bool
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MarketListResponse(BaseModel):
    """Schema for paginated market list."""
    
    markets: List[MarketResponse]
    total: int
    skip: int
    limit: int


class MarketStatsResponse(BaseModel):
    """Schema for detailed market statistics."""
    
    market_id: UUID
    
    # Financial stats
    total_stake_amount: float
    yes_stake_amount: float
    no_stake_amount: float
    average_stake_size: float
    
    # Participant stats
    total_participants: int
    yes_participants: int
    no_participants: int
    unique_participants: int
    
    # Probability stats
    yes_probability: float
    no_probability: float
    probability_history: Optional[List[Dict[str, Any]]] = None
    
    # Volume stats
    daily_volume: Optional[float] = None
    weekly_volume: Optional[float] = None
    volume_trend: Optional[str] = None
    
    # Time stats
    time_remaining: Optional[int] = None  # seconds
    activity_score: Optional[float] = None
    
    # Resolution stats
    oracle_submissions: int
    resolution_confidence: Optional[float] = None
    
    class Config:
        from_attributes = True
