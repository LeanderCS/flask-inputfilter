import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import CustomCondition
from flask_inputfilter.exceptions import ValidationError


class TestCustomCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()
        self.input_filter.add("field")
        self.input_filter.add_condition(
            CustomCondition(
                lambda data: "field" in data and data["field"] == "value"
            )
        )

    def test_validates_when_custom_condition_is_true(self) -> None:
        """Test that CustomCondition works when the condition is
        true."""
        self.input_filter.validate_data({"field": "value"})

    def test_raises_validation_error_when_custom_condition_is_false(
        self,
    ) -> None:
        """Test that CustomCondition raises a ValidationError when
        false."""
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})
