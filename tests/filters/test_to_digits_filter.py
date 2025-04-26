import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToDigitsFilter


class TestToDigitsFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_string_to_number(self) -> None:
        self.input_filter.add(
            "number", required=True, filters=[ToDigitsFilter()]
        )

        validated_data = self.input_filter.validateData({"number": "25"})
        self.assertEqual(validated_data["number"], 25)

        validated_data = self.input_filter.validateData({"number": "25.3"})
        self.assertEqual(validated_data["number"], 25.3)

    def test_invalid_number_string_remains_string(self) -> None:
        self.input_filter.add(
            "number", required=True, filters=[ToDigitsFilter()]
        )

        validated_data = self.input_filter.validateData({"number": "25.3.3"})
        self.assertIsInstance(validated_data["number"], str)

        validated_data = self.input_filter.validateData(
            {"number": "no number"}
        )
        self.assertIsInstance(validated_data["number"], str)

    def test_non_string_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "number", required=True, filters=[ToDigitsFilter()]
        )

        validated_data = self.input_filter.validateData({"number": 1.23})
        self.assertEqual(validated_data["number"], 1.23)
