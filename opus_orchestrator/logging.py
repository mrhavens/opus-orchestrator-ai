"""Logging configuration for Opus.

Structured logging with levels, formats, and handlers.
"""

import logging
import sys
from pathlib import Path


def setup_logging(
    level: str = "INFO",
    log_file: str = None,
    format: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
) -> logging.Logger:
    """Setup structured logging for Opus.
    
    Args:
        level: DEBUG, INFO, WARNING, ERROR
        log_file: Optional file path
        format: Log message format
        
    Returns:
        Configured logger
    """
    # Create logger
    logger = logging.getLogger("opus")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(getattr(logging, level.upper()))
    console.setFormatter(logging.Formatter(format))
    logger.addHandler(console)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
        ))
        logger.addHandler(file_handler)
    
    return logger


# Default logger
logger = setup_logging()


# Usage in modules:
# from opus_orchestrator.logging import logger
# logger.info("Starting generation")
# logger.error(f"Failed: {e}")
