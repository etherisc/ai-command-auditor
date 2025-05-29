# AI Command Auditor - Devcontainer Integration Proposal

## Overview

Transform the AI Command Auditor into a reusable tool that can be easily integrated into any devcontainer setup, with user-customizable rules and simple installation.

## Proposed Solution: Hybrid Approach

### 1. Python Package Distribution (PyPI)

**Package Name**: `ai-command-auditor`

**Core Components**:

- Python modules for command validation and security checking
- CLI interface for setup and management
- Core git hooks and CI pipeline templates

**Installation**: `pip install ai-command-auditor`

### 2. One-Line Installer Script

**Usage**:

```bash
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

**What it does**:

1. Installs the Python package
2. Creates `.ai-auditor/` directory in project root
3. Copies all user-customizable files to accessible locations
4. Sets up git hooks and pre-commit configuration
5. Provides setup verification

## Directory Structure After Installation

```
your-project/
├── .ai-auditor/                    # User-customizable configuration
│   ├── config/
│   │   ├── auditor.yml            # Main configuration
│   │   ├── rules/
│   │   │   ├── security-rules.yml  # Security validation rules
│   │   │   ├── style-rules.yml     # Code style rules
│   │   │   └── custom-rules.yml    # User custom rules
│   │   └── prompts/
│   │       ├── openai-prompts.yml  # AI validation prompts
│   │       └── custom-prompts.yml  # User custom prompts
│   ├── hooks/                      # Git hook scripts (customizable)
│   │   ├── pre-commit.sh
│   │   ├── pre-push.sh
│   │   └── setup-hooks.sh
│   ├── workflows/                  # GitHub Actions templates
│   │   └── ai-auditor-ci.yml
│   └── README.md                   # Configuration guide
├── .pre-commit-config.yaml         # Generated pre-commit config
├── .github/workflows/               # Generated CI pipeline
└── your existing project files...
```

## Installation Options

### Option A: One-Line Installer (Recommended)

```bash
# Install everything with defaults
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh

# Install with custom options
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --config-dir=.auditor --no-hooks
```

### Option B: Python Package + Manual Setup

```bash
# Install package
pip install ai-command-auditor

# Initialize in project
ai-auditor init

# Setup git hooks
ai-auditor setup-hooks
```

### Option C: Devcontainer Integration

Add to `.devcontainer/Dockerfile`:

```dockerfile
# Install AI Command Auditor
RUN curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --system-wide
```

Add to `.devcontainer/devcontainer.json`:

```json
{
  "postCreateCommand": "ai-auditor init --project-setup"
}
```

## Key Features

### 1. User-Accessible Configuration

**Location**: `.ai-auditor/config/`

- All rules and prompts in YAML format
- Well-documented with examples
- Easy to version control
- Template system for common configurations

### 2. Flexible Installation

**Installer Options**:

- `--config-dir=PATH`: Custom config directory (default: `.ai-auditor`)
- `--no-hooks`: Skip git hooks setup
- `--no-ci`: Skip GitHub Actions setup
- `--template=TYPE`: Use predefined template (python, node, general)
- `--system-wide`: Install globally for all projects

### 3. CLI Management

**Commands**:

```bash
ai-auditor init                    # Initialize in current project
ai-auditor setup-hooks            # Setup/update git hooks
ai-auditor check-command "cmd"     # Test command validation
ai-auditor update-config           # Update config templates
ai-auditor validate-setup          # Verify installation
ai-auditor generate-ci             # Generate GitHub Actions workflow
```

### 4. Template System

**Predefined Templates**:

- `python`: Python-focused rules and CI
- `node`: Node.js/JavaScript rules
- `rust`: Rust development rules
- `general`: Language-agnostic rules
- `security`: Security-focused configuration

## Configuration Customization

### Security Rules (`.ai-auditor/config/rules/security-rules.yml`)

```yaml
dangerous_patterns:
  - pattern: "rm\\s+-rf\\s+/"
    severity: "critical"
    message: "Attempting to delete root directory"

  - pattern: "sudo\\s+chmod\\s+777"
    severity: "high"
    message: "Setting dangerous file permissions"

custom_validators:
  - name: "check_api_keys"
    enabled: true
    script: ".ai-auditor/validators/api_key_check.py"
```

### AI Prompts (`.ai-auditor/config/prompts/openai-prompts.yml`)

```yaml
security_analysis_prompt: |
  Analyze this command for security risks:
  Command: {command}
  Context: {context}

  Rate from 1-10 and explain any concerns:

code_review_prompt: |
  Review this code change for:
  - Security vulnerabilities
  - Code quality issues
  - Best practice violations

  Code: {code}
```

## Distribution Strategy

### 1. Python Package (PyPI)

- Core functionality and CLI
- Automatic dependency management
- Version updates via pip
- Standard `pip install ai-command-auditor`

### 2. GitHub-Based Distribution

- **Installer Script**: Hosted as `install.sh` in repository root
- **GitHub Releases**: Versioned releases with release assets
- **Raw GitHub Content**: Direct access to installer script
- **GitHub Pages**: Documentation and installation guides

### 3. Documentation & Installation Hub

- **GitHub Pages Site**: `etherisc.github.io/ai-command-auditor`
- **Repository README**: Primary documentation entry point
- **Wiki**: Detailed configuration guides and examples
- **Releases Page**: Download links and changelog

### 4. Alternative Installation Methods

- **GitHub CLI**: `gh repo clone etherisc/ai-command-auditor && cd ai-command-auditor && ./install.sh`
- **Download ZIP**: Manual download and local installation
- **Git Submodule**: For projects wanting to include as dependency

## Benefits for Users

### 1. Easy Integration

- Single command setup using GitHub's reliable infrastructure
- Works with existing projects
- Minimal configuration required
- No dependency on external services

### 2. Full Customization

- All rules in accessible files
- Easy to modify prompts and validators
- Version control friendly
- Template-based quick start

### 3. Maintenance

- Easy updates via package manager or GitHub releases
- Config files preserved during updates
- Clear separation between tool and configuration
- GitHub's built-in version management

### 4. Flexibility

- Works with any project structure
- Multiple programming languages
- Custom validation scripts
- Configurable CI pipelines
- GitHub's ecosystem integration

## Implementation Plan

### Phase 1: Package Structure

- Refactor current code into proper Python package
- Create CLI interface
- Design configuration file structure
- Create installer script in repository root

### Phase 2: GitHub Integration

- Setup GitHub Pages for documentation
- Create release workflow for automated PyPI publishing
- Design installer script with GitHub API integration
- Implement GitHub-based template system

### Phase 3: Distribution Setup

- Publish to PyPI via GitHub Actions
- Setup GitHub Pages documentation site
- Create comprehensive README and Wiki
- Test installer script from GitHub

### Phase 4: Testing & Documentation

- Test with various project types
- Create integration guides on GitHub Pages
- Build example configurations in repository
- Create video tutorials and documentation

## Success Criteria

- [ ] One-command installation in any project
- [ ] All configuration files easily accessible and modifiable
- [ ] Works seamlessly with existing devcontainer setups
- [ ] Clear documentation and examples
- [ ] Template system for common use cases
- [ ] Backward compatibility with current setup

## Next Steps

1. **User Review**: Get feedback on this proposal
2. **Architecture Design**: Plan the package refactoring
3. **Create Task Planning**: Break down into implementable tasks
4. **Begin Implementation**: Start with package structure

This approach provides maximum flexibility while maintaining ease of use, making the AI Command Auditor a valuable tool for any development team.

---

# Detailed Implementation Planning

## Implementation Tasks

| # | Task Description | Definition of Done | Status |
|---|------------------|-------------------|--------|
| 8.1 | **Package Structure Refactoring** - Refactor current codebase into proper Python package structure with setup.py, CLI interface, and modular components | Python package installable via pip, CLI commands functional (`ai-auditor --help`), modular structure with core/analysis/cli modules | Complete |
| 8.2 | **CLI Interface Development** - Create comprehensive CLI with init, setup-hooks, check-command, validate-setup commands | All CLI commands work: `ai-auditor init`, `ai-auditor setup-hooks`, `ai-auditor check-command "test"`, `ai-auditor validate-setup` | Complete |
| 8.3 | **Configuration Template System** - Create user-accessible configuration directory structure with templates for different project types | `.ai-auditor/` directory created with config/, rules/, prompts/, hooks/ subdirectories, templates for python/node/rust/general setups | Open |
| 8.4 | **Installer Script Creation** - Develop GitHub-hosted installer script that sets up the tool in any project | `install.sh` script works: downloads package, creates config directory, sets up hooks, verifies installation | Open |
| 8.5 | **GitHub Pages Documentation** - Create comprehensive documentation site with installation guides and configuration examples | GitHub Pages site live at `etherisc.github.io/ai-command-auditor` with complete installation and configuration docs | Open |
| 8.6 | **PyPI Package Publishing** - Setup automated PyPI publishing via GitHub Actions and prepare package for distribution | Package published to PyPI as `ai-command-auditor`, GitHub Actions workflow for automated publishing working | Open |
| 8.7 | **Integration Testing** - Test the complete installation and setup process across different project types and environments | Installation tested on clean environments, works with Python/Node.js/Rust projects, devcontainer integration verified | Open |
| 8.8 | **Documentation and Examples** - Create comprehensive README, usage examples, and troubleshooting guide | Repository README updated, examples provided for common use cases, troubleshooting guide available | Open |

## Implementation Details

### Phase 1: Core Package Structure (Tasks 8.1-8.2)

**8.1 Package Structure Refactoring**

- Create `setup.py` and `pyproject.toml` for pip installation
- Reorganize code into proper package structure:

  ```
  ai_command_auditor/
  ├── __init__.py
  ├── core/
  │   ├── __init__.py
  │   ├── validator.py
  │   ├── config.py
  │   └── rules.py
  ├── analysis/
  │   ├── __init__.py
  │   ├── openai_checker.py
  │   └── security_analyzer.py
  ├── cli/
  │   ├── __init__.py
  │   └── main.py
  └── templates/
      ├── config/
      ├── rules/
      ├── prompts/
      └── hooks/
  ```

- Create entry point for CLI: `ai-auditor` command

**8.2 CLI Interface Development**

- `ai-auditor init [--template TYPE] [--config-dir PATH]`: Initialize project
- `ai-auditor setup-hooks [--force]`: Setup git hooks
- `ai-auditor check-command "command"`: Test command validation
- `ai-auditor validate-setup`: Verify installation
- `ai-auditor update-config`: Update configuration templates

### Phase 2: Configuration and Installation (Tasks 8.3-8.4)

**8.3 Configuration Template System**

- Create `.ai-auditor/` directory structure
- Template files for different project types
- User-customizable rules and prompts
- Git hooks that reference user config

**8.4 Installer Script Creation**

- `install.sh` script in repository root
- Detects environment and installs appropriately
- Supports command-line options
- Verifies installation success

### Phase 3: Distribution and Documentation (Tasks 8.5-8.8)

**8.5 GitHub Pages Documentation**

- Setup GitHub Pages with Jekyll
- Installation guides for different scenarios
- Configuration examples and tutorials
- API documentation for custom validators

**8.6 PyPI Package Publishing**

- GitHub Actions workflow for automated publishing
- Version management and release tagging
- Package metadata and dependencies

**8.7-8.8 Testing and Documentation**

- End-to-end testing across environments
- Comprehensive documentation and examples

## Technical Requirements

### Primary Goals

- [ ] One-command installation: `curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh`
- [ ] All configuration files easily accessible in `.ai-auditor/` directory
- [ ] Works seamlessly with existing devcontainer setups
- [ ] Package available on PyPI: `pip install ai-command-auditor`

### Quality Gates

- [ ] All linting and tests pass
- [ ] Installation works on fresh Ubuntu/Debian environments
- [ ] Documentation complete with examples
- [ ] Security review of installer script completed

## Dependencies and Prerequisites

### External Dependencies

- Python 3.8+ for package development
- GitHub Actions for CI/CD and publishing
- PyPI account for package publishing
- GitHub Pages for documentation hosting

### Internal Dependencies

- Current codebase in working state (✅ Complete)
- Git hooks and CI pipeline functional (✅ Complete)
- Project structure established (✅ Complete)

## Risk Assessment

### Medium Risk

- **PyPI Publishing**: First-time setup may require troubleshooting
- **Cross-platform Compatibility**: Installer script needs to work across different environments
- **Template System**: Balancing flexibility with simplicity

### Mitigation Strategies

- Test PyPI publishing on test.pypi.org first
- Use Docker containers for cross-platform testing
- Start with simple templates, expand based on feedback

## Timeline Estimate

- **Phase 1** (8.1-8.2): 2-3 implementation sessions
- **Phase 2** (8.3-8.4): 2 implementation sessions
- **Phase 3** (8.5-8.8): 2-3 implementation sessions

**Total Estimated Effort**: 6-8 implementation sessions
