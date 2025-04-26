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
        self.input_filter.addCondition(
            OneOfCondition(["field1", "field2", "field3"])
        )

        self.input_filter.validateData({"field1": "value"})
        self.input_filter.validateData({"field2": "value"})
        self.input_filter.validateData({"field1": "value", "field2": "value"})
        self.input_filter.validateData(
            {"field": "not value", "field2": "value"}
        )

    def test_invalidates_when_no_fields_are_present(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            OneOfCondition(["field1", "field2", "field3"])
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validateData({})
