---
layout: default
title: Configuration
nav_order: 4
description: "Configure AI Command Auditor for your specific needs"
---

# ⚙️ Configuration Guide

AI Command Auditor is highly configurable to fit your project's specific security and validation needs. This guide covers all configuration options, from basic setup to advanced customization.

## 🏗️ Configuration Overview

AI Command Auditor uses a hierarchical configuration system with the following structure:

```
.ai-auditor/
├── config/
│   ├── auditor.yml           # Main configuration
│   ├── rules/
│   │   ├── security-rules.yml # Security validation rules
│   │   ├── performance-rules.yml # Performance rules
│   │   └── custom-rules.yml   # Custom validation rules
│   ├── prompts/
│   │   ├── analysis-prompt.yml # AI analysis prompts
│   │   ├── security-prompt.yml # Security-specific prompts
│   │   └── custom-prompts.yml  # Custom AI prompts
│   └── templates/
│       ├── python.yml         # Python project template
│       ├── nodejs.yml         # Node.js project template
│       ├── rust.yml           # Rust project template
│       ├── general.yml        # General purpose template
│       └── security.yml       # Security-focused template
├── logs/
│   └── auditor.log           # Application logs
└── hooks/
    ├── pre-commit             # Git pre-commit hook
    └── pre-push               # Git pre-push hook
```

## 📝 Main Configuration (`auditor.yml`)

The main configuration file controls core AI Command Auditor behavior:

```yaml
# AI Configuration
ai:
  model: "gpt-4o"                    # AI model to use
  timeout: 30                        # Request timeout (seconds)
  max_retries: 3                     # Maximum retry attempts
  temperature: 0.1                   # AI creativity (0.0-1.0)
  max_tokens: 1000                   # Maximum response tokens

  # API Configuration
  api:
    base_url: "https://api.openai.com/v1"  # API endpoint
    # API key from environment: OPENAI_API_KEY

# Security Settings
security:
  max_command_length: 1000           # Maximum command length
  allow_multiline: false             # Allow multiline commands
  strict_mode: false                 # Enable strict validation
  quarantine_dangerous: true         # Quarantine dangerous commands

  # Severity thresholds
  thresholds:
    critical: "block"                # Block critical issues
    high: "warn"                     # Warn on high severity
    medium: "log"                    # Log medium severity
    low: "ignore"                    # Ignore low severity

# Logging Configuration
logging:
  level: "INFO"                      # Log level (DEBUG, INFO, WARNING, ERROR)
  file: ".ai-auditor/logs/auditor.log"  # Log file path
  max_size: "10MB"                   # Maximum log file size
  backup_count: 5                    # Number of backup files
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Performance Settings
performance:
  cache_enabled: true                # Enable response caching
  cache_ttl: 3600                   # Cache TTL (seconds)
  parallel_requests: 3               # Parallel API requests

# Git Integration
git:
  hooks_enabled: true                # Enable git hooks
  auto_setup: true                   # Auto-setup hooks on init
  backup_existing: true              # Backup existing hooks

  # Hook configuration
  hooks:
    pre_commit: true                 # Enable pre-commit hook
    pre_push: false                  # Enable pre-push hook
    commit_msg: false                # Enable commit-msg hook

# Template Settings
templates:
  default: "general"                 # Default template
  auto_detect: true                  # Auto-detect project type

# Reporting
reporting:
  enabled: true                      # Enable reporting
  format: "json"                     # Report format (json, yaml, text)
  output_dir: ".ai-auditor/reports" # Report output directory
```

## 🛡️ Security Rules Configuration

Security rules define what commands are considered dangerous or suspicious. They use pattern matching and severity levels:

<div class="config-grid">
  <div class="config-item">
    <h3>🔒 Security Rules</h3>
    <p>Define dangerous command patterns and validation rules</p>
    <a href="/configuration/security-rules/" class="btn btn--primary">Configure Rules</a>
  </div>

  <div class="config-item">
    <h3>🎯 Performance Rules</h3>
    <p>Validate commands for performance and efficiency</p>
    <a href="/configuration/performance-rules/" class="btn btn--primary">Configure Performance</a>
  </div>

  <div class="config-item">
    <h3>✏️ Custom Rules</h3>
    <p>Create your own validation rules and patterns</p>
    <a href="/configuration/custom-rules/" class="btn btn--primary">Create Custom Rules</a>
  </div>
</div>

## 🤖 AI Prompts Configuration

Customize how AI analyzes commands by configuring prompts:

<div class="config-grid">
  <div class="config-item">
    <h3>🧠 Analysis Prompts</h3>
    <p>Configure how AI analyzes command safety and intent</p>
    <a href="/configuration/ai-prompts/#analysis-prompts" class="btn btn--primary">Configure Analysis</a>
  </div>

  <div class="config-item">
    <h3>🔐 Security Prompts</h3>
    <p>Specialized prompts for security-focused analysis</p>
    <a href="/configuration/ai-prompts/#security-prompts" class="btn btn--primary">Configure Security</a>
  </div>

  <div class="config-item">
    <h3>🎨 Custom Prompts</h3>
    <p>Create domain-specific analysis prompts</p>
    <a href="/configuration/ai-prompts/#custom-prompts" class="btn btn--primary">Create Custom</a>
  </div>
</div>

## 🎨 Template System

Templates provide pre-configured settings for different project types:

<div class="template-grid">
  <div class="template-item">
    <h4>🐍 Python Template</h4>
    <p>Optimized for Python development workflows</p>
    <code>ai-auditor init --template python</code>
  </div>

  <div class="template-item">
    <h4>🟢 Node.js Template</h4>
    <p>Configured for JavaScript/TypeScript projects</p>
    <code>ai-auditor init --template nodejs</code>
  </div>

  <div class="template-item">
    <h4>🦀 Rust Template</h4>
    <p>Tailored for Rust development environments</p>
    <code>ai-auditor init --template rust</code>
  </div>

  <div class="template-item">
    <h4>🔒 Security Template</h4>
    <p>Enhanced security rules for production environments</p>
    <code>ai-auditor init --template security</code>
  </div>

  <div class="template-item">
    <h4>🎯 General Template</h4>
    <p>Universal configuration for any project type</p>
    <code>ai-auditor init --template general</code>
  </div>

  <div class="template-item">
    <h4>✏️ Custom Template</h4>
    <p>Create your own template configurations</p>
    <a href="/configuration/templates/#custom-templates">Learn More</a>
  </div>
</div>

## 🔗 Git Hooks Integration

Configure automatic command validation with git hooks:

```yaml
# Git hooks configuration
git:
  hooks_enabled: true
  auto_setup: true
  backup_existing: true

  hooks:
    pre_commit:
      enabled: true
      validate_commands: true
      check_commit_msg: false

    pre_push:
      enabled: false
      validate_branch: true

    commit_msg:
      enabled: false
      validate_format: true
```

[Learn more about Git Hooks →](/configuration/git-hooks/)

## 🚀 Quick Configuration Examples

### Basic Python Project Setup

```bash
# Initialize with Python template
ai-auditor init --template python

# Customize security level
ai-auditor config set security.strict_mode true
ai-auditor config set security.thresholds.medium "warn"
```

### High-Security Environment

```bash
# Initialize with security template
ai-auditor init --template security --security-level strict

# Enable all security features
ai-auditor config set security.quarantine_dangerous true
ai-auditor config set security.thresholds.low "warn"
ai-auditor config set git.hooks.pre_push true
```

### Development Environment

```bash
# Initialize with relaxed settings
ai-auditor init --template general

# Configure for development
ai-auditor config set security.strict_mode false
ai-auditor config set logging.level "DEBUG"
ai-auditor config set performance.cache_enabled false
```

## 🛠️ Configuration Management

### View Current Configuration

```bash
# View all configuration
ai-auditor config show

# View specific section
ai-auditor config show security

# View specific setting
ai-auditor config get security.strict_mode
```

### Update Configuration

```bash
# Set individual values
ai-auditor config set ai.model "gpt-4-turbo"
ai-auditor config set security.max_command_length 2000

# Enable/disable features
ai-auditor config set git.hooks_enabled true
ai-auditor config set logging.level "WARNING"
```

### Reset Configuration

```bash
# Reset to defaults
ai-auditor config reset

# Reset specific section
ai-auditor config reset security

# Reset to template
ai-auditor config reset --template python
```

## 🔄 Environment-Specific Configuration

Manage different configurations for different environments:

```yaml
# Development environment
environment: development
ai:
  model: "gpt-3.5-turbo"  # Faster/cheaper model
  timeout: 10

security:
  strict_mode: false      # Relaxed validation
  thresholds:
    critical: "warn"      # Don't block in dev

logging:
  level: "DEBUG"          # Verbose logging
```

```yaml
# Production environment
environment: production
ai:
  model: "gpt-4o"         # Best model
  timeout: 30

security:
  strict_mode: true       # Strict validation
  thresholds:
    critical: "block"     # Block dangerous commands

logging:
  level: "WARNING"        # Minimal logging
```

Switch environments:

```bash
ai-auditor config env development
ai-auditor config env production
```

## 📊 Configuration Validation

Validate your configuration:

```bash
# Check configuration syntax
ai-auditor config validate

# Test configuration with sample commands
ai-auditor config test

# Show configuration summary
ai-auditor config summary
```

## 🔧 Advanced Configuration Topics

<div class="advanced-topics">
  <div class="topic-item">
    <h4>🔌 Plugin System</h4>
    <p>Extend functionality with custom plugins</p>
    <a href="/configuration/plugins/">Configure Plugins</a>
  </div>

  <div class="topic-item">
    <h4>🌐 Network Configuration</h4>
    <p>Configure proxies, timeouts, and API endpoints</p>
    <a href="/configuration/network/">Network Settings</a>
  </div>

  <div class="topic-item">
    <h4>📊 Monitoring & Metrics</h4>
    <p>Configure monitoring and performance metrics</p>
    <a href="/configuration/monitoring/">Setup Monitoring</a>
  </div>

  <div class="topic-item">
    <h4>🔐 Security Hardening</h4>
    <p>Advanced security configuration and hardening</p>
    <a href="/configuration/security-hardening/">Security Guide</a>
  </div>
</div>

## 📚 Next Steps

Once you've configured AI Command Auditor:

- 🎯 [Try the Tutorial](/examples/tutorial/) - Learn with hands-on examples
- 🔌 [Explore CLI Commands](/api/cli/) - Master the command-line interface
- 💡 [Browse Examples](/examples/) - See real-world configurations
- ❓ [Get Support](/support/) - Find help and community resources

<style>
.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.config-item {
  padding: 1.5rem;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  text-align: center;
  background: #f8f9fa;
}

.config-item h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.template-item {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
  background: #fafbfc;
}

.template-item h4 {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.template-item p {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.template-item code {
  font-size: 0.8rem;
  display: block;
  margin-top: 0.5rem;
}

.advanced-topics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.topic-item {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}

.topic-item h4 {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.topic-item p {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .config-grid,
  .template-grid {
    grid-template-columns: 1fr;
  }

  .advanced-topics {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .advanced-topics {
    grid-template-columns: 1fr;
  }
}
</style>
