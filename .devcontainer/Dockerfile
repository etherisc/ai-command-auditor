# Simple Dockerfile for AI Command Auditor
FROM python:3.11-bullseye

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install basic system packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    bash-completion \
    shellcheck \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# Create vscode user
RUN useradd -m -s /bin/bash vscode \
    && echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to vscode user
USER vscode
WORKDIR /workspaces/ai-command-auditor

# Install Python packages
RUN pip install --user --upgrade pip \
    && pip install --user \
        black \
        pytest \
        pylint \
        requests \
        pyyaml \
        click

# Set up environment
ENV PATH="/home/vscode/.local/bin:${PATH}"
ENV PYTHONPATH="/workspaces/ai-command-auditor/scripts/python:${PYTHONPATH}"

# Default command
CMD ["bash"] 