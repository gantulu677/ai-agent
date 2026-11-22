# Runtime Test Suite

Run all tests from the repository root after installing development dependencies:

    python -m pip install -e ".[dev]"
    python -m pytest

The suite covers filesystem discovery boundaries, structured instruction parsing,
category and file ordering, basic schema/configuration validation, report formats,
file-cache invalidation, explicit tool registration, and provider orchestration.
