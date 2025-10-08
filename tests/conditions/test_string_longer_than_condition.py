import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import StringLongerThanCondition
from flask_inputfilter.exceptions import ValidationError


class TestStringLongerThanCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_string_is_longer(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )

        self.input_filter.validate_data({"field1": "value", "field2": "val"})

    def test_invalidates_when_string_not_longer(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "value"}
            )

    def test_invalidates_when_first_field_is_missing(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field2": "val"})

    def test_validates_when_second_field_is_missing(self) -> None:
        """Missing field becomes None, which is treated as empty string."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )
        # Missing field2 is treated as "", so "value" > "" passes
        self.input_filter.validate_data({"field1": "value"})

    def test_invalidates_when_both_fields_are_missing(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_validates_when_fields_contain_none(self) -> None:
        """None values are treated as empty strings."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )
        # None is treated as "", so "value" > "" passes
        self.input_filter.validate_data(
            {"field1": "value", "field2": None}
        )

    def test_invalidates_when_first_field_is_none(self) -> None:
        """First field None (empty) is not longer than non-empty."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": "val"})

    def test_raises_type_error_with_integer_fields(self) -> None:
        """Integer fields cause TypeError when trying len()."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )
        # Integer causes TypeError on len()
        with self.assertRaises(TypeError):
            self.input_filter.validate_data({"field1": 123, "field2": "val"})
        with self.assertRaises(TypeError):
            self.input_filter.validate_data({"field1": "value", "field2": 123})

    def test_validates_with_empty_second_string(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )
        self.input_filter.validate_data({"field1": "value", "field2": ""})

    def test_invalidates_when_both_strings_are_empty(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "", "field2": ""})

    def test_invalidates_when_first_string_is_shorter(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "val", "field2": "value"})

    def test_validates_with_unicode_characters(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )
        self.input_filter.validate_data({"field1": "hello🌍", "field2": "hi"})
        self.input_filter.validate_data({"field1": "länger", "field2": "kurz"})
