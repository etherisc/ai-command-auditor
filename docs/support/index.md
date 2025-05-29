---
layout: single
title: "Support & Help"
description: "Get help, find answers, and connect with the community"
toc: true
toc_label: "Support Topics"
toc_icon: "question-circle"
sidebar:
  nav: "docs"
---

# 🆘 Support & Help

Need help with AI Command Auditor? You're in the right place! Find answers to common questions, troubleshooting guides, and ways to connect with our community.

## 🔍 Quick Help

<div class="help-grid">
  <div class="help-card">
    <h3>❓ FAQ</h3>
    <p>Frequently asked questions and quick answers</p>
    <a href="/support/faq/" class="btn btn--primary">View FAQ</a>
  </div>

  <div class="help-card">
    <h3>🔧 Troubleshooting</h3>
    <p>Common issues and step-by-step solutions</p>
    <a href="/support/troubleshooting/" class="btn btn--primary">Get Help</a>
  </div>

  <div class="help-card">
    <h3>👥 Community</h3>
    <p>Connect with other users and developers</p>
    <a href="/support/community/" class="btn btn--primary">Join Community</a>
  </div>

  <div class="help-card">
    <h3>🤝 Contributing</h3>
    <p>Help improve AI Command Auditor</p>
    <a href="/support/contributing/" class="btn btn--primary">Contribute</a>
  </div>
</div>

## 🚨 Common Issues

### Installation Problems

**Issue**: Installation script fails with permission errors

```bash
# Solution: Use sudo or install to user directory
sudo curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh

# Or install to user directory
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --user-install
```

**Issue**: Python version incompatibility

```bash
# Check Python version
python3 --version

# Update Python (Ubuntu/Debian)
sudo apt update && sudo apt install python3.10

# Update Python (macOS)
brew install python@3.10
```

**Issue**: Command not found after installation

```bash
# Add to PATH manually
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or reinstall with global flag
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --global
```

### Configuration Issues

**Issue**: AI API calls failing

```bash
# Check API key
echo $OPENAI_API_KEY

# Set API key if missing
export OPENAI_API_KEY="your-api-key-here"

# Test API connection
ai-auditor check-command "echo test" --debug
```

**Issue**: Git hooks not working

```bash
# Reinstall hooks
ai-auditor setup-hooks --force

# Check hook permissions
ls -la .git/hooks/pre-commit

# Make executable if needed
chmod +x .git/hooks/pre-commit
```

**Issue**: Configuration validation errors

```bash
# Validate configuration
ai-auditor config validate

# Reset to defaults
ai-auditor config reset

# Use a working template
ai-auditor config reset --template python
```

### Performance Issues

**Issue**: Slow command validation

```bash
# Enable caching
ai-auditor config set performance.cache_enabled true

# Reduce parallel requests
ai-auditor config set performance.parallel_requests 1

# Use faster AI model
ai-auditor config set ai.model "gpt-3.5-turbo"
```

**Issue**: High memory usage

```bash
# Clear cache
ai-auditor cache clear

# Disable verbose logging
ai-auditor config set logging.level "WARNING"

# Reduce batch size
ai-auditor config set performance.batch_size 5
```

## 💬 Frequently Asked Questions

### General Questions

**Q: Is AI Command Auditor free to use?**
A: Yes! AI Command Auditor is open source and free to use. However, you'll need an API key for the AI service (like OpenAI), which may have costs associated with usage.

**Q: What AI models are supported?**
A: We support OpenAI models (GPT-3.5, GPT-4), Anthropic Claude, and other OpenAI-compatible APIs. You can configure the model in the settings.

**Q: Can I use it offline?**
A: The core validation rules work offline, but AI-powered analysis requires internet connectivity for API calls.

**Q: Is my data sent to AI services?**
A: Only the commands you're validating are sent to the AI service for analysis. No other data from your system is transmitted.

### Installation Questions

**Q: Which operating systems are supported?**
A: Linux, macOS, and Windows (via WSL2) are officially supported. Most Unix-like systems should work.

**Q: Do I need admin/root privileges?**
A: No, you can install to your user directory. Admin privileges are only needed for system-wide installation.

**Q: Can I install without internet?**
A: The installer requires internet to download components. For offline environments, you'll need to manually transfer the installation files.

### Configuration Questions

**Q: How do I customize security rules?**
A: Edit `.ai-auditor/config/rules/security-rules.yml` or use `ai-auditor config set` commands. See the [Configuration Guide](/configuration/).

**Q: Can I disable certain validations?**
A: Yes, you can adjust severity thresholds, disable specific rules, or use different templates. See the configuration documentation.

**Q: How do I share configuration across a team?**
A: Commit the `.ai-auditor/config/` directory to your repository. Team members will inherit the shared configuration.

### Usage Questions

**Q: Can I validate entire scripts?**
A: Yes, use `ai-auditor scan-file script.sh` or `ai-auditor scan-directory scripts/` to validate multiple commands or files.

**Q: How accurate is the AI analysis?**
A: AI analysis is very good at detecting common dangerous patterns but isn't 100% perfect. Combine it with custom rules for best results.

**Q: Can I integrate with CI/CD?**
A: Absolutely! We provide examples for GitHub Actions, GitLab CI, Jenkins, and other platforms. See the [Examples](/examples/) section.

## 🛠️ Getting Help

### Before Asking for Help

1. **Check the documentation**: Look through our comprehensive guides
2. **Search existing issues**: Your question might already be answered
3. **Try troubleshooting**: Use our troubleshooting guides
4. **Enable debug mode**: Get more detailed error information

```bash
# Enable debug logging
ai-auditor config set logging.level "DEBUG"

# Run with verbose output
ai-auditor check-command "your command" --debug --verbose

# Check system information
ai-auditor system-info
```

### How to Report Issues

When reporting issues, please include:

1. **AI Command Auditor version**: `ai-auditor --version`
2. **Operating system**: `uname -a`
3. **Python version**: `python3 --version`
4. **Error message**: Full error output
5. **Steps to reproduce**: What you were trying to do
6. **Configuration**: Relevant config snippets (sanitized)

### Where to Get Help

<div class="support-channels">
  <div class="channel-item">
    <h4>🐛 Bug Reports</h4>
    <p>Found a bug? Report it on GitHub Issues</p>
    <a href="https://github.com/etherisc/ai-command-auditor/issues/new?template=bug_report.md" target="_blank">Report Bug</a>
  </div>

  <div class="channel-item">
    <h4>💡 Feature Requests</h4>
    <p>Have an idea for improvement?</p>
    <a href="https://github.com/etherisc/ai-command-auditor/issues/new?template=feature_request.md" target="_blank">Request Feature</a>
  </div>

  <div class="channel-item">
    <h4>💬 Discussions</h4>
    <p>General questions and community chat</p>
    <a href="https://github.com/etherisc/ai-command-auditor/discussions" target="_blank">Join Discussion</a>
  </div>

  <div class="channel-item">
    <h4>📧 Email Support</h4>
    <p>Direct support for enterprise users</p>
    <a href="mailto:support@etherisc.com">Contact Support</a>
  </div>
</div>

## 🤝 Community

### Join Our Community

- **GitHub Discussions**: Ask questions, share examples, get help
- **Discord Server**: Real-time chat with developers and users
- **Monthly Meetups**: Virtual meetups with demos and Q&A
- **Newsletter**: Updates, tips, and feature announcements

### Community Guidelines

1. **Be respectful**: Treat everyone with kindness and respect
2. **Stay on topic**: Keep discussions relevant to AI Command Auditor
3. **Help others**: Share your knowledge and experience
4. **Search first**: Check if your question has been asked before
5. **Provide context**: Include relevant details when asking questions

### Contributing to the Community

- **Answer questions**: Help other users in discussions
- **Share examples**: Contribute usage examples and tutorials
- **Write documentation**: Improve our guides and documentation
- **Report bugs**: Help us improve by reporting issues
- **Spread the word**: Tell others about AI Command Auditor

## 📚 Additional Resources

### Documentation

- 📖 [Complete Documentation](/docs/) - Full documentation
- 🚀 [Getting Started](/installation/) - Installation and quick start
- ⚙️ [Configuration Guide](/configuration/) - Detailed configuration
- 🔌 [API Reference](/api/) - CLI and Python API
- 💡 [Examples](/examples/) - Practical examples and tutorials

### External Resources

- **GitHub Repository**: Source code and issues
- **Release Notes**: What's new in each version
- **Roadmap**: Planned features and improvements
- **Security Policy**: How we handle security issues
- **License**: MIT License details

### Training and Tutorials

- **Video Tutorials**: Step-by-step video guides (coming soon)
- **Webinars**: Live training sessions (monthly)
- **Workshop Materials**: Hands-on workshop content
- **Certification**: AI Command Auditor certification program (planned)

## 🔐 Security and Privacy

### Security Issues

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email us at <security@etherisc.com>
3. Include details about the vulnerability
4. Allow time for us to address the issue

### Privacy Policy

- We don't collect personal data from the tool
- Commands sent to AI services are processed according to their privacy policies
- Local configuration and logs stay on your system
- See our full [Privacy Policy](https://etherisc.com/privacy) for details

## 📞 Enterprise Support

Need enterprise-level support? We offer:

- **Priority Support**: Faster response times
- **Custom Integration**: Help with complex setups
- **Training**: Team training and workshops
- **SLA Agreements**: Service level guarantees
- **Custom Development**: Feature development for your needs

Contact us at <enterprise@etherisc.com> for more information.

## ⭐ Show Your Support

Love AI Command Auditor? Here's how you can support the project:

- ⭐ **Star the project** on GitHub
- 🐛 **Report bugs** and issues
- 💡 **Suggest features** and improvements
- 📖 **Improve documentation**
- 🗣️ **Spread the word** to other developers
- 💰 **Sponsor the project** (GitHub Sponsors)

<div class="support-cta">
  <h3>Ready to Get Help?</h3>
  <p>Choose the best option for your needs:</p>
  <div class="cta-buttons">
    <a href="/support/faq/" class="btn btn--primary">Check FAQ</a>
    <a href="/support/troubleshooting/" class="btn btn--secondary">Troubleshoot</a>
    <a href="https://github.com/etherisc/ai-command-auditor/discussions" class="btn btn--outline" target="_blank">Ask Community</a>
  </div>
</div>

<style>
.help-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.help-card {
  padding: 1.5rem;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  text-align: center;
  background: #f8f9fa;
}

.help-card h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.support-channels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.channel-item {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
  background: #fafbfc;
}

.channel-item h4 {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.channel-item p {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.support-cta {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  margin: 3rem 0;
}

.support-cta h3 {
  color: white;
  margin-bottom: 1rem;
}

.cta-buttons {
  margin-top: 1rem;
}

.cta-buttons .btn {
  margin: 0.25rem;
}

@media (max-width: 768px) {
  .help-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .support-channels {
    grid-template-columns: 1fr;
  }

  .cta-buttons .btn {
    display: block;
    margin: 0.5rem auto;
    max-width: 200px;
  }
}

@media (max-width: 480px) {
  .help-grid {
    grid-template-columns: 1fr;
  }
}
</style>
