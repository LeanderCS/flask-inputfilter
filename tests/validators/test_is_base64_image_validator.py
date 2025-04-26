import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsBase64ImageValidator


class TestIsBase64ImageValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.input_filter = InputFilter()

    def test_valid_base64_image(self) -> None:
        self.input_filter.add("image", validators=[IsBase64ImageValidator()])
        with open("tests/data/base64_image.txt", "r") as file:
            self.input_filter.validateData({"image": file.read()})

    def test_invalid_base64_image(self) -> None:
        self.input_filter.add("image", validators=[IsBase64ImageValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"image": "not_base64"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "image2",
            validators=[IsBase64ImageValidator(error_message="Custom error")],
        )
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validateData({"image2": "not_base64"})
        self.assertEqual(context.exception.args[0]["image2"], "Custom error")
