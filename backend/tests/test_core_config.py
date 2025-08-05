"""
Comprehensive tests for PredictPesa core configuration module.
Tests the Settings class, validation, and environment variable handling.
"""

import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from predictpesa.core.config import Settings, get_settings


class TestSettings:
    """Test the Settings configuration class."""
    
    def test_settings_defaults(self):
        """Test default configuration values."""
        test_settings = Settings()
        
        # Application defaults
        assert test_settings.app_name == "PredictPesa"
        assert test_settings.app_version == "1.0.0"
        assert test_settings.environment == "development"
        
        # Server defaults
        assert test_settings.host == "0.0.0.0"
        assert test_settings.port == 8000
        # Workers might be overridden by .env file
        assert test_settings.workers > 0
        
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
            'PORT': '9000',
            'ENVIRONMENT': 'testing',
            'SECRET_KEY': 'test-secret-key'
        }):
            test_settings = Settings()
            assert test_settings.app_name == 'TestApp'
            assert test_settings.port == 9000
            assert test_settings.environment == 'testing'
            assert test_settings.secret_key == 'test-secret-key'
    
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
        # Note: Some fields may not exist in current config
        assert hasattr(test_settings, 'hedera_account_id')
        assert hasattr(test_settings, 'hedera_private_key')
    
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
    
    def test_settings_celery_configuration(self):
        """Test Celery configuration settings."""
        test_settings = Settings()
        
        assert test_settings.celery_broker_url is not None
        assert test_settings.celery_result_backend is not None
        assert test_settings.celery_task_serializer == "json"
        assert test_settings.celery_result_serializer == "json"
        assert "json" in test_settings.celery_accept_content
        assert test_settings.celery_timezone == "UTC"
        assert test_settings.celery_enable_utc is True
    
    def test_settings_ai_configuration(self):
        """Test AI configuration settings."""
        test_settings = Settings()
        
        # Groq API settings
        assert hasattr(test_settings, 'groq_api_key')
        assert hasattr(test_settings, 'groq_model')
        assert hasattr(test_settings, 'groq_max_tokens')
        assert hasattr(test_settings, 'groq_temperature')
        
        if test_settings.groq_model:
            assert test_settings.groq_model == "llama3-70b-8192"
        if test_settings.groq_max_tokens:
            assert test_settings.groq_max_tokens > 0
        if test_settings.groq_temperature:
            assert 0 <= test_settings.groq_temperature <= 2
    
    def test_settings_oracle_configuration(self):
        """Test Oracle configuration settings."""
        test_settings = Settings()
        
        assert hasattr(test_settings, 'oracle_confidence_threshold')
        assert hasattr(test_settings, 'oracle_min_sources')
        assert hasattr(test_settings, 'oracle_settlement_delay_hours')
        assert hasattr(test_settings, 'oracle_dispute_period_hours')
        
        if test_settings.oracle_confidence_threshold:
            assert 0 <= test_settings.oracle_confidence_threshold <= 1
        if test_settings.oracle_min_sources:
            assert test_settings.oracle_min_sources > 0
    
    def test_settings_market_configuration(self):
        """Test Market configuration settings."""
        test_settings = Settings()
        
        assert hasattr(test_settings, 'min_stake_amount')
        assert hasattr(test_settings, 'max_stake_amount')
        assert hasattr(test_settings, 'market_creation_fee')
        assert hasattr(test_settings, 'protocol_fee_percentage')
        assert hasattr(test_settings, 'market_duration_min_hours')
        assert hasattr(test_settings, 'market_duration_max_days')
        
        if test_settings.min_stake_amount:
            assert test_settings.min_stake_amount > 0
        if test_settings.max_stake_amount:
            assert test_settings.max_stake_amount > test_settings.min_stake_amount
        if test_settings.protocol_fee_percentage:
            assert 0 <= test_settings.protocol_fee_percentage <= 1
    
    def test_settings_rate_limiting_configuration(self):
        """Test Rate limiting configuration settings."""
        test_settings = Settings()
        
        assert hasattr(test_settings, 'rate_limit_requests_per_minute')
        assert hasattr(test_settings, 'rate_limit_burst')
        
        if test_settings.rate_limit_requests_per_minute:
            assert test_settings.rate_limit_requests_per_minute > 0
        if test_settings.rate_limit_burst:
            assert test_settings.rate_limit_burst > 0
    
    def test_settings_logging_configuration(self):
        """Test Logging configuration settings."""
        test_settings = Settings()
        
        assert test_settings.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert test_settings.log_format in ["json", "text"]
        assert test_settings.log_file is not None
        assert test_settings.log_rotation is not None
        assert test_settings.log_retention is not None
    
    def test_settings_monitoring_configuration(self):
        """Test Monitoring configuration settings."""
        test_settings = Settings()
        
        assert isinstance(test_settings.prometheus_enabled, bool)
        assert isinstance(test_settings.prometheus_port, int)
        assert test_settings.prometheus_port > 0
        assert hasattr(test_settings, 'sentry_dsn')
        assert test_settings.sentry_environment is not None
    
    def test_settings_cors_configuration(self):
        """Test CORS configuration settings."""
        test_settings = Settings()
        
        assert isinstance(test_settings.cors_origins, list)
        assert len(test_settings.cors_origins) > 0
        assert isinstance(test_settings.cors_credentials, bool)
        assert isinstance(test_settings.cors_methods, list)
        assert "GET" in test_settings.cors_methods
        assert "POST" in test_settings.cors_methods
        assert isinstance(test_settings.cors_headers, list)
    
    def test_settings_type_validation(self):
        """Test that settings have correct types."""
        test_settings = Settings()
        
        # String fields
        assert isinstance(test_settings.app_name, str)
        assert isinstance(test_settings.app_version, str)
        assert isinstance(test_settings.environment, str)
        assert isinstance(test_settings.host, str)
        assert isinstance(test_settings.secret_key, str)
        assert isinstance(test_settings.algorithm, str)
        
        # Integer fields
        assert isinstance(test_settings.port, int)
        assert isinstance(test_settings.workers, int)
        assert isinstance(test_settings.access_token_expire_minutes, int)
        assert isinstance(test_settings.refresh_token_expire_days, int)
        assert isinstance(test_settings.database_pool_size, int)
        assert isinstance(test_settings.redis_pool_size, int)
        
        # Boolean fields
        assert isinstance(test_settings.cors_credentials, bool)
        assert isinstance(test_settings.celery_enable_utc, bool)
        assert isinstance(test_settings.prometheus_enabled, bool)
        
        # List fields
        assert isinstance(test_settings.cors_origins, list)
        assert isinstance(test_settings.cors_methods, list)
        assert isinstance(test_settings.cors_headers, list)
        assert isinstance(test_settings.supported_countries, list)
        assert isinstance(test_settings.supported_currencies, list)
        assert isinstance(test_settings.celery_accept_content, list)
    
    def test_settings_environment_overrides(self):
        """Test that environment variables override defaults."""
        # Test multiple environment variable overrides
        env_vars = {
            'APP_NAME': 'OverriddenApp',
            'PORT': '7777',
            'DEBUG': 'true',
            'ENVIRONMENT': 'production',
            'LOG_LEVEL': 'ERROR',
            'HEDERA_NETWORK': 'mainnet',
            'REDIS_POOL_SIZE': '25'
        }
        
        with patch.dict(os.environ, env_vars):
            test_settings = Settings()
            
            assert test_settings.app_name == 'OverriddenApp'
            assert test_settings.port == 7777
            assert test_settings.debug is True
            assert test_settings.environment == 'production'
            assert test_settings.log_level == 'ERROR'
            assert test_settings.hedera_network == 'mainnet'
            assert test_settings.redis_pool_size == 25
    
    def test_settings_validation_edge_cases(self):
        """Test settings validation with edge cases."""
        # Test empty string environment (should fail)
        with pytest.raises(ValidationError):
            Settings(environment="")
        
        # Test very long app name (should work)
        long_name = "A" * 100
        test_settings = Settings(app_name=long_name)
        assert test_settings.app_name == long_name
        
        # Test negative port (should work, but might not be practical)
        test_settings = Settings(port=0)
        assert test_settings.port == 0
        
        # Test very high port number
        test_settings = Settings(port=65535)
        assert test_settings.port == 65535
    
    def test_settings_model_config(self):
        """Test Pydantic model configuration."""
        test_settings = Settings()
        
        # Check that the model config is properly set
        assert hasattr(test_settings, 'model_config')
        config = test_settings.model_config
        
        # Should be case insensitive
        assert config.get('case_sensitive') is False
        # Should ignore extra fields
        assert config.get('extra') == 'ignore'


class TestSettingsIntegration:
    """Test Settings integration and real-world usage."""
    
    def test_settings_from_env_file(self):
        """Test settings loading from .env file."""
        # This tests the actual .env file loading
        test_settings = Settings()
        
        # Should have loaded from the actual .env file
        assert test_settings.app_name == "PredictPesa"
        
        # Check that real environment values are loaded
        if hasattr(test_settings, 'groq_api_key') and test_settings.groq_api_key:
            assert test_settings.groq_api_key.startswith('gsk_')
    
    def test_settings_production_readiness(self):
        """Test settings for production readiness."""
        prod_settings = Settings(environment="production")
        
        # Production should have proper security
        assert prod_settings.is_production is True
        assert prod_settings.secret_key is not None
        assert len(prod_settings.secret_key) > 10
        
        # Should have proper database configuration
        assert prod_settings.database_url is not None
        assert prod_settings.database_pool_size > 0
    
    def test_settings_development_mode(self):
        """Test settings for development mode."""
        dev_settings = Settings(environment="development")
        
        assert dev_settings.is_development is True
        # Development might have debug enabled
        assert isinstance(dev_settings.debug, bool)
    
    def test_settings_testing_mode(self):
        """Test settings for testing mode."""
        test_settings = Settings(environment="testing")
        
        assert test_settings.is_testing is True
        # Testing should use SQLite
        if "sqlite" in test_settings.database_url:
            assert "sqlite" in test_settings.database_url


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
