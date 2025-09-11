from poem.core import _get_active_version, _get_poetry_bin
import shutil
from pathlib import Path
import subprocess
import sys
import os
import platform

UNIX_SHIM_PATH = "$HOME/.poem/shims"
WINDOWS_SHIM_PATH = "%APPDATA%\\.poem\\shims"


def _create_shim_directory() -> str:
    """Create and return the path to the shim directory."""
    if platform.system() == "Windows":
        shim_dir = os.path.join(os.environ.get(
            "APPDATA", ""), ".poem", "shims")

    else:
        shim_dir = os.path.expanduser("~/.poem/shims")

    os.makedirs(shim_dir, exist_ok=True)
    return shim_dir


def _create_windows_shim() -> None:
    """Create a Windows batch file shim for Poetry."""
    shim_dir = _create_shim_directory()
    shim_path = os.path.join(shim_dir, "poetry.bat")
    poem_path = os.path.join(os.path.dirname(shim_dir), "shim.py")

    with open(shim_path, "w") as f:
        f.write("@echo off\r\n")
        f.write("setlocal\r\n")
        f.write("set POEM_EXEC_DIR=%~dp0\r\n")
        f.write("python \"%POEM_EXEC_DIR%..\\poem.py\" %*\r\n")

    # Get the absolute path to shim.py in the package
    import inspect
    from poem import shim  # Import your shim module
    source_path = inspect.getfile(shim)

    # Copy it to the destination
    shutil.copy(source_path, poem_path)

    print(f"Created Windows shim at: {shim_path}")
    print(f"Add '{shim_dir}' to your PATH to use poetry commands with poem")


def _create_unix_shim() -> None:
    """Create a Unix shell script shim for Poetry."""
    shim_dir = _create_shim_directory()
    shim_path = os.path.join(shim_dir, "poetry")
    poem_path = os.path.join(os.path.dirname(shim_dir), "shim.py")

    with open(shim_path, "w") as f:
        f.write("#!/bin/sh\n")
        f.write("POEM_EXEC_DIR=\"$(dirname \"$0\")\"\n")
        f.write("exec python \"${POEM_EXEC_DIR}/../poem.py\" \"$@\"\n")

    # Get the absolute path to shim.py in the package
    import inspect
    from poem import shim  # Import your shim module
    source_path = inspect.getfile(shim)

    # Copy it to the destination
    shutil.copy(source_path, poem_path)

    # Make the shim executable
    os.chmod(shim_path, 0o755)

    print(f"Created Unix shim at: {shim_path}")
    print(f"Add '{shim_dir}' to your PATH to use poetry commands with poem")


def install_shims() -> None:
    """Install shims for transparent usage of Poetry through poem."""
    print("Installing poem shims for Poetry...")

    if platform.system() == "Windows":
        _create_windows_shim()
    else:
        _create_unix_shim()

    print("\nTo complete installation:")
    print("1. Add the shim directory to your PATH")
    if platform.system() == "Windows":
        print("   In PowerShell: $env:PATH=\"$env:APPDATA\\.poem\\shims;$env:PATH\"")
        print("   In Command Prompt: SET PATH=%APPDATA%\\.poem\\shims;%PATH%")
    else:
        print("   export PATH=\"$HOME/.poem/shims:$PATH\"")
    print("2. Add this to your shell profile for permanent installation")
