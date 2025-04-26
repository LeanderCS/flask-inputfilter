import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsFloatValidator


class TestIsFloatValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_float(self) -> None:
        self.input_filter.add("price", validators=[IsFloatValidator()])
        self.input_filter.validateData({"price": 19.99})

    def test_invalid_float(self) -> None:
        self.input_filter.add("price", validators=[IsFloatValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"price": "not_a_float"})
