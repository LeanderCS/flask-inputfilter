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

    def test_invalidates_when_first_field_is_missing(self) -> None:
        self.input_filter.add_condition(
            IntegerBiggerThanCondition("field", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field2": 10})

    def test_invalidates_when_both_fields_are_missing(self) -> None:
        self.input_filter.add_condition(
            IntegerBiggerThanCondition("field", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_invalidates_when_fields_contain_none(self) -> None:
        self.input_filter.add_condition(
            IntegerBiggerThanCondition("field", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field": None, "field2": 10})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field": 10, "field2": None})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field": None, "field2": None})

    def test_allows_comparison_with_compatible_types(self) -> None:
        """Python allows comparison between compatible types."""
        self.input_filter.add_condition(
            IntegerBiggerThanCondition("field", "field2")
        )
        # Float comparison works in Python
        self.input_filter.validate_data({"field": 15.5, "field2": 10})
        # Note: String/list comparisons with integers will raise TypeError
        # but we don't test those edge cases here

    def test_validates_with_negative_integers(self) -> None:
        self.input_filter.add_condition(
            IntegerBiggerThanCondition("field", "field2")
        )
        self.input_filter.validate_data({"field": -5, "field2": -10})
        self.input_filter.validate_data({"field": 0, "field2": -1})

    def test_invalidates_with_negative_integers_when_first_is_smaller(
        self,
    ) -> None:
        self.input_filter.add_condition(
            IntegerBiggerThanCondition("field", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field": -10, "field2": -5})

    def test_validates_with_large_integers(self) -> None:
        self.input_filter.add_condition(
            IntegerBiggerThanCondition("field", "field2")
        )
        self.input_filter.validate_data(
            {"field": 1000000, "field2": 999999}
        )
