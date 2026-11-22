# Python Runtime

This directory contains the Python runtime package for the AI Agent repository.

## Phase 1 scope

Phase 1 establishes the installable Python package, basic configuration data models,
and a minimal CLI. It does not implement agent discovery, instruction loading,
skill loading, validation, LLM integration, or agent execution.

## Development setup

From the repository root:

    python -m venv .venv
    python -m pip install -e ".[dev]"

Run the CLI:

    agent-runtime --version
    agent-runtime info

Run tests:

    python -m pytest

The package source is located at runtime/src/agent_runtime/.
