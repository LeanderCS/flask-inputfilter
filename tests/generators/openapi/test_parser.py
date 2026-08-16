import json
import tempfile
import unittest
from pathlib import Path

try:
    import yaml  # noqa: F401

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from flask_inputfilter.generators.openapi.parser import OpenAPIParser


class TestOpenAPIParser(unittest.TestCase):
    """Test suite for OpenAPI parser."""

    def test_from_string_yaml(self):
        """Test parsing from YAML string."""
        if not HAS_YAML:
            self.skipTest("pyyaml not installed")

        yaml_content = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
components:
  schemas:
    User:
      type: object
      properties:
        name:
          type: string
"""
        parser = OpenAPIParser.from_string(yaml_content, format="yaml")
        self.assertIsInstance(parser, OpenAPIParser)

    def test_from_string_json(self):
        """Test parsing from JSON string."""
        json_content = json.dumps(
            {
                "openapi": "3.0.0",
                "info": {"title": "Test API", "version": "1.0.0"},
                "components": {
                    "schemas": {
                        "User": {
                            "type": "object",
                            "properties": {"name": {"type": "string"}},
                        }
                    }
                },
            }
        )
        parser = OpenAPIParser.from_string(json_content, format="json")
        self.assertIsInstance(parser, OpenAPIParser)

    def test_from_file_yaml(self):
        """Test parsing from YAML file."""
        if not HAS_YAML:
            self.skipTest("pyyaml not installed")

        yaml_content = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
components:
  schemas:
    User:
      type: object
      properties:
        name:
          type: string
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as f:
            f.write(yaml_content)
            temp_path = f.name

        try:
            parser = OpenAPIParser.from_file(temp_path)
            self.assertIsInstance(parser, OpenAPIParser)
        finally:
            Path(temp_path).unlink()

    def test_from_file_json(self):
        """Test parsing from JSON file."""
        json_content = json.dumps(
            {
                "openapi": "3.0.0",
                "info": {"title": "Test API", "version": "1.0.0"},
                "components": {
                    "schemas": {
                        "User": {
                            "type": "object",
                            "properties": {"name": {"type": "string"}},
                        }
                    }
                },
            }
        )
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write(json_content)
            temp_path = f.name

        try:
            parser = OpenAPIParser.from_file(temp_path)
            self.assertIsInstance(parser, OpenAPIParser)
        finally:
            Path(temp_path).unlink()

    def test_extract_schemas(self):
        """Test schema extraction."""
        openapi_content = {
            "components": {
                "schemas": {
                    "User": {
                        "type": "object",
                        "properties": {"name": {"type": "string"}},
                    }
                }
            }
        }
        parser = OpenAPIParser(openapi_content=openapi_content)
        schemas = parser.extract_schemas()
        self.assertIn("User", schemas)

    def test_get_schema(self):
        """Test getting specific schema."""
        openapi_content = {
            "components": {
                "schemas": {
                    "User": {
                        "type": "object",
                        "properties": {"name": {"type": "string"}},
                    }
                }
            }
        }
        parser = OpenAPIParser(openapi_content=openapi_content)
        schema = parser.get_schema("User")
        self.assertIsNotNone(schema)
        self.assertEqual(schema["type"], "object")

    def test_resolve_ref(self):
        """Test resolving $ref references."""
        openapi_content = {
            "components": {
                "schemas": {
                    "User": {
                        "type": "object",
                        "properties": {"name": {"type": "string"}},
                    }
                }
            }
        }
        parser = OpenAPIParser(openapi_content=openapi_content)
        ref_schema = parser.resolve_ref("#/components/schemas/User")
        self.assertIsNotNone(ref_schema)
        self.assertEqual(ref_schema["type"], "object")

    def test_extract_request_body(self):
        """Test extracting request body."""
        openapi_content = {
            "paths": {
                "/users": {
                    "post": {
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"}
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        parser = OpenAPIParser(openapi_content=openapi_content)
        schema = parser.extract_request_body("/users", "post")
        self.assertIsNotNone(schema)
        self.assertEqual(schema["type"], "object")

    def test_non_dict_root_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            OpenAPIParser(openapi_content=["not", "a", "mapping"])

    def test_circular_ref_resolution_returns_object_stub(self) -> None:
        openapi_content = {
            "components": {
                "schemas": {
                    "Node": {
                        "type": "object",
                        "properties": {
                            "child": {"$ref": "#/components/schemas/Node"}
                        },
                    }
                }
            }
        }
        parser = OpenAPIParser(openapi_content=openapi_content)
        schema = parser.extract_schemas()["Node"]
        resolved = parser.resolve_schema_refs(schema)
        self.assertEqual(
            resolved["properties"]["child"]["properties"]["child"],
            {"type": "object"},
        )
