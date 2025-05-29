"""
AI Command Auditor - Python Scripts Package

This package contains Python scripts and modules for auditing, analyzing,
and monitoring AI command interactions and system behaviors.

Modules:
    core: Core functionality and utilities
    analysis: Analysis and metrics collection
    reporting: Report generation and formatting
    tests: Test suite for the package
"""

__version__ = "0.1.0"
__author__ = "AI Command Auditor Team"
__email__ = "team@ai-command-auditor.dev"

# Package-level imports for easy access
from .core import *
from .analysis import *
from .reporting import *

__all__ = [
    "core",
    "analysis", 
    "reporting",
    "tests"
] 