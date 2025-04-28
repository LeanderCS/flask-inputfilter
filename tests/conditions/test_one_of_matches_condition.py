import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import OneOfMatchesCondition
from flask_inputfilter.exceptions import ValidationError


class TestOneOfMatchesCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_at_least_one_field_matches(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], "value")
        )

        self.input_filter.validate_data({"field1": "value"})
        self.input_filter.validate_data({"field2": "value"})
        self.input_filter.validate_data({"field1": "value", "field2": "value"})

    def test_invalidates_when_no_fields_match(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfMatchesCondition(["field1", "field2"], "value")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field": "not value"})
