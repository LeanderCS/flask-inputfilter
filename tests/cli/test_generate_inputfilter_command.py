import subprocess
import tempfile
import difflib
from pathlib import Path


def test_cli_generate_inputfilter_comprehensive() -> None:
    """Test fif generate:inputfilter with comprehensive schema and compare with expected output."""
    schema_path = Path(__file__).parent / 'schema/test_generate_inputfilter_schema.json'
    expected_path = Path(__file__).parent / 'expected/TestInputFilter.py'

    # Generate the InputFilter
    result = subprocess.run([
        'fif', 'generate:inputfilter',
        '--schema', str(schema_path),
        '--class', 'TestInputFilter',
        '--out', '-',
    ], capture_output=True, text=True)

    assert result.returncode == 0, f"Command failed: {result.stderr}"

    # Read expected output
    with open(expected_path, 'r') as f:
        expected_content = f.read().strip()

    generated_content = result.stdout.strip()

    # Normalize whitespace for comparison
    def normalize_content(content) -> str:
        # Remove extra whitespace but preserve line structure
        lines = [line.rstrip() for line in content.split('\n')]
        # Remove empty lines at start and end
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
        return '\n'.join(lines)

    expected_normalized = normalize_content(expected_content)
    generated_normalized = normalize_content(generated_content)

    # If they don't match exactly, show the diff for debugging
    if expected_normalized != generated_normalized:
        diff = '\n'.join(difflib.unified_diff(
            expected_normalized.splitlines(keepends=True),
            generated_normalized.splitlines(keepends=True),
            fromfile='expected',
            tofile='generated',
            lineterm=''
        ))
        assert False, f"Generated content doesn't match expected:\n{diff}"


def test_cli_generate_inputfilter_to_stdout() -> None:
    """Test fif generate:inputfilter with output to stdout."""
    schema_path = Path(__file__).parent / 'schema/test_generate_inputfilter_schema.json'

    result = subprocess.run([
        'fif', 'generate:inputfilter',
        '--schema', str(schema_path),
        '--class', 'TestInputFilter',
        '--out', '-'
    ], capture_output=True, text=True)

    assert result.returncode == 0
    assert 'class TestInputFilter' in result.stdout
    assert 'from flask_inputfilter import InputFilter' in result.stdout
    assert 'name' in result.stdout  # Property from schema
    assert 'email' in result.stdout  # Property from schema


def test_cli_generate_inputfilter_with_all_options() -> None:
    """Test fif generate:inputfilter with all available options."""
    schema_path = Path(__file__).parent / 'schema/test_generate_inputfilter_schema.json'

    result = subprocess.run([
        'fif', 'generate:inputfilter',
        '--schema', str(schema_path),
        '--class', 'CustomInputFilter',
        '--out', '-',
        '--field-name', 'field',
        '--strict',
    ], capture_output=True, text=True)

    assert result.returncode == 0
    assert 'class CustomInputFilter' in result.stdout
    assert 'from flask_inputfilter import InputFilter' in result.stdout
