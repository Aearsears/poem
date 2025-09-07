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
    assert "pvm" in captured.out
    assert "0.1.0" in captured.out


def test_help(capsys):
    """Test the help output."""
    with pytest.raises(SystemExit) as e:
        main(["--help"])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "usage: pvm" in captured.out


@patch("poem.core.list_versions")
def test_list_command(mock_list_versions, capsys):
    """Test the list command."""
    assert main(["list"]) == 0
    mock_list_versions.assert_called_once_with(installed_only=True)


@patch("poem.core.get_remote_versions")
def test_ls_remote_command(mock_get_remote_versions, capsys):
    """Test the ls-remote command."""
    assert main(["ls-remote"]) == 0
    mock_get_remote_versions.assert_called_once()


@patch("poem.core.switch_version")
def test_use_command(mock_switch_version, capsys):
    """Test the use command."""
    assert main(["use", "1.1.0"]) == 0
    mock_switch_version.assert_called_once_with("1.1.0")


@patch("poem.core.get_current_version_with_source")
def test_current_command(mock_get_current_version_with_source, capsys):
    """Test the current command."""
    assert main(["current"]) == 0
    mock_get_current_version_with_source.assert_called_once()


@patch("poem.core.install_version")
def test_install_command(mock_install_version, capsys):
    """Test the install command."""
    assert main(["install", "1.1.0"]) == 0
    mock_install_version.assert_called_once_with("1.1.0")


@patch("poem.core.uninstall_version")
def test_uninstall_command(mock_uninstall_version, capsys):
    """Test the uninstall command."""
    assert main(["uninstall", "1.1.0"]) == 0
    mock_uninstall_version.assert_called_once_with("1.1.0")


@patch("poem.core.set_global_version")
def test_global_command(mock_set_global_version, capsys):
    """Test the global command."""
    assert main(["global", "1.1.0"]) == 0
    mock_set_global_version.assert_called_once_with("1.1.0")


@patch("poem.core.set_local_version")
def test_local_command(mock_set_local_version, capsys):
    """Test the local command."""
    assert main(["local", "1.1.0"]) == 0
    mock_set_local_version.assert_called_once_with("1.1.0")


@patch("poem.core.doctor")
def test_doctor_command(mock_doctor, capsys):
    """Test the doctor command."""
    assert main(["doctor"]) == 0
    mock_doctor.assert_called_once()


@patch("poem.core.which_poetry")
def test_which_command(mock_which_poetry, capsys):
    """Test the which command."""
    assert main(["which"]) == 0
    mock_which_poetry.assert_called_once()
