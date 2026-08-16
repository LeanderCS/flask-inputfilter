import tempfile
import unittest
from pathlib import Path

try:
    import yaml  # noqa: F401

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.generators.openapi import generate_from_openapi


class TestGenerateFromOpenAPI(unittest.TestCase):
    """Test suite for generate_from_openapi function."""

    def test_generate_from_string(self):
        """Test generating from OpenAPI string."""
        if not HAS_YAML:
            self.skipTest("pyyaml not installed")

        openapi_content = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
components:
  schemas:
    User:
      type: object
      required:
        - name
      properties:
        name:
          type: string
          minLength: 2
          maxLength: 50
"""
        code = generate_from_openapi(openapi_content=openapi_content)
        self.assertIn("class UserInputFilter", code)
        self.assertIn("InputFilter", code)

    def test_generate_from_file(self):
        """Test generating from OpenAPI file."""
        if not HAS_YAML:
            self.skipTest("pyyaml not installed")

        openapi_content = """
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
            f.write(openapi_content)
            temp_path = f.name

        try:
            code = generate_from_openapi(openapi_file=temp_path)
            self.assertIn("class UserInputFilter", code)
        finally:
            Path(temp_path).unlink()

    def test_generate_specific_schema(self):
        """Test generating specific schema."""
        if not HAS_YAML:
            self.skipTest("pyyaml not installed")

        openapi_content = """
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
    Product:
      type: object
      properties:
        title:
          type: string
"""
        code = generate_from_openapi(
            openapi_content=openapi_content, schema_name="User"
        )
        self.assertIn("class UserInputFilter", code)
        self.assertNotIn("class ProductInputFilter", code)

    def test_generate_to_file(self):
        """Test generating and writing to file."""
        if not HAS_YAML:
            self.skipTest("pyyaml not installed")

        openapi_content = """
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
        ) as openapi_file:
            openapi_file.write(openapi_content)
            openapi_path = openapi_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as output_file:
            output_path = output_file.name

        try:
            generate_from_openapi(
                openapi_file=openapi_path, output_file=output_path
            )
            generated_code = Path(output_path).read_text()
            self.assertIn("class UserInputFilter", generated_code)
        finally:
            Path(openapi_path).unlink()
            Path(output_path).unlink()

    def test_generate_all_schemas(self):
        """Test generating all schemas."""
        if not HAS_YAML:
            self.skipTest("pyyaml not installed")

        openapi_content = """
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
    Product:
      type: object
      properties:
        title:
          type: string
"""
        code = generate_from_openapi(openapi_content=openapi_content)
        self.assertIn("class UserInputFilter", code)
        self.assertIn("class ProductInputFilter", code)

    def test_example_api_yaml_smoke(self) -> None:
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("pyyaml not installed")

        example_path = (
            Path(__file__).resolve().parents[3]
            / "examples"
            / "openapi_generator"
            / "api.yaml"
        )
        if not example_path.exists():
            self.skipTest("example api.yaml not found")

        code = generate_from_openapi(openapi_file=example_path)
        self.assertIn("from __future__ import annotations", code)
        self.assertIn("class AddressInputFilter(InputFilter):", code)
        self.assertIn("class UserInputFilter(InputFilter):", code)
        self.assertIn("input_filter=AddressInputFilter", code)
        self.assertIn("class ItemsItemInputFilter(InputFilter):", code)
        self.assertIn(
            "ArrayElementValidator(element_filter=ItemsItemInputFilter())",
            code,
        )
        self.assertIn("class CategoryInputFilter(InputFilter):", code)
        self.assertNotIn("ShippingaddressInputFilter", code)
        self.assertNotIn("Categoryinputfilter", code)

        namespace: dict = {}
        exec(compile(code, str(example_path), "exec"), namespace)  # noqa: S102
        order = namespace["OrderInputFilter"]()
        validated = order.validate_data(
            {
                "user_id": 1,
                "items": [{"product_id": 10, "quantity": 2, "price": 9.5}],
            }
        )
        self.assertEqual(validated["items"][0]["product_id"], 10)
        with self.assertRaises(ValidationError):
            order.validate_data({"user_id": 1, "items": [{}]})
