"""
Core functionality for AI Command Auditor.

This module provides core utilities, base classes, and common functionality
used throughout the AI Command Auditor system.
"""

from .config import Config, get_config, setup_logging
from .security import (
    CommandValidator,
    SecurityError,
    sanitize_command,
    validate_command,
)

__version__ = "2.0.0"

__all__ = [
    "get_config",
    "setup_logging",
    "Config",
    "CommandValidator",
    "SecurityError",
    "validate_command",
    "sanitize_command",
]
