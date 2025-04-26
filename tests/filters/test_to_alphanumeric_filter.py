import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToAlphaNumericFilter


class TestToAlphaNumericFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_removes_non_alphanumeric_characters(self) -> None:
        self.input_filter.add(
            "alphanumeric_field",
            required=False,
            filters=[ToAlphaNumericFilter()],
        )
        validated_data = self.input_filter.validateData(
            {"alphanumeric_field": "Hello World!123"}
        )
        self.assertEqual(validated_data["alphanumeric_field"], "HelloWorld123")

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "alphanumeric_field",
            required=False,
            filters=[ToAlphaNumericFilter()],
        )
        validated_data = self.input_filter.validateData(
            {"alphanumeric_field": 123}
        )
        self.assertEqual(validated_data["alphanumeric_field"], 123)
