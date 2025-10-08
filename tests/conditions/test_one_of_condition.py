import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import OneOfCondition
from flask_inputfilter.exceptions import ValidationError


class TestOneOfCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_one_field_is_present(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfCondition(["field1", "field2", "field3"])
        )

        self.input_filter.validate_data({"field1": "value"})
        self.input_filter.validate_data({"field2": "value"})
        self.input_filter.validate_data({"field1": "value", "field2": "value"})
        self.input_filter.validate_data(
            {"field": "not value", "field2": "value"}
        )

    def test_invalidates_when_no_fields_are_present(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfCondition(["field1", "field2", "field3"])
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({})

    def test_validates_when_only_one_field_is_present(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            OneOfCondition(["field1", "field2", "field3"])
        )
        self.input_filter.validate_data({"field3": "value"})

    def test_invalidates_when_fields_contain_only_none(self) -> None:
        """None values don't count as 'present' in OneOfCondition."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfCondition(["field1", "field2"])
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": None})

    def test_validates_when_fields_contain_empty_strings(self) -> None:
        """Empty strings DO count as 'present' in OneOfCondition."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfCondition(["field1", "field2"])
        )
        self.input_filter.validate_data({"field1": ""})

    def test_validates_when_fields_contain_zero(self) -> None:
        """Zero DOES count as 'present' in OneOfCondition."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfCondition(["field1", "field2"])
        )
        self.input_filter.validate_data({"field1": 0})

    def test_validates_when_fields_contain_false(self) -> None:
        """False DOES count as 'present' in OneOfCondition."""
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            OneOfCondition(["field1", "field2"])
        )
        self.input_filter.validate_data({"field1": False})

    def test_validates_with_multiple_fields_present(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add("field3")
        self.input_filter.add_condition(
            OneOfCondition(["field1", "field2", "field3"])
        )
        self.input_filter.validate_data(
            {"field1": "value1", "field2": "value2", "field3": "value3"}
        )
