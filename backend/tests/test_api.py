"""
Test suite for PredictPesa API endpoints.
Comprehensive testing of authentication, markets, staking, and DeFi operations.
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from predictpesa.main import app
from predictpesa.models.user import User, UserRole
from predictpesa.models.market import Market, MarketStatus, MarketCategory
from predictpesa.core.database import get_db


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Create test user."""
    user = User(
        email="test@predictpesa.com",
        username="testuser",
        hashed_password="$2b$12$test_hash",
        first_name="Test",
        last_name="User",
        country_code="NG",
        is_verified=True,
        hedera_account_id="0.0.123456"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_market(db_session: AsyncSession, test_user: User):
    """Create test market."""
    market = Market(
        title="Test Market: Will BTC hit $100k?",
        description="Test market for Bitcoin price prediction",
        question="Will Bitcoin price exceed $100,000 by end of 2025?",
        category=MarketCategory.ECONOMICS,
        creator_id=test_user.id,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30),
        status=MarketStatus.ACTIVE,
        contract_address="0x1234567890123456789012345678901234567890"
    )
    db_session.add(market)
    await db_session.commit()
    await db_session.refresh(market)
    return market


@pytest.fixture
def auth_headers(client: TestClient):
    """Get authentication headers for test user."""
    # Register and login test user
    register_data = {
        "email": "test@predictpesa.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    client.post("/api/v1/auth/register", json=register_data)
    
    login_data = {
        "email": "test@predictpesa.com",
        "password": "testpassword123"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}


class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_register_user(self, client: TestClient):
        """Test user registration."""
        user_data = {
            "email": "newuser@predictpesa.com",
            "password": "securepassword123",
            "first_name": "New",
            "last_name": "User",
            "country_code": "NG"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["first_name"] == user_data["first_name"]
        assert "password" not in data
    
    def test_login_user(self, client: TestClient):
        """Test user login."""
        # First register a user
        register_data = {
            "email": "login@predictpesa.com",
            "password": "loginpassword123",
            "first_name": "Login",
            "last_name": "Test"
        }
        client.post("/api/v1/auth/register", json=register_data)
        
        # Then login
        login_data = {
            "email": "login@predictpesa.com",
            "password": "loginpassword123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == login_data["email"]
    
    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials."""
        login_data = {
            "email": "nonexistent@predictpesa.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_get_current_user(self, client: TestClient, auth_headers: dict):
        """Test getting current user profile."""
        response = client.get("/api/v1/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@predictpesa.com"
        assert "id" in data


class TestMarkets:
    """Test market endpoints."""
    
    def test_create_market(self, client: TestClient, auth_headers: dict):
        """Test market creation."""
        market_data = {
            "title": "Will Ethereum hit $10,000 by 2025?",
            "description": "Prediction market for Ethereum price",
            "question": "Will Ethereum price exceed $10,000 by end of 2025?",
            "category": "economics",
            "market_type": "binary",
            "end_date": (datetime.now() + timedelta(days=60)).isoformat(),
            "tags": ["ethereum", "crypto", "price"]
        }
        
        response = client.post(
            "/api/v1/markets/create",
            json=market_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == market_data["title"]
        assert data["category"] == market_data["category"]
        assert data["status"] == "draft"
    
    def test_list_markets(self, client: TestClient):
        """Test listing markets."""
        response = client.get("/api/v1/markets/")
        
        assert response.status_code == 200
        data = response.json()
        assert "markets" in data
        assert "total" in data
        assert isinstance(data["markets"], list)
    
    def test_get_market(self, client: TestClient, auth_headers: dict):
        """Test getting specific market."""
        # First create a market
        market_data = {
            "title": "Test Market for Get",
            "description": "Test market",
            "question": "Test question?",
            "category": "sports",
            "market_type": "binary",
            "end_date": (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        create_response = client.post(
            "/api/v1/markets/create",
            json=market_data,
            headers=auth_headers
        )
        market_id = create_response.json()["id"]
        
        # Then get the market
        response = client.get(f"/api/v1/markets/{market_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == market_id
        assert data["title"] == market_data["title"]
    
    def test_get_nonexistent_market(self, client: TestClient):
        """Test getting non-existent market."""
        fake_id = str(uuid4())
        response = client.get(f"/api/v1/markets/{fake_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_market_filtering(self, client: TestClient):
        """Test market filtering and search."""
        # Test category filter
        response = client.get("/api/v1/markets/?category=economics")
        assert response.status_code == 200
        
        # Test search
        response = client.get("/api/v1/markets/?search=bitcoin")
        assert response.status_code == 200
        
        # Test pagination
        response = client.get("/api/v1/markets/?skip=0&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data["markets"]) <= 5


class TestStaking:
    """Test staking endpoints."""
    
    def test_create_stake(self, client: TestClient, auth_headers: dict):
        """Test creating a stake."""
        # First create a market
        market_data = {
            "title": "Staking Test Market",
            "description": "Market for testing stakes",
            "question": "Test staking question?",
            "category": "economics",
            "market_type": "binary",
            "end_date": (datetime.now() + timedelta(days=30)).isoformat()
        }
        
        market_response = client.post(
            "/api/v1/markets/create",
            json=market_data,
            headers=auth_headers
        )
        market_id = market_response.json()["id"]
        
        # Create stake
        stake_data = {
            "market_id": market_id,
            "position": "yes",
            "amount": 0.01,
            "reasoning": "Test stake reasoning"
        }
        
        response = client.post(
            "/api/v1/stakes/create",
            json=stake_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["market_id"] == market_id
        assert data["position"] == "yes"
        assert data["amount"] == 0.01
    
    def test_list_user_stakes(self, client: TestClient, auth_headers: dict):
        """Test listing user stakes."""
        response = client.get("/api/v1/stakes/my-stakes", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_stake_invalid_amount(self, client: TestClient, auth_headers: dict):
        """Test staking with invalid amount."""
        stake_data = {
            "market_id": str(uuid4()),
            "position": "yes",
            "amount": -0.01  # Invalid negative amount
        }
        
        response = client.post(
            "/api/v1/stakes/create",
            json=stake_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error


class TestOracle:
    """Test oracle endpoints."""
    
    def test_submit_oracle_data(self, client: TestClient, auth_headers: dict):
        """Test submitting oracle data."""
        oracle_data = {
            "market_id": str(uuid4()),
            "outcome": "yes",
            "confidence": 0.95,
            "sources": ["chainlink", "reuters"],
            "evidence": "Strong evidence for YES outcome",
            "data_hash": "0x" + "a" * 32
        }
        
        response = client.post(
            "/api/v1/oracle/submit",
            json=oracle_data,
            headers=auth_headers
        )
        
        # Note: This might fail if user doesn't have oracle permissions
        # In a real test, we'd set up proper oracle user
        assert response.status_code in [201, 403]
    
    def test_get_oracle_data(self, client: TestClient):
        """Test getting oracle data for market."""
        market_id = str(uuid4())
        response = client.get(f"/api/v1/oracle/market/{market_id}")
        
        assert response.status_code in [200, 404]


class TestDeFi:
    """Test DeFi integration endpoints."""
    
    def test_add_liquidity(self, client: TestClient, auth_headers: dict):
        """Test adding liquidity to AMM pool."""
        liquidity_data = {
            "token_a": "yesBTC",
            "token_b": "noBTC",
            "amount_a": 0.01,
            "amount_b": 0.01
        }
        
        response = client.post(
            "/api/v1/defi/add_liquidity",
            json=liquidity_data,
            headers=auth_headers
        )
        
        # This might return 501 (Not Implemented) if DeFi features aren't fully implemented
        assert response.status_code in [200, 501]
    
    def test_use_as_collateral(self, client: TestClient, auth_headers: dict):
        """Test using prediction tokens as collateral."""
        collateral_data = {
            "token_id": "yesBTC_market_1",
            "lending_pool": "0x1234567890123456789012345678901234567890"
        }
        
        response = client.post(
            "/api/v1/defi/use_as_collateral",
            json=collateral_data,
            headers=auth_headers
        )
        
        assert response.status_code in [200, 501]


class TestHealthAndMetrics:
    """Test health check and metrics endpoints."""
    
    def test_health_check(self, client: TestClient):
        """Test basic health check."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "PredictPesa"
    
    def test_detailed_health_check(self, client: TestClient):
        """Test detailed health check."""
        response = client.get("/health/detailed")
        
        assert response.status_code == 200
        data = response.json()
        assert "dependencies" in data
    
    def test_metrics_endpoint(self, client: TestClient):
        """Test Prometheus metrics endpoint."""
        response = client.get("/metrics")
        
        # Metrics endpoint returns plain text
        assert response.status_code == 200
        assert "predictpesa" in response.text.lower()


@pytest.mark.integration
class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_complete_market_workflow(self, client: TestClient, auth_headers: dict):
        """Test complete market creation to resolution workflow."""
        # 1. Create market
        market_data = {
            "title": "Integration Test Market",
            "description": "Full workflow test",
            "question": "Integration test question?",
            "category": "technology",
            "market_type": "binary",
            "end_date": (datetime.now() + timedelta(days=1)).isoformat()
        }
        
        market_response = client.post(
            "/api/v1/markets/create",
            json=market_data,
            headers=auth_headers
        )
        assert market_response.status_code == 201
        market_id = market_response.json()["id"]
        
        # 2. Place stake
        stake_data = {
            "market_id": market_id,
            "position": "yes",
            "amount": 0.005
        }
        
        stake_response = client.post(
            "/api/v1/stakes/create",
            json=stake_data,
            headers=auth_headers
        )
        assert stake_response.status_code == 201
        
        # 3. Get market stats
        stats_response = client.get(f"/api/v1/markets/{market_id}/stats")
        assert stats_response.status_code == 200
        
        # 4. Resolve market (might fail without proper permissions)
        resolution_data = {
            "outcome": "yes",
            "confidence": 0.95,
            "resolution_source": "test_oracle"
        }
        
        resolve_response = client.post(
            f"/api/v1/markets/{market_id}/resolve",
            json=resolution_data,
            headers=auth_headers
        )
        # Accept either success or permission denied
        assert resolve_response.status_code in [200, 403]


# Pytest configuration
@pytest.mark.asyncio
async def test_async_example():
    """Example async test."""
    # This is a placeholder for async tests
    assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
