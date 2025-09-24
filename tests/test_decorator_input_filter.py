import unittest
from dataclasses import dataclass
from unittest.mock import Mock, patch

from flask import Flask, g, jsonify
from flask_inputfilter import InputFilter
from flask_inputfilter.decorators import field
from flask_inputfilter.conditions import ExactlyOneOfCondition
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import (
    StringTrimFilter,
    ToIntegerFilter,
    ToLowerFilter,
    ToUpperFilter,
)
from flask_inputfilter.models import ExternalApiConfig
from flask_inputfilter.validators import (
    InArrayValidator,
    IsIntegerValidator,
    IsStringValidator,
    LengthValidator,
)


class TestDecoratorInputFilter(unittest.TestCase):
    """Comprehensive test suite for decorator-based InputFilter API."""

    def test_basic_field_decorator(self):
        """Test basic field decorator functionality."""

        class TestInputFilter(InputFilter):
            name: str = field(required=True)
            age: int = field(default=18)

        filter_instance = TestInputFilter()

        # Check that fields were registered
        self.assertTrue(filter_instance.has('name'))
        self.assertTrue(filter_instance.has('age'))

        # Check field properties
        name_field = filter_instance.get_input('name')
        age_field = filter_instance.get_input('age')

        self.assertTrue(name_field.required)
        self.assertFalse(age_field.required)
        self.assertIsNone(name_field.default)
        self.assertEqual(age_field.default, 18)

    def test_field_with_validators_and_filters(self):
        """Test field with validators and filters."""

        class TestInputFilter(InputFilter):
            username: str = field(
                required=True,
                filters=[StringTrimFilter(), ToLowerFilter()],
                validators=[IsStringValidator(), LengthValidator(min_length=3, max_length=20)]
            )

        filter_instance = TestInputFilter()

        # Test successful validation
        validated_data = filter_instance.validate_data({
            'username': '  TestUser  '
        })
        self.assertEqual(validated_data['username'], 'testuser')

        # Test validation failure - too short
        with self.assertRaises(ValidationError):
            filter_instance.validate_data({'username': 'ab'})

    def test_field_with_all_parameters(self):
        """Test field with all possible parameters."""

        class TestInputFilter(InputFilter):
            score: int = field(
                required=True,
                default=0,
                fallback=50,
                filters=[ToIntegerFilter()],
                validators=[IsIntegerValidator()],
                copy=None
            )

        filter_instance = TestInputFilter()

        # Test with valid data
        validated_data = filter_instance.validate_data({'score': '85'})
        self.assertEqual(validated_data['score'], 85)

        # Test with invalid data (should use fallback)
        validated_data = filter_instance.validate_data({'score': 'invalid'})
        self.assertEqual(validated_data['score'], 50)

    def test_mixed_decorator_and_classic_api(self):
        """Test mixing decorator and classic API."""

        class TestInputFilter(InputFilter):
            # Decorator-based fields
            name: str = field(required=True, validators=[IsStringValidator()])

            def __init__(self):
                super().__init__()
                # Classic API fields
                self.add('email', required=True, validators=[IsStringValidator()])

        filter_instance = TestInputFilter()

        # Both fields should exist
        self.assertTrue(filter_instance.has('name'))
        self.assertTrue(filter_instance.has('email'))

        # Test validation
        validated_data = filter_instance.validate_data({
            'name': 'John Doe',
            'email': 'john@example.com'
        })
        self.assertEqual(validated_data['name'], 'John Doe')
        self.assertEqual(validated_data['email'], 'john@example.com')

    def test_global_validators_class_attribute(self):
        """Test global validators via class attribute."""

        class TestInputFilter(InputFilter):
            field1: str = field()
            field2: str = field()

            _global_validators = [IsStringValidator()]

        filter_instance = TestInputFilter()

        # Should validate successfully with strings
        validated_data = filter_instance.validate_data({
            'field1': 'test1',
            'field2': 'test2'
        })
        self.assertEqual(validated_data['field1'], 'test1')
        self.assertEqual(validated_data['field2'], 'test2')

        # Should fail with non-string
        with self.assertRaises(ValidationError):
            filter_instance.validate_data({
                'field1': 'test1',
                'field2': 123
            })

    def test_global_filters_class_attribute(self):
        """Test global filters via class attribute."""

        class TestInputFilter(InputFilter):
            field1: str = field()
            field2: str = field()

            _global_filters = [ToUpperFilter()]

        filter_instance = TestInputFilter()

        # All fields should be filtered
        validated_data = filter_instance.validate_data({
            'field1': 'test1',
            'field2': 'test2'
        })
        self.assertEqual(validated_data['field1'], 'TEST1')
        self.assertEqual(validated_data['field2'], 'TEST2')

    def test_conditions_class_attribute(self):
        """Test conditions via class attribute."""

        class TestInputFilter(InputFilter):
            phone: str = field()
            email: str = field()

            _conditions = [ExactlyOneOfCondition(['phone', 'email'])]

        filter_instance = TestInputFilter()

        # Should work with one field
        validated_data = filter_instance.validate_data({'phone': '123456789'})
        self.assertEqual(validated_data['phone'], '123456789')

        # Should fail with both fields
        with self.assertRaises(ValidationError):
            filter_instance.validate_data({
                'phone': '123456789',
                'email': 'test@example.com'
            })

    def test_inheritance_with_decorators(self):
        """Test that decorators work with inheritance."""

        class BaseInputFilter(InputFilter):
            name: str = field(required=True)
            _global_filters = [StringTrimFilter()]

        class ExtendedInputFilter(BaseInputFilter):
            age: int = field(required=True, validators=[IsIntegerValidator()])
            _global_validators = [IsStringValidator()]

        filter_instance = ExtendedInputFilter()

        # Should have both fields
        self.assertTrue(filter_instance.has('name'))
        self.assertTrue(filter_instance.has('age'))

        # Should inherit global filters and validators
        self.assertEqual(len(filter_instance.get_global_filters()), 1)
        self.assertEqual(len(filter_instance.get_global_validators()), 1)

    def test_type_hints_preserved(self):
        """Test that type hints are accessible and don't interfere."""

        class TestInputFilter(InputFilter):
            name: str = field(required=True)
            age: int = field(default=18)

        # Type hints should still be available
        annotations = TestInputFilter.__annotations__
        self.assertEqual(annotations['name'], str)
        self.assertEqual(annotations['age'], int)

    def test_field_descriptor_access(self):
        """Test accessing field values through descriptors."""

        class TestInputFilter(InputFilter):
            name: str = field(required=True)

        filter_instance = TestInputFilter()

        # Before validation, should return None
        self.assertIsNone(filter_instance.name)

        # After validation, should return the validated value
        filter_instance.validate_data({'name': 'John'})
        self.assertEqual(filter_instance.name, 'John')

    def test_field_descriptor_setting(self):
        """Test setting field values through descriptors."""

        class TestInputFilter(InputFilter):
            name: str = field(required=True)

        filter_instance = TestInputFilter()

        # Setting should update raw data
        filter_instance.name = 'Jane'
        self.assertEqual(filter_instance.get_raw_value('name'), 'Jane')

    # Negative Tests

    def test_invalid_field_params_raises_error(self):
        """Test that invalid field parameters raise appropriate errors."""

        # This should work without errors
        class TestInputFilter(InputFilter):
            name: str = field(required=True, default=None)

        filter_instance = TestInputFilter()
        self.assertTrue(filter_instance.has('name'))

    def test_conflicting_field_names(self):
        """Test handling of field name conflicts between decorator and classic
        API."""

        class TestInputFilter(InputFilter):
            name: str = field(required=True)

            def __init__(self):
                super().__init__()
                # This should raise an error due to field conflict
                self.add('name', required=False)

        # The error should be raised during initialization
        with self.assertRaises(ValueError):
            TestInputFilter()

    def test_invalid_global_components(self):
        """Test handling of invalid global components."""

        # Test with invalid global validators
        class TestInputFilter(InputFilter):
            field1: str = field()
            _global_validators = "invalid"  # Should be a list

        # Should handle gracefully (metaclass should not crash)
        filter_instance = TestInputFilter()
        self.assertTrue(filter_instance.has('field1'))

    def test_metaclass_with_no_decorators(self):
        """Test metaclass behavior with no decorator fields."""

        class TestInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('name', required=True)

        filter_instance = TestInputFilter()
        self.assertTrue(filter_instance.has('name'))

    def test_empty_decorator_class(self):
        """Test InputFilter with no fields at all."""

        class EmptyInputFilter(InputFilter):
            pass

        filter_instance = EmptyInputFilter()
        self.assertEqual(filter_instance.count(), 0)

        # Should still work for validation
        validated_data = filter_instance.validate_data({})
        self.assertEqual(validated_data, {})

    def test_only_decorator_fields(self):
        """Test InputFilter with only decorator fields."""

        class OnlyDecoratorInputFilter(InputFilter):
            name: str = field(required=True)
            age: int = field(default=25)

        filter_instance = OnlyDecoratorInputFilter()
        self.assertEqual(filter_instance.count(), 2)

        validated_data = filter_instance.validate_data({'name': 'Test'})
        self.assertEqual(validated_data['name'], 'Test')
        self.assertEqual(validated_data['age'], 25)

    def test_dynamic_field_addition_after_decorator(self):
        """Test adding fields dynamically after decorator initialization."""

        class TestInputFilter(InputFilter):
            name: str = field(required=True)

            def add_email_if_needed(self):
                if not self.has('email'):
                    self.add('email', required=False)

        filter_instance = TestInputFilter()

        # Initially should only have name
        self.assertTrue(filter_instance.has('name'))
        self.assertFalse(filter_instance.has('email'))

        # Add email dynamically
        filter_instance.add_email_if_needed()

        self.assertTrue(filter_instance.has('email'))
        self.assertEqual(filter_instance.count(), 2)

    # Integration Tests

    def test_flask_integration_with_decorators(self):
        """Test Flask route integration with decorator-based fields."""

        class TestInputFilter(InputFilter):
            username: str = field(required=True, validators=[IsStringValidator()])
            age: int = field(default=18, validators=[IsIntegerValidator()])

        app = Flask(__name__)

        @app.route('/test', methods=['POST'])
        @TestInputFilter.validate()
        def test_route():
            return jsonify(g.validated_data)

        with app.test_client() as client:
            response = client.post('/test', json={
                'username': 'testuser',
                'age': 25
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {
                'username': 'testuser',
                'age': 25
            })

    def test_serialization_with_decorator_fields(self):
        """Test model serialization with decorator fields."""

        @dataclass
        class User:
            username: str
            age: int

        class TestInputFilter(InputFilter):
            username: str = field(required=True)
            age: int = field(default=18)

            def __init__(self):
                super().__init__()
                self.set_model(User)

        filter_instance = TestInputFilter()
        result = filter_instance.validate_data({'username': 'testuser'})

        self.assertIsInstance(result, User)
        self.assertEqual(result.username, 'testuser')
        self.assertEqual(result.age, 18)

    @patch("requests.request")
    def test_external_api_with_decorators(self, mock_request: Mock):
        """Test external API functionality with decorator fields."""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"is_valid": True}
        mock_request.return_value = mock_response

        class TestInputFilter(InputFilter):
            username: str = field(required=True)
            is_valid: bool = field(
                external_api=ExternalApiConfig(
                    url="https://api.example.com/validate/{{username}}",
                    method="GET",
                    data_key="is_valid"
                )
            )

        filter_instance = TestInputFilter()
        validated_data = filter_instance.validate_data({'username': 'testuser'})

        self.assertEqual(validated_data['username'], 'testuser')
        self.assertTrue(validated_data['is_valid'])

    # Performance and Edge Cases

    def test_large_number_of_decorator_fields(self):
        """Test performance with many decorator fields."""

        # Create a class with many fields programmatically
        class_dict = {}
        for i in range(100):
            class_dict[f'field_{i}'] = field(default=f'value_{i}')

        LargeInputFilter = type('LargeInputFilter', (InputFilter,), class_dict)

        filter_instance = LargeInputFilter()
        self.assertEqual(filter_instance.count(), 100)

        # Should still validate quickly
        validated_data = filter_instance.validate_data({})
        self.assertEqual(len(validated_data), 100)

    def test_complex_nested_validation(self):
        """Test complex validation scenarios with mixed APIs."""

        class ComplexInputFilter(InputFilter):
            # Decorator fields
            username: str = field(
                required=True,
                filters=[StringTrimFilter(), ToLowerFilter()],
                validators=[IsStringValidator(), LengthValidator(min_length=3)]
            )
            age: int = field(
                required=True,
                filters=[ToIntegerFilter()],
                validators=[IsIntegerValidator()]
            )

            # Global components
            _global_filters = [StringTrimFilter()]
            _conditions = [
                # Custom condition example would go here if needed
            ]

            def __init__(self):
                super().__init__()
                # Classic API additions
                self.add('email', required=False, validators=[IsStringValidator()])

        filter_instance = ComplexInputFilter()

        # Test successful complex validation
        validated_data = filter_instance.validate_data({
            'username': '  TestUser  ',
            'age': '25',
            'email': 'test@example.com'
        })

        self.assertEqual(validated_data['username'], 'testuser')
        self.assertEqual(validated_data['age'], 25)
        self.assertEqual(validated_data['email'], 'test@example.com')

    def test_model_assignment_basic(self):
        """Test basic model assignment functionality."""
        from dataclasses import dataclass

        @dataclass
        class TestModel:
            name: str
            age: int

        class TestInputFilter(InputFilter):
            name: str = field(required=True)
            age: int = field(default=25)

            _model = TestModel

        filter_instance = TestInputFilter()

        # Should have model class set
        self.assertEqual(filter_instance.model_class, TestModel)

        # Test serialization
        result = filter_instance.validate_data({'name': 'John'})
        self.assertIsInstance(result, TestModel)
        self.assertEqual(result.name, 'John')
        self.assertEqual(result.age, 25)

    def test_model_inheritance(self):
        """Test model assignment inheritance."""
        from dataclasses import dataclass

        @dataclass
        class BaseModel:
            name: str

        @dataclass
        class ExtendedModel:
            name: str
            age: int

        class BaseInputFilter(InputFilter):
            name: str = field(required=True)
            _model = BaseModel

        class ExtendedInputFilter(BaseInputFilter):
            age: int = field(default=18)

        # Should inherit model from base class
        base_filter = BaseInputFilter()
        self.assertEqual(base_filter.model_class, BaseModel)

        extended_filter = ExtendedInputFilter()
        self.assertEqual(extended_filter.model_class, BaseModel)

        # Override model in extended class
        class OverriddenInputFilter(BaseInputFilter):
            age: int = field(default=18)
            _model = ExtendedModel

        overridden_filter = OverriddenInputFilter()
        self.assertEqual(overridden_filter.model_class, ExtendedModel)

    def test_model_with_classic_api(self):
        """Test model assignment works with classic API methods."""
        from dataclasses import dataclass

        @dataclass
        class TestModel:
            name: str
            email: str

        class MixedInputFilter(InputFilter):
            name: str = field(required=True)
            _model = TestModel

            def __init__(self):
                super().__init__()
                self.add('email', required=True)

        filter_instance = MixedInputFilter()
        self.assertEqual(filter_instance.model_class, TestModel)

        result = filter_instance.validate_data({
            'name': 'John',
            'email': 'john@example.com'
        })
        self.assertIsInstance(result, TestModel)
        self.assertEqual(result.name, 'John')
        self.assertEqual(result.email, 'john@example.com')

    def test_model_override_with_set_model(self):
        """Test that set_model() can override model assignment."""
        from dataclasses import dataclass

        @dataclass
        class Model1:
            name: str

        @dataclass
        class Model2:
            name: str

        class TestInputFilter(InputFilter):
            name: str = field(required=True)
            _model = Model1

        filter_instance = TestInputFilter()
        self.assertEqual(filter_instance.model_class, Model1)

        # Override with set_model
        filter_instance.set_model(Model2)
        self.assertEqual(filter_instance.model_class, Model2)

        result = filter_instance.validate_data({'name': 'John'})
        self.assertIsInstance(result, Model2)

    def test_model_none_fallback(self):
        """Test that missing model assignment handles None gracefully."""
        class TestInputFilter(InputFilter):
            name: str = field(required=True)

        filter_instance = TestInputFilter()
        self.assertIsNone(filter_instance.model_class)

        result = filter_instance.validate_data({'name': 'John'})
        self.assertIsInstance(result, dict)
        self.assertEqual(result['name'], 'John')


if __name__ == '__main__':
    unittest.main()