"""Core functionality for managing poetry versions."""

import http.client
import logging
import os
import platform
import subprocess
import sys
import json
from pathlib import Path
from typing import List, Optional, Tuple, Dict

from poem.http import HTTP


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


def _get_config_dir() -> str:
    """Get the poem configuration directory."""
    if platform.system() == "Windows":
        config_dir = os.path.join(os.environ.get("APPDATA", ""), "poem")
    else:
        config_dir = os.path.expanduser("~/.config/poem")

    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def _get_global_version_file() -> str:
    """Get the global version file path."""
    return os.path.join(_get_config_dir(), "global-version")


def _get_poetry_bin(version: str) -> str:
    """Get the path to the Poetry binary for a specific version."""
    poetry_home = _get_poetry_home()
    if platform.system() == "Windows":
        return os.path.join(poetry_home, "venv", version, "Scripts", "poetry.exe")
    else:
        return os.path.join(poetry_home, "venv", version, "bin", "poetry")


def _get_active_version() -> Tuple[str, str]:
    """Get the active Poetry version and its source.

    Returns:
        A tuple containing the version and source ("local", "global", or "default")
    """
    # Check for local .poetry-version file
    if os.path.exists(".poetry-version"):
        with open(".poetry-version", "r") as f:
            version = f.read().strip()
            return version, "local"

    # Check for global version
    global_version_file = _get_global_version_file()
    if os.path.exists(global_version_file):
        with open(global_version_file, "r") as f:
            version = f.read().strip()
            return version, "global"

    # Return the default system version
    try:
        version = get_current_version()
        if version:
            return version, "default"
        else:
            return "unknown", "unknown"
    except:
        return "unknown", "unknown"


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

    # Create a temporary script that modifies the current shell session
    if platform.system() == "Windows":
        # For Windows, we can export instructions
        print(f"To use poetry version {version} in your current shell, run:")
        poetry_path = os.path.dirname(_get_poetry_bin(version))
        print(f"    $env:PATH=\"{poetry_path};$env:PATH\"  # PowerShell")
        print(f"    SET PATH={poetry_path};%PATH%  # Command Prompt")
    else:
        # For Unix systems
        print(f"To use poetry version {version} in your current shell, run:")
        poetry_path = os.path.dirname(_get_poetry_bin(version))
        print(f"    export PATH=\"{poetry_path}:$PATH\"")

    print(f"\nPoetry version {version} is ready to use.")


def set_global_version(version: str) -> None:
    """Set the global default Poetry version.

    Args:
        version: The version to set as global default
    """
    # Check if the version is installed
    poetry_home = _get_poetry_home()
    version_dir = os.path.join(poetry_home, "venv", version)

    if not os.path.exists(version_dir):
        print(f"Poetry version {version} is not installed. Installing now...")
        install_version(version)

    # Set the global version
    with open(_get_global_version_file(), "w") as f:
        f.write(version)

    print(f"Set global poetry version to {version}")
    print("This setting will apply to new shell sessions.")


def set_local_version(version: str) -> None:
    """Set the local project Poetry version.

    Args:
        version: The version to set for the local project
    """
    # Create .poetry-version file
    with open(".poetry-version", "w") as f:
        f.write(version)

    print(f"Set local poetry version to {version}")
    print("This setting will apply when you're in this directory.")


def uninstall_version(version: str) -> None:
    """Uninstall a specific Poetry version.

    Args:
        version: The version to uninstall
    """
    # Check if it's currently in use
    active_version, source = _get_active_version()
    if active_version == version:
        print(
            f"Warning: You're trying to uninstall the active poetry version ({version}).")
        print(f"This version is set as your {source} version.")
        return

    # Check if the version is installed
    poetry_home = _get_poetry_home()
    version_dir = os.path.join(poetry_home, "venv", version)

    if not os.path.exists(version_dir):
        print(f"Poetry version {version} is not installed.")
        return

    # Remove the version directory
    try:
        import shutil
        shutil.rmtree(version_dir)
        print(f"Successfully uninstalled poetry {version}")
    except Exception as e:
        print(
            f"Failed to uninstall poetry {version}: {str(e)}", file=sys.stderr)
        sys.exit(1)


def get_remote_versions() -> None:
    """List available Poetry versions from GitHub releases."""
    pass
    try:
        print("Fetching available versions from GitHub...")
        releases = HTTP.get(
            "https://api.github.com/repos/python-poetry/poetry/releases", headers={
                "User-Agent": "pvm-tool",
                "Accept": "application/vnd.github.v3+json"
            })

        print(
            f"Available Poetry versions: {[release['tag_name'].lstrip("v") for release in releases]}")

    except Exception as e:
        print(f"Failed to fetch remote versions: {str(e)}", file=sys.stderr)
        print("Try using pip: pip index versions poetry")


def get_current_version_with_source() -> str:
    """Get the current Poetry version and its source.

    Returns:
        The current version string
    """
    version, source = _get_active_version()
    if version == "unknown":
        print("Poetry is not installed or not in PATH")
    else:
        print(f"Current poetry version: {version} (from {source})")
    return version


def which_poetry() -> None:
    """Show the path to the active Poetry binary."""
    version, _ = _get_active_version()
    if version == "unknown":
        print("Poetry is not installed or not in PATH")
        return

    try:
        poetry_bin = _get_poetry_bin(version)
        if os.path.exists(poetry_bin):
            print(poetry_bin)
        else:
            result = subprocess.run(
                ["where" if platform.system() == "Windows" else "which", "poetry"],
                capture_output=True,
                text=True,
            )
            print(result.stdout.strip())
    except:
        print("Could not determine poetry path")


def doctor() -> None:
    """Diagnose setup issues with Poetry installation."""
    print("Poetry Version Manager (PVM) Doctor")
    print("===================================")

    # Check PVM configuration
    print("\n## PVM Configuration")
    config_dir = _get_config_dir()
    print(f"Config directory: {config_dir}")
    if os.path.exists(config_dir):
        print("✓ Configuration directory exists")
    else:
        print("✗ Configuration directory does not exist")

    # Check global version
    global_version_file = _get_global_version_file()
    if os.path.exists(global_version_file):
        with open(global_version_file, "r") as f:
            global_version = f.read().strip()
        print(f"Global version: {global_version}")
    else:
        print("No global version set")

    # Check local version
    if os.path.exists(".poetry-version"):
        with open(".poetry-version", "r") as f:
            local_version = f.read().strip()
        print(f"Local version: {local_version}")
    else:
        print("No local version file (.poetry-version) found")

    # Check Poetry installation
    print("\n## Poetry Installation")
    poetry_home = _get_poetry_home()
    print(f"Poetry home: {poetry_home}")

    if os.path.exists(poetry_home):
        print("✓ Poetry home directory exists")

        venv_dir = os.path.join(poetry_home, "venv")
        if os.path.exists(venv_dir):
            print("✓ Poetry venv directory exists")
            versions = [d for d in os.listdir(
                venv_dir) if os.path.isdir(os.path.join(venv_dir, d))]
            print(
                f"Installed versions: {', '.join(versions) if versions else 'None'}")
        else:
            print("✗ Poetry venv directory does not exist")
    else:
        print("✗ Poetry home directory does not exist")

    # Check PATH
    print("\n## Environment")
    try:
        path = os.environ.get("PATH", "")
        paths = path.split(os.pathsep)

        # Check for poetry in PATH
        poetry_in_path = False
        for p in paths:
            if "poetry" in p.lower() and os.path.exists(p):
                poetry_in_path = True
                print(f"Poetry directory in PATH: {p}")

        if not poetry_in_path:
            print("✗ No Poetry directory found in PATH")

        # Check active version
        print("\n## Active Poetry")
        version, source = _get_active_version()
        print(f"Active version: {version} (from {source})")

        if version != "unknown":
            try:
                output = _run_command(["poetry", "--version"])
                print(f"Poetry reports: {output}")
                print("✓ Poetry is working correctly")
            except:
                print("✗ Error running poetry command")
    except Exception as e:
        print(f"Error during diagnosis: {str(e)}")
