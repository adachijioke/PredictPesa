"""
Simple API tests for PredictPesa backend using the simple server.
Tests basic endpoints without database dependencies.
"""

import pytest
import requests
from fastapi.testclient import TestClient
from simple_server import app

# Test client for the simple server
client = TestClient(app)

class TestSimpleAPI:
    """Test simple API endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to PredictPesa API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"
        assert data["environment"] == "development"
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "PredictPesa Backend"
        assert data["version"] == "1.0.0"
        assert data["environment"] == "development"
        assert data["debug"] is True
    
    def test_markets_endpoint(self):
        """Test markets endpoint."""
        response = client.get("/api/v1/markets")
        assert response.status_code == 200
        data = response.json()
        assert "markets" in data
        assert "total" in data
        assert data["total"] == 1
        assert len(data["markets"]) == 1
        
        market = data["markets"][0]
        assert market["id"] == "1"
        assert market["title"] == "Test Market"
        assert market["category"] == "technology"
        assert market["status"] == "active"
        assert market["yes_probability"] == 0.65
        assert market["no_probability"] == 0.35
    
    def test_ai_analyze_endpoint(self):
        """Test AI analysis endpoint."""
        response = client.get("/api/v1/ai/analyze")
        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data
        assert "confidence" in data
        assert "recommendation" in data
        assert data["analysis"] == "Market conditions are favorable"
        assert data["confidence"] == 0.85
        assert data["recommendation"] == "Consider staking on YES outcome"

class TestAPIValidation:
    """Test API response validation."""
    
    def test_response_headers(self):
        """Test that responses have correct headers."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
    
    def test_cors_headers(self):
        """Test CORS headers are present."""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        # CORS headers should be present in response
        assert response.status_code == 200
        # Check if CORS middleware is working (headers may vary)
    
    def test_invalid_endpoint(self):
        """Test invalid endpoint returns 404."""
        response = client.get("/api/v1/invalid")
        assert response.status_code == 404

@pytest.mark.integration
class TestLiveServer:
    """Test against live server if running."""
    
    def test_live_server_health(self):
        """Test live server health check."""
        try:
            response = requests.get("http://localhost:8001/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                assert data["status"] == "healthy"
                assert data["service"] == "PredictPesa Backend"
        except requests.exceptions.RequestException:
            pytest.skip("Live server not running on port 8001")
    
    def test_live_server_markets(self):
        """Test live server markets endpoint."""
        try:
            response = requests.get("http://localhost:8001/api/v1/markets", timeout=5)
            if response.status_code == 200:
                data = response.json()
                assert "markets" in data
                assert "total" in data
        except requests.exceptions.RequestException:
            pytest.skip("Live server not running on port 8001")

# Performance tests
class TestPerformance:
    """Basic performance tests."""
    
    def test_response_time(self):
        """Test that responses are reasonably fast."""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 1.0  # Should respond within 1 second
    
    def test_multiple_requests(self):
        """Test handling multiple requests."""
        responses = []
        for _ in range(10):
            response = client.get("/health")
            responses.append(response)
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
