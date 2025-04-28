import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ExactlyNOfMatchesCondition
from flask_inputfilter.exceptions import ValidationError


class TestExactlyNthOfMatchesCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_exactly_n_fields_that_match(self) -> None:
        """Test that exactly N fields match a value."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(
                ["field1", "field2", "field3"], 2, "value"
            )
        )
        self.input_filter.validate_data({"field1": "value", "field2": "value"})

    def test_invalidates_when_less_than_n_fields_match(self) -> None:
        """Test that less than N matching fields raise a
        ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(
                ["field1", "field2", "field3"], 2, "value"
            )
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "value"})

    def test_invalidates_when_more_than_n_fields_match(self) -> None:
        """Test that more than N matching fields raise a
        ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(
                ["field1", "field2", "field3"], 2, "value"
            )
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "value", "field3": "value"}
            )
