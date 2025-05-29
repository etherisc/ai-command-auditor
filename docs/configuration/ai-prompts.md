---
layout: single
title: "AI Prompts Configuration"
description: "Configure and customize AI analysis prompts"
toc: true
toc_label: "AI Prompts"
toc_icon: "brain"
sidebar:
  nav: "docs"
---

# 🧠 AI Prompts Configuration

AI prompts control how the AI analyzes commands, providing context, instructions, and guidelines for intelligent command validation. Customizing prompts allows you to tailor AI behavior for your specific domain, security requirements, and use cases.

## 📋 Overview

AI prompts work alongside security rules to provide comprehensive command analysis:

- **Context Setting**: Provide domain-specific context for analysis
- **Instruction Clarity**: Clear guidelines for what to look for
- **Output Formatting**: Structured responses for consistent processing
- **Domain Expertise**: Specialized knowledge for different fields
- **Customization**: Adapt AI behavior to your specific needs

## 🏗️ Prompt Structure

AI prompts are organized in the `.ai-auditor/config/prompts/` directory:

```
.ai-auditor/config/prompts/
├── analysis-prompt.yml         # General command analysis
├── security-prompt.yml         # Security-focused analysis
├── performance-prompt.yml      # Performance analysis
├── custom-prompts.yml         # Your custom prompts
└── domain-specific/
    ├── python-prompt.yml      # Python development
    ├── devops-prompt.yml      # DevOps and infrastructure
    ├── web-dev-prompt.yml     # Web development
    └── data-science-prompt.yml # Data science workflows
```

## 📝 Prompt Configuration Format

### Basic Prompt Structure

```yaml
# analysis-prompt.yml
version: "1.0"
metadata:
  name: "General Command Analysis"
  description: "General purpose command analysis prompt"
  model_compatibility: ["gpt-4", "gpt-3.5-turbo", "claude-3"]

prompts:
  primary:
    system_message: |
      You are an expert security analyst specializing in command-line security.
      Analyze commands for potential security risks, performance issues, and best practices.

    user_template: |
      Please analyze this command for security and safety:

      Command: {command}
      Context: {context}
      Environment: {environment}

      Provide analysis in this format:
      - Risk Level: [low/medium/high/critical]
      - Safety Score: [0-100]
      - Issues Found: [list of specific issues]
      - Recommendations: [specific actionable advice]
      - Explanation: [detailed reasoning]

    examples:
      - command: "rm -rf /"
        expected_response: |
          Risk Level: critical
          Safety Score: 0
          Issues Found: Destructive command that would delete entire filesystem
          Recommendations: Never run this command; use specific file paths
          Explanation: This command recursively deletes all files starting from root
```

### Advanced Prompt Configuration

```yaml
# security-prompt.yml
version: "1.0"
metadata:
  name: "Security-Focused Analysis"
  description: "Enhanced security analysis with threat modeling"
  tags: ["security", "threat-analysis", "compliance"]

configuration:
  model_settings:
    temperature: 0.1        # Low creativity for consistent security analysis
    max_tokens: 1000       # Detailed responses
    top_p: 0.9            # Focus on high-probability tokens

  analysis_depth: "comprehensive"
  focus_areas:
    - "privilege_escalation"
    - "data_exfiltration"
    - "system_modification"
    - "network_security"
    - "code_injection"

prompts:
  primary:
    system_message: |
      You are a cybersecurity expert with deep knowledge of:
      - Common attack vectors and exploitation techniques
      - Security best practices and compliance requirements
      - System administration and DevSecOps
      - Threat modeling and risk assessment

      Analyze commands with extreme attention to security implications.
      Consider both obvious and subtle security risks.

    user_template: |
      SECURITY ANALYSIS REQUEST
      ========================

      Command: {command}
      User Context: {user_role}
      Environment: {environment}
      System Info: {system_info}
      Previous Commands: {command_history}

      REQUIRED ANALYSIS:
      1. Threat Assessment
         - Immediate risks
         - Potential attack vectors
         - Privilege implications

      2. Security Violations
         - Policy violations
         - Compliance issues
         - Best practice deviations

      3. Risk Mitigation
         - Safer alternatives
         - Required precautions
         - Monitoring recommendations

      FORMAT RESPONSE AS JSON:
      {
        "threat_level": "low|medium|high|critical",
        "confidence": 0-100,
        "immediate_risks": ["list of immediate threats"],
        "attack_vectors": ["potential exploitation methods"],
        "policy_violations": ["security policy violations"],
        "mitigation_strategies": ["specific countermeasures"],
        "safer_alternatives": ["alternative commands"],
        "monitoring_required": ["what to monitor"],
        "explanation": "detailed technical analysis"
      }

    fallback_prompt: |
      Analyze this command for security risks: {command}
      Provide risk level and explanation.
```

## 🎯 Prompt Types and Use Cases

### Analysis Prompts

General command analysis for everyday use:

```yaml
# analysis-prompt.yml
general_analysis:
  focus: "balanced analysis of security, performance, and best practices"
  system_message: |
    You are an experienced systems administrator and security professional.
    Analyze commands for potential issues while considering practical usage.

  template: |
    Command to analyze: {command}

    Please evaluate:
    1. Security implications
    2. Performance impact
    3. Best practice compliance
    4. Alternative approaches

    Provide clear, actionable feedback.
```

### Security Prompts

Enhanced security analysis for high-security environments:

```yaml
# security-prompt.yml
security_analysis:
  focus: "comprehensive security threat assessment"
  system_message: |
    You are a security analyst in a high-security environment.
    Every command must be scrutinized for potential security implications.
    Consider advanced threats, insider risks, and compliance requirements.

  template: |
    SECURITY REVIEW REQUIRED
    Command: {command}
    Classification Level: {security_level}

    Assess for:
    - Advanced persistent threats
    - Insider threat indicators
    - Compliance violations
    - Data protection risks
    - Supply chain security
```

### Performance Prompts

Performance and efficiency analysis:

```yaml
# performance-prompt.yml
performance_analysis:
  focus: "command efficiency and system performance impact"
  system_message: |
    You are a performance engineering expert.
    Analyze commands for efficiency, resource usage, and optimization opportunities.

  template: |
    Performance Review: {command}

    Analyze:
    1. Resource consumption (CPU, memory, I/O)
    2. Execution efficiency
    3. Scalability implications
    4. Optimization opportunities
    5. Alternative implementations
```

## 🔧 Domain-Specific Prompts

### Python Development

```yaml
# python-prompt.yml
python_analysis:
  metadata:
    domain: "python_development"
    expertise: ["python", "pip", "virtual_environments", "security"]

  system_message: |
    You are a Python security expert with deep knowledge of:
    - Python package ecosystem and PyPI security
    - Virtual environment best practices
    - Common Python security vulnerabilities
    - Python development workflows and tooling

  template: |
    Python Command Analysis: {command}
    Project Context: {project_type}

    Evaluate for Python-specific concerns:
    - Package security and authenticity
    - Virtual environment isolation
    - Dependency management risks
    - Python execution safety
    - Development workflow security

    Consider Python-specific threats:
    - Malicious packages
    - Dependency confusion
    - Code injection via imports
    - Pickle/deserialization risks
```

### DevOps and Infrastructure

```yaml
# devops-prompt.yml
devops_analysis:
  metadata:
    domain: "devops_infrastructure"
    expertise: ["docker", "kubernetes", "ci_cd", "infrastructure"]

  system_message: |
    You are a DevOps security specialist with expertise in:
    - Container security and Docker best practices
    - Infrastructure as Code security
    - CI/CD pipeline security
    - Cloud security and compliance
    - Kubernetes security

  template: |
    Infrastructure Command Review: {command}
    Environment: {infrastructure_env}
    Pipeline Stage: {ci_cd_stage}

    Assess for DevOps security:
    - Container security implications
    - Infrastructure drift risks
    - CI/CD security boundaries
    - Cloud permission escalation
    - Supply chain integrity

    Consider infrastructure threats:
    - Container escapes
    - Privilege escalation
    - Secret exposure
    - Network security
```

### Web Development

```yaml
# web-dev-prompt.yml
web_development_analysis:
  metadata:
    domain: "web_development"
    expertise: ["npm", "node", "web_security", "frontend", "backend"]

  system_message: |
    You are a web application security expert with knowledge of:
    - Frontend and backend security best practices
    - npm ecosystem security
    - Web application vulnerabilities
    - API security and authentication
    - Modern web development frameworks

  template: |
    Web Development Command: {command}
    Tech Stack: {web_stack}

    Review for web-specific security:
    - npm package security
    - Frontend build security
    - API endpoint exposure
    - Authentication/authorization
    - Cross-site security

    Web security considerations:
    - XSS and injection risks
    - CSRF vulnerabilities
    - Dependency vulnerabilities
    - Build process security
```

### Data Science

```yaml
# data-science-prompt.yml
data_science_analysis:
  metadata:
    domain: "data_science"
    expertise: ["jupyter", "pandas", "machine_learning", "data_privacy"]

  system_message: |
    You are a data science security specialist with expertise in:
    - Jupyter notebook security
    - Data privacy and protection
    - Machine learning pipeline security
    - Statistical analysis security
    - Research data handling

  template: |
    Data Science Command: {command}
    Data Sensitivity: {data_classification}

    Evaluate for data science risks:
    - Data privacy violations
    - Jupyter security issues
    - Package authenticity
    - Model security
    - Research reproducibility

    Data science threats:
    - Data exfiltration
    - Model poisoning
    - Notebook execution risks
    - Dependency vulnerabilities
```

## 🛠️ Custom Prompt Development

### Creating Custom Prompts

```yaml
# custom-prompts.yml
company_specific:
  metadata:
    name: "Company XYZ Security Analysis"
    version: "2.1"
    compliance: ["SOX", "GDPR", "HIPAA"]

  system_message: |
    You are a security analyst for Company XYZ with knowledge of:
    - Company-specific security policies
    - Industry compliance requirements
    - Internal tool usage guidelines
    - Approved software and procedures

  template: |
    Company Security Review: {command}
    Employee Role: {user_role}
    Department: {department}
    Compliance Context: {compliance_requirements}

    Check against company policies:
    - Approved software usage
    - Data handling procedures
    - Access control requirements
    - Audit trail compliance

    Company-specific considerations:
    - Internal tool restrictions
    - Data classification rules
    - Vendor approval status
    - Incident response procedures
```

### Prompt Variables and Context

Available variables for prompt templates:

| Variable | Description | Example |
|----------|-------------|---------|
| `{command}` | The command being analyzed | `rm -rf temp/` |
| `{context}` | Additional context information | Project directory, git status |
| `{environment}` | Runtime environment | development, staging, production |
| `{user_role}` | User's role or permissions | developer, admin, guest |
| `{project_type}` | Type of project | python, nodejs, rust |
| `{security_level}` | Required security level | basic, standard, strict |
| `{compliance_requirements}` | Applicable compliance standards | GDPR, HIPAA, SOX |
| `{command_history}` | Previous commands (optional) | Last 5 commands |
| `{system_info}` | System information | OS, architecture |
| `{file_context}` | File being operated on | File type, permissions |

## ⚙️ Prompt Configuration Management

### Selecting Active Prompts

```yaml
# In auditor.yml
ai:
  prompts:
    primary: "security-prompt"      # Main prompt to use
    fallback: "analysis-prompt"     # Backup if primary fails
    domain_specific: true           # Enable domain-specific prompts

  prompt_selection:
    auto_detect: true               # Auto-select based on context
    user_override: true             # Allow user to specify prompt

  context_mapping:
    python_files: "python-prompt"
    shell_scripts: "security-prompt"
    ci_cd: "devops-prompt"
    default: "analysis-prompt"
```

### Dynamic Prompt Selection

```bash
# Use specific prompt for command
ai-auditor check-command "pip install package" --prompt python-analysis

# Set default prompt for session
ai-auditor config set ai.prompts.primary "security-prompt"

# List available prompts
ai-auditor prompts list

# Validate prompt configuration
ai-auditor prompts validate
```

## 🎨 Prompt Engineering Best Practices

### Writing Effective Prompts

1. **Be Specific**: Clear, unambiguous instructions
2. **Provide Context**: Include relevant background information
3. **Use Examples**: Show expected input/output patterns
4. **Structure Output**: Request consistent, parseable responses
5. **Consider Edge Cases**: Handle unusual or malformed commands

### Prompt Optimization

```yaml
# Example of well-structured prompt
optimized_prompt:
  system_message: |
    ROLE: You are a cybersecurity expert and systems administrator

    EXPERTISE:
    - Command-line security analysis
    - System administration best practices
    - Threat detection and assessment

    GUIDELINES:
    - Analyze commands for security risks
    - Provide specific, actionable recommendations
    - Consider context and environment
    - Be concise but thorough

  template: |
    TASK: Analyze the following command for security implications

    COMMAND: {command}
    CONTEXT: {context}

    REQUIRED OUTPUT:
    1. Risk Level: [critical/high/medium/low]
    2. Primary Concerns: [list top 3 issues]
    3. Recommendations: [specific actions to take]
    4. Explanation: [brief technical reasoning]

    CONSTRAINTS:
    - Response must be under 500 words
    - Focus on actionable insights
    - Use clear, technical language
```

### Testing and Validation

```bash
# Test prompt with sample commands
ai-auditor test-prompt security-prompt "rm -rf /"

# Compare prompt responses
ai-auditor compare-prompts analysis-prompt security-prompt "sudo command"

# Analyze prompt performance
ai-auditor prompt-metrics security-prompt
```

## 📊 Prompt Performance and Analytics

### Monitoring Prompt Effectiveness

```yaml
# Enable prompt analytics
analytics:
  prompt_performance: true
  response_quality: true
  accuracy_tracking: true

metrics:
  track_accuracy: true
  false_positive_rate: true
  response_time: true
  user_satisfaction: true
```

### Prompt A/B Testing

```yaml
# A/B test configuration
ab_testing:
  enabled: true
  tests:
    security_analysis:
      prompt_a: "security-prompt-v1"
      prompt_b: "security-prompt-v2"
      split_ratio: 50
      metrics: ["accuracy", "false_positives", "response_time"]
```

## 🔄 Prompt Versioning and Management

### Version Control

```yaml
# Prompt versioning
version_control:
  current_version: "2.1"
  previous_versions:
    - "2.0": "security-prompt-v2.0.yml"
    - "1.5": "security-prompt-v1.5.yml"

  changelog:
    "2.1":
      - "Improved threat detection accuracy"
      - "Added compliance context"
      - "Optimized for GPT-4"
    "2.0":
      - "Major rewrite for better structure"
      - "Added domain-specific analysis"
```

### Prompt Deployment

```bash
# Deploy new prompt version
ai-auditor prompts deploy security-prompt-v2.1.yml

# Rollback to previous version
ai-auditor prompts rollback security-prompt 2.0

# Compare prompt versions
ai-auditor prompts diff security-prompt-v2.0 security-prompt-v2.1
```

## 🔗 Integration with Security Rules

### Combining Prompts and Rules

```yaml
# Coordinated analysis configuration
analysis_strategy:
  rule_first: true              # Run rules before AI analysis
  ai_context_from_rules: true   # Provide rule results to AI
  ai_override_rules: false      # AI cannot override rule blocks

  escalation:
    rule_uncertainty: "ask_ai"  # Use AI when rules are uncertain
    ai_disagreement: "warn"     # Warn when AI disagrees with rules
```

### Rule-Informed Prompts

```yaml
# Prompt that considers rule results
rule_informed_prompt:
  template: |
    Command: {command}
    Rule Analysis Results: {rule_results}

    The automated rules have identified: {triggered_rules}

    Please provide additional analysis considering:
    1. Are the rule triggers accurate?
    2. Are there risks the rules missed?
    3. What additional context is relevant?
    4. How would you refine the analysis?
```

## 📚 Example Prompt Library

### Quick Start Prompts

```yaml
# Basic security prompt
basic_security:
  template: "Analyze this command for security risks: {command}"

# Development-friendly prompt
dev_friendly:
  template: |
    Command: {command}

    Quick security check - any major concerns?
    Keep it brief and practical for development workflow.

# Strict compliance prompt
strict_compliance:
  template: |
    COMPLIANCE ANALYSIS: {command}
    Standards: {compliance_requirements}

    Full security and compliance review required.
    Document all findings and recommendations.
```

## 🔧 Troubleshooting Prompts

### Common Issues

**Inconsistent Responses**:

```yaml
# Solution: Add more structure and examples
structured_prompt:
  template: |
    Command: {command}

    Respond in exactly this format:
    RISK: [critical/high/medium/low]
    ISSUES: [specific problems found]
    ACTIONS: [what to do about it]
```

**Too Verbose**:

```yaml
# Solution: Add word limits and constraints
concise_prompt:
  template: |
    Command: {command}

    Brief analysis (under 100 words):
    - Risk level and main concern
    - One specific recommendation
```

**Missing Context**:

```yaml
# Solution: Provide more context variables
contextual_prompt:
  template: |
    Analyzing: {command}
    Project: {project_type}
    Environment: {environment}
    User: {user_role}

    Consider all context factors in analysis.
```

## 📖 Next Steps

- 🎯 [See Prompts in Action](/examples/) - Practical examples
- 🛡️ [Security Rules](/configuration/security-rules/) - Combine with rules
- 🎨 [Templates](/configuration/templates/) - Prompt templates
- 🔧 [CLI Reference](/api/cli/) - Command-line prompt management

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

.prompt-example {
  background-color: #f8f9fa;
  border-left: 4px solid #007bff;
  padding: 1rem;
  margin: 1rem 0;
  font-family: monospace;
}

.best-practice {
  background-color: #e8f5e8;
  border-left: 4px solid #28a745;
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
