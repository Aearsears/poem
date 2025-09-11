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


def install_shims(add_to_path: bool = False) -> None:
    """Install shims for transparent usage of Poetry through poem.

    Args:
        add_to_path: If True, attempts to add shims to PATH
    """
    print("Installing poem shims for Poetry...")

    if platform.system() == "Windows":
        shim_dir = _create_windows_shim()
        if add_to_path:
            add_to_windows_path(shim_dir)
    else:
        shim_dir = _create_unix_shim()
        if add_to_path:
            add_to_unix_path(shim_dir)

    if not add_to_path:
        print("\nTo complete installation manually:")
        print("1. Add the shim directory to your PATH")
        if platform.system() == "Windows":
            print(f"   In PowerShell: $env:PATH=\"{shim_dir};$env:PATH\"")
            print(f"   In Command Prompt: SET PATH={shim_dir};%PATH%")
        else:
            print(f"   export PATH=\"{shim_dir}:$PATH\"")
        print("2. Add this to your shell profile for permanent installation")


def add_to_windows_path(shim_dir: str) -> bool:
    """Add shim directory to Windows PATH environment variable.

    Returns True if successful, False otherwise.
    """
    try:
        # For current session only
        os.environ["PATH"] = f"{shim_dir};{os.environ.get('PATH', '')}"

        # For permanent changes, use the Windows Registry
        import winreg
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_READ | winreg.KEY_WRITE
        ) as key:
            current_path, _ = winreg.QueryValueEx(key, "PATH")
            if shim_dir not in current_path:
                new_path = f"{shim_dir};{current_path}"
                winreg.SetValueEx(
                    key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)

                # Notify Windows of environment variable change
                import ctypes
                HWND_BROADCAST = 0xFFFF
                WM_SETTINGCHANGE = 0x001A
                SMTO_ABORTIFHUNG = 0x0002
                result = ctypes.windll.user32.SendMessageTimeoutW(
                    HWND_BROADCAST, WM_SETTINGCHANGE, 0,
                    "Environment", SMTO_ABORTIFHUNG, 5000, 0
                )

                print(f"Added {shim_dir} to your PATH environment variable")
                print("The change will take effect in new command prompts")
                return True
            else:
                print(f"{shim_dir} is already in your PATH")
                return True
    except Exception as e:
        print(f"Failed to add {shim_dir} to PATH: {str(e)}")
        return False


def add_to_unix_path(shim_dir: str) -> bool:
    """Add shim directory to Unix PATH environment variable.

    Returns True if successful, False otherwise.
    """
    try:
        # For current session only
        os.environ["PATH"] = f"{shim_dir}:{os.environ.get('PATH', '')}"

        # Attempt to add to the user's shell profile
        home = os.path.expanduser("~")
        shells_to_try = [
            # Bash
            (os.path.join(home, ".bash_profile"),
             "export PATH=\"{shim_dir}:$PATH\""),
            (os.path.join(home, ".bashrc"),
             "export PATH=\"{shim_dir}:$PATH\""),
            # Zsh
            (os.path.join(home, ".zshrc"), "export PATH=\"{shim_dir}:$PATH\""),
            # Fish
            (os.path.join(home, ".config", "fish", "config.fish"),
             "set -gx PATH {shim_dir} $PATH")
        ]

        modified = False
        for profile_path, line_template in shells_to_try:
            if os.path.exists(profile_path):
                line = line_template.format(shim_dir=shim_dir)
                with open(profile_path, "r") as f:
                    content = f.read()

                # Only add if not already there
                if line not in content:
                    with open(profile_path, "a") as f:
                        f.write(f"\n# Added by poem\n{line}\n")
                    print(f"Added poem shim path to {profile_path}")
                    modified = True

        if modified:
            print("Please restart your terminal or run:")
            print(f"export PATH=\"{shim_dir}:$PATH\"")
            return True
        else:
            print("Could not automatically update your shell profile.")
            print("Please manually add the following line to your shell profile:")
            print(f"export PATH=\"{shim_dir}:$PATH\"")
            return False

    except Exception as e:
        print(f"Failed to add {shim_dir} to PATH: {str(e)}")
        return False
