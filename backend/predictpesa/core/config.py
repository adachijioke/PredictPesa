"""
Configuration management for PredictPesa backend.
Handles environment variables, validation, and application settings.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application Settings
    app_name: str = Field(default="PredictPesa", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    app_description: str = Field(
        default="DeFi-native prediction market platform on Hedera",
        description="Application description"
    )
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    workers: int = Field(default=4, description="Number of workers")
    reload: bool = Field(default=False, description="Auto-reload on changes")
    
    # Security
    secret_key: str = Field(
        default="your-super-secret-key-change-this-in-production",
        description="Secret key for JWT tokens"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30, description="Access token expiration in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=7, description="Refresh token expiration in days"
    )
    
    # CORS Settings
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Allowed CORS origins"
    )
    cors_credentials: bool = Field(default=True, description="Allow credentials")
    cors_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Allowed CORS methods"
    )
    cors_headers: List[str] = Field(default=["*"], description="Allowed CORS headers")
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql+asyncpg://predictpesa:password@localhost:5432/predictpesa_db",
        description="Database connection URL"
    )
    database_pool_size: int = Field(default=20, description="Database pool size")
    database_max_overflow: int = Field(default=30, description="Database max overflow")
    database_pool_timeout: int = Field(default=30, description="Database pool timeout")
    database_pool_recycle: int = Field(default=3600, description="Database pool recycle")
    
    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379/0", description="Redis connection URL"
    )
    redis_pool_size: int = Field(default=10, description="Redis pool size")
    redis_socket_timeout: int = Field(default=5, description="Redis socket timeout")
    redis_socket_connect_timeout: int = Field(
        default=5, description="Redis socket connect timeout"
    )
    
    # Celery Configuration
    celery_broker_url: str = Field(
        default="redis://localhost:6379/1", description="Celery broker URL"
    )
    celery_result_backend: str = Field(
        default="redis://localhost:6379/2", description="Celery result backend"
    )
    celery_task_serializer: str = Field(default="json", description="Celery task serializer")
    celery_result_serializer: str = Field(default="json", description="Celery result serializer")
    celery_accept_content: List[str] = Field(default=["json"], description="Celery accept content")
    celery_timezone: str = Field(default="UTC", description="Celery timezone")
    celery_enable_utc: bool = Field(default=True, description="Celery enable UTC")
    
    # Hedera Network Configuration
    hedera_network: str = Field(default="testnet", description="Hedera network")
    hedera_account_id: str = Field(default="0.0.123456", description="Hedera account ID")
    hedera_private_key: str = Field(
        default="your-hedera-private-key-here", description="Hedera private key"
    )
    hedera_mirror_node_url: str = Field(
        default="https://testnet.mirrornode.hedera.com", description="Hedera mirror node URL"
    )
    hedera_json_rpc_url: str = Field(
        default="https://testnet.hashio.io/api", description="Hedera JSON-RPC URL"
    )
    
    # Smart Contract Addresses
    market_factory_contract: str = Field(
        default="0x1234567890123456789012345678901234567890",
        description="Market factory contract address"
    )
    staking_vault_contract: str = Field(
        default="0x2345678901234567890123456789012345678901",
        description="Staking vault contract address"
    )
    amm_pool_contract: str = Field(
        default="0x3456789012345678901234567890123456789012",
        description="AMM pool contract address"
    )
    
    # Token Addresses
    wbtc_token_address: str = Field(
        default="0x4567890123456789012345678901234567890123",
        description="WBTC token address"
    )
    yes_btc_token_id: str = Field(default="0.0.789012", description="yesBTC token ID")
    no_btc_token_id: str = Field(default="0.0.789013", description="noBTC token ID")
    
    # External APIs
    chainlink_api_key: Optional[str] = Field(default=None, description="Chainlink API key")
    coinbase_api_key: Optional[str] = Field(default=None, description="Coinbase API key")
    coinbase_api_secret: Optional[str] = Field(default=None, description="Coinbase API secret")
    binance_api_key: Optional[str] = Field(default=None, description="Binance API key")
    binance_api_secret: Optional[str] = Field(default=None, description="Binance API secret")
    
    # AI Configuration
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    groq_model: str = Field("llama3-70b-8192", env="GROQ_MODEL")
    groq_max_tokens: int = Field(2000, env="GROQ_MAX_TOKENS")
    groq_temperature: float = Field(0.7, env="GROQ_TEMPERATURE")
    
    # Oracle Configuration
    oracle_confidence_threshold: float = Field(
        default=0.95, description="Oracle confidence threshold"
    )
    oracle_min_sources: int = Field(default=3, description="Oracle minimum sources")
    oracle_settlement_delay_hours: int = Field(
        default=24, description="Oracle settlement delay in hours"
    )
    oracle_dispute_period_hours: int = Field(
        default=72, description="Oracle dispute period in hours"
    )
    
    # Market Configuration
    min_stake_amount: float = Field(default=0.001, description="Minimum stake amount")
    max_stake_amount: float = Field(default=10.0, description="Maximum stake amount")
    market_creation_fee: float = Field(default=0.01, description="Market creation fee")
    protocol_fee_percentage: float = Field(default=0.1, description="Protocol fee percentage")
    market_duration_min_hours: int = Field(
        default=1, description="Market minimum duration in hours"
    )
    market_duration_max_days: int = Field(
        default=365, description="Market maximum duration in days"
    )
    
    # Rate Limiting
    rate_limit_requests_per_minute: int = Field(
        default=100, description="Rate limit requests per minute"
    )
    rate_limit_burst: int = Field(default=20, description="Rate limit burst")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="json", description="Log format")
    log_file: str = Field(default="logs/predictpesa.log", description="Log file path")
    log_rotation: str = Field(default="1 day", description="Log rotation")
    log_retention: str = Field(default="30 days", description="Log retention")
    
    # Monitoring & Metrics
    prometheus_enabled: bool = Field(default=True, description="Enable Prometheus metrics")
    prometheus_port: int = Field(default=9090, description="Prometheus port")
    sentry_dsn: Optional[str] = Field(default=None, description="Sentry DSN")
    sentry_environment: str = Field(default="development", description="Sentry environment")
    
    # Feature Flags
    enable_market_creation: bool = Field(default=True, description="Enable market creation")
    enable_staking: bool = Field(default=True, description="Enable staking")
    enable_ai_suggestions: bool = Field(default=True, description="Enable AI suggestions")
    enable_mobile_ussd: bool = Field(default=False, description="Enable mobile USSD")
    enable_synthetic_indices: bool = Field(default=False, description="Enable synthetic indices")
    enable_yield_farming: bool = Field(default=False, description="Enable yield farming")
    
    # Geographic Configuration
    default_timezone: str = Field(default="UTC", description="Default timezone")
    supported_countries: List[str] = Field(
        default=["NG", "KE", "GH", "ZA", "UG", "TZ", "RW"],
        description="Supported countries"
    )
    default_currency: str = Field(default="USD", description="Default currency")
    supported_currencies: List[str] = Field(
        default=["USD", "NGN", "KES", "GHS", "ZAR", "UGX", "TZS", "RWF"],
        description="Supported currencies"
    )
    
    @validator("environment")
    def validate_environment(cls, v):
        """Validate environment setting."""
        allowed_environments = ["development", "staging", "production", "testing"]
        if v not in allowed_environments:
            raise ValueError(f"Environment must be one of {allowed_environments}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level setting."""
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of {allowed_levels}")
        return v.upper()
    
    @validator("hedera_network")
    def validate_hedera_network(cls, v):
        """Validate Hedera network setting."""
        allowed_networks = ["testnet", "mainnet", "previewnet"]
        if v not in allowed_networks:
            raise ValueError(f"Hedera network must be one of {allowed_networks}")
        return v
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode."""
        return self.environment == "testing"
    



@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
