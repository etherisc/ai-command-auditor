---
layout: single
title: "Installation"
description: "Install AI Command Auditor quickly and easily"
toc: true
toc_label: "Installation Methods"
toc_icon: "download"
sidebar:
  nav: "docs"
---

# 📥 Installation Guide

AI Command Auditor offers multiple installation methods to fit your development environment and preferences. Choose the method that works best for your use case.

## 🚀 Quick Start (Recommended)

The fastest way to get started is with our one-line installer:

```bash
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

This will:

- ✅ Detect your system and install dependencies
- ✅ Install the AI Command Auditor CLI
- ✅ Set up default configuration
- ✅ Configure git hooks (optional)
- ✅ Verify the installation

### Verify Installation

```bash
# Check version
ai-auditor --version

# Test with a simple command
ai-auditor check-command "echo hello world"

# View help
ai-auditor --help
```

## 📋 System Requirements

Before installing, ensure your system meets these requirements:

### Minimum Requirements

- **Operating System**: Linux, macOS, or Windows (WSL2)
- **Python**: 3.8 or higher
- **Memory**: 512MB RAM
- **Disk Space**: 100MB free space

### Recommended Requirements

- **Python**: 3.10 or higher
- **Memory**: 1GB RAM
- **Git**: For git hooks integration
- **Internet**: For AI API calls

### Supported Platforms

- ✅ Ubuntu 18.04+
- ✅ Debian 10+
- ✅ CentOS 7+
- ✅ macOS 10.15+
- ✅ Windows 10/11 (WSL2)

## 🛠️ Installation Methods

Choose the installation method that best fits your needs:

<div class="installation-grid">
  <div class="install-method">
    <h3>🚀 One-Line Installer</h3>
    <p><strong>Best for:</strong> Quick setup, production use</p>
    <p>Automatic installation with sensible defaults</p>
    <a href="/installation/methods/#one-line-installer" class="btn btn--primary">View Guide</a>
  </div>

  <div class="install-method">
    <h3>🐍 Python Package</h3>
    <p><strong>Best for:</strong> Python developers, custom environments</p>
    <p>Install via pip with full control</p>
    <a href="/installation/methods/#python-package" class="btn btn--primary">View Guide</a>
  </div>

  <div class="install-method">
    <h3>🐳 Devcontainer</h3>
    <p><strong>Best for:</strong> VS Code users, containerized development</p>
    <p>Automatic setup in development containers</p>
    <a href="/installation/methods/#devcontainer" class="btn btn--primary">View Guide</a>
  </div>

  <div class="install-method">
    <h3>⚙️ Manual Installation</h3>
    <p><strong>Best for:</strong> Advanced users, custom setups</p>
    <p>Step-by-step manual configuration</p>
    <a href="/installation/methods/#manual-installation" class="btn btn--primary">View Guide</a>
  </div>
</div>

## 🎯 Environment-Specific Guides

<div class="environment-grid">
  <div class="env-guide">
    <h4>🐧 Ubuntu/Debian</h4>
    <p>Installation on Ubuntu and Debian systems</p>
    <a href="/installation/environments/ubuntu/">Ubuntu Guide</a>
  </div>

  <div class="env-guide">
    <h4>🍎 macOS</h4>
    <p>Installation on macOS with Homebrew</p>
    <a href="/installation/environments/macos/">macOS Guide</a>
  </div>

  <div class="env-guide">
    <h4>🪟 Windows WSL2</h4>
    <p>Installation on Windows with WSL2</p>
    <a href="/installation/environments/windows/">Windows Guide</a>
  </div>

  <div class="env-guide">
    <h4>🐳 Docker</h4>
    <p>Installation in Docker containers</p>
    <a href="/installation/environments/docker/">Docker Guide</a>
  </div>
</div>

## ⚡ Quick Installation Examples

### For Python Projects

```bash
# Install with Python template
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --template python

# Or using pip
pip install ai-command-auditor[python]
```

### For Node.js Projects

```bash
# Install with Node.js template
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --template nodejs

# Add to package.json scripts
npm run audit-setup
```

### For DevOps/Security Teams

```bash
# Install with strict security settings
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --template security --security-level strict
```

## 🔧 Post-Installation Setup

After installation, you may want to:

1. **Initialize in your project**:

   ```bash
   cd your-project
   ai-auditor init
   ```

2. **Customize configuration**:

   ```bash
   # Edit main config
   nano .ai-auditor/config/auditor.yml

   # Edit security rules
   nano .ai-auditor/config/rules/security-rules.yml
   ```

3. **Set up git hooks**:

   ```bash
   ai-auditor setup-hooks
   ```

4. **Test the setup**:

   ```bash
   ai-auditor check-command "rm -rf /"
   ```

## ❗ Troubleshooting

Having installation issues? Here are common solutions:

### Permission Errors

```bash
# If you get permission errors, try:
sudo curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh

# Or install to user directory:
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --user-install
```

### Python Version Issues

```bash
# Check Python version
python3 --version

# If Python is too old, update it:
# Ubuntu/Debian:
sudo apt update && sudo apt install python3.10

# macOS:
brew install python@3.10
```

### Network Issues

```bash
# If download fails, try manual download:
wget https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh
chmod +x install.sh
./install.sh
```

## 📚 Next Steps

Once installed, check out these resources:

- 📖 [Configuration Guide](/configuration/) - Customize AI Command Auditor
- 🎯 [Getting Started Tutorial](/examples/tutorial/) - Learn the basics
- 🔌 [API Reference](/api/) - Explore CLI commands
- ❓ [FAQ](/support/faq/) - Common questions and answers

Need help? Visit our [support page](/support/) or [file an issue](https://github.com/etherisc/ai-command-auditor/issues).

<style>
.installation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.install-method {
  padding: 1.5rem;
  border: 1px solid #e1e1e1;
  border-radius: 8px;
  text-align: center;
  background: #f8f9fa;
}

.install-method h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.install-method p {
  margin-bottom: 0.5rem;
}

.environment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.env-guide {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}

.env-guide h4 {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.env-guide p {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .installation-grid {
    grid-template-columns: 1fr;
  }

  .environment-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .environment-grid {
    grid-template-columns: 1fr;
  }
}
</style>
