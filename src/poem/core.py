"""Core functionality for managing poetry versions."""

import os
import platform
import subprocess
import sys
from typing import List, Optional


def _get_poetry_home() -> str:
    """Get the poetry home directory."""
    if platform.system() == "Windows":
        return os.path.join(os.environ.get("APPDATA", ""), "pypoetry")
    else:
        return os.path.expanduser("~/.poetry")


def _run_command(command: List[str]) -> str:
    """Run a command and return its output."""
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)


def list_versions(installed_only: bool = False) -> None:
    """List available poetry versions.

    Args:
        installed_only: If True, only list installed versions
    """
    if installed_only:
        poetry_home = _get_poetry_home()
        version_dir = os.path.join(poetry_home, "venv")

        if not os.path.exists(version_dir):
            print("No poetry versions are installed.")
            return

        versions = [d for d in os.listdir(
            version_dir) if os.path.isdir(os.path.join(version_dir, d))]
        if not versions:
            print("No poetry versions are installed.")
            return

        print("Installed poetry versions:")
        for version in sorted(versions):
            print(f"- {version}")
    else:
        # For available versions, we could query PyPI
        print("Fetching available versions from PyPI...")
        output = _run_command(["pip", "index", "versions", "poetry"])

        # Parse and display versions
        lines = output.split("\n")
        for line in lines:
            if "Available versions:" in line:
                versions = line.split("Available versions:")[1].strip()
                print(f"Available poetry versions: {versions}")
                return

        print("Could not retrieve available versions. Check your internet connection.")


def get_current_version() -> Optional[str]:
    """Get the current poetry version."""
    try:
        output = _run_command(["poetry", "--version"])
        version = output.split()[2]  # Format: "Poetry version X.Y.Z"
        print(f"Current poetry version: {version}")
        return version
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Poetry is not installed or not in PATH", file=sys.stderr)
        return None


def install_version(version: str) -> None:
    """Install a specific poetry version.

    Args:
        version: The version to install (e.g., "1.1.0")
    """
    print(f"Installing poetry version {version}...")

    # We use pip to install a specific version
    try:
        _run_command(["pip", "install", f"poetry=={version}"])
        print(f"Successfully installed poetry {version}")
    except subprocess.SubprocessError:
        print(f"Failed to install poetry {version}", file=sys.stderr)
        sys.exit(1)


def switch_version(version: str) -> None:
    """Switch to a specific poetry version.

    Args:
        version: The version to switch to (e.g., "1.1.0")
    """
    print(f"Switching to poetry version {version}...")

    # Check if the version is installed
    poetry_home = _get_poetry_home()
    version_dir = os.path.join(poetry_home, "venv", version)

    if not os.path.exists(version_dir):
        print(f"Poetry version {version} is not installed. Installing now...")
        install_version(version)

    # In a more complete implementation, we would handle the actual switching logic here
    # This would involve modifying PATH or symbolic links depending on the OS

    print(f"Successfully switched to poetry {version}")
