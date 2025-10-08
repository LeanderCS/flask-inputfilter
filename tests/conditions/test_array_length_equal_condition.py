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
        """Test that differing array lengths raise a ValidationError."""
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": [1, 2], "field2": [1]})
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": [1, 2], "field2": [1, 2, 3]}
            )

    def test_invalidates_when_first_field_is_missing(self) -> None:
        """Test that a missing first field raises a ValidationError."""
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field2": [1, 2]})

    def test_validates_when_both_fields_are_missing(self) -> None:
        """Test that both missing fields are treated as empty arrays (equal
        length)."""
        # Both None -> both treated as [], same length
        self.input_filter.validate_data({})

    def test_invalidates_when_first_field_is_none(self) -> None:
        """Test that None in first field raises a ValidationError."""
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": [1, 2]})

    def test_invalidates_when_second_field_is_none(self) -> None:
        """Test that None in second field raises a ValidationError."""
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": [1, 2], "field2": None})

    def test_validates_when_both_fields_are_none(self) -> None:
        """Test that None in both fields are treated as empty arrays
        (equal)."""
        # Both None -> both treated as [], same length
        self.input_filter.validate_data({"field1": None, "field2": None})

    def test_invalidates_or_raises_when_first_field_is_not_array(self) -> None:
        """Non-array types cause ValidationError (str has len) or TypeError
        (int)."""
        # String has len(), so it just fails the condition
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "not array", "field2": [1, 2]}
            )
        # Integer causes TypeError on len()
        with self.assertRaises(TypeError):
            self.input_filter.validate_data({"field1": 123, "field2": [1, 2]})

    def test_invalidates_or_raises_when_second_field_is_not_array(self) -> None:
        """Non-array types cause ValidationError (str has len) or TypeError
        (dict)."""
        # String has len(), so it just fails the condition
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": [1, 2], "field2": "not array"}
            )
        # Dict has len(), so it just fails the condition
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": [1, 2], "field2": {}})

    def test_validates_large_arrays_with_equal_length(self) -> None:
        """Test that large arrays with equal length pass validation."""
        large_array = list(range(1000))
        self.input_filter.validate_data(
            {"field1": large_array, "field2": large_array.copy()}
        )
