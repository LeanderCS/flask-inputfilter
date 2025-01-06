import unittest
from enum import Enum

from src.flask_inputfilter.Exception import ValidationError
from src.flask_inputfilter.Filter import (StringTrimFilter, ToFloatFilter,
                                          ToIntFilter, ToLowerFilter,
                                          ToNullFilter, ToUpperFilter)
from src.flask_inputfilter.InputFilter import InputFilter
from src.flask_inputfilter.Validator import (ArrayElementValidator,
                                             InArrayValidator,
                                             InEnumValidator, IsArrayValidator,
                                             IsBase64ImageCorrectSizeValidator,
                                             IsBoolValidator, IsFloatValidator,
                                             IsInstanceValidator,
                                             IsIntegerValidator,
                                             LengthValidator, RegexValidator)


class TestInputFilter(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up a basic InputFilter instance for testing.
        """

        self.inputFilter = InputFilter()

        self.inputFilter.add(
            'age',
            required=True,
            filters=[ToIntFilter()],
            validators=[IsIntegerValidator()]
        )

        self.inputFilter.add(
            'name',
            required=False,
            validators=[
                LengthValidator(minLength=3)
            ]
        )

        self.inputFilter.add(
            'gender',
            required=False,
            validators=[
                InArrayValidator(
                    haystack=['male', 'female', 'other']
                )
            ]
        )

        self.inputFilter.add(
            'email',
            required=False,
            validators=[
                RegexValidator(
                    pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$'
                )
            ]
        )

        self.inputFilter.add(
            'tags',
            required=False,
            validators=[
                IsArrayValidator()
            ]
        )

    def test_required_validation(self) -> None:
        """
        Test validation of required fields.
        """

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({'age': None})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({})

    def test_length_validation(self) -> None:
        """
        Test length validation.
        """

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({'age': 25, 'name': 'Jo'})

    def test_successful_validation(self) -> None:
        """
        Test successful validation.
        """

        data = {
            'age': '40',
            'name': 'Alice',
            'gender': 'female',
            'email': 'alice@example.com'}
        validatedData = self.inputFilter.validateData(data)

        self.assertEqual(validatedData['age'], 40)
        self.assertEqual(validatedData['name'], 'Alice')
        self.assertEqual(validatedData['gender'], 'female')
        self.assertEqual(validatedData['email'], 'alice@example.com')

    def test_null_filter(self) -> None:
        """
        Test that ToNullFilter transforms empty string to None.
        """

        self.inputFilter.add(
            'optional_field',
            required=False,
            filters=[
                ToNullFilter()])
        validatedData = self.inputFilter.validateData(
            {'age': 25, 'name': 'test', 'optional_field': ''})

        self.assertIsNone(validatedData['optional_field'])

    def test_invalid_gender(self) -> None:
        """
        Test validation for invalid gender.
        """

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {'age': 25, 'name': 'Alice', 'gender': 'unknown'})

    def test_invalid_email_format(self) -> None:
        """
        Test validation for invalid email format.
        """

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {'age': 25, 'name': 'Alice', 'email': 'invalid_email'})

    def test_valid_email(self) -> None:
        """
        Test successful validation of a valid email format.
        """

        data = {'age': '30', 'name': 'Alice', 'email': 'alice@example.com'}

        validatedData = self.inputFilter.validateData(data)
        self.assertEqual(validatedData['email'], 'alice@example.com')

    def test_successful_optional(self) -> None:
        """
        Test that optional field validation works.
        """

        data = {'age': '30', 'name': 'Alice'}
        validatedData = self.inputFilter.validateData(data)
        self.assertIsNone(validatedData.get('gender'))

    def test_string_trim_filter(self) -> None:
        """
        Test that StringTrimFilter trims whitespace.
        """

        self.inputFilter.add(
            'trimmed_field',
            required=False,
            filters=[
                StringTrimFilter()])
        validatedData = self.inputFilter.validateData(
            {'age': 25, 'name': 'test', 'trimmed_field': '   Hello World   '})
        self.assertEqual(validatedData['trimmed_field'], 'Hello World')

    def test_is_array_validator(self) -> None:
        """
        Test that IsArrayValidator validates array type.
        """

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {'age': 25, 'name': 'Alice', 'tags': 'not_an_array'})

        data = {'age': 25, 'name': 'Alice', 'tags': ['tag1', 'tag2']}
        validatedData = self.inputFilter.validateData(data)
        self.assertEqual(validatedData['tags'], ['tag1', 'tag2'])

    def test_to_float_filter(self) -> None:
        """
        Test that ToFloatFilter converts string to float.
        """

        self.inputFilter.add(
            'price',
            required=True,
            filters=[
                ToFloatFilter()])
        validatedData = self.inputFilter.validateData(
            {'age': 25, 'name': 'test', 'price': '19.99'})
        self.assertEqual(validatedData['price'], 19.99)

    def test_is_float_validator(self) -> None:
        """
        Test that IsFloatValidator validates float type.
        """

        self.inputFilter.add(
            'price',
            required=True,
            validators=[
                IsFloatValidator()])
        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {'age': 25, 'name': 'Alice', 'price': 'not_a_float'})

        data = {'age': 25, 'name': 'Alice', 'price': 19.99}
        validatedData = self.inputFilter.validateData(data)
        self.assertEqual(validatedData['price'], 19.99)

    def test_to_lower_filter(self) -> None:
        """
        Test that ToLowerFilter converts string to lowercase.
        """

        self.inputFilter.add(
            'username',
            required=True,
            filters=[
                ToLowerFilter()])
        validatedData = self.inputFilter.validateData(
            {'age': 25, 'name': 'test', 'username': 'TESTUSER'})
        self.assertEqual(validatedData['username'], 'testuser')

    def test_to_upper_filter(self) -> None:
        """
        Test that ToUpperFilter converts string to uppercase.
        """

        self.inputFilter.add(
            'username',
            required=True,
            filters=[
                ToUpperFilter()])
        validatedData = self.inputFilter.validateData(
            {'age': 25, 'name': 'test', 'username': 'testuser'})
        self.assertEqual(validatedData['username'], 'TESTUSER')

    def test_array_element_validator(self) -> None:
        """
        Test ArrayElementValidator.
        """

        elementFilter = InputFilter()
        elementFilter.add(
            'id', required=True, filters=[
                ToIntFilter()], validators=[
                IsIntegerValidator()])

        self.inputFilter.add(
            'items', required=True, validators=[
                ArrayElementValidator(elementFilter)])

        valid_data = {'age': 30, 'items': [{'id': '1'}, {'id': '2'}]}
        validated_data = self.inputFilter.validateData(valid_data)
        self.assertEqual(validated_data['items'], [{'id': 1}, {'id': 2}])

        invalid_data = {'age': 30, 'items': [{'id': '1'}, {'id': 'invalid'}]}
        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(invalid_data)

    def test_in_enum_validator(self) -> None:
        """
        Test InEnumValidator.
        """

        class Color(Enum):
            RED = 'red'
            GREEN = 'green'
            BLUE = 'blue'

        self.inputFilter.add(
            'color', required=True, validators=[
                InEnumValidator(Color)])

        valid_data = {'age': 30, 'color': 'red'}
        validated_data = self.inputFilter.validateData(valid_data)
        self.assertEqual(validated_data['color'], 'red')

        invalid_data = {'age': 30, 'color': 'yellow'}
        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(invalid_data)

    def test_is_base64_image_correct_size_validator(self) -> None:
        """
        Test IsBase64ImageCorrectSizeValidator.
        """

        self.inputFilter.add(
            'image', required=True, validators=[
                IsBase64ImageCorrectSizeValidator(
                    minSize=10, maxSize=50)])

        valid_data = {'age': 30, 'image': 'iVBORw0KGgoAAAANSUhEUgAAAAUA'}
        validated_data = self.inputFilter.validateData(valid_data)
        self.assertEqual(
            validated_data['image'],
            'iVBORw0KGgoAAAANSUhEUgAAAAUA')

        invalid_data = {'age': 30, 'image': 'iVBORw0KGgoAAAANSUhEUgAAAAU'}
        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(invalid_data)

    def test_is_bool_validator(self) -> None:
        """
        Test IsBoolValidator.
        """

        self.inputFilter.add(
            'is_active',
            required=True,
            validators=[
                IsBoolValidator()])

        valid_data = {'age': 30, 'is_active': True}
        validated_data = self.inputFilter.validateData(valid_data)
        self.assertEqual(validated_data['is_active'], True)

        invalid_data = {'age': 30, 'is_active': 'yes'}
        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(invalid_data)

    def test_is_instance_validator(self) -> None:
        """
        Test IsInstanceValidator.
        """

        self.inputFilter.add(
            'user', required=True, validators=[
                IsInstanceValidator(dict)])

        valid_data = {'age': 30, 'user': {'name': 'Alice'}}
        validated_data = self.inputFilter.validateData(valid_data)
        self.assertEqual(validated_data['user'], {'name': 'Alice'})

        invalid_data = {'age': 30, 'user': 'Alice'}
        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(invalid_data)
