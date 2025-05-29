#!/usr/bin/env python3
"""
Setup script for AI Command Auditor package.
"""

from setuptools import setup, find_packages
import pathlib

# Read the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")


# Read requirements
def read_requirements(filename):
    """Read requirements from a file."""
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="ai-command-auditor",
    version="1.0.0",
    author="Etherisc",
    author_email="dev@etherisc.com",
    description="AI-powered command auditing and security validation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/etherisc/ai-command-auditor",
    project_urls={
        "Bug Reports": "https://github.com/etherisc/ai-command-auditor/issues",
        "Source": "https://github.com/etherisc/ai-command-auditor",
        "Documentation": "https://etherisc.github.io/ai-command-auditor",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
    },
    entry_points={
        "console_scripts": [
            "ai-auditor=ai_command_auditor.cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ai_command_auditor": [
            "templates/**/*",
            "templates/**/**/*",
        ],
    },
    keywords="security, command-validation, ai, devops, git-hooks",
    zip_safe=False,
)
