#!/usr/bin/env python3
"""
Configuration management for AI Command Auditor.

This module handles configuration loading, path resolution, and environment
variable management for the command checking system.

Author: AI Assistant
Date: 2024
Version: 1.0
"""

import copy
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

# Set up logging
logger = logging.getLogger(__name__)


# Project root detection
def get_project_root() -> Path:
    """
    Find the project root directory by looking for key files.

    Returns:
        Path: The project root directory

    Raises:
        RuntimeError: If project root cannot be determined
    """
    current = Path(__file__).resolve()

    # Look for key project files to identify root
    root_markers = ["requirements.txt", "README.md", ".git", "scripts", "docs"]

    # First try to find the ideal root with both scripts and docs
    for parent in [current] + list(current.parents):
        if any((parent / marker).exists() for marker in root_markers):
            if (parent / "scripts").exists() and (parent / "docs").exists():
                return parent

    # Fallback: if we can't find the ideal root, use the first one with any marker
    for parent in [current] + list(current.parents):
        if any((parent / marker).exists() for marker in root_markers):
            return parent

    raise RuntimeError("Could not determine project root directory")


# Initialize paths safely
try:
    PROJECT_ROOT = get_project_root()
    SCRIPTS_DIR = PROJECT_ROOT / "scripts"
    CONFIG_DIR = PROJECT_ROOT / "config"
    RULES_DIR = SCRIPTS_DIR / "rules"
    AI_PROMPTS_DIR = SCRIPTS_DIR / "ai-prompts"
except Exception as e:
    # Fallback to current directory if path resolution fails
    PROJECT_ROOT = Path.cwd()
    SCRIPTS_DIR = PROJECT_ROOT / "scripts"
    CONFIG_DIR = PROJECT_ROOT / "config"
    RULES_DIR = SCRIPTS_DIR / "rules"
    AI_PROMPTS_DIR = SCRIPTS_DIR / "ai-prompts"
    print(f"Warning: Could not determine project root, using current directory: {e}")


# Default configuration
DEFAULT_CONFIG = {
    "rules": {
        "python_auditor_rules": str(
            RULES_DIR / "python-auditor" / "check_command_rules.yml"
        ),
        "ai_auditor_prompt": str(RULES_DIR / "ai-auditor" / "check_command_prompt.md"),
    },
    "ai": {
        "wrapper_prompt": str(AI_PROMPTS_DIR / "core" / "check_command_prompt.md"),
        "model": "gpt-4o",
        "timeout": 30,
        "max_retries": 3,
    },
    "security": {
        "max_command_length": 1000,
        "allow_multiline": False,
        "blocked_patterns": [
            r"rm\s+-rf\s+/",  # Dangerous rm commands
            r">(\/dev\/sda|\/dev\/hda)",  # Direct disk writes
            r"curl.*\|\s*bash",  # Piped execution
        ],
    },
    "logging": {
        "level": "INFO",
        "file": str(PROJECT_ROOT / "logs" / "command_checker.log"),
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    },
}


class Config:
    """Configuration manager with environment variable support."""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_file: Optional path to configuration file
        """
        # Use deep copy to ensure nested dictionaries are properly copied
        self._config = copy.deepcopy(DEFAULT_CONFIG)
        self._load_config_file(config_file)
        self._apply_environment_variables()

    def _load_config_file(self, config_file: Optional[str]) -> None:
        """Load configuration from file if it exists."""
        if config_file:
            config_path = Path(config_file)
        else:
            config_path = CONFIG_DIR / "config.yml"

        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    file_config = yaml.safe_load(f) or {}
                logger.debug(f"Loaded file config: {file_config}")
                self._merge_config(self._config, file_config)
                logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load config file {config_path}: {e}")
        else:
            logger.debug(f"Config file not found: {config_path}")

    def _apply_environment_variables(self) -> None:
        """Apply environment variable overrides."""
        # OpenAI API key
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            self._config.setdefault("ai", {})["api_key"] = api_key

        # Rules file override
        rules_file = os.environ.get("COMMAND_CHECKER_RULES")
        if rules_file:
            self._config["rules"]["python_auditor_rules"] = rules_file

        # Prompt file override
        prompt_file = os.environ.get("COMMAND_CHECKER_PROMPT")
        if prompt_file:
            self._config["ai"]["wrapper_prompt"] = prompt_file

        # Logging level
        log_level = os.environ.get("COMMAND_CHECKER_LOG_LEVEL")
        if log_level:
            self._config["logging"]["level"] = log_level.upper()

    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Recursively merge configuration dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'ai.model')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_rules_file(self) -> str:
        """Get path to rules file."""
        return self.get("rules.python_auditor_rules")

    def get_ai_prompt_file(self) -> str:
        """Get path to AI prompt wrapper file."""
        return self.get("ai.wrapper_prompt")

    def get_ai_rules_prompt_file(self) -> str:
        """Get path to AI rules prompt file."""
        return self.get("rules.ai_auditor_prompt")

    def get_api_key(self) -> Optional[str]:
        """Get OpenAI API key."""
        return self.get("ai.api_key")

    def validate_paths(self) -> bool:
        """
        Validate that all required files exist.

        Returns:
            bool: True if all paths are valid
        """
        required_files = [
            ("rules file", self.get_rules_file()),
            ("AI prompt file", self.get_ai_prompt_file()),
        ]

        for file_desc, file_path in required_files:
            if file_path is None:
                logger.error(f"Required {file_desc} path is None - configuration error")
                return False

            if not Path(file_path).exists():
                logger.error(f"Required {file_desc} not found: {file_path}")
                return False

        return True


# Global configuration instance
_config_instance = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


def setup_logging() -> None:
    """Set up logging configuration."""
    config = get_config()

    # Create logs directory if it doesn't exist
    log_file = Path(config.get("logging.file"))
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config.get("logging.level", "INFO")),
        format=config.get("logging.format"),
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )
