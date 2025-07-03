import base64
import io
import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.enums import ImageFormatEnum
from flask_inputfilter.filters import ToBase64ImageFilter
from PIL import Image


class TestToBase64ImageFilter(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a new InputFilter instance before each test."""
        self.input_filter = InputFilter()

    def test_pil_image_to_base64(self) -> None:
        """Should convert PIL Image to base64 string."""
        self.input_filter.add("image", filters=[ToBase64ImageFilter()])
        img = Image.new("RGB", (100, 100), color="red")
        validated_data = self.input_filter.validate_data({"image": img})
        
        # Verify it's a base64 string
        result = validated_data["image"]
        self.assertIsInstance(result, str)
        
        # Verify it can be decoded back to an image
        decoded_img = Image.open(io.BytesIO(base64.b64decode(result)))
        self.assertEqual(decoded_img.size, (100, 100))

    def test_bytes_to_base64(self) -> None:
        """Should convert image bytes to base64 string."""
        self.input_filter.add("image", filters=[ToBase64ImageFilter()])
        img = Image.new("RGB", (50, 50), color="blue")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        
        validated_data = self.input_filter.validate_data({"image": image_bytes})
        
        # Verify it's a base64 string
        result = validated_data["image"]
        self.assertIsInstance(result, str)
        
        # Verify it can be decoded back to an image
        decoded_img = Image.open(io.BytesIO(base64.b64decode(result)))
        self.assertEqual(decoded_img.size, (50, 50))

    def test_existing_base64_unchanged(self) -> None:
        """Should return existing base64 strings unchanged."""
        self.input_filter.add("image", filters=[ToBase64ImageFilter()])
        with open("tests/data/base64_image.txt") as file:
            original_base64 = file.read()
        
        validated_data = self.input_filter.validate_data({"image": original_base64})
        self.assertEqual(validated_data["image"], original_base64)

    def test_jpeg_format(self) -> None:
        """Should convert to JPEG format when specified."""
        self.input_filter.add(
            "image", 
            filters=[ToBase64ImageFilter(format=ImageFormatEnum.JPEG)]
        )
        img = Image.new("RGB", (100, 100), color="green")
        validated_data = self.input_filter.validate_data({"image": img})
        
        # Verify it's a base64 string and can be decoded as JPEG
        result = validated_data["image"]
        decoded_img = Image.open(io.BytesIO(base64.b64decode(result)))
        self.assertEqual(decoded_img.format, "JPEG")

    def test_non_image_input_unchanged(self) -> None:
        """Should return non-image inputs unchanged."""
        self.input_filter.add("image", filters=[ToBase64ImageFilter()])
        
        # Test with string
        validated_data = self.input_filter.validate_data({"image": "not_an_image"})
        self.assertEqual(validated_data["image"], "not_an_image")
        
        # Test with number
        validated_data = self.input_filter.validate_data({"image": 123})
        self.assertEqual(validated_data["image"], 123)

    def test_quality_parameter(self) -> None:
        """Should use quality parameter for JPEG images."""
        self.input_filter.add(
            "image", 
            filters=[ToBase64ImageFilter(
                format=ImageFormatEnum.JPEG, 
                quality=50
            )]
        )
        img = Image.new("RGB", (100, 100), color="red")
        validated_data = self.input_filter.validate_data({"image": img})
        
        # Verify it's a base64 string
        result = validated_data["image"]
        self.assertIsInstance(result, str)
        
        # Verify it can be decoded back to an image
        decoded_img = Image.open(io.BytesIO(base64.b64decode(result)))
        self.assertEqual(decoded_img.format, "JPEG")