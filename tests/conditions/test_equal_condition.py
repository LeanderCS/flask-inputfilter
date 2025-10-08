import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import EqualCondition
from flask_inputfilter.exceptions import ValidationError


class TestEqualCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_equal_fields(self) -> None:
        """Test that EqualCondition validates equal fields."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        self.input_filter.validate_data({"field1": "value", "field2": "value"})

    def test_invalidates_when_fields_are_not_equal(self) -> None:
        """Test that EqualCondition raises an error when fields differ."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "not value"}
            )

    def test_invalidates_when_first_field_is_missing(self) -> None:
        """Test that EqualCondition raises an error when first field is
        missing."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field2": "value"})

    def test_invalidates_when_second_field_is_missing(self) -> None:
        """Test that EqualCondition raises an error when second field is
        missing."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "value"})

    def test_validates_when_both_fields_are_missing(self) -> None:
        """Test that EqualCondition validates when both fields are missing
        (both None)."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        # When both are missing, both are None, so they are equal
        self.input_filter.validate_data({})

    def test_validates_when_both_fields_are_none(self) -> None:
        """Test that EqualCondition validates when both fields are None."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        self.input_filter.validate_data({"field1": None, "field2": None})

    def test_invalidates_when_only_one_field_is_none(self) -> None:
        """Test that EqualCondition raises an error when only one field is
        None."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": "value"})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "value", "field2": None})

    def test_validates_with_different_types_when_equal(self) -> None:
        """Test that EqualCondition validates different types that are
        equal."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        self.input_filter.validate_data({"field1": 0, "field2": 0})
        self.input_filter.validate_data({"field1": "", "field2": ""})
        self.input_filter.validate_data({"field1": [], "field2": []})

    def test_validates_with_different_types_when_equal_by_value(self) -> None:
        """Test that EqualCondition uses == comparison (0 == False in
        Python)."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        # Python evaluates 0 == False as True
        self.input_filter.validate_data({"field1": False, "field2": 0})

    def test_invalidates_with_different_types_when_not_equal(self) -> None:
        """Test that EqualCondition raises error for different types that
        aren't equal."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": 0, "field2": "0"})

    def test_validates_with_empty_strings(self) -> None:
        """Test that EqualCondition validates equal empty strings."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(EqualCondition("field1", "field2"))
        self.input_filter.validate_data({"field1": "", "field2": ""})
