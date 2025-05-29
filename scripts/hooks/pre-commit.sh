#!/bin/bash
#
# Pre-commit hook: Run linting checks
#
# This script runs all linting checks that should pass before committing code.
# It follows the same checks as the CI pipeline lint stage.
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Running pre-commit checks...${NC}"
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

# Check if Python code exists
PYTHON_FILES=$(find scripts/python -name "*.py" -type f 2>/dev/null | wc -l)
BASH_FILES=$(find scripts/bash -name "*.sh" -type f 2>/dev/null | wc -l)

echo "Found $PYTHON_FILES Python files and $BASH_FILES Bash files to check"
echo

# Flag to track if any checks failed
CHECKS_FAILED=0

# Python linting
if [ "$PYTHON_FILES" -gt 0 ]; then
    print_section "Python Code Formatting (Black)"
    if black --check --diff scripts/python/; then
        print_success "Black formatting check passed"
    else
        print_error "Black formatting check failed"
        echo "Run: black scripts/python/ to fix formatting issues"
        CHECKS_FAILED=1
    fi
    echo

    print_section "Python Import Sorting (isort)"
    if isort --check-only --diff --profile=black scripts/python/; then
        print_success "isort import sorting check passed"
    else
        print_error "isort check failed"
        echo "Run: isort --profile=black scripts/python/ to fix import sorting"
        CHECKS_FAILED=1
    fi
    echo

    print_section "Python Code Quality (Pylint)"
    if pylint scripts/python/ --exit-zero --reports=no; then
        print_success "Pylint check completed"
    else
        print_warning "Pylint found issues (not blocking commit)"
    fi
    echo

    print_section "Python Type Checking (MyPy)"
    if mypy scripts/python/ --ignore-missing-imports --no-strict-optional; then
        print_success "MyPy type checking passed"
    else
        print_warning "MyPy found type issues (not blocking commit)"
    fi
    echo
else
    print_warning "No Python files found to lint"
fi

# Bash linting
if [ "$BASH_FILES" -gt 0 ]; then
    print_section "Bash Linting (ShellCheck)"
    if command -v shellcheck >/dev/null 2>&1; then
        if find scripts/bash -name "*.sh" -type f -exec shellcheck {} \;; then
            print_success "ShellCheck passed"
        else
            print_error "ShellCheck found issues"
            CHECKS_FAILED=1
        fi
    else
        print_warning "ShellCheck not installed, skipping bash linting"
    fi
    echo
else
    print_warning "No Bash files found to lint"
fi

# Security checks
print_section "Security Checks (Bandit)"
if command -v bandit >/dev/null 2>&1 && [ "$PYTHON_FILES" -gt 0 ]; then
    if bandit -r scripts/python/ --exit-zero; then
        print_success "Bandit security scan completed"
    else
        print_warning "Bandit found security issues (review recommended)"
    fi
else
    print_warning "Bandit not available or no Python files to scan"
fi
echo

# Final result
if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All pre-commit checks passed!${NC}"
    echo -e "${GREEN}✅ Code is ready to commit${NC}"
    exit 0
else
    echo -e "${RED}💥 Some pre-commit checks failed!${NC}"
    echo -e "${RED}❌ Please fix the issues above before committing${NC}"
    echo
    echo "Quick fixes:"
    echo "  - Format Python code: black scripts/python/"
    echo "  - Sort imports: isort --profile=black scripts/python/"
    echo "  - Fix bash issues: follow shellcheck suggestions"
    exit 1
fi
