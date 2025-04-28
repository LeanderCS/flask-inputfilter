import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import StringLongerThanCondition
from flask_inputfilter.exceptions import ValidationError


class TestStringLongerThanCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_string_is_longer(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )

        self.input_filter.validate_data({"field1": "value", "field2": "val"})

    def test_invalidates_when_string_not_longer(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.add_condition(
            StringLongerThanCondition("field1", "field2")
        )

        with self.assertRaises(ValidationError):
            self.input_filter.validate_data(
                {"field1": "value", "field2": "value"}
            )
