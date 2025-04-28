import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import IntegerBiggerThanCondition
from flask_inputfilter.exceptions import ValidationError


class TestIntegerBiggerThanCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()
        self.input_filter.add("field")
        self.input_filter.add("field2")

    def test_validates_when_first_integer_is_bigger(self) -> None:
        self.input_filter.add_condition(
            IntegerBiggerThanCondition("field", "field2")
        )
        self.input_filter.validate_data({"field": 11, "field2": 10})

    def test_invalidates_when_first_integer_is_equal_or_smaller(self) -> None:
        self.input_filter.add_condition(
            IntegerBiggerThanCondition("field", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field": 10, "field2": 10})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field": 10, "field2": 11})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field": 10})
