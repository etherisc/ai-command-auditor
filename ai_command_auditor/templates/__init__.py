"""
Template system for AI Command Auditor.

This module provides template discovery, loading, and validation functionality
for different project types and configurations.

Author: Etherisc
Date: 2024
Version: 1.0
"""

from pathlib import Path
from typing import List

# Template directory structure
TEMPLATE_DIR = Path(__file__).parent


def get_available_templates() -> List[str]:
    """
    Get list of available template types.

    Returns:
        List of template names (directory names)
    """
    template_types = []
    for item in TEMPLATE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("__"):
            template_types.append(item.name)
    return sorted(template_types)


def get_template_dir(template_type: str) -> Path:
    """
    Get the directory path for a specific template type.

    Args:
        template_type: Name of the template (e.g., 'python', 'node', 'general')

    Returns:
        Path to the template directory

    Raises:
        ValueError: If template type is not found
    """
    template_dir = TEMPLATE_DIR / template_type
    if not template_dir.exists():
        available = get_available_templates()
        raise ValueError(
            f"Template '{template_type}' not found. Available: {available}"
        )

    return template_dir


def validate_template_structure(template_type: str) -> bool:
    """
    Validate that a template has the required structure.

    Args:
        template_type: Name of the template to validate

    Returns:
        True if template structure is valid
    """
    try:
        template_dir = get_template_dir(template_type)

        # Check for required template files
        required_files = [
            "auditor.yml.template",
            "security-rules.yml.template",
            "openai-prompts.yml.template",
        ]

        for file_name in required_files:
            if not (template_dir / file_name).exists():
                return False

        return True

    except ValueError:
        return False


__all__ = [
    "TEMPLATE_DIR",
    "get_available_templates",
    "get_template_dir",
    "validate_template_structure",
]
