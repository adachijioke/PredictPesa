"""Stake model for user predictions."""

from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum
import uuid

from sqlalchemy import String, Numeric, DateTime, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from predictpesa.models.base import Base


class StakeStatus(PyEnum):
    """Stake status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SETTLED = "settled"
    CANCELLED = "cancelled"


class StakePosition(PyEnum):
    """Stake position enumeration."""
    YES = "yes"
    NO = "no"


class Stake(Base):
    """Stake model for user predictions."""
    
    __tablename__ = "stakes"
    
    # User and market references
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    market_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("markets.id"),
        nullable=False,
        index=True
    )
    
    # Stake details
    position: Mapped[StakePosition] = mapped_column(
        Enum(StakePosition),
        nullable=False
    )
    
    amount: Mapped[float] = mapped_column(
        Numeric(precision=18, scale=8),
        nullable=False
    )
    
    status: Mapped[StakeStatus] = mapped_column(
        Enum(StakeStatus),
        default=StakeStatus.PENDING,
        nullable=False,
        index=True
    )
    
    # Token information
    token_amount: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=18, scale=8),
        nullable=True
    )
    
    token_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    
    # Blockchain data
    transaction_hash: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=True
    )
    
    block_number: Mapped[Optional[int]] = mapped_column(
        nullable=True
    )
    
    # Settlement data
    payout_amount: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=18, scale=8),
        nullable=True
    )
    
    payout_transaction_hash: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    settled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # User reasoning
    reasoning: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    # Metadata
    odds_at_stake: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=8, scale=4),
        nullable=True
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="stakes"
    )
    
    market: Mapped["Market"] = relationship(
        "Market",
        back_populates="stakes"
    )
    
    @property
    def is_winning(self) -> Optional[bool]:
        """Check if this stake is on the winning side."""
        if not self.market.is_settled:
            return None
        
        return self.position.value == self.market.winning_outcome
    
    @property
    def potential_payout(self) -> Optional[float]:
        """Calculate potential payout based on current odds."""
        if not self.odds_at_stake:
            return None
        
        return float(self.amount * self.odds_at_stake)
    
    def calculate_payout(self) -> float:
        """Calculate actual payout for winning stakes."""
        if not self.is_winning:
            return 0.0
        
        # Simple payout calculation - in reality this would be more complex
        # involving the total pool and winning/losing ratios
        if self.odds_at_stake:
            return float(self.amount * self.odds_at_stake)
        
        return float(self.amount)  # 1:1 payout as fallback
