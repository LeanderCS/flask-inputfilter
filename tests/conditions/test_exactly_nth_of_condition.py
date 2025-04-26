import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ExactlyNOfCondition
from flask_inputfilter.exceptions import ValidationError


class TestExactlyNthOfCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_exactly_nth_of_condition(self) -> None:
        """Test that exactly N fields are validated."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            ExactlyNOfCondition(["field1", "field2", "field3"], 1)
        )
        self.input_filter.validateData({"field1": "value"})

    def test_invalidates_when_more_than_n_fields_are_present(self) -> None:
        """Test that more than N fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            ExactlyNOfCondition(["field1", "field2", "field3"], 1)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"field1": "value", "field2": "value"}
            )
