import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import NOfCondition
from flask_inputfilter.exceptions import ValidationError


class TestNOfCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_exactly_n_fields_are_present(self) -> None:
        """Test that exactly N fields are validated."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            NOfCondition(["field1", "field2", "field3"], 2)
        )
        self.input_filter.validate_data({"field1": "value", "field2": "value"})
        self.input_filter.validate_data(
            {"field1": "value", "field2": "value", "field3": "value"}
        )

    def test_invalidates_when_less_than_n_fields_are_present(self) -> None:
        """Test that less than N fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            NOfCondition(["field1", "field2", "field3"], 2)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "value"})

    def test_invalidates_when_no_fields_are_present(self) -> None:
        """Test that zero fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            NOfCondition(["field1", "field2", "field3"], 2)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_validates_with_exactly_n_fields(self) -> None:
        """Test that exactly N fields pass validation."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            NOfCondition(["field1", "field2", "field3"], 2)
        )
        self.input_filter.validate_data({"field1": "value", "field3": "value"})

    def test_validates_with_more_than_n_fields(self) -> None:
        """Test that more than N fields pass validation."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            NOfCondition(["field1", "field2", "field3"], 1)
        )
        self.input_filter.validate_data(
            {"field1": "value", "field2": "value", "field3": "value"}
        )

    def test_invalidates_with_none_values(self) -> None:
        """Test that None values don't count as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            NOfCondition(["field1", "field2"], 2)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": None})

    def test_validates_with_empty_string_values(self) -> None:
        """Test that empty string values DO count as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            NOfCondition(["field1", "field2"], 2)
        )
        self.input_filter.validate_data({"field1": "", "field2": ""})

    def test_validates_with_zero_values(self) -> None:
        """Test that zero values DO count as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            NOfCondition(["field1", "field2"], 2)
        )
        self.input_filter.validate_data({"field1": 0, "field2": 0})

    def test_validates_with_false_values(self) -> None:
        """Test that False values DO count as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            NOfCondition(["field1", "field2"], 2)
        )
        self.input_filter.validate_data({"field1": False, "field2": False})

    def test_validates_n_equals_zero(self) -> None:
        """Test that N=0 always validates."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            NOfCondition(["field1", "field2"], 0)
        )
        self.input_filter.validate_data({})
        self.input_filter.validate_data({"field1": "value"})
        self.input_filter.validate_data({"field1": "value", "field2": "value"})
