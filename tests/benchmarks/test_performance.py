"""Performance benchmarks for flask-inputfilter.

These tests benchmark both Pure Python and Cython implementations.
The version used is determined automatically based on the environment.
"""

import pytest
from flask import Flask, g

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ExactlyOneOfCondition, RequiredIfCondition
from flask_inputfilter.filters import (
    StringSlugifyFilter,
    StringTrimFilter,
    ToIntegerFilter,
    ToLowerFilter,
    ToNullFilter,
    ToUpperFilter,
)
from flask_inputfilter.validators import (
    InArrayValidator,
    IsIntegerValidator,
    IsStringValidator,
    LengthValidator,
    RegexValidator,
)


@pytest.fixture
def flask_app():
    """Create a Flask app for testing."""
    return Flask(__name__)


class TestInputFilterCreation:
    """Benchmark InputFilter instantiation with different complexities."""

    def test_create_simple_filter(self, benchmark):
        """Benchmark creating a simple InputFilter with 5 fields."""

        def create_filter():
            class SimpleFilter(InputFilter):
                def __init__(self):
                    super().__init__()
                    self.add(name="field1", required=True)
                    self.add(name="field2", required=True)
                    self.add(name="field3", required=True)
                    self.add(name="field4", required=True)
                    self.add(name="field5", required=True)

            return SimpleFilter()

        benchmark(create_filter)

    def test_create_medium_filter(self, benchmark):
        """Benchmark creating a medium InputFilter with 20 fields."""

        def create_filter():
            class MediumFilter(InputFilter):
                def __init__(self):
                    super().__init__()
                    for i in range(20):
                        self.add(name=f"field{i}", required=i % 2 == 0)

            return MediumFilter()

        benchmark(create_filter)

    def test_create_complex_filter(self, benchmark):
        """Benchmark creating a complex InputFilter with 50 fields."""

        def create_filter():
            class ComplexFilter(InputFilter):
                def __init__(self):
                    super().__init__()
                    for i in range(50):
                        self.add(
                            name=f"field{i}",
                            required=i % 3 == 0,
                            filters=[StringTrimFilter()],
                            validators=[IsStringValidator()],
                        )

            return ComplexFilter()

        benchmark(create_filter)


class TestSimpleValidation:
    """Benchmark simple validation operations."""

    def test_validate_string_fields(self, benchmark, flask_app):
        """Benchmark validating simple string fields."""

        class StringFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(name="name", required=True, validators=[IsStringValidator()])
                self.add(name="email", required=True, validators=[IsStringValidator()])
                self.add(name="address", required=False, validators=[IsStringValidator()])

        input_filter = StringFilter()
        test_data = {"name": "John Doe", "email": "john@example.com", "address": "123 Main St"}

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)

    def test_validate_integer_fields(self, benchmark, flask_app):
        """Benchmark validating integer fields."""

        class IntegerFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(name="age", required=True, validators=[IsIntegerValidator()])
                self.add(name="score", required=True, validators=[IsIntegerValidator()])
                self.add(name="count", required=False, validators=[IsIntegerValidator()])

        input_filter = IntegerFilter()
        test_data = {"age": 25, "score": 100, "count": 5}

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)

    def test_validate_mixed_fields(self, benchmark, flask_app):
        """Benchmark validating mixed field types."""

        class MixedFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(name="username", required=True, validators=[IsStringValidator()])
                self.add(name="age", required=True, validators=[IsIntegerValidator()])
                self.add(name="email", required=True, validators=[IsStringValidator()])
                self.add(name="score", required=False, validators=[IsIntegerValidator()])

        input_filter = MixedFilter()
        test_data = {"username": "johndoe", "age": 25, "email": "john@example.com", "score": 100}

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)


class TestComplexValidation:
    """Benchmark complex validation with multiple validators and filters."""

    def test_validate_with_filters(self, benchmark, flask_app):
        """Benchmark validation with multiple filters per field."""

        class FilteredInput(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(
                    name="username",
                    required=True,
                    filters=[StringTrimFilter(), ToLowerFilter()],
                    validators=[IsStringValidator(), LengthValidator(min_length=3, max_length=20)],
                )
                self.add(
                    name="email",
                    required=True,
                    filters=[StringTrimFilter(), ToLowerFilter()],
                    validators=[IsStringValidator()],
                )
                self.add(
                    name="slug",
                    required=False,
                    filters=[StringSlugifyFilter()],
                    validators=[IsStringValidator()],
                )

        input_filter = FilteredInput()
        test_data = {"username": "  JohnDoe  ", "email": "  JOHN@EXAMPLE.COM  ", "slug": "Hello World!"}

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)

    def test_validate_with_multiple_validators(self, benchmark, flask_app):
        """Benchmark validation with multiple validators per field."""

        class MultiValidatorInput(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(
                    name="status",
                    required=True,
                    validators=[
                        IsStringValidator(),
                        InArrayValidator(["active", "inactive", "pending"]),
                    ],
                )
                self.add(
                    name="age",
                    required=True,
                    filters=[ToIntegerFilter(), ToNullFilter()],
                    validators=[IsIntegerValidator()],
                )
                self.add(
                    name="username",
                    required=True,
                    filters=[StringTrimFilter()],
                    validators=[
                        IsStringValidator(),
                        LengthValidator(min_length=3, max_length=20),
                        RegexValidator(r"^[a-zA-Z0-9_]+$", "Invalid username format"),
                    ],
                )

        input_filter = MultiValidatorInput()
        test_data = {"status": "active", "age": "25", "username": "john_doe_123"}

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)

    def test_validate_large_dataset(self, benchmark, flask_app):
        """Benchmark validation of a large dataset with 30 fields."""

        class LargeFilter(InputFilter):
            def __init__(self):
                super().__init__()
                for i in range(30):
                    if i % 3 == 0:
                        self.add(
                            name=f"field{i}",
                            required=True,
                            filters=[ToIntegerFilter()],
                            validators=[IsIntegerValidator()],
                        )
                    else:
                        self.add(
                            name=f"field{i}",
                            required=True,
                            filters=[StringTrimFilter()],
                            validators=[IsStringValidator()],
                        )

        input_filter = LargeFilter()
        test_data = {f"field{i}": i if i % 3 == 0 else f"value{i}" for i in range(30)}

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)


class TestConditions:
    """Benchmark condition evaluation."""

    def test_exactly_one_of_condition(self, benchmark, flask_app):
        """Benchmark ExactlyOneOfCondition validation."""

        class ConditionalFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(name="email", required=False, validators=[IsStringValidator()])
                self.add(name="phone", required=False, validators=[IsStringValidator()])
                self.add_condition(ExactlyOneOfCondition(["email", "phone"]))

        input_filter = ConditionalFilter()
        test_data = {"email": "john@example.com"}

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)

    def test_required_if_condition(self, benchmark, flask_app):
        """Benchmark RequiredIfCondition validation."""

        class ConditionalFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(name="has_address", required=True, validators=[IsStringValidator()])
                self.add(name="address", required=False, validators=[IsStringValidator()])
                self.add_condition(
                    RequiredIfCondition("address", "has_address", "yes")
                )

        input_filter = ConditionalFilter()
        test_data = {"has_address": "yes", "address": "123 Main St"}

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)

    def test_multiple_conditions(self, benchmark, flask_app):
        """Benchmark multiple conditions in one filter."""

        class MultiConditionFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(name="email", required=False, validators=[IsStringValidator()])
                self.add(name="phone", required=False, validators=[IsStringValidator()])
                self.add(name="contact_method", required=True, validators=[IsStringValidator()])
                self.add(name="preferred_contact", required=False, validators=[IsStringValidator()])

                self.add_condition(ExactlyOneOfCondition(["email", "phone"]))
                self.add_condition(
                    RequiredIfCondition("preferred_contact", "contact_method", "custom")
                )

        input_filter = MultiConditionFilter()
        test_data = {"email": "john@example.com", "contact_method": "email"}

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)


class TestFullRequestCycle:
    """Benchmark full request validation cycle using the decorator."""

    def test_decorator_validation_simple(self, benchmark, flask_app):
        """Benchmark full decorator validation with simple data."""

        class RequestFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(name="username", required=True, validators=[IsStringValidator()])
                self.add(name="age", required=False, default=18, validators=[IsIntegerValidator()])

        @flask_app.route("/test", methods=["POST"])
        @RequestFilter.validate()
        def test_route():
            return g.validated_data

        def run_request():
            with flask_app.test_client() as client:
                return client.post("/test", json={"username": "johndoe", "age": 25})

        benchmark(run_request)

    def test_decorator_validation_complex(self, benchmark, flask_app):
        """Benchmark full decorator validation with complex data."""

        class ComplexRequestFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(
                    name="username",
                    required=True,
                    filters=[StringTrimFilter(), ToLowerFilter()],
                    validators=[
                        IsStringValidator(),
                        LengthValidator(min_length=3, max_length=20),
                    ],
                )
                self.add(
                    name="email",
                    required=True,
                    filters=[StringTrimFilter(), ToLowerFilter()],
                    validators=[IsStringValidator()],
                )
                self.add(
                    name="age",
                    required=True,
                    filters=[ToIntegerFilter()],
                    validators=[IsIntegerValidator()],
                )
                self.add(
                    name="phone",
                    required=False,
                    validators=[IsStringValidator()],
                )

        @flask_app.route("/test-complex", methods=["POST"])
        @ComplexRequestFilter.validate()
        def test_route():
            return g.validated_data

        def run_request():
            with flask_app.test_client() as client:
                return client.post(
                    "/test-complex",
                    json={
                        "username": "  JohnDoe  ",
                        "email": "  JOHN@EXAMPLE.COM  ",
                        "age": "25",
                        "phone": "+1234567890",
                    },
                )

        benchmark(run_request)


class TestHeavyFilters:
    """Benchmark computationally intensive filters."""

    def test_slugify_filter(self, benchmark, flask_app):
        """Benchmark SlugifyFilter with various inputs."""

        class SlugFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(
                    name="title",
                    required=True,
                    filters=[StringSlugifyFilter()],
                    validators=[IsStringValidator()],
                )

        input_filter = SlugFilter()
        test_data = {"title": "This is a Very Long Title with Special Characters!!! @#$%"}

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)

    def test_multiple_string_transformations(self, benchmark, flask_app):
        """Benchmark multiple string transformation filters."""

        class TransformFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(
                    name="text1",
                    required=True,
                    filters=[StringTrimFilter(), ToLowerFilter(), StringSlugifyFilter()],
                    validators=[IsStringValidator()],
                )
                self.add(
                    name="text2",
                    required=True,
                    filters=[StringTrimFilter(), ToUpperFilter()],
                    validators=[IsStringValidator()],
                )
                self.add(
                    name="text3",
                    required=True,
                    filters=[StringTrimFilter()],
                    validators=[IsStringValidator(), LengthValidator(max_length=100)],
                )

        input_filter = TransformFilter()
        test_data = {
            "text1": "  Hello World! This is a Test  ",
            "text2": "  another test string  ",
            "text3": "  yet another test string with some content  ",
        }

        def validate():
            with flask_app.test_request_context(json=test_data):
                return input_filter.is_valid()

        benchmark(validate)
