import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ExactlyOneOfMatchesCondition
from flask_inputfilter.exceptions import ValidationError


class TestExactlyOneOfMatchesCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_exactly_one_field_matches(self) -> None:
        """Test that exactly one field matches the value."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], "value")
        )
        self.input_filter.validate_data({"field1": "value"})

    def test_invalidates_when_more_than_one_field_matches(self) -> None:
        """Test that more than one matching field raises a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], "value")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "value"}
            )

    def test_invalidates_when_no_fields_match(self) -> None:
        """Test that no matching fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], "value")
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
            ExactlyOneOfMatchesCondition(["field1", "field2"], "value")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_invalidates_when_all_fields_are_none(self) -> None:
        """Test that None fields don't count as matches."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], "value")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": None})

    def test_validates_when_one_field_matches_none_value(self) -> None:
        """Test that matching None value works correctly."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], None)
        )
        self.input_filter.validate_data({"field1": None, "field2": "value"})

    def test_invalidates_when_both_fields_match_none(self) -> None:
        """Test that both fields matching None raises ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], None)
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None, "field2": None})

    def test_invalidates_when_type_mismatch(self) -> None:
        """Test that type mismatches don't count as matches."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], "123")
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": 123, "field2": 456})

    def test_validates_with_empty_string_match(self) -> None:
        """Test that empty string matching works correctly."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], "")
        )
        self.input_filter.validate_data({"field1": "", "field2": "value"})

    def test_validates_with_integer_match(self) -> None:
        """Test that integer matching works correctly."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            ExactlyOneOfMatchesCondition(["field1", "field2"], 42)
        )
        self.input_filter.validate_data({"field1": 42, "field2": 0})

    def test_invalidates_when_all_three_fields_match(self) -> None:
        """Test that three matching fields raise a ValidationError."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            ExactlyOneOfMatchesCondition(
                ["field1", "field2", "field3"], "value"
            )
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "value", "field3": "value"}
            )
