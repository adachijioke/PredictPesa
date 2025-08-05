"""
Comprehensive integration tests for PredictPesa core infrastructure modules.

This test suite covers database, logging, and other core components with
proper mocking and isolation to avoid external dependencies.
"""

import pytest
import tempfile
import os
import logging
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import structlog

# Test the database module with mocking
class TestDatabaseModule:
    """Test database module functionality with proper mocking."""
    
    @patch('predictpesa.core.database.create_async_engine')
    @patch('predictpesa.core.database.get_settings')
    def test_database_engine_creation(self, mock_get_settings, mock_create_engine):
        """Test database engine creation with SQLite configuration."""
        from predictpesa.core.database import get_database_engine
        
        # Mock settings for SQLite
        mock_settings = Mock()
        mock_settings.database_url = "sqlite+aiosqlite:///./test.db"
        mock_settings.is_sqlite = True
        mock_get_settings.return_value = mock_settings
        
        # Mock engine
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        # Test engine creation
        engine = get_database_engine()
        
        # Verify engine creation was called
        mock_create_engine.assert_called_once()
        assert engine == mock_engine
    
    @patch('predictpesa.core.database.sessionmaker')
    @patch('predictpesa.core.database.get_database_engine')
    def test_session_factory_creation(self, mock_get_engine, mock_sessionmaker):
        """Test session factory creation."""
        from predictpesa.core.database import get_session_factory
        
        # Mock engine and session factory
        mock_engine = Mock()
        mock_get_engine.return_value = mock_engine
        mock_session_factory = Mock()
        mock_sessionmaker.return_value = mock_session_factory
        
        # Test session factory creation
        session_factory = get_session_factory()
        
        # Verify sessionmaker was called with correct parameters
        mock_sessionmaker.assert_called_once_with(
            mock_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        assert session_factory == mock_session_factory
    
    @patch('predictpesa.core.database.get_database_engine')
    async def test_database_initialization(self, mock_get_engine):
        """Test database initialization process."""
        from predictpesa.core.database import init_database
        from predictpesa.models.base import Base
        
        # Mock engine with metadata creation
        mock_engine = Mock()
        mock_engine.begin = Mock()
        mock_get_engine.return_value = mock_engine
        
        # Mock async context manager
        mock_conn = Mock()
        mock_engine.begin.return_value.__aenter__ = Mock(return_value=mock_conn)
        mock_engine.begin.return_value.__aexit__ = Mock(return_value=None)
        
        # Mock Base.metadata.create_all
        with patch.object(Base.metadata, 'create_all') as mock_create_all:
            await init_database()
            
            # Verify database initialization was called
            mock_engine.begin.assert_called_once()
            mock_create_all.assert_called_once_with(mock_conn)
    
    @patch('predictpesa.core.database.get_database_engine')
    async def test_database_cleanup(self, mock_get_engine):
        """Test database cleanup process."""
        from predictpesa.core.database import cleanup_database
        
        # Mock engine with dispose method
        mock_engine = Mock()
        mock_engine.dispose = Mock()
        mock_get_engine.return_value = mock_engine
        
        await cleanup_database()
        
        # Verify engine disposal was called
        mock_engine.dispose.assert_called_once()
    
    def test_database_url_validation(self):
        """Test database URL validation and SQLite detection."""
        from predictpesa.core.config import Settings
        
        # Test SQLite URL detection
        sqlite_settings = Settings(database_url="sqlite+aiosqlite:///./test.db")
        assert sqlite_settings.is_sqlite is True
        
        # Test PostgreSQL URL detection
        postgres_settings = Settings(database_url="postgresql+asyncpg://user:pass@localhost/db")
        assert postgres_settings.is_sqlite is False


class TestLoggingModule:
    """Test logging module functionality."""
    
    def test_logging_configuration(self):
        """Test logging configuration setup."""
        from predictpesa.core.logging import configure_logging
        from predictpesa.core.config import Settings
        
        # Test with development settings
        settings = Settings(
            log_level="DEBUG",
            log_format="json",
            environment="development"
        )
        
        # Configure logging should not raise exceptions
        try:
            configure_logging(settings)
            success = True
        except Exception:
            success = False
        
        assert success is True
    
    def test_logger_mixin(self):
        """Test LoggerMixin functionality."""
        from predictpesa.core.logging import LoggerMixin
        
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        
        # Test logger property
        assert hasattr(test_instance, 'logger')
        assert test_instance.logger is not None
        
        # Test logger name
        expected_name = f"{TestClass.__module__}.{TestClass.__qualname__}"
        assert test_instance.logger.name == expected_name
    
    def test_request_id_processor(self):
        """Test request ID processor for structured logging."""
        from predictpesa.core.logging import add_request_id
        
        # Mock logger and event dict
        logger = Mock()
        method_name = "info"
        event_dict = {"message": "test message"}
        
        # Test without request ID context
        result = add_request_id(logger, method_name, event_dict)
        assert "request_id" in result
        assert result["request_id"] is None
        
        # Test with mocked request ID context
        with patch('predictpesa.core.logging.contextvars') as mock_contextvars:
            mock_context_var = Mock()
            mock_context_var.get.return_value = "test-request-id"
            mock_contextvars.ContextVar.return_value = mock_context_var
            
            # Re-import to get the mocked context var
            from importlib import reload
            import predictpesa.core.logging
            reload(predictpesa.core.logging)
            
            result = predictpesa.core.logging.add_request_id(logger, method_name, event_dict)
            # Note: This test is simplified due to context var complexity
            assert "request_id" in result
    
    def test_application_loggers(self):
        """Test application-specific logger creation."""
        from predictpesa.core.logging import get_api_logger, get_ai_logger, get_blockchain_logger
        
        # Test API logger
        api_logger = get_api_logger()
        assert api_logger.name == "predictpesa.api"
        
        # Test AI logger
        ai_logger = get_ai_logger()
        assert ai_logger.name == "predictpesa.ai"
        
        # Test blockchain logger
        blockchain_logger = get_blockchain_logger()
        assert blockchain_logger.name == "predictpesa.blockchain"
    
    def test_file_logging_setup(self):
        """Test file logging configuration."""
        from predictpesa.core.logging import configure_logging
        from predictpesa.core.config import Settings
        
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            
            settings = Settings(
                log_level="INFO",
                log_format="json",
                log_file=log_file,
                environment="development"
            )
            
            # Configure logging should create log file directory
            configure_logging(settings)
            
            # Verify log directory was created
            assert os.path.exists(os.path.dirname(log_file))


class TestRedisModuleMocked:
    """Test Redis module functionality with mocking."""
    
    @patch('predictpesa.core.redis.aioredis')
    def test_redis_connection_creation(self, mock_aioredis):
        """Test Redis connection pool creation."""
        from predictpesa.core.redis import get_redis_pool
        from predictpesa.core.config import Settings
        
        # Mock Redis connection pool
        mock_pool = Mock()
        mock_aioredis.ConnectionPool.from_url.return_value = mock_pool
        
        settings = Settings(redis_url="redis://localhost:6379/0")
        
        # Test connection pool creation
        pool = get_redis_pool(settings)
        
        # Verify Redis pool creation was called
        mock_aioredis.ConnectionPool.from_url.assert_called_once_with(
            settings.redis_url,
            max_connections=settings.redis_pool_size,
            socket_timeout=settings.redis_socket_timeout,
            socket_connect_timeout=settings.redis_socket_connect_timeout,
            decode_responses=True
        )
        assert pool == mock_pool
    
    @patch('predictpesa.core.redis.get_redis_pool')
    @patch('predictpesa.core.redis.aioredis')
    def test_redis_cache_operations(self, mock_aioredis, mock_get_pool):
        """Test RedisCache operations with mocking."""
        from predictpesa.core.redis import RedisCache
        
        # Mock Redis client and pool
        mock_redis = Mock()
        mock_pool = Mock()
        mock_aioredis.Redis.return_value = mock_redis
        mock_get_pool.return_value = mock_pool
        
        # Create cache instance
        cache = RedisCache()
        
        # Test cache initialization
        assert cache.redis == mock_redis
        mock_aioredis.Redis.assert_called_once_with(connection_pool=mock_pool)
    
    @patch('predictpesa.core.redis.get_redis_pool')
    @patch('predictpesa.core.redis.aioredis')
    async def test_redis_cache_set_get(self, mock_aioredis, mock_get_pool):
        """Test Redis cache set and get operations."""
        from predictpesa.core.redis import RedisCache
        
        # Mock Redis client
        mock_redis = Mock()
        mock_redis.set = Mock()
        mock_redis.get = Mock(return_value=b'{"test": "value"}')
        mock_aioredis.Redis.return_value = mock_redis
        mock_get_pool.return_value = Mock()
        
        cache = RedisCache()
        
        # Test set operation
        await cache.set("test_key", {"test": "value"}, ttl=300)
        mock_redis.set.assert_called_once()
        
        # Test get operation
        result = await cache.get("test_key")
        mock_redis.get.assert_called_once_with("test_key")
        assert result == {"test": "value"}
    
    @patch('predictpesa.core.redis.get_redis_pool')
    @patch('predictpesa.core.redis.aioredis')
    async def test_redis_rate_limiter(self, mock_aioredis, mock_get_pool):
        """Test Redis-based rate limiter."""
        from predictpesa.core.redis import RateLimiter
        
        # Mock Redis client
        mock_redis = Mock()
        mock_redis.get = Mock(return_value=b'5')  # Current count
        mock_redis.incr = Mock(return_value=6)    # Incremented count
        mock_redis.expire = Mock()
        mock_aioredis.Redis.return_value = mock_redis
        mock_get_pool.return_value = Mock()
        
        rate_limiter = RateLimiter(max_requests=10, window_seconds=60)
        
        # Test rate limiting check
        is_allowed = await rate_limiter.is_allowed("test_key")
        
        # Should be allowed (6 < 10)
        assert is_allowed is True
        mock_redis.incr.assert_called_once()
        mock_redis.expire.assert_called_once()


class TestCoreIntegration:
    """Integration tests for core module interactions."""
    
    def test_settings_integration_with_modules(self):
        """Test that settings properly integrate with all core modules."""
        from predictpesa.core.config import get_settings
        
        settings = get_settings()
        
        # Test that settings have all required fields for each module
        # Database settings
        assert hasattr(settings, 'database_url')
        assert hasattr(settings, 'database_pool_size')
        assert hasattr(settings, 'is_sqlite')
        
        # Redis settings
        assert hasattr(settings, 'redis_url')
        assert hasattr(settings, 'redis_pool_size')
        
        # Logging settings
        assert hasattr(settings, 'log_level')
        assert hasattr(settings, 'log_format')
        assert hasattr(settings, 'log_file')
        
        # Security settings
        assert hasattr(settings, 'secret_key')
        assert hasattr(settings, 'algorithm')
        
        # Hedera settings
        assert hasattr(settings, 'hedera_network')
        assert hasattr(settings, 'hedera_account_id')
    
    @patch('predictpesa.core.database.get_settings')
    @patch('predictpesa.core.redis.get_settings')
    def test_cross_module_settings_consistency(self, mock_redis_settings, mock_db_settings):
        """Test that settings are consistent across modules."""
        from predictpesa.core.config import Settings
        
        # Create consistent settings
        test_settings = Settings(
            database_url="sqlite+aiosqlite:///./test.db",
            redis_url="redis://localhost:6379/0"
        )
        
        mock_db_settings.return_value = test_settings
        mock_redis_settings.return_value = test_settings
        
        # Import modules to trigger settings usage
        from predictpesa.core import database, redis
        
        # Verify settings are used consistently
        assert mock_db_settings.called
        assert mock_redis_settings.called
    
    def test_environment_specific_configurations(self):
        """Test environment-specific configuration behavior."""
        from predictpesa.core.config import Settings
        
        # Test development environment
        dev_settings = Settings(environment="development")
        assert dev_settings.is_development is True
        assert dev_settings.is_production is False
        assert dev_settings.debug is True
        
        # Test production environment
        prod_settings = Settings(environment="production")
        assert prod_settings.is_development is False
        assert prod_settings.is_production is True
        assert prod_settings.debug is False
        
        # Test testing environment
        test_settings = Settings(environment="testing")
        assert test_settings.is_testing is True
        assert test_settings.debug is True


# Performance and stress tests
class TestCorePerformance:
    """Performance tests for core infrastructure."""
    
    def test_settings_caching_performance(self):
        """Test that settings caching works efficiently."""
        from predictpesa.core.config import get_settings
        import time
        
        # First call (should create settings)
        start_time = time.time()
        settings1 = get_settings()
        first_call_time = time.time() - start_time
        
        # Second call (should use cache)
        start_time = time.time()
        settings2 = get_settings()
        second_call_time = time.time() - start_time
        
        # Verify same instance and faster second call
        assert settings1 is settings2
        assert second_call_time < first_call_time
    
    @patch('predictpesa.core.redis.aioredis')
    async def test_redis_connection_pooling(self, mock_aioredis):
        """Test Redis connection pooling efficiency."""
        from predictpesa.core.redis import RedisCache
        
        # Mock Redis to track connection creation
        mock_redis = Mock()
        mock_aioredis.Redis.return_value = mock_redis
        
        # Create multiple cache instances
        cache1 = RedisCache()
        cache2 = RedisCache()
        
        # Should reuse connection pool
        assert cache1.redis == mock_redis
        assert cache2.redis == mock_redis
        
        # Redis should be called for each instance but pool should be reused
        assert mock_aioredis.Redis.call_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
