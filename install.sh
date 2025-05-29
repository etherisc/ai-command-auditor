#!/bin/bash
#
# Script Name: install.sh
# Description: AI Command Auditor Installer - One-command installation and setup
# Author: Etherisc
# Date: 2024
# Version: 1.0
#
# Usage: curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh
# Example: curl -fsSL https://raw.githubusercontent.com/etherisc/ai-command-auditor/main/install.sh | sh -s -- --template python --verbose
#

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Constants
readonly SCRIPT_NAME="$(basename "$0")"
readonly LOG_FILE="/tmp/ai-auditor-install.log"
readonly PACKAGE_NAME="ai-command-auditor"
readonly GITHUB_REPO="etherisc/ai-command-auditor"
readonly MIN_PYTHON_VERSION="3.8"

# Global variables
VERBOSE=false
QUIET=false
DRY_RUN=false
FORCE=false
CONFIG_DIR=".ai-auditor"
TEMPLATE="general"
INSTALL_HOOKS=true
INSTALL_CI=true
SYSTEM_WIDE=false
PYTHON_CMD=""
PIP_CMD=""
INSTALL_LOG=""

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Logging functions
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp="$(date +'%Y-%m-%d %H:%M:%S')"

    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"

    if [[ "$level" == "ERROR" ]]; then
        echo -e "${RED}ERROR: $message${NC}" >&2
    elif [[ "$level" == "WARN" ]]; then
        echo -e "${YELLOW}WARNING: $message${NC}" >&2
    elif [[ "$level" == "INFO" ]]; then
        if [[ "$QUIET" != true ]]; then
            echo -e "${BLUE}INFO: $message${NC}"
        fi
    elif [[ "$level" == "SUCCESS" ]]; then
        if [[ "$QUIET" != true ]]; then
            echo -e "${GREEN}✓ $message${NC}"
        fi
    elif [[ "$level" == "DEBUG" ]]; then
        if [[ "$VERBOSE" == true ]]; then
            echo -e "${BLUE}DEBUG: $message${NC}"
        fi
    fi
}

info() {
    log "INFO" "$@"
}

success() {
    log "SUCCESS" "$@"
}

warn() {
    log "WARN" "$@"
}

error() {
    log "ERROR" "$@"
}

debug() {
    log "DEBUG" "$@"
}

# Progress indicator
show_progress() {
    local current="$1"
    local total="$2"
    local task="$3"

    if [[ "$QUIET" != true ]]; then
        echo -e "${BLUE}[$current/$total] $task${NC}"
    fi
}

# Usage information
usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

AI Command Auditor Installer - One-command installation and setup

OPTIONS:
    -h, --help              Show this help message
    -v, --verbose           Enable verbose output
    -q, --quiet             Minimal output mode
    -d, --dry-run           Show what would be done without executing
    -f, --force             Force installation even if already installed

    --config-dir=PATH       Custom config directory (default: .ai-auditor)
    --template=TYPE         Template selection: python, node, rust, general, security (default: general)
    --no-hooks              Skip git hooks setup
    --no-ci                 Skip GitHub Actions setup
    --system-wide           Install globally for all projects

EXAMPLES:
    # Basic installation
    $SCRIPT_NAME

    # Python project with verbose output
    $SCRIPT_NAME --template python --verbose

    # Install without git hooks
    $SCRIPT_NAME --no-hooks --template general

    # Dry run to see what would happen
    $SCRIPT_NAME --dry-run --verbose

For more information, visit: https://github.com/$GITHUB_REPO

EOF
}

# Error cleanup
cleanup_on_error() {
    local exit_code=$?

    error "Installation failed with exit code $exit_code"
    error "Rolling back changes..."

    # Rollback logic
    if [[ -n "${INSTALL_LOG:-}" ]] && [[ -f "$INSTALL_LOG" ]]; then
        debug "Installation log available at: $INSTALL_LOG"
    fi

    # Remove partially created config directory
    if [[ -d "$CONFIG_DIR" ]] && [[ "$DRY_RUN" != true ]]; then
        warn "Removing partially created config directory: $CONFIG_DIR"
        rm -rf "$CONFIG_DIR" || true
    fi

    error "Installation failed. Check the log file: $LOG_FILE"
    error "For help, visit: https://github.com/$GITHUB_REPO/issues"

    exit $exit_code
}

# Set up error trap
trap cleanup_on_error ERR

# Command validation
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Version comparison
version_compare() {
    # Compare versions in format x.y.z
    # Returns 0 if version1 >= version2, 1 otherwise
    local version1="$1"
    local version2="$2"

    # Convert to comparable format
    local v1_major v1_minor v1_patch
    local v2_major v2_minor v2_patch

    IFS='.' read -r v1_major v1_minor v1_patch <<< "$version1"
    IFS='.' read -r v2_major v2_minor v2_patch <<< "$version2"

    # Default patch versions to 0 if not provided
    v1_patch=${v1_patch:-0}
    v2_patch=${v2_patch:-0}

    # Compare major version
    if [[ $v1_major -gt $v2_major ]]; then
        return 0
    elif [[ $v1_major -lt $v2_major ]]; then
        return 1
    fi

    # Compare minor version
    if [[ $v1_minor -gt $v2_minor ]]; then
        return 0
    elif [[ $v1_minor -lt $v2_minor ]]; then
        return 1
    fi

    # Compare patch version
    if [[ $v1_patch -ge $v2_patch ]]; then
        return 0
    else
        return 1
    fi
}

# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -q|--quiet)
                QUIET=true
                shift
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -f|--force)
                FORCE=true
                shift
                ;;
            --config-dir=*)
                CONFIG_DIR="${1#*=}"
                shift
                ;;
            --config-dir)
                CONFIG_DIR="$2"
                shift 2
                ;;
            --template=*)
                TEMPLATE="${1#*=}"
                shift
                ;;
            --template)
                TEMPLATE="$2"
                shift 2
                ;;
            --no-hooks)
                INSTALL_HOOKS=false
                shift
                ;;
            --no-ci)
                INSTALL_CI=false
                shift
                ;;
            --system-wide)
                SYSTEM_WIDE=true
                shift
                ;;
            *)
                error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done

    # Validate template option
    case "$TEMPLATE" in
        python|node|rust|general|security)
            debug "Using template: $TEMPLATE"
            ;;
        *)
            error "Invalid template: $TEMPLATE"
            error "Valid templates: python, node, rust, general, security"
            exit 1
            ;;
    esac

    # Validate config directory
    if [[ -z "$CONFIG_DIR" ]]; then
        error "Config directory cannot be empty"
        exit 1
    fi

    debug "Parsed arguments:"
    debug "  CONFIG_DIR: $CONFIG_DIR"
    debug "  TEMPLATE: $TEMPLATE"
    debug "  INSTALL_HOOKS: $INSTALL_HOOKS"
    debug "  INSTALL_CI: $INSTALL_CI"
    debug "  SYSTEM_WIDE: $SYSTEM_WIDE"
    debug "  VERBOSE: $VERBOSE"
    debug "  QUIET: $QUIET"
    debug "  DRY_RUN: $DRY_RUN"
    debug "  FORCE: $FORCE"
}

# Print banner
print_banner() {
    if [[ "$QUIET" != true ]]; then
        cat << 'EOF'

╔═══════════════════════════════════════════════════════════╗
║                 AI Command Auditor Installer              ║
║                                                           ║
║   Secure command validation and analysis for your        ║
║   development workflow                                    ║
╚═══════════════════════════════════════════════════════════╝

EOF
    fi

    info "Starting AI Command Auditor installation..."

    if [[ "$DRY_RUN" == true ]]; then
        warn "DRY RUN MODE - No changes will be made"
    fi
}

# Check prerequisites
check_prerequisites() {
    show_progress 1 7 "Checking prerequisites"

    debug "Checking system prerequisites..."

    # Check for required commands
    local required_commands=("curl" "python3")
    local missing_commands=()

    for cmd in "${required_commands[@]}"; do
        if ! command_exists "$cmd"; then
            missing_commands+=("$cmd")
        fi
    done

    if [[ ${#missing_commands[@]} -gt 0 ]]; then
        error "Missing required commands: ${missing_commands[*]}"
        error "Please install the missing commands and try again"
        exit 1
    fi

    success "Prerequisites check completed"
}

# Python environment detection
detect_python_environment() {
    debug "Detecting Python environment..."

    # Find available Python commands
    local python_candidates=("python3" "python")
    local found_python=""

    for cmd in "${python_candidates[@]}"; do
        if command_exists "$cmd"; then
            local version
            version=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
            debug "Found $cmd with version: $version"

            if version_compare "$version" "$MIN_PYTHON_VERSION"; then
                found_python="$cmd"
                PYTHON_CMD="$cmd"
                debug "Selected Python command: $PYTHON_CMD"
                break
            else
                debug "$cmd version $version is below minimum required $MIN_PYTHON_VERSION"
            fi
        fi
    done

    if [[ -z "$found_python" ]]; then
        error "Python $MIN_PYTHON_VERSION or higher is required"
        error "Please install Python $MIN_PYTHON_VERSION+ and try again"
        exit 1
    fi

    # Check for pip
    local pip_candidates=("pip3" "pip")
    local found_pip=""

    for cmd in "${pip_candidates[@]}"; do
        if command_exists "$cmd"; then
            # Verify this pip works with our Python
            if $cmd --version >/dev/null 2>&1; then
                found_pip="$cmd"
                PIP_CMD="$cmd"
                debug "Selected pip command: $PIP_CMD"
                break
            fi
        fi
    done

    if [[ -z "$found_pip" ]]; then
        error "pip is required but not found"
        error "Please install pip and try again"
        exit 1
    fi

    # Check if we're in a virtual environment
    if [[ -n "${VIRTUAL_ENV:-}" ]]; then
        info "Virtual environment detected: $VIRTUAL_ENV"
        debug "Will install to virtual environment"
    elif [[ -n "${CONDA_DEFAULT_ENV:-}" ]]; then
        info "Conda environment detected: $CONDA_DEFAULT_ENV"
        debug "Will install to conda environment"
    else
        debug "No virtual environment detected"
        if [[ "$SYSTEM_WIDE" != true ]]; then
            warn "Installing to system Python - consider using a virtual environment"
        fi
    fi

    success "Python environment detection completed"
}

# Check if package is already installed
check_existing_installation() {
    debug "Checking for existing installation..."

    if $PYTHON_CMD -c "import $PACKAGE_NAME" >/dev/null 2>&1; then
        local installed_version
        installed_version=$($PYTHON_CMD -c "import $PACKAGE_NAME; print(getattr($PACKAGE_NAME, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")

        if [[ "$FORCE" == true ]]; then
            warn "Package $PACKAGE_NAME is already installed (version: $installed_version) - forcing reinstall"
            return 1  # Not installed (force reinstall)
        else
            success "Package $PACKAGE_NAME is already installed (version: $installed_version)"
            return 0  # Already installed
        fi
    else
        debug "Package $PACKAGE_NAME is not installed"
        return 1  # Not installed
    fi
}

# Install the package
install_ai_command_auditor() {
    debug "Installing AI Command Auditor package..."

    local install_cmd="$PIP_CMD install"

    # Add additional options based on configuration
    if [[ "$VERBOSE" == true ]]; then
        install_cmd="$install_cmd --verbose"
    fi

    if [[ "$FORCE" == true ]]; then
        install_cmd="$install_cmd --force-reinstall"
    fi

    # For now, we'll install from the local directory (development mode)
    # In production, this would be: install_cmd="$install_cmd $PACKAGE_NAME"
    if [[ -f "setup.py" ]] || [[ -f "pyproject.toml" ]]; then
        info "Installing from local development package..."
        install_cmd="$install_cmd -e ."
    else
        # Fallback to PyPI (when package is published)
        info "Installing from PyPI..."
        install_cmd="$install_cmd $PACKAGE_NAME"
    fi

    debug "Installation command: $install_cmd"

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would execute: $install_cmd"
        return 0
    fi

    # Execute installation
    if $install_cmd; then
        success "Package installation completed"
    else
        error "Package installation failed"
        exit 1
    fi
}

# Verify CLI installation
verify_cli_installation() {
    debug "Verifying CLI installation..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would verify CLI installation"
        return 0
    fi

    # Check if ai-auditor command is available
    if command_exists "ai-auditor"; then
        local version
        version=$(ai-auditor --version 2>/dev/null || echo "unknown")
        success "AI Command Auditor CLI is available (version: $version)"
    else
        error "AI Command Auditor CLI not found in PATH"
        error "You may need to restart your terminal or add the installation directory to PATH"
        exit 1
    fi
}

# Main package installation function
install_package() {
    show_progress 2 7 "Installing AI Command Auditor package"

    detect_python_environment

    # Check if already installed
    if check_existing_installation; then
        if [[ "$FORCE" != true ]]; then
            info "Package already installed, skipping installation"
            return 0
        fi
    fi

    install_ai_command_auditor
    verify_cli_installation

    success "Package installation completed successfully"
}

# Check for existing configuration
check_existing_configuration() {
    debug "Checking for existing configuration..."

    if [[ -d "$CONFIG_DIR" ]]; then
        if [[ "$FORCE" == true ]]; then
            warn "Configuration directory $CONFIG_DIR exists - forcing recreation"
            return 1  # Recreate config
        else
            info "Configuration directory $CONFIG_DIR already exists"
            if [[ -f "$CONFIG_DIR/config/auditor.yml" ]]; then
                success "Configuration appears to be complete"
                return 0  # Config exists
            else
                warn "Configuration directory exists but appears incomplete"
                return 1  # Recreate config
            fi
        fi
    else
        debug "Configuration directory $CONFIG_DIR does not exist"
        return 1  # Create config
    fi
}

# Create configuration directory structure
create_config_directory() {
    debug "Creating configuration directory structure..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would create directory: $CONFIG_DIR"
        return 0
    fi

    # Create main config directory
    if ! mkdir -p "$CONFIG_DIR"; then
        error "Failed to create configuration directory: $CONFIG_DIR"
        exit 1
    fi

    # Create subdirectories
    local subdirs=("config" "config/rules" "config/prompts" "hooks" "workflows" "logs")

    for subdir in "${subdirs[@]}"; do
        local full_path="$CONFIG_DIR/$subdir"
        if ! mkdir -p "$full_path"; then
            error "Failed to create directory: $full_path"
            exit 1
        fi
        debug "Created directory: $full_path"
    done

    success "Configuration directory structure created"
}

# Apply template using AI Command Auditor CLI
apply_configuration_template() {
    debug "Applying configuration template: $TEMPLATE"

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would apply template: $TEMPLATE to $CONFIG_DIR"
        return 0
    fi

    # Check if CLI is available
    if ! command_exists "ai-auditor"; then
        warn "AI Command Auditor CLI not available - using fallback configuration"
        create_fallback_configuration
        return 0
    fi

    # Use the CLI to initialize with template
    local init_cmd="ai-auditor init"
    init_cmd="$init_cmd --template $TEMPLATE"
    init_cmd="$init_cmd --config-dir $CONFIG_DIR"

    # Add environment and security level if specified in template
    case "$TEMPLATE" in
        python)
            init_cmd="$init_cmd --environment development --security-level standard"
            ;;
        security)
            init_cmd="$init_cmd --environment production --security-level strict"
            ;;
        *)
            init_cmd="$init_cmd --environment development --security-level standard"
            ;;
    esac

    debug "Template application command: $init_cmd"

    # Execute template application
    if $init_cmd; then
        success "Template application completed"
    else
        warn "Template application failed - using fallback configuration"
        create_fallback_configuration
    fi
}

# Create fallback configuration if template application fails
create_fallback_configuration() {
    debug "Creating fallback configuration..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would create fallback configuration"
        return 0
    fi

    # Create basic auditor.yml
    cat > "$CONFIG_DIR/config/auditor.yml" << 'EOF'
# AI Command Auditor Configuration
# This is a fallback configuration - customize as needed

# AI Configuration
ai:
  model: "gpt-4o"
  timeout: 30
  max_retries: 3
  temperature: 0.1
  max_tokens: 1000

# Security Configuration
security:
  max_command_length: 1000
  allow_multiline: false
  strict_mode: false
  blocked_commands: []

# Logging Configuration
logging:
  level: "INFO"
  file: ".ai-auditor/logs/auditor.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validation Configuration
validation:
  enable_ai_check: true
  enable_rule_check: true
  require_context: false
  cache_results: true

# Integration Configuration
integration:
  git_hooks: true
  ci_integration: true
  pre_commit: true
  pre_push: true

# Policy Configuration
policy:
  block_on_critical: true
  warn_on_high: true
  log_all_matches: true
  require_approval_for: ["critical", "high"]
EOF

    # Create basic security rules
    cat > "$CONFIG_DIR/config/rules/security-rules.yml" << 'EOF'
# Security Rules Configuration
# Customize these rules for your project needs

dangerous_patterns:
  - pattern: "rm\\s+-rf\\s+/"
    severity: "critical"
    message: "Attempting to delete root directory"

  - pattern: "sudo\\s+chmod\\s+777"
    severity: "high"
    message: "Setting dangerous file permissions"

  - pattern: "curl.*\\|.*sh"
    severity: "medium"
    message: "Downloading and executing scripts from internet"

  - pattern: "wget.*\\|.*sh"
    severity: "medium"
    message: "Downloading and executing scripts from internet"
EOF

    # Create basic OpenAI prompts
    cat > "$CONFIG_DIR/config/prompts/openai-prompts.yml" << 'EOF'
# OpenAI Prompts Configuration
# Customize these prompts for your analysis needs

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
EOF

    # Create README
    cat > "$CONFIG_DIR/README.md" << 'EOF'
# AI Command Auditor Configuration

This directory contains your AI Command Auditor configuration files.

## Structure

- `config/auditor.yml` - Main configuration file
- `config/rules/` - Security and validation rules
- `config/prompts/` - AI prompts for analysis
- `hooks/` - Git hook scripts (if enabled)
- `workflows/` - GitHub Actions workflows (if enabled)
- `logs/` - Application logs

## Customization

All files in this directory can be customized for your project needs.
See the documentation for details on configuration options.

## Getting Started

1. Review and customize `config/auditor.yml`
2. Add project-specific rules in `config/rules/`
3. Customize AI prompts in `config/prompts/`
4. Test your setup: `ai-auditor validate-setup`

For more information, visit: https://github.com/etherisc/ai-command-auditor
EOF

    success "Fallback configuration created"
}

# Set proper file permissions
set_config_permissions() {
    debug "Setting configuration file permissions..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would set file permissions on $CONFIG_DIR"
        return 0
    fi

    # Set directory permissions
    find "$CONFIG_DIR" -type d -exec chmod 755 {} \; 2>/dev/null || true

    # Set file permissions
    find "$CONFIG_DIR" -type f -exec chmod 644 {} \; 2>/dev/null || true

    # Make hook scripts executable if they exist
    if [[ -d "$CONFIG_DIR/hooks" ]]; then
        find "$CONFIG_DIR/hooks" -name "*.sh" -exec chmod 755 {} \; 2>/dev/null || true
    fi

    success "File permissions set"
}

# Main configuration setup function
setup_configuration() {
    show_progress 3 7 "Setting up configuration"

    # Check if configuration already exists
    if check_existing_configuration; then
        if [[ "$FORCE" != true ]]; then
            info "Configuration already exists, skipping setup"
            return 0
        fi
    fi

    create_config_directory
    apply_configuration_template
    set_config_permissions

    success "Configuration setup completed successfully"
}

# Check if we're in a git repository and setup hooks
check_git_repository() {
    debug "Checking git repository status..."

    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        warn "Not in a git repository - git hooks will be skipped"
        return 1
    fi

    local git_dir
    git_dir=$(git rev-parse --git-dir)
    debug "Git directory: $git_dir"

    if [[ ! -d "$git_dir/hooks" ]]; then
        debug "Creating git hooks directory"
        if [[ "$DRY_RUN" != true ]]; then
            mkdir -p "$git_dir/hooks"
        fi
    fi

    return 0
}

# Check for existing git hooks
check_existing_hooks() {
    local hook_name="$1"
    local git_dir
    git_dir=$(git rev-parse --git-dir)
    local hook_file="$git_dir/hooks/$hook_name"

    if [[ -f "$hook_file" ]] && [[ -s "$hook_file" ]]; then
        debug "Existing $hook_name hook found"
        return 0
    else
        debug "No existing $hook_name hook found"
        return 1
    fi
}

# Backup existing git hook
backup_existing_hook() {
    local hook_name="$1"
    local git_dir
    git_dir=$(git rev-parse --git-dir)
    local hook_file="$git_dir/hooks/$hook_name"
    local backup_file
    backup_file="$hook_file.backup.$(date +%Y%m%d_%H%M%S)"

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would backup $hook_name hook to $backup_file"
        return 0
    fi

    if cp "$hook_file" "$backup_file"; then
        success "Backed up existing $hook_name hook to $backup_file"
        return 0
    else
        error "Failed to backup existing $hook_name hook"
        return 1
    fi
}

# Check for pre-commit framework
check_precommit_framework() {
    debug "Checking for pre-commit framework..."

    # Check if pre-commit is installed
    if command_exists "pre-commit"; then
        debug "pre-commit command found"

        # Check if .pre-commit-config.yaml exists
        if [[ -f ".pre-commit-config.yaml" ]]; then
            info "Pre-commit framework detected with configuration"
            return 0
        else
            debug "pre-commit installed but no configuration found"
            return 1
        fi
    else
        debug "pre-commit framework not found"
        return 1
    fi
}

# Install hooks using AI Command Auditor CLI
install_hooks_via_cli() {
    debug "Installing hooks using AI Command Auditor CLI..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would execute: ai-auditor setup-hooks --config-dir $CONFIG_DIR"
        return 0
    fi

    # Check if CLI is available
    if ! command_exists "ai-auditor"; then
        warn "AI Command Auditor CLI not available - using manual hook setup"
        install_hooks_manually
        return $?
    fi

    # Use the CLI to setup hooks
    local setup_cmd="ai-auditor setup-hooks"
    setup_cmd="$setup_cmd --config-dir $CONFIG_DIR"

    if [[ "$VERBOSE" == true ]]; then
        setup_cmd="$setup_cmd --verbose"
    fi

    debug "Hook setup command: $setup_cmd"

    # Execute hook setup
    if $setup_cmd; then
        success "Hooks installed successfully via CLI"
        return 0
    else
        warn "CLI hook setup failed - falling back to manual setup"
        install_hooks_manually
        return $?
    fi
}

# Manual hook installation as fallback
install_hooks_manually() {
    debug "Installing hooks manually..."

    local git_dir
    git_dir=$(git rev-parse --git-dir)
    local hooks_dir="$git_dir/hooks"

    # Define hooks to install
    local hooks=("pre-commit" "pre-push")

    for hook in "${hooks[@]}"; do
        debug "Installing $hook hook..."

        local hook_file="$hooks_dir/$hook"

        if [[ "$DRY_RUN" == true ]]; then
            info "DRY RUN: Would create $hook hook at $hook_file"
            continue
        fi

        # Create the hook script
        cat > "$hook_file" << EOF
#!/bin/bash
#
# AI Command Auditor Git Hook: $hook
# Auto-generated by installer
#

# Exit on any error
set -e

# Get the config directory
CONFIG_DIR="\$(git rev-parse --show-toplevel)/$CONFIG_DIR"

# Check if ai-auditor is available
if ! command -v ai-auditor >/dev/null 2>&1; then
    echo "Warning: ai-auditor command not found - skipping validation"
    exit 0
fi

# Check if config directory exists
if [[ ! -d "\$CONFIG_DIR" ]]; then
    echo "Warning: AI Command Auditor config not found at \$CONFIG_DIR - skipping validation"
    exit 0
fi

# Run the appropriate validation
case "$hook" in
    pre-commit)
        echo "Running AI Command Auditor pre-commit validation..."
        ai-auditor validate-commit --config-dir "\$CONFIG_DIR"
        ;;
    pre-push)
        echo "Running AI Command Auditor pre-push validation..."
        ai-auditor validate-push --config-dir "\$CONFIG_DIR"
        ;;
esac

exit 0
EOF

        # Make the hook executable
        if chmod +x "$hook_file"; then
            success "Created $hook hook"
        else
            error "Failed to make $hook hook executable"
            return 1
        fi
    done

    success "Manual hook installation completed"
    return 0
}

# Setup pre-commit framework integration
setup_precommit_integration() {
    debug "Setting up pre-commit framework integration..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would setup pre-commit integration"
        return 0
    fi

    # Create .pre-commit-config.yaml if it doesn't exist
    if [[ ! -f ".pre-commit-config.yaml" ]]; then
        info "Creating .pre-commit-config.yaml for AI Command Auditor"

        cat > ".pre-commit-config.yaml" << 'EOF'
# Pre-commit configuration for AI Command Auditor
repos:
  - repo: local
    hooks:
      - id: ai-command-auditor
        name: AI Command Auditor
        entry: ai-auditor validate-commit
        language: system
        pass_filenames: false
        always_run: true
        stages: [commit]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
EOF

        success "Created .pre-commit-config.yaml"
    else
        info "Existing .pre-commit-config.yaml found - you may need to manually add AI Command Auditor hooks"
    fi

    # Install pre-commit hooks
    if command_exists "pre-commit"; then
        info "Installing pre-commit hooks..."
        if pre-commit install; then
            success "Pre-commit hooks installed successfully"
        else
            warn "Failed to install pre-commit hooks"
        fi
    else
        info "Pre-commit not available - skipping hook installation"
    fi
}

# Verify hook installation
verify_hook_installation() {
    debug "Verifying hook installation..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would verify hook installation"
        return 0
    fi

    local git_dir
    git_dir=$(git rev-parse --git-dir)
    local hooks_dir="$git_dir/hooks"

    # Check if hooks exist and are executable
    local hooks=("pre-commit" "pre-push")
    local hooks_installed=0

    for hook in "${hooks[@]}"; do
        local hook_file="$hooks_dir/$hook"

        if [[ -f "$hook_file" ]] && [[ -x "$hook_file" ]]; then
            debug "$hook hook is installed and executable"
            ((hooks_installed++))
        else
            warn "$hook hook is missing or not executable"
        fi
    done

    if [[ $hooks_installed -eq ${#hooks[@]} ]]; then
        success "All git hooks verified successfully"
        return 0
    else
        warn "Some git hooks may not be properly installed"
        return 1
    fi
}

setup_git_hooks() {
    show_progress 4 7 "Setting up git hooks"

    if [[ "$INSTALL_HOOKS" != true ]]; then
        info "Git hooks installation skipped (--no-hooks specified)"
        return 0
    fi

    # Check if we're in a git repository
    if ! check_git_repository; then
        info "Git hooks setup skipped (not in a git repository)"
        return 0
    fi

    debug "Starting git hooks setup..."

    # Handle existing hooks
    local hooks=("pre-commit" "pre-push")
    for hook in "${hooks[@]}"; do
        if check_existing_hooks "$hook"; then
            if [[ "$FORCE" == true ]]; then
                warn "Existing $hook hook found - backing up and replacing"
                backup_existing_hook "$hook"
            else
                warn "Existing $hook hook found - use --force to replace"
                info "Skipping $hook hook installation"
                continue
            fi
        fi
    done

    # Check for pre-commit framework
    if check_precommit_framework; then
        info "Pre-commit framework detected - setting up integration"
        setup_precommit_integration
    else
        info "Installing direct git hooks"
        install_hooks_via_cli
    fi

    # Verify installation
    verify_hook_installation

    success "Git hooks setup completed successfully"
}

setup_ci_pipeline() {
    show_progress 5 7 "Setting up CI pipeline"

    if [[ "$INSTALL_CI" != true ]]; then
        info "CI pipeline installation skipped (--no-ci specified)"
        return 0
    fi

    debug "CI pipeline setup..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would setup CI pipeline integration"
        return 0
    fi

    # TODO: Implement GitHub Actions workflow setup
    # This would create .github/workflows/ai-command-auditor.yml
    warn "CI pipeline setup is not yet implemented"
    warn "You can manually add GitHub Actions workflows from the documentation"

    info "CI pipeline setup completed (manual setup required)"
}

# Test package import
test_package_import() {
    debug "Testing package import..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would test package import"
        return 0
    fi

    if $PYTHON_CMD -c "import ai_command_auditor" 2>/dev/null; then
        success "Package import test passed"
        return 0
    else
        error "Package import test failed"
        return 1
    fi
}

# Test CLI availability and basic functionality
test_cli_functionality() {
    debug "Testing CLI functionality..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would test CLI functionality"
        return 0
    fi

    # Test --version command
    if ai-auditor --version >/dev/null 2>&1; then
        local version
        version=$(ai-auditor --version 2>/dev/null || echo "unknown")
        success "CLI version test passed (version: $version)"
    else
        error "CLI version test failed"
        return 1
    fi

    # Test --help command
    if ai-auditor --help >/dev/null 2>&1; then
        success "CLI help test passed"
    else
        error "CLI help test failed"
        return 1
    fi

    return 0
}

# Test configuration validity
test_configuration_validity() {
    debug "Testing configuration validity..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would test configuration validity"
        return 0
    fi

    # Check if config directory exists
    if [[ ! -d "$CONFIG_DIR" ]]; then
        error "Configuration directory not found: $CONFIG_DIR"
        return 1
    fi

    # Check main configuration file
    local config_file="$CONFIG_DIR/config/auditor.yml"
    if [[ ! -f "$config_file" ]]; then
        error "Main configuration file not found: $config_file"
        return 1
    fi

    # Test configuration validation if CLI supports it
    if command_exists "ai-auditor"; then
        # Try to validate setup using CLI
        if ai-auditor validate-setup --config-dir "$CONFIG_DIR" >/dev/null 2>&1; then
            success "Configuration validation test passed"
            return 0
        else
            warn "Configuration validation test failed - config may need adjustment"
            return 1
        fi
    else
        # Basic YAML syntax check
        if $PYTHON_CMD -c "import yaml; yaml.safe_load(open('$config_file'))" 2>/dev/null; then
            success "Configuration syntax test passed"
            return 0
        else
            error "Configuration syntax test failed - invalid YAML"
            return 1
        fi
    fi
}

# Test git hooks functionality
test_git_hooks() {
    debug "Testing git hooks functionality..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would test git hooks functionality"
        return 0
    fi

    if [[ "$INSTALL_HOOKS" != true ]]; then
        info "Git hooks not installed - skipping hook tests"
        return 0
    fi

    # Check if we're in a git repository
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        info "Not in git repository - skipping hook tests"
        return 0
    fi

    local git_dir
    git_dir=$(git rev-parse --git-dir)
    local hooks_dir="$git_dir/hooks"

    # Test each hook
    local hooks=("pre-commit" "pre-push")
    local hooks_working=0

    for hook in "${hooks[@]}"; do
        local hook_file="$hooks_dir/$hook"

        if [[ -f "$hook_file" ]] && [[ -x "$hook_file" ]]; then
            # Test if hook script is valid bash
            if bash -n "$hook_file" 2>/dev/null; then
                debug "$hook hook syntax test passed"
                ((hooks_working++))
            else
                warn "$hook hook has syntax errors"
            fi
        else
            warn "$hook hook is missing or not executable"
        fi
    done

    if [[ $hooks_working -eq ${#hooks[@]} ]]; then
        success "Git hooks functionality test passed"
        return 0
    else
        warn "Some git hooks may not be working properly"
        return 1
    fi
}

# Test sample command validation
test_sample_command() {
    debug "Testing sample command validation..."

    if [[ "$DRY_RUN" == true ]]; then
        info "DRY RUN: Would test sample command validation"
        return 0
    fi

    if ! command_exists "ai-auditor"; then
        warn "CLI not available - skipping sample command test"
        return 0
    fi

    # Test with a safe command
    local test_command="echo 'hello world'"

    if ai-auditor check-command --config-dir "$CONFIG_DIR" "$test_command" >/dev/null 2>&1; then
        success "Sample command validation test passed"
        return 0
    else
        warn "Sample command validation test failed - may need configuration adjustment"
        return 1
    fi
}

# Collect system information for troubleshooting
collect_system_info() {
    debug "Collecting system information..."

    local info_file="/tmp/ai-auditor-system-info.txt"

    {
        echo "AI Command Auditor Installation System Information"
        echo "Generated: $(date)"
        echo "=================================================="
        echo

        echo "System Information:"
        echo "- OS: $(uname -s)"
        echo "- Kernel: $(uname -r)"
        echo "- Architecture: $(uname -m)"
        echo

        echo "Python Environment:"
        if command_exists "$PYTHON_CMD"; then
            echo "- Python: $($PYTHON_CMD --version 2>&1)"
            echo "- Python Path: $(which "$PYTHON_CMD")"
        fi
        if command_exists "$PIP_CMD"; then
            echo "- Pip: $($PIP_CMD --version 2>&1)"
        fi
        if [[ -n "${VIRTUAL_ENV:-}" ]]; then
            echo "- Virtual Environment: $VIRTUAL_ENV"
        fi
        echo

        echo "Git Information:"
        if command_exists "git"; then
            echo "- Git: $(git --version 2>&1)"
            if git rev-parse --git-dir >/dev/null 2>&1; then
                echo "- Git Repository: Yes"
                echo "- Git Directory: $(git rev-parse --git-dir)"
            else
                echo "- Git Repository: No"
            fi
        else
            echo "- Git: Not installed"
        fi
        echo

        echo "AI Command Auditor:"
        if command_exists "ai-auditor"; then
            echo "- CLI Available: Yes"
            echo "- Version: $(ai-auditor --version 2>&1 || echo 'unknown')"
        else
            echo "- CLI Available: No"
        fi
        echo

        echo "Configuration:"
        echo "- Config Directory: $CONFIG_DIR"
        echo "- Config Exists: $(if [[ -d "$CONFIG_DIR" ]]; then echo "Yes"; else echo "No"; fi)"
        echo "- Template Used: $TEMPLATE"
        echo

        echo "Installation Options:"
        echo "- Install Hooks: $INSTALL_HOOKS"
        echo "- Install CI: $INSTALL_CI"
        echo "- System Wide: $SYSTEM_WIDE"
        echo "- Force: $FORCE"
        echo

    } > "$info_file"

    debug "System information saved to: $info_file"
    echo "$info_file"
}

# Generate installation report
generate_installation_report() {
    local tests_passed="$1"
    local total_tests="$2"
    local system_info_file="$3"

    debug "Generating installation report..."

    local report_file="/tmp/ai-auditor-installation-report.txt"

    {
        echo "AI Command Auditor Installation Report"
        echo "Generated: $(date)"
        echo "======================================"
        echo

        echo "Installation Summary:"
        echo "- Status: $(if [[ $tests_passed -eq $total_tests ]]; then echo "SUCCESS"; else echo "PARTIAL"; fi)"
        echo "- Tests Passed: $tests_passed/$total_tests"
        echo "- Configuration: $CONFIG_DIR"
        echo "- Template: $TEMPLATE"
        echo

        if [[ $tests_passed -eq $total_tests ]]; then
            echo "✅ All verification tests passed!"
            echo "Your AI Command Auditor installation is ready to use."
        else
            echo "⚠️  Some verification tests failed."
            echo "Your installation may need additional configuration."
        fi
        echo

        echo "Next Steps:"
        echo "1. Review configuration in: $CONFIG_DIR/"
        echo "2. Test the installation: ai-auditor --version"
        echo "3. Run a command check: ai-auditor check-command \"ls -la\""
        echo "4. View documentation: https://github.com/$GITHUB_REPO"
        echo

        if [[ $tests_passed -ne $total_tests ]]; then
            echo "Troubleshooting:"
            echo "- Check the installation log: $LOG_FILE"
            echo "- Review system information: $system_info_file"
            echo "- Visit: https://github.com/$GITHUB_REPO/issues"
            echo
        fi

        echo "Installation Log: $LOG_FILE"
        echo "System Information: $system_info_file"

    } > "$report_file"

    debug "Installation report saved to: $report_file"
    echo "$report_file"
}

# Provide troubleshooting information
provide_troubleshooting_info() {
    local failed_tests="$1"

    info "Troubleshooting Information:"
    echo

    if [[ " $failed_tests " =~ " package_import " ]]; then
        error "Package Import Failed:"
        echo "  - Check if the package was installed correctly"
        echo "  - Try: $PIP_CMD show ai-command-auditor"
        echo "  - Try: $PYTHON_CMD -c 'import sys; print(sys.path)'"
        echo
    fi

    if [[ " $failed_tests " =~ " cli_functionality " ]]; then
        error "CLI Functionality Failed:"
        echo "  - Check if ai-auditor is in your PATH"
        echo "  - Try: which ai-auditor"
        echo "  - You may need to restart your terminal"
        echo
    fi

    if [[ " $failed_tests " =~ " configuration " ]]; then
        error "Configuration Validation Failed:"
        echo "  - Check configuration files in: $CONFIG_DIR/"
        echo "  - Verify YAML syntax in config files"
        echo "  - Try: ai-auditor validate-setup --config-dir $CONFIG_DIR"
        echo
    fi

    if [[ " $failed_tests " =~ " git_hooks " ]]; then
        error "Git Hooks Failed:"
        echo "  - Check hook files in: .git/hooks/"
        echo "  - Verify hooks are executable: ls -la .git/hooks/"
        echo "  - Try reinstalling with: --force option"
        echo
    fi

    echo "For more help:"
    echo "  - Installation log: $LOG_FILE"
    echo "  - Documentation: https://github.com/$GITHUB_REPO"
    echo "  - Issues: https://github.com/$GITHUB_REPO/issues"
}

verify_installation() {
    show_progress 6 7 "Verifying installation"

    info "Running comprehensive installation verification..."

    # Define all tests
    local tests=(
        "package_import:test_package_import"
        "cli_functionality:test_cli_functionality"
        "configuration:test_configuration_validity"
        "git_hooks:test_git_hooks"
        "sample_command:test_sample_command"
    )

    local total_tests=${#tests[@]}
    local tests_passed=0
    local failed_tests=""

    # Run each test
    for test_def in "${tests[@]}"; do
        local test_name="${test_def%:*}"
        local test_function="${test_def#*:}"

        info "Running $test_name test..."

        if $test_function; then
            ((tests_passed++))
        else
            failed_tests="$failed_tests $test_name"
        fi
    done

    # Collect system information
    local system_info_file
    system_info_file=$(collect_system_info)

    # Generate installation report
    local report_file
    report_file=$(generate_installation_report "$tests_passed" "$total_tests" "$system_info_file")

    # Provide results
    echo
    if [[ $tests_passed -eq $total_tests ]]; then
        success "All verification tests passed! ($tests_passed/$total_tests)"
        info "Installation report: $report_file"
    else
        warn "Some verification tests failed ($tests_passed/$total_tests)"
        provide_troubleshooting_info "$failed_tests"
        info "Installation report: $report_file"
        info "System information: $system_info_file"
    fi

    success "Installation verification completed"
}

# Print success message
print_success_message() {
    show_progress 7 7 "Installation completed"

    if [[ "$QUIET" != true ]]; then
        cat << EOF

╔═══════════════════════════════════════════════════════════╗
║               🎉 Installation Completed! 🎉               ║
╚═══════════════════════════════════════════════════════════╝

AI Command Auditor has been successfully installed!

Next steps:
  1. Review configuration in: $CONFIG_DIR/
  2. Test the installation: ai-auditor --version
  3. Run a command check: ai-auditor check-command "ls -la"

For documentation and examples:
  https://github.com/$GITHUB_REPO

Installation log: $LOG_FILE

EOF
    fi

    success "AI Command Auditor installation completed successfully!"
}

# Main function
main() {
    # Initialize log file
    echo "AI Command Auditor Installation Log - $(date)" > "$LOG_FILE"

    parse_arguments "$@"
    print_banner
    check_prerequisites
    install_package
    setup_configuration

    if [[ "$INSTALL_HOOKS" == true ]]; then
        setup_git_hooks
    fi

    if [[ "$INSTALL_CI" == true ]]; then
        setup_ci_pipeline
    fi

    verify_installation
    print_success_message
}

# Run main function with all arguments
main "$@"
