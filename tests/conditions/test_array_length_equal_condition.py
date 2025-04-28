import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ArrayLengthEqualCondition
from flask_inputfilter.exceptions import ValidationError


class TestArrayLengthEqualCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLengthEqualCondition("field1", "field2")
        )

    def test_validates_equal_array_length(self) -> None:
        """Test that arrays with equal lengths pass validation."""
        self.input_filter.validate_data({"field1": [1, 2], "field2": [1, 2]})

    def test_validates_empty_arrays(self) -> None:
        """Test that empty arrays pass validation."""
        self.input_filter.validate_data({"field1": [], "field2": []})

    def test_invalidates_when_field_is_missing(self) -> None:
        """Test that a missing field raises a ValidationError."""
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": [1, 2]})

    def test_invalidates_when_array_lengths_differ(self) -> None:
        """Test that differing array lengths raise a
        ValidationError."""
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": [1, 2], "field2": [1]})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": [1, 2], "field2": [1, 2, 3]}
            )
