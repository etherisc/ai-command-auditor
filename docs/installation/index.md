---
layout: default
title: Installation
nav_order: 2
has_children: true
description: "Install AI Command Auditor quickly and easily"
---

# 📥 Installation Guide
{: .fs-8 }

AI Command Auditor offers multiple installation methods to fit your development environment and preferences. Choose the method that works best for your use case.
{: .fs-6 .fw-300 }

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

| Method | Best For | Description |
|:-------|:---------|:------------|
| [One-Line Installer](/installation/methods#one-line-installer) | Quick setup, production use | Automatic installation with sensible defaults |
| [Python Package](/installation/methods#python-package) | Python developers, custom environments | Install via pip with full control |
| [Devcontainer](/installation/methods#devcontainer) | VS Code users, containerized development | Automatic setup in development containers |
| [Manual Installation](/installation/methods#manual-installation) | Advanced users, custom setups | Step-by-step manual configuration |

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

{: .note }
> **Permission Errors**: If you get permission errors, try running with `sudo` or check your user permissions.

{: .warning }
> **Python Version**: Make sure you have Python 3.8+ installed. Check with `python --version`.

{: .highlight }
> **Need Help?**: Visit our [Support](/support) section for more troubleshooting tips and community help.

---

[Next: Installation Methods](/installation/methods){: .btn .btn-primary }
[Skip to Configuration](/configuration){: .btn .btn-outline }

<style>
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
