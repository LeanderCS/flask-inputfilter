import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.conditions import ExactlyOneOfCondition
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import ToLowerFilter, ToIntegerFilter, StringTrimFilter
from flask_inputfilter.validators import IsStringValidator, IsIntegerValidator, LengthValidator


class TestInputFilterInheritance(unittest.TestCase):
    """Test suite for InputFilter inheritance behavior."""

    def test_basic_inheritance(self):
        """Test basic inheritance where child class adds new fields."""

        class UserInputFilter(InputFilter):
            username = field(required=True, validators=[IsStringValidator()])
            email = field(required=True, validators=[IsStringValidator()])

        class ProfileInputFilter(UserInputFilter):
            bio = field(required=False, default='No bio')
            age = field(required=False, validators=[IsIntegerValidator()])

        profile_filter = ProfileInputFilter()

        # Check that all fields are present (inherited + new)
        expected_fields = {'username', 'email', 'bio', 'age'}
        actual_fields = set(profile_filter.fields.keys())
        self.assertEqual(expected_fields, actual_fields)

        # Check field properties are preserved
        username_field = profile_filter.get_input('username')
        bio_field = profile_filter.get_input('bio')

        self.assertTrue(username_field.required)
        self.assertFalse(bio_field.required)
        self.assertEqual(bio_field.default, 'No bio')

    def test_field_overriding(self):
        """Test that child classes can override parent field definitions."""

        class BaseInputFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            value = field(required=False)

        class EnhancedInputFilter(BaseInputFilter):
            # Override with additional filters and validators
            name = field(
                required=True,
                validators=[IsStringValidator(), LengthValidator(min_length=3)],
                filters=[StringTrimFilter(), ToLowerFilter()]
            )
            # Add new field
            description = field(required=False, default='')

        enhanced_filter = EnhancedInputFilter()

        # Check that overridden field has new properties
        name_field = enhanced_filter.get_input('name')
        self.assertEqual(len(name_field.validators), 2)
        self.assertEqual(len(name_field.filters), 2)

        # Check that both inherited and new fields exist
        self.assertTrue(enhanced_filter.has('name'))
        self.assertTrue(enhanced_filter.has('value'))
        self.assertTrue(enhanced_filter.has('description'))

    def test_multi_level_inheritance(self):
        """Test inheritance through multiple levels."""

        class BaseInputFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])

        class UserInputFilter(BaseInputFilter):
            username = field(required=True, validators=[IsStringValidator()])
            email = field(required=True, validators=[IsStringValidator()])

        class AdminInputFilter(UserInputFilter):
            role = field(required=True, default='admin')
            permissions = field(required=False, default=[])

        admin_filter = AdminInputFilter()

        # Check all fields from all inheritance levels are present
        expected_fields = {'id', 'username', 'email', 'role', 'permissions'}
        actual_fields = set(admin_filter.fields.keys())
        self.assertEqual(expected_fields, actual_fields)

        # Verify field count
        self.assertEqual(admin_filter.count(), 5)

    def test_validation_with_inherited_fields(self):
        """Test that validation works correctly with inherited fields."""

        class UserInputFilter(InputFilter):
            username = field(required=True, validators=[IsStringValidator()])
            email = field(required=True, validators=[IsStringValidator()])

        class ProfileInputFilter(UserInputFilter):
            bio = field(required=False, default='Developer')
            age = field(required=False, validators=[IsIntegerValidator()])

        profile_filter = ProfileInputFilter()

        # Test successful validation with all field types
        test_data = {
            'username': 'john_doe',
            'email': 'john@example.com',
            'bio': 'Senior Developer',
            'age': 30
        }

        validated_data = profile_filter.validate_data(test_data)
        self.assertEqual(validated_data['username'], 'john_doe')
        self.assertEqual(validated_data['email'], 'john@example.com')
        self.assertEqual(validated_data['bio'], 'Senior Developer')
        self.assertEqual(validated_data['age'], 30)

        # Test validation with missing optional fields (should use defaults)
        minimal_data = {
            'username': 'jane_doe',
            'email': 'jane@example.com'
        }

        validated_data = profile_filter.validate_data(minimal_data)
        self.assertEqual(validated_data['bio'], 'Developer')  # default value

        # Test validation failure for required inherited field
        invalid_data = {
            'email': 'test@example.com',
            # missing required 'username'
        }

        with self.assertRaises(ValidationError) as context:
            profile_filter.validate_data(invalid_data)

        errors = context.exception.args[0]
        self.assertIn('username', errors)

    def test_conditions_inheritance(self):
        """Test that conditions can be inherited and work with inherited
        fields."""

        class BaseInputFilter(InputFilter):
            field_a = field(required=False)
            field_b = field(required=False)

            def __init__(self):
                super().__init__()
                self.add_condition(ExactlyOneOfCondition(['field_a', 'field_b']))

        class ExtendedInputFilter(BaseInputFilter):
            field_c = field(required=False)

        extended_filter = ExtendedInputFilter()

        # Check that condition is inherited
        conditions = extended_filter.get_conditions()
        self.assertEqual(len(conditions), 1)
        self.assertIsInstance(conditions[0], ExactlyOneOfCondition)

        # Test that inherited condition works
        valid_data = {'field_a': 'value1'}
        validated_data = extended_filter.validate_data(valid_data)
        self.assertEqual(validated_data['field_a'], 'value1')

        # Test condition violation
        invalid_data = {'field_a': 'value1', 'field_b': 'value2'}
        with self.assertRaises(ValidationError):
            extended_filter.validate_data(invalid_data)

    def test_global_filters_and_validators_inheritance(self):
        """Test that global filters and validators are inherited."""

        class BaseInputFilter(InputFilter):
            name = field(required=True)

            def __init__(self):
                super().__init__()
                self.add_global_filter(StringTrimFilter())
                self.add_global_validator(IsStringValidator())

        class ChildInputFilter(BaseInputFilter):
            description = field(required=False, default='No description')

        child_filter = ChildInputFilter()

        # Check that global filters and validators are inherited
        global_filters = child_filter.get_global_filters()
        global_validators = child_filter.get_global_validators()

        self.assertEqual(len(global_filters), 1)
        self.assertEqual(len(global_validators), 1)
        self.assertIsInstance(global_filters[0], StringTrimFilter)
        self.assertIsInstance(global_validators[0], IsStringValidator)

        # Test that global filter works on inherited fields
        test_data = {'name': '  john  ', 'description': '  A developer  '}
        validated_data = child_filter.validate_data(test_data)
        self.assertEqual(validated_data['name'], 'john')  # trimmed by global filter
        self.assertEqual(validated_data['description'], 'A developer')  # also trimmed

    def test_inheritance_with_programmatic_fields(self):
        """Test inheritance when parent uses programmatic field addition."""

        class ProgrammaticInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('username', required=True, validators=[IsStringValidator()])
                self.add('email', required=True, validators=[IsStringValidator()])

        class DeclarativeChildInputFilter(ProgrammaticInputFilter):
            bio = field(required=False, default='No bio')
            age = field(required=False, validators=[IsIntegerValidator()])

        child_filter = DeclarativeChildInputFilter()

        # Check that both programmatic and declarative fields exist
        expected_fields = {'username', 'email', 'bio', 'age'}
        actual_fields = set(child_filter.fields.keys())
        self.assertEqual(expected_fields, actual_fields)

        # Test validation works for both types
        test_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'bio': 'Developer',
            'age': 28
        }

        validated_data = child_filter.validate_data(test_data)
        self.assertEqual(len(validated_data), 4)
        self.assertEqual(validated_data['username'], 'test_user')
        self.assertEqual(validated_data['bio'], 'Developer')

    def test_deep_inheritance_chain(self):
        """Test a deep inheritance chain to ensure all levels work
        correctly."""

        class Level1InputFilter(InputFilter):
            level1_field = field(required=False, default='level1')

        class Level2InputFilter(Level1InputFilter):
            level2_field = field(required=False, default='level2')

        class Level3InputFilter(Level2InputFilter):
            level3_field = field(required=False, default='level3')

        class Level4InputFilter(Level3InputFilter):
            level4_field = field(required=False, default='level4')

        deep_filter = Level4InputFilter()

        # Check all fields from all levels are present
        expected_fields = {'level1_field', 'level2_field', 'level3_field', 'level4_field'}
        actual_fields = set(deep_filter.fields.keys())
        self.assertEqual(expected_fields, actual_fields)

        # Test validation with all defaults
        validated_data = deep_filter.validate_data({})
        self.assertEqual(validated_data['level1_field'], 'level1')
        self.assertEqual(validated_data['level2_field'], 'level2')
        self.assertEqual(validated_data['level3_field'], 'level3')
        self.assertEqual(validated_data['level4_field'], 'level4')

    def test_inheritance_does_not_modify_parent_class(self):
        """Test that creating child classes doesn't modify parent class."""

        class ParentInputFilter(InputFilter):
            parent_field = field(required=True)

        # Create instance of parent before child class definition
        parent_instance_before = ParentInputFilter()

        class ChildInputFilter(ParentInputFilter):
            child_field = field(required=True)

        # Create instance of parent after child class definition
        parent_instance_after = ParentInputFilter()
        child_instance = ChildInputFilter()

        # Parent instances should only have parent fields
        self.assertEqual(set(parent_instance_before.fields.keys()), {'parent_field'})
        self.assertEqual(set(parent_instance_after.fields.keys()), {'parent_field'})

        # Child instance should have both fields
        self.assertEqual(set(child_instance.fields.keys()), {'parent_field', 'child_field'})


if __name__ == '__main__':
    unittest.main()
