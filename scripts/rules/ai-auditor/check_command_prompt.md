# Ruleset for the AI Command Auditor

## Forbidden commands and command flags

- Instruction: Never use "--force" or "--no-verify" in git commands.
  - Reason: "--force" breaks the CI/CD workflow. This wastes time.
  - Alternative:
    - Always fix all issues before pushing to remote.
    - Ensure that all tests pass before pushing

- Instruction: Some `gh` commands run interactivly. Append " | cat" to run them non-interactively.
  - Reason: Interactive commands break the AI agent workflow.
  - Alternatives: Append " \| cat" to make it non-interactively.
