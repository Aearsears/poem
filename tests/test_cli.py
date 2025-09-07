"""Tests for the poem CLI."""

from poem.cli import main
import sys
import os
import pytest
from unittest.mock import patch

# Add src directory to path for tests
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "src"))


def test_version(capsys):
    """Test the --version flag."""
    with pytest.raises(SystemExit) as e:
        main(["--version"])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "poem" in captured.out
    assert "0.1.0" in captured.out


def test_help(capsys):
    """Test the help output."""
    with pytest.raises(SystemExit) as e:
        main(["--help"])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "usage: poem" in captured.out


@patch("poem.core.list_versions")
def test_list_command(mock_list_versions, capsys):
    """Test the list command."""
    assert main(["list"]) == 0
    mock_list_versions.assert_called_once_with(False)


@patch("poem.core.list_versions")
def test_list_installed_command(mock_list_versions, capsys):
    """Test the list --installed command."""
    assert main(["list", "--installed"]) == 0
    mock_list_versions.assert_called_once_with(True)


@patch("poem.core.switch_version")
def test_use_command(mock_switch_version, capsys):
    """Test the use command."""
    assert main(["use", "1.1.0"]) == 0
    mock_switch_version.assert_called_once_with("1.1.0")


@patch("poem.core.get_current_version")
def test_current_command(mock_get_current_version, capsys):
    """Test the current command."""
    assert main(["current"]) == 0
    mock_get_current_version.assert_called_once()


@patch("poem.core.install_version")
def test_install_command(mock_install_version, capsys):
    """Test the install command."""
    assert main(["install", "1.1.0"]) == 0
    mock_install_version.assert_called_once_with("1.1.0")
