import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ExactlyNOfCondition
from flask_inputfilter.exceptions import ValidationError


class TestExactlyNthOfCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_exactly_nth_of_condition(self) -> None:
        """Test that exactly N fields are validated."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2", "field3"], 1)
        )
        self.input_filter.validate_data({"field1": "value"})

    def test_invalidates_when_more_than_n_fields_are_present(self) -> None:
        """Test that more than N fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2", "field3"], 1)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "value"}
            )

    def test_invalidates_when_less_than_n_fields_are_present(self) -> None:
        """Test that less than N fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2", "field3"], 2)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "value"})

    def test_invalidates_when_no_fields_are_present(self) -> None:
        """Test that no fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2"], 1)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_invalidates_when_fields_have_none_values(
        self,
    ) -> None:
        """Test that fields with None values are NOT counted as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2", "field3"], 2)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": None})

    def test_invalidates_when_only_one_field_is_none(self) -> None:
        """Test that only one None field fails when expecting two."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2"], 2)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None})

    def test_validates_with_empty_strings(self) -> None:
        """Test that empty strings are counted as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2"], 2)
        )
        self.input_filter.validate_data({"field1": "", "field2": ""})

    def test_validates_with_zero_values(self) -> None:
        """Test that zero values are counted as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2"], 2)
        )
        self.input_filter.validate_data({"field1": 0, "field2": 0})

    def test_validates_with_false_values(self) -> None:
        """Test that False values are counted as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2"], 2)
        )
        self.input_filter.validate_data({"field1": False, "field2": False})

    def test_validates_with_n_zero(self) -> None:
        """Test that n=0 validates when no fields are present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2"], 0)
        )
        self.input_filter.validate_data({})

    def test_invalidates_when_all_fields_present_but_expecting_zero(
        self,
    ) -> None:
        """Test that all fields present fails when expecting zero."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2"], 0)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "value", "field2": "value"})

    def test_validates_with_mixed_field_types(self) -> None:
        """Test that different types of values are counted as present."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyNOfCondition(["field1", "field2", "field3"], 3)
        )
        self.input_filter.validate_data(
            {"field1": "string", "field2": 42, "field3": []}
        )
