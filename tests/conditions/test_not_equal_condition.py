import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import NotEqualCondition
from flask_inputfilter.exceptions import ValidationError


class TestNotEqualCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_values_are_not_equal(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        self.input_filter.validate_data(
            {"field1": "value", "field2": "not value"}
        )

    def test_invalidates_when_values_are_equal(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "value"}
            )

    def test_validates_when_first_field_is_missing(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        self.input_filter.validate_data({"field2": "value"})

    def test_validates_when_second_field_is_missing(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        self.input_filter.validate_data({"field1": "value"})

    def test_invalidates_when_both_fields_are_missing(self) -> None:
        """When both missing, both are None, so they are equal - fails NotEqual."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_validates_when_one_field_is_none(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        self.input_filter.validate_data({"field1": None, "field2": "value"})
        self.input_filter.validate_data({"field1": "value", "field2": None})

    def test_invalidates_when_both_fields_are_none(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": None})

    def test_validates_with_different_types(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        self.input_filter.validate_data({"field1": 0, "field2": "0"})
        # Note: 0 == False in Python, so this will fail NotEqual
        # self.input_filter.validate_data({"field1": False, "field2": 0})
        self.input_filter.validate_data({"field1": [], "field2": ""})

    def test_invalidates_when_types_are_equal_by_value(self) -> None:
        """Test that 0 == False causes NotEqual to fail."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": False, "field2": 0})

    def test_invalidates_with_same_type_equal_values(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": 0, "field2": 0})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "", "field2": ""})

    def test_validates_with_empty_values(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(NotEqualCondition("field1", "field2"))
        self.input_filter.validate_data({"field1": "", "field2": "value"})
        self.input_filter.validate_data({"field1": [], "field2": [1]})
