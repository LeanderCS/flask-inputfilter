import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsTypedDictValidator

# TODO: Readd when Python 3.7 support is dropped
# class User(TypedDict):
#     id: int


class User:
    __annotations__ = {"id": int}

    def __init__(self, id: int):
        self.id = id

    def __eq__(self, other):
        if isinstance(other, dict):
            return other == {"id": self.id}
        return NotImplemented


class TestIsTypedDictValidator(unittest.TestCase):
    def setUp(self):
        self.input_filter = InputFilter()

    def test_valid_typed_dict(self):
        self.input_filter.add("data", validators=[IsTypedDictValidator(User)])
        self.input_filter.validateData({"data": {"id": 123}})

    def test_invalid_typed_dict(self):
        self.input_filter.add("data", validators=[IsTypedDictValidator(User)])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"data": "not a dict"})

    def test_custom_error_message(self):
        self.input_filter.add(
            "data2",
            validators=[
                IsTypedDictValidator(
                    User, error_message="Custom error message"
                )
            ],
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"data2": "not a dict"})
