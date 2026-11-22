"""Minimal command-line interface for the runtime foundation."""

import argparse

from agent_runtime import __version__
from agent_runtime.application import RuntimeApplication


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-runtime",
        description="Manage the AI Agent Python runtime.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("info", help="show runtime implementation information")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "info":
        info = RuntimeApplication().get_info()
        print(f"{info.name} {info.version}")
        print(info.implementation_phase)
        print("Implemented capabilities:")
        for capability in info.implemented_capabilities:
            print(f"- {capability}")
        print("Agent discovery and execution are not implemented yet.")
        return 0

    parser.print_help()
    return 0
