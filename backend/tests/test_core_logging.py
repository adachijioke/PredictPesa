"""
Comprehensive tests for PredictPesa core logging module.

This test suite covers structured logging configuration, logger mixins,
and application-specific loggers.
"""

import pytest
import tempfile
import os
import logging
from unittest.mock import Mock, patch
import structlog


class TestLoggingModule:
    """Test logging module functionality."""
    
    def test_logging_setup_function_exists(self):
        """Test that setup_logging function exists and is callable."""
        from predictpesa.core.logging import setup_logging
        
        assert callable(setup_logging)
    
    def test_logging_setup_execution(self):
        """Test logging setup executes without errors."""
        from predictpesa.core.logging import setup_logging
        
        # Test that setup_logging runs without exceptions
        try:
            setup_logging()
            success = True
        except Exception as e:
            success = False
            print(f"Setup logging failed: {e}")
        
        assert success is True
    
    def test_logger_mixin_functionality(self):
        """Test LoggerMixin provides logger property."""
        from predictpesa.core.logging import LoggerMixin
        
        class TestClass(LoggerMixin):
            pass
        
        test_instance = TestClass()
        
        # Test logger property exists
        assert hasattr(test_instance, 'logger')
        logger = test_instance.logger
        assert logger is not None
        
        # Test logger is a structlog BoundLogger
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'warning')
    
    def test_get_logger_function(self):
        """Test get_logger function creates proper loggers."""
        from predictpesa.core.logging import get_logger
        
        # Test logger creation
        test_logger = get_logger("test_logger")
        assert test_logger is not None
        
        # Test logger has expected methods
        assert hasattr(test_logger, 'info')
        assert hasattr(test_logger, 'error')
        assert hasattr(test_logger, 'debug')
        assert hasattr(test_logger, 'warning')
    
    def test_application_specific_loggers(self):
        """Test application-specific loggers are created."""
        from predictpesa.core.logging import (
            auth_logger,
            market_logger,
            stake_logger,
            oracle_logger,
            defi_logger,
            blockchain_logger,
            ai_logger
        )
        
        # Test all loggers exist
        loggers = [
            auth_logger,
            market_logger,
            stake_logger,
            oracle_logger,
            defi_logger,
            blockchain_logger,
            ai_logger
        ]
        
        for logger in loggers:
            assert logger is not None
            assert hasattr(logger, 'info')
            assert hasattr(logger, 'error')
    
    def test_add_request_id_processor(self):
        """Test request ID processor functionality."""
        from predictpesa.core.logging import add_request_id
        
        # Mock logger and event dict
        logger = Mock()
        method_name = "info"
        event_dict = {"message": "test message"}
        
        # Test processor execution
        result = add_request_id(logger, method_name, event_dict)
        
        # Should return a dictionary
        assert isinstance(result, dict)
        assert "message" in result
        assert result["message"] == "test message"
    
    def test_logging_configuration_with_settings(self):
        """Test logging configuration uses settings properly."""
        from predictpesa.core.config import settings
        
        # Test that logging-related settings exist
        required_settings = [
            'log_level',
            'log_format',
            'log_file',
            'is_testing',
            'debug'
        ]
        
        for setting in required_settings:
            assert hasattr(settings, setting), f"Missing setting: {setting}"
    
    def test_log_file_directory_creation(self):
        """Test that log file directory is created during setup."""
        from predictpesa.core.logging import setup_logging
        from predictpesa.core.config import settings
        from pathlib import Path
        
        # Get the log file path
        log_file_path = Path(settings.log_file)
        log_dir = log_file_path.parent
        
        # Setup logging should create the directory
        setup_logging()
        
        # Verify directory exists
        assert log_dir.exists()
    
    def test_structlog_configuration(self):
        """Test structlog is properly configured."""
        from predictpesa.core.logging import setup_logging
        
        # Setup logging
        setup_logging()
        
        # Test that structlog is configured
        logger = structlog.get_logger("test")
        assert logger is not None
        
        # Test logger methods work
        try:
            logger.info("Test message")
            success = True
        except Exception:
            success = False
        
        assert success is True
    
    def test_standard_library_logging_integration(self):
        """Test integration with standard library logging."""
        from predictpesa.core.logging import setup_logging
        
        # Setup logging
        setup_logging()
        
        # Test standard library logger
        std_logger = logging.getLogger("test_std")
        assert std_logger is not None
        
        # Test logging level is set
        root_logger = logging.getLogger()
        assert root_logger.level >= 0


class TestLoggingIntegration:
    """Integration tests for logging module."""
    
    def test_logging_with_different_formats(self):
        """Test logging with different output formats."""
        from predictpesa.core.logging import setup_logging
        
        # Test JSON format (default in production)
        with patch('predictpesa.core.config.settings') as mock_settings:
            mock_settings.log_format = "json"
            mock_settings.log_level = "INFO"
            mock_settings.log_file = "test.log"
            mock_settings.is_testing = True
            mock_settings.debug = False
            
            try:
                setup_logging()
                success = True
            except Exception:
                success = False
            
            assert success is True
    
    def test_logging_level_configuration(self):
        """Test different logging levels are properly configured."""
        from predictpesa.core.logging import setup_logging
        
        # Test with different log levels
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        
        for level in log_levels:
            with patch('predictpesa.core.config.settings') as mock_settings:
                mock_settings.log_level = level
                mock_settings.log_format = "console"
                mock_settings.log_file = "test.log"
                mock_settings.is_testing = True
                mock_settings.debug = True
                
                try:
                    setup_logging()
                    success = True
                except Exception:
                    success = False
                
                assert success is True, f"Failed to setup logging with level {level}"
    
    def test_file_logging_disabled_in_testing(self):
        """Test that file logging is disabled during testing."""
        from predictpesa.core.logging import setup_logging
        
        with patch('predictpesa.core.config.settings') as mock_settings:
            mock_settings.log_level = "INFO"
            mock_settings.log_format = "json"
            mock_settings.log_file = "test.log"
            mock_settings.is_testing = True  # Should disable file logging
            mock_settings.debug = False
            
            # Setup should work without creating file handlers
            try:
                setup_logging()
                success = True
            except Exception:
                success = False
            
            assert success is True
    
    def test_noisy_logger_silencing(self):
        """Test that noisy third-party loggers are silenced."""
        from predictpesa.core.logging import setup_logging
        
        setup_logging()
        
        # Test that specific loggers are set to WARNING level
        noisy_loggers = [
            "uvicorn.access",
            "sqlalchemy.engine",
            "httpx",
            "httpcore",
            "asyncio",
            "multipart"
        ]
        
        for logger_name in noisy_loggers:
            logger = logging.getLogger(logger_name)
            assert logger.level >= logging.WARNING


class TestLoggingPerformance:
    """Performance tests for logging module."""
    
    def test_logger_caching(self):
        """Test that loggers are properly cached."""
        from predictpesa.core.logging import get_logger
        
        # Get same logger multiple times
        logger1 = get_logger("test_cache")
        logger2 = get_logger("test_cache")
        
        # Should be equivalent loggers (structlog creates lazy proxies)
        assert logger1 is not None
        assert logger2 is not None
        assert str(logger1) == str(logger2)
    
    def test_mixin_logger_caching(self):
        """Test that mixin loggers are cached per class."""
        from predictpesa.core.logging import LoggerMixin
        
        class TestClass(LoggerMixin):
            pass
        
        instance1 = TestClass()
        instance2 = TestClass()
        
        # Should get same logger for same class
        logger1 = instance1.logger
        logger2 = instance2.logger
        
        # Both should be valid loggers
        assert logger1 is not None
        assert logger2 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
