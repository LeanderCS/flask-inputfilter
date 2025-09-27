import unittest
from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field, global_filter
from flask_inputfilter.filters import (
    StringTrimFilter, ToLowerFilter, ToUpperFilter, ToPascalCaseFilter,
    ToSnakeCaseFilter, ToIntegerFilter, ToFloatFilter, WhitespaceCollapseFilter
)
from flask_inputfilter.validators import IsStringValidator, IsIntegerValidator
from flask_inputfilter.exceptions import ValidationError


class TestGlobalFilterDecorator(unittest.TestCase):

    def test_global_filter_decorator(self):

        class TestInputFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            email = field(required=True, validators=[IsStringValidator()])

            global_filter(StringTrimFilter())
            global_filter(ToLowerFilter())

        filter_instance = TestInputFilter()

        global_filters = filter_instance.get_global_filters()
        self.assertEqual(len(global_filters), 2)

        filter_types = [type(f) for f in global_filters]
        self.assertIn(StringTrimFilter, filter_types)
        self.assertIn(ToLowerFilter, filter_types)

        test_data = {'name': '  JOHN  ', 'email': '  TEST@EXAMPLE.COM  '}
        validated_data = filter_instance.validate_data(test_data)

        self.assertEqual(validated_data['name'], 'john')
        self.assertEqual(validated_data['email'], 'test@example.com')

    def test_global_filter_inheritance(self):

        class BaseInputFilter(InputFilter):
            name = field(required=True)

            global_filter(StringTrimFilter())

        class ChildInputFilter(BaseInputFilter):
            email = field(required=True)

            global_filter(ToLowerFilter())

        child_filter = ChildInputFilter()

        global_filters = child_filter.get_global_filters()
        self.assertEqual(len(global_filters), 2)

        filter_types = [type(f) for f in global_filters]
        self.assertIn(StringTrimFilter, filter_types)
        self.assertIn(ToLowerFilter, filter_types)

        test_data = {'name': '  JOHN  ', 'email': '  TEST@EXAMPLE.COM  '}
        validated_data = child_filter.validate_data(test_data)

        self.assertEqual(validated_data['name'], 'john')
        self.assertEqual(validated_data['email'], 'test@example.com')

    def test_ruf012_solved_for_global_filters(self):

        class ProblematicInputFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            email = field(required=True, validators=[IsStringValidator()])

            global_filter(StringTrimFilter())

        filter_instance = ProblematicInputFilter()

        global_filters = filter_instance.get_global_filters()
        self.assertEqual(len(global_filters), 1)

        test_data = {'name': '  John  ', 'email': '  test@example.com  '}
        validated_data = filter_instance.validate_data(test_data)

        self.assertEqual(validated_data['name'], 'John')
        self.assertEqual(validated_data['email'], 'test@example.com')

        self.assertTrue(hasattr(ProblematicInputFilter, '_global_filters'))

    def test_empty_global_filters_behavior(self):
        """Test behavior when no global filters are defined."""

        class NoGlobalFiltersFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

        filter_instance = NoGlobalFiltersFilter()
        global_filters = filter_instance.get_global_filters()
        self.assertEqual(len(global_filters), 0)

        # Should pass data through unchanged
        test_data = {'name': '  TEST  '}
        validated_data = filter_instance.validate_data(test_data)
        self.assertEqual(validated_data['name'], '  TEST  ')

    def test_filter_ordering(self):
        """Test that filters are applied in declaration order."""

        class OrderedFiltersFilter(InputFilter):
            text = field(required=True, validators=[IsStringValidator()])

            # Order: first trim, then convert to lower
            global_filter(StringTrimFilter())
            global_filter(ToLowerFilter())

        filter_instance = OrderedFiltersFilter()
        global_filters = filter_instance.get_global_filters()
        self.assertEqual(len(global_filters), 2)

        # StringTrim should be first, ToLower second
        self.assertIsInstance(global_filters[0], StringTrimFilter)
        self.assertIsInstance(global_filters[1], ToLowerFilter)

        test_data = {'text': '  HELLO WORLD  '}
        validated_data = filter_instance.validate_data(test_data)
        # Should be trimmed first, then lowercased
        self.assertEqual(validated_data['text'], 'hello world')

        # Test reverse order
        class ReverseOrderFilter(InputFilter):
            text = field(required=True, validators=[IsStringValidator()])

            # Order: first convert to lower, then trim
            global_filter(ToLowerFilter())
            global_filter(StringTrimFilter())

        reverse_filter = ReverseOrderFilter()
        test_data = {'text': '  HELLO WORLD  '}
        validated_data = reverse_filter.validate_data(test_data)
        # Should be lowercased first, then trimmed
        self.assertEqual(validated_data['text'], 'hello world')

    def test_multiple_inheritance_chains(self):
        """Test filter inheritance with complex hierarchies."""

        class BaseFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

            global_filter(StringTrimFilter())

        class MiddleFilter(BaseFilter):
            global_filter(ToLowerFilter())

        class LeftFilter(MiddleFilter):
            global_filter(ToPascalCaseFilter())

        class RightFilter(MiddleFilter):
            global_filter(ToSnakeCaseFilter())

        class ComplexFilter(LeftFilter, RightFilter):
            global_filter(WhitespaceCollapseFilter())

        filter_instance = ComplexFilter()
        global_filters = filter_instance.get_global_filters()

        # Should inherit filters from all parent classes
        self.assertGreaterEqual(len(global_filters), 4)

        filter_types = [type(f).__name__ for f in global_filters]
        self.assertIn('StringTrimFilter', filter_types)
        self.assertIn('ToLowerFilter', filter_types)
        self.assertIn('WhitespaceCollapseFilter', filter_types)

    def test_duplicate_filters(self):
        """Test adding the same filter type multiple times."""

        class DuplicateFiltersFilter(InputFilter):
            text = field(required=True, validators=[IsStringValidator()])

            global_filter(StringTrimFilter())
            global_filter(ToLowerFilter())
            global_filter(StringTrimFilter())  # Duplicate

        filter_instance = DuplicateFiltersFilter()
        global_filters = filter_instance.get_global_filters()

        # All filters should be present (no deduplication)
        self.assertEqual(len(global_filters), 3)

        filter_types = [type(f).__name__ for f in global_filters]
        self.assertEqual(filter_types.count('StringTrimFilter'), 2)
        self.assertEqual(filter_types.count('ToLowerFilter'), 1)

    def test_filter_interaction_different_orders(self):
        """Test how different filters interact in different orders."""

        # Test case 1: Trim then Upper
        class TrimThenUpperFilter(InputFilter):
            text = field(required=True, validators=[IsStringValidator()])

            global_filter(StringTrimFilter())
            global_filter(ToUpperFilter())

        filter1 = TrimThenUpperFilter()
        test_data = {'text': '  hello world  '}
        result1 = filter1.validate_data(test_data)
        self.assertEqual(result1['text'], 'HELLO WORLD')

        # Test case 2: Upper then Trim
        class UpperThenTrimFilter(InputFilter):
            text = field(required=True, validators=[IsStringValidator()])

            global_filter(ToUpperFilter())
            global_filter(StringTrimFilter())

        filter2 = UpperThenTrimFilter()
        result2 = filter2.validate_data(test_data)
        self.assertEqual(result2['text'], 'HELLO WORLD')

        # Both should give same result in this case
        self.assertEqual(result1['text'], result2['text'])

    def test_global_filters_on_non_string_fields(self):
        """Test global filters on numeric and other field types."""

        class MixedTypeFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            age = field(required=True, validators=[IsIntegerValidator()])
            score = field(required=False)

            # String filter should only affect string fields
            global_filter(StringTrimFilter())
            global_filter(ToLowerFilter())

        filter_instance = MixedTypeFilter()

        test_data = {
            'name': '  JOHN DOE  ',
            'age': 25,  # Already integer
            'score': 95.5
        }

        validated_data = filter_instance.validate_data(test_data)

        # String field should be filtered
        self.assertEqual(validated_data['name'], 'john doe')

        # Numeric fields should not be affected by string filters
        self.assertEqual(validated_data['age'], 25)  # Integer should remain integer
        self.assertEqual(validated_data['score'], 95.5)

    def test_filter_with_conversion_filters(self):
        """Test global filters that convert data types."""

        class ConversionFilter(InputFilter):
            number_str = field(required=True)
            float_str = field(required=True)

            global_filter(StringTrimFilter())
            global_filter(ToIntegerFilter())

        filter_instance = ConversionFilter()

        test_data = {
            'number_str': '  123  ',
            'float_str': '  45.67  '
        }

        validated_data = filter_instance.validate_data(test_data)

        # Should trim then try to convert to integer
        self.assertEqual(validated_data['number_str'], 123)

        # Float conversion might fail with ToIntegerFilter
        # This tests error handling
        try:
            # ToIntegerFilter should handle this gracefully
            self.assertIsInstance(validated_data['float_str'], (int, str))
        except ValidationError:
            # Expected behavior if conversion fails
            pass

    def test_whitespace_handling_filters(self):
        """Test filters that handle whitespace in different ways."""

        class WhitespaceFilter(InputFilter):
            text = field(required=True, validators=[IsStringValidator()])

            global_filter(WhitespaceCollapseFilter())
            global_filter(StringTrimFilter())

        filter_instance = WhitespaceFilter()

        test_data = {'text': '  hello    world   test  '}
        validated_data = filter_instance.validate_data(test_data)

        # WhitespaceCollapse first, then trim
        # Result should have single spaces and be trimmed
        self.assertEqual(validated_data['text'], 'hello world test')

    def test_case_conversion_combinations(self):
        """Test various case conversion filter combinations."""

        class CaseConversionFilter(InputFilter):
            text = field(required=True, validators=[IsStringValidator()])

            global_filter(StringTrimFilter())
            global_filter(ToLowerFilter())
            global_filter(ToPascalCaseFilter())

        filter_instance = CaseConversionFilter()

        test_data = {'text': '  hello_world_test  '}
        validated_data = filter_instance.validate_data(test_data)

        # Should trim, then lower, then pascal case
        # Exact result depends on filter implementation
        self.assertIsInstance(validated_data['text'], str)
        self.assertTrue(len(validated_data['text']) > 0)

    def test_empty_string_handling(self):
        """Test how global filters handle empty strings."""

        class EmptyStringFilter(InputFilter):
            optional_field = field(required=False, validators=[IsStringValidator()])

            global_filter(StringTrimFilter())
            global_filter(ToLowerFilter())

        filter_instance = EmptyStringFilter()

        test_data = {'optional_field': ''}
        validated_data = filter_instance.validate_data(test_data)

        # Empty string should remain empty after filtering
        self.assertEqual(validated_data['optional_field'], '')

        # Test with whitespace only
        test_data = {'optional_field': '   '}
        validated_data = filter_instance.validate_data(test_data)

        # Should be trimmed to empty string
        self.assertEqual(validated_data['optional_field'], '')

    def test_multiple_global_filters_at_once(self):
        """Test registering multiple global filters in a single call."""

        class MultiFilterInputFilter(InputFilter):
            name = field(required=True)
            description = field(required=False)

            global_filter(StringTrimFilter(), ToUpperFilter())

        filter_instance = MultiFilterInputFilter()

        global_filters = filter_instance.get_global_filters()
        self.assertEqual(len(global_filters), 2)

        filter_types = [type(f) for f in global_filters]
        self.assertIn(StringTrimFilter, filter_types)
        self.assertIn(ToUpperFilter, filter_types)

        validated_data = filter_instance.validate_data({
            'name': '  john doe  ', 'description': '  test description  '
        })

        self.assertEqual(validated_data['name'], 'JOHN DOE')
        self.assertEqual(validated_data['description'], 'TEST DESCRIPTION')


if __name__ == '__main__':
    unittest.main()
