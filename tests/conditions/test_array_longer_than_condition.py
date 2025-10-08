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
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        self.input_filter.validate_data({"field1": [1, 2], "field2": [1]})

    def test_invalidates_when_arrays_are_equal(self) -> None:
        """Test that equal arrays fail validation."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": [1, 2], "field2": [1, 2]}
            )

    def test_invalidates_when_first_array_is_shorter(self) -> None:
        """Test that shorter first array fails validation."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": [1], "field2": [1, 2]})

    def test_invalidates_when_first_field_is_missing(self) -> None:
        """Test that missing first field fails validation."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field2": [1]})

    def test_validates_when_second_field_is_missing(self) -> None:
        """Test that missing second field is treated as empty array."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        # Missing field2 is treated as [], so [1, 2] > [] passes
        self.input_filter.validate_data({"field1": [1, 2]})

    def test_invalidates_when_both_fields_are_missing(self) -> None:
        """Test that both missing fields fail validation."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_validates_when_second_field_is_none(self) -> None:
        """Test that None in second field is treated as empty array."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        # field2=None is treated as [], so [1, 2] > [] passes
        self.input_filter.validate_data({"field1": [1, 2], "field2": None})

    def test_invalidates_when_first_field_is_none(self) -> None:
        """Test that None in first field is treated as empty array."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        # field1=None is treated as [], so [] is not > [1]
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": [1]})

    def test_invalidates_or_raises_when_fields_are_not_arrays(self) -> None:
        """Non-array values may cause TypeError or ValidationError depending on
        type."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        # String has len(), so it uses string length comparison
        self.input_filter.validate_data(
            {"field1": "longstring", "field2": [1]}
        )
        # Integer causes TypeError on len()
        with self.assertRaises(TypeError):
            self.input_filter.validate_data({"field1": [1, 2], "field2": 123})
        # Dict has len(), so it uses dict length comparison
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": {}, "field2": [1]})

    def test_validates_with_empty_second_array(self) -> None:
        """Test that first array longer than empty array passes validation."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        self.input_filter.validate_data({"field1": [1], "field2": []})

    def test_invalidates_when_both_arrays_are_empty(self) -> None:
        """Test that both empty arrays fail validation."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ArrayLongerThanCondition("field1", "field2")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": [], "field2": []})
