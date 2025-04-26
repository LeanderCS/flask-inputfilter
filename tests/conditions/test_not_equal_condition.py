import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import NotEqualCondition
from flask_inputfilter.exceptions import ValidationError


class TestNotEqualCondition(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_validates_when_values_are_not_equal(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(NotEqualCondition("field1", "field2"))
        self.input_filter.validateData(
            {"field1": "value", "field2": "not value"}
        )

    def test_invalidates_when_values_are_equal(self) -> None:
        self.input_filter.add("field1")
        self.input_filter.add("field2")
        self.input_filter.addCondition(NotEqualCondition("field1", "field2"))
        with self.assertRaises(ValidationError):
            self.input_filter.validateData(
                {"field1": "value", "field2": "value"}
            )
