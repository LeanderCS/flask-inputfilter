import unittest
from datetime import date, datetime

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToIsoFilter


class TestToIsoFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_to_iso_string(self) -> None:
        self.input_filter.add("date", filters=[ToIsoFilter()])

        validated_data = self.input_filter.validateData(
            {"date": date(2021, 1, 1)}
        )
        self.assertEqual(validated_data["date"], "2021-01-01")

        validated_data = self.input_filter.validateData(
            {"date": datetime(2021, 1, 1, 12, 0, 0)}
        )
        self.assertEqual(validated_data["date"], "2021-01-01T12:00:00")

        validated_data = self.input_filter.validateData(
            {"date": "2020-01-01T12:00:00"}
        )
        self.assertEqual(validated_data["date"], "2020-01-01T12:00:00")

    def test_non_date_input_remains_unchanged(self) -> None:
        self.input_filter.add("date", filters=[ToIsoFilter()])

        validated_data = self.input_filter.validateData({"date": "no date"})
        self.assertEqual(validated_data["date"], "no date")
