import unittest
from datetime import date, datetime

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToDateTimeFilter


class TestToDateTimeFilter(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_converts_to_datetime(self) -> None:
        self.input_filter.add(
            "created_at", required=True, filters=[ToDateTimeFilter()]
        )

        validated_data = self.input_filter.validate_data(
            {"created_at": "2021-01-01T12:00:00"}
        )
        self.assertEqual(
            validated_data["created_at"], datetime(2021, 1, 1, 12, 0, 0)
        )

        validated_data = self.input_filter.validate_data(
            {"created_at": date(2021, 1, 1)}
        )
        self.assertEqual(
            validated_data["created_at"], datetime(2021, 1, 1, 0, 0, 0)
        )

        validated_data = self.input_filter.validate_data(
            {"created_at": datetime(2021, 1, 1, 12, 0, 0)}
        )
        self.assertEqual(
            validated_data["created_at"], datetime(2021, 1, 1, 12, 0, 0)
        )

    def test_invalid_input_remains_unchanged(self) -> None:
        self.input_filter.add(
            "created_at", required=True, filters=[ToDateTimeFilter()]
        )
        validated_data = self.input_filter.validate_data(
            {"created_at": "no date"}
        )
        self.assertEqual(validated_data["created_at"], "no date")

        validated_data = self.input_filter.validate_data({"created_at": 123})
        self.assertEqual(validated_data["created_at"], 123)
