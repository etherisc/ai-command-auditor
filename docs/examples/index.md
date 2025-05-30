---
layout: default
title: Examples & Tutorials
nav_order: 5
has_children: true
description: "Practical examples and step-by-step tutorials"
---

# 💡 Examples & Tutorials

Get hands-on experience with AI Command Auditor through practical examples and step-by-step tutorials.

[Start Tutorial]({{ site.baseurl }}/examples/tutorial){: .btn .btn-primary }

## 🎯 Getting Started Tutorial

### 🚀 Complete Beginner Tutorial

Learn everything from installation to advanced configuration in 30 minutes

- ✅ Installation and setup
- ✅ First command validation
- ✅ Configuration customization
- ✅ Git hooks integration
- ✅ Team workflow setup

[Start Tutorial]({{ site.baseurl }}/examples/tutorial){: .btn .btn-primary }

## 🎨 Project-Specific Examples

Choose your development environment and follow tailored examples:

### 🐍 Python Projects

Flask, Django, FastAPI, and general Python development

- Virtual environment validation
- Package management security
- Script execution safety
- CI/CD integration

### 🟢 Node.js Projects

React, Express, Nest.js, and JavaScript/TypeScript

- npm/yarn security validation
- Script execution checks
- Package.json integration
- Build process security

### 🦀 Rust Projects

Cargo, system-level programming, and Rust toolchain

- Cargo command validation
- System call security
- Cross-compilation safety
- Performance optimization

### 🐳 DevOps & Infrastructure

Docker, Kubernetes, Terraform, and automation

- Container security validation
- Infrastructure as Code checks
- Deployment pipeline safety
- Cloud command validation

### 🔒 Security-Focused

High-security environments and compliance

- Strict security policies
- Compliance validation
- Audit trail setup
- Zero-trust workflows

### 🏢 Enterprise Integration

Large teams, multiple projects, centralized management

- Centralized configuration
- Team policy management
- Monitoring and reporting
- Custom integrations

## 🔗 Integration Examples

### GitHub Actions

```yaml
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
        run: ai-auditor scan-repository
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ai-command-auditor
        name: AI Command Auditor
        entry: ai-auditor check-staged-commands
        language: system
```

### Makefile Integration

```makefile
# Makefile
validate-commands:
 ai-auditor validate-makefile $(MAKEFILE_LIST)

deploy: validate-commands
 ./deploy.sh
```

## 📖 Example Configurations

### Basic Security Rules

```yaml
# .ai-auditor/config/rules/security-rules.yml
rules:
  dangerous_commands:
    - pattern: "rm -rf /"
      severity: critical
      message: "Dangerous recursive delete detected"
    - pattern: "sudo.*"
      severity: medium
      message: "Sudo command requires review"
```

### Team Configuration

```yaml
# .ai-auditor/config/team-config.yml
team:
  policy_level: "strict"
  required_reviewers: 2
  blocked_commands:
    - "curl.*|.*sh"
    - "wget.*|.*sh"
  allowed_sudo_commands:
    - "sudo docker"
    - "sudo systemctl"
```

## 🚀 Quick Examples

### Basic Command Validation

```bash
# Check a single command
ai-auditor check-command "rm -rf /tmp/*"

# Validate a script
ai-auditor validate-script deploy.sh

# Scan entire repository
ai-auditor scan-repository --recursive
```

### Configuration Management

```bash
# Show current configuration
ai-auditor config show

# Update security settings
ai-auditor config set security.strict_mode true

# Load team configuration
ai-auditor config load team-config.yml
```

## 📚 Learn More

Ready to dive deeper? Check out our comprehensive documentation:

- [Installation Guide]({{ site.baseurl }}/installation/) - Get started quickly
- [Configuration Reference]({{ site.baseurl }}/configuration/) - Configure for your needs
- [API Reference]({{ site.baseurl }}/api/) - CLI and Python API docs
- [FAQ]({{ site.baseurl }}/faq/) - Get help and find answers
