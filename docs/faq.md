---
layout: default
title: FAQ
nav_order: 6
description: "Frequently asked questions about AI Command Auditor"
---

# ❓ Frequently Asked Questions

Common questions and answers about AI Command Auditor.

## Installation & Setup

### Q: How do I install AI Command Auditor?

**A:** Use the one-line installer:

```bash
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

### Q: What are the system requirements?

**A:** AI Command Auditor works on:

- Linux (all major distributions)
- macOS (10.14+)
- Windows (via WSL2)
- Python 3.8+ or Node.js 16+

### Q: Can I install it without internet access?

**A:** Yes, download the installer and run it offline. Check our [Installation Guide]({{ site.baseurl }}/installation/) for details.

## Usage & Commands

### Q: How do I check if a command is safe?

**A:** Use the `check-command` command:

```bash
ai-auditor check-command "your command here"
```

### Q: How do I setup git hooks?

**A:** Run the setup command in your repository:

```bash
ai-auditor setup-hooks
```

### Q: Can I customize the security rules?

**A:** Yes! Edit `.ai-auditor/config/rules/security-rules.yml` or see our [Configuration Guide]({{ site.baseurl }}/configuration/).

## Configuration

### Q: Where are configuration files stored?

**A:** Configuration files are stored in:

- Project-specific: `.ai-auditor/config/`
- User-wide: `~/.ai-auditor/config/`
- System-wide: `/etc/ai-auditor/config/`

### Q: How do I enable strict security mode?

**A:** Use the config command:

```bash
ai-auditor config set security.strict_mode true
```

### Q: Can I use custom AI models?

**A:** Yes! Configure your AI provider in the config:

```bash
ai-auditor config set ai.model "your-model"
ai-auditor config set ai.api_key "your-key"
```

## Troubleshooting

### Q: AI Command Auditor is running slowly

**A:** Try these solutions:

- Enable caching: `ai-auditor config set performance.cache_enabled true`
- Reduce parallel requests: `ai-auditor config set performance.parallel_requests 1`
- Use a faster AI model: `ai-auditor config set ai.model "gpt-3.5-turbo"`

### Q: I'm getting false positives

**A:** Adjust sensitivity settings:

```bash
ai-auditor config set security.strict_mode false
ai-auditor config set security.thresholds.medium "warn"
```

### Q: Commands are being blocked that shouldn't be

**A:** Add exceptions to your security rules or whitelist specific commands.

## Integration

### Q: How do I integrate with GitHub Actions?

**A:** Add this to your workflow:

```yaml
- name: Install AI Command Auditor
  run: curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
- name: Validate Commands
  run: ai-auditor scan-repository
```

### Q: Can I use it with pre-commit hooks?

**A:** Yes! Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: ai-command-auditor
        name: AI Command Auditor
        entry: ai-auditor check-staged-commands
        language: system
```

### Q: Does it work with Docker?

**A:** Yes! See our [Examples]({{ site.baseurl }}/examples/) for Docker integration patterns.

## Team & Enterprise

### Q: How do I set up team-wide policies?

**A:** Create shared configuration files and use version control. See our [Configuration Guide]({{ site.baseurl }}/configuration/) for details.

### Q: Can I generate audit reports?

**A:** Yes! Use the reporting commands:

```bash
ai-auditor generate-report --format json
ai-auditor generate-report --format html
```

### Q: Is it suitable for enterprise use?

**A:** Absolutely! AI Command Auditor supports:

- Centralized configuration management
- Audit logging and compliance
- Team policy enforcement
- Custom integrations

## API & Development

### Q: Can I use AI Command Auditor programmatically?

**A:** Yes! Use the Python API:

```python
from ai_command_auditor import CommandAuditor

auditor = CommandAuditor()
result = auditor.analyze_command("your command")
```

### Q: How do I create custom validators?

**A:** See our [API Documentation]({{ site.baseurl }}/api/) for extension examples.

### Q: Can I contribute to the project?

**A:** Absolutely! Check our [Contributing Guide](https://github.com/etherisc/ai-command-auditor/blob/main/CONTRIBUTING.md).

## Security & Privacy

### Q: What data is sent to AI providers?

**A:** Only the command text and configuration context. No sensitive data like file contents or environment variables.

### Q: Can I use it offline?

**A:** Yes, with local AI models or by pre-caching responses.

### Q: Is it safe to use in production?

**A:** Yes! AI Command Auditor is designed for production use with proper security practices.

## Still Need Help?

- 📚 [Check our Documentation]({{ site.baseurl }}/installation/)
- 💬 [Join our Community](https://github.com/etherisc/ai-command-auditor/discussions)
- 🐛 [Report Issues](https://github.com/etherisc/ai-command-auditor/issues)

---

*Don't see your question here? [Ask the community](https://github.com/etherisc/ai-command-auditor/discussions) or [report an issue](https://github.com/etherisc/ai-command-auditor/issues).*
