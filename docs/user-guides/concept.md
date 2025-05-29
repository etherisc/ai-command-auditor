# Shell Command Checker – Reference Summary

## Purpose

This project aims to protect against dangerous, incorrect, or policy-breaking shell commands issued by junior developers by intercepting and validating each command in an interactive shell session.

## Architecture Overview

### 1. Shell Hook

A `command_checker()` function is added via `trap DEBUG` in `.bashrc`:

- Intercepts each command
- Passes it to `scripts/python/core/check_command.py`
- Based on the result, decides whether to:
  - run the command as-is
  - replace it with a safer version
  - block it and print an error message

### 2. Python Validation Script (`.check_command.py`)

This script performs two levels of checks:

#### a. Rule-Based (YAML)

Loaded from `scripts/rules/python-auditor/check_command_rules.yml`. Each rule defines:

- A `pattern` (regex)
- An optional `replace` (correct command)
- Or an `error` message

#### b. AI-Based (Fallback)

If no rules match, the script:

- Builds a prompt using rules found in
`scripts/rules/ai-auditor/check_command_prompt.md`
- Injects the rules and the command in a wrapper prompt `scripts/ai-prompts/core/check_command_prompt.md`
- Sends it to the OpenAI API (`gpt-4o`)
- Expects a strict JSON response: `PASS`, `EXECUTE`, or `ERROR`
- Returns a structured response which guides the AI agent to fix the command.

### 3. Wrapper Prompt Template (`scripts/ai-prompts/core/check_command_prompt.md`)

If the python script cannot fix the command using the deterministic pattern-matching
process, the command is sent to an AI via OpenAI API call.
This AI is provided with the original command and a ruleset.
The wrapper prompt contains fixed instructions to the AI auditor:

- Context: DevOps engineer reviewing junior developer commands
- Structured format for response
- Rule placeholders are filled in dynamically from YAML rules

# Known Issues and Mitigations

## 1. Shell Metacharacter Injection / Misinterpretation

**Problem:** Commands with unescaped characters (`;`, `|`, `&`, `>`, `$()`, etc.) may be interpreted unexpectedly when passed via `eval`.
**Mitigation:**

- Avoid multiline commands by checking for newlines
- Sanitize before `eval`
- Log corrected commands before execution
- Use `bash -c "$cmd"` for stricter parsing if needed

## 2. Multiline Input or Compound Commands

**Problem:** Users might enter compound or multiline commands that are unsafe to auto-correct.
**Mitigation:**

- Reject all multiline commands with explicit checks (`$'\n'`)
- Encourage safe command chaining with semicolon awareness if needed

## 6. Rule Matching Ambiguity

**Problem:** Overlapping rules could conflict
**Mitigation:**

- Match in YAML sequentially and exit after first match
- Document rule priority clearly

## 7. AI Hallucination or Non-JSON Output

**Problem:** OpenAI API might return malformed or verbose results
**Mitigation:**

- Always enforce `--response-format json`
- Parse with strict JSON parser
- Fallback to `PASS` on failure
