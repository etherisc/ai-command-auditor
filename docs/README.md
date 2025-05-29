# Documentation

This directory contains all documentation for the AI Command Auditor project.

## Structure

```
docs/
├── planning/       # Project planning and design documents
├── api/           # API documentation and references
├── user-guides/   # User guides and tutorials
└── README.md      # This file
```

## Documentation Types

### Planning Documentation (`planning/`)
- Project planning documents
- Architecture decisions
- Design specifications
- Development roadmaps

### API Documentation (`api/`)
- Python module documentation
- Function and class references
- Usage examples
- Integration guides

### User Guides (`user-guides/`)
- Installation instructions
- Usage tutorials
- Best practices
- Troubleshooting guides
- FAQ

## Contributing to Documentation

1. Use Markdown format for all documentation
2. Follow consistent formatting and structure
3. Include code examples where appropriate
4. Keep documentation up-to-date with code changes
5. Use clear, concise language

## Building Documentation

For API documentation, use Sphinx:
```bash
cd docs/api
sphinx-build -b html . _build/html
```

## Documentation Standards

- Use descriptive titles and headers
- Include table of contents for longer documents
- Add cross-references between related documents
- Include screenshots and diagrams where helpful
- Keep examples current and tested 