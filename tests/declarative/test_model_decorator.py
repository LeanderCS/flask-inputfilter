import unittest
from dataclasses import dataclass
from typing import Optional, Dict, Any
from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field, model
from flask_inputfilter.validators import IsStringValidator, IsIntegerValidator
from flask_inputfilter.exceptions import ValidationError

try:
    from typing import TypedDict
    TYPEDDICT_AVAILABLE = True
except ImportError:
    try:
        from typing_extensions import TypedDict
        TYPEDDICT_AVAILABLE = True
    except ImportError:
        TYPEDDICT_AVAILABLE = False

try:
    from pydantic import BaseModel
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False


class TestModelDecorator(unittest.TestCase):

    def test_model_decorator(self):

        @dataclass
        class TestModel:
            name: str
            email: str

        class TestInputFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            email = field(required=True, validators=[IsStringValidator()])

            model(TestModel)

        filter_instance = TestInputFilter()

        self.assertEqual(filter_instance.model_class, TestModel)

        test_data = {'name': 'John', 'email': 'john@example.com'}
        validated_data = filter_instance.validate_data(test_data)

        self.assertIsInstance(validated_data, TestModel)
        self.assertEqual(validated_data.name, 'John')
        self.assertEqual(validated_data.email, 'john@example.com')

    def test_model_inheritance(self):

        @dataclass
        class BaseModel:
            name: str

        @dataclass
        class ExtendedModel:
            name: str
            age: int

        class BaseInputFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

            model(BaseModel)

        class ChildInputFilter(BaseInputFilter):
            age = field(required=True)

            model(ExtendedModel)

        child_filter = ChildInputFilter()

        self.assertEqual(child_filter.model_class, ExtendedModel)

        validated_data = child_filter.validate_data({'name': 'John', 'age': 25})

        self.assertIsInstance(validated_data, ExtendedModel)
        self.assertEqual(validated_data.name, 'John')
        self.assertEqual(validated_data.age, 25)

    def test_model_backward_compatibility(self):

        @dataclass
        class TestModel:
            name: str

        class OldStyleInputFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

            _model = TestModel

        class NewStyleInputFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

            model(TestModel)

        old_filter = OldStyleInputFilter()
        new_filter = NewStyleInputFilter()

        self.assertEqual(old_filter.model_class, TestModel)
        self.assertEqual(new_filter.model_class, TestModel)

        test_data = {'name': 'John'}

        old_validated = old_filter.validate_data(test_data)
        new_validated = new_filter.validate_data(test_data)

        self.assertIsInstance(old_validated, TestModel)
        self.assertIsInstance(new_validated, TestModel)
        self.assertEqual(old_validated.name, 'John')
        self.assertEqual(new_validated.name, 'John')

    def test_ruf012_solved_for_model(self):

        @dataclass
        class ProblematicModel:
            name: str

        class ProblematicInputFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

            model(ProblematicModel)

        filter_instance = ProblematicInputFilter()

        self.assertEqual(filter_instance.model_class, ProblematicModel)

        validated_data = filter_instance.validate_data({'name': 'John'})

        self.assertIsInstance(validated_data, ProblematicModel)
        self.assertEqual(validated_data.name, 'John')

        self.assertTrue(hasattr(ProblematicInputFilter, '_model'))

    def test_missing_model_class_behavior(self):
        """Test behavior when no model decorator is used."""

        class NoModelFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

        filter_instance = NoModelFilter()

        self.assertIsNone(getattr(filter_instance, 'model_class', None))

        validated_data = filter_instance.validate_data({'name': 'John'})
        self.assertEqual(validated_data['name'], 'John')

        self.assertIsInstance(validated_data, dict)
        self.assertEqual(validated_data['name'], 'John')

    @unittest.skipUnless(TYPEDDICT_AVAILABLE, "TypedDict not available")
    def test_typeddict_models(self):
        """Test with TypedDict instead of dataclass."""

        class UserDict(TypedDict):
            name: str
            age: int

        class TypedDictFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            age = field(required=True, validators=[IsIntegerValidator()])

            model(UserDict)

        filter_instance = TypedDictFilter()
        self.assertEqual(filter_instance.model_class, UserDict)

        validated_data = filter_instance.validate_data({'name': 'John', 'age': 25})

        self.assertIsInstance(validated_data, dict)
        self.assertEqual(validated_data['name'], 'John')
        self.assertEqual(validated_data['age'], 25)

    @unittest.skipUnless(PYDANTIC_AVAILABLE, "Pydantic not available")
    def test_pydantic_models(self):
        """Test with Pydantic model classes."""

        class PydanticUser(BaseModel):
            name: str
            age: int
            email: Optional[str] = None

        class PydanticFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            age = field(required=True, validators=[IsIntegerValidator()])
            email = field(required=False, validators=[IsStringValidator()])

            model(PydanticUser)

        filter_instance = PydanticFilter()
        self.assertEqual(filter_instance.model_class, PydanticUser)

        validated_data = filter_instance.validate_data({
            'name': 'John', 'age': 25, 'email': 'john@example.com'
        })

        self.assertIsInstance(validated_data, PydanticUser)
        self.assertEqual(validated_data.name, 'John')
        self.assertEqual(validated_data.age, 25)
        self.assertEqual(validated_data.email, 'john@example.com')

    def test_multiple_model_decorators_error(self):
        """Test error handling with multiple model() calls."""

        @dataclass
        class FirstModel:
            name: str

        @dataclass
        class SecondModel:
            title: str

        class MultipleModelFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

            model(FirstModel)
            model(SecondModel)

        filter_instance = MultipleModelFilter()

        self.assertEqual(filter_instance.model_class, SecondModel)

    def test_serialization_errors(self):
        """Test handling of serialization failures."""

        @dataclass
        class StrictModel:
            name: str
            required_field: str

        class SerializationErrorFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

            model(StrictModel)

        filter_instance = SerializationErrorFilter()

        with self.assertRaises(TypeError):
            filter_instance.validate_data({'name': 'John'})

    def test_partial_field_coverage(self):
        """Test models with subset of filter fields."""

        @dataclass
        class PartialModel:
            name: str

        class PartialCoverageFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            age = field(required=False, validators=[IsIntegerValidator()])
            email = field(required=False, validators=[IsStringValidator()])

            model(PartialModel)

        filter_instance = PartialCoverageFilter()

        serialized = filter_instance.validate_data({'name': 'John'})

        self.assertIsInstance(serialized, PartialModel)
        self.assertEqual(serialized.name, 'John')

    def test_model_with_optional_fields(self):
        """Test models with optional fields."""

        @dataclass
        class OptionalFieldsModel:
            name: str
            age: Optional[int] = None
            email: Optional[str] = None

        class OptionalFieldsFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            age = field(required=False, validators=[IsIntegerValidator()])
            email = field(required=False, validators=[IsStringValidator()])

            model(OptionalFieldsModel)

        filter_instance = OptionalFieldsFilter()

        validated_data1 = filter_instance.validate_data({'name': 'John', 'age': 25, 'email': 'john@example.com'})
        self.assertEqual(validated_data1.name, 'John')
        self.assertEqual(validated_data1.age, 25)
        self.assertEqual(validated_data1.email, 'john@example.com')

        validated_data2 = filter_instance.validate_data({'name': 'Jane'})
        self.assertEqual(validated_data2.name, 'Jane')
        self.assertIsNone(validated_data2.age)
        self.assertIsNone(validated_data2.email)

    def test_complex_model_types(self):
        """Test with complex model field types."""

        @dataclass
        class ComplexModel:
            name: str
            metadata: Dict[str, Any]
            tags: list

        class ComplexModelFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            metadata = field(required=False)
            tags = field(required=False)

            model(ComplexModel)

        filter_instance = ComplexModelFilter()

        validated_data = filter_instance.validate_data({
            'name': 'Test',
            'metadata': {'key1': 'value1', 'key2': 42},
            'tags': ['tag1', 'tag2']
        })

        self.assertEqual(validated_data.name, 'Test')
        self.assertEqual(validated_data.metadata, {'key1': 'value1', 'key2': 42})
        self.assertEqual(validated_data.tags, ['tag1', 'tag2'])

    def test_model_inheritance_overrides(self):
        """Test model decorator inheritance and overrides."""

        @dataclass
        class BaseUserModel:
            name: str

        @dataclass
        class ExtendedUserModel:
            name: str
            age: int
            role: str

        class BaseModelFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

            model(BaseUserModel)

        class ExtendedModelFilter(BaseModelFilter):
            age = field(required=True, validators=[IsIntegerValidator()])
            role = field(required=True, validators=[IsStringValidator()])

            model(ExtendedUserModel)

        filter_instance = ExtendedModelFilter()

        self.assertEqual(filter_instance.model_class, ExtendedUserModel)

        test_data = {'name': 'John', 'age': 25, 'role': 'admin'}
        validated_data = filter_instance.validate_data(test_data)

        self.assertIsInstance(validated_data, ExtendedUserModel)
        self.assertEqual(validated_data.name, 'John')
        self.assertEqual(validated_data.age, 25)
        self.assertEqual(validated_data.role, 'admin')

    def test_model_with_nested_objects(self):
        """Test models with nested object structures."""

        @dataclass
        class Address:
            street: str
            city: str

        @dataclass
        class UserWithAddress:
            name: str
            address: Address

        class NestedModelFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            address = field(required=True)

            model(UserWithAddress)

        filter_instance = NestedModelFilter()

        validated_data = filter_instance.validate_data({
            'name': 'John',
            'address': {'street': '123 Main St', 'city': 'Anytown'}
        })
        self.assertEqual(validated_data.name, 'John')

    def test_empty_model_class(self):
        """Test with empty dataclass model."""

        @dataclass
        class EmptyModel:
            pass

        class EmptyModelFilter(InputFilter):
            model(EmptyModel)

        filter_instance = EmptyModelFilter()
        self.assertEqual(filter_instance.model_class, EmptyModel)

        validated_data = filter_instance.validate_data({})
        self.assertIsInstance(validated_data, EmptyModel)


if __name__ == '__main__':
    unittest.main()
