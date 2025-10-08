import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import OneOfMatchesCondition
from flask_inputfilter.exceptions import ValidationError


class TestOneOfMatchesCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_at_least_one_field_matches(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], "value")
        )

        self.input_filter.validate_data({"field1": "value"})
        self.input_filter.validate_data({"field2": "value"})
        self.input_filter.validate_data({"field1": "value", "field2": "value"})

    def test_invalidates_when_no_fields_match(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], "value")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field": "not value"})

    def test_invalidates_when_all_fields_are_missing(self) -> None:
        """Test that condition fails when all fields are missing."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], "value")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_invalidates_when_fields_have_wrong_values(self) -> None:
        """Test that condition fails when fields have wrong values."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], "expected")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "wrong", "field2": "also wrong"}
            )

    def test_invalidates_when_fields_are_none(self) -> None:
        """Test that condition fails when fields are None."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], "value")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": None})

    def test_validates_when_one_field_matches_none(self) -> None:
        """Test that condition passes when one field matches None value."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], None)
        )

        self.input_filter.validate_data({"field1": None})

    def test_invalidates_when_matching_none_but_fields_have_values(
        self,
    ) -> None:
        """Test that condition fails when matching None but fields have
        values."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], None)
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "value"}
            )

    def test_validates_with_empty_string_match(self) -> None:
        """Test that condition passes when matching empty strings."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], "")
        )

        self.input_filter.validate_data({"field1": ""})

    def test_invalidates_when_type_mismatch(self) -> None:
        """Test that condition fails with type mismatches."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], "123")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": 123, "field2": 456})

    def test_validates_with_integer_match(self) -> None:
        """Test that condition passes when matching integers."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], 42)
        )

        self.input_filter.validate_data({"field1": 42})

    def test_validates_with_boolean_match(self) -> None:
        """Test that condition passes when matching booleans."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], True)
        )

        self.input_filter.validate_data({"field1": True})
