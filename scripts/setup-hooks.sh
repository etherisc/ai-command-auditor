#!/bin/bash
#
# Setup script for Git hooks
#
# This script installs pre-commit hooks and sets up pre-push hooks
# for the AI Command Auditor project.
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo -e "${BLUE}▶ $1${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo -e "${BLUE}🔧 Setting up Git hooks for AI Command Auditor${NC}"
echo

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository"
    exit 1
fi

# Get the project root
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

# Check if Python is available
if ! command -v python3 >/dev/null 2>&1; then
    print_error "Python 3 is required but not found"
    exit 1
fi

# Install development dependencies
print_section "Installing development dependencies"
if [ -f "requirements-dev.txt" ]; then
    if python3 -m pip install -r requirements-dev.txt; then
        print_success "Development dependencies installed"
    else
        print_error "Failed to install development dependencies"
        exit 1
    fi
else
    print_warning "requirements-dev.txt not found, installing pre-commit manually"
    python3 -m pip install pre-commit
fi
echo

# Install pre-commit hooks
print_section "Installing pre-commit hooks"
if pre-commit install; then
    print_success "Pre-commit hooks installed"
else
    print_error "Failed to install pre-commit hooks"
    exit 1
fi
echo

# Install pre-commit for commit-msg hook (optional)
print_section "Installing commit-msg hooks"
if pre-commit install --hook-type commit-msg; then
    print_success "Commit-msg hooks installed"
else
    print_warning "Failed to install commit-msg hooks (optional)"
fi
echo

# Set up pre-push hook
print_section "Setting up pre-push hook"
GIT_HOOKS_DIR="$(git rev-parse --git-dir)/hooks"
PRE_PUSH_HOOK="$GIT_HOOKS_DIR/pre-push"

# Create the pre-push hook
cat > "$PRE_PUSH_HOOK" << 'EOF'
#!/bin/bash
#
# Pre-push hook: Run comprehensive tests
#
# This hook runs all tests that should pass before pushing code.
#

# Get the project root
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

# Run our custom pre-push script
exec ./scripts/hooks/pre-push.sh "$@"
EOF

# Make the pre-push hook executable
chmod +x "$PRE_PUSH_HOOK"
print_success "Pre-push hook installed"
echo

# Make sure our hook scripts are executable
print_section "Making hook scripts executable"
chmod +x scripts/hooks/*.sh
print_success "Hook scripts are executable"
echo

# Test the installation
print_section "Testing hook installation"

# Test pre-commit
if pre-commit --version >/dev/null 2>&1; then
    print_success "Pre-commit is working"
else
    print_error "Pre-commit test failed"
    exit 1
fi

# Test our scripts
if [ -x "scripts/hooks/pre-commit.sh" ]; then
    print_success "Pre-commit script is executable"
else
    print_error "Pre-commit script is not executable"
    exit 1
fi

if [ -x "scripts/hooks/pre-push.sh" ]; then
    print_success "Pre-push script is executable"
else
    print_error "Pre-push script is not executable"
    exit 1
fi

echo
echo -e "${GREEN}🎉 Git hooks setup completed successfully!${NC}"
echo
echo "What's been set up:"
echo "  ✅ Pre-commit hooks (via pre-commit tool)"
echo "     - Code formatting (Black, isort)"
echo "     - Linting (Pylint, MyPy, ShellCheck)"
echo "     - Security scanning (Bandit)"
echo "     - YAML/Markdown linting"
echo "     - File checks (trailing whitespace, etc.)"
echo
echo "  ✅ Pre-push hooks (via Git native hooks)"
echo "     - All linting checks"
echo "     - Unit tests"
echo "     - Integration tests"
echo "     - Security validation"
echo
echo "Usage:"
echo "  • Pre-commit hooks run automatically on 'git commit'"
echo "  • Pre-push hooks run automatically on 'git push'"
echo "  • To run pre-commit manually: pre-commit run --all-files"
echo "  • To run pre-push tests manually: ./scripts/hooks/pre-push.sh origin https://github.com/user/repo"
echo
echo "To bypass hooks (not recommended):"
echo "  • Skip pre-commit: git commit --no-verify"
echo "  • Skip pre-push: git push --no-verify"
echo
print_success "Ready for development!"
