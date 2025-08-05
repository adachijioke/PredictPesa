"""Market models for prediction markets."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum as PyEnum
import uuid

from sqlalchemy import (
    String, Boolean, DateTime, Text, Enum, Numeric, 
    Integer, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from predictpesa.models.base import Base


class MarketCategory(PyEnum):
    """Market category enumeration."""
    POLITICS = "politics"
    SPORTS = "sports"
    ECONOMICS = "economics"
    WEATHER = "weather"
    TECHNOLOGY = "technology"
    ENTERTAINMENT = "entertainment"
    HEALTH = "health"
    EDUCATION = "education"
    AGRICULTURE = "agriculture"
    ENERGY = "energy"
    OTHER = "other"


class MarketStatus(PyEnum):
    """Market status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    CLOSED = "closed"
    SETTLED = "settled"
    DISPUTED = "disputed"
    CANCELLED = "cancelled"


class MarketType(PyEnum):
    """Market type enumeration."""
    BINARY = "binary"  # Yes/No outcomes
    MULTIPLE = "multiple"  # Multiple choice outcomes
    SCALAR = "scalar"  # Numeric range outcomes


class Market(Base):
    """Market model for prediction markets."""
    
    __tablename__ = "markets"
    
    # Basic market information
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True
    )
    
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    question: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    category: Mapped[MarketCategory] = mapped_column(
        Enum(MarketCategory),
        nullable=False,
        index=True
    )
    
    market_type: Mapped[MarketType] = mapped_column(
        Enum(MarketType),
        default=MarketType.BINARY,
        nullable=False
    )
    
    status: Mapped[MarketStatus] = mapped_column(
        Enum(MarketStatus),
        default=MarketStatus.DRAFT,
        nullable=False,
        index=True
    )
    
    # Market creator
    creator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    # Timing
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
    
    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )
    
    resolution_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    settlement_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Blockchain integration
    contract_address: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=True
    )
    
    market_id_hash: Mapped[Optional[str]] = mapped_column(
        String(66),  # SHA-256 hash
        unique=True,
        index=True,
        nullable=True
    )
    
    yes_token_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    
    no_token_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    
    # Financial data
    total_stake_amount: Mapped[float] = mapped_column(
        Numeric(precision=18, scale=8),
        default=0.0,
        nullable=False
    )
    
    yes_stake_amount: Mapped[float] = mapped_column(
        Numeric(precision=18, scale=8),
        default=0.0,
        nullable=False
    )
    
    no_stake_amount: Mapped[float] = mapped_column(
        Numeric(precision=18, scale=8),
        default=0.0,
        nullable=False
    )
    
    creation_fee: Mapped[float] = mapped_column(
        Numeric(precision=18, scale=8),
        default=0.0,
        nullable=False
    )
    
    protocol_fee: Mapped[float] = mapped_column(
        Numeric(precision=18, scale=8),
        default=0.0,
        nullable=False
    )
    
    # Market statistics
    total_participants: Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )
    
    yes_participants: Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )
    
    no_participants: Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )
    
    # Probabilities (calculated)
    yes_probability: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=5, scale=4),
        nullable=True
    )
    
    no_probability: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=5, scale=4),
        nullable=True
    )
    
    # Resolution data
    winning_outcome: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    
    resolution_source: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True
    )
    
    resolution_confidence: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=5, scale=4),
        nullable=True
    )
    
    # Metadata
    tags: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True
    )
    
    market_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True
    )
    
    # Geographic data
    country_codes: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True
    )
    
    # AI/ML data
    ai_generated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    ai_confidence: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=5, scale=4),
        nullable=True
    )
    
    # Feature flags
    is_featured: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    is_trending: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    allow_early_resolution: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    # Relationships
    creator: Mapped["User"] = relationship(
        "User",
        back_populates="created_markets"
    )
    
    outcomes: Mapped[List["MarketOutcome"]] = relationship(
        "MarketOutcome",
        back_populates="market",
        cascade="all, delete-orphan"
    )
    
    stakes: Mapped[List["Stake"]] = relationship(
        "Stake",
        back_populates="market",
        lazy="dynamic"
    )
    
    oracle_data: Mapped[List["OracleData"]] = relationship(
        "OracleData",
        back_populates="market",
        lazy="dynamic"
    )
    
    @property
    def is_active(self) -> bool:
        """Check if market is currently active."""
        now = datetime.utcnow()
        return (
            self.status == MarketStatus.ACTIVE and
            self.start_date <= now <= self.end_date
        )
    
    @property
    def is_closed(self) -> bool:
        """Check if market is closed for new stakes."""
        return (
            self.status in [MarketStatus.CLOSED, MarketStatus.SETTLED] or
            datetime.utcnow() > self.end_date
        )
    
    @property
    def is_settled(self) -> bool:
        """Check if market is settled."""
        return self.status == MarketStatus.SETTLED
    
    @property
    def time_remaining(self) -> Optional[int]:
        """Get seconds remaining until market closes."""
        if self.is_closed:
            return 0
        
        now = datetime.utcnow()
        if now >= self.end_date:
            return 0
        
        return int((self.end_date - now).total_seconds())
    
    def calculate_probabilities(self) -> None:
        """Calculate outcome probabilities based on stake amounts."""
        if self.total_stake_amount == 0:
            self.yes_probability = 0.5
            self.no_probability = 0.5
        else:
            self.yes_probability = float(self.yes_stake_amount / self.total_stake_amount)
            self.no_probability = float(self.no_stake_amount / self.total_stake_amount)
    
    def can_stake(self) -> bool:
        """Check if new stakes can be placed on this market."""
        return (
            self.status == MarketStatus.ACTIVE and
            not self.is_closed and
            self.contract_address is not None
        )


class MarketOutcome(Base):
    """Market outcome model for multiple choice markets."""
    
    __tablename__ = "market_outcomes"
    
    # Market reference
    market_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("markets.id"),
        nullable=False,
        index=True
    )
    
    # Outcome details
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    outcome_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    # Token information
    token_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    
    # Financial data
    stake_amount: Mapped[float] = mapped_column(
        Numeric(precision=18, scale=8),
        default=0.0,
        nullable=False
    )
    
    participants: Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )
    
    probability: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=5, scale=4),
        nullable=True
    )
    
    # Resolution
    is_winning: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True
    )
    
    # Relationships
    market: Mapped["Market"] = relationship(
        "Market",
        back_populates="outcomes"
    )
