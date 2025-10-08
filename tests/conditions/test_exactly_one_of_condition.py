import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ExactlyOneOfCondition
from flask_inputfilter.exceptions import ValidationError


class TestExactlyOneOfCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_exactly_one_field_is_present(self) -> None:
        """Test that exactly one field is present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfCondition(["field1", "field2", "field3"])
        )
        self.input_filter.validate_data({"field1": "value"})

    def test_invalidates_when_more_than_one_field_is_present(self) -> None:
        """Test that more than one field raises a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfCondition(["field1", "field2", "field3"])
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "value"}
            )

    def test_invalidates_when_no_fields_are_present(self) -> None:
        """Test that zero fields raises a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfCondition(["field1", "field2", "field3"])
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_invalidates_when_all_three_fields_are_present(self) -> None:
        """Test that all three fields raises a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyOneOfCondition(["field1", "field2", "field3"])
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "v1", "field2": "v2", "field3": "v3"}
            )

    def test_invalidates_with_none_value(self) -> None:
        """Test that None value doesn't count as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfCondition(["field1", "field2"])
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None})

    def test_validates_with_empty_string(self) -> None:
        """Test that empty string DOES count as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfCondition(["field1", "field2"])
        )
        self.input_filter.validate_data({"field1": ""})

    def test_validates_with_zero(self) -> None:
        """Test that zero DOES count as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfCondition(["field1", "field2"])
        )
        self.input_filter.validate_data({"field1": 0})

    def test_validates_with_false(self) -> None:
        """Test that False DOES count as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfCondition(["field1", "field2"])
        )
        self.input_filter.validate_data({"field1": False})
