import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import NOfMatchesCondition
from flask_inputfilter.exceptions import ValidationError


class TestNOfMatchesCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_exactly_n_fields_match(self) -> None:
        """Test that exactly N fields match a value."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add("field4")
        self.input_filter.addCondition(
            NOfMatchesCondition(["field1", "field2", "field3"], 3, "value")
        )
        self.input_filter.validateData(
            {"field1": "value", "field2": "value", "field3": "value"}
        )

    def test_invalidates_when_less_than_n_fields_match(self) -> None:
        """Test that less than N matching fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.addCondition(
            NOfMatchesCondition(["field1", "field2", "field3"], 3, "value")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"field1": "value", "field2": "value"}
            )
