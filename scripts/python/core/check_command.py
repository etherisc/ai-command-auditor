#!/usr/bin/env python3
"""
Shell Command Checker - Main command validation script.

This script validates shell commands using rule-based and AI-based checks
to protect against dangerous or incorrect commands.

Author: AI Assistant
Date: 2024
Version: 2.0
"""

import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Add the parent directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Local imports
try:
    from scripts.python.core.config import get_config, setup_logging
    from scripts.python.core.security import CommandValidator, SecurityError
except ImportError:
    # Try relative imports if absolute imports fail
    from .config import get_config, setup_logging
    from .security import CommandValidator, SecurityError

# Third-party imports
try:
    import openai
    import yaml
except ImportError as e:
    print(f"ERROR: Missing required dependency: {e}", file=sys.stderr)
    sys.exit(1)

# Set up logging
logger = logging.getLogger(__name__)


class CommandChecker:
    """Main command checking class that orchestrates rule-based and AI-based validation."""

    def __init__(self):
        """Initialize the command checker."""
        self.config = get_config()
        self.validator = CommandValidator()
        self._rules = None
        self._ai_client = None

        # Validate configuration
        if not self.config.validate_paths():
            logger.error(
                "Configuration validation failed - some required files are missing"
            )

    def load_rules(self) -> List[Dict[str, Any]]:
        """
        Load validation rules from the YAML file.

        Returns:
            List of rule dictionaries
        """
        if self._rules is not None:
            return self._rules

        try:
            rules_file = self.config.get_rules_file()
            if not Path(rules_file).exists():
                logger.warning(f"Rules file not found: {rules_file}")
                return []

            with open(rules_file, "r") as f:
                self._rules = yaml.safe_load(f) or []

            logger.info(f"Loaded {len(self._rules)} rules from {rules_file}")
            return self._rules

        except Exception as e:
            logger.error(f"Failed to load rules: {e}")
            return []

    def _get_ai_client(self) -> Optional[openai.OpenAI]:
        """Get initialized OpenAI client."""
        if self._ai_client is not None:
            return self._ai_client

        api_key = self.config.get_api_key()
        if not api_key:
            logger.warning("OpenAI API key not found - AI validation disabled")
            return None

        try:
            self._ai_client = openai.OpenAI(api_key=api_key)
            logger.debug("OpenAI client initialized successfully")
            return self._ai_client
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            return None

    def apply_rules(self, command: str) -> Tuple[str, Dict[str, Any]]:
        """
        Apply rule-based validation to a command.

        Args:
            command: The command to check

        Returns:
            Tuple of (action, result_dict)
        """
        rules = self.load_rules()

        for rule in rules:
            pattern = rule.get("pattern")
            if not pattern:
                continue

            try:
                if re.search(pattern, command):
                    logger.info(f"Rule matched: {pattern}")

                    if "replace" in rule:
                        new_command = re.sub(pattern, rule["replace"], command)
                        return "EXECUTE", {
                            "action": "EXECUTE",
                            "command": new_command,
                            "reason": rule.get("reason", "Rule-based replacement"),
                            "rule_pattern": pattern,
                        }

                    if "error" in rule:
                        return "ERROR", {
                            "action": "ERROR",
                            "message": rule["error"],
                            "reason": rule.get("reason", "Rule-based blocking"),
                            "rule_pattern": pattern,
                        }

            except re.error as e:
                logger.error(f"Invalid regex pattern in rule: {pattern} - {e}")
                continue

        # No rules matched
        return "NONE", {"action": "NONE"}

    def build_ai_prompt(self, command: str) -> str:
        """
        Build the AI prompt from template and rules.

        Args:
            command: The command to analyze

        Returns:
            Complete prompt string
        """
        try:
            # Load wrapper prompt template
            wrapper_file = self.config.get_ai_prompt_file()
            with open(wrapper_file, "r") as f:
                wrapper_prompt = f.read()

            # Load AI rules content
            ai_rules_file = self.config.get_ai_rules_prompt_file()
            if Path(ai_rules_file).exists():
                with open(ai_rules_file, "r") as f:
                    rules_content = f.read()
            else:
                logger.warning(f"AI rules file not found: {ai_rules_file}")
                rules_content = "No specific rules defined."

            # Replace placeholders
            prompt = wrapper_prompt.replace("{{RULES}}", rules_content)
            prompt = prompt.replace("{{COMMAND}}", command)

            return prompt

        except Exception as e:
            logger.error(f"Failed to build AI prompt: {e}")
            # Return a minimal prompt as fallback
            return f"""You are a DevOps security expert. Analyze this command for safety:

Command: {command}

Respond with valid JSON only:
{{"action": "PASS"}} for safe commands
{{"action": "EXECUTE", "command": "corrected_command"}} for fixable issues
{{"action": "ERROR", "message": "explanation"}} for dangerous commands"""

    def call_openai(self, prompt: str) -> Tuple[str, Dict[str, Any]]:
        """
        Call OpenAI API to analyze a command.

        Args:
            prompt: The prompt to send to OpenAI

        Returns:
            Tuple of (action, result_dict)
        """
        client = self._get_ai_client()
        if not client:
            logger.warning("OpenAI client not available, falling back to PASS")
            return "PASS", {"action": "PASS", "reason": "AI unavailable"}

        try:
            response = client.chat.completions.create(
                model=self.config.get("ai.model", "gpt-4o"),
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                timeout=self.config.get("ai.timeout", 30),
                max_tokens=500,
            )

            if not response.choices:
                logger.error("No response from OpenAI")
                return "PASS", {"action": "PASS", "reason": "Empty AI response"}

            content = response.choices[0].message.content
            if not content:
                logger.error("Empty content in OpenAI response")
                return "PASS", {"action": "PASS", "reason": "Empty AI content"}

            # Parse JSON response
            result = json.loads(content)
            action = result.get("action", "PASS").upper()

            # Validate action
            if action not in ["PASS", "EXECUTE", "ERROR"]:
                logger.warning(f"Invalid action from AI: {action}, defaulting to PASS")
                action = "PASS"
                result["action"] = "PASS"

            logger.info(f"AI analysis result: {action}")
            return action, result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            return "PASS", {"action": "PASS", "reason": "Invalid AI JSON response"}

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return "PASS", {"action": "PASS", "reason": f"AI error: {str(e)}"}

    def check_command(self, command: str) -> Dict[str, Any]:
        """
        Main command checking logic.

        Args:
            command: The command to check

        Returns:
            Result dictionary with action and details
        """
        if not command or not command.strip():
            return {"action": "PASS", "reason": "Empty command"}

        # Sanitize the command
        sanitized_command = self.validator.sanitize_command(command)

        # Security validation first
        is_safe, security_error = self.validator.validate_command(sanitized_command)
        if not is_safe:
            self.validator.log_security_event(
                "BLOCKED", sanitized_command, security_error or "Security violation"
            )
            return {
                "action": "ERROR",
                "message": f"Security violation: {security_error}",
                "reason": "Security check failed",
            }

        # Apply rule-based checks
        rule_action, rule_result = self.apply_rules(sanitized_command)

        if rule_action in ["EXECUTE", "ERROR"]:
            logger.info(f"Rule-based decision: {rule_action}")
            return rule_result

        # If no rules matched, try AI-based analysis
        logger.info("No rules matched, attempting AI analysis")
        ai_action, ai_result = self.call_openai(self.build_ai_prompt(sanitized_command))

        # Add metadata
        ai_result["analysis_type"] = "ai"
        ai_result["original_command"] = command
        ai_result["sanitized_command"] = sanitized_command

        return ai_result


def format_output(result: Dict[str, Any]) -> str:
    """
    Format the result for shell consumption.

    Args:
        result: Result dictionary from command checking

    Returns:
        Formatted output string
    """
    action = result.get("action", "PASS")

    if action == "PASS":
        return "PASS"
    elif action == "EXECUTE":
        command = result.get("command", "")
        return f"EXECUTE: {command}"
    elif action == "ERROR":
        message = result.get("message", "Command blocked")
        return f"ERROR: {message}"
    else:
        # Fallback for unknown actions
        return "PASS"


def main() -> None:
    """Main entry point for the command checker."""
    try:
        # Set up logging
        setup_logging()

        if len(sys.argv) < 2:
            logger.warning("No command provided")
            print(json.dumps({"action": "PASS", "reason": "No command provided"}))
            return

        # Get command from arguments
        command = sys.argv[1]
        logger.info(
            f"Checking command: {command[:100]}{'...' if len(command) > 100 else ''}"
        )

        # Initialize checker and process command
        checker = CommandChecker()
        result = checker.check_command(command)

        # Output for shell consumption (simple format)
        output = format_output(result)
        print(output)

        # Log detailed result
        logger.info(f"Command check result: {result}")

    except KeyboardInterrupt:
        logger.info("Command checking interrupted by user")
        print("PASS")  # Allow command to proceed if interrupted
        sys.exit(0)

    except Exception as e:
        import traceback

        logger.error(f"Unexpected error in main: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        print("PASS")  # Fail open on unexpected errors
        sys.exit(0)


if __name__ == "__main__":
    main()
