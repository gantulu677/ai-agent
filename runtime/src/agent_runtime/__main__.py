"""Allow running the CLI with python -m agent_runtime."""

from agent_runtime.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
