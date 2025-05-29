# AI Command Auditor

A comprehensive collection of bash and python scripts for auditing, analyzing, and monitoring AI command interactions and system behaviors.

## 🎯 Project Overview

This repository provides tools and scripts to help developers, system administrators, and AI practitioners monitor, audit, and analyze AI command executions, system interactions, and performance metrics. The project is designed with modern development practices including containerized development environments and organized code structure.

## ✨ Features

- **Command Auditing**: Track and analyze AI command executions
- **Performance Monitoring**: Monitor system resources during AI operations
- **Security Analysis**: Audit AI interactions for security compliance
- **Reporting Tools**: Generate comprehensive reports and analytics
- **Automation Scripts**: Automate common auditing and monitoring tasks

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- VS Code with Dev Containers extension
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-command-auditor
   ```

2. **Open in Development Container**
   - Open the project in VS Code
   - When prompted, click "Reopen in Container" or use Command Palette: `Dev Containers: Reopen in Container`
   - Wait for the container to build (first time may take a few minutes)

3. **Verify Installation**
   ```bash
   python --version
   gh --version
   bash --version
   ```

## 📁 Project Structure

```
ai-command-auditor/
├── docs/                   # Documentation
│   ├── planning/          # Project planning documents
│   ├── api/              # API documentation
│   └── user-guides/      # User guides and tutorials
├── scripts/              # Main script collection
│   ├── bash/            # Bash scripts
│   │   ├── utils/       # Utility scripts
│   │   ├── automation/  # Automation scripts
│   │   └── monitoring/  # Monitoring scripts
│   └── python/          # Python scripts
│       ├── core/        # Core functionality
│       ├── analysis/    # Analysis tools
│       ├── reporting/   # Reporting tools
│       └── tests/       # Test scripts
├── config/              # Configuration files
├── data/               # Data storage
│   ├── input/          # Input data
│   ├── output/         # Output results
│   └── samples/        # Sample data
├── templates/          # Script templates
└── tools/             # Development tools
```

## 🛠️ Usage

### Running Scripts

**Python Scripts:**
```bash
# From the container terminal
cd scripts/python
python -m core.script_name
```

**Bash Scripts:**
```bash
# From the container terminal
cd scripts/bash
./script_name.sh
```

### Configuration

Configuration files are stored in the `config/` directory. Copy template files and modify according to your environment:

```bash
cp config/template.conf config/local.conf
# Edit local.conf with your settings
```

## 🧪 Testing

Run the test suite:
```bash
cd scripts/python
python -m pytest tests/
```

## 📚 Documentation

- **[Project Plan](docs/planning/project_plan.md)** - Detailed project setup and implementation plan
- **[API Documentation](docs/api/)** - API reference and examples
- **[User Guides](docs/user-guides/)** - Step-by-step tutorials and guides

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes in the development container
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- All development should be done within the dev container
- Follow the established coding standards (see `.cursor/rules/`)
- Write tests for new functionality
- Update documentation as needed
- Use meaningful commit messages

## 📋 Requirements

### System Requirements
- Docker 20.10+
- VS Code with Dev Containers extension
- Git 2.20+

### Container Includes
- Python 3.11+
- GitHub CLI
- Essential development tools
- Pre-configured VS Code extensions

## 🐛 Troubleshooting

### Common Issues

**Container fails to build:**
- Ensure Docker is running
- Check Docker daemon is accessible
- Try rebuilding: `Dev Containers: Rebuild Container`

**Scripts not executable:**
```bash
chmod +x scripts/bash/*.sh
```

**Python module not found:**
```bash
export PYTHONPATH="${PYTHONPATH}:/workspaces/ai-command-auditor/scripts/python"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who help improve this project
- Built with modern development practices and container-first approach
- Inspired by the need for better AI system monitoring and auditing

## 📞 Support

- Create an issue for bug reports or feature requests
- Check the documentation in the `docs/` folder
- Review existing issues before creating new ones

---

**Happy Auditing! 🔍✨** 