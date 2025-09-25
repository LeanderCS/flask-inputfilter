import unittest

from flask_inputfilter.declarative import (
    field,
    FieldDescriptor,
)
from flask_inputfilter.filters import StringTrimFilter, ToUpperFilter
from flask_inputfilter.models import ExternalApiConfig
from flask_inputfilter.validators import IsStringValidator, IsIntegerValidator


class TestFieldDescriptor(unittest.TestCase):
    """Test cases for FieldDescriptor functionality."""

    def test_field_descriptor_creation(self):
        """Test basic FieldDescriptor creation."""
        descriptor = field(required=True, default="test")

        self.assertIsInstance(descriptor, FieldDescriptor)
        self.assertTrue(descriptor.required)
        self.assertEqual(descriptor.default, "test")
        self.assertEqual(descriptor.filters, [])
        self.assertEqual(descriptor.validators, [])

    def test_field_descriptor_with_filters_and_validators(self):
        """Test FieldDescriptor with filters and validators."""
        filters = [StringTrimFilter()]
        validators = [IsStringValidator()]

        descriptor = field(
            required=True,
            filters=filters,
            validators=validators
        )

        self.assertEqual(descriptor.filters, filters)
        self.assertEqual(descriptor.validators, validators)

    def test_field_descriptor_with_all_parameters(self):
        """Test FieldDescriptor with all possible parameters."""
        filters = [StringTrimFilter()]
        validators = [IsStringValidator()]
        external_api = ExternalApiConfig(
            url="https://api.example.com/test",
            method="GET",
            data_key="result"
        )

        descriptor = field(
            required=True,
            default="default_value",
            fallback="fallback_value",
            filters=filters,
            validators=validators,
            external_api=external_api,
            copy="other_field"
        )

        self.assertTrue(descriptor.required)
        self.assertEqual(descriptor.default, "default_value")
        self.assertEqual(descriptor.fallback, "fallback_value")
        self.assertEqual(descriptor.filters, filters)
        self.assertEqual(descriptor.validators, validators)
        self.assertEqual(descriptor.external_api, external_api)
        self.assertEqual(descriptor.copy, "other_field")

    def test_field_descriptor_set_name(self):
        """Test __set_name__ functionality."""
        descriptor = field(required=True)

        # Simulate what happens when assigned to a class
        descriptor.__set_name__(object, "test_field")

        self.assertEqual(descriptor.name, "test_field")

    def test_field_descriptor_get_without_instance(self):
        """Test descriptor __get__ without instance."""
        descriptor = field(required=True)

        # Should return descriptor itself when accessed on class
        result = descriptor.__get__(None, object)
        self.assertEqual(result, descriptor)

    def test_field_descriptor_get_with_instance(self):
        """Test descriptor __get__ with instance."""
        descriptor = field(required=True)
        descriptor.name = "test_field"

        # Mock object with validated_data
        mock_obj = type('MockObj', (), {
            'validated_data': {'test_field': 'test_value'}
        })()

        result = descriptor.__get__(mock_obj)
        self.assertEqual(result, 'test_value')

    def test_field_descriptor_get_without_validated_data(self):
        """Test descriptor __get__ without validated_data."""
        descriptor = field(required=True)
        descriptor.name = "test_field"

        # Mock object without validated_data
        mock_obj = type('MockObj', (), {})()

        result = descriptor.__get__(mock_obj)
        self.assertIsNone(result)

    def test_field_descriptor_set(self):
        """Test descriptor __set__ functionality."""
        descriptor = field(required=True)
        descriptor.name = "test_field"

        # Mock object with data attribute
        mock_obj = type('MockObj', (), {'data': {}})()

        # Set value through descriptor
        descriptor.__set__(mock_obj, "test_value")

        self.assertEqual(mock_obj.data["test_field"], "test_value")

    def test_field_descriptor_repr(self):
        """Test string representation of FieldDescriptor."""
        descriptor = field(
            required=True,
            default="test",
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )
        descriptor.name = "test_field"

        repr_str = repr(descriptor)

        self.assertIn("FieldDescriptor", repr_str)
        self.assertIn("test_field", repr_str)
        self.assertIn("required=True", repr_str)
        self.assertIn("filters=1", repr_str)
        self.assertIn("validators=1", repr_str)




class TestFactoryFunctions(unittest.TestCase):
    """Test cases for field factory function."""

    def test_field_factory_function(self):
        """Test field() factory function."""
        # Test with no arguments
        descriptor1 = field()
        self.assertIsInstance(descriptor1, FieldDescriptor)
        self.assertFalse(descriptor1.required)
        self.assertIsNone(descriptor1.default)

        # Test with arguments
        descriptor2 = field(required=True, default="test")
        self.assertTrue(descriptor2.required)
        self.assertEqual(descriptor2.default, "test")


class TestDescriptorIntegration(unittest.TestCase):
    """Integration tests for descriptors working together."""

    def test_field_descriptor_creation(self):
        """Test that field descriptors can be created."""
        # This is a smoke test to ensure field descriptors work
        field_desc = field(required=True, validators=[IsStringValidator()])

        # Should be FieldDescriptor type
        self.assertIsInstance(field_desc, FieldDescriptor)

    def test_descriptor_immutability(self):
        """Test that descriptors maintain their state correctly."""
        descriptor = field(required=True, default="original")

        # Original values should be preserved
        self.assertTrue(descriptor.required)
        self.assertEqual(descriptor.default, "original")

        # Creating another descriptor shouldn't affect the first
        descriptor2 = field(required=False, default="different")

        self.assertTrue(descriptor.required)  # Should still be True
        self.assertEqual(descriptor.default, "original")  # Should still be original
        self.assertFalse(descriptor2.required)
        self.assertEqual(descriptor2.default, "different")


if __name__ == '__main__':
    unittest.main()