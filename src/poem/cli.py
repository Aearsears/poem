"""CLI module for the poem package."""

import argparse
import sys
from typing import List, Optional

from poem import __version__
from poem.core import (
    list_versions,
    switch_version,
    get_current_version,
    install_version,
    uninstall_version,
    set_global_version,
    set_local_version,
    get_remote_versions,
    get_current_version_with_source,
    which_poetry,
    doctor,
)


def create_parser() -> argparse.ArgumentParser:
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="pvm",  # Changed from "poem" to "pvm" based on README commands
        description="Poetry Version Manager - A CLI tool for managing poetry versions",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # List command
    list_parser = subparsers.add_parser(
        "list", help="List installed poetry versions"
    )

    # ls-remote command
    subparsers.add_parser(
        "ls-remote", help="List available poetry versions from GitHub releases"
    )

    # Use command
    use_parser = subparsers.add_parser(
        "use", help="Switch to a specific poetry version for the current shell session"
    )
    use_parser.add_argument(
        "version", help="Version to use (e.g. 1.1.0)"
    )

    # Current command
    subparsers.add_parser(
        "current", help="Show the active poetry version and its source"
    )

    # Install command
    install_parser = subparsers.add_parser(
        "install", help="Install a specific poetry version"
    )
    install_parser.add_argument(
        "version", help="Version to install (e.g. 1.1.0)"
    )

    # Uninstall command
    uninstall_parser = subparsers.add_parser(
        "uninstall", help="Remove an installed poetry version"
    )
    uninstall_parser.add_argument(
        "version", help="Version to uninstall (e.g. 1.1.0)"
    )

    # Global command
    global_parser = subparsers.add_parser(
        "global", help="Set a global default poetry version"
    )
    global_parser.add_argument(
        "version", help="Version to set as global default (e.g. 1.1.0)"
    )

    # Local command
    local_parser = subparsers.add_parser(
        "local", help="Set a local project poetry version (.poetry-version)"
    )
    local_parser.add_argument(
        "version", help="Version to set for this directory (e.g. 1.1.0)"
    )

    # Which command
    which_parser = subparsers.add_parser(
        "which", help="Show the path to the active Poetry binary"
    )

    # Doctor command
    subparsers.add_parser(
        "doctor", help="Diagnose setup issues (shims, PATH, install dirs)"
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
        list_versions(installed_only=True)  # Always show installed versions
    elif parsed_args.command == "ls-remote":
        get_remote_versions()
    elif parsed_args.command == "use":
        switch_version(parsed_args.version)
    elif parsed_args.command == "current":
        get_current_version_with_source()
    elif parsed_args.command == "install":
        install_version(parsed_args.version)
    elif parsed_args.command == "uninstall":
        uninstall_version(parsed_args.version)
    elif parsed_args.command == "global":
        set_global_version(parsed_args.version)
    elif parsed_args.command == "local":
        set_local_version(parsed_args.version)
    elif parsed_args.command == "which":
        which_poetry()
    elif parsed_args.command == "doctor":
        doctor()
    else:
        print(f"Unknown command: {parsed_args.command}")
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
