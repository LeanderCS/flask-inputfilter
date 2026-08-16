import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from flask_inputfilter.generators.openapi.cli import main

OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {"title": "Test API", "version": "1.0.0"},
    "paths": {
        "/users": {
            "post": {
                "operationId": "createUser",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            }
        }
    },
}

FILTER_MODULE = '''
from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.validators import IsStringValidator


class UserInputFilter(InputFilter):
    name: str = field(required=True, validators=[IsStringValidator()])
'''


class TestGenerateCli(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.spec_path = Path(self.tempdir.name) / "api.json"
        self.spec_path.write_text(json.dumps(OPENAPI_SPEC))

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _run(self, *argv: str) -> None:
        with patch.object(sys, "argv", ["flask-inputfilter", *argv]):
            main()

    def test_generate_single_file(self) -> None:
        output = Path(self.tempdir.name) / "filters.py"
        self._run(
            "generate", "openapi", str(self.spec_path),
            "--output", str(output),
        )

        code = output.read_text()
        self.assertIn("class UserInputFilter(InputFilter):", code)

    def test_generate_with_endpoints(self) -> None:
        output = Path(self.tempdir.name) / "filters.py"
        self._run(
            "generate", "openapi", str(self.spec_path),
            "--output", str(output), "--include-endpoints",
        )

        code = output.read_text()
        self.assertIn(
            "class CreateUserInputFilter(UserInputFilter):", code
        )

    def test_endpoints_with_output_dir_rejected(self) -> None:
        with self.assertRaises(SystemExit):
            self._run(
                "generate", "openapi", str(self.spec_path),
                "--output-dir", self.tempdir.name, "--include-endpoints",
            )

    def test_generate_output_dir(self) -> None:
        output_dir = Path(self.tempdir.name) / "filters"
        self._run(
            "generate", "openapi", str(self.spec_path),
            "--output-dir", str(output_dir),
        )

        generated = output_dir / "user_filter.py"
        self.assertTrue(generated.exists())
        self.assertIn(
            "class UserInputFilter(InputFilter):",
            generated.read_text(),
        )

    def test_generate_without_output_fails(self) -> None:
        with self.assertRaises(SystemExit):
            self._run("generate", "openapi", str(self.spec_path))

    def test_generate_output_and_output_dir_fails(self) -> None:
        output = Path(self.tempdir.name) / "filters.py"
        with self.assertRaises(SystemExit):
            self._run(
                "generate", "openapi", str(self.spec_path),
                "--output", str(output),
                "--output-dir", self.tempdir.name,
            )


class TestExportCli(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        module_path = Path(self.tempdir.name) / "my_filters.py"
        module_path.write_text(FILTER_MODULE)
        sys.path.insert(0, self.tempdir.name)

    def tearDown(self) -> None:
        sys.path.remove(self.tempdir.name)
        sys.modules.pop("my_filters", None)
        self.tempdir.cleanup()

    def _run(self, *argv: str) -> None:
        with patch.object(sys, "argv", ["flask-inputfilter", *argv]):
            main()

    def test_export_single_class(self) -> None:
        output = Path(self.tempdir.name) / "schema.json"
        self._run(
            "export", "openapi", "my_filters:UserInputFilter",
            "--output", str(output),
        )

        schema = json.loads(output.read_text())
        self.assertEqual(schema["type"], "object")
        self.assertEqual(schema["required"], ["name"])
        self.assertEqual(schema["properties"]["name"]["type"], "string")

    def test_export_all(self) -> None:
        output = Path(self.tempdir.name) / "components.json"
        self._run(
            "export", "openapi", "my_filters", "--all",
            "--output", str(output),
        )

        document = json.loads(output.read_text())
        self.assertIn("User", document["components"]["schemas"])

    def test_export_components_flag(self) -> None:
        output = Path(self.tempdir.name) / "schema.json"
        self._run(
            "export", "openapi", "my_filters:UserInputFilter",
            "--components", "--output", str(output),
        )

        document = json.loads(output.read_text())
        self.assertIn("User", document["components"]["schemas"])
        self.assertEqual(
            document["components"]["schemas"]["User"]["required"],
            ["name"],
        )

    def test_export_yaml_format(self) -> None:
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML is not installed")

        output = Path(self.tempdir.name) / "schema.yaml"
        self._run(
            "export", "openapi", "my_filters:UserInputFilter",
            "--format", "yaml", "--output", str(output),
        )

        schema = yaml.safe_load(output.read_text())
        self.assertEqual(schema["required"], ["name"])
        self.assertEqual(schema["properties"]["name"]["type"], "string")

    def test_export_unknown_class_fails(self) -> None:
        with self.assertRaises(SystemExit):
            self._run("export", "openapi", "my_filters:DoesNotExist")

    def test_export_without_class_or_all_fails(self) -> None:
        with self.assertRaises(SystemExit):
            self._run("export", "openapi", "my_filters")


if __name__ == "__main__":
    unittest.main()
