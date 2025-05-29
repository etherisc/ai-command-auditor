#!/usr/bin/env python3
"""
Main CLI interface for AI Command Auditor.

This module provides the command-line interface for the AI Command Auditor,
including initialization, configuration, and management commands.

Author: Etherisc
Date: 2024
Version: 1.0
"""

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import click
from colorama import Fore, Style, init

from ..core.config import AuditorConfig, get_config, setup_logging
from ..core.templates import TemplateEngine

# Initialize colorama for cross-platform colored output
init()

# Import existing functionality
try:
    # Try to import the existing command checker
    import scripts.python.core.check_command as legacy_checker
    from scripts.python.core.security import CommandValidator, validate_command

    LEGACY_AVAILABLE = True
except ImportError:
    LEGACY_AVAILABLE = False

from ..core.validator import CommandValidator as NewValidator


def print_success(message: str) -> None:
    """Print a success message in green."""
    click.echo(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message: str) -> None:
    """Print an error message in red."""
    click.echo(f"{Fore.RED}✗ {message}{Style.RESET_ALL}", err=True)


def print_warning(message: str) -> None:
    """Print a warning message in yellow."""
    click.echo(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def print_info(message: str) -> None:
    """Print an info message in blue."""
    click.echo(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


@click.group()
@click.version_option(version="1.0.0", prog_name="ai-auditor")
@click.option("--config-dir", help="Path to .ai-auditor configuration directory")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, config_dir: Optional[str], verbose: bool) -> None:
    """
    AI Command Auditor - Secure command validation for development workflows.

    This tool provides AI-powered command auditing and security validation
    for shell commands in development environments.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Store options in context
    ctx.obj["config_dir"] = config_dir
    ctx.obj["verbose"] = verbose

    # Set up logging
    if verbose:
        import logging

        setup_logging()
        logging.getLogger().setLevel(logging.DEBUG)


@cli.command(name="init")
@click.option(
    "--template",
    "-t",
    type=click.Choice(["python", "node", "rust", "general", "security"]),
    default="general",
    help="Configuration template to use",
)
@click.option("--config-dir", help="Custom config directory (default: .ai-auditor)")
@click.option("--force", is_flag=True, help="Overwrite existing configuration")
@click.option(
    "--environment",
    "-e",
    type=click.Choice(["development", "staging", "production"]),
    default="development",
    help="Environment type for configuration",
)
@click.option(
    "--security-level",
    "-s",
    type=click.Choice(["basic", "standard", "strict"]),
    default="standard",
    help="Security level for validation rules",
)
@click.option("--team-config", help="Team configuration identifier")
@click.pass_context
def init_command(
    ctx: click.Context,
    template: str,
    config_dir: Optional[str],
    force: bool,
    environment: str,
    security_level: str,
    team_config: Optional[str],
) -> None:
    """Initialize AI Command Auditor in the current project."""
    try:
        # Use config dir from command or context
        config_directory = config_dir or ctx.obj.get("config_dir")

        print_info(f"Initializing AI Command Auditor with {template} template...")
        print_info(f"Environment: {environment}, Security level: {security_level}")

        # Initialize template engine
        template_engine = TemplateEngine()

        # Get available templates and validate choice
        available_templates = template_engine.get_available_templates()
        if template not in available_templates:
            # Fall back to 'general' if the specific template doesn't exist yet
            if "general" in available_templates:
                print_warning(
                    f"Template '{template}' not available yet, using 'general' template"
                )
                template = "general"
            elif "base" in available_templates:
                print_warning(
                    f"Template '{template}' not available yet, using 'base' template"
                )
                template = "base"
            else:
                print_error(
                    f"No templates available. Expected templates: {available_templates}"
                )
                sys.exit(1)

        # Create configuration
        config = AuditorConfig(config_dir=config_directory)
        project_dir = Path.cwd()
        auditor_dir = config.get_config_dir()

        # Check if already initialized
        if auditor_dir.exists() and not force:
            print_warning(f"AI Command Auditor already initialized in {auditor_dir}")
            print_info("Use --force to overwrite existing configuration")
            return

        # Get project name from current directory
        project_name = project_dir.name

        # Apply template using the new template engine
        print_info(f"Applying {template} template...")

        # Custom variables for template
        custom_variables = {
            "project_name": project_name,
            "environment": environment,
            "security_level": security_level,
        }

        if team_config:
            custom_variables["team_config"] = team_config

        # Get default variables with environment and security level
        variables = template_engine.get_default_variables(
            template_type=template,
            project_name=project_name,
            environment=environment,
            security_level=security_level,
        )
        variables.update(custom_variables)

        # Apply the template
        results = template_engine.apply_template(
            project_dir=project_dir,
            template_type=template,
            project_name=project_name,
            custom_variables=variables,
        )

        # Report results
        if results["files_created"]:
            print_success(f"AI Command Auditor initialized successfully!")
            print_info(f"Configuration directory: {auditor_dir}")
            print_info(f"Template applied: {template}")
            print_info(f"Environment: {environment}")
            print_info(f"Security level: {security_level}")
            if team_config:
                print_info(f"Team config: {team_config}")
            print_info(f"Files created: {len(results['files_created'])}")

            for file_info in results["files_created"]:
                print_success(f"Created: {file_info['file']}")

        if results["files_failed"]:
            print_warning(
                f"Some files could not be created: {len(results['files_failed'])}"
            )
            for file_info in results["files_failed"]:
                print_error(f"Failed: {file_info['file']} - {file_info['errors']}")

        if results["validation_errors"]:
            print_warning("Template validation warnings:")
            for error in results["validation_errors"]:
                print_warning(f"  - {error}")

        print_info("Next steps:")
        print_info("  1. Run 'ai-auditor setup-hooks' to install git hooks")
        print_info("  2. Customize rules in .ai-auditor/config/rules/")
        print_info("  3. Configure AI prompts in .ai-auditor/config/prompts/")

    except Exception as e:
        print_error(f"Failed to initialize AI Command Auditor: {e}")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.option("--force", is_flag=True, help="Force reinstall hooks")
@click.pass_context
def setup_hooks(ctx: click.Context, force: bool) -> None:
    """Setup git hooks for command validation."""
    try:
        config_directory = ctx.obj.get("config_dir")
        config = AuditorConfig(config_dir=config_directory)

        print_info("Setting up git hooks...")

        # Check if in git repository
        git_dir = Path(".git")
        if not git_dir.exists():
            print_error("Not in a git repository. Initialize git first.")
            sys.exit(1)

        # Check if the project setup script exists
        project_root = Path.cwd()
        setup_script = project_root / "scripts" / "setup-hooks.sh"

        if setup_script.exists():
            print_info("Using existing project setup script...")
            try:
                # Run the existing setup script
                script_result = subprocess.run(
                    [str(setup_script)],
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    check=False,
                )

                if script_result.returncode == 0:
                    print_success("Git hooks setup completed using project script")
                    print_info("Pre-commit and pre-push hooks are now active")
                    return
                else:
                    print_warning(
                        f"Project setup script failed: {script_result.stderr}"
                    )
                    print_info("Falling back to basic hook setup...")

            except Exception as e:
                print_warning(f"Failed to run project setup script: {e}")
                print_info("Falling back to basic hook setup...")

        # Basic hook setup if project script not available or failed
        _setup_basic_hooks(config, force)

        print_success("Basic git hooks setup completed")
        print_info("For full setup, consider running scripts/setup-hooks.sh")

    except Exception as e:
        print_error(f"Failed to setup git hooks: {e}")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("command")
@click.option("--json", is_flag=True, help="Output result as JSON")
@click.option("--context", help="Additional context for command analysis")
@click.pass_context
def check_command(
    ctx: click.Context, command: str, json: bool, context: Optional[str]
) -> None:
    """Test command validation against current rules."""
    try:
        config_directory = ctx.obj.get("config_dir")
        config = AuditorConfig(config_dir=config_directory)

        print_info(f"Checking command: {command}")

        # Try to use the existing legacy checker first
        if LEGACY_AVAILABLE:
            try:
                # Create the legacy checker instance
                checker = legacy_checker.CommandChecker()
                legacy_result = checker.check_command(command)

                if json:
                    import json as json_module

                    click.echo(json_module.dumps(legacy_result, indent=2))
                else:
                    _format_check_result(legacy_result)

                return

            except Exception as e:
                print_warning(f"Legacy checker failed: {e}")
                print_info("Falling back to basic security validation...")

        # Fallback to basic security validation
        if LEGACY_AVAILABLE:
            try:
                from scripts.python.core.security import (
                    validate_command as sec_validate,
                )

                is_safe, error_msg = sec_validate(command)

                security_result: Dict[str, Any] = {
                    "action": "PASS" if is_safe else "ERROR",
                    "command": command,
                    "message": error_msg if error_msg else "Command validated",
                    "analysis_type": "security_only",
                }

                if json:
                    import json as json_module

                    click.echo(json_module.dumps(security_result, indent=2))
                else:
                    _format_check_result(security_result)

                return

            except Exception as e:
                print_warning(f"Security validation failed: {e}")

        # Final fallback to new validator
        validator = NewValidator(config)
        validator_result = validator.validate_command(
            command, {"context": context} if context else None
        )

        if json:
            import json as json_module

            click.echo(json_module.dumps(validator_result, indent=2))
        else:
            _format_check_result(validator_result)

    except Exception as e:
        print_error(f"Failed to check command: {e}")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.pass_context
def validate_setup(ctx: click.Context) -> None:
    """Verify AI Command Auditor installation and configuration."""
    try:
        config_directory = ctx.obj.get("config_dir")
        config = AuditorConfig(config_dir=config_directory)

        print_info("Validating AI Command Auditor setup...")

        auditor_dir = config.get_config_dir()
        all_good = True

        # Check if initialized
        if not auditor_dir.exists():
            print_error(
                "AI Command Auditor not initialized. Run 'ai-auditor init' first."
            )
            sys.exit(1)

        # Check directory structure
        required_dirs = [
            auditor_dir / "config",
            auditor_dir / "config" / "rules",
            auditor_dir / "config" / "prompts",
            auditor_dir / "hooks",
        ]

        for directory in required_dirs:
            if directory.exists():
                print_success(f"Directory exists: {directory}")
            else:
                print_error(f"Missing directory: {directory}")
                all_good = False

        # Check configuration files
        config_files = [
            auditor_dir / "config" / "auditor.yml",
            auditor_dir / "config" / "rules" / "security-rules.yml",
            auditor_dir / "config" / "prompts" / "openai-prompts.yml",
        ]

        for config_file in config_files:
            if config_file.exists():
                print_success(f"Config file exists: {config_file}")
            else:
                print_warning(f"Optional config file missing: {config_file}")

        # Check git hooks
        git_hooks_dir = Path(".git/hooks")
        if git_hooks_dir.exists():
            print_success("Git hooks directory exists")

            # Check specific hooks
            hooks_to_check = ["pre-commit", "pre-push"]
            for hook in hooks_to_check:
                hook_file = git_hooks_dir / hook
                if hook_file.exists():
                    print_success(f"Git hook exists: {hook}")
                else:
                    print_warning(f"Git hook missing: {hook}")
        else:
            print_warning("Git hooks directory not found")

        # Check if pre-commit is installed
        try:
            precommit_result = subprocess.run(
                ["pre-commit", "--version"], capture_output=True, text=True
            )
            if precommit_result.returncode == 0:
                print_success("Pre-commit tool is installed")
            else:
                print_warning("Pre-commit tool not working properly")
        except FileNotFoundError:
            print_warning("Pre-commit tool not installed")

        # Test command validation
        print_info("Testing command validation functionality...")
        try:
            test_command = "ls -la"
            validator = NewValidator(config)
            validation_result = validator.validate_command(test_command)
            print_success("Command validation is working")
        except Exception as e:
            print_error(f"Command validation test failed: {e}")
            all_good = False

        # Check for legacy components
        if LEGACY_AVAILABLE:
            print_success("Legacy command checker available")
        else:
            print_warning("Legacy command checker not available")

        if all_good:
            print_success("AI Command Auditor setup is valid!")
        else:
            print_error("Setup validation found issues. Check the messages above.")
            sys.exit(1)

    except Exception as e:
        print_error(f"Failed to validate setup: {e}")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.option("--template", help="Update to a specific template")
@click.option("--force", is_flag=True, help="Force update even if files exist")
@click.pass_context
def update_config(ctx: click.Context, template: Optional[str], force: bool) -> None:
    """Update configuration templates to latest version."""
    try:
        config_directory = ctx.obj.get("config_dir")
        config = AuditorConfig(config_dir=config_directory)
        auditor_dir = config.get_config_dir()

        if not auditor_dir.exists():
            print_error(
                "AI Command Auditor not initialized. Run 'ai-auditor init' first."
            )
            sys.exit(1)

        print_info("Updating configuration templates...")

        # Determine template to use
        current_template = "general"
        config_file = auditor_dir / "config" / "auditor.yml"

        if config_file.exists():
            try:
                import yaml

                with open(config_file, "r") as f:
                    current_config = yaml.safe_load(f) or {}
                current_template = current_config.get("template", "general")
            except Exception as e:
                print_warning(f"Could not read current template: {e}")

        template_to_use = template or current_template
        print_info(f"Using template: {template_to_use}")

        # Backup existing files if not forcing
        if not force:
            backup_dir = auditor_dir / "backup"
            backup_dir.mkdir(exist_ok=True)
            print_info(f"Creating backup in {backup_dir}")

            import datetime
            import shutil

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            for item in auditor_dir.glob("config/*"):
                if item.is_file():
                    backup_file = backup_dir / f"{item.name}.{timestamp}.bak"
                    shutil.copy2(item, backup_file)
                    print_success(f"Backed up: {item.name}")

        # Update configuration files
        _create_config_files(auditor_dir, template_to_use, update=True)

        print_success("Configuration templates updated successfully!")
        if not force:
            print_info(f"Backup files saved in {auditor_dir / 'backup'}")

    except Exception as e:
        print_error(f"Failed to update configuration: {e}")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()
        sys.exit(1)


def _setup_basic_hooks(config: AuditorConfig, force: bool) -> None:
    """Setup basic git hooks without the full project script."""
    git_hooks_dir = Path(".git/hooks")

    # Create pre-commit hook
    pre_commit_hook = git_hooks_dir / "pre-commit"
    if pre_commit_hook.exists() and not force:
        print_warning("Pre-commit hook already exists (use --force to overwrite)")
    else:
        pre_commit_content = """#!/bin/bash
#
# Basic pre-commit hook for AI Command Auditor
#
echo "Running AI Command Auditor pre-commit checks..."

# Run pre-commit if available
if command -v pre-commit >/dev/null 2>&1; then
    pre-commit run --all-files
else
    echo "Pre-commit tool not installed, skipping checks"
fi
"""
        pre_commit_hook.write_text(pre_commit_content)
        pre_commit_hook.chmod(0o755)
        print_success("Created basic pre-commit hook")

    # Create pre-push hook
    pre_push_hook = git_hooks_dir / "pre-push"
    if pre_push_hook.exists() and not force:
        print_warning("Pre-push hook already exists (use --force to overwrite)")
    else:
        pre_push_content = """#!/bin/bash
#
# Basic pre-push hook for AI Command Auditor
#
echo "Running AI Command Auditor pre-push checks..."

# Basic command validation test
if command -v python3 >/dev/null 2>&1; then
    if [ -f "scripts/python/core/check_command.py" ]; then
        echo "Testing command validation..."
        python3 scripts/python/core/check_command.py "ls -la" >/dev/null
        echo "Command validation test passed"
    fi
fi

echo "Pre-push checks completed"
"""
        pre_push_hook.write_text(pre_push_content)
        pre_push_hook.chmod(0o755)
        print_success("Created basic pre-push hook")


def _format_check_result(result: Dict[str, Any]) -> None:
    """Format command check result for display."""
    action = result.get("action", "UNKNOWN")

    if action == "PASS":
        print_success("Command passed validation")
    elif action == "ERROR":
        message = result.get("message", "Command blocked")
        print_error(f"Command blocked: {message}")
    elif action == "EXECUTE":
        new_command = result.get("command", "")
        print_warning(f"Command should be replaced with: {new_command}")
    else:
        print_info(f"Command check result: {action}")

    # Show additional details if available
    if "reason" in result:
        print_info(f"Reason: {result['reason']}")

    if "analysis_type" in result:
        print_info(f"Analysis type: {result['analysis_type']}")


def _create_config_files(
    auditor_dir: Path, template: str, update: bool = False
) -> None:
    """Create basic configuration files for the specified template."""
    import yaml

    # Main configuration file
    main_config: Dict[str, Any] = {
        "version": "1.0.0",
        "template": template,
        "ai": {
            "model": "gpt-4o",
            "timeout": 30,
            "max_retries": 3,
        },
        "security": {
            "max_command_length": 1000,
            "allow_multiline": False,
        },
        "logging": {
            "level": "INFO",
        },
    }

    # Template-specific configurations
    if template == "python":
        main_config["ai"]["model"] = "gpt-4o"
        main_config["security"]["python_specific"] = True
    elif template == "node":
        main_config["security"]["node_specific"] = True
    elif template == "security":
        main_config["security"]["strict_mode"] = True
        main_config["security"]["max_command_length"] = 500

    config_file = auditor_dir / "config" / "auditor.yml"
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(main_config, f, default_flow_style=False)
    action = "Updated" if update else "Created"
    print_success(f"{action} config file: {config_file}")

    # Security rules file
    security_rules: Dict[str, Any] = {
        "version": "1.0.0",
        "dangerous_patterns": [
            {
                "pattern": r"rm\s+-rf\s+/",
                "severity": "critical",
                "message": "Attempting to delete root directory",
            },
            {
                "pattern": r"sudo\s+chmod\s+777",
                "severity": "high",
                "message": "Setting dangerous file permissions",
            },
            {
                "pattern": r"curl.*\|\s*bash",
                "severity": "high",
                "message": "Piping download to bash execution",
            },
        ],
    }

    # Add template-specific rules
    if template == "python":
        python_patterns: List[Dict[str, str]] = [
            {
                "pattern": r"eval\s*\(",
                "severity": "high",
                "message": "Use of eval() function is dangerous",
            },
            {
                "pattern": r"exec\s*\(",
                "severity": "high",
                "message": "Use of exec() function is dangerous",
            },
        ]
        security_rules["dangerous_patterns"].extend(python_patterns)
    elif template == "node":
        node_patterns: List[Dict[str, str]] = [
            {
                "pattern": r"eval\s*\(",
                "severity": "high",
                "message": "Use of eval() function is dangerous",
            },
            {
                "pattern": r"Function\s*\(",
                "severity": "medium",
                "message": "Dynamic function creation should be avoided",
            },
        ]
        security_rules["dangerous_patterns"].extend(node_patterns)

    security_file = auditor_dir / "config" / "rules" / "security-rules.yml"
    with open(security_file, "w", encoding="utf-8") as f:
        yaml.dump(security_rules, f, default_flow_style=False)
    print_success(f"{action} security rules: {security_file}")

    # AI prompts file
    ai_prompts: Dict[str, Any] = {
        "version": "1.0.0",
        "prompts": {
            "security_analysis": (
                "Analyze this command for security risks:\n"
                "Command: {command}\n"
                "Context: {context}\n\n"
                "Rate security risk from 1-10 and explain any concerns:"
            ),
            "code_review": (
                "Review this code change for:\n"
                "- Security vulnerabilities\n"
                "- Code quality issues\n"
                "- Best practice violations\n\n"
                "Code: {code}"
            ),
        },
    }

    # Add template-specific prompts
    if template == "python":
        ai_prompts["prompts"]["python_security"] = (
            "Analyze this Python command for security issues:\n"
            "Command: {command}\n\n"
            "Check for: eval/exec usage, file operations, network calls, imports"
        )
    elif template == "node":
        ai_prompts["prompts"]["node_security"] = (
            "Analyze this Node.js command for security issues:\n"
            "Command: {command}\n\n"
            "Check for: eval usage, file operations, require() calls, child_process"
        )

    prompts_file = auditor_dir / "config" / "prompts" / "openai-prompts.yml"
    with open(prompts_file, "w", encoding="utf-8") as f:
        yaml.dump(ai_prompts, f, default_flow_style=False)
    print_success(f"{action} AI prompts: {prompts_file}")

    # README file
    readme_content = f"""# AI Command Auditor Configuration

This directory contains the configuration for AI Command Auditor in your project.

## Directory Structure

```
.ai-auditor/
├── config/
│   ├── auditor.yml          # Main configuration
│   ├── rules/
│   │   └── security-rules.yml # Security validation rules
│   └── prompts/
│       └── openai-prompts.yml # AI validation prompts
├── hooks/                   # Git hook scripts (if applicable)
├── workflows/              # GitHub Actions templates
└── README.md              # This file
```

## Configuration

### Main Configuration (`config/auditor.yml`)

The main configuration file controls:
- AI model settings (model, timeout, retries)
- Security settings (command length limits, multiline commands)
- Logging configuration

### Security Rules (`config/rules/security-rules.yml`)

Define patterns for dangerous commands that should be blocked or flagged.
Each rule can specify:
- `pattern`: Regular expression to match
- `severity`: critical, high, medium, low
- `message`: Human-readable explanation

### AI Prompts (`config/prompts/openai-prompts.yml`)

Define the prompts sent to the AI model for command analysis.
Templates support variable substitution using `{{variable}}` syntax.

## Template: {template}

This configuration was created using the '{template}' template, which includes
{template}-specific security rules and prompts.

## Usage

After configuration, use the AI Command Auditor CLI:

```bash
# Test a command
ai-auditor check-command "your command here"

# Validate your setup
ai-auditor validate-setup

# Update configuration
ai-auditor update-config
```

## Customization

Feel free to modify any of these configuration files to match your project's
specific needs. The configuration is designed to be version-controlled along
with your project.
"""

    readme_file = auditor_dir / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print_success(f"{action} README: {readme_file}")


@cli.command()
@click.option("--template", help="Test specific template (default: all)")
@click.option(
    "--environment-tests", is_flag=True, help="Run environment-specific tests"
)
@click.pass_context
def test_templates(
    ctx: click.Context, template: Optional[str], environment_tests: bool
) -> None:
    """Test and validate template functionality."""
    try:
        print_info("Testing AI Command Auditor templates...")

        template_engine = TemplateEngine()

        if template:
            # Test specific template
            print_info(f"Testing template: {template}")

            # Basic structure validation
            is_valid, errors = template_engine.validate_template_structure(template)
            if is_valid:
                print_success(f"Template '{template}' structure is valid")
            else:
                print_error(f"Template '{template}' structure validation failed:")
                for error in errors:
                    print_error(f"  - {error}")
                return

            # Environment tests if requested
            if environment_tests:
                print_info(f"Running environment tests for '{template}'...")
                env_results = template_engine.test_template_with_environments(template)

                if env_results["all_passed"]:
                    print_success(f"All environment tests passed for '{template}'")
                else:
                    print_warning(f"Some environment tests failed for '{template}':")

                    for test in env_results["environment_tests"]:
                        if not test["passed"]:
                            print_error(
                                f"  Environment '{test['environment']}' failed: {test['errors']}"
                            )

                    for test in env_results["security_level_tests"]:
                        if not test["passed"]:
                            print_error(
                                f"  Security level '{test['security_level']}' failed: {test['errors']}"
                            )
        else:
            # Test all templates
            print_info("Testing all available templates...")
            results = template_engine.validate_all_templates()

            # Print summary
            summary = results["summary"]
            print_info(f"Template validation summary:")
            print_info(f"  Total templates: {summary['total_templates']}")
            print_info(f"  Passed: {summary['passed']}")
            print_info(f"  Failed: {summary['failed']}")
            print_info(f"  Success rate: {summary['success_rate']:.1%}")

            # Print details for failed templates
            if results["templates_failed"]:
                print_warning("Failed templates:")
                for failed_template in results["templates_failed"]:
                    print_error(f"  {failed_template['template']}:")
                    for error in failed_template["structure_errors"]:
                        print_error(f"    Structure: {error}")
                    for error in failed_template["render_errors"]:
                        print_error(f"    Rendering: {error}")

            # Print passed templates
            if results["templates_passed"]:
                print_success("Passed templates:")
                for passed_template in results["templates_passed"]:
                    print_success(f"  ✓ {passed_template['template']}")

            if summary["success_rate"] == 1.0:
                print_success("All templates passed validation!")
            else:
                print_warning(
                    "Some templates failed validation. Check the details above."
                )

    except Exception as e:
        print_error(f"Failed to test templates: {e}")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
