import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ExactlyOneOfMatchesCondition
from flask_inputfilter.exceptions import ValidationError


class TestExactlyOneOfMatchesCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_exactly_one_field_matches(self) -> None:
        """Test that exactly one field matches the value."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], "value")
        )
        self.input_filter.validateData({"field1": "value"})

    def test_invalidates_when_more_than_one_field_matches(self) -> None:
        """Test that more than one matching field raises a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], "value")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"field1": "value", "field2": "value"}
            )
