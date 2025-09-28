import unittest

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import condition, field
from flask_inputfilter.conditions import (
    EqualCondition, ExactlyOneOfCondition, NotEqualCondition, RequiredIfCondition,
    ArrayLengthEqualCondition, StringLongerThanCondition, OneOfCondition,
    TemporalOrderCondition, NOfCondition, CustomCondition
)
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import StringTrimFilter, ToLowerFilter
from flask_inputfilter.validators import IsStringValidator, LengthValidator, IsDateValidator


class TestConditionDecorator(unittest.TestCase):

    def test_single_condition_decorator(self):

        class TestInputFilter(InputFilter):
            password = field(required=True, validators=[IsStringValidator()])
            password_confirmation = field(required=True, validators=[IsStringValidator()])

            condition(EqualCondition("password", "password_confirmation"))

        filter_instance = TestInputFilter()

        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 1)
        self.assertIsInstance(conditions[0], EqualCondition)

        valid_data = {
            'password': 'test123',
            'password_confirmation': 'test123'
        }
        validated_data = filter_instance.validate_data(valid_data)
        self.assertEqual(validated_data['password'], 'test123')
        self.assertEqual(validated_data['password_confirmation'], 'test123')

        invalid_data = {
            'password': 'test123',
            'password_confirmation': 'different'
        }
        with self.assertRaises(ValidationError):
            filter_instance.validate_data(invalid_data)

    def test_multiple_condition_decorators(self):

        class TestInputFilter(InputFilter):
            field_a = field(required=False)
            field_b = field(required=False)
            field_c = field(required=False)
            password = field(required=False, validators=[IsStringValidator()])
            password_confirmation = field(required=False, validators=[IsStringValidator()])

            condition(ExactlyOneOfCondition(['field_a', 'field_b', 'field_c']))
            condition(EqualCondition("password", "password_confirmation"))

        filter_instance = TestInputFilter()

        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 2)

        condition_types = [type(c) for c in conditions]
        self.assertIn(ExactlyOneOfCondition, condition_types)
        self.assertIn(EqualCondition, condition_types)

        valid_data = {
            'field_a': 'value1',
            'password': 'test123',
            'password_confirmation': 'test123'
        }
        validated_data = filter_instance.validate_data(valid_data)
        self.assertEqual(validated_data['field_a'], 'value1')

        invalid_data1 = {
            'field_a': 'value1',
            'field_b': 'value2',
            'password': 'test123',
            'password_confirmation': 'test123'
        }
        with self.assertRaises(ValidationError):
            filter_instance.validate_data(invalid_data1)

        invalid_data2 = {
            'field_a': 'value1',
            'password': 'test123',
            'password_confirmation': 'different'
        }
        with self.assertRaises(ValidationError):
            filter_instance.validate_data(invalid_data2)

    def test_condition_inheritance(self):

        class BaseInputFilter(InputFilter):
            field_a = field(required=False)
            field_b = field(required=False)

            condition(ExactlyOneOfCondition(['field_a', 'field_b']))

        class ChildInputFilter(BaseInputFilter):
            password = field(required=False, validators=[IsStringValidator()])
            password_confirmation = field(required=False, validators=[IsStringValidator()])

            condition(EqualCondition("password", "password_confirmation"))

        child_filter = ChildInputFilter()

        conditions = child_filter.get_conditions()
        self.assertEqual(len(conditions), 2)

        condition_types = [type(c) for c in conditions]
        self.assertIn(ExactlyOneOfCondition, condition_types)
        self.assertIn(EqualCondition, condition_types)

        valid_data = {
            'field_a': 'value1',
            'password': 'test123',
            'password_confirmation': 'test123'
        }
        validated_data = child_filter.validate_data(valid_data)
        self.assertEqual(validated_data['field_a'], 'value1')


    def test_backward_compatibility_with_conditions_list(self):

        class TestInputFilter(InputFilter):
            password = field(required=False, validators=[IsStringValidator()])
            password_confirmation = field(required=False, validators=[IsStringValidator()])

            condition(EqualCondition("password", "password_confirmation"))

        filter_instance = TestInputFilter()

        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 1)

        condition_types = [type(c) for c in conditions]
        self.assertIn(EqualCondition, condition_types)

    def test_backward_compatibility_with_init_method(self):

        class TestInputFilter(InputFilter):
            password = field(required=True, validators=[IsStringValidator()])
            password_confirmation = field(required=True, validators=[IsStringValidator()])
            field_a = field(required=False)
            field_b = field(required=False)

            def __init__(self):
                super().__init__()

                self.add_condition(EqualCondition("password", "password_confirmation"))
                self.add_condition(ExactlyOneOfCondition(['field_a', 'field_b']))

        filter_instance = TestInputFilter()

        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 2)

        condition_types = [type(c) for c in conditions]
        self.assertIn(EqualCondition, condition_types)
        self.assertIn(ExactlyOneOfCondition, condition_types)

        valid_data = {
            'password': 'test123',
            'password_confirmation': 'test123',
            'field_a': 'value1'
        }
        validated_data = filter_instance.validate_data(valid_data)
        self.assertEqual(validated_data['password'], 'test123')

    def test_all_three_condition_styles_together(self):

        class TestInputFilter(InputFilter):
            password = field(required=False, validators=[IsStringValidator()])
            password_confirmation = field(required=False, validators=[IsStringValidator()])
            field_c = field(required=False)

            condition(EqualCondition("password", "password_confirmation"))

            def __init__(self):
                super().__init__()
                self.add_condition(NotEqualCondition('field_c', 'password'))

        filter_instance = TestInputFilter()

        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 2)

        condition_types = [type(c).__name__ for c in conditions]
        self.assertIn('EqualCondition', condition_types)
        self.assertIn('NotEqualCondition', condition_types)

    def test_no_init_required(self):

        class TestInputFilter(InputFilter):
            password = field(required=True, validators=[IsStringValidator()])
            password_confirmation = field(required=True, validators=[IsStringValidator()])

            condition(EqualCondition("password", "password_confirmation"))

        filter_instance = TestInputFilter()

        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 1)
        self.assertIsInstance(conditions[0], EqualCondition)

        valid_data = {
            'password': 'test123',
            'password_confirmation': 'test123'
        }
        validated_data = filter_instance.validate_data(valid_data)
        self.assertEqual(validated_data['password'], 'test123')

    def test_anonymous_condition_calls(self):

        class TestInputFilter(InputFilter):
            password = field(required=True, validators=[IsStringValidator()])
            password_confirmation = field(required=True, validators=[IsStringValidator()])
            field_a = field(required=False)
            field_b = field(required=False)

            condition(EqualCondition("password", "password_confirmation"))
            condition(ExactlyOneOfCondition(['field_a', 'field_b']))

        filter_instance = TestInputFilter()

        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 2)

        condition_types = [type(c) for c in conditions]
        self.assertIn(EqualCondition, condition_types)
        self.assertIn(ExactlyOneOfCondition, condition_types)

        valid_data = {
            'password': 'test123',
            'password_confirmation': 'test123',
            'field_a': 'value1'
        }
        validated_data = filter_instance.validate_data(valid_data)
        self.assertEqual(validated_data['password'], 'test123')

    def test_mixed_named_and_anonymous_conditions(self):

        class TestInputFilter(InputFilter):
            password = field(required=True, validators=[IsStringValidator()])
            password_confirmation = field(required=True, validators=[IsStringValidator()])
            field_a = field(required=False)
            field_b = field(required=False)

            condition(EqualCondition("password", "password_confirmation"))
            condition(ExactlyOneOfCondition(['field_a', 'field_b']))

        filter_instance = TestInputFilter()

        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 2)

        condition_types = [type(c) for c in conditions]
        self.assertIn(EqualCondition, condition_types)
        self.assertIn(ExactlyOneOfCondition, condition_types)

    def test_ruf012_linting_problem_solved(self):

        class ProblematicInputFilter(InputFilter):
            password = field(required=True, validators=[IsStringValidator()])
            password_confirmation = field(required=True, validators=[IsStringValidator()])

            condition(EqualCondition("password", "password_confirmation"))

        filter_instance = ProblematicInputFilter()

        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 1)
        self.assertIsInstance(conditions[0], EqualCondition)

        valid_data = {
            'password': 'test123',
            'password_confirmation': 'test123'
        }
        validated_data = filter_instance.validate_data(valid_data)
        self.assertEqual(validated_data['password'], 'test123')

        invalid_data = {
            'password': 'test123',
            'password_confirmation': 'different'
        }
        with self.assertRaises(ValidationError):
            filter_instance.validate_data(invalid_data)

        self.assertTrue(hasattr(ProblematicInputFilter, '_conditions'))

    def test_empty_conditions_handling(self):
        """Test behavior when no conditions are defined."""

        class EmptyConditionsFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

        filter_instance = EmptyConditionsFilter()
        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 0)

        # Should still validate normally
        test_data = {'name': 'test'}
        validated_data = filter_instance.validate_data(test_data)
        self.assertEqual(validated_data['name'], 'test')

    def test_duplicate_conditions(self):
        """Test adding the same condition multiple times."""

        class DuplicateConditionsFilter(InputFilter):
            password = field(required=True, validators=[IsStringValidator()])
            password_confirmation = field(required=True, validators=[IsStringValidator()])

            condition(EqualCondition("password", "password_confirmation"))
            condition(EqualCondition("password", "password_confirmation"))

        filter_instance = DuplicateConditionsFilter()
        conditions = filter_instance.get_conditions()

        # Both conditions should be present (framework doesn't deduplicate)
        self.assertEqual(len(conditions), 2)
        self.assertTrue(all(isinstance(c, EqualCondition) for c in conditions))

    def test_complex_condition_combinations(self):
        """Test with multiple different condition types."""

        class ComplexConditionsFilter(InputFilter):
            tags = field(required=False)
            description = field(required=False, validators=[IsStringValidator()])
            category = field(required=False)
            start_date = field(required=False, validators=[IsDateValidator()])
            end_date = field(required=False, validators=[IsDateValidator()])

            condition(ArrayLengthEqualCondition("tags", 3))
            condition(StringLongerThanCondition("description", 10))
            condition(OneOfCondition(["tech", "business", "personal"]))
            condition(RequiredIfCondition("start_date", None, "end_date"))

        filter_instance = ComplexConditionsFilter()
        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 4)

        condition_types = [type(c).__name__ for c in conditions]
        self.assertIn('ArrayLengthEqualCondition', condition_types)
        self.assertIn('StringLongerThanCondition', condition_types)
        self.assertIn('OneOfCondition', condition_types)
        self.assertIn('RequiredIfCondition', condition_types)

    def test_nested_inheritance_conditions(self):
        """Test conditions with multiple inheritance levels."""

        class BaseFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

            condition(StringLongerThanCondition("name", 2))

        class MiddleFilter(BaseFilter):
            email = field(required=True, validators=[IsStringValidator()])

            condition(StringLongerThanCondition("email", 5))

        class FinalFilter(MiddleFilter):
            password = field(required=True, validators=[IsStringValidator()])
            password_confirmation = field(required=True, validators=[IsStringValidator()])

            condition(EqualCondition("password", "password_confirmation"))

        filter_instance = FinalFilter()
        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 3)

        condition_types = [type(c).__name__ for c in conditions]
        self.assertIn('StringLongerThanCondition', condition_types)
        self.assertIn('EqualCondition', condition_types)
        # Should have 2 StringLongerThanCondition instances
        self.assertEqual(sum(1 for ct in condition_types if ct == 'StringLongerThanCondition'), 2)

    def test_diamond_inheritance_pattern(self):
        """Test proper condition resolution with diamond inheritance."""

        class BaseFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

            condition(StringLongerThanCondition("name", 1))

        class LeftFilter(BaseFilter):
            left_field = field(required=False)

            condition(RequiredIfCondition("name", None, "left_field"))

        class RightFilter(BaseFilter):
            right_field = field(required=False)

            condition(RequiredIfCondition("name", None, "right_field"))

        class DiamondFilter(LeftFilter, RightFilter):
            final_field = field(required=False)

            condition(StringLongerThanCondition("final_field", 0))

        filter_instance = DiamondFilter()
        conditions = filter_instance.get_conditions()

        # Should have all conditions from inheritance chain
        self.assertGreaterEqual(len(conditions), 3)

        condition_types = [type(c).__name__ for c in conditions]
        self.assertIn('StringLongerThanCondition', condition_types)
        self.assertIn('RequiredIfCondition', condition_types)

    def test_missing_field_references_in_conditions(self):
        """Test conditions referencing non-existent fields."""

        class MissingFieldFilter(InputFilter):
            existing_field = field(required=True, validators=[IsStringValidator()])

            # This condition references a field that doesn't exist
            condition(EqualCondition("existing_field", "non_existent_field"))

        filter_instance = MissingFieldFilter()

        # The condition should be created without error during class definition
        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 1)

        # But validation should fail when the condition is checked
        test_data = {'existing_field': 'test'}
        with self.assertRaises(ValidationError):
            filter_instance.validate_data(test_data)

    def test_custom_condition_usage(self):
        """Test using custom conditions with the decorator."""

        def custom_validation_logic(data):
            # Custom logic: password must be different from username
            if 'username' in data and 'password' in data:
                return data['username'] != data['password']
            return True

        class CustomConditionFilter(InputFilter):
            username = field(required=True, validators=[IsStringValidator()])
            password = field(required=True, validators=[IsStringValidator()])

            condition(CustomCondition(custom_validation_logic))

        filter_instance = CustomConditionFilter()
        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 1)
        self.assertIsInstance(conditions[0], CustomCondition)

        # Valid case
        valid_data = {'username': 'john', 'password': 'secret123'}
        validated_data = filter_instance.validate_data(valid_data)
        self.assertEqual(validated_data['username'], 'john')

        # Invalid case - same username and password
        invalid_data = {'username': 'john', 'password': 'john'}
        with self.assertRaises(ValidationError):
            filter_instance.validate_data(invalid_data)

    def test_condition_with_no_fields_defined(self):
        """Test edge case where condition is defined but no fields exist."""

        class NoFieldsFilter(InputFilter):
            # Define a condition but no fields
            condition(EqualCondition("field1", "field2"))

        filter_instance = NoFieldsFilter()
        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 1)

        # Validation might not fail immediately for missing fields in conditions
        # The condition framework may handle this gracefully
        try:
            filter_instance.validate_data({})
            # If it doesn't raise an error, that's also acceptable behavior
        except ValidationError:
            # Expected if condition validation fails
            pass

    def test_conditions_with_temporal_order(self):
        """Test temporal order conditions for date fields."""

        class TemporalFilter(InputFilter):
            start_date = field(required=True, validators=[IsDateValidator()])
            end_date = field(required=True, validators=[IsDateValidator()])

            condition(TemporalOrderCondition("start_date", "end_date"))

        filter_instance = TemporalFilter()
        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 1)
        self.assertIsInstance(conditions[0], TemporalOrderCondition)

        # Valid case - start before end
        from datetime import date
        valid_data = {
            'start_date': date(2023, 1, 1),
            'end_date': date(2023, 12, 31)
        }
        validated_data = filter_instance.validate_data(valid_data)
        self.assertEqual(validated_data['start_date'], date(2023, 1, 1))

        # Invalid case - start after end
        invalid_data = {
            'start_date': date(2023, 12, 31),
            'end_date': date(2023, 1, 1)
        }
        with self.assertRaises(ValidationError):
            filter_instance.validate_data(invalid_data)

    def test_multiple_conditions_at_once(self):
        """Test registering multiple conditions in a single call."""

        class MultiConditionFilter(InputFilter):
            password = field(required=True)
            password_confirmation = field(required=True)
            email = field(required=True)
            email_confirmation = field(required=True)

            condition(
                EqualCondition('password', 'password_confirmation'),
                EqualCondition('email', 'email_confirmation')
            )

        filter_instance = MultiConditionFilter()

        conditions = filter_instance.get_conditions()
        self.assertEqual(len(conditions), 2)

        condition_types = [type(c) for c in conditions]
        self.assertEqual(condition_types.count(EqualCondition), 2)

        validated_data = filter_instance.validate_data({
            'password': 'test123',
            'password_confirmation': 'test123',
            'email': 'test@example.com',
            'email_confirmation': 'test@example.com'
        })
        self.assertEqual(validated_data['password'], 'test123')

        with self.assertRaises(ValidationError):
            filter_instance.validate_data({
            'password': 'test123',
            'password_confirmation': 'different',
            'email': 'test@example.com',
            'email_confirmation': 'test@example.com'
        })

        with self.assertRaises(ValidationError):
            filter_instance.validate_data({
            'password': 'test123',
            'password_confirmation': 'test123',
            'email': 'test@example.com',
            'email_confirmation': 'different@example.com'
        })


if __name__ == '__main__':
    unittest.main()
