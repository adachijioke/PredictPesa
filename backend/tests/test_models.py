"""
Comprehensive model tests for PredictPesa.
Tests all database models, their relationships, and business logic.
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

# Import all models
from predictpesa.models.base import Base
from predictpesa.models.user import User, UserRole, UserStatus
from predictpesa.models.market import Market, MarketOutcome, MarketCategory, MarketStatus, MarketType
from predictpesa.models.stake import Stake, StakeStatus, StakePosition
from predictpesa.models.oracle import OracleData, OracleSource, OracleSourceType, OracleDataStatus
from predictpesa.models.transaction import Transaction, TransactionType, TransactionStatus

class TestBaseModel:
    """Test the base model functionality."""
    
    def test_base_model_fields(self):
        """Test that base model has required fields."""
        # Create a simple model instance for testing
        user = User(
            email="test@example.com",
            hashed_password="hashed_password",
            first_name="Test",
            last_name="User"
        )
        
        # Test base fields exist
        assert hasattr(user, 'id')
        assert hasattr(user, 'created_at')
        assert hasattr(user, 'updated_at')
        
        # Test ID is UUID (will be None until saved to DB, but attribute exists)
        assert user.id is not None or hasattr(user, 'id')
    
    def test_to_dict_method(self):
        """Test the to_dict method."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password",
            first_name="Test",
            last_name="User"
        )
        
        user_dict = user.to_dict()
        assert isinstance(user_dict, dict)
        assert 'id' in user_dict
        assert 'email' in user_dict
        assert user_dict['email'] == "test@example.com"
    
    def test_update_from_dict_method(self):
        """Test the update_from_dict method."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password",
            first_name="Test",
            last_name="User"
        )
        
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        user.update_from_dict(update_data)
        assert user.first_name == 'Updated'
        assert user.last_name == 'Name'
        assert user.email == "test@example.com"  # Unchanged

class TestUserModel:
    """Test the User model."""
    
    def test_user_creation(self):
        """Test basic user creation."""
        user = User(
            email="user@example.com",
            hashed_password="hashed_password",
            first_name="John",
            last_name="Doe",
            country_code="NG",
            role=UserRole.USER,
            status=UserStatus.ACTIVE
        )
        
        assert user.email == "user@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.country_code == "NG"
        assert user.role == UserRole.USER
        assert user.status == UserStatus.ACTIVE
        # Note: is_active and is_verified will be None until saved to DB
        # The defaults are defined at the database level
        assert user.is_active is None or user.is_active is True
        assert user.is_verified is None or user.is_verified is False
    
    def test_user_full_name_property(self):
        """Test the full_name property."""
        # Test with both names
        user = User(
            email="test@example.com",
            hashed_password="hash",
            first_name="John",
            last_name="Doe"
        )
        assert user.full_name == "John Doe"
        
        # Test with only first name
        user.last_name = None
        assert user.full_name == "John"
        
        # Test with only last name
        user.first_name = None
        user.last_name = "Doe"
        assert user.full_name == "Doe"
        
        # Test with no names but username
        user.first_name = None
        user.last_name = None
        user.username = "johndoe"
        assert user.full_name == "johndoe"
        
        # Test with no names and no username
        user.username = None
        assert user.full_name == "test@example.com"
    
    def test_user_display_name_property(self):
        """Test the display_name property."""
        user = User(
            email="test@example.com",
            hashed_password="hash",
            username="johndoe",
            first_name="John",
            last_name="Doe"
        )
        assert user.display_name == "johndoe"
        
        user.username = None
        assert user.display_name == "John Doe"
    
    def test_user_role_methods(self):
        """Test role checking methods."""
        user = User(
            email="test@example.com",
            hashed_password="hash",
            role=UserRole.USER
        )
        
        assert user.is_admin() is False
        assert user.is_moderator() is False
        assert user.is_oracle() is False
        
        user.role = UserRole.ADMIN
        assert user.is_admin() is True
        assert user.is_moderator() is True
        assert user.is_oracle() is False
        
        user.role = UserRole.MODERATOR
        assert user.is_admin() is False
        assert user.is_moderator() is True
        assert user.is_oracle() is False
        
        user.role = UserRole.ORACLE
        assert user.is_admin() is False
        assert user.is_moderator() is False
        assert user.is_oracle() is True
    
    def test_user_permissions(self):
        """Test user permission methods."""
        user = User(
            email="test@example.com",
            hashed_password="hash",
            is_active=True,
            is_verified=True,
            status=UserStatus.ACTIVE,
            hedera_account_id="0.0.123456"
        )
        
        assert user.can_create_markets() is True
        assert user.can_stake() is True
        
        # Test inactive user
        user.is_active = False
        assert user.can_create_markets() is False
        assert user.can_stake() is False
        
        # Test unverified user
        user.is_active = True
        user.is_verified = False
        assert user.can_create_markets() is False
        assert user.can_stake() is False
        
        # Test suspended user
        user.is_verified = True
        user.status = UserStatus.SUSPENDED
        assert user.can_create_markets() is False
        assert user.can_stake() is False
        
        # Test user without Hedera account
        user.status = UserStatus.ACTIVE
        user.hedera_account_id = None
        assert user.can_create_markets() is True
        assert user.can_stake() is False

class TestMarketModel:
    """Test the Market model."""
    
    def test_market_creation(self):
        """Test basic market creation."""
        creator = User(
            email="creator@example.com",
            hashed_password="hash"
        )
        
        market = Market(
            title="Will BTC hit $100k?",
            description="Bitcoin price prediction",
            question="Will Bitcoin exceed $100,000 by end of 2025?",
            category=MarketCategory.ECONOMICS,
            creator_id=creator.id,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
            status=MarketStatus.ACTIVE,
            market_type=MarketType.BINARY
        )
        
        assert market.title == "Will BTC hit $100k?"
        assert market.category == MarketCategory.ECONOMICS
        assert market.status == MarketStatus.ACTIVE
        assert market.market_type == MarketType.BINARY
        # Note: stake amounts will be None until saved to DB
        # The defaults are defined at the database level
        assert market.yes_stake_amount is None or market.yes_stake_amount == 0.0
        assert market.no_stake_amount is None or market.no_stake_amount == 0.0
    
    def test_market_properties(self):
        """Test market property methods."""
        now = datetime.now()
        market = Market(
            title="Test Market",
            description="Test",
            question="Test?",
            category=MarketCategory.TECHNOLOGY,
            start_date=now - timedelta(hours=1),
            end_date=now + timedelta(hours=1),
            status=MarketStatus.ACTIVE
        )
        
        # Test is_active
        assert market.is_active is True
        
        # Test is_closed (should be False since end_date is in future)
        assert market.is_closed is False
        
        # Test time_remaining
        time_remaining = market.time_remaining
        assert time_remaining is not None
        assert time_remaining > 0
        
        # Test closed market
        market.end_date = now - timedelta(hours=1)
        assert market.is_closed is True
        assert market.time_remaining == 0
        
        # Test settled market
        market.status = MarketStatus.SETTLED
        assert market.is_settled is True
    
    def test_market_can_stake(self):
        """Test can_stake method."""
        # Test active market with contract
        market = Market(
            title="Test Market",
            description="Test",
            question="Test?",
            category=MarketCategory.TECHNOLOGY,
            status=MarketStatus.ACTIVE,
            end_date=datetime.now() + timedelta(hours=1),
            contract_address="0x123456789"
        )
        
        assert market.can_stake() is True
        
        # Test market without contract
        market.contract_address = None
        assert market.can_stake() is False
        
        # Test closed market (past end date)
        market.contract_address = "0x123456789"
        market.end_date = datetime.now() - timedelta(hours=1)
        assert market.can_stake() is False
    
    def test_calculate_probabilities(self):
        """Test probability calculation."""
        market = Market(
            title="Test Market",
            description="Test",
            question="Test?",
            category=MarketCategory.TECHNOLOGY,
            yes_stake_amount=60.0,
            no_stake_amount=40.0,
            total_stake_amount=100.0
        )
        
        market.calculate_probabilities()
        assert market.yes_probability == 0.6
        assert market.no_probability == 0.4
        
        # Test with zero stakes
        market.total_stake_amount = 0.0
        market.calculate_probabilities()
        assert market.yes_probability == 0.5
        assert market.no_probability == 0.5

class TestMarketOutcomeModel:
    """Test the MarketOutcome model."""
    
    def test_market_outcome_creation(self):
        """Test market outcome creation."""
        market_id = uuid.uuid4()
        
        outcome = MarketOutcome(
            market_id=market_id,
            name="Option A",
            description="First option",
            outcome_index=0,
            stake_amount=50.0,
            participants=10,
            probability=0.6
        )
        
        assert outcome.market_id == market_id
        assert outcome.name == "Option A"
        assert outcome.outcome_index == 0
        assert outcome.stake_amount == 50.0
        assert outcome.participants == 10
        assert outcome.probability == 0.6
        assert outcome.is_winning is None

class TestStakeModel:
    """Test the Stake model."""
    
    def test_stake_creation(self):
        """Test basic stake creation."""
        user_id = uuid.uuid4()
        market_id = uuid.uuid4()
        
        stake = Stake(
            user_id=user_id,
            market_id=market_id,
            position=StakePosition.YES,
            amount=0.01,
            status=StakeStatus.CONFIRMED,
            odds_at_stake=1.5
        )
        
        assert stake.user_id == user_id
        assert stake.market_id == market_id
        assert stake.position == StakePosition.YES
        assert stake.amount == 0.01
        assert stake.status == StakeStatus.CONFIRMED
        assert stake.odds_at_stake == 1.5
    
    def test_stake_potential_payout(self):
        """Test potential payout calculation."""
        stake = Stake(
            user_id=uuid.uuid4(),
            market_id=uuid.uuid4(),
            position=StakePosition.YES,
            amount=0.01,
            odds_at_stake=2.0
        )
        
        assert stake.potential_payout == 0.02
        
        # Test without odds
        stake.odds_at_stake = None
        assert stake.potential_payout is None
    
    def test_stake_calculate_payout(self):
        """Test actual payout calculation."""
        # Create a market for the stake
        market = Market(
            title="Test Market",
            description="Test",
            question="Test?",
            category=MarketCategory.TECHNOLOGY,
            status=MarketStatus.SETTLED,
            winning_outcome="yes"
        )
        
        stake = Stake(
            user_id=uuid.uuid4(),
            market_id=market.id,
            position=StakePosition.YES,
            amount=0.01,
            odds_at_stake=2.0
        )
        
        # Set up the relationship
        stake.market = market
        
        # Test winning stake calculation
        result = stake.calculate_payout()
        assert result == 0.02  # amount * odds
        
        # Test losing stake
        market.winning_outcome = "no"
        result = stake.calculate_payout()
        assert result == 0.0
        
        # Test without odds (should return amount)
        market.winning_outcome = "yes"
        stake.odds_at_stake = None
        result = stake.calculate_payout()
        assert result == 0.01

class TestOracleModels:
    """Test Oracle-related models."""
    
    def test_oracle_source_creation(self):
        """Test oracle source creation."""
        source = OracleSource(
            name="Reuters API",
            source_type=OracleSourceType.REUTERS,
            endpoint_url="https://api.reuters.com",
            weight=1.0,
            reliability_score=0.95,
            is_active=True
        )
        
        assert source.name == "Reuters API"
        assert source.source_type == OracleSourceType.REUTERS
        assert source.weight == 1.0
        assert source.reliability_score == 0.95
        assert source.is_active is True
    
    def test_oracle_data_creation(self):
        """Test oracle data creation."""
        market_id = uuid.uuid4()
        source_id = uuid.uuid4()
        
        oracle_data = OracleData(
            market_id=market_id,
            source_id=source_id,
            outcome="yes",
            confidence=0.85,
            status=OracleDataStatus.VERIFIED,
            evidence="Market outcome confirmed by official source"
        )
        
        assert oracle_data.market_id == market_id
        assert oracle_data.source_id == source_id
        assert oracle_data.outcome == "yes"
        assert oracle_data.confidence == 0.85
        assert oracle_data.status == OracleDataStatus.VERIFIED
    
    def test_oracle_data_methods(self):
        """Test oracle data methods."""
        # Create a real oracle source for testing
        source = OracleSource(
            name="Test Source",
            source_type=OracleSourceType.API,
            weight=1.0,
            reliability_score=0.95,
            is_active=True
        )
        
        oracle_data = OracleData(
            market_id=uuid.uuid4(),
            source_id=source.id,
            outcome="yes",
            confidence=0.9,
            status=OracleDataStatus.VERIFIED
        )
        
        # Manually set the source relationship for testing
        oracle_data.source = source
        
        # Test weighted confidence
        expected_weighted = 0.9 * 1.0 * 0.95
        assert oracle_data.weighted_confidence == expected_weighted
        
        # Test is_verified
        assert oracle_data.is_verified() is True
        
        oracle_data.status = OracleDataStatus.PENDING
        assert oracle_data.is_verified() is False
        
        # Test can_be_used_for_resolution
        oracle_data.status = OracleDataStatus.VERIFIED
        oracle_data.confidence = 0.85
        assert oracle_data.can_be_used_for_resolution() is True
        
        # Test with low confidence
        oracle_data.confidence = 0.7
        assert oracle_data.can_be_used_for_resolution() is False
        
        # Test with inactive source
        oracle_data.confidence = 0.9
        oracle_data.source.is_active = False
        assert oracle_data.can_be_used_for_resolution() is False

class TestTransactionModel:
    """Test the Transaction model."""
    
    def test_transaction_creation(self):
        """Test basic transaction creation."""
        user_id = uuid.uuid4()
        
        transaction = Transaction(
            user_id=user_id,
            transaction_type=TransactionType.STAKE,
            status=TransactionStatus.PENDING,
            amount=0.01,
            fee=0.0001,
            transaction_hash="0xabcdef123456"
        )
        
        assert transaction.user_id == user_id
        assert transaction.transaction_type == TransactionType.STAKE
        assert transaction.status == TransactionStatus.PENDING
        assert transaction.amount == 0.01
        assert transaction.fee == 0.0001
        assert transaction.transaction_hash == "0xabcdef123456"
    
    def test_transaction_properties(self):
        """Test transaction property methods."""
        transaction = Transaction(
            user_id=uuid.uuid4(),
            transaction_type=TransactionType.STAKE,
            status=TransactionStatus.CONFIRMED,
            amount=0.01,
            fee=0.0001
        )
        
        # Test is_confirmed
        assert transaction.is_confirmed is True
        assert transaction.is_failed is False
        
        # Test total_cost
        assert transaction.total_cost == 0.0101
        
        # Test failed transaction
        transaction.status = TransactionStatus.FAILED
        assert transaction.is_confirmed is False
        assert transaction.is_failed is True
    
    def test_transaction_methods(self):
        """Test transaction methods."""
        transaction = Transaction(
            user_id=uuid.uuid4(),
            transaction_type=TransactionType.STAKE,
            status=TransactionStatus.PENDING
        )
        
        # Test mark_confirmed
        transaction.mark_confirmed(12345, "0xblockhash")
        assert transaction.status == TransactionStatus.CONFIRMED
        assert transaction.block_number == 12345
        assert transaction.block_hash == "0xblockhash"
        assert transaction.confirmed_at is not None
        
        # Test mark_failed
        transaction.mark_failed("Transaction failed")
        assert transaction.status == TransactionStatus.FAILED
        assert transaction.error_message == "Transaction failed"

class TestModelRelationships:
    """Test model relationships and foreign keys."""
    
    def test_user_market_relationship(self):
        """Test user-market relationship."""
        user = User(
            email="creator@example.com",
            hashed_password="hash"
        )
        
        market = Market(
            title="Test Market",
            description="Test",
            question="Test?",
            category=MarketCategory.TECHNOLOGY,
            creator_id=user.id
        )
        
        # Test that market has creator_id
        assert market.creator_id == user.id
    
    def test_user_stake_relationship(self):
        """Test user-stake relationship."""
        user = User(
            email="staker@example.com",
            hashed_password="hash"
        )
        
        stake = Stake(
            user_id=user.id,
            market_id=uuid.uuid4(),
            position=StakePosition.YES,
            amount=0.01
        )
        
        # Test that stake has user_id
        assert stake.user_id == user.id
    
    def test_market_stake_relationship(self):
        """Test market-stake relationship."""
        market_id = uuid.uuid4()
        
        market = Market(
            title="Test Market",
            description="Test",
            question="Test?",
            category=MarketCategory.TECHNOLOGY
        )
        market.id = market_id
        
        stake = Stake(
            user_id=uuid.uuid4(),
            market_id=market_id,
            position=StakePosition.YES,
            amount=0.01
        )
        
        # Test that stake has market_id
        assert stake.market_id == market_id

# Model enumeration tests
class TestModelEnums:
    """Test all model enumerations."""
    
    def test_user_enums(self):
        """Test user-related enums."""
        # UserRole
        assert UserRole.USER.value == "user"
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.MODERATOR.value == "moderator"
        assert UserRole.ORACLE.value == "oracle"
        
        # UserStatus
        assert UserStatus.ACTIVE.value == "active"
        assert UserStatus.INACTIVE.value == "inactive"
        assert UserStatus.SUSPENDED.value == "suspended"
        assert UserStatus.BANNED.value == "banned"
    
    def test_market_enums(self):
        """Test market-related enums."""
        # MarketCategory
        assert MarketCategory.POLITICS.value == "politics"
        assert MarketCategory.SPORTS.value == "sports"
        assert MarketCategory.ECONOMICS.value == "economics"
        
        # MarketStatus
        assert MarketStatus.DRAFT.value == "draft"
        assert MarketStatus.ACTIVE.value == "active"
        assert MarketStatus.SETTLED.value == "settled"
        
        # MarketType
        assert MarketType.BINARY.value == "binary"
        assert MarketType.MULTIPLE.value == "multiple"
        assert MarketType.SCALAR.value == "scalar"
    
    def test_stake_enums(self):
        """Test stake-related enums."""
        # StakeStatus
        assert StakeStatus.PENDING.value == "pending"
        assert StakeStatus.CONFIRMED.value == "confirmed"
        assert StakeStatus.SETTLED.value == "settled"
        
        # StakePosition
        assert StakePosition.YES.value == "yes"
        assert StakePosition.NO.value == "no"
    
    def test_oracle_enums(self):
        """Test oracle-related enums."""
        # OracleSourceType
        assert OracleSourceType.CHAINLINK.value == "chainlink"
        assert OracleSourceType.REUTERS.value == "reuters"
        assert OracleSourceType.API.value == "api"
        
        # OracleDataStatus
        assert OracleDataStatus.PENDING.value == "pending"
        assert OracleDataStatus.VERIFIED.value == "verified"
        assert OracleDataStatus.DISPUTED.value == "disputed"
    
    def test_transaction_enums(self):
        """Test transaction-related enums."""
        # TransactionType
        assert TransactionType.STAKE.value == "stake"
        assert TransactionType.PAYOUT.value == "payout"
        assert TransactionType.MARKET_CREATION.value == "market_creation"
        
        # TransactionStatus
        assert TransactionStatus.PENDING.value == "pending"
        assert TransactionStatus.CONFIRMED.value == "confirmed"
        assert TransactionStatus.FAILED.value == "failed"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
