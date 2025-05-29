#!/usr/bin/env python3
"""
Main CLI interface for AI Command Auditor.

This module provides the command-line interface for the AI Command Auditor,
including initialization, configuration, and management commands.

Author: Etherisc
Date: 2024
Version: 1.0
"""

import sys
from pathlib import Path
from typing import Optional

import click
from colorama import Fore, Style, init

from ..core.config import AuditorConfig, get_config, setup_logging

# Initialize colorama for cross-platform colored output
init()


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
@click.pass_context
def init_command(
    ctx: click.Context, template: str, config_dir: Optional[str], force: bool
) -> None:
    """Initialize AI Command Auditor in the current project."""
    try:
        # Use config dir from command or context
        config_directory = config_dir or ctx.obj.get("config_dir")

        print_info(f"Initializing AI Command Auditor with {template} template...")

        # Create configuration
        config = AuditorConfig(config_dir=config_directory)
        auditor_dir = config.get_config_dir()

        # Check if already initialized
        if auditor_dir.exists() and not force:
            print_warning(f"AI Command Auditor already initialized in {auditor_dir}")
            print_info("Use --force to overwrite existing configuration")
            return

        # Create directory structure
        directories = [
            auditor_dir / "config" / "rules",
            auditor_dir / "config" / "prompts",
            auditor_dir / "hooks",
            auditor_dir / "workflows",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print_success(f"Created directory: {directory}")

        # Create basic configuration files
        _create_config_files(auditor_dir, template)

        print_success(f"AI Command Auditor initialized successfully!")
        print_info(f"Configuration directory: {auditor_dir}")
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

        # TODO: Implement hook setup logic
        print_warning("Git hooks setup is not yet implemented.")
        print_info("This will be implemented in Task 8.2")

    except Exception as e:
        print_error(f"Failed to setup git hooks: {e}")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument("command")
@click.pass_context
def check_command(ctx: click.Context, command: str) -> None:
    """Test command validation against current rules."""
    try:
        config_directory = ctx.obj.get("config_dir")
        config = AuditorConfig(config_dir=config_directory)

        print_info(f"Checking command: {command}")

        # TODO: Implement command checking logic
        print_warning("Command checking is not yet implemented.")
        print_info("This will be implemented in Task 8.2")

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

        all_good = True
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
            # TODO: Check specific hooks
        else:
            print_warning("Git hooks directory not found")

        if all_good:
            print_success("AI Command Auditor setup is valid!")
        else:
            print_error("Setup validation failed. Run 'ai-auditor init' to fix issues.")
            sys.exit(1)

    except Exception as e:
        print_error(f"Failed to validate setup: {e}")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()
        sys.exit(1)


def _create_config_files(auditor_dir: Path, template: str) -> None:
    """Create basic configuration files for the specified template."""

    # Main configuration file
    main_config = {
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

    config_file = auditor_dir / "config" / "auditor.yml"
    with open(config_file, "w", encoding="utf-8") as f:
        import yaml

        yaml.dump(main_config, f, default_flow_style=False)
    print_success(f"Created config file: {config_file}")

    # Security rules file
    security_rules = {
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

    security_file = auditor_dir / "config" / "rules" / "security-rules.yml"
    with open(security_file, "w", encoding="utf-8") as f:
        import yaml

        yaml.dump(security_rules, f, default_flow_style=False)
    print_success(f"Created security rules: {security_file}")

    # AI prompts file
    ai_prompts = {
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

    prompts_file = auditor_dir / "config" / "prompts" / "openai-prompts.yml"
    with open(prompts_file, "w", encoding="utf-8") as f:
        import yaml

        yaml.dump(ai_prompts, f, default_flow_style=False)
    print_success(f"Created AI prompts: {prompts_file}")

    # README file
    readme_content = f"""# AI Command Auditor Configuration

This directory contains the configuration for AI Command Auditor in your project.

## Directory Structure

- `config/auditor.yml` - Main configuration file
- `config/rules/` - Security and validation rules
- `config/prompts/` - AI prompts for analysis
- `hooks/` - Git hook scripts
- `workflows/` - GitHub Actions workflows

## Template: {template}

This configuration was initialized with the {template} template.

## Customization

Feel free to modify any files in this directory to customize the behavior
of AI Command Auditor for your project needs.

## Documentation

For more information, visit: https://etherisc.github.io/ai-command-auditor
"""

    readme_file = auditor_dir / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print_success(f"Created README: {readme_file}")


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
