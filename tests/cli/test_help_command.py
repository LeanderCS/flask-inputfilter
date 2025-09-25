import subprocess
import tempfile
from pathlib import Path


def test_cli_help_command() -> None:
    """Test fif help command shows general help."""
    result = subprocess.run(['fif', 'help'], capture_output=True, text=True)

    assert result.returncode == 0
    assert "Flask InputFilter CLI" in result.stdout
    assert "generate:inputfilter" in result.stdout
    assert "help" in result.stdout


def test_cli_help_with_specific_command() -> None:
    """Test fif help with specific command."""
    result = subprocess.run(['fif', 'help', 'generate:inputfilter'], capture_output=True, text=True)

    assert result.returncode == 0
    assert "Generate an InputFilter class from a JSON Schema file" in result.stdout
    assert "--schema" in result.stdout
    assert "--class" in result.stdout
