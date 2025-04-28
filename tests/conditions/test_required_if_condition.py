import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import RequiredIfCondition
from flask_inputfilter.exceptions import ValidationError


class TestRequiredIfCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_required_if_single_value(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            RequiredIfCondition("field1", "value", "field2")
        )

        self.input_filter.validate_data({"field1": "not value"})
        self.input_filter.validate_data({"field2": "value"})
        self.input_filter.validate_data(
            {"field1": "value", "field2": "other value"}
        )

    def test_invalidates_when_required_field_missing_single_value(
        self,
    ) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            RequiredIfCondition("field1", "value", "field2")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field1": "value"})

    def test_required_if_list_of_values(self) -> None:
        self.input_filter.add("field3")
        self.input_filter.add("field4")
        self.input_filter.add_condition(
            RequiredIfCondition("field3", ["value1", "value2"], "field4")
        )

        self.input_filter.validate_data({"field4": "value2"})
        self.input_filter.validate_data(
            {"field3": "value1", "field4": "value"}
        )
        self.input_filter.validate_data(
            {"field3": "value2", "field4": "value"}
        )

    def test_invalidates_when_required_field_missing_list_of_values(
        self,
    ) -> None:
        self.input_filter.add("field3")
        self.input_filter.add("field4")
        self.input_filter.add_condition(
            RequiredIfCondition("field3", ["value1", "value2"], "field4")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field3": "value1"})

    def test_required_if_none_value(self) -> None:
        self.input_filter.add("field5")
        self.input_filter.add("field6")
        self.input_filter.add_condition(
            RequiredIfCondition("field5", None, "field6")
        )

        self.input_filter.validate_data({"field6": "value"})
        self.input_filter.validate_data(
            {"field5": "any_value", "field6": "value"}
        )

    def test_invalidates_when_required_field_missing_none_value(self) -> None:
        self.input_filter.add("field5")
        self.input_filter.add("field6")
        self.input_filter.add_condition(
            RequiredIfCondition("field5", None, "field6")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"field5": "any_value"})
