import unittest
from datetime import date, datetime

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import TemporalOrderCondition
from flask_inputfilter.exceptions import ValidationError


class TestTemporalOrderCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_first_date_before_second(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            TemporalOrderCondition("field1", "field2")
        )

        self.input_filter.validateData(
            {"field1": "2021-01-01", "field2": "2021-01-02"}
        )
        self.input_filter.validateData(
            {
                "field1": datetime(2021, 1, 1, 12, 0, 0),
                "field2": datetime(2021, 1, 2, 12, 0, 0),
            }
        )

    def test_invalidates_when_first_date_after_second(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            TemporalOrderCondition("field1", "field2")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"field1": "2021-01-02", "field2": "2021-01-01"}
            )

    def test_invalidates_when_type_mismatch(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            TemporalOrderCondition("field1", "field2")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"field1": date(2023, 1, 1), "field2": "2021-01-01"}
            )

    def test_invalidates_when_field_missing(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            TemporalOrderCondition("field1", "field2")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"field1": "2021-01-01"})

    def test_invalidates_when_not_a_datetime(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(
            TemporalOrderCondition("field1", "field2")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"field1": "not a datetime"})
