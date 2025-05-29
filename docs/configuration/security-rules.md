---
layout: single
title: "Security Rules Configuration"
description: "Configure security rules and validation patterns"
toc: true
toc_label: "Security Rules"
toc_icon: "shield-alt"
sidebar:
  nav: "docs"
---

# 🛡️ Security Rules Configuration

Security rules are the foundation of AI Command Auditor's validation system. They define patterns, severity levels, and actions for different types of potentially dangerous commands.

## 📋 Overview

Security rules work in combination with AI analysis to provide comprehensive command validation:

- **Pattern Matching**: Regular expressions and string patterns to detect dangerous commands
- **Severity Levels**: Critical, high, medium, low severity classification
- **Actions**: Block, warn, log, or ignore based on severity thresholds
- **Context Awareness**: Rules can be context-specific (file types, environments, etc.)
- **Customization**: Easily add, modify, or disable rules for your needs

## 🏗️ Rule Structure

Security rules are defined in YAML files in the `.ai-auditor/config/rules/` directory:

```
.ai-auditor/config/rules/
├── security-rules.yml          # Main security rules
├── performance-rules.yml       # Performance-related rules
├── custom-rules.yml           # Your custom rules
└── environment-specific/
    ├── production.yml         # Production-only rules
    ├── development.yml        # Development rules
    └── ci-cd.yml             # CI/CD pipeline rules
```

## 📝 Rule Definition Format

### Basic Rule Structure

```yaml
# security-rules.yml
rules:
  rule_name:
    pattern: "regex_pattern_here"
    severity: "critical|high|medium|low"
    message: "Human-readable description"
    category: "rule_category"
    enabled: true
    environments: ["production", "staging"]  # Optional
    file_types: [".sh", ".py"]              # Optional
    contexts: ["git_hook", "cli"]           # Optional
```

### Complete Example

```yaml
# Example security rules configuration
version: "1.0"
metadata:
  description: "Security rules for AI Command Auditor"
  last_updated: "2024-01-15"

rules:
  # Destructive file operations
  dangerous_rm:
    pattern: "rm\\s+(-[rf]+|--recursive|--force).*(/|\\*|~)"
    severity: "critical"
    message: "Potentially destructive file deletion detected"
    category: "file_operations"
    enabled: true
    explanation: |
      This rule detects recursive or forced file deletion commands that could
      remove important system files or directories.
    examples:
      - "rm -rf /"
      - "rm -f ~/.bashrc"
      - "rm --recursive /usr"

  # Privilege escalation
  sudo_without_args:
    pattern: "sudo\\s*$"
    severity: "high"
    message: "Interactive sudo without specific command"
    category: "privilege_escalation"
    enabled: true

  # Network operations
  curl_pipe_sh:
    pattern: "curl.*\\|.*sh"
    severity: "critical"
    message: "Downloading and executing scripts is dangerous"
    category: "network_security"
    enabled: true

  # System modification
  modify_etc:
    pattern: "(echo|cat|tee).*>.*(/etc/|/usr/|/var/)"
    severity: "high"
    message: "Modifying system directories detected"
    category: "system_modification"
    enabled: true
    environments: ["production", "staging"]

  # Development tools misuse
  eval_usage:
    pattern: "eval\\s*\\("
    severity: "medium"
    message: "Use of eval() function detected"
    category: "code_execution"
    enabled: true
    file_types: [".py", ".js", ".php"]
```

## 🔧 Rule Categories

Security rules are organized into logical categories:

### File Operations

- **Dangerous deletions**: `rm -rf`, recursive removes
- **Permission changes**: `chmod 777`, excessive permissions
- **Ownership changes**: `chown`, `chgrp` on sensitive files

```yaml
file_operations:
  rm_recursive:
    pattern: "rm\\s+(-r|-rf|--recursive)"
    severity: "high"
    message: "Recursive file deletion"

  chmod_777:
    pattern: "chmod\\s+(777|a\\+rwx)"
    severity: "medium"
    message: "Overly permissive file permissions"

  chown_root:
    pattern: "chown\\s+root"
    severity: "high"
    message: "Changing file ownership to root"
```

### Network Security

- **Download and execute**: `curl | sh`, `wget | bash`
- **Suspicious downloads**: Downloads from suspicious domains
- **Unencrypted transfers**: HTTP instead of HTTPS

```yaml
network_security:
  download_execute:
    pattern: "(curl|wget).*\\|\\s*(sh|bash|python)"
    severity: "critical"
    message: "Downloading and executing code"

  http_download:
    pattern: "(curl|wget)\\s+http://"
    severity: "medium"
    message: "Unencrypted download detected"

  suspicious_domains:
    pattern: "(curl|wget).*\\.(tk|ml|ga|cf)/"
    severity: "high"
    message: "Download from suspicious domain"
```

### Privilege Escalation

- **Sudo misuse**: Interactive sudo, sudo without commands
- **SUID operations**: Setting SUID bits
- **User switching**: `su` without proper context

```yaml
privilege_escalation:
  interactive_sudo:
    pattern: "sudo\\s*$"
    severity: "high"
    message: "Interactive sudo session"

  suid_bit:
    pattern: "chmod\\s+[4567][0-7][0-7][0-7]"
    severity: "critical"
    message: "Setting SUID/SGID bits"

  sudo_all:
    pattern: "sudo\\s+.*\\*"
    severity: "high"
    message: "Sudo with wildcard patterns"
```

### Code Execution

- **Dynamic execution**: `eval`, `exec`, `system`
- **Code injection**: String interpolation in commands
- **Unsafe deserialization**: `pickle.loads`, `eval(input())`

```yaml
code_execution:
  python_eval:
    pattern: "eval\\s*\\("
    severity: "medium"
    message: "Python eval() usage"
    file_types: [".py"]

  shell_injection:
    pattern: "os\\.system\\s*\\("
    severity: "high"
    message: "Potential shell injection"
    file_types: [".py"]

  javascript_eval:
    pattern: "eval\\s*\\("
    severity: "medium"
    message: "JavaScript eval() usage"
    file_types: [".js", ".ts"]
```

### System Modification

- **Service management**: Starting/stopping critical services
- **System configuration**: Modifying `/etc` files
- **Package management**: Installing suspicious packages

```yaml
system_modification:
  service_stop:
    pattern: "(systemctl|service)\\s+(stop|disable)"
    severity: "medium"
    message: "Stopping system services"

  etc_modification:
    pattern: "(echo|cat|tee).*>.*(/etc/)"
    severity: "high"
    message: "Modifying system configuration"

  package_install:
    pattern: "(apt|yum|dnf)\\s+install"
    severity: "low"
    message: "Package installation"
    environments: ["production"]
```

## ⚙️ Severity Levels and Actions

### Severity Levels

| Severity | Description | Default Action | Use Cases |
|----------|-------------|----------------|-----------|
| **Critical** | Extremely dangerous commands that could cause system damage | Block | `rm -rf /`, `chmod 777 /etc` |
| **High** | Potentially dangerous commands requiring review | Warn | `sudo` usage, system modifications |
| **Medium** | Suspicious patterns that should be logged | Log | `eval()` usage, unencrypted downloads |
| **Low** | Information-only, tracking patterns | Ignore | Package installations, basic commands |

### Action Configuration

Configure how AI Command Auditor responds to different severity levels:

```yaml
# In auditor.yml
security:
  thresholds:
    critical: "block"    # Block command execution
    high: "warn"         # Show warning, allow execution
    medium: "log"        # Log only, no user interruption
    low: "ignore"        # No action taken

  # Additional options
  strict_mode: false     # Treat warnings as blocks
  quarantine_dangerous: true  # Move dangerous commands to quarantine
  allow_override: true   # Allow users to override warnings
```

## 🎯 Context-Specific Rules

Rules can be applied selectively based on context:

### Environment-Specific Rules

```yaml
# Only apply in production
production_only:
  package_changes:
    pattern: "(apt|yum|pip)\\s+(install|remove)"
    severity: "critical"
    message: "Package changes forbidden in production"
    environments: ["production"]

# Relaxed rules for development
development_relaxed:
  debug_commands:
    pattern: "(gdb|strace|ltrace)"
    severity: "low"
    message: "Debug tools usage"
    environments: ["development"]
```

### File Type-Specific Rules

```yaml
# Python-specific rules
python_security:
  pickle_usage:
    pattern: "pickle\\.loads?"
    severity: "high"
    message: "Unsafe deserialization detected"
    file_types: [".py"]

  input_eval:
    pattern: "eval\\s*\\(\\s*input"
    severity: "critical"
    message: "Evaluating user input is dangerous"
    file_types: [".py"]

# Shell script rules
shell_security:
  unquoted_variables:
    pattern: "\\$[A-Za-z_][A-Za-z0-9_]*[^\"']"
    severity: "medium"
    message: "Unquoted variable usage"
    file_types: [".sh", ".bash"]
```

### Context-Aware Rules

```yaml
# Git hook specific rules
git_hook_rules:
  blocking_operations:
    pattern: "(sleep|read|prompt)"
    severity: "high"
    message: "Blocking operations in git hooks"
    contexts: ["git_hook"]

# CI/CD pipeline rules
ci_cd_rules:
  secret_exposure:
    pattern: "(password|token|key)\\s*="
    severity: "critical"
    message: "Potential secret exposure in CI"
    contexts: ["ci_cd"]
```

## 🛠️ Custom Rules

Create your own security rules for specific needs:

### Adding Custom Rules

```yaml
# custom-rules.yml
custom_rules:
  company_specific:
    internal_tools:
      pattern: "company-internal-tool"
      severity: "medium"
      message: "Use approved tool alternatives"

    database_access:
      pattern: "mysql.*-p.*\\$"
      severity: "high"
      message: "Database password in command line"

    cloud_credentials:
      pattern: "aws\\s+configure\\s+set"
      severity: "medium"
      message: "Cloud credential configuration"
```

### Domain-Specific Rules

```yaml
# Data science rules
data_science:
  jupyter_root:
    pattern: "jupyter.*--allow-root"
    severity: "medium"
    message: "Running Jupyter as root"

  untrusted_packages:
    pattern: "pip\\s+install.*--trusted-host"
    severity: "high"
    message: "Installing from untrusted sources"

# Web development rules
web_development:
  npm_audit:
    pattern: "npm\\s+install.*--ignore-scripts"
    severity: "medium"
    message: "Ignoring npm security scripts"

  cors_wildcard:
    pattern: "Access-Control-Allow-Origin.*\\*"
    severity: "medium"
    message: "Wildcard CORS configuration"
```

## 🔄 Rule Management

### Enabling/Disabling Rules

```bash
# Disable specific rule
ai-auditor config set rules.dangerous_rm.enabled false

# Enable rule for specific environment
ai-auditor config set rules.package_install.environments '["production"]'

# Set rule severity
ai-auditor config set rules.curl_pipe_sh.severity "critical"
```

### Testing Rules

```bash
# Test rule against command
ai-auditor test-rule dangerous_rm "rm -rf /"

# Test all rules against command
ai-auditor check-command "sudo rm -rf /tmp" --show-rules

# Validate rule syntax
ai-auditor validate-rules
```

### Rule Performance

```bash
# Show rule performance statistics
ai-auditor rules stats

# Profile rule execution time
ai-auditor rules profile

# Show most triggered rules
ai-auditor rules top-triggered
```

## 📊 Rule Analytics

Monitor rule effectiveness:

```yaml
# Enable rule analytics
analytics:
  enabled: true
  track_matches: true
  performance_monitoring: true

reporting:
  rule_usage: true
  false_positive_tracking: true
  effectiveness_metrics: true
```

View analytics:

```bash
# Rule usage report
ai-auditor report rules-usage

# False positive analysis
ai-auditor report false-positives

# Rule effectiveness metrics
ai-auditor report rule-effectiveness
```

## 🚀 Best Practices

### Rule Design

1. **Be Specific**: Avoid overly broad patterns that cause false positives
2. **Test Thoroughly**: Test rules against real commands before deployment
3. **Document Well**: Include clear messages and explanations
4. **Use Categories**: Organize rules logically for easy management
5. **Consider Context**: Apply rules appropriately based on environment

### Performance Optimization

1. **Order Matters**: Put most common rules first
2. **Optimize Regex**: Use efficient regular expressions
3. **Cache Results**: Enable rule result caching
4. **Monitor Performance**: Regular performance analysis

### Team Collaboration

1. **Version Control**: Keep rule files in version control
2. **Code Review**: Review rule changes like code
3. **Documentation**: Maintain rule documentation
4. **Testing**: Include rule tests in CI/CD

## 📚 Examples and Templates

### Starter Rule Set

```yaml
# starter-rules.yml - Basic security rules
starter_rules:
  rm_recursive:
    pattern: "rm\\s+(-rf|--recursive)"
    severity: "high"
    message: "Recursive file deletion"

  sudo_usage:
    pattern: "sudo\\s+"
    severity: "medium"
    message: "Privilege escalation"

  download_execute:
    pattern: "(curl|wget).*\\|.*sh"
    severity: "critical"
    message: "Download and execute"
```

### Enterprise Rule Set

```yaml
# enterprise-rules.yml - Comprehensive enterprise rules
enterprise_rules:
  # ... (extensive rule set)
```

### Development Rule Set

```yaml
# development-rules.yml - Development-friendly rules
development_rules:
  # ... (relaxed rules for development)
```

## 🔗 Related Configuration

- [AI Prompts](/configuration/ai-prompts/) - Configure AI analysis prompts
- [Templates](/configuration/templates/) - Rule templates for different projects
- [Git Hooks](/configuration/git-hooks/) - Integrate rules with git workflows
- [Main Configuration](/configuration/) - Overall configuration options

## 📖 Next Steps

- 🎯 [Try Examples](/examples/) - See rules in action
- 🔧 [CLI Reference](/api/cli/) - Command-line rule management
- 🤝 [Contributing](/support/contributing/) - Contribute new rules
- 🆘 [Get Help](/support/) - Support and troubleshooting

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

.highlight {
  background-color: #f8f9fa;
  border-left: 4px solid #28a745;
  padding: 1rem;
  margin: 1rem 0;
}

.warning {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 1rem;
  margin: 1rem 0;
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
