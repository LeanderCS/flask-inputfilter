import unittest

from flask_inputfilter import filters, validators
from flask_inputfilter.generators.openapi.mapping_registry import (
    CONSTRAINT_MAPPINGS,
    PATTERN_TO_FORMAT,
    TYPE_MAPPINGS,
    constraint_mapping_for,
    type_mapping_for,
    type_mapping_for_component,
)


class TestMappingRegistry(unittest.TestCase):
    def test_all_filter_names_resolve(self) -> None:
        for mapping in TYPE_MAPPINGS:
            if mapping.filter_name:
                self.assertTrue(
                    hasattr(filters, mapping.filter_name),
                    f"Unknown filter: {mapping.filter_name}",
                )

    def test_all_validator_names_resolve(self) -> None:
        for mapping in TYPE_MAPPINGS:
            if mapping.validator_name:
                self.assertTrue(
                    hasattr(validators, mapping.validator_name),
                    f"Unknown validator: {mapping.validator_name}",
                )

    def test_constraint_validator_names_and_params_resolve(self) -> None:
        for mapping in CONSTRAINT_MAPPINGS:
            validator_class = getattr(validators, mapping.validator_name)
            for param in mapping.params_to_keywords:
                self.assertIn(
                    param,
                    validator_class.__slots__,
                    f"{mapping.validator_name} has no attribute {param}",
                )

    def test_type_mapping_lookup_with_format(self) -> None:
        mapping = type_mapping_for("string", "date")
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.filter_name, "ToDateFilter")
        self.assertEqual(mapping.validator_name, "IsDateValidator")

    def test_type_mapping_lookup_falls_back_to_base_type(self) -> None:
        mapping = type_mapping_for("string", "unknown-format")
        self.assertIsNotNone(mapping)
        self.assertIsNone(mapping.openapi_format)
        self.assertEqual(mapping.validator_name, "IsStringValidator")

    def test_type_mapping_lookup_unknown_type(self) -> None:
        self.assertIsNone(type_mapping_for("does-not-exist"))

    def test_component_lookup(self) -> None:
        mapping = type_mapping_for_component("ToIntegerFilter")
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.openapi_type, "integer")

        mapping = type_mapping_for_component("IsEmailValidator")
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.openapi_format, "email")

        self.assertIsNone(type_mapping_for_component("UnknownValidator"))

    def test_constraint_lookup(self) -> None:
        mapping = constraint_mapping_for("RangeValidator")
        self.assertIsNotNone(mapping)
        self.assertEqual(
            mapping.params_to_keywords,
            {"min_value": "minimum", "max_value": "maximum"},
        )

        self.assertIsNone(constraint_mapping_for("UnknownValidator"))

    def test_pattern_to_format_patterns_are_strings(self) -> None:
        for pattern, format_name in PATTERN_TO_FORMAT.items():
            self.assertIsInstance(pattern, str)
            self.assertIsInstance(format_name, str)


if __name__ == "__main__":
    unittest.main()
