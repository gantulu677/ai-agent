# Python Runtime

This directory contains the Python runtime package for the AI Agent repository.
The approved Python Runtime Architecture v1.0 is the implementation baseline.
The repository requirement baseline R-01 through R-50 is unchanged.

## Implemented capabilities

- Phase 1: installable package, configuration models, and CLI foundation.
- Phase 2: agent, skill, and instruction discovery; JSON Schema and semantic validation.
- Phase 3: Markdown/TXT/JSON/YAML parsing, category/file ordering, agent and on-demand skill loaders.
- Phase 4: isolated agent contexts and sessions, async LLM provider protocol, explicit tool registry, orchestration.
- Phase 5: in-memory file cache with stat-based invalidation, concurrent independent runs, timing helper, and standard logging.
- Phase 6: unit tests, GitHub Actions test workflow, and implementation documentation.

## Development setup

From the repository root:

    python -m venv .venv
    python -m pip install -e ".[dev]"

Run CLI commands:

    agent-runtime --version
    agent-runtime info
    agent-runtime discover
    agent-runtime --root . validate

Run tests:

    python -m pytest -q

## Runtime boundaries and safety

- Discovery does not execute skill scripts.
- Skill dependencies are inspected only; the runtime does not install packages or make network requests to resolve them.
- Tools must be explicitly registered with ToolExecutor.
- Each AgentContext and AgentSession is created per agent; run_many concurrently executes independent contexts without merging their histories and returns failures per task.
- The provider is an injected protocol. No vendor-specific LLM client or credentials are bundled.
- FileCache is process-local and invalidates entries when file modification time, change time, or size changes. It is not a distributed cache.

## Current limitations

- No production LLM provider implementation is bundled.
- No automatic skill-script execution or sandbox is provided.
- Tool permission policies and external dependency schema details remain implementation-level extensions, not new R-01–R-50 requirements.
- Validation currently focuses on configuration schema, IDs, skill structure, instruction parsing, and ordering metadata.
- Performance claims require benchmarking in the deployment environment; async execution reduces I/O wait but does not make CPU-bound work intrinsically faster.
