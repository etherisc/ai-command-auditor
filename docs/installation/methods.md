---
layout: default
title: Installation Methods
parent: Installation
nav_order: 1
description: "Detailed installation methods for AI Command Auditor"
---

# Installation Methods

{: .fs-8 }

Choose the installation method that best fits your development environment and requirements.
{: .fs-6 .fw-300 }

## 🚀 One-Line Installer

**Best for**: Quick setup, production use, most users

The one-line installer automatically detects your system and installs AI Command Auditor with sensible defaults.

```bash
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

### What it does

- Detects your operating system and architecture
- Installs Python dependencies if needed
- Downloads and installs the AI Command Auditor CLI
- Sets up default configuration files
- Optionally configures git hooks
- Verifies the installation

### Options

```bash
# Install with specific template
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --template python

# Install to user directory (no sudo required)
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --user-install

# Install with strict security settings
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --security-level strict

# Skip git hooks setup
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --no-git-hooks
```

---

## 🐍 Python Package

**Best for**: Python developers, custom environments, virtual environments

Install AI Command Auditor as a Python package using pip.

### Basic Installation

```bash
# Install from PyPI
pip install ai-command-auditor

# Or install with extras for specific use cases
pip install ai-command-auditor[python]     # Python development extras
pip install ai-command-auditor[nodejs]    # Node.js development extras
pip install ai-command-auditor[security]  # Enhanced security features
pip install ai-command-auditor[all]       # All extras
```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv ai-auditor-env
source ai-auditor-env/bin/activate  # On Windows: ai-auditor-env\Scripts\activate

# Install AI Command Auditor
pip install ai-command-auditor

# Initialize configuration
ai-auditor init
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/etherisc/ai-command-auditor.git
cd ai-command-auditor

# Install in development mode
pip install -e .

# Or with development dependencies
pip install -e .[dev]
```

---

## 🐳 Devcontainer

**Best for**: VS Code users, containerized development, team consistency

Add AI Command Auditor to your VS Code devcontainer for automatic setup.

### Method 1: Feature (Recommended)

Add to your `.devcontainer/devcontainer.json`:

```json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/etherisc/ai-command-auditor/devcontainer-feature:latest": {
      "version": "latest",
      "template": "python",
      "setupGitHooks": true
    }
  }
}
```

### Method 2: Manual Setup

Add to your `.devcontainer/devcontainer.json`:

```json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "postCreateCommand": "curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh",
  "customizations": {
    "vscode": {
      "extensions": [
        "etherisc.ai-command-auditor"
      ]
    }
  }
}
```

### Method 3: Dockerfile

Add to your `Dockerfile`:

```dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install AI Command Auditor
RUN curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh

# Copy configuration (optional)
COPY .ai-auditor/ /workspaces/.ai-auditor/
```

---

## ⚙️ Manual Installation

**Best for**: Advanced users, custom setups, air-gapped environments

Step-by-step manual installation for maximum control.

### Step 1: Install Dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip git curl

# CentOS/RHEL
sudo yum install python3 python3-pip git curl

# macOS
brew install python git curl

# Windows (WSL2)
sudo apt update && sudo apt install python3 python3-pip git curl
```

### Step 2: Download AI Command Auditor

```bash
# Download latest release
curl -L https://github.com/etherisc/ai-command-auditor/releases/latest/download/ai-command-auditor.tar.gz -o ai-command-auditor.tar.gz

# Extract
tar -xzf ai-command-auditor.tar.gz
cd ai-command-auditor
```

### Step 3: Install Python Package

```bash
# Install dependencies
pip install -r requirements.txt

# Install AI Command Auditor
pip install .

# Or install in development mode
pip install -e .
```

### Step 4: Configure

```bash
# Create configuration directory
mkdir -p ~/.ai-auditor/config

# Copy default configuration
cp config/defaults/* ~/.ai-auditor/config/

# Edit configuration
nano ~/.ai-auditor/config/auditor.yml
```

### Step 5: Setup Git Hooks (Optional)

```bash
# Navigate to your project
cd /path/to/your/project

# Setup git hooks
ai-auditor setup-hooks

# Or manually copy hooks
cp ~/.ai-auditor/hooks/* .git/hooks/
chmod +x .git/hooks/*
```

### Step 6: Verify Installation

```bash
# Check version
ai-auditor --version

# Test command validation
ai-auditor check-command "echo hello"

# Run self-test
ai-auditor self-test
```

---

## 🔧 Platform-Specific Instructions

### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install dependencies
sudo apt install python3 python3-pip python3-venv git curl

# Install AI Command Auditor
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

### CentOS/RHEL

```bash
# Install EPEL repository (if needed)
sudo yum install epel-release

# Install dependencies
sudo yum install python3 python3-pip git curl

# Install AI Command Auditor
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python git curl

# Install AI Command Auditor
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

### Windows (WSL2)

```bash
# Enable WSL2 and install Ubuntu
wsl --install

# Update and install dependencies
sudo apt update
sudo apt install python3 python3-pip git curl

# Install AI Command Auditor
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

---

## ✅ Verification

After installation, verify everything is working:

```bash
# Check version
ai-auditor --version

# Test basic functionality
ai-auditor check-command "ls -la"

# Test dangerous command detection
ai-auditor check-command "rm -rf /"

# Run comprehensive self-test
ai-auditor self-test --verbose
```

{: .note }
> **Success**: If all tests pass, you're ready to start using AI Command Auditor!

{: .warning }
> **Issues**: If you encounter problems, check our [FAQ]({{ site.baseurl }}/faq/) or [file an issue](https://github.com/etherisc/ai-command-auditor/issues).

---

[Next: Configuration](/configuration){: .btn .btn-primary }
[Back: Installation Overview](/installation){: .btn .btn-outline }
