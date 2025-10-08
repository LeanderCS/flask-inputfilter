import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ExactlyNOfMatchesCondition
from flask_inputfilter.exceptions import ValidationError


class TestExactlyNthOfMatchesCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_exactly_n_fields_that_match(self) -> None:
        """Test that exactly N fields match a value."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(
                ["field1", "field2", "field3"], 2, "value"
            )
        )
        self.input_filter.validate_data({"field1": "value", "field2": "value"})

    def test_invalidates_when_less_than_n_fields_match(self) -> None:
        """Test that less than N matching fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(
                ["field1", "field2", "field3"], 2, "value"
            )
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "value"})

    def test_invalidates_when_more_than_n_fields_match(self) -> None:
        """Test that more than N matching fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(
                ["field1", "field2", "field3"], 2, "value"
            )
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "value", "field3": "value"}
            )

    def test_invalidates_when_no_fields_match(self) -> None:
        """Test that no matching fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(["field1", "field2"], 2, "value")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "wrong", "field2": "wrong"}
            )

    def test_invalidates_when_all_fields_missing(self) -> None:
        """Test that missing fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(["field1", "field2"], 1, "value")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_invalidates_when_fields_are_none(self) -> None:
        """Test that None fields don't count as matches."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(["field1", "field2"], 2, "value")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": None})

    def test_validates_when_n_fields_match_none_value(self) -> None:
        """Test that matching None values works correctly."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(["field1", "field2", "field3"], 2, None)
        )
        self.input_filter.validate_data(
            {"field1": None, "field2": None, "field3": "value"}
        )

    def test_invalidates_when_type_mismatch(self) -> None:
        """Test that type mismatches don't count as matches."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(["field1", "field2"], 2, "123")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": 123, "field2": 123})

    def test_validates_with_empty_string_matches(self) -> None:
        """Test that empty strings can be matched."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(["field1", "field2"], 2, "")
        )
        self.input_filter.validate_data({"field1": "", "field2": ""})

    def test_validates_with_integer_matches(self) -> None:
        """Test that integer values can be matched."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(["field1", "field2"], 2, 42)
        )
        self.input_filter.validate_data({"field1": 42, "field2": 42})

    def test_validates_with_n_zero(self) -> None:
        """Test that n=0 validates when no fields match."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(["field1", "field2"], 0, "value")
        )
        self.input_filter.validate_data({"field1": "other", "field2": "other"})

    def test_invalidates_with_partial_matches(self) -> None:
        """Test that partial matches fail when expecting exact count."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add("field4")
        self.input_filter.add_condition(
            ExactlyNOfMatchesCondition(
                ["field1", "field2", "field3", "field4"], 3, "value"
            )
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "wrong", "field3": "value"}
            )
