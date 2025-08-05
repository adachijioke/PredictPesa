"""Transaction model for blockchain operations."""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum as PyEnum
import uuid

from sqlalchemy import String, Numeric, DateTime, Text, Enum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from predictpesa.models.base import Base


class TransactionType(PyEnum):
    """Transaction type enumeration."""
    STAKE = "stake"
    PAYOUT = "payout"
    MARKET_CREATION = "market_creation"
    TOKEN_MINT = "token_mint"
    TOKEN_BURN = "token_burn"
    LIQUIDITY_ADD = "liquidity_add"
    LIQUIDITY_REMOVE = "liquidity_remove"
    SWAP = "swap"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"


class TransactionStatus(PyEnum):
    """Transaction status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Transaction(Base):
    """Transaction model for blockchain operations."""
    
    __tablename__ = "transactions"
    
    # User reference
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    # Transaction details
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType),
        nullable=False,
        index=True
    )
    
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus),
        default=TransactionStatus.PENDING,
        nullable=False,
        index=True
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
    
    block_hash: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    gas_used: Mapped[Optional[int]] = mapped_column(
        nullable=True
    )
    
    gas_price: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=18, scale=8),
        nullable=True
    )
    
    # Financial data
    amount: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=18, scale=8),
        nullable=True
    )
    
    fee: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=18, scale=8),
        nullable=True
    )
    
    # Token data
    token_address: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    token_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    
    token_amount: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=18, scale=8),
        nullable=True
    )
    
    # Contract interaction
    contract_address: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    function_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    # Related entities
    market_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("markets.id"),
        nullable=True,
        index=True
    )
    
    stake_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stakes.id"),
        nullable=True,
        index=True
    )
    
    # Metadata
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    raw_transaction_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True
    )
    
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    # Timing
    submitted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="transactions"
    )
    
    market: Mapped[Optional["Market"]] = relationship(
        "Market",
        foreign_keys=[market_id]
    )
    
    stake: Mapped[Optional["Stake"]] = relationship(
        "Stake",
        foreign_keys=[stake_id]
    )
    
    @property
    def is_confirmed(self) -> bool:
        """Check if transaction is confirmed."""
        return self.status == TransactionStatus.CONFIRMED
    
    @property
    def is_failed(self) -> bool:
        """Check if transaction failed."""
        return self.status == TransactionStatus.FAILED
    
    @property
    def total_cost(self) -> Optional[float]:
        """Calculate total transaction cost including fees."""
        if self.amount is None:
            return None
        
        fee = self.fee or 0
        return float(self.amount + fee)
    
    def mark_confirmed(self, block_number: int, block_hash: str) -> None:
        """Mark transaction as confirmed."""
        self.status = TransactionStatus.CONFIRMED
        self.block_number = block_number
        self.block_hash = block_hash
        self.confirmed_at = datetime.utcnow()
    
    def mark_failed(self, error_message: str) -> None:
        """Mark transaction as failed."""
        self.status = TransactionStatus.FAILED
        self.error_message = error_message
