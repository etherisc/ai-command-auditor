"""
AI Command Auditor - A security tool for intercepting and validating shell commands.

This package provides command validation through rule-based and AI-based checks,
with the ability to block or modify dangerous commands.

Author: Etherisc
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Etherisc"
__email__ = "dev@etherisc.com"
__description__ = "AI-powered command auditing and security validation tool"

# Package-level imports
from .core.config import AuditorConfig
from .core.rules import RuleEngine
from .core.validator import CommandValidator

__all__ = [
    "AuditorConfig",
    "CommandValidator",
    "RuleEngine",
    "__version__",
]
