from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsBase64ImageValidator
from tests.validators import BaseValidatorTest


class TestIsBase64ImageValidator(BaseValidatorTest):
    def test_valid_base64_image(self) -> None:
        self.input_filter.add("image", validators=[IsBase64ImageValidator()])
        with open("tests/data/base64_image.txt", "r") as file:
            self.input_filter.validate_data({"image": file.read()})

    def test_invalid_base64_image(self) -> None:
        self.input_filter.add("image", validators=[IsBase64ImageValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"image": "not_base64"})

    def test_custom_error_message(self) -> None:
        self.input_filter.add(
            "image2",
            validators=[IsBase64ImageValidator(error_message="Custom error")],
        )
        self.assertValidationError("image2", "not_base64", "Custom error")
