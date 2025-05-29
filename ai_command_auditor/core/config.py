"""
Configuration management for AI Command Auditor.

This module handles configuration loading, path resolution, and environment
variable management for the command checking system. Updated to support
the new packageized structure with user-accessible .ai-auditor directories.

Author: Etherisc
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


def get_project_root() -> Path:
    """
    Find the project root directory by looking for key files.

    For packaged installations, this will find the project where ai-auditor
    is being used, not the package installation directory.

    Returns:
        Path: The project root directory

    Raises:
        RuntimeError: If project root cannot be determined
    """
    current = Path.cwd()

    # Look for key project files to identify root
    root_markers = [
        ".git",
        ".ai-auditor",
        "pyproject.toml",
        "setup.py",
        "requirements.txt",
        "README.md",
    ]

    # First try to find a directory with .ai-auditor (our config directory)
    for parent in [current] + list(current.parents):
        if (parent / ".ai-auditor").exists():
            return parent

    # Fallback: look for other project markers
    for parent in [current] + list(current.parents):
        if any((parent / marker).exists() for marker in root_markers):
            return parent

    # Final fallback: use current working directory
    return current


def get_user_config_dir(project_root: Optional[Path] = None) -> Path:
    """
    Get the user-accessible configuration directory (.ai-auditor).

    Args:
        project_root: Optional project root path

    Returns:
        Path to .ai-auditor directory
    """
    if project_root is None:
        project_root = get_project_root()

    return project_root / ".ai-auditor"


def get_default_config_paths(config_dir: Path) -> Dict[str, str]:
    """
    Get default configuration file paths for user-accessible config.

    Args:
        config_dir: Path to .ai-auditor directory

    Returns:
        Dictionary of configuration paths
    """
    return {
        "main_config": str(config_dir / "config" / "auditor.yml"),
        "security_rules": str(config_dir / "config" / "rules" / "security-rules.yml"),
        "style_rules": str(config_dir / "config" / "rules" / "style-rules.yml"),
        "custom_rules": str(config_dir / "config" / "rules" / "custom-rules.yml"),
        "openai_prompts": str(config_dir / "config" / "prompts" / "openai-prompts.yml"),
        "custom_prompts": str(config_dir / "config" / "prompts" / "custom-prompts.yml"),
        "hooks_dir": str(config_dir / "hooks"),
        "workflows_dir": str(config_dir / "workflows"),
    }


# Initialize paths safely
try:
    PROJECT_ROOT = get_project_root()
    USER_CONFIG_DIR = get_user_config_dir(PROJECT_ROOT)
    CONFIG_PATHS = get_default_config_paths(USER_CONFIG_DIR)
except Exception as e:
    # Fallback to current directory if path resolution fails
    PROJECT_ROOT = Path.cwd()
    USER_CONFIG_DIR = PROJECT_ROOT / ".ai-auditor"
    CONFIG_PATHS = get_default_config_paths(USER_CONFIG_DIR)
    print(f"Warning: Could not determine project root, using current directory: {e}")


# Default configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    "rules": {
        "security_rules": CONFIG_PATHS["security_rules"],
        "style_rules": CONFIG_PATHS["style_rules"],
        "custom_rules": CONFIG_PATHS["custom_rules"],
    },
    "ai": {
        "prompts": CONFIG_PATHS["openai_prompts"],
        "custom_prompts": CONFIG_PATHS["custom_prompts"],
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
        "file": str(PROJECT_ROOT / "logs" / "ai-auditor.log"),
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    },
    "paths": {
        "project_root": str(PROJECT_ROOT),
        "config_dir": str(USER_CONFIG_DIR),
        "hooks_dir": CONFIG_PATHS["hooks_dir"],
        "workflows_dir": CONFIG_PATHS["workflows_dir"],
    },
}


class AuditorConfig:
    """Configuration manager with environment variable support and user-accessible configs."""

    def __init__(
        self, config_file: Optional[str] = None, config_dir: Optional[str] = None
    ):
        """
        Initialize configuration manager.

        Args:
            config_file: Optional path to main configuration file
            config_dir: Optional path to .ai-auditor directory
        """
        # Set up paths
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = USER_CONFIG_DIR

        # Use deep copy to ensure nested dictionaries are properly copied
        self._config = copy.deepcopy(DEFAULT_CONFIG)

        # Update paths to use the specified config directory
        self._update_config_paths()

        # Load configuration
        self._load_config_file(config_file)
        self._apply_environment_variables()

    def _update_config_paths(self) -> None:
        """Update configuration paths to use the specified config directory."""
        paths = get_default_config_paths(self.config_dir)

        self._config["rules"]["security_rules"] = paths["security_rules"]
        self._config["rules"]["style_rules"] = paths["style_rules"]
        self._config["rules"]["custom_rules"] = paths["custom_rules"]
        self._config["ai"]["prompts"] = paths["openai_prompts"]
        self._config["ai"]["custom_prompts"] = paths["custom_prompts"]
        self._config["paths"]["config_dir"] = str(self.config_dir)
        self._config["paths"]["hooks_dir"] = paths["hooks_dir"]
        self._config["paths"]["workflows_dir"] = paths["workflows_dir"]

    def _load_config_file(self, config_file: Optional[str]) -> None:
        """Load configuration from file if it exists."""
        if config_file:
            config_path = Path(config_file)
        else:
            config_path = self.config_dir / "config" / "auditor.yml"

        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
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
            if "ai" not in self._config:
                self._config["ai"] = {}
            self._config["ai"]["api_key"] = api_key

        # Rules file overrides
        security_rules = os.environ.get("AI_AUDITOR_SECURITY_RULES")
        if security_rules:
            self._config["rules"]["security_rules"] = security_rules

        # Prompt file override
        prompts = os.environ.get("AI_AUDITOR_PROMPTS")
        if prompts:
            self._config["ai"]["prompts"] = prompts

        # Logging level
        log_level = os.environ.get("AI_AUDITOR_LOG_LEVEL")
        if log_level:
            self._config["logging"]["level"] = log_level.upper()

        # Model override
        model = os.environ.get("AI_AUDITOR_MODEL")
        if model:
            self._config["ai"]["model"] = model

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
        value: Any = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_security_rules_file(self) -> str:
        """Get path to security rules file."""
        result = self.get("rules.security_rules")
        return str(result) if result is not None else ""

    def get_style_rules_file(self) -> str:
        """Get path to style rules file."""
        result = self.get("rules.style_rules")
        return str(result) if result is not None else ""

    def get_custom_rules_file(self) -> str:
        """Get path to custom rules file."""
        result = self.get("rules.custom_rules")
        return str(result) if result is not None else ""

    def get_ai_prompts_file(self) -> str:
        """Get path to AI prompts file."""
        result = self.get("ai.prompts")
        return str(result) if result is not None else ""

    def get_custom_prompts_file(self) -> str:
        """Get path to custom prompts file."""
        result = self.get("ai.custom_prompts")
        return str(result) if result is not None else ""

    def get_api_key(self) -> Optional[str]:
        """Get OpenAI API key."""
        result = self.get("ai.api_key")
        return str(result) if result is not None else None

    def get_config_dir(self) -> Path:
        """Get the configuration directory path."""
        return self.config_dir

    def get_project_root(self) -> Path:
        """Get the project root directory path."""
        return Path(self.get("paths.project_root", PROJECT_ROOT))

    def validate_paths(self) -> bool:
        """
        Validate that all required files exist.

        Returns:
            bool: True if all paths are valid
        """
        # Don't require all files to exist for initial setup
        # Just check that the config directory exists or can be created
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(
                f"Cannot create or access config directory {self.config_dir}: {e}"
            )
            return False


# Global configuration instance
_config_instance: Optional[AuditorConfig] = None


def get_config(config_dir: Optional[str] = None) -> AuditorConfig:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = AuditorConfig(config_dir=config_dir)
    return _config_instance


def setup_logging(config: Optional[AuditorConfig] = None) -> None:
    """Set up logging configuration."""
    if config is None:
        config = get_config()

    # Create logs directory if it doesn't exist
    log_file = Path(config.get("logging.file"))
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config.get("logging.level", "INFO")),
        format=config.get("logging.format"),
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
        force=True,  # Override any existing configuration
    )
