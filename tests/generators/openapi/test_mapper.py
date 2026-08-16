import unittest

from flask_inputfilter.generators.openapi.mapper import SchemaMapper


class TestSchemaMapper(unittest.TestCase):
    """Test suite for schema mapper."""

    def test_map_string_field(self):
        """Test mapping string field."""
        schema = {"type": "string"}
        field_config = SchemaMapper.map_field("name", schema)
        self.assertFalse(field_config["required"])
        self.assertTrue(
            any(
                v.get("type") == "IsStringValidator"
                for v in field_config["validators"]
            )
        )

    def test_map_string_field_with_length(self):
        """Test mapping string field with minLength/maxLength."""
        schema = {
            "type": "string",
            "minLength": 2,
            "maxLength": 50,
        }
        field_config = SchemaMapper.map_field("name", schema, ["name"])
        self.assertTrue(field_config["required"])
        length_validator = next(
            (
                v
                for v in field_config["validators"]
                if v.get("type") == "LengthValidator"
            ),
            None,
        )
        self.assertIsNotNone(length_validator)
        self.assertEqual(length_validator["min_length"], 2)
        self.assertEqual(length_validator["max_length"], 50)

    def test_map_string_field_with_email_format(self):
        """Test mapping string field with email format."""
        schema = {"type": "string", "format": "email"}
        field_config = SchemaMapper.map_field("email", schema)
        regex_validator = next(
            (
                v
                for v in field_config["validators"]
                if v.get("type") == "RegexValidator"
            ),
            None,
        )
        self.assertIsNotNone(regex_validator)

    def test_map_integer_field(self):
        """Test mapping integer field."""
        schema = {"type": "integer"}
        field_config = SchemaMapper.map_field("age", schema)
        self.assertTrue(
            any(
                f.get("type") == "ToIntegerFilter"
                for f in field_config["filters"]
            )
        )
        self.assertTrue(
            any(
                v.get("type") == "IsIntegerValidator"
                for v in field_config["validators"]
            )
        )

    def test_map_integer_field_with_range(self):
        """Test mapping integer field with minimum/maximum."""
        schema = {"type": "integer", "minimum": 18, "maximum": 120}
        field_config = SchemaMapper.map_field("age", schema)
        range_validator = next(
            (
                v
                for v in field_config["validators"]
                if v.get("type") == "RangeValidator"
            ),
            None,
        )
        self.assertIsNotNone(range_validator)
        self.assertEqual(range_validator["min_value"], 18)
        self.assertEqual(range_validator["max_value"], 120)

    def test_map_number_field(self):
        """Test mapping number field."""
        schema = {"type": "number"}
        field_config = SchemaMapper.map_field("price", schema)
        self.assertTrue(
            any(
                f.get("type") == "ToFloatFilter"
                for f in field_config["filters"]
            )
        )
        self.assertTrue(
            any(
                v.get("type") == "IsFloatValidator"
                for v in field_config["validators"]
            )
        )

    def test_map_boolean_field(self):
        """Test mapping boolean field."""
        schema = {"type": "boolean"}
        field_config = SchemaMapper.map_field("active", schema)
        self.assertTrue(
            any(
                f.get("type") == "ToBooleanFilter"
                for f in field_config["filters"]
            )
        )
        self.assertTrue(
            any(
                v.get("type") == "IsBooleanValidator"
                for v in field_config["validators"]
            )
        )

    def test_map_enum_field(self):
        """Test mapping enum field."""
        schema = {"type": "string", "enum": ["active", "inactive", "pending"]}
        field_config = SchemaMapper.map_field("status", schema)
        enum_validator = next(
            (
                v
                for v in field_config["validators"]
                if v.get("type") == "InArrayValidator"
            ),
            None,
        )
        self.assertIsNotNone(enum_validator)
        self.assertEqual(
            enum_validator["haystack"], ["active", "inactive", "pending"]
        )

    def test_map_array_field(self):
        """Test mapping array field."""
        schema = {
            "type": "array",
            "items": {"type": "string"},
        }
        field_config = SchemaMapper.map_field("tags", schema)
        self.assertTrue(
            any(
                v.get("type") == "IsArrayValidator"
                for v in field_config["validators"]
            )
        )

    def test_map_nested_object(self):
        """Test mapping nested object."""
        schema = {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"},
            },
        }
        field_config = SchemaMapper.map_field("address", schema)
        self.assertTrue(field_config.get("_nested"))
        self.assertIn("_nested_class_name", field_config)

    def test_map_field_with_default(self):
        """Test mapping field with default value."""
        schema = {"type": "string", "default": "unknown"}
        field_config = SchemaMapper.map_field("name", schema)
        self.assertEqual(field_config["default"], "unknown")

    def test_map_field_required(self):
        """Test mapping required field."""
        schema = {"type": "string"}
        field_config = SchemaMapper.map_field("name", schema, ["name"])
        self.assertTrue(field_config["required"])

    def test_date_formats_do_not_emit_string_validator(self):
        """ToDateFilter converts before validation, so IsStringValidator must
        not be emitted for date/date-time formats (regression)."""
        for format_type, filter_name, validator_name in (
            ("date", "ToDateFilter", "IsDateValidator"),
            ("date-time", "ToDateTimeFilter", "IsDateTimeValidator"),
        ):
            config = SchemaMapper.map_field(
                "d", {"type": "string", "format": format_type}
            )
            validator_types = [v["type"] for v in config["validators"]]
            filter_types = [f["type"] for f in config["filters"]]
            self.assertNotIn("IsStringValidator", validator_types)
            self.assertIn(validator_name, validator_types)
            self.assertIn(filter_name, filter_types)

    def test_non_converting_formats_keep_string_validator(self):
        """Uuid/uri/email formats validate strings, so IsStringValidator
        stays."""
        for format_type in ("uuid", "uri", "email", "unknown-format", None):
            schema = {"type": "string"}
            if format_type:
                schema["format"] = format_type
            config = SchemaMapper.map_field("f", schema)
            validator_types = [v["type"] for v in config["validators"]]
            self.assertIn("IsStringValidator", validator_types, format_type)
