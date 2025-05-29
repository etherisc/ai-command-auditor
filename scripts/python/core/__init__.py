"""
AI Command Auditor - Core Module

This module provides core functionality for the AI Command Auditor.
It includes configuration management, security validation, and OpenAI integration.
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
    "Config",
    "get_config",
    "setup_logging",
    "CommandValidator",
    "SecurityError",
    "sanitize_command",
    "validate_command",
]
