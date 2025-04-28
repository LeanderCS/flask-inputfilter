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
