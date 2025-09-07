"""Tests for the poem core functionality."""

from poem.core import (
    _get_poetry_home,
    _run_command,
    list_versions,
    get_current_version,
    install_version,
    switch_version,
)
import os
import platform
import subprocess
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add src directory to path for tests
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "src"))


def test_get_poetry_home():
    """Test the _get_poetry_home function."""
    with patch("platform.system") as mock_system:
        # Test Windows path
        mock_system.return_value = "Windows"
        with patch.dict(os.environ, {"APPDATA": "C:\\Users\\Test\\AppData\\Roaming"}):
            assert _get_poetry_home() == "C:\\Users\\Test\\AppData\\Roaming\\pypoetry"

        # Test Unix path
        mock_system.return_value = "Linux"
        with patch("os.path.expanduser") as mock_expanduser:
            mock_expanduser.return_value = "/home/test/.poetry"
            assert _get_poetry_home() == "/home/test/.poetry"


@patch("subprocess.run")
def test_run_command_success(mock_run):
    """Test the _run_command function with successful execution."""
    mock_result = MagicMock()
    mock_result.stdout = "command output\n"
    mock_run.return_value = mock_result

    result = _run_command(["some", "command"])
    assert result == "command output"
    mock_run.assert_called_once_with(
        ["some", "command"],
        check=True,
        capture_output=True,
        text=True,
    )


@patch("subprocess.run")
def test_run_command_failure(mock_run, capsys):
    """Test the _run_command function with failed execution."""
    mock_run.side_effect = subprocess.CalledProcessError(
        1, ["some", "command"], stderr="error message\n")

    with pytest.raises(SystemExit) as e:
        _run_command(["some", "command"])

    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Error: error message" in captured.err


@patch("os.path.exists")
@patch("os.listdir")
@patch("os.path.isdir")
@patch("poem.core._get_poetry_home")
def test_list_versions_installed(mock_get_home, mock_isdir, mock_listdir, mock_exists, capsys):
    """Test the list_versions function with --installed flag."""
    mock_get_home.return_value = "/home/test/.poetry"
    mock_exists.return_value = True
    mock_listdir.return_value = ["1.0.0", "1.1.0", "1.2.0"]
    mock_isdir.return_value = True

    list_versions(installed_only=True)

    captured = capsys.readouterr()
    assert "Installed poetry versions:" in captured.out
    assert "- 1.0.0" in captured.out
    assert "- 1.1.0" in captured.out
    assert "- 1.2.0" in captured.out


@patch("poem.core._run_command")
def test_get_current_version(mock_run_command, capsys):
    """Test the get_current_version function."""
    mock_run_command.return_value = "Poetry version 1.1.0"

    result = get_current_version()

    assert result == "1.1.0"
    captured = capsys.readouterr()
    assert "Current poetry version: 1.1.0" in captured.out
