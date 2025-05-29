#!/usr/bin/env python3
"""
Security module for AI Command Auditor.

This module handles input validation, command sanitization, and security
logging to prevent dangerous command execution.

Author: AI Assistant
Date: 2024
Version: 1.0
"""

import logging
import re
import shlex
from typing import Any, Dict, List, Optional, Tuple

from .config import get_config

logger = logging.getLogger(__name__)


class SecurityError(Exception):
    """Raised when a security violation is detected."""

    pass


class CommandValidator:
    """Validates and sanitizes shell commands for security."""

    def __init__(self):
        """Initialize the command validator."""
        self.config = get_config()
        self._load_security_patterns()

    def _load_security_patterns(self) -> None:
        """Load security patterns from configuration."""
        self.blocked_patterns = [
            re.compile(pattern)
            for pattern in self.config.get("security.blocked_patterns", [])
        ]

        # Additional security patterns
        self.dangerous_patterns = [
            re.compile(r"rm\s+-r[f]*\s+/"),  # rm -rf /
            re.compile(r"rm\s+-[rf]*r[f]*\s+/"),  # rm -fr /
            re.compile(r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;:\s*"),  # Fork bomb
            re.compile(r"cat\s+/dev/random"),  # Random data flood
            re.compile(r"dd\s+if=/dev/zero"),  # Disk fill
            re.compile(r">\s*/dev/sd[a-z][0-9]*"),  # Direct disk write
            re.compile(r"mkfs\."),  # Format filesystem
            re.compile(r"fdisk\s+/dev/"),  # Disk partitioning
            re.compile(r"curl.*\|\s*(sh|bash|zsh|fish)"),  # Piped execution
            re.compile(r"wget.*\|\s*(sh|bash|zsh|fish)"),  # Piped execution
            re.compile(r'eval\s+["\']?\$\('),  # Command injection via eval
            re.compile(r"sudo\s+chmod\s+777"),  # Dangerous permissions
            re.compile(r"chmod\s+777\s+/"),  # Root directory permissions
        ]

        # Suspicious patterns that require extra scrutiny
        self.suspicious_patterns = [
            re.compile(r"sudo\s+rm"),  # sudo rm
            re.compile(r"sudo\s+dd"),  # sudo dd
            re.compile(r"sudo\s+mount"),  # sudo mount
            re.compile(r"nc\s+.*-[le]"),  # netcat listeners
            re.compile(r"python.*-c.*exec"),  # Python exec
            re.compile(r"perl.*-e"),  # Perl one-liners
            re.compile(r"ruby.*-e"),  # Ruby one-liners
            re.compile(r"node.*-e"),  # Node one-liners
        ]

    def validate_command(self, command: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a command for security issues.

        Args:
            command: The command to validate

        Returns:
            Tuple of (is_safe, error_message)
        """
        try:
            # Basic sanity checks
            if not self._basic_validation(command):
                return False, "Command failed basic validation checks"

            # Check for dangerous patterns
            danger_result = self._check_dangerous_patterns(command)
            if not danger_result[0]:
                return danger_result

            # Check for suspicious patterns
            suspicious_result = self._check_suspicious_patterns(command)
            if not suspicious_result[0]:
                return suspicious_result

            # Check for command injection attempts
            injection_result = self._check_command_injection(command)
            if not injection_result[0]:
                return injection_result

            logger.info(f"Command passed security validation: {command[:50]}...")
            return True, None

        except Exception as e:
            logger.error(f"Error during command validation: {e}")
            return False, f"Validation error: {str(e)}"

    def _basic_validation(self, command: str) -> bool:
        """Perform basic validation checks."""
        if not command or not command.strip():
            return False

        # Check command length
        max_length = self.config.get("security.max_command_length", 1000)
        if len(command) > max_length:
            logger.warning(f"Command too long: {len(command)} > {max_length}")
            return False

        # Check for multiline commands if not allowed
        if not self.config.get("security.allow_multiline", False):
            if "\n" in command or "\r" in command:
                logger.warning("Multiline commands not allowed")
                return False

        # Check for null bytes
        if "\x00" in command:
            logger.warning("Null bytes detected in command")
            return False

        return True

    def _check_dangerous_patterns(self, command: str) -> Tuple[bool, Optional[str]]:
        """Check for dangerous command patterns."""
        for pattern in self.dangerous_patterns:
            if pattern.search(command):
                error_msg = f"Dangerous command pattern detected: {pattern.pattern}"
                logger.error(f"SECURITY ALERT: {error_msg} in command: {command}")
                return False, error_msg

        # Check configured blocked patterns
        for pattern in self.blocked_patterns:
            if pattern.search(command):
                error_msg = f"Blocked command pattern: {pattern.pattern}"
                logger.warning(f"Blocked command: {error_msg} in command: {command}")
                return False, error_msg

        return True, None

    def _check_suspicious_patterns(self, command: str) -> Tuple[bool, Optional[str]]:
        """Check for suspicious command patterns that need extra scrutiny."""
        for pattern in self.suspicious_patterns:
            if pattern.search(command):
                logger.warning(
                    f"Suspicious pattern detected: {pattern.pattern} in command: {command}"
                )
                # Don't block, but log for review

        return True, None

    def _check_command_injection(self, command: str) -> Tuple[bool, Optional[str]]:
        """Check for command injection attempts."""
        # Common injection patterns
        injection_patterns = [
            r";\s*rm\s+",  # ; rm
            r"&&\s*rm\s+",  # && rm
            r"\|\s*rm\s+",  # | rm
            r"`.*rm.*`",  # `rm` backticks
            r"\$\(.*rm.*\)",  # $(rm) command substitution
            r">\s*/etc/passwd",  # passwd file manipulation
            r">\s*/etc/shadow",  # shadow file manipulation
            r"<\s*/dev/tcp/",  # Network connections
        ]

        for pattern_str in injection_patterns:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            if pattern.search(command):
                error_msg = f"Command injection attempt detected: {pattern_str}"
                logger.error(f"SECURITY ALERT: {error_msg} in command: {command}")
                return False, error_msg

        return True, None

    def sanitize_command(self, command: str) -> str:
        """
        Sanitize a command by removing/escaping dangerous elements.

        Args:
            command: The command to sanitize

        Returns:
            Sanitized command string
        """
        # Remove leading/trailing whitespace
        command = command.strip()

        # Remove dangerous control characters
        command = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", command)

        # Log the sanitization
        logger.debug(f"Sanitized command: {command}")

        return command

    def parse_command_safely(self, command: str) -> List[str]:
        """
        Parse a command into components using safe shell parsing.

        Args:
            command: The command to parse

        Returns:
            List of command components

        Raises:
            SecurityError: If parsing fails or command is unsafe
        """
        try:
            # Use shlex for safe parsing
            parts = shlex.split(command)

            if not parts:
                raise SecurityError("Empty command after parsing")

            return parts

        except ValueError as e:
            raise SecurityError(f"Invalid shell syntax: {e}")

    def log_security_event(self, event_type: str, command: str, details: str) -> None:
        """
        Log a security-related event.

        Args:
            event_type: Type of security event
            command: The command involved
            details: Additional details about the event
        """
        logger.warning(
            f"SECURITY EVENT - Type: {event_type}, "
            f"Command: {command[:100]}{'...' if len(command) > 100 else ''}, "
            f"Details: {details}"
        )


def validate_command(command: str) -> Tuple[bool, Optional[str]]:
    """
    Convenient function to validate a command.

    Args:
        command: The command to validate

    Returns:
        Tuple of (is_safe, error_message)
    """
    validator = CommandValidator()
    return validator.validate_command(command)


def sanitize_command(command: str) -> str:
    """
    Convenient function to sanitize a command.

    Args:
        command: The command to sanitize

    Returns:
        Sanitized command string
    """
    validator = CommandValidator()
    return validator.sanitize_command(command)
