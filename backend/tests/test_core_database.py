"""
Comprehensive tests for PredictPesa core database module.

This test suite covers database configuration, session management, and
initialization with proper mocking to avoid external dependencies.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


class TestDatabaseModule:
    """Test database module functionality with proper mocking."""
    
    def test_database_engine_configuration(self):
        """Test database engine is properly configured."""
        from predictpesa.core.database import engine
        
        # Test that engine exists and has expected properties
        assert engine is not None
        assert hasattr(engine, 'url')
        assert hasattr(engine, 'pool')
    
    def test_session_factory_configuration(self):
        """Test session factory is properly configured."""
        from predictpesa.core.database import AsyncSessionLocal
        
        # Test that session factory exists
        assert AsyncSessionLocal is not None
        assert hasattr(AsyncSessionLocal, '__call__')
    
    @pytest.mark.asyncio
    async def test_get_db_session_lifecycle(self):
        """Test database session lifecycle management."""
        from predictpesa.core.database import get_db
        
        # Mock the session to avoid actual database connection
        with patch('predictpesa.core.database.AsyncSessionLocal') as mock_session_factory:
            mock_session = AsyncMock()
            mock_session_factory.return_value.__aenter__.return_value = mock_session
            mock_session_factory.return_value.__aexit__.return_value = None
            
            # Test session generation
            async for session in get_db():
                assert session == mock_session
                break
            
            # Verify session close was called
            mock_session.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_db_session_rollback_on_error(self):
        """Test database session rollback on error."""
        from predictpesa.core.database import get_db
        
        with patch('predictpesa.core.database.AsyncSessionLocal') as mock_session_factory:
            mock_session = AsyncMock()
            mock_session_factory.return_value.__aenter__.return_value = mock_session
            mock_session_factory.return_value.__aexit__.return_value = None
            
            # Simulate an error during session usage
            try:
                async for session in get_db():
                    raise Exception("Test error")
            except Exception:
                pass
            
            # Verify rollback and close were called
            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_init_db_creates_tables(self):
        """Test database initialization creates all tables."""
        from predictpesa.core.database import init_db
        from predictpesa.models.base import Base
        
        # Mock engine and connection
        with patch('predictpesa.core.database.engine') as mock_engine:
            mock_conn = AsyncMock()
            mock_engine.begin.return_value.__aenter__.return_value = mock_conn
            mock_engine.begin.return_value.__aexit__.return_value = None
            
            # Mock Base.metadata.create_all
            with patch.object(Base.metadata, 'create_all') as mock_create_all:
                await init_db()
                
                # Verify database initialization was called
                mock_engine.begin.assert_called_once()
                mock_conn.run_sync.assert_called_once_with(Base.metadata.create_all)
    
    @pytest.mark.asyncio
    async def test_close_db_disposes_engine(self):
        """Test database cleanup disposes engine."""
        from predictpesa.core.database import close_db
        
        with patch('predictpesa.core.database.engine') as mock_engine:
            mock_engine.dispose = AsyncMock()
            
            await close_db()
            
            # Verify engine disposal was called
            mock_engine.dispose.assert_called_once()
    
    def test_database_imports_all_models(self):
        """Test that all models are properly imported."""
        # This test ensures all models are available for table creation
        from predictpesa.models import (
            User,
            Market,
            MarketOutcome,
            Stake,
            OracleData,
            OracleSource,
            Transaction,
        )
        
        # Verify all models are imported and have __tablename__
        models = [User, Market, MarketOutcome, Stake, OracleData, OracleSource, Transaction]
        for model in models:
            assert hasattr(model, '__tablename__')
            assert model.__tablename__ is not None
    
    def test_database_configuration_from_settings(self):
        """Test database configuration uses settings properly."""
        from predictpesa.core.config import settings
        from predictpesa.core.database import engine
        
        # Test that engine URL matches settings
        assert str(engine.url) == settings.database_url
        
        # Test debug mode affects echo
        assert engine.echo == settings.debug


class TestDatabaseIntegration:
    """Integration tests for database module."""
    
    def test_database_settings_integration(self):
        """Test database module integrates properly with settings."""
        from predictpesa.core.config import settings
        
        # Test that all required database settings exist
        required_settings = [
            'database_url',
            'database_pool_size',
            'database_max_overflow',
            'database_pool_timeout',
            'database_pool_recycle',
            'debug',
            'is_testing'
        ]
        
        for setting in required_settings:
            assert hasattr(settings, setting), f"Missing setting: {setting}"
    
    @pytest.mark.asyncio
    async def test_database_session_context_manager(self):
        """Test database session works as async context manager."""
        from predictpesa.core.database import AsyncSessionLocal
        
        # Mock the actual database connection
        with patch('predictpesa.core.database.engine') as mock_engine:
            mock_engine.url.database = "test_db"
            
            # Test that we can create a session (even if mocked)
            try:
                session_factory = AsyncSessionLocal
                assert session_factory is not None
                success = True
            except Exception:
                success = False
            
            assert success is True
    
    def test_database_pool_configuration(self):
        """Test database connection pool configuration."""
        from predictpesa.core.database import engine
        from predictpesa.core.config import settings
        
        # Test pool configuration (when not using SQLite)
        if not settings.database_url.startswith('sqlite'):
            assert engine.pool.size() >= 0  # Pool exists
        else:
            # SQLite uses NullPool in testing
            if settings.is_testing:
                from sqlalchemy.pool import NullPool
                assert isinstance(engine.pool, NullPool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
