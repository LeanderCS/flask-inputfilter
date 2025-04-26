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
        self.input_filter.addCondition(
            ExactlyOneOfCondition(["field1", "field2", "field3"])
        )
        self.input_filter.validateData({"field1": "value"})

    def test_invalidates_when_more_than_one_field_is_present(self) -> None:
        """Test that more than one field raises a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            ExactlyOneOfCondition(["field1", "field2", "field3"])
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"field1": "value", "field2": "value"}
            )
