import base64
import io
import unittest

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsImageValidator
from PIL import Image

from tests.validators import BaseValidatorTest


class TestIsImageValidator(BaseValidatorTest):
    def test_valid_pil_image(self) -> None:
        """Should accept PIL Image objects."""
        self.input_filter.add("image", validators=[IsImageValidator()])
        img = Image.new("RGB", (100, 100), color="red")
        self.input_filter.validate_data({"image": img})

    def test_valid_base64_image(self) -> None:
        """Should accept valid base64 encoded images."""
        self.input_filter.add("image", validators=[IsImageValidator()])
        with open("tests/data/base64_image.txt") as file:
            self.input_filter.validate_data({"image": file.read()})

    def test_valid_bytes_image(self) -> None:
        """Should accept valid image bytes."""
        self.input_filter.add("image", validators=[IsImageValidator()])
        img = Image.new("RGB", (100, 100), color="blue")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        self.input_filter.validate_data({"image": image_bytes})

    def test_invalid_string(self) -> None:
        """Should reject invalid strings."""
        self.input_filter.add("image", validators=[IsImageValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"image": "not_an_image"})

    def test_invalid_bytes(self) -> None:
        """Should reject invalid bytes."""
        self.input_filter.add("image", validators=[IsImageValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"image": b"not_an_image"})

    def test_invalid_type(self) -> None:
        """Should reject invalid types."""
        self.input_filter.add("image", validators=[IsImageValidator()])
        with self.assertRaises(ValidationError):
            self.input_filter.validate_data({"image": 123})

    def test_custom_error_message(self) -> None:
        """Should use custom error message."""
        self.input_filter.add(
            "image",
            validators=[IsImageValidator(error_message="Custom error")],
        )
        self.assertValidationError("image", "not_an_image", "Custom error")