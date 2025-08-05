"""Oracle models for market resolution data."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum as PyEnum
import uuid

from sqlalchemy import String, Numeric, DateTime, Text, Enum, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from predictpesa.models.base import Base


class OracleSourceType(PyEnum):
    """Oracle source type enumeration."""
    CHAINLINK = "chainlink"
    REUTERS = "reuters"
    JOURNALIST = "journalist"
    DAO_VOTE = "dao_vote"
    API = "api"
    MANUAL = "manual"


class OracleDataStatus(PyEnum):
    """Oracle data status enumeration."""
    PENDING = "pending"
    VERIFIED = "verified"
    DISPUTED = "disputed"
    REJECTED = "rejected"


class OracleSource(Base):
    """Oracle source configuration."""
    
    __tablename__ = "oracle_sources"
    
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    
    source_type: Mapped[OracleSourceType] = mapped_column(
        Enum(OracleSourceType),
        nullable=False
    )
    
    endpoint_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    
    api_key_hash: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    weight: Mapped[float] = mapped_column(
        Numeric(precision=3, scale=2),
        default=1.0,
        nullable=False
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    
    reliability_score: Mapped[float] = mapped_column(
        Numeric(precision=3, scale=2),
        default=1.0,
        nullable=False
    )
    
    # Metadata
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    configuration: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True
    )
    
    # Relationships
    oracle_data: Mapped[List["OracleData"]] = relationship(
        "OracleData",
        back_populates="source",
        lazy="dynamic"
    )


class OracleData(Base):
    """Oracle data submissions for market resolution."""
    
    __tablename__ = "oracle_data"
    
    # Market reference
    market_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("markets.id"),
        nullable=False,
        index=True
    )
    
    # Source reference
    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("oracle_sources.id"),
        nullable=False,
        index=True
    )
    
    # Submitter (if manual)
    submitter_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )
    
    # Oracle data
    outcome: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    confidence: Mapped[float] = mapped_column(
        Numeric(precision=5, scale=4),
        nullable=False
    )
    
    status: Mapped[OracleDataStatus] = mapped_column(
        Enum(OracleDataStatus),
        default=OracleDataStatus.PENDING,
        nullable=False,
        index=True
    )
    
    # Evidence and proof
    evidence: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    data_hash: Mapped[Optional[str]] = mapped_column(
        String(66),  # IPFS hash or similar
        nullable=True
    )
    
    proof_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    
    # Blockchain integration
    hcs_topic_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    
    hcs_sequence_number: Mapped[Optional[int]] = mapped_column(
        nullable=True
    )
    
    transaction_hash: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    # Verification data
    verified_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )
    
    verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Raw data from source
    raw_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True
    )
    
    # Processing metadata
    processing_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    # Relationships
    market: Mapped["Market"] = relationship(
        "Market",
        back_populates="oracle_data"
    )
    
    source: Mapped["OracleSource"] = relationship(
        "OracleSource",
        back_populates="oracle_data"
    )
    
    submitter: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[submitter_id]
    )
    
    verifier: Mapped[Optional["User"]] = relationship(
        "User",
        foreign_keys=[verified_by]
    )
    
    @property
    def weighted_confidence(self) -> float:
        """Get confidence weighted by source reliability."""
        return float(self.confidence * self.source.weight * self.source.reliability_score)
    
    def is_verified(self) -> bool:
        """Check if oracle data is verified."""
        return self.status == OracleDataStatus.VERIFIED
    
    def can_be_used_for_resolution(self) -> bool:
        """Check if this data can be used for market resolution."""
        return (
            self.status == OracleDataStatus.VERIFIED and
            self.confidence >= 0.8 and
            self.source.is_active
        )
