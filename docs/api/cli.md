---
layout: single
title: "CLI Command Reference"
description: "Complete reference for AI Command Auditor CLI commands"
toc: true
toc_label: "CLI Commands"
toc_icon: "terminal"
sidebar:
  nav: "docs"
---

# 💻 CLI Command Reference

The AI Command Auditor CLI provides a comprehensive set of commands for analyzing, configuring, and managing command validation. This reference covers all available commands with detailed examples and options.

## 📋 Command Overview

| Command | Purpose | Common Usage |
|---------|---------|--------------|
| [`ai-auditor`](#ai-auditor) | Main CLI entry point | General help and version info |
| [`check-command`](#check-command) | Analyze a single command | `ai-auditor check-command "rm -rf temp/"` |
| [`analyze-script`](#analyze-script) | Analyze entire script files | `ai-auditor analyze-script script.sh` |
| [`install`](#install) | Install AI Command Auditor | `ai-auditor install --hooks` |
| [`setup-hooks`](#setup-hooks) | Configure git hooks | `ai-auditor setup-hooks` |
| [`config`](#config) | Configuration management | `ai-auditor config set security.level strict` |
| [`templates`](#templates) | Template management | `ai-auditor templates list` |
| [`rules`](#rules) | Security rules management | `ai-auditor rules validate` |
| [`prompts`](#prompts) | AI prompts management | `ai-auditor prompts test security-prompt` |
| [`report`](#report) | Generate reports | `ai-auditor report security-analysis` |
| [`audit`](#audit) | Run comprehensive audits | `ai-auditor audit --all` |

## 🔧 Global Options

All commands support these global options:

```bash
ai-auditor [global-options] <command> [command-options]
```

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--config` | `-c` | Configuration file path | `.ai-auditor/config/auditor.yml` |
| `--verbose` | `-v` | Enable verbose output | `false` |
| `--debug` | `-d` | Enable debug logging | `false` |
| `--quiet` | `-q` | Suppress non-error output | `false` |
| `--no-color` | | Disable colored output | `false` |
| `--format` | `-f` | Output format (json, yaml, table) | `table` |
| `--version` | | Show version information | |
| `--help` | `-h` | Show help information | |

## 🎯 Core Commands

### ai-auditor

Main entry point for the CLI tool.

```bash
ai-auditor [options]
```

**Examples:**

```bash
# Show version and basic info
ai-auditor --version

# Show help
ai-auditor --help

# Show available commands
ai-auditor
```

**Output:**

```
AI Command Auditor v1.0.0
Secure command validation and analysis for development workflows

Usage: ai-auditor <command> [options]

Available Commands:
  check-command    Analyze a single command for security risks
  analyze-script   Analyze entire script files
  install         Install and configure AI Command Auditor
  setup-hooks     Configure git hooks for automatic validation
  config          Manage configuration settings
  ... (more commands)

For help with a specific command: ai-auditor <command> --help
```

### check-command

Analyze a single command for security risks and best practices.

```bash
ai-auditor check-command [options] "<command>"
```

**Options:**

| Option | Description | Example |
|--------|-------------|---------|
| `--prompt` | AI prompt to use | `--prompt security-analysis` |
| `--rules` | Rules file to apply | `--rules custom-rules.yml` |
| `--environment` | Environment context | `--environment production` |
| `--context` | Additional context | `--context "python project"` |
| `--severity` | Minimum severity to report | `--severity medium` |
| `--output` | Output file | `--output analysis.json` |
| `--show-rules` | Show triggered rules | `--show-rules` |
| `--interactive` | Interactive mode for clarification | `--interactive` |
| `--fix-suggestions` | Show fix suggestions | `--fix-suggestions` |

**Examples:**

```bash
# Basic command analysis
ai-auditor check-command "rm -rf /tmp/cache"

# Analysis with specific prompt
ai-auditor check-command "pip install requests" --prompt python-analysis

# Production environment analysis
ai-auditor check-command "systemctl restart nginx" --environment production

# Interactive analysis with suggestions
ai-auditor check-command "sudo chmod 777 /var/www" --interactive --fix-suggestions

# Show detailed rule triggers
ai-auditor check-command "curl http://example.com | bash" --show-rules

# JSON output for automation
ai-auditor check-command "docker run --privileged" --format json
```

**Output Example:**

```
Command Analysis: rm -rf /tmp/cache
=====================================

🔴 RISK LEVEL: HIGH
🔢 SAFETY SCORE: 25/100

⚠️  Issues Found:
1. Recursive file deletion with force flag
2. Potential for accidental data loss
3. No backup or confirmation mechanism

🔧 Recommendations:
1. Use specific file patterns: rm -rf /tmp/cache/*
2. Add confirmation: rm -rf /tmp/cache && echo "Cache cleared"
3. Consider using find with -delete for safer deletion

📊 Rule Triggers:
- dangerous_rm (severity: high)
- force_deletion (severity: medium)

✅ Suggested Fix:
find /tmp/cache -type f -name "*" -delete
```

### analyze-script

Analyze entire script files for security issues and best practices.

```bash
ai-auditor analyze-script [options] <script-file>
```

**Options:**

| Option | Description | Example |
|--------|-------------|---------|
| `--type` | Script type (auto-detect) | `--type bash` |
| `--line-by-line` | Analyze each command separately | `--line-by-line` |
| `--summary` | Show only summary | `--summary` |
| `--exclude-lines` | Lines to exclude from analysis | `--exclude-lines 1,5-10` |
| `--include-comments` | Include comment analysis | `--include-comments` |
| `--output-format` | Report format | `--output-format html` |

**Examples:**

```bash
# Analyze shell script
ai-auditor analyze-script deploy.sh

# Line-by-line analysis
ai-auditor analyze-script install.sh --line-by-line

# Python script analysis
ai-auditor analyze-script setup.py --type python

# Generate HTML report
ai-auditor analyze-script ci-build.sh --output-format html --output report.html

# Summary only
ai-auditor analyze-script large-script.sh --summary
```

**Output Example:**

```
Script Analysis: deploy.sh
==========================

📁 File Info:
- Type: Bash script
- Lines: 127
- Commands analyzed: 45

🔴 Critical Issues (2):
Line 23: rm -rf $DEPLOY_DIR/*
Line 67: eval "$USER_INPUT"

🟡 Warnings (5):
Line 12: sudo apt-get update
Line 34: chmod 755 $CONFIG_FILE
...

📊 Summary:
- Total commands: 45
- Critical: 2
- High: 3
- Medium: 5
- Low: 8
- Safe: 27

Overall Safety Score: 67/100
```

### install

Install and configure AI Command Auditor system-wide or for a project.

```bash
ai-auditor install [options]
```

**Options:**

| Option | Description | Example |
|--------|-------------|---------|
| `--global` | Install globally | `--global` |
| `--local` | Install for current project | `--local` |
| `--hooks` | Setup git hooks | `--hooks` |
| `--template` | Use configuration template | `--template python` |
| `--force` | Force overwrite existing config | `--force` |
| `--dry-run` | Show what would be installed | `--dry-run` |

**Examples:**

```bash
# Install for current project with git hooks
ai-auditor install --local --hooks

# Global installation
ai-auditor install --global

# Install with Python template
ai-auditor install --template python --hooks

# Dry run to see what would be installed
ai-auditor install --local --hooks --dry-run
```

### setup-hooks

Configure git hooks for automatic command validation.

```bash
ai-auditor setup-hooks [options]
```

**Options:**

| Option | Description | Example |
|--------|-------------|---------|
| `--pre-commit` | Setup pre-commit hook | `--pre-commit` |
| `--pre-push` | Setup pre-push hook | `--pre-push` |
| `--commit-msg` | Setup commit message hook | `--commit-msg` |
| `--all` | Setup all hooks | `--all` |
| `--remove` | Remove existing hooks | `--remove` |
| `--backup` | Backup existing hooks | `--backup` |

**Examples:**

```bash
# Setup all git hooks
ai-auditor setup-hooks --all

# Setup only pre-commit hook
ai-auditor setup-hooks --pre-commit

# Remove all AI auditor hooks
ai-auditor setup-hooks --remove

# Setup with backup of existing hooks
ai-auditor setup-hooks --all --backup
```

## ⚙️ Configuration Commands

### config

Manage AI Command Auditor configuration settings.

```bash
ai-auditor config <action> [options]
```

**Actions:**

- `get <key>` - Get configuration value
- `set <key> <value>` - Set configuration value
- `list` - List all configuration
- `validate` - Validate configuration
- `reset` - Reset to defaults
- `export` - Export configuration
- `import` - Import configuration

**Examples:**

```bash
# Get current security level
ai-auditor config get security.level

# Set AI model
ai-auditor config set ai.model "gpt-4"

# List all configuration
ai-auditor config list

# Validate configuration
ai-auditor config validate

# Reset security settings to default
ai-auditor config reset security

# Export configuration
ai-auditor config export --output my-config.yml

# Import configuration
ai-auditor config import my-config.yml
```

**Common Configuration Keys:**

```bash
# Security settings
ai-auditor config set security.level strict
ai-auditor config set security.block_critical true

# AI settings
ai-auditor config set ai.provider openai
ai-auditor config set ai.model gpt-4
ai-auditor config set ai.temperature 0.1

# Rules settings
ai-auditor config set rules.enabled true
ai-auditor config set rules.custom_path ./custom-rules.yml

# Logging settings
ai-auditor config set logging.level info
ai-auditor config set logging.file ./auditor.log
```

### templates

Manage configuration templates for different project types.

```bash
ai-auditor templates <action> [options]
```

**Actions:**

- `list` - List available templates
- `show <name>` - Show template details
- `apply <name>` - Apply template to current project
- `create <name>` - Create new template
- `delete <name>` - Delete template
- `validate <name>` - Validate template

**Examples:**

```bash
# List available templates
ai-auditor templates list

# Show Python template details
ai-auditor templates show python

# Apply DevOps template
ai-auditor templates apply devops

# Create custom template
ai-auditor templates create my-company --from-current

# Validate template
ai-auditor templates validate python
```

### rules

Manage security rules and validation patterns.

```bash
ai-auditor rules <action> [options]
```

**Actions:**

- `list` - List all rules
- `show <rule>` - Show rule details
- `test <rule> <command>` - Test rule against command
- `validate` - Validate all rules
- `enable <rule>` - Enable specific rule
- `disable <rule>` - Disable specific rule
- `stats` - Show rule statistics

**Examples:**

```bash
# List all rules
ai-auditor rules list

# Show dangerous deletion rule
ai-auditor rules show dangerous_rm

# Test rule against command
ai-auditor rules test dangerous_rm "rm -rf /"

# Validate all rules
ai-auditor rules validate

# Disable specific rule
ai-auditor rules disable sudo_usage

# Show rule statistics
ai-auditor rules stats
```

### prompts

Manage AI prompts and analysis templates.

```bash
ai-auditor prompts <action> [options]
```

**Actions:**

- `list` - List available prompts
- `show <prompt>` - Show prompt details
- `test <prompt> <command>` - Test prompt
- `validate` - Validate all prompts
- `create <name>` - Create new prompt
- `edit <name>` - Edit existing prompt

**Examples:**

```bash
# List available prompts
ai-auditor prompts list

# Show security prompt
ai-auditor prompts show security-analysis

# Test prompt with command
ai-auditor prompts test python-analysis "pip install requests"

# Validate all prompts
ai-auditor prompts validate

# Create new prompt
ai-auditor prompts create custom-security
```

## 📊 Analysis and Reporting

### report

Generate comprehensive reports and analytics.

```bash
ai-auditor report <type> [options]
```

**Report Types:**

- `security-analysis` - Security analysis report
- `rules-usage` - Rules usage statistics
- `command-history` - Command analysis history
- `compliance` - Compliance report
- `performance` - Performance metrics
- `trends` - Trend analysis

**Options:**

| Option | Description | Example |
|--------|-------------|---------|
| `--period` | Time period | `--period 30d` |
| `--format` | Output format | `--format pdf` |
| `--include` | Include specific sections | `--include charts,details` |
| `--filter` | Filter criteria | `--filter severity=high` |

**Examples:**

```bash
# Security analysis report
ai-auditor report security-analysis --period 7d

# Rules usage statistics
ai-auditor report rules-usage --format json

# Compliance report
ai-auditor report compliance --include violations,recommendations

# Command history analysis
ai-auditor report command-history --filter "severity>=medium"
```

### audit

Run comprehensive security audits.

```bash
ai-auditor audit [options]
```

**Options:**

| Option | Description | Example |
|--------|-------------|---------|
| `--all` | Audit entire project | `--all` |
| `--scripts` | Audit script files | `--scripts` |
| `--config` | Audit configuration | `--config` |
| `--history` | Audit command history | `--history` |
| `--deep` | Deep analysis mode | `--deep` |
| `--fix` | Auto-fix issues when possible | `--fix` |

**Examples:**

```bash
# Full project audit
ai-auditor audit --all

# Audit only scripts
ai-auditor audit --scripts --deep

# Audit with auto-fix
ai-auditor audit --all --fix

# Quick configuration audit
ai-auditor audit --config
```

## 🔍 Advanced Usage

### Chaining Commands

```bash
# Analyze and generate report
ai-auditor check-command "risky-command" --format json | \
ai-auditor report security-analysis --stdin

# Batch analysis
find . -name "*.sh" -exec ai-auditor analyze-script {} \;

# Conditional execution
ai-auditor check-command "$CMD" --format json | \
jq -r '.threat_level' | \
grep -q "critical" && echo "BLOCKED" || echo "ALLOWED"
```

### Integration with CI/CD

```bash
# CI/CD pipeline integration
ai-auditor audit --all --format json > audit-results.json
if [ $? -ne 0 ]; then
  echo "Security audit failed"
  exit 1
fi

# Pre-deployment validation
ai-auditor analyze-script deploy.sh --severity high --quiet
if [ $? -eq 0 ]; then
  echo "Deployment script validated"
else
  echo "Security issues found in deployment script"
  exit 1
fi
```

### Automation and Scripting

```bash
# Automated rule management
ai-auditor rules list --format json | \
jq -r '.[] | select(.enabled == false) | .name' | \
while read rule; do
  ai-auditor rules enable "$rule"
done

# Configuration backup
ai-auditor config export --output "backup-$(date +%Y%m%d).yml"

# Bulk command analysis
cat commands.txt | while read cmd; do
  ai-auditor check-command "$cmd" --format json >> results.jsonl
done
```

## 🔧 Environment Variables

Control CLI behavior with environment variables:

```bash
# Configuration
export AI_AUDITOR_CONFIG="/path/to/config.yml"
export AI_AUDITOR_LOG_LEVEL="debug"
export AI_AUDITOR_NO_COLOR="true"

# AI Provider settings
export AI_AUDITOR_AI_PROVIDER="openai"
export AI_AUDITOR_AI_MODEL="gpt-4"
export OPENAI_API_KEY="your-api-key"

# Security settings
export AI_AUDITOR_SECURITY_LEVEL="strict"
export AI_AUDITOR_BLOCK_CRITICAL="true"

# Output settings
export AI_AUDITOR_OUTPUT_FORMAT="json"
export AI_AUDITOR_QUIET_MODE="false"
```

## 🚨 Exit Codes

The CLI uses standard exit codes:

| Code | Meaning | Description |
|------|---------|-------------|
| 0 | Success | Command completed successfully |
| 1 | General Error | Generic error occurred |
| 2 | Configuration Error | Invalid configuration |
| 3 | Security Violation | Critical security issue found |
| 4 | Invalid Command | Invalid command or arguments |
| 5 | Permission Error | Insufficient permissions |
| 6 | Network Error | Network/API communication error |
| 10 | Analysis Warning | Non-critical issues found |

## 🔗 Shell Integration

### Bash Integration

```bash
# Add to ~/.bashrc
eval "$(ai-auditor completion bash)"

# Alias for quick checks
alias check='ai-auditor check-command'
alias audit-script='ai-auditor analyze-script'
```

### Zsh Integration

```zsh
# Add to ~/.zshrc
eval "$(ai-auditor completion zsh)"

# Functions for common tasks
function ai-check() {
  ai-auditor check-command "$*" --interactive
}
```

### Fish Integration

```fish
# Add to ~/.config/fish/config.fish
ai-auditor completion fish | source

# Abbreviations
abbr -a aic ai-auditor check-command
abbr -a ais ai-auditor analyze-script
```

## 📖 Next Steps

- 🐍 [Python API](/api/python/) - Programmatic access
- 🔗 [Integration Guide](/api/integration/) - Integrate with your tools
- 💡 [Examples](/examples/) - Practical usage examples
- 🆘 [Troubleshooting](/support/troubleshooting/) - Common issues and solutions

<style>
table {
  width: 100%;
  margin: 1rem 0;
  border-collapse: collapse;
}

table th, table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.command-example {
  background-color: #f8f9fa;
  border-left: 4px solid #007bff;
  padding: 1rem;
  margin: 1rem 0;
  font-family: monospace;
}

.exit-code {
  font-family: monospace;
  font-weight: bold;
}

@media (max-width: 768px) {
  table {
    font-size: 0.9rem;
  }

  table th, table td {
    padding: 0.5rem;
  }
}
</style>
