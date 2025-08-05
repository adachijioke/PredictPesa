"""User model for authentication and profile management."""

from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum

from sqlalchemy import String, Boolean, DateTime, Text, Enum, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from predictpesa.models.base import Base


class UserRole(PyEnum):
    """User role enumeration."""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
    ORACLE = "oracle"


class UserStatus(PyEnum):
    """User status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    BANNED = "banned"


class User(Base):
    """User model for authentication and profile management."""
    
    __tablename__ = "users"
    
    # Authentication fields
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    
    username: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=True
    )
    
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    # Profile fields
    first_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    last_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True
    )
    
    country_code: Mapped[Optional[str]] = mapped_column(
        String(2),
        nullable=True
    )
    
    timezone: Mapped[str] = mapped_column(
        String(50),
        default="UTC",
        nullable=False
    )
    
    preferred_currency: Mapped[str] = mapped_column(
        String(3),
        default="USD",
        nullable=False
    )
    
    bio: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    
    # Role and permissions
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )
    
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus),
        default=UserStatus.ACTIVE,
        nullable=False
    )
    
    # Blockchain integration
    hedera_account_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=True
    )
    
    wallet_address: Mapped[Optional[str]] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=True
    )
    
    # Statistics
    total_stakes: Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )
    
    total_winnings: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=18, scale=8),
        default=0.0,
        nullable=True
    )
    
    success_rate: Mapped[Optional[float]] = mapped_column(
        Numeric(precision=5, scale=4),
        default=0.0,
        nullable=True
    )
    
    reputation_score: Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )
    
    # Timestamps
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Relationships
    stakes: Mapped[List["Stake"]] = relationship(
        "Stake",
        back_populates="user",
        lazy="dynamic"
    )
    
    created_markets: Mapped[List["Market"]] = relationship(
        "Market",
        back_populates="creator",
        lazy="dynamic"
    )
    
    transactions: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        back_populates="user",
        lazy="dynamic"
    )
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.username or self.email
    
    @property
    def display_name(self) -> str:
        """Get user's display name."""
        return self.username or self.full_name
    
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role == UserRole.ADMIN
    
    def is_moderator(self) -> bool:
        """Check if user is moderator or admin."""
        return self.role in [UserRole.ADMIN, UserRole.MODERATOR]
    
    def is_oracle(self) -> bool:
        """Check if user is oracle."""
        return self.role == UserRole.ORACLE
    
    def can_create_markets(self) -> bool:
        """Check if user can create markets."""
        return (
            self.is_active and
            self.is_verified and
            self.status == UserStatus.ACTIVE
        )
    
    def can_stake(self) -> bool:
        """Check if user can place stakes."""
        return (
            self.is_active and
            self.is_verified and
            self.status == UserStatus.ACTIVE and
            self.hedera_account_id is not None
        )
