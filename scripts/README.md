# Scripts Directory

This directory contains all the executable scripts for the AI Command Auditor project, organized by language and functionality.

## Structure

```
scripts/
├── bash/           # Bash shell scripts
│   ├── utils/      # Utility scripts
│   ├── automation/ # Automation scripts  
│   └── monitoring/ # System monitoring scripts
└── python/         # Python modules and scripts
    ├── core/       # Core functionality
    ├── analysis/   # Analysis and metrics
    ├── reporting/  # Report generation
    └── tests/      # Test suite
```

## Usage

### Python Scripts

To run Python scripts, use the module format from the project root:

```bash
# Example: Run a core utility
python -m scripts.python.core.utils

# Example: Run analysis
python -m scripts.python.analysis.command_analyzer

# Example: Generate reports
python -m scripts.python.reporting.report_generator
```

### Bash Scripts

Bash scripts should be made executable and can be run directly:

```bash
# Make scripts executable
chmod +x scripts/bash/**/*.sh

# Run a utility script
./scripts/bash/utils/system-info.sh

# Run a monitoring script
./scripts/bash/monitoring/performance-monitor.sh
```

## Development Guidelines

1. **Python Scripts**: Follow PEP 8 and the project's coding standards defined in `.cursor/rules/`
2. **Bash Scripts**: Use the template structure defined in the Cursor rules
3. **Documentation**: Include docstrings and comments explaining functionality
4. **Testing**: Write tests for all new functionality in the `tests/` directory
5. **Error Handling**: Implement proper error handling and logging

## Adding New Scripts

### Python Module
1. Create the module file in the appropriate subdirectory
2. Add necessary imports to the `__init__.py` file
3. Write corresponding tests
4. Update documentation

### Bash Script
1. Use the standard template from `.cursor/rules/cursor_rules.md`
2. Make the script executable: `chmod +x script.sh`
3. Add appropriate error handling and logging
4. Test thoroughly before committing

## Dependencies

- **Python**: See `requirements.txt` and `requirements-dev.txt`
- **Bash**: Standard bash tools plus those installed in the dev container
- **System Tools**: Various system monitoring and analysis tools

## Testing

Run the Python test suite:
```bash
pytest scripts/python/tests/
```

Test bash scripts manually or with bats (Bash Automated Testing System) if configured. 