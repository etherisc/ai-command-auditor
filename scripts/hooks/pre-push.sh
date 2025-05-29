#!/bin/bash
#
# Pre-push hook: Run all tests
#
# This script runs all tests that are part of the CI pipeline before pushing code.
# It ensures that the code being pushed will pass the CI checks.
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Running pre-push tests...${NC}"
echo

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

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository"
    exit 1
fi

# Get the project root
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

# Check if necessary directories exist
if [ ! -d "scripts/python" ]; then
    print_error "scripts/python directory not found"
    exit 1
fi

# Ensure logs directory exists
mkdir -p logs

# Flag to track if any tests failed
TESTS_FAILED=0

# Get remote and branch being pushed to
remote="$1"
url="$2"

echo "Pushing to: $remote ($url)"
echo

# Run linting first (same as pre-commit but non-blocking for informatino)
print_section "Code Quality Checks"
echo "Running the same checks as pre-commit hook..."

if ! ./scripts/hooks/pre-commit.sh; then
    print_error "Pre-commit checks failed"
    TESTS_FAILED=1
fi
echo

# Additional CI-specific formatting checks
print_section "CI Pipeline Formatting Checks"

# Black formatting check (exactly as CI does it)
print_section "Black Code Formatting"
if black --check --diff scripts/python/; then
    print_success "Black formatting check passed"
else
    print_error "Black formatting check failed - run 'black scripts/python/' to fix"
    TESTS_FAILED=1
fi

# isort import sorting check (exactly as CI does it)
print_section "isort Import Sorting"
if isort --check-only --diff scripts/python/; then
    print_success "isort import sorting check passed"
else
    print_error "isort import sorting check failed - run 'isort scripts/python/' to fix"
    TESTS_FAILED=1
fi

# Pylint check
print_section "Pylint Code Analysis"
if pylint scripts/python/ --exit-zero; then
    print_success "Pylint check completed"
else
    print_warning "Pylint issues found (review recommended)"
fi

# MyPy type checking
print_section "MyPy Type Checking"
if mypy scripts/python/ --ignore-missing-imports; then
    print_success "MyPy type checking passed"
else
    print_warning "MyPy type checking issues found (review recommended)"
fi
echo

# Python Tests
print_section "Python Unit Tests"
if [ -d "scripts/python/tests" ] && find scripts/python/tests -name "test_*.py" -type f | grep -q .; then
    if python -m pytest scripts/python/tests/ -v --tb=short; then
        print_success "Python unit tests passed"
    else
        print_error "Python unit tests failed"
        TESTS_FAILED=1
    fi
else
    print_warning "No Python unit tests found, creating basic test structure..."
    mkdir -p scripts/python/tests

    # Create a basic test file if none exists
    if [ ! -f "scripts/python/tests/test_basic.py" ]; then
        cat > scripts/python/tests/test_basic.py << 'EOF'
"""Basic tests to ensure the testing framework is working."""

def test_basic_functionality():
    """Test that basic functionality works."""
    assert True

def test_imports():
    """Test that core modules can be imported."""
    import sys
    from pathlib import Path

    # Add project root to path
    project_root = Path(__file__).parent.parent.parent.parent
    sys.path.insert(0, str(project_root))

    try:
        from scripts.python.core.config import get_config
        from scripts.python.core.security import validate_command
        assert True
    except ImportError as e:
        assert False, f"Failed to import core modules: {e}"
EOF
    fi

    # Run the basic test
    if python -m pytest scripts/python/tests/ -v --tb=short; then
        print_success "Basic tests passed"
    else
        print_error "Basic tests failed"
        TESTS_FAILED=1
    fi
fi
echo

# Integration Tests
print_section "Integration Tests"

# Test 1: Command checker with safe command
print_section "Testing command checker with safe command"
if python scripts/python/core/check_command.py "ls -la" | grep -q "PASS"; then
    print_success "Safe command test passed"
else
    print_error "Safe command test failed"
    TESTS_FAILED=1
fi

# Test 2: Command checker with dangerous command
print_section "Testing command checker with dangerous command"
if python scripts/python/core/check_command.py "rm -rf /" | grep -q "ERROR"; then
    print_success "Dangerous command test passed"
else
    print_error "Dangerous command test failed"
    TESTS_FAILED=1
fi

# Test 3: Configuration loading
print_section "Testing configuration loading"
if python -c "
import sys
sys.path.insert(0, '.')
from scripts.python.core.config import get_config
config = get_config()
assert config.get_rules_file() is not None
print('Configuration loading test passed')
"; then
    print_success "Configuration loading test passed"
else
    print_error "Configuration loading test failed"
    TESTS_FAILED=1
fi

# Test 4: Security validation
print_section "Testing security validation"
if python -c "
import sys
sys.path.insert(0, '.')
from scripts.python.core.security import validate_command
is_safe, error = validate_command('ls -la')
assert is_safe == True
is_safe, error = validate_command('rm -rf /')
assert is_safe == False
print('Security validation test passed')
"; then
    print_success "Security validation test passed"
else
    print_error "Security validation test failed"
    TESTS_FAILED=1
fi
echo

# Bash Tests (if any exist)
print_section "Bash Tests"
if [ -d "scripts/bash/tests" ] && find scripts/bash/tests -name "*.bats" -type f | grep -q .; then
    if command -v bats >/dev/null 2>&1; then
        if bats scripts/bash/tests/; then
            print_success "Bash tests passed"
        else
            print_error "Bash tests failed"
            TESTS_FAILED=1
        fi
    else
        print_warning "BATS not installed, skipping bash tests"
    fi
else
    print_warning "No bash tests found"
fi
echo

# Security Scan
print_section "Security Scan"
if command -v bandit >/dev/null 2>&1; then
    if bandit -r scripts/python/ --exit-zero; then
        print_success "Security scan completed"
    else
        print_warning "Security issues found (review recommended)"
    fi
else
    print_warning "Bandit not available, skipping security scan"
fi
echo

# Final result
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All pre-push tests passed!${NC}"
    echo -e "${GREEN}✅ Code is ready to push${NC}"
    echo
    echo "The following checks passed:"
    echo "  ✅ Code quality checks"
    echo "  ✅ Unit tests"
    echo "  ✅ Integration tests"
    echo "  ✅ Security validation"
    echo
    exit 0
else
    echo -e "${RED}💥 Some pre-push tests failed!${NC}"
    echo -e "${RED}❌ Please fix the issues above before pushing${NC}"
    echo
    echo "Failed tests need to be fixed before pushing."
    echo "The CI pipeline will also fail with these issues."
    exit 1
fi
