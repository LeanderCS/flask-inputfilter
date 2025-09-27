import unittest

from flask import Flask, g, jsonify
from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.conditions import ExactlyOneOfCondition
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import StringTrimFilter, ToLowerFilter, ToUpperFilter
from flask_inputfilter.validators import IsIntegerValidator, IsStringValidator, LengthValidator


class TestMixedAPI(unittest.TestCase):
    """Test cases for mixing decorator-based and classic API."""

    def test_basic_mixed_usage(self):
        """Test basic combination of decorator and classic API."""

        class MixedInputFilter(InputFilter):
            # Decorator-based fields
            name: str = field(required=True, validators=[IsStringValidator()])

            def __init__(self):
                super().__init__()
                # Classic API fields
                self.add('age', required=True, validators=[IsIntegerValidator()])

        filter_instance = MixedInputFilter()

        # Both fields should exist
        self.assertTrue(filter_instance.has('name'))
        self.assertTrue(filter_instance.has('age'))
        self.assertEqual(filter_instance.count(), 2)

        # Test validation
        validated_data = filter_instance.validate_data({
            'name': 'John Doe',
            'age': 30
        })
        self.assertEqual(validated_data['name'], 'John Doe')
        self.assertEqual(validated_data['age'], 30)

    def test_decorator_overrides_prevention(self):
        """Test that classic API cannot override decorator fields."""

        class MixedInputFilter(InputFilter):
            name: str = field(required=True)

            def __init__(self):
                super().__init__()
                # This should raise an error
                self.add('name', required=False)

        # Test during initialization
        with self.assertRaises(ValueError):
            MixedInputFilter()

    def test_mixed_global_components(self):
        """Test mixing global components from both APIs."""

        class MixedInputFilter(InputFilter):
            field1: str = field()
            field2: str = field()

            # Decorator-based global components
            _global_filters = [StringTrimFilter()]
            _global_validators = [IsStringValidator()]

            def __init__(self):
                super().__init__()
                # Classic API global components
                self.add_global_filter(ToUpperFilter())
                self.add_global_validator(LengthValidator(min_length=1))

        filter_instance = MixedInputFilter()

        # Should have both global filters and validators
        self.assertEqual(len(filter_instance.get_global_filters()), 2)
        self.assertEqual(len(filter_instance.get_global_validators()), 2)

        # Test that both are applied
        validated_data = filter_instance.validate_data({
            'field1': '  test  ',
            'field2': '  another  '
        })
        # Should be trimmed and uppercased
        self.assertEqual(validated_data['field1'], 'TEST')
        self.assertEqual(validated_data['field2'], 'ANOTHER')

    def test_mixed_conditions(self):
        """Test mixing conditions from both APIs."""

        class MixedInputFilter(InputFilter):
            phone: str = field()
            email: str = field()
            address: str = field()

            # Decorator-based condition
            _conditions = [ExactlyOneOfCondition(['phone', 'email'])]

            def __init__(self):
                super().__init__()
                # Classic API condition
                # Note: We can't easily test this without creating a custom condition
                # but the framework should support it

        filter_instance = MixedInputFilter()

        # Should work with one field from the condition
        validated_data = filter_instance.validate_data({
            'phone': '123456789',
            'address': 'Main Street 123'
        })
        self.assertEqual(validated_data['phone'], '123456789')
        self.assertEqual(validated_data['address'], 'Main Street 123')

        # Should fail with both fields from the condition
        with self.assertRaises(ValidationError):
            filter_instance.validate_data({
                'phone': '123456789',
                'email': 'test@example.com',
                'address': 'Main Street 123'
            })

    def test_dynamic_field_addition(self):
        """Test adding fields dynamically to decorator-based filter."""

        class MixedInputFilter(InputFilter):
            name: str = field(required=True)

            def __init__(self):
                super().__init__()
                # Start with just the decorator field

            def add_optional_fields(self):
                """Add optional fields dynamically."""
                if not self.has('email'):
                    self.add('email', required=False, validators=[IsStringValidator()])
                if not self.has('phone'):
                    self.add('phone', required=False, validators=[IsStringValidator()])

        filter_instance = MixedInputFilter()

        # Initially should only have name
        self.assertTrue(filter_instance.has('name'))
        self.assertFalse(filter_instance.has('email'))
        self.assertFalse(filter_instance.has('phone'))
        self.assertEqual(filter_instance.count(), 1)

        # Add optional fields
        filter_instance.add_optional_fields()

        # Now should have all fields
        self.assertTrue(filter_instance.has('name'))
        self.assertTrue(filter_instance.has('email'))
        self.assertTrue(filter_instance.has('phone'))
        self.assertEqual(filter_instance.count(), 3)

        # Test validation with all fields
        validated_data = filter_instance.validate_data({
            'name': 'John Doe',
            'email': 'john@example.com'
        })
        self.assertEqual(validated_data['name'], 'John Doe')
        self.assertEqual(validated_data['email'], 'john@example.com')
        self.assertIsNone(validated_data['phone'])

    def test_classic_api_modification_of_decorator_fields(self):
        """Test modifying decorator fields with classic API methods."""

        class MixedInputFilter(InputFilter):
            name: str = field(required=True)

        filter_instance = MixedInputFilter()

        # Should be able to replace decorator field
        filter_instance.replace('name', required=False, default='Anonymous')

        # Field should now have new properties
        name_field = filter_instance.get_input('name')
        self.assertFalse(name_field.required)
        self.assertEqual(name_field.default, 'Anonymous')

        # Should be able to remove decorator field
        removed_field = filter_instance.remove('name')
        self.assertIsNotNone(removed_field)
        self.assertFalse(filter_instance.has('name'))

    def test_inheritance_with_mixed_api(self):
        """Test inheritance combining both APIs."""

        class BaseInputFilter(InputFilter):
            # Base decorator field
            name: str = field(required=True)
            _global_filters = [StringTrimFilter()]

            def __init__(self):
                super().__init__()
                # Base classic field
                self.add('created_at', required=False)

        class ExtendedInputFilter(BaseInputFilter):
            # Extended decorator field
            email: str = field(required=True, validators=[IsStringValidator()])

            def __init__(self):
                super().__init__()
                # Extended classic field
                self.add('updated_at', required=False)

        filter_instance = ExtendedInputFilter()

        # Should have all fields from both levels
        self.assertTrue(filter_instance.has('name'))      # Base decorator
        self.assertTrue(filter_instance.has('created_at')) # Base classic
        self.assertTrue(filter_instance.has('email'))     # Extended decorator
        self.assertTrue(filter_instance.has('updated_at')) # Extended classic
        self.assertEqual(filter_instance.count(), 4)

        # Should have inherited global filters
        self.assertEqual(len(filter_instance.get_global_filters()), 1)

    def test_flask_integration_mixed(self):
        """Test Flask integration with mixed API."""

        class MixedInputFilter(InputFilter):
            username: str = field(required=True, validators=[IsStringValidator()])

            def __init__(self):
                super().__init__()
                self.add('age', required=False, default=18, validators=[IsIntegerValidator()])

        app = Flask(__name__)

        @app.route('/test', methods=['POST'])
        @MixedInputFilter.validate()
        def test_route():
            return jsonify(g.validated_data)

        with app.test_client() as client:
            # Test with both fields
            response = client.post('/test', json={
                'username': 'testuser',
                'age': 25
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {
                'username': 'testuser',
                'age': 25
            })

            # Test with only decorator field (classic should use default)
            response = client.post('/test', json={
                'username': 'testuser2'
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {
                'username': 'testuser2',
                'age': 18  # Default from classic API
            })

    def test_complex_mixed_validation(self):
        """Test complex validation scenario mixing both APIs."""

        class ComplexMixedInputFilter(InputFilter):
            # Decorator fields with complex validation
            username: str = field(
                required=True,
                filters=[StringTrimFilter(), ToLowerFilter()],
                validators=[IsStringValidator(), LengthValidator(min_length=3, max_length=20)]
            )
            profile_type: str = field(required=True)

            # Global components via decorator
            _global_filters = [StringTrimFilter()]

            def __init__(self):
                super().__init__()
                # Classic fields with dynamic logic
                self.add('email', required=True, validators=[IsStringValidator()])

                # Add conditional fields based on profile type
                # (This would typically be done based on some logic)
                self.add('company', required=False, validators=[IsStringValidator()])

                # Classic global components
                self.add_global_validator(IsStringValidator())

        filter_instance = ComplexMixedInputFilter()

        # Test successful validation
        validated_data = filter_instance.validate_data({
            'username': '  TestUser123  ',
            'profile_type': 'business',
            'email': 'test@example.com',
            'company': 'Test Corp'
        })

        self.assertEqual(validated_data['username'], 'testuser123')  # Trimmed and lowered
        self.assertEqual(validated_data['profile_type'], 'business')
        self.assertEqual(validated_data['email'], 'test@example.com')
        self.assertEqual(validated_data['company'], 'Test Corp')

        # Test validation failure on decorator field
        with self.assertRaises(ValidationError):
            filter_instance.validate_data({
                'username': 'ab',  # Too short
                'profile_type': 'business',
                'email': 'test@example.com'
            })

        # Test validation failure on classic field
        with self.assertRaises(ValidationError):
            filter_instance.validate_data({
                'username': 'validuser',
                'profile_type': 'business',
                'email': 123  # Invalid type
            })

    def test_method_availability_mixed(self):
        """Test that all expected methods are available in mixed usage."""

        class MixedInputFilter(InputFilter):
            decorator_field: str = field(required=True)

            def __init__(self):
                super().__init__()
                self.add('classic_field', required=True)

        filter_instance = MixedInputFilter()

        # Classic API methods should all be available
        self.assertTrue(hasattr(filter_instance, 'add'))
        self.assertTrue(hasattr(filter_instance, 'remove'))
        self.assertTrue(hasattr(filter_instance, 'replace'))
        self.assertTrue(hasattr(filter_instance, 'add_condition'))
        self.assertTrue(hasattr(filter_instance, 'add_global_filter'))
        self.assertTrue(hasattr(filter_instance, 'add_global_validator'))

        # Getter methods should be available
        self.assertTrue(hasattr(filter_instance, 'get_conditions'))
        self.assertTrue(hasattr(filter_instance, 'get_global_filters'))
        self.assertTrue(hasattr(filter_instance, 'get_global_validators'))
        self.assertTrue(hasattr(filter_instance, 'get_input'))
        self.assertTrue(hasattr(filter_instance, 'get_inputs'))

        # Core methods should be available
        self.assertTrue(hasattr(filter_instance, 'validate_data'))
        self.assertTrue(hasattr(filter_instance, 'is_valid'))
        self.assertTrue(hasattr(filter_instance, 'has'))
        self.assertTrue(hasattr(filter_instance, 'count'))

    def test_edge_case_empty_mixed_filter(self):
        """Test edge case of empty filter with mixed API setup."""

        class EmptyMixedInputFilter(InputFilter):
            # No decorator fields
            pass

        filter_instance = EmptyMixedInputFilter()

        # Should work even with no fields
        self.assertEqual(filter_instance.count(), 0)
        validated_data = filter_instance.validate_data({})
        self.assertEqual(validated_data, {})

        # Should be able to add fields dynamically
        filter_instance.add('dynamic_field', required=False, default='test')
        self.assertEqual(filter_instance.count(), 1)

        validated_data = filter_instance.validate_data({})
        self.assertEqual(validated_data['dynamic_field'], 'test')

    def test_mixed_api_with_model(self):
        """Test mixing decorator and classic API with model assignment."""
        from dataclasses import dataclass

        @dataclass
        class UserModel:
            name: str
            age: int
            email: str

        class MixedInputFilter(InputFilter):
            # Decorator-based field
            name: str = field(required=True, validators=[IsStringValidator()])

            _model = UserModel

            def __init__(self):
                super().__init__()
                # Classic API fields
                self.add('age', default=18, validators=[IsIntegerValidator()])
                self.add('email', required=False, validators=[IsStringValidator()])

        filter_instance = MixedInputFilter()

        # Should have model class set
        self.assertEqual(filter_instance.model_class, UserModel)

        # Test validation and serialization
        result = filter_instance.validate_data({
            'name': 'John Doe',
            'email': 'john@example.com'
        })

        self.assertIsInstance(result, UserModel)
        self.assertEqual(result.name, 'John Doe')
        self.assertEqual(result.age, 18)  # Default from classic API
        self.assertEqual(result.email, 'john@example.com')

    def test_model_inheritance_mixed(self):
        """Test model assignment inheritance with mixed APIs."""
        from dataclasses import dataclass

        @dataclass
        class BaseModel:
            name: str

        @dataclass
        class ExtendedModel:
            name: str
            age: int
            email: str

        class BaseInputFilter(InputFilter):
            # Decorator field
            name: str = field(required=True)
            _model = BaseModel

            def __init__(self):
                super().__init__()
                # Classic API for additional setup

        class ExtendedInputFilter(BaseInputFilter):
            # Override model in extended class
            _model = ExtendedModel

            def __init__(self):
                super().__init__()
                # Add classic API fields
                self.add('age', default=25)
                self.add('email', required=False)

        # Base should use BaseModel
        base_filter = BaseInputFilter()
        self.assertEqual(base_filter.model_class, BaseModel)

        # Extended should use ExtendedModel (overridden)
        extended_filter = ExtendedInputFilter()
        self.assertEqual(extended_filter.model_class, ExtendedModel)

        result = extended_filter.validate_data({'name': 'John'})
        self.assertIsInstance(result, ExtendedModel)
        self.assertEqual(result.name, 'John')
        self.assertEqual(result.age, 25)
        self.assertIsNone(result.email)

    def test_model_override_in_mixed_api(self):
        """Test that classic API set_model() overrides model assignment."""
        from dataclasses import dataclass

        @dataclass
        class Model1:
            name: str

        @dataclass
        class Model2:
            name: str
            extra: str

        class MixedInputFilter(InputFilter):
            name: str = field(required=True)
            _model = Model1

            def __init__(self):
                super().__init__()

                self.add('extra')
                self.set_model(Model2)

        filter_instance = MixedInputFilter()
        self.assertEqual(filter_instance.model_class, Model2)

        result = filter_instance.validate_data({'name': 'John'})
        self.assertIsInstance(result, Model2)
        self.assertEqual(result.name, 'John')

    def test_model_error_cases(self):
        """Test error cases with model assignment in mixed API."""
        from dataclasses import dataclass

        @dataclass
        class TestModel:
            name: str
            missing_field: str  # This field won't be provided

        class MixedInputFilter(InputFilter):
            name: str = field(required=True)
            _model = TestModel

        filter_instance = MixedInputFilter()

        # This should raise an error because TestModel requires missing_field
        # but our InputFilter doesn't define it
        with self.assertRaises(Exception):
            filter_instance.validate_data({'name': 'John'})

    def test_model_with_complex_mixed_validation(self):
        """Test model assignment with complex mixed validation."""
        from dataclasses import dataclass

        @dataclass
        class ComplexModel:
            username: str
            age: int
            email: str
            company: str

        class ComplexMixedInputFilter(InputFilter):
            # Decorator fields with complex validation
            username: str = field(
                required=True,
                filters=[StringTrimFilter(), ToLowerFilter()],
                validators=[IsStringValidator(), LengthValidator(min_length=3, max_length=20)]
            )

            _model = ComplexModel
            _global_filters = [StringTrimFilter()]

            def __init__(self):
                super().__init__()
                # Classic fields with dynamic logic
                self.add('age', required=True, default=18, validators=[IsIntegerValidator()])
                self.add('email', required=True, validators=[IsStringValidator()])
                self.add('company', required=False, default='Unknown', validators=[IsStringValidator()])

        filter_instance = ComplexMixedInputFilter()
        self.assertEqual(filter_instance.model_class, ComplexModel)

        # Test successful validation
        result = filter_instance.validate_data({
            'username': '  TestUser123  ',
            'age': 25,
            'email': 'test@example.com'
        })

        self.assertIsInstance(result, ComplexModel)
        self.assertEqual(result.username, 'testuser123')  # Trimmed and lowered
        self.assertEqual(result.age, 25)
        self.assertEqual(result.email, 'test@example.com')
        self.assertEqual(result.company, 'Unknown')  # Default value


if __name__ == '__main__':
    unittest.main()