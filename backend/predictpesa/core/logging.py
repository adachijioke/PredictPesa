"""
Structured logging configuration for PredictPesa.
Provides consistent, searchable logs across the application.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict

import structlog
from structlog.stdlib import LoggerFactory

from predictpesa.core.config import settings


def setup_logging() -> None:
    """Configure structured logging for the application."""
    
    # Create logs directory if it doesn't exist
    log_file_path = Path(settings.log_file)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            # Add log level and timestamp
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            # Add request ID if available
            add_request_id,
            # Format output
            structlog.processors.JSONRenderer() if settings.log_format == "json"
            else structlog.dev.ConsoleRenderer(colors=True),
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level),
    )
    
    # Set up file logging if specified
    if settings.log_file and not settings.is_testing:
        file_handler = logging.FileHandler(settings.log_file)
        file_handler.setLevel(getattr(logging, settings.log_level))
        
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
    
    # Silence noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    # Set third-party loggers to WARNING
    for logger_name in [
        "httpx",
        "httpcore",
        "asyncio",
        "multipart",
    ]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def add_request_id(logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add request ID to log entries if available.
    
    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary
        
    Returns:
        Modified event dictionary
    """
    # Try to get request ID from context
    try:
        import contextvars
        request_id = contextvars.ContextVar('request_id', default=None).get()
        if request_id:
            event_dict['request_id'] = request_id
    except (ImportError, LookupError):
        pass
    
    return event_dict


class LoggerMixin:
    """Mixin to add structured logging to classes."""
    
    @property
    def logger(self) -> structlog.BoundLogger:
        """Get logger for this class."""
        return structlog.get_logger(self.__class__.__name__)


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Structured logger
    """
    return structlog.get_logger(name)


# Application-specific loggers
auth_logger = get_logger("auth")
market_logger = get_logger("market")
stake_logger = get_logger("stake")
oracle_logger = get_logger("oracle")
defi_logger = get_logger("defi")
blockchain_logger = get_logger("blockchain")
ai_logger = get_logger("ai")
