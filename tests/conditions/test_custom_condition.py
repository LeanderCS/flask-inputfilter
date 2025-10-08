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
        """Test that CustomCondition works when the condition is true."""
        self.input_filter.validate_data({"field": "value"})

    def test_raises_validation_error_when_custom_condition_is_false(
        self,
    ) -> None:
        """Test that CustomCondition raises a ValidationError when false."""
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_invalidates_when_field_missing(self) -> None:
        """Test that condition fails when required field is missing."""
        input_filter = InputFilter()
        input_filter.add("field")
        input_filter.add_condition(
            CustomCondition(lambda data: "field" in data and data["field"] and len(data["field"]) > 0)
        )
        with self.assertRaises(ValidationError):
            input_filter.validate_data({})

    def test_invalidates_when_field_is_none(self) -> None:
        """Test that condition fails when field is None."""
        input_filter = InputFilter()
        input_filter.add("field")
        input_filter.add_condition(
            CustomCondition(
                lambda data: "field" in data and data["field"] is not None
            )
        )
        with self.assertRaises(ValidationError):
            input_filter.validate_data({"field": None})

    def test_validates_with_complex_condition(self) -> None:
        """Test that complex conditions work correctly."""
        input_filter = InputFilter()
        input_filter.add("age")
        input_filter.add("country")
        input_filter.add_condition(
            CustomCondition(
                lambda data: data.get("age", 0) >= 18
                and data.get("country") == "US"
            )
        )
        input_filter.validate_data({"age": 21, "country": "US"})

    def test_invalidates_with_complex_condition_failure(self) -> None:
        """Test that complex conditions fail correctly."""
        input_filter = InputFilter()
        input_filter.add("age")
        input_filter.add("country")
        input_filter.add_condition(
            CustomCondition(
                lambda data: data.get("age", 0) >= 18
                and data.get("country") == "US"
            )
        )
        with self.assertRaises(ValidationError):
            input_filter.validate_data({"age": 16, "country": "US"})
        with self.assertRaises(ValidationError):
            input_filter.validate_data({"age": 21, "country": "UK"})

    def test_validates_with_multiple_field_check(self) -> None:
        """Test that condition checking multiple fields works."""
        input_filter = InputFilter()
        input_filter.add("field1")
        input_filter.add("field2")
        input_filter.add_condition(
            CustomCondition(
                lambda data: data.get("field1") == data.get("field2")
            )
        )
        input_filter.validate_data({"field1": "same", "field2": "same"})

    def test_invalidates_when_multiple_fields_differ(self) -> None:
        """Test that condition fails when multiple fields differ."""
        input_filter = InputFilter()
        input_filter.add("field1")
        input_filter.add("field2")
        input_filter.add_condition(
            CustomCondition(
                lambda data: data.get("field1") == data.get("field2")
            )
        )
        with self.assertRaises(ValidationError):
            input_filter.validate_data({"field1": "same", "field2": "different"})

    def test_validates_with_empty_data_when_allowed(self) -> None:
        """Test that empty data validates if condition allows it."""
        input_filter = InputFilter()
        input_filter.add_condition(CustomCondition(lambda data: len(data) == 0))
        input_filter.validate_data({})

    def test_invalidates_with_type_check_failure(self) -> None:
        """Test that condition fails with type mismatches."""
        input_filter = InputFilter()
        input_filter.add("field")
        input_filter.add_condition(
            CustomCondition(
                lambda data: isinstance(data.get("field"), str)
                and len(data["field"]) > 0
            )
        )
        with self.assertRaises(ValidationError):
            input_filter.validate_data({"field": 123})

    def test_validates_with_boolean_return(self) -> None:
        """Test that condition works with boolean fields."""
        input_filter = InputFilter()
        input_filter.add("active")
        input_filter.add_condition(
            CustomCondition(lambda data: data.get("active") is True)
        )
        input_filter.validate_data({"active": True})

    def test_invalidates_with_falsy_values(self) -> None:
        """Test that condition fails with falsy values."""
        input_filter = InputFilter()
        input_filter.add("field")
        input_filter.add_condition(
            CustomCondition(lambda data: bool(data.get("field")))
        )
        with self.assertRaises(ValidationError):
            input_filter.validate_data({"field": ""})
        with self.assertRaises(ValidationError):
            input_filter.validate_data({"field": 0})
        with self.assertRaises(ValidationError):
            input_filter.validate_data({"field": False})
