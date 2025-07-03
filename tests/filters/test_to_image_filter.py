import base64
import io
import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToImageFilter
from PIL import Image


class TestToImageFilter(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a new InputFilter instance before each test."""
        self.input_filter = InputFilter()

    def test_pil_image_unchanged(self) -> None:
        """Should return PIL Image objects unchanged."""
        self.input_filter.add("image", filters=[ToImageFilter()])
        img = Image.new("RGB", (100, 100), color="red")
        validated_data = self.input_filter.validate_data({"image": img})
        
        result = validated_data["image"]
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (100, 100))

    def test_base64_to_image(self) -> None:
        """Should convert base64 strings to PIL Image objects."""
        self.input_filter.add("image", filters=[ToImageFilter()])
        with open("tests/data/base64_image.txt") as file:
            base64_string = file.read()
        
        validated_data = self.input_filter.validate_data({"image": base64_string})
        
        result = validated_data["image"]
        self.assertIsInstance(result, Image.Image)
        self.assertTrue(hasattr(result, 'size'))

    def test_bytes_to_image(self) -> None:
        """Should convert image bytes to PIL Image objects."""
        self.input_filter.add("image", filters=[ToImageFilter()])
        
        # Create image bytes
        img = Image.new("RGB", (50, 50), color="blue")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        
        validated_data = self.input_filter.validate_data({"image": image_bytes})
        
        result = validated_data["image"]
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (50, 50))

    def test_invalid_string_unchanged(self) -> None:
        """Should return invalid strings unchanged."""
        self.input_filter.add("image", filters=[ToImageFilter()])
        
        validated_data = self.input_filter.validate_data({"image": "not_an_image"})
        self.assertEqual(validated_data["image"], "not_an_image")

    def test_invalid_bytes_unchanged(self) -> None:
        """Should return invalid bytes unchanged."""
        self.input_filter.add("image", filters=[ToImageFilter()])
        
        validated_data = self.input_filter.validate_data({"image": b"not_an_image"})
        self.assertEqual(validated_data["image"], b"not_an_image")

    def test_non_image_input_unchanged(self) -> None:
        """Should return non-image inputs unchanged."""
        self.input_filter.add("image", filters=[ToImageFilter()])
        
        # Test with number
        validated_data = self.input_filter.validate_data({"image": 123})
        self.assertEqual(validated_data["image"], 123)
        
        # Test with list
        validated_data = self.input_filter.validate_data({"image": [1, 2, 3]})
        self.assertEqual(validated_data["image"], [1, 2, 3])

    def test_preserve_image_properties(self) -> None:
        """Should preserve image properties when converting."""
        self.input_filter.add("image", filters=[ToImageFilter()])
        
        # Create a colored image
        original_img = Image.new("RGB", (200, 150), color="green")
        buffer = io.BytesIO()
        original_img.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        
        validated_data = self.input_filter.validate_data({"image": image_bytes})
        
        result = validated_data["image"]
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (200, 150))
        self.assertEqual(result.mode, "RGB")