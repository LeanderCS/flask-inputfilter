import unittest
from datetime import date, datetime

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToDateFilter


class TestToDateFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_to_date(self) -> None:
        self.input_filter.add("dob", required=True, filters=[ToDateFilter()])

        validated_data = self.input_filter.validate_data({"dob": "1996-12-01"})
        self.assertEqual(validated_data["dob"], date(1996, 12, 1))

        validated_data = self.input_filter.validate_data(
            {"dob": date(1996, 12, 1)}
        )
        self.assertEqual(validated_data["dob"], date(1996, 12, 1))

        validated_data = self.input_filter.validate_data(
            {"dob": datetime(1996, 12, 1, 12, 0, 0)}
        )
        self.assertEqual(validated_data["dob"], date(1996, 12, 1))

    def test_invalid_input_remains_unchanged(self) -> None:
        self.input_filter.add("dob", required=True, filters=[ToDateFilter()])
        validated_data = self.input_filter.validate_data({"dob": "no date"})
        self.assertEqual(validated_data["dob"], "no date")

        validated_data = self.input_filter.validate_data({"dob": 123})
        self.assertEqual(validated_data["dob"], 123)
