"""
Enhanced template engine for AI Command Auditor.

This module provides advanced template processing capabilities including
variable substitution, template inheritance, and validation.

Author: Etherisc
Date: 2024
Version: 1.0
"""

import re
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from .config import AuditorConfig


class TemplateEngine:
    """Enhanced template engine with variable substitution and inheritance."""

    def __init__(self, config: Optional[AuditorConfig] = None):
        """
        Initialize the template engine.

        Args:
            config: Optional configuration instance
        """
        self.config = config or AuditorConfig()
        self.variables: Dict[str, Any] = {}
        self.template_dir = Path(__file__).parent.parent / "templates"

    def set_variables(self, variables: Dict[str, Any]) -> None:
        """
        Set template variables for substitution.

        Args:
            variables: Dictionary of variables to use in templates
        """
        self.variables.update(variables)

    def get_default_variables(
        self,
        template_type: str,
        project_name: str = "project",
        environment: str = "development",
        security_level: str = "standard",
    ) -> Dict[str, Any]:
        """
        Get default variable values for a template type.

        Args:
            template_type: Type of template (python, node, rust, etc.)
            project_name: Name of the project
            environment: Environment type (development, staging, production)
            security_level: Security level (basic, standard, strict)

        Returns:
            Dictionary of default variables
        """
        defaults = {
            # Project information
            "template_type": template_type,
            "project_name": project_name,
            "environment": environment,
            "security_level": security_level,
            "team_config": "",
            # AI configuration
            "ai_model": "gpt-4o",
            "ai_timeout": 30,
            "ai_max_retries": 3,
            "ai_temperature": 0.1,
            "ai_max_tokens": 1000,
            # Security configuration
            "security_max_command_length": 1000,
            "security_allow_multiline": False,
            "security_strict_mode": False,
            "security_blocked_commands": "[]",
            # Logging configuration
            "logging_level": "INFO",
            "logging_file": ".ai-auditor/logs/auditor.log",
            "logging_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            # Validation configuration
            "validation_enable_ai_check": True,
            "validation_enable_rule_check": True,
            "validation_require_context": False,
            "validation_cache_results": True,
            # Integration configuration
            "integration_git_hooks": True,
            "integration_ci_integration": True,
            "integration_pre_commit": True,
            "integration_pre_push": True,
            # Policy configuration
            "policy_block_on_critical": True,
            "policy_warn_on_high": True,
            "policy_log_all_matches": True,
            "policy_require_approval_for": '["critical", "high"]',
            # Context configuration
            "context_include_user_history": False,
            "context_include_file_context": True,
            # Template description
            "template_description": self._get_template_description(template_type),
        }

        # Environment-specific overrides
        if environment == "production":
            defaults.update(
                {
                    "security_strict_mode": True,
                    "security_max_command_length": 500,
                    "logging_level": "WARNING",
                    "validation_require_context": True,
                    "ai_temperature": 0.0,  # More deterministic for production
                    "policy_block_on_critical": True,
                    "context_include_user_history": False,
                }
            )
        elif environment == "staging":
            defaults.update(
                {
                    "security_strict_mode": False,
                    "logging_level": "INFO",
                    "validation_require_context": True,
                    "ai_temperature": 0.05,
                }
            )
        elif environment == "development":
            defaults.update(
                {
                    "security_strict_mode": False,
                    "logging_level": "DEBUG",
                    "validation_require_context": False,
                    "ai_temperature": 0.1,
                    "context_include_user_history": True,
                }
            )

        # Security level overrides
        if security_level == "strict":
            defaults.update(
                {
                    "security_strict_mode": True,
                    "security_max_command_length": 300,
                    "policy_block_on_critical": True,
                    "policy_warn_on_high": True,
                    "validation_require_context": True,
                    "ai_temperature": 0.0,
                }
            )
        elif security_level == "basic":
            defaults.update(
                {
                    "security_strict_mode": False,
                    "security_max_command_length": 2000,
                    "policy_block_on_critical": False,
                    "policy_warn_on_high": False,
                    "validation_require_context": False,
                }
            )

        # Template-specific overrides
        if template_type == "python":
            defaults.update(
                {
                    "ai_model": "gpt-4o",
                    "security_blocked_commands": '["eval", "exec", "__import__"]',
                    "validation_require_context": True,
                }
            )
        elif template_type == "node":
            defaults.update(
                {
                    "security_blocked_commands": '["eval", "Function", "vm.runInThisContext"]',
                    "validation_require_context": True,
                }
            )
        elif template_type == "rust":
            defaults.update(
                {
                    "security_max_command_length": 500,
                    "security_blocked_commands": '["unsafe", "transmute"]',
                }
            )
        elif template_type == "security":
            defaults.update(
                {
                    "security_strict_mode": True,
                    "security_max_command_length": 500,
                    "policy_block_on_critical": True,
                    "validation_require_context": True,
                    "ai_temperature": 0.0,  # More deterministic for security
                }
            )
        elif template_type == "general":
            # Use defaults as-is
            pass

        return defaults

    def _get_template_description(self, template_type: str) -> str:
        """Get description for a template type."""
        descriptions = {
            "python": "Python-specific security rules, virtual environment detection, and package management integration",
            "node": "Node.js/npm security scanning, framework-specific rules, and package.json validation",
            "rust": "Rust-specific security patterns, Cargo.toml validation, and memory safety checks",
            "security": "Stricter validation rules, compliance framework integration, and advanced threat detection",
            "general": "Language-agnostic rules, universal security patterns, and basic CI/CD integration",
            "base": "Foundation template providing core functionality for all other templates",
        }
        return descriptions.get(
            template_type, f"Configuration template for {template_type} projects"
        )

    def load_template(self, template_type: str, file_name: str) -> str:
        """
        Load a template file with inheritance support.

        Args:
            template_type: Type of template (python, node, rust, etc.)
            file_name: Name of the template file to load

        Returns:
            Template content as string

        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        # First try specific template type
        template_path = self.template_dir / template_type / file_name

        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()

        # Fall back to base template
        base_path = self.template_dir / "base" / file_name
        if base_path.exists():
            with open(base_path, "r", encoding="utf-8") as f:
                return f.read()

        raise FileNotFoundError(
            f"Template '{file_name}' not found for type '{template_type}'"
        )

    def render_template(
        self, template: str, variables: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Render template with variable substitution.

        Args:
            template: Template string to render
            variables: Variables to use for substitution (optional)

        Returns:
            Rendered template string
        """
        # Merge provided variables with instance variables
        render_vars = self.variables.copy()
        if variables:
            render_vars.update(variables)

        # Simple variable substitution using ${variable} syntax
        def substitute_variable(match):
            var_name = match.group(1)
            value = render_vars.get(
                var_name, f"${{{var_name}}}"
            )  # Keep original if not found
            return str(value)

        # Replace ${variable} patterns
        result = re.sub(r"\$\{([^}]+)\}", substitute_variable, template)

        return result

    def validate_output(self, content: str, file_type: str) -> Tuple[bool, List[str]]:
        """
        Validate rendered template content.

        Args:
            content: Rendered template content
            file_type: Type of file (yml, yaml, md, etc.)

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors: List[str] = []

        # YAML validation for config files
        if file_type.lower() in ["yml", "yaml"]:
            try:
                yaml.safe_load(content)
            except yaml.YAMLError as e:
                errors.append(f"YAML syntax error: {e}")

        # Check for unresolved variables
        unresolved = re.findall(r"\$\{([^}]+)\}", content)
        if unresolved:
            errors.append(f"Unresolved variables: {', '.join(unresolved)}")

        # Basic content validation
        if not content.strip():
            errors.append("Template produced empty content")

        return len(errors) == 0, errors

    def apply_template(
        self,
        project_dir: Path,
        template_type: str,
        project_name: str = "project",
        custom_variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Apply complete template set to project directory.

        Args:
            project_dir: Directory to create configuration in
            template_type: Type of template to apply
            project_name: Name of the project
            custom_variables: Custom variables to override defaults

        Returns:
            Dictionary containing results of template application
        """
        # Prepare variables
        variables = self.get_default_variables(template_type, project_name)
        if custom_variables:
            variables.update(custom_variables)

        self.set_variables(variables)

        # Create directory structure
        config_dir = project_dir / ".ai-auditor"
        directories = [
            config_dir / "config" / "rules",
            config_dir / "config" / "prompts",
            config_dir / "hooks",
            config_dir / "workflows",
            config_dir / "logs",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        # Template files to process
        template_files = [
            ("auditor.yml.template", "config/auditor.yml"),
            ("security-rules.yml.template", "config/rules/security-rules.yml"),
            ("openai-prompts.yml.template", "config/prompts/openai-prompts.yml"),
            ("README.md.template", "README.md"),
        ]

        results = {
            "template_type": template_type,
            "project_name": project_name,
            "files_created": [],
            "files_failed": [],
            "variables_used": variables,
            "validation_errors": [],
        }

        # Process each template file
        for template_file, output_file in template_files:
            try:
                # Load and render template
                template_content = self.load_template(template_type, template_file)
                rendered_content = self.render_template(template_content)

                # Validate rendered content
                file_ext = Path(output_file).suffix.lstrip(".")
                is_valid, validation_errors = self.validate_output(
                    rendered_content, file_ext
                )

                if not is_valid:
                    results["files_failed"].append(
                        {
                            "file": output_file,
                            "template": template_file,
                            "errors": validation_errors,
                        }
                    )
                    results["validation_errors"].extend(validation_errors)
                    continue

                # Write rendered content
                output_path = config_dir / output_file
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(rendered_content)

                results["files_created"].append(
                    {
                        "file": str(output_path),
                        "template": template_file,
                        "size": len(rendered_content),
                    }
                )

            except Exception as e:
                results["files_failed"].append(
                    {"file": output_file, "template": template_file, "errors": [str(e)]}
                )

        return results

    def get_available_templates(self) -> List[str]:
        """
        Get list of available template types.

        Returns:
            List of template names
        """
        templates = []
        for item in self.template_dir.iterdir():
            if item.is_dir() and not item.name.startswith("__"):
                # Verify template has required files
                required_files = [
                    "auditor.yml.template",
                    "security-rules.yml.template",
                    "openai-prompts.yml.template",
                ]
                if all((item / f).exists() for f in required_files):
                    templates.append(item.name)
        return sorted(templates)

    def validate_template_structure(self, template_type: str) -> Tuple[bool, List[str]]:
        """
        Validate that a template has the required structure.

        Args:
            template_type: Name of template to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors: List[str] = []
        template_dir = self.template_dir / template_type

        if not template_dir.exists():
            errors.append(f"Template directory '{template_type}' does not exist")
            return False, errors

        # Check required files
        required_files = [
            "auditor.yml.template",
            "security-rules.yml.template",
            "openai-prompts.yml.template",
        ]

        for file_name in required_files:
            file_path = template_dir / file_name
            if not file_path.exists():
                errors.append(f"Required template file missing: {file_name}")
            else:
                # Try to load and validate syntax
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Basic template syntax validation
                    if not content.strip():
                        errors.append(f"Template file is empty: {file_name}")

                except Exception as e:
                    errors.append(f"Cannot read template file {file_name}: {e}")

        return len(errors) == 0, errors

    def validate_all_templates(self) -> Dict[str, Any]:
        """
        Validate all available templates.

        Returns:
            Dictionary containing validation results for all templates
        """
        results: Dict[str, Any] = {
            "templates_tested": [],
            "templates_passed": [],
            "templates_failed": [],
            "validation_errors": [],
            "summary": {},
        }

        available_templates = self.get_available_templates()

        for template_type in available_templates:
            print(f"Validating template: {template_type}")

            # Test template structure
            is_valid, errors = self.validate_template_structure(template_type)

            template_result: Dict[str, Any] = {
                "template": template_type,
                "structure_valid": is_valid,
                "structure_errors": errors,
                "render_test_passed": False,
                "render_errors": [],
            }

            results["templates_tested"].append(template_type)

            if is_valid:
                # Test template rendering
                try:
                    test_variables = self.get_default_variables(
                        template_type, "test-project"
                    )

                    # Test each template file
                    template_files = [
                        "auditor.yml.template",
                        "security-rules.yml.template",
                        "openai-prompts.yml.template",
                        "README.md.template",
                    ]

                    render_success = True
                    for template_file in template_files:
                        try:
                            template_content = self.load_template(
                                template_type, template_file
                            )
                            rendered_content = self.render_template(
                                template_content, test_variables
                            )

                            # Validate rendered content
                            file_ext = (
                                Path(template_file)
                                .suffix.replace(".template", "")
                                .lstrip(".")
                            )
                            content_valid, content_errors = self.validate_output(
                                rendered_content, file_ext
                            )

                            if not content_valid:
                                template_result["render_errors"].extend(content_errors)
                                render_success = False

                        except Exception as e:
                            template_result["render_errors"].append(
                                f"Failed to render {template_file}: {e}"
                            )
                            render_success = False

                    template_result["render_test_passed"] = render_success

                except Exception as e:
                    template_result["render_errors"].append(
                        f"Template rendering failed: {e}"
                    )

            # Categorize results
            if (
                template_result["structure_valid"]
                and template_result["render_test_passed"]
            ):
                results["templates_passed"].append(template_result)
            else:
                results["templates_failed"].append(template_result)
                results["validation_errors"].extend(template_result["structure_errors"])
                results["validation_errors"].extend(template_result["render_errors"])

        # Generate summary
        results["summary"] = {
            "total_templates": len(available_templates),
            "passed": len(results["templates_passed"]),
            "failed": len(results["templates_failed"]),
            "success_rate": (
                len(results["templates_passed"]) / len(available_templates)
                if available_templates
                else 0
            ),
        }

        return results

    def test_template_with_environments(self, template_type: str) -> Dict[str, Any]:
        """
        Test a template with different environment and security level combinations.

        Args:
            template_type: Name of template to test

        Returns:
            Dictionary containing test results
        """
        results = {
            "template": template_type,
            "environment_tests": [],
            "security_level_tests": [],
            "combination_tests": [],
            "all_passed": True,
        }

        environments = ["development", "staging", "production"]
        security_levels = ["basic", "standard", "strict"]

        # Test each environment
        for env in environments:
            try:
                variables = self.get_default_variables(
                    template_type, "test-project", env, "standard"
                )
                template_content = self.load_template(
                    template_type, "auditor.yml.template"
                )
                rendered_content = self.render_template(template_content, variables)

                is_valid, errors = self.validate_output(rendered_content, "yml")

                results["environment_tests"].append(
                    {"environment": env, "passed": is_valid, "errors": errors}
                )

                if not is_valid:
                    results["all_passed"] = False

            except Exception as e:
                results["environment_tests"].append(
                    {"environment": env, "passed": False, "errors": [str(e)]}
                )
                results["all_passed"] = False

        # Test each security level
        for sec_level in security_levels:
            try:
                variables = self.get_default_variables(
                    template_type, "test-project", "development", sec_level
                )
                template_content = self.load_template(
                    template_type, "auditor.yml.template"
                )
                rendered_content = self.render_template(template_content, variables)

                is_valid, errors = self.validate_output(rendered_content, "yml")

                results["security_level_tests"].append(
                    {"security_level": sec_level, "passed": is_valid, "errors": errors}
                )

                if not is_valid:
                    results["all_passed"] = False

            except Exception as e:
                results["security_level_tests"].append(
                    {"security_level": sec_level, "passed": False, "errors": [str(e)]}
                )
                results["all_passed"] = False

        # Test combinations
        for env in environments:
            for sec_level in security_levels:
                try:
                    variables = self.get_default_variables(
                        template_type, "test-project", env, sec_level
                    )
                    template_content = self.load_template(
                        template_type, "auditor.yml.template"
                    )
                    rendered_content = self.render_template(template_content, variables)

                    is_valid, errors = self.validate_output(rendered_content, "yml")

                    results["combination_tests"].append(
                        {
                            "environment": env,
                            "security_level": sec_level,
                            "passed": is_valid,
                            "errors": errors,
                        }
                    )

                    if not is_valid:
                        results["all_passed"] = False

                except Exception as e:
                    results["combination_tests"].append(
                        {
                            "environment": env,
                            "security_level": sec_level,
                            "passed": False,
                            "errors": [str(e)],
                        }
                    )
                    results["all_passed"] = False

        return results
