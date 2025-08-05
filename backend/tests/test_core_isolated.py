"""
Isolated tests for PredictPesa core infrastructure components.
Tests configuration, logging, and core functionality without module-level dependencies.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Any, Dict

import pytest
import structlog
from pydantic import ValidationError

# Import only safe core modules
from predictpesa.core.config import Settings, get_settings


class TestSettings:
    """Test the Settings configuration class."""
    
    def test_settings_defaults(self):
        """Test default configuration values."""
        test_settings = Settings()
        
        # Application defaults
        assert test_settings.app_name == "PredictPesa"
        assert test_settings.app_version == "1.0.0"
        assert test_settings.debug is False
        assert test_settings.environment == "development"
        
        # Server defaults
        assert test_settings.host == "0.0.0.0"
        assert test_settings.port == 8000
        assert test_settings.workers == 4
        
        # Security defaults
        assert test_settings.algorithm == "HS256"
        assert test_settings.access_token_expire_minutes == 30
        assert test_settings.refresh_token_expire_days == 7
        
        # CORS defaults
        assert "http://localhost:3000" in test_settings.cors_origins
        assert test_settings.cors_credentials is True
        assert "GET" in test_settings.cors_methods
    
    def test_settings_environment_variables(self):
        """Test settings loading from environment variables."""
        with patch.dict(os.environ, {
            'APP_NAME': 'TestApp',
            'DEBUG': 'true',
            'PORT': '9000',
            'ENVIRONMENT': 'testing'
        }):
            test_settings = Settings()
            assert test_settings.app_name == 'TestApp'
            assert test_settings.debug is True
            assert test_settings.port == 9000
            assert test_settings.environment == 'testing'
    
    def test_settings_validation_environment(self):
        """Test environment validation."""
        # Valid environments
        for env in ["development", "staging", "production", "testing"]:
            test_settings = Settings(environment=env)
            assert test_settings.environment == env
        
        # Invalid environment should raise validation error
        with pytest.raises(ValidationError):
            Settings(environment="invalid")
    
    def test_settings_validation_log_level(self):
        """Test log level validation."""
        # Valid log levels
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            test_settings = Settings(log_level=level)
            assert test_settings.log_level == level
        
        # Case insensitive
        test_settings = Settings(log_level="info")
        assert test_settings.log_level == "INFO"
        
        # Invalid log level should raise validation error
        with pytest.raises(ValidationError):
            Settings(log_level="INVALID")
    
    def test_settings_validation_hedera_network(self):
        """Test Hedera network validation."""
        # Valid networks
        for network in ["testnet", "mainnet", "previewnet"]:
            test_settings = Settings(hedera_network=network)
            assert test_settings.hedera_network == network
        
        # Invalid network should raise validation error
        with pytest.raises(ValidationError):
            Settings(hedera_network="invalid")
    
    def test_settings_properties(self):
        """Test settings property methods."""
        # Development mode
        dev_settings = Settings(environment="development")
        assert dev_settings.is_development is True
        assert dev_settings.is_production is False
        assert dev_settings.is_testing is False
        
        # Production mode
        prod_settings = Settings(environment="production")
        assert prod_settings.is_development is False
        assert prod_settings.is_production is True
        assert prod_settings.is_testing is False
        
        # Testing mode
        test_settings = Settings(environment="testing")
        assert test_settings.is_development is False
        assert test_settings.is_production is False
        assert test_settings.is_testing is True
    
    def test_get_settings_cached(self):
        """Test that get_settings returns cached instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2
    
    def test_settings_database_configuration(self):
        """Test database configuration settings."""
        test_settings = Settings()
        
        assert test_settings.database_url is not None
        assert test_settings.database_pool_size > 0
        assert test_settings.database_max_overflow > 0
        assert test_settings.database_pool_timeout > 0
        assert test_settings.database_pool_recycle > 0
    
    def test_settings_redis_configuration(self):
        """Test Redis configuration settings."""
        test_settings = Settings()
        
        assert test_settings.redis_url is not None
        assert test_settings.redis_pool_size > 0
        assert test_settings.redis_socket_timeout > 0
        assert test_settings.redis_socket_connect_timeout > 0
    
    def test_settings_hedera_configuration(self):
        """Test Hedera configuration settings."""
        test_settings = Settings()
        
        assert test_settings.hedera_network in ["testnet", "mainnet", "previewnet"]
        assert test_settings.hedera_mirror_node_url is not None
        assert test_settings.hedera_consensus_node_url is not None
    
    def test_settings_feature_flags(self):
        """Test feature flag settings."""
        test_settings = Settings()
        
        # Feature flags should be boolean
        assert isinstance(test_settings.enable_market_creation, bool)
        assert isinstance(test_settings.enable_staking, bool)
        assert isinstance(test_settings.enable_ai_suggestions, bool)
        assert isinstance(test_settings.enable_mobile_ussd, bool)
        assert isinstance(test_settings.enable_synthetic_indices, bool)
        assert isinstance(test_settings.enable_yield_farming, bool)
    
    def test_settings_geographic_configuration(self):
        """Test geographic configuration settings."""
        test_settings = Settings()
        
        assert test_settings.default_timezone == "UTC"
        assert isinstance(test_settings.supported_countries, list)
        assert "NG" in test_settings.supported_countries  # Nigeria should be supported
        assert test_settings.default_currency == "USD"
        assert isinstance(test_settings.supported_currencies, list)
        assert "USD" in test_settings.supported_currencies


class TestLoggingIsolated:
    """Test logging configuration in isolation."""
    
    def test_logging_imports(self):
        """Test that logging module imports work."""
        from predictpesa.core import logging as core_logging
        
        # Check that key functions exist
        assert hasattr(core_logging, 'setup_logging')
        assert hasattr(core_logging, 'add_request_id')
        assert hasattr(core_logging, 'LoggerMixin')
        assert hasattr(core_logging, 'get_logger')
    
    def test_setup_logging_function(self):
        """Test setup_logging function."""
        from predictpesa.core.logging import setup_logging
        
        # Should not raise an exception
        setup_logging()
        
        # Check that structlog is configured
        assert structlog.is_configured()
    
    def test_add_request_id_processor(self):
        """Test request ID processor."""
        from predictpesa.core.logging import add_request_id
        
        logger = MagicMock()
        event_dict = {"message": "test"}
        
        # Without request ID
        result = add_request_id(logger, "info", event_dict)
        assert result == event_dict
        
        # With mocked request ID
        with patch('contextvars.ContextVar') as mock_context:
            mock_context.return_value.get.return_value = "test-request-id"
            result = add_request_id(logger, "info", event_dict)
            assert "request_id" in result
            assert result["request_id"] == "test-request-id"
    
    def test_logger_mixin(self):
        """Test LoggerMixin functionality."""
        from predictpesa.core.logging import LoggerMixin
        
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        logger = test_instance.logger
        
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'warning')
    
    def test_get_logger_function(self):
        """Test get_logger function."""
        from predictpesa.core.logging import get_logger
        
        logger = get_logger("test")
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
    
    def test_logging_with_file_output(self):
        """Test logging with file output."""
        from predictpesa.core.logging import setup_logging
        
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test.log"
            
            with patch('predictpesa.core.config.settings') as mock_settings:
                mock_settings.log_file = str(log_file)
                mock_settings.is_testing = False
                mock_settings.log_level = "INFO"
                mock_settings.log_format = "json"
                
                setup_logging()
                
                # Log file parent directory should be created
                assert log_file.parent.exists()


class TestDatabaseIsolated:
    """Test database configuration in isolation."""
    
    def test_database_settings_validation(self):
        """Test database settings validation."""
        test_settings = Settings()
        
        # Database URL should be configured
        assert test_settings.database_url is not None
        assert len(test_settings.database_url) > 0
        
        # Pool settings should be positive integers
        assert isinstance(test_settings.database_pool_size, int)
        assert test_settings.database_pool_size > 0
        
        assert isinstance(test_settings.database_max_overflow, int)
        assert test_settings.database_max_overflow > 0
        
        assert isinstance(test_settings.database_pool_timeout, int)
        assert test_settings.database_pool_timeout > 0
        
        assert isinstance(test_settings.database_pool_recycle, int)
        assert test_settings.database_pool_recycle > 0
    
    def test_database_url_sqlite_for_testing(self):
        """Test that SQLite is used for testing."""
        test_settings = Settings(environment="testing")
        
        if test_settings.is_testing:
            # Should use SQLite for testing
            assert "sqlite" in test_settings.database_url.lower()
    
    @pytest.mark.asyncio
    async def test_database_module_imports(self):
        """Test database module imports with mocking."""
        # Mock the problematic SQLAlchemy components
        with patch('predictpesa.core.database.create_async_engine') as mock_engine:
            with patch('predictpesa.core.database.async_sessionmaker') as mock_session:
                # Import after mocking
                from predictpesa.core import database
                
                # Verify the module has the expected functions
                assert hasattr(database, 'get_db')
                assert hasattr(database, 'init_db')
                assert hasattr(database, 'close_db')


class TestRedisIsolated:
    """Test Redis configuration in isolation."""
    
    def test_redis_settings_validation(self):
        """Test Redis settings validation."""
        test_settings = Settings()
        
        # Redis URL should be configured
        assert test_settings.redis_url is not None
        assert len(test_settings.redis_url) > 0
        
        # Pool settings should be positive integers
        assert isinstance(test_settings.redis_pool_size, int)
        assert test_settings.redis_pool_size > 0
        
        assert isinstance(test_settings.redis_socket_timeout, int)
        assert test_settings.redis_socket_timeout > 0
        
        assert isinstance(test_settings.redis_socket_connect_timeout, int)
        assert test_settings.redis_socket_connect_timeout > 0
    
    def test_redis_module_structure(self):
        """Test Redis module structure without initialization."""
        # Test that we can import the classes without triggering initialization
        with patch('predictpesa.core.redis.get_redis') as mock_get_redis:
            mock_get_redis.side_effect = RuntimeError("Not initialized")
            
            from predictpesa.core.redis import RedisCache, RateLimiter
            
            # Classes should be importable
            assert RedisCache is not None
            assert RateLimiter is not None
    
    @pytest.mark.asyncio
    async def test_redis_cache_functionality(self):
        """Test RedisCache functionality with mocking."""
        from predictpesa.core.redis import RedisCache
        
        # Mock Redis client
        mock_client = AsyncMock()
        
        with patch('predictpesa.core.redis.get_redis', return_value=mock_client):
            cache = RedisCache(prefix="test")
            
            # Test key creation
            key = cache._make_key("test_key")
            assert key == "test:test_key"
            
            # Test cache operations with mocked client
            mock_client.get.return_value = '{"test": "value"}'
            result = await cache.get("test_key")
            assert result == {"test": "value"}
            
            mock_client.set.return_value = True
            result = await cache.set("test_key", {"data": "value"})
            assert result is True
    
    @pytest.mark.asyncio
    async def test_rate_limiter_functionality(self):
        """Test RateLimiter functionality with mocking."""
        from predictpesa.core.redis import RateLimiter
        
        # Mock Redis client
        mock_client = AsyncMock()
        mock_pipe = AsyncMock()
        mock_client.pipeline.return_value = mock_pipe
        mock_pipe.execute.return_value = [5, True]  # Current count, expire result
        
        rate_limiter = RateLimiter(redis_client=mock_client)
        
        is_allowed, remaining = await rate_limiter.is_allowed("user:123", 10, 60)
        
        assert is_allowed is True
        assert remaining == 5  # 10 - 5
        
        mock_pipe.incr.assert_called_once_with("user:123")
        mock_pipe.expire.assert_called_once_with("user:123", 60)


class TestCoreIntegration:
    """Test integration between core components."""
    
    def test_settings_integration(self):
        """Test settings integration across components."""
        test_settings = Settings()
        
        # All major configuration sections should be present
        assert test_settings.database_url is not None
        assert test_settings.redis_url is not None
        assert test_settings.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert test_settings.hedera_network in ["testnet", "mainnet", "previewnet"]
    
    def test_environment_specific_settings(self):
        """Test environment-specific settings."""
        # Development settings
        dev_settings = Settings(environment="development")
        assert dev_settings.debug is False  # Default is False even in dev
        assert dev_settings.is_development is True
        
        # Production settings
        prod_settings = Settings(environment="production")
        assert prod_settings.is_production is True
        assert prod_settings.debug is False
        
        # Testing settings
        test_settings = Settings(environment="testing")
        assert test_settings.is_testing is True
    
    def test_configuration_completeness(self):
        """Test that all required configuration is present."""
        test_settings = Settings()
        
        # Core application settings
        assert test_settings.app_name
        assert test_settings.app_version
        assert test_settings.secret_key
        
        # Database settings
        assert test_settings.database_url
        assert test_settings.database_pool_size > 0
        
        # Redis settings
        assert test_settings.redis_url
        assert test_settings.redis_pool_size > 0
        
        # Hedera settings
        assert test_settings.hedera_network
        assert test_settings.hedera_mirror_node_url
        
        # Security settings
        assert test_settings.algorithm
        assert test_settings.access_token_expire_minutes > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
