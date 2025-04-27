from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import Base64ImageDownscaleFilter
from flask_inputfilter.validators import IsVerticalImageValidator
from tests.validators import BaseValidatorTest


class TestIsVerticalImageValidator(BaseValidatorTest):
    def test_valid_vertical_image(self):
        self.input_filter.add(
            "vertically_image",
            filters=[
                Base64ImageDownscaleFilter(
                    width=100, height=200, proportionally=False
                )
            ],
            validators=[IsVerticalImageValidator()],
        )
        with open("tests/data/base64_image.txt", "r") as file:
            self.input_filter.validateData({"vertically_image": file.read()})

    def test_invalid_not_base64(self):
        self.input_filter.add("image", validators=[IsVerticalImageValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"image": "not_a_base64_image"})

    def test_invalid_horizontal_image(self):
        self.input_filter.add(
            "horizontally_image",
            filters=[
                Base64ImageDownscaleFilter(
                    width=200, height=100, proportionally=False
                )
            ],
            validators=[IsVerticalImageValidator()],
        )
        with open("tests/data/base64_image.txt", "r") as file:
            with self.assertRaises(ValidationError):
                self.input_filter.validateData(
                    {"horizontally_image": file.read()}
                )

    def test_invalid_wrong_type(self):
        self.input_filter.add(
            "vertically_image", validators=[IsVerticalImageValidator()]
        )
        with self.assertRaises(ValidationError):
            self.input_filter.validateData({"vertically_image": 123})

    def test_custom_error_message(self):
        self.input_filter.add(
            "vertically_image",
            validators=[
                IsVerticalImageValidator(error_message="Custom error message")
            ],
        )
        self.assertValidationError(
            "vertically_image", "not_a_base64_image", "Custom error message"
        )
