---
layout: single
title: "Installation Methods"
description: "Detailed installation guides for all supported methods"
toc: true
toc_label: "Installation Methods"
toc_icon: "download"
sidebar:
  nav: "docs"
---

# 🛠️ Installation Methods

AI Command Auditor offers multiple installation methods to fit different environments and use cases. This guide provides detailed instructions for each installation method.

## 🚀 One-Line Installer (Recommended)

The quickest and most reliable way to install AI Command Auditor.

### Basic Installation

```bash
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

This will:

- ✅ Detect your system automatically
- ✅ Install Python dependencies
- ✅ Download and install AI Command Auditor
- ✅ Set up default configuration
- ✅ Configure PATH variables
- ✅ Verify the installation

### Installation Options

The installer supports various options for customization:

```bash
# Install with specific template
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --template python

# Install to user directory (no sudo required)
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --user-install

# Install with custom configuration directory
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --config-dir ~/.my-auditor

# Install with strict security settings
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --security-level strict

# Force reinstall over existing installation
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --force

# Dry run (show what would be done)
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --dry-run
```

### Complete Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `--template TYPE` | Use specific template (python, nodejs, rust, general, security) | `--template python` |
| `--config-dir PATH` | Custom configuration directory | `--config-dir ~/.auditor` |
| `--user-install` | Install to user directory (no sudo) | `--user-install` |
| `--global` | Install system-wide (requires sudo) | `--global` |
| `--security-level LEVEL` | Security level (basic, standard, strict) | `--security-level strict` |
| `--environment ENV` | Environment (development, staging, production) | `--environment production` |
| `--force` | Force reinstall over existing | `--force` |
| `--dry-run` | Show what would be done | `--dry-run` |
| `--quiet` | Minimal output | `--quiet` |
| `--verbose` | Detailed output | `--verbose` |

### Installation Verification

After installation, verify everything works:

```bash
# Check version
ai-auditor --version

# Test basic functionality
ai-auditor check-command "echo hello"

# Verify configuration
ai-auditor config show

# Test git hooks (if in a git repository)
ai-auditor setup-hooks --dry-run
```

## 🐍 Python Package Installation

For Python developers who prefer pip-based installation.

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Basic pip Installation

```bash
# Install from PyPI
pip install ai-command-auditor

# Install with optional dependencies
pip install ai-command-auditor[all]

# Install specific features
pip install ai-command-auditor[python]  # Python development features
pip install ai-command-auditor[nodejs] # Node.js development features
pip install ai-command-auditor[devops] # DevOps and security features
```

### Virtual Environment Setup

**Recommended approach for Python projects:**

```bash
# Create virtual environment
python3 -m venv ai-auditor-env

# Activate virtual environment
source ai-auditor-env/bin/activate  # Linux/macOS
# ai-auditor-env\Scripts\activate     # Windows

# Install AI Command Auditor
pip install ai-command-auditor

# Initialize configuration
ai-auditor init --template python
```

### Development Installation

For contributing or custom development:

```bash
# Clone repository
git clone https://github.com/etherisc/ai-command-auditor.git
cd ai-command-auditor

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

### Requirements File

Add to your project's `requirements.txt`:

```text
# requirements.txt
ai-command-auditor>=1.0.0

# Or with specific features
ai-command-auditor[python]>=1.0.0
```

Or for development (`requirements-dev.txt`):

```text
# requirements-dev.txt
ai-command-auditor[dev]>=1.0.0
pytest>=7.0.0
black>=22.0.0
isort>=5.0.0
```

## 🐳 Devcontainer Integration

Perfect for VS Code users and containerized development.

### Automatic Integration

Add AI Command Auditor to your devcontainer:

```json
// .devcontainer/devcontainer.json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",

  "features": {
    "ghcr.io/etherisc/devcontainer-features/ai-command-auditor:1": {
      "template": "python",
      "securityLevel": "standard"
    }
  },

  "postCreateCommand": "ai-auditor init --template python",

  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "etherisc.ai-command-auditor"
      ]
    }
  }
}
```

### Manual Devcontainer Setup

```json
// .devcontainer/devcontainer.json
{
  "name": "Python Development",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",

  "postCreateCommand": [
    "curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --template python",
    "ai-auditor setup-hooks"
  ],

  "mounts": [
    "source=${localWorkspaceFolder}/.ai-auditor,target=/workspaces/${localWorkspaceFolderBasename}/.ai-auditor,type=bind"
  ],

  "remoteEnv": {
    "OPENAI_API_KEY": "${localEnv:OPENAI_API_KEY}"
  }
}
```

### Dockerfile Integration

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install AI Command Auditor
RUN curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Initialize AI Command Auditor
RUN ai-auditor init --template python

# Copy application code
COPY . .

# Setup git hooks if .git directory exists
RUN if [ -d ".git" ]; then ai-auditor setup-hooks; fi

CMD ["python", "app.py"]
```

### Docker Compose Integration

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - .:/app
      - ~/.ai-auditor:/root/.ai-auditor  # Share configuration
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    command: |
      sh -c "
        ai-auditor init --template python &&
        ai-auditor setup-hooks &&
        python app.py
      "
```

## ⚙️ Manual Installation

For advanced users who need full control over the installation.

### Step 1: Download Source Code

```bash
# Download latest release
wget https://github.com/etherisc/ai-command-auditor/archive/refs/tags/v1.0.0.tar.gz

# Extract
tar -xzf v1.0.0.tar.gz
cd ai-command-auditor-1.0.0

# Or clone repository
git clone https://github.com/etherisc/ai-command-auditor.git
cd ai-command-auditor
```

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install optional dependencies (choose what you need)
pip install openai>=1.0.0        # For OpenAI models
pip install anthropic>=0.3.0     # For Claude models
pip install requests>=2.28.0     # For HTTP requests
pip install pyyaml>=6.0          # For YAML configuration
pip install click>=8.0.0         # For CLI interface
```

### Step 3: Install AI Command Auditor

```bash
# Install in development mode (for customization)
pip install -e .

# Or install normally
pip install .

# Verify installation
python -c "import ai_command_auditor; print('OK')"
```

### Step 4: Create Configuration

```bash
# Create configuration directory
mkdir -p ~/.ai-auditor/config

# Copy default configuration
cp -r config/* ~/.ai-auditor/config/

# Or use the CLI to initialize
python -m ai_command_auditor.cli init --template general
```

### Step 5: Setup PATH (if needed)

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or create symlink
sudo ln -s $(which ai-auditor) /usr/local/bin/ai-auditor
```

### Step 6: Configure Git Hooks (Optional)

```bash
# For existing git repository
cd your-project
ai-auditor setup-hooks

# Or manually copy hooks
cp ~/.ai-auditor/hooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

## 🌍 Environment-Specific Installation

### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv git curl

# Install AI Command Auditor
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh

# Add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### CentOS/RHEL/Fedora

```bash
# Install dependencies
sudo dnf install python3 python3-pip git curl  # Fedora
# sudo yum install python3 python3-pip git curl  # CentOS/RHEL

# Install AI Command Auditor
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install AI Command Auditor
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

### Windows (WSL2)

```bash
# In WSL2 terminal
# Update packages
sudo apt update

# Install dependencies
sudo apt install python3 python3-pip git curl

# Install AI Command Auditor
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh

# Note: Windows paths might need special handling
# Add to ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

## 🔧 Post-Installation Configuration

### API Key Setup

```bash
# Set OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Add to shell profile for persistence
echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.bashrc

# Or use configuration file
ai-auditor config set ai.api_key "your-api-key-here"
```

### Project Initialization

```bash
# Initialize in your project
cd your-project
ai-auditor init

# Choose template based on project type
ai-auditor init --template python    # Python projects
ai-auditor init --template nodejs    # Node.js projects
ai-auditor init --template security  # High-security environments
```

### Git Hooks Setup

```bash
# Setup git hooks
ai-auditor setup-hooks

# Verify hooks are installed
ls -la .git/hooks/

# Test hooks
ai-auditor test-hooks
```

## ❗ Troubleshooting Installation

### Common Issues

**Permission denied errors:**

```bash
# Use sudo for system-wide installation
sudo curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh

# Or install to user directory
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --user-install
```

**Python version too old:**

```bash
# Check Python version
python3 --version

# Install newer Python (Ubuntu/Debian)
sudo apt install python3.10

# Install newer Python (macOS)
brew install python@3.10
```

**Command not found after installation:**

```bash
# Check if installed
which ai-auditor

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or find installation location
find / -name "ai-auditor" 2>/dev/null
```

**Network/download issues:**

```bash
# Try manual download
wget https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh
chmod +x install.sh
./install.sh

# Or use alternative mirror
curl -fsSL https://cdn.etherisc.com/ai-command-auditor/install.sh | sh
```

### Getting Help

If you encounter issues:

1. Check our [Troubleshooting Guide](/support/troubleshooting/)
2. Search [GitHub Issues](https://github.com/etherisc/ai-command-auditor/issues)
3. Ask on [GitHub Discussions](https://github.com/etherisc/ai-command-auditor/discussions)
4. Contact [Support](/support/)

## 📚 Next Steps

After successful installation:

- 📖 [Configure AI Command Auditor](/configuration/) for your project
- 🎯 [Follow the Tutorial](/examples/tutorial/) to learn the basics
- 🔌 [Explore CLI Commands](/api/cli/) for advanced usage
- 💡 [Browse Examples](/examples/) for your specific use case

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
  border-left: 4px solid #007bff;
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
