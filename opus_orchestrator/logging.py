"""Structured Logging for Opus Orchestrator.

Provides JSON-formatted logging for production environments.
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Optional
from enum import Enum


class LogLevel(str, Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        return json.dumps(log_data)


class OpusLogger:
    """Structured logger for Opus."""
    
    def __init__(self, name: str, level: str = "INFO"):
        """Initialize logger.
        
        Args:
            name: Logger name (usually module name)
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Only add handler once
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(StructuredFormatter())
            self.logger.addHandler(handler)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        self.logger.debug(message, extra={"extra": kwargs} if kwargs else {})
    
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self.logger.info(message, extra={"extra": kwargs} if kwargs else {})
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self.logger.warning(message, extra={"extra": kwargs} if kwargs else {})
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self.logger.error(message, extra={"extra": kwargs} if kwargs else {})
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message."""
        self.logger.critical(message, extra={"extra": kwargs} if kwargs else {})
    
    def log_request(self, method: str, path: str, status_code: int, duration_ms: float) -> None:
        """Log HTTP request."""
        self.info(
            "HTTP Request",
            method=method,
            path=path,
            status_code=status_code,
            duration_ms=duration_ms,
        )
    
    def log_llm_request(self, provider: str, model: str, duration_ms: float, success: bool) -> None:
        """Log LLM API request."""
        self.info(
            "LLM Request",
            provider=provider,
            model=model,
            duration_ms=duration_ms,
            success=success,
        )
    
    def log_generation(self, book_type: str, genre: str, word_count: int, duration_s: float) -> None:
        """Log book generation."""
        self.info(
            "Book Generation",
            book_type=book_type,
            genre=genre,
            word_count=word_count,
            duration_s=duration_s,
        )


def get_logger(name: str, level: Optional[str] = None) -> OpusLogger:
    """Get a structured logger.
    
    Args:
        name: Logger name
        level: Optional log level override
        
    Returns:
        OpusLogger instance
    """
    import os
    env_level = os.environ.get("OPUS_LOG_LEVEL", level or "INFO")
    return OpusLogger(name, env_level)


# Convenience function for quick logging
def log(name: str, level: str, message: str, **kwargs: Any) -> None:
    """Quick logging function.
    
    Args:
        name: Logger name
        level: Log level
        message: Log message
        **kwargs: Additional context
    """
    logger = get_logger(name)
    getattr(logger, level.lower())(message, **kwargs)
