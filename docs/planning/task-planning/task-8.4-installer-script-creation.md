# Task 8.4: Installer Script Creation

## Overview

Task 8.4 focuses on creating a GitHub-hosted installer script that enables one-command installation of AI Command Auditor in any project. This builds on the template system from Task 8.3 and provides seamless distribution and setup capabilities.

## Task Breakdown

| Sub-task | Task Description | Definition of Done | Status |
|----------|------------------|-------------------|--------|
| 8.4.1 | **Core Installer Script** - Create the main install.sh script with command-line argument parsing and error handling | Complete install.sh script that can download, install, and configure AI Command Auditor with proper error handling and logging | ✅ Complete |
| 8.4.2 | **Installation Detection and Setup** - Implement environment detection and appropriate installation methods (pip, system package manager, etc.) | Script detects Python environment, installs ai-command-auditor package, handles virtual environments and system installations | ✅ Complete |
| 8.4.3 | **Configuration Directory Creation** - Implement the `.ai-auditor/` directory setup with template selection and customization | Script creates complete .ai-auditor/ directory structure, applies selected templates, and sets up user-customizable configuration files | ✅ Complete |
| 8.4.4 | **Git Hooks Integration** - Integrate git hooks setup into the installer with optional hook configuration | Script sets up git hooks using ai-auditor CLI, handles existing hooks gracefully, and provides hook customization options | ✅ Complete |
| 8.4.5 | **Installation Verification and Testing** - Implement comprehensive verification of successful installation and testing framework | Script verifies all components are working, runs test commands, and provides troubleshooting information on failure | ✅ Complete |

## Detailed Requirements

### 8.4.1 Core Installer Script

**Objective**: Create a robust, user-friendly installer script

**Implementation Details**:

```bash
#!/bin/bash
# AI Command Auditor Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

**Features**:

- Command-line argument parsing (`--config-dir`, `--template`, `--no-hooks`, etc.)
- Comprehensive error handling and logging
- Progress indicators and user feedback
- Support for interactive and non-interactive modes
- Rollback capability on installation failure

**Command-line Options**:

- `--config-dir=PATH`: Custom config directory (default: `.ai-auditor`)
- `--template=TYPE`: Template selection (python, node, rust, general, security)
- `--no-hooks`: Skip git hooks setup
- `--no-ci`: Skip GitHub Actions setup
- `--system-wide`: Install globally for all projects
- `--quiet`: Minimal output mode
- `--verbose`: Detailed logging mode
- `--dry-run`: Show what would be done without executing

**DoD**:

- [x] Script accepts and processes all command-line options
- [x] Proper error handling with meaningful error messages
- [x] Progress indicators show installation status
- [x] Script works in both interactive and non-interactive modes
- [x] Rollback functionality on installation failure

### 8.4.2 Installation Detection and Setup

**Objective**: Intelligent environment detection and package installation

**Implementation Details**:

- Detect Python version and availability
- Handle virtual environments vs system installation
- Support multiple installation methods (pip, pipx, system packages)
- Verify package installation success

**Environment Detection**:

```bash
# Python environment detection
detect_python_environment() {
    # Check for Python 3.8+
    # Detect virtual environment
    # Check pip availability
    # Determine installation method
}
```

**Installation Methods**:

- **Pip Installation**: `pip install ai-command-auditor`
- **Pipx Installation**: `pipx install ai-command-auditor` (for global CLI tools)
- **Virtual Environment**: Create/activate venv if needed
- **System Package**: Fall back to system package manager if available

**DoD**:

- [x] Correctly detects Python 3.8+ availability
- [x] Handles virtual environments appropriately
- [x] Installs package using best available method
- [x] Verifies package installation and CLI availability
- [x] Provides fallback options for installation failures

### 8.4.3 Configuration Directory Creation

**Objective**: Set up complete `.ai-auditor/` directory with templates

**Implementation Details**:

- Use the TemplateEngine from Task 8.3
- Apply selected template (python, node, rust, general, security)
- Create directory structure with proper permissions
- Generate configuration files with user-specific defaults

**Directory Structure Creation**:

```bash
# Create .ai-auditor/ directory structure
create_config_directory() {
    # Create directory structure
    # Apply template using ai-auditor CLI
    # Set proper file permissions
    # Generate custom configuration
}
```

**Template Integration**:

- Use `ai-auditor init --template TYPE` command
- Customize templates based on detected project type
- Allow user customization of template variables
- Preserve existing configuration if present

**DoD**:

- [x] Creates complete .ai-auditor/ directory structure
- [x] Applies selected template correctly
- [x] Generates valid configuration files
- [x] Sets appropriate file permissions
- [x] Preserves existing configuration when upgrading

### 8.4.4 Git Hooks Integration

**Objective**: Set up git hooks with graceful handling of existing setups

**Implementation Details**:

- Use `ai-auditor setup-hooks` command
- Handle existing git hooks gracefully
- Provide options for hook customization
- Support pre-commit framework integration

**Git Hooks Setup**:

```bash
# Setup git hooks
setup_git_hooks() {
    # Check for existing hooks
    # Backup existing hooks if present
    # Install AI Command Auditor hooks
    # Verify hook installation
}
```

**Hook Management**:

- Detect existing git hooks and pre-commit setups
- Merge with existing hooks when possible
- Provide backup/restore functionality
- Support both direct hooks and pre-commit framework

**DoD**:

- [x] Sets up git hooks successfully
- [x] Handles existing hooks gracefully (backup/merge)
- [x] Supports both direct hooks and pre-commit framework
- [x] Provides hook customization options
- [x] Verifies hook functionality after installation

### 8.4.5 Installation Verification and Testing

**Objective**: Comprehensive verification and troubleshooting support

**Implementation Details**:

- Run installation verification tests
- Test all installed components
- Provide troubleshooting information
- Generate installation report

**Verification Tests**:

```bash
# Verify installation
verify_installation() {
    # Check package installation
    # Verify CLI commands work
    # Test configuration validity
    # Test git hooks functionality
    # Run sample command validation
}
```

**Test Suite**:

- Package import test: `python -c "import ai_command_auditor"`
- CLI availability: `ai-auditor --version`
- Configuration validity: `ai-auditor validate-setup`
- Hook functionality: Test with sample command
- Template rendering: Verify configuration files are valid

**Troubleshooting**:

- Collect system information
- Provide common issue solutions
- Generate detailed error reports
- Offer manual installation steps as fallback

**DoD**:

- [x] Runs comprehensive verification tests
- [x] Tests all installed components
- [x] Provides clear success/failure feedback
- [x] Generates troubleshooting information on failure
- [x] Creates installation report with system details

## Technical Implementation

### Script Structure

```bash
#!/bin/bash
set -euo pipefail

# Global variables and configuration
SCRIPT_NAME="AI Command Auditor Installer"
CONFIG_DIR=".ai-auditor"
TEMPLATE="general"
INSTALL_HOOKS=true
INSTALL_CI=true
VERBOSE=false
DRY_RUN=false

# Main functions
main() {
    parse_arguments "$@"
    print_banner
    check_prerequisites
    install_package
    setup_configuration
    setup_git_hooks
    verify_installation
    print_success_message
}

# Implementation functions
parse_arguments() { }
check_prerequisites() { }
install_package() { }
setup_configuration() { }
setup_git_hooks() { }
verify_installation() { }
```

### Error Handling Strategy

```bash
# Error handling
set -euo pipefail
trap cleanup_on_error ERR

cleanup_on_error() {
    echo "Installation failed. Rolling back changes..."
    # Rollback logic
}

log_error() {
    echo "ERROR: $1" >&2
    echo "See installation log: $LOG_FILE"
}
```

### Testing Strategy

**Local Testing**:

- Test in clean Docker containers
- Test with different Python environments
- Test with existing git setups
- Test all command-line options

**CI Testing**:

- GitHub Actions workflow to test installer
- Test on multiple OS environments (Ubuntu, Debian)
- Test with different project types
- Integration testing with devcontainers

## Usage Examples

### Basic Installation

```bash
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
```

### Python Project with Production Settings

```bash
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- \
  --template python \
  --config-dir .ai-auditor \
  --verbose
```

### No Git Hooks (CI Only)

```bash
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- \
  --no-hooks \
  --template general
```

### Dry Run (See What Would Happen)

```bash
curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- \
  --dry-run \
  --verbose
```

## Dependencies

### External Dependencies

- **curl**: For downloading the installer
- **bash**: Shell environment (4.0+)
- **Python 3.8+**: Runtime environment
- **pip**: Package installation
- **git**: Version control (optional but recommended)

### Internal Dependencies

- **ai-command-auditor package**: Must be installable via pip
- **TemplateEngine**: From Task 8.3 for configuration setup
- **CLI commands**: All CLI functionality from Task 8.2

## Success Criteria

- [x] One-command installation works: `curl -fsSL ... | sh`
- [x] All command-line options function correctly
- [x] Handles various environment configurations
- [x] Sets up complete working installation
- [x] Provides clear feedback and error handling
- [x] Works in CI/CD environments
- [x] Comprehensive testing and verification

## Risk Assessment

### High Risk Areas

- **Cross-platform compatibility**: Bash script differences
- **Python environment detection**: Virtual envs, system installs
- **Existing git hooks**: Conflicts with user setups
- **Network dependencies**: Download failures

### Mitigation Strategies

- Extensive testing in different environments
- Robust error handling and rollback mechanisms
- Clear documentation and troubleshooting guides
- Fallback installation methods

## Timeline Estimate

**Total Estimated Effort**: 2-3 implementation sessions

**Session 1**: Core installer script and environment detection (8.4.1, 8.4.2)
**Session 2**: Configuration setup and git hooks (8.4.3, 8.4.4)
**Session 3**: Verification, testing, and polish (8.4.5)

## Implementation Notes

- Follow established bash coding standards from cursor rules
- Use comprehensive error handling and logging
- Provide user-friendly output with progress indicators
- Support both interactive and automated installation scenarios
- Ensure script is idempotent (can be run multiple times safely)
