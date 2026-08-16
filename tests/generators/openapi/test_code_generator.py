import unittest

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.generators.openapi.code_generator import CodeGenerator
from flask_inputfilter.generators.openapi.parser import OpenAPIParser


class TestCodeGenerator(unittest.TestCase):
    """Test suite for code generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.openapi_content = {
            "components": {
                "schemas": {
                    "User": {
                        "type": "object",
                        "required": ["name", "email"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "minLength": 2,
                                "maxLength": 50,
                            },
                            "email": {"type": "string", "format": "email"},
                            "age": {
                                "type": "integer",
                                "minimum": 18,
                                "maximum": 120,
                            },
                        },
                    }
                }
            }
        }
        self.parser = OpenAPIParser(openapi_content=self.openapi_content)
        self.generator = CodeGenerator(parser=self.parser)

    def test_generate_class(self):
        """Test generating a class from schema."""
        schema = self.openapi_content["components"]["schemas"]["User"]
        code = self.generator.generate_class("User", schema)
        self.assertIn("class UserInputFilter", code)
        self.assertIn("InputFilter", code)
        self.assertIn("field", code)

    def test_generate_class_with_required_fields(self):
        """Test generating class with required fields."""
        schema = self.openapi_content["components"]["schemas"]["User"]
        code = self.generator.generate_class("User", schema)
        self.assertIn("required=True", code)

    def test_generate_class_with_validators(self):
        """Test generating class with validators."""
        schema = self.openapi_content["components"]["schemas"]["User"]
        code = self.generator.generate_class("User", schema)
        self.assertIn("IsStringValidator", code)
        self.assertIn("IsIntegerValidator", code)
        self.assertIn("LengthValidator", code)
        self.assertIn("RangeValidator", code)

    def test_generate_class_with_filters(self):
        """Test generating class with filters."""
        schema = self.openapi_content["components"]["schemas"]["User"]
        code = self.generator.generate_class("User", schema)
        self.assertIn("ToIntegerFilter", code)

    def test_generate_class_with_enum(self):
        """Test generating class with enum."""
        schema = {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["active", "inactive", "pending"],
                }
            },
        }
        code = self.generator.generate_class("Status", schema)
        self.assertIn("InArrayValidator", code)
        self.assertIn("active", code)
        self.assertIn("inactive", code)
        self.assertIn("pending", code)

    def test_generate_class_with_nested_object(self):
        """Test generating class with nested object."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                    },
                },
            },
        }
        code = self.generator.generate_class("User", schema)
        self.assertIn("AddressInputFilter", code)
        self.assertIn("input_filter=AddressInputFilter", code)

    def test_generate_class_with_array(self):
        """Test generating class with array."""
        schema = {
            "type": "object",
            "properties": {
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                }
            },
        }
        code = self.generator.generate_class("Post", schema)
        self.assertIn("IsArrayValidator", code)
        self.assertIn("ArrayElementValidator", code)

    def test_to_class_name(self):
        """Test converting schema name to class name."""
        self.assertEqual(
            self.generator.to_class_name("User"), "UserInputFilter"
        )
        self.assertEqual(
            self.generator.to_class_name("user-profile"),
            "UserProfileInputFilter",
        )
        self.assertEqual(
            self.generator.to_class_name("user_profile"),
            "UserProfileInputFilter",
        )
        self.assertEqual(
            self.generator.to_class_name("123foo"),
            "N123fooInputFilter",
        )

    def test_multi_word_nested_object_class_name_matches_field(self):
        schema = {
            "type": "object",
            "properties": {
                "shipping_address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                    },
                    "required": ["street"],
                }
            },
        }
        code = self.generator.generate_class("Order", schema)
        self.assertIn("class ShippingAddressInputFilter(InputFilter):", code)
        self.assertIn("input_filter=ShippingAddressInputFilter", code)
        self.assertNotIn("ShippingaddressInputFilter", code)
        namespace = self._exec(code)
        order = namespace["OrderInputFilter"]()
        result = order.validate_data(
            {"shipping_address": {"street": "Main", "city": "Berlin"}}
        )
        self.assertEqual(result["shipping_address"]["street"], "Main")

    def test_array_of_objects_uses_array_element_input_filter(self):
        schema = {
            "type": "object",
            "required": ["items"],
            "properties": {
                "items": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["product_id"],
                        "properties": {
                            "product_id": {"type": "integer"},
                            "quantity": {
                                "type": "integer",
                                "minimum": 1,
                            },
                        },
                    },
                }
            },
        }
        code = self.generator.generate_class("Order", schema)
        self.assertIn("class ItemsItemInputFilter(InputFilter):", code)
        self.assertIn(
            "ArrayElementValidator(element_filter=ItemsItemInputFilter())",
            code,
        )
        namespace = self._exec(code)
        order = namespace["OrderInputFilter"]()
        result = order.validate_data(
            {"items": [{"product_id": 1, "quantity": 2}]}
        )
        self.assertEqual(result["items"][0]["product_id"], 1)
        with self.assertRaises(ValidationError):
            order.validate_data({"items": [{"quantity": 2}]})

    def test_top_level_ref_reuses_component_class_name(self):
        openapi = {
            "components": {
                "schemas": {
                    "Address": {
                        "type": "object",
                        "properties": {
                            "street": {"type": "string"},
                        },
                    },
                    "User": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "$ref": "#/components/schemas/Address"
                            },
                        },
                    },
                }
            }
        }
        parser = OpenAPIParser(openapi_content=openapi)
        generator = CodeGenerator(parser=parser)
        code = generator.generate_class(
            "User", openapi["components"]["schemas"]["User"]
        )
        self.assertIn("input_filter=AddressInputFilter", code)
        self.assertNotIn("class AddressInputFilter", code)

    def test_circular_ref_does_not_recurse(self):
        openapi = {
            "components": {
                "schemas": {
                    "User": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "friend": {"$ref": "#/components/schemas/User"},
                        },
                    }
                }
            }
        }
        parser = OpenAPIParser(openapi_content=openapi)
        generator = CodeGenerator(parser=parser)
        code = generator.generate_class(
            "User", openapi["components"]["schemas"]["User"]
        )
        self.assertIn("input_filter=UserInputFilter", code)
        self.assertIn(
            "from __future__ import annotations", generator.generate_imports()
        )

    def test_generated_imports_include_future_annotations(self):
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
        }
        code = self.generator.generate_class(
            "User", schema, include_imports=True
        )
        self.assertTrue(code.startswith("from __future__ import annotations"))

    def _exec(self, code):
        namespace = {}
        preamble = (
            "from __future__ import annotations\n"
            "from typing import Any\n"
            "from flask_inputfilter import InputFilter\n"
            "from flask_inputfilter.declarative import field\n"
            "from flask_inputfilter.filters import *\n"
            "from flask_inputfilter.validators import *\n"
        )
        exec(  # noqa: S102
            compile(preamble + code, "<generated>", "exec"), namespace
        )
        return namespace

    def test_string_default_with_quotes_and_backslashes(self):
        """String defaults must be escaped properly (regression)."""
        schema = {
            "type": "object",
            "properties": {
                "q": {"type": "string", "default": 'say "hi"'},
                "bs": {"type": "string", "default": "back\\slash"},
            },
        }
        code = self.generator.generate_class("Thing", schema)
        namespace = self._exec(code)
        validated = namespace["ThingInputFilter"]().validate_data({})
        self.assertEqual(validated["q"], 'say "hi"')
        self.assertEqual(validated["bs"], "back\\slash")

    def test_pattern_with_trailing_backslash(self):
        """Patterns are emitted via repr, so any content stays valid
        (regression: raw-string escaping broke on quotes/backslashes)."""
        schema = {
            "type": "object",
            "properties": {
                "p": {"type": "string", "pattern": r'^\d+"x"\\$'},
            },
        }
        code = self.generator.generate_class("Thing", schema)
        namespace = self._exec(code)
        namespace["ThingInputFilter"]().validate_data({"p": '1"x"\\'})

    def test_invalid_identifier_properties_are_skipped_with_warning(self):
        """Keyword or non-identifier property names must not break the
        generated code (regression)."""
        schema = {
            "type": "object",
            "properties": {
                "class": {"type": "string"},
                "user-name": {"type": "string"},
                "123abc": {"type": "string"},
                "ok_field": {"type": "string"},
            },
        }
        code = self.generator.generate_class("Thing", schema)
        self.assertIn("WARNING", code)
        namespace = self._exec(code)
        instance = namespace["ThingInputFilter"]()
        self.assertTrue(instance.has("ok_field"))

    def test_only_invalid_identifier_properties_still_compiles(self):
        """A class body with only warning comments needs a pass statement."""
        schema = {
            "type": "object",
            "properties": {"class": {"type": "string"}},
        }
        code = self.generator.generate_class("Thing", schema)
        namespace = self._exec(code)
        namespace["ThingInputFilter"]().validate_data({})

    def test_date_format_generates_working_validation(self):
        """format: date must produce code that accepts date strings
        (regression: IsStringValidator rejected the converted date)."""
        import datetime

        schema = {
            "type": "object",
            "properties": {
                "d": {"type": "string", "format": "date"},
                "dt": {"type": "string", "format": "date-time"},
            },
        }
        code = self.generator.generate_class("Thing", schema)
        namespace = self._exec(code)
        validated = namespace["ThingInputFilter"]().validate_data(
            {"d": "2024-01-01", "dt": "2024-01-01T10:00:00"}
        )
        self.assertEqual(validated["d"], datetime.date(2024, 1, 1))
