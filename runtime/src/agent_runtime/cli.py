"""Command-line interface for the AI Agent runtime."""
import argparse
from pathlib import Path

from agent_runtime import __version__
from agent_runtime.application import RuntimeApplication


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-runtime", description="Manage the AI Agent Python runtime.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root (default: current directory)")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("info", help="show runtime capabilities")
    commands.add_parser("discover", help="list discovered agents")
    validate = commands.add_parser("validate", help="validate repository configuration")
    validate.add_argument("--report-dir", type=Path, default=Path("reports"))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    app = RuntimeApplication(args.root)
    if args.command == "info":
        info = app.get_info()
        print(f"{info.name} {info.version} - {info.implementation_phase}")
        for item in info.implemented_capabilities:
            print(f"- {item}")
        return 0
    if args.command == "discover":
        agents = app.discover()
        for agent in agents:
            print(f"{agent.directory.name}: {agent.config_path.relative_to(app.repository_root)}")
        print(f"Discovered {len(agents)} agent(s).")
        return 0
    if args.command == "validate":
        report = app.validate()
        destination = args.report_dir if args.report_dir.is_absolute() else app.repository_root / args.report_dir
        json_path, markdown_path = report.write(destination)
        print(report.to_markdown())
        print(f"Reports: {json_path} and {markdown_path}")
        return 1 if report.has_critical else 0
    parser.print_help()
    return 0
