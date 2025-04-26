import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ArrayLongerThanCondition
from flask_inputfilter.exceptions import ValidationError


class TestArrayLongerThanCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_first_array_is_longer(self) -> None:
        """Test that the first array is longer than the second."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            ArrayLongerThanCondition("field1", "field2")
        )
        self.input_filter.validateData({"field1": [1, 2], "field2": [1]})

    def test_invalidates_when_arrays_are_equal(self) -> None:
        """Test that equal arrays fail validation."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            ArrayLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"field1": [1, 2], "field2": [1, 2]}
            )
