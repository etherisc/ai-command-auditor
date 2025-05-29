"""
Analysis module for AI Command Auditor.

This module provides functionality for analyzing AI commands, collecting metrics,
and performing security assessments.
"""

from .command_analyzer import *
from .metrics_collector import *
from .security_analyzer import *

__version__ = "0.1.0"

__all__ = [
    "command_analyzer",
    "metrics_collector",
    "security_analyzer"
] 