---
layout: single
title: "API Reference"
description: "Complete CLI and Python API documentation"
toc: true
toc_label: "API Topics"
toc_icon: "code"
sidebar:
  nav: "docs"
---

# 🔌 API Reference

AI Command Auditor provides both a powerful command-line interface (CLI) and a comprehensive Python API for integration into your workflows and applications.

## 🖥️ Command Line Interface (CLI)

The CLI is the primary way to interact with AI Command Auditor. It provides commands for validation, configuration, and integration.

### Quick Reference

```bash
# Core Commands
ai-auditor check-command "your command here"    # Validate a command
ai-auditor init                                 # Initialize in project
ai-auditor setup-hooks                          # Setup git hooks

# Configuration
ai-auditor config show                          # View configuration
ai-auditor config set security.strict_mode true # Update settings

# Information
ai-auditor --version                            # Show version
ai-auditor --help                               # Show help
```

<div class="cli-grid">
  <div class="cli-section">
    <h3>🔍 Command Validation</h3>
    <p>Validate individual commands or scripts for security</p>
    <a href="/api/cli/#command-validation" class="btn btn--primary">View Commands</a>
  </div>

  <div class="cli-section">
    <h3>⚙️ Configuration</h3>
    <p>Manage configuration settings and templates</p>
    <a href="/api/cli/#configuration" class="btn btn--primary">View Commands</a>
  </div>

  <div class="cli-section">
    <h3>🔗 Git Integration</h3>
    <p>Setup and manage git hooks integration</p>
    <a href="/api/cli/#git-integration" class="btn btn--primary">View Commands</a>
  </div>

  <div class="cli-section">
    <h3>📊 Reporting</h3>
    <p>Generate reports and view analysis results</p>
    <a href="/api/cli/#reporting" class="btn btn--primary">View Commands</a>
  </div>
</div>

## 🐍 Python API

The Python API allows you to integrate AI Command Auditor into your Python applications, scripts, and automation workflows.

```python
from ai_command_auditor import CommandAuditor, SecurityRules

# Initialize auditor
auditor = CommandAuditor()

# Check a command
result = auditor.analyze_command("rm -rf /tmp/*")
print(f"Safety Score: {result.safety_score}")
print(f"Recommendations: {result.recommendations}")

# Load custom rules
rules = SecurityRules.from_file("custom-rules.yml")
auditor.update_rules(rules)
```

<div class="api-grid">
  <div class="api-section">
    <h3>🔧 Core API</h3>
    <p>Main classes and functions for command analysis</p>
    <a href="/api/python/#core-api" class="btn btn--primary">View API</a>
  </div>

  <div class="api-section">
    <h3>🛡️ Security API</h3>
    <p>Security rules, validation, and policy management</p>
    <a href="/api/python/#security-api" class="btn btn--primary">View API</a>
  </div>

  <div class="api-section">
    <h3>🤖 AI Integration</h3>
    <p>AI model configuration and prompt management</p>
    <a href="/api/python/#ai-integration" class="btn btn--primary">View API</a>
  </div>

  <div class="api-section">
    <h3>🔌 Extensions</h3>
    <p>Plugin system and custom validators</p>
    <a href="/api/python/#extensions" class="btn btn--primary">View API</a>
  </div>
</div>

## 🚀 Getting Started Examples

### CLI Quick Start

```bash
# 1. Install and initialize
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
cd your-project && ai-auditor init

# 2. Check your first command
ai-auditor check-command "sudo rm -rf /var/log/*"

# 3. Setup git hooks
ai-auditor setup-hooks

# 4. Configure for your project
ai-auditor config set templates.default "python"
```

### Python API Quick Start

```python
# 1. Install the package
# pip install ai-command-auditor

# 2. Basic usage
from ai_command_auditor import CommandAuditor

auditor = CommandAuditor()
result = auditor.analyze_command("python -c 'import os; os.system(\"rm -rf /\")'")

if result.is_dangerous:
    print(f"⚠️  Dangerous command detected!")
    print(f"Severity: {result.severity}")
    print(f"Reason: {result.reason}")
else:
    print("✅ Command appears safe")

# 3. Custom configuration
auditor.configure({
    'security': {'strict_mode': True},
    'ai': {'model': 'gpt-4o'}
})
```

## 📖 Detailed Documentation

### CLI Documentation

The complete CLI reference covers all commands, options, and use cases:

| Section | Description | Link |
|---------|-------------|------|
| **Command Validation** | Validate commands and scripts | [CLI Commands →](/api/cli/#command-validation) |
| **Configuration Management** | Manage settings and templates | [Config Commands →](/api/cli/#configuration) |
| **Git Integration** | Setup hooks and automation | [Git Commands →](/api/cli/#git-integration) |
| **Reporting & Analysis** | Generate reports and insights | [Report Commands →](/api/cli/#reporting) |
| **Utility Commands** | Helper and diagnostic commands | [Utility Commands →](/api/cli/#utilities) |

### Python API Documentation

Complete Python API reference with examples:

| Module | Description | Link |
|--------|-------------|------|
| **`CommandAuditor`** | Main auditor class and methods | [Core API →](/api/python/#commandauditor) |
| **`SecurityRules`** | Security policy management | [Security API →](/api/python/#securityrules) |
| **`AIAnalyzer`** | AI-powered analysis engine | [AI API →](/api/python/#aianalyzer) |
| **`Configuration`** | Configuration management | [Config API →](/api/python/#configuration) |
| **`Validators`** | Custom validation framework | [Validators →](/api/python/#validators) |

## 🔗 Integration Patterns

### CI/CD Integration

```yaml
# GitHub Actions example
name: Command Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install AI Command Auditor
        run: curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh

      - name: Validate Commands
        run: |
          ai-auditor scan-scripts scripts/
          ai-auditor validate-makefile Makefile
```

### Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ai-command-auditor
        name: AI Command Auditor
        entry: ai-auditor check-staged-commands
        language: system
        stages: [commit]
```

### Python Integration

```python
# Custom integration example
import subprocess
from ai_command_auditor import CommandAuditor

class SafeCommandRunner:
    def __init__(self):
        self.auditor = CommandAuditor()

    def run_command(self, command: str) -> str:
        # Validate before execution
        result = self.auditor.analyze_command(command)

        if result.is_dangerous:
            raise SecurityError(f"Dangerous command blocked: {result.reason}")

        # Execute if safe
        return subprocess.check_output(command, shell=True, text=True)

# Usage
runner = SafeCommandRunner()
output = runner.run_command("ls -la")  # Safe
# runner.run_command("rm -rf /")       # Would raise SecurityError
```

## 🛠️ Development & Extension

### Custom Validators

```python
from ai_command_auditor.validators import BaseValidator

class CustomValidator(BaseValidator):
    def __init__(self):
        super().__init__("custom_validator")

    def validate(self, command: str) -> ValidationResult:
        # Custom validation logic
        if "dangerous_pattern" in command:
            return ValidationResult(
                valid=False,
                severity="high",
                message="Custom security rule violation"
            )
        return ValidationResult(valid=True)

# Register custom validator
auditor = CommandAuditor()
auditor.add_validator(CustomValidator())
```

### Plugin Development

```python
# Create a plugin
from ai_command_auditor.plugins import BasePlugin

class MyPlugin(BasePlugin):
    def on_command_analyzed(self, command: str, result: AnalysisResult):
        # Custom post-analysis logic
        if result.severity == "critical":
            self.send_alert(command, result)

    def send_alert(self, command: str, result: AnalysisResult):
        # Send notification, log to external system, etc.
        pass

# Load plugin
auditor.load_plugin(MyPlugin())
```

## 📊 Performance & Optimization

### Async API Usage

```python
import asyncio
from ai_command_auditor import AsyncCommandAuditor

async def validate_commands(commands: list[str]):
    auditor = AsyncCommandAuditor()

    # Validate multiple commands concurrently
    results = await asyncio.gather(*[
        auditor.analyze_command(cmd) for cmd in commands
    ])

    return results

# Usage
commands = ["ls -la", "rm temp.txt", "python script.py"]
results = asyncio.run(validate_commands(commands))
```

### Caching and Performance

```python
from ai_command_auditor import CommandAuditor

# Configure caching for better performance
auditor = CommandAuditor({
    'performance': {
        'cache_enabled': True,
        'cache_ttl': 3600,  # 1 hour
        'parallel_requests': 5
    }
})

# Batch processing
results = auditor.analyze_commands(command_list, batch_size=10)
```

## 🔍 Advanced Usage

### Custom AI Models

```python
# Use custom AI model
auditor = CommandAuditor({
    'ai': {
        'model': 'custom-model',
        'api_base': 'https://your-api.com/v1',
        'api_key': 'your-api-key'
    }
})
```

### Security Policy Management

```python
from ai_command_auditor import SecurityPolicy

# Create custom security policy
policy = SecurityPolicy()
policy.add_rule("no_rm_rf", r"rm\s+-rf\s+/", severity="critical")
policy.add_rule("no_curl_eval", r"curl.*\|\s*sh", severity="high")

auditor = CommandAuditor()
auditor.apply_policy(policy)
```

## 📚 API Reference Links

### Complete Documentation

- 🖥️ [**Complete CLI Reference**](/api/cli/) - All CLI commands and options
- 🐍 [**Complete Python API**](/api/python/) - Full Python API documentation
- 🔗 [**Integration Guide**](/api/integration/) - Integration patterns and examples
- 👩‍💻 [**Developer Guide**](/api/developer/) - Contributing and development

### Quick Links

- [Installation Guide](/installation/) - Get started quickly
- [Configuration Reference](/configuration/) - Configure for your needs
- [Examples & Tutorials](/examples/) - Learn with practical examples
- [Support & FAQ](/support/) - Get help and find answers

<style>
.cli-grid, .api-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.cli-section, .api-section {
  padding: 1.5rem;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  text-align: center;
  background: #f8f9fa;
}

.cli-section h3, .api-section h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.cli-section p, .api-section p {
  margin-bottom: 1rem;
}

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

@media (max-width: 768px) {
  .cli-grid, .api-grid {
    grid-template-columns: 1fr;
  }

  table {
    font-size: 0.9rem;
  }
}
</style>
