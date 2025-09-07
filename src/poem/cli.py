"""CLI module for the poem package."""

import argparse
import sys
from typing import List, Optional

from poem import __version__
from poem.core import list_versions, switch_version, get_current_version, install_version


def create_parser() -> argparse.ArgumentParser:
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="poem",
        description="A CLI tool for managing poetry versions",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # List command
    list_parser = subparsers.add_parser(
        "list", help="List available poetry versions"
    )
    list_parser.add_argument(
        "--installed", action="store_true", help="Show only installed versions"
    )

    # Use command
    use_parser = subparsers.add_parser(
        "use", help="Switch to a specific poetry version"
    )
    use_parser.add_argument(
        "version", help="Version to use (e.g. 1.1.0)"
    )

    # Current command
    subparsers.add_parser(
        "current", help="Show the current poetry version"
    )

    # Install command
    install_parser = subparsers.add_parser(
        "install", help="Install a specific poetry version"
    )
    install_parser.add_argument(
        "version", help="Version to install (e.g. 1.1.0)"
    )

    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Run the CLI application."""
    if args is None:
        args = sys.argv[1:]

    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        return 1

    if parsed_args.command == "list":
        list_versions(parsed_args.installed)
    elif parsed_args.command == "use":
        switch_version(parsed_args.version)
    elif parsed_args.command == "current":
        get_current_version()
    elif parsed_args.command == "install":
        install_version(parsed_args.version)

    return 0


if __name__ == "__main__":
    sys.exit(main())
