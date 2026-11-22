# Python Runtime

This directory contains the Python runtime package for the AI Agent repository.
The approved Python Runtime Architecture v1.0 is the implementation baseline.
The approved requirement baseline R-01 through R-50 is unchanged.

## Implemented capabilities

- Phase 1: installable package, configuration models, and CLI foundation.
- Phase 2: agent, skill, and instruction discovery; JSON Schema and semantic validation.
- Phase 3: Markdown/TXT/JSON/YAML parsing, category/file ordering, agent and on-demand skill loaders.
- Phase 4: isolated agent contexts and sessions, async LLM provider protocol, explicit tool registry, orchestration.
- Phase 5: process-local file cache, concurrent independent runs, per-agent error logging, and timing helper.
- Phase 6: unit tests, GitHub Actions test workflow, and implementation documentation.

## Development setup

From the repository root:

    python -m venv .venv
    python -m pip install -e ".[dev]"

Commands:

    agent-runtime --version
    agent-runtime info
    agent-runtime discover
    agent-runtime --root . validate
    python -m pytest -q

## Runtime boundaries

- Discovery does not execute skill scripts.
- Skill dependencies are inspected only; the runtime does not install packages or make network requests to resolve them.
- Tools must be explicitly registered with ToolExecutor.
- Each AgentContext and AgentSession is independent.
- `RuntimeApplication.load_valid_agents()` rejects agents with Critical findings and continues loading valid peers.
- Concurrent orchestration returns each task's result or exception and logs individual failures.
- The provider is an injected protocol; no vendor-specific LLM client or credentials are bundled.
- FileCache is process-local, not a distributed cache.

## Audit findings and limitations

The R-01–R-50 implementation cross-audit is documented in [docs/IMPLEMENTATION_AUDIT_R01-R50.md](../docs/IMPLEMENTATION_AUDIT_R01-R50.md).

- R-15 is partial: severity levels exist and Critical rejection is implemented, but warning-producing validation conditions have not been specified/implemented.
- R-41 is partial: external dependency declarations are read and inspected, but no formal dependency schema or full resolver is implemented.
- No production LLM provider, automatic skill-script execution, dependency installation, or security sandbox is included.
- Passing the latest CI suite and environment-specific security/performance benchmarks must be confirmed before production use.
