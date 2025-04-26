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
        self.input_filter.addCondition(EqualCondition("field1", "field2"))
        self.input_filter.validateData({"field1": "value", "field2": "value"})

    def test_invalidates_when_fields_are_not_equal(self) -> None:
        """Test that EqualCondition raises an error when fields differ."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(EqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"field1": "value", "field2": "not value"}
            )
