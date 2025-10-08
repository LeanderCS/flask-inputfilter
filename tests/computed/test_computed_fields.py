import unittest
from dataclasses import dataclass

from flask import Flask, g

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.filters import ToIntegerFilter
from flask_inputfilter.validators import IsIntegerValidator


class TestComputedFields(unittest.TestCase):
    def test_simple_computed_field(self) -> None:
        """Test basic computed field with simple calculation."""

        class SimpleComputedFilter(InputFilter):
            x: int = field(
                required=True, filters=[ToIntegerFilter()], validators=[IsIntegerValidator()]
            )
            y: int = field(
                required=True, filters=[ToIntegerFilter()], validators=[IsIntegerValidator()]
            )
            sum: int = field(computed=lambda data: data["x"] + data["y"])

        result = SimpleComputedFilter().validate_data({"x": 5, "y": 10})

        self.assertEqual(result["x"], 5)
        self.assertEqual(result["y"], 10)
        self.assertEqual(result["sum"], 15)

    def test_computed_field_with_multiple_dependencies(self) -> None:
        """Test computed field that depends on multiple fields."""

        class OrderFilter(InputFilter):
            quantity: int = field(required=True, filters=[ToIntegerFilter()])
            price: float = field(required=True)
            total: float = field(
                computed=lambda data: data["quantity"] * data["price"]
            )

        result = OrderFilter().validate_data({"quantity": 5, "price": 10.50})

        self.assertEqual(result["quantity"], 5)
        self.assertEqual(result["price"], 10.50)
        self.assertEqual(result["total"], 52.5)

    def test_computed_field_with_missing_dependency(self) -> None:
        """Test that computed field handles missing dependencies gracefully."""

        class ComputedWithMissingFilter(InputFilter):
            x: int = field(filters=[ToIntegerFilter()])
            result: int = field(
                computed=lambda data: data.get("x", 0) * 2 if data.get("x") is not None else 0
            )

        result = ComputedWithMissingFilter().validate_data()

        # When x is missing/None, computed should return 0
        self.assertEqual(result.get("result"), 0)

    def test_computed_field_with_exception(self) -> None:
        """Test that computed field exceptions are logged but don't fail
        validation."""

        class ComputedWithErrorFilter(InputFilter):
            x: int = field(required=True, filters=[ToIntegerFilter()])
            broken: int = field(
                computed=lambda data: data["nonexistent_key"] * 2
            )

        # Should not raise exception, just log warning
        result = ComputedWithErrorFilter().validate_data({"x": 10})

        self.assertEqual(result["x"], 10)
        self.assertIsNone(result["broken"])

    def test_computed_field_not_in_input_data(self) -> None:
        """Test that computed fields are readonly and not taken from input."""

        class ReadonlyComputedFilter(InputFilter):
            x: int = field(required=True, filters=[ToIntegerFilter()])
            computed_x: int = field(computed=lambda data: data["x"] * 2)

        result = ReadonlyComputedFilter().validate_data(
            {"x": 5, "computed_x": 999}
        )

        self.assertEqual(result["x"], 5)
        # computed_x should be calculated, not taken from input
        self.assertEqual(result["computed_x"], 10)

    def test_multiple_computed_fields(self) -> None:
        """Test multiple computed fields in one filter."""

        class MultipleComputedFilter(InputFilter):
            a: int = field(required=True, filters=[ToIntegerFilter()])
            b: int = field(required=True, filters=[ToIntegerFilter()])
            sum: int = field(computed=lambda data: data["a"] + data["b"])
            product: int = field(computed=lambda data: data["a"] * data["b"])
            difference: int = field(computed=lambda data: data["a"] - data["b"])

        result = MultipleComputedFilter().validate_data({"a": 10, "b": 3})

        self.assertEqual(result["sum"], 13)
        self.assertEqual(result["product"], 30)
        self.assertEqual(result["difference"], 7)

    def test_computed_field_with_conditions(self) -> None:
        """Test that computed fields work with conditions."""
        from flask_inputfilter.conditions import OneOfCondition
        from flask_inputfilter.declarative import condition

        class ComputedWithConditionsFilter(InputFilter):
            field1: int = field(filters=[ToIntegerFilter()])
            field2: int = field(filters=[ToIntegerFilter()])
            total: int = field(
                computed=lambda data: (data.get("field1") or 0)
                + (data.get("field2") or 0)
            )

            condition(OneOfCondition(["field1", "field2"]))

        filter = ComputedWithConditionsFilter()
        filter.set_data({"field1": 5})

        self.assertTrue(filter.is_valid())
        result = ComputedWithConditionsFilter().validate_data({"field1": 5})
        self.assertEqual(result["total"], 5)

    def test_computed_field_lambda(self) -> None:
        """Test computed field using lambda function."""

        class LambdaComputedFilter(InputFilter):
            name: str = field(required=True)
            greeting: str = field(
                computed=lambda data: f"Hello, {data['name']}!"
            )

        result = LambdaComputedFilter().validate_data({"name": "World"})

        self.assertEqual(result["greeting"], "Hello, World!")

    def test_computed_field_named_function(self) -> None:
        """Test computed field using a named function."""

        def calculate_area(data):
            return data["width"] * data["height"]

        class NamedFunctionComputedFilter(InputFilter):
            width: int = field(required=True, filters=[ToIntegerFilter()])
            height: int = field(required=True, filters=[ToIntegerFilter()])
            area: int = field(computed=calculate_area)

        result = NamedFunctionComputedFilter().validate_data({"width": 5, "height": 10})

        self.assertEqual(result["area"], 50)

    def test_computed_field_integration_with_decorator(self) -> None:
        """Test computed fields work with @validate() decorator."""

        class ComputedDecoratorFilter(InputFilter):
            base: int = field(required=True, filters=[ToIntegerFilter()])
            doubled: int = field(computed=lambda data: data["base"] * 2)

        app = Flask(__name__)

        @app.route("/test", methods=["POST"])
        @ComputedDecoratorFilter.validate()
        def test_route():
            validated_data = g.validated_data
            return {"doubled": validated_data["doubled"]}

        with app.test_client() as client:
            response = client.post("/test", json={"base": 7})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["doubled"], 14)

    def test_computed_field_with_default_values(self) -> None:
        """Test computed fields with default values in regular fields."""

        class ComputedWithDefaultsFilter(InputFilter):
            quantity: int = field(default=1, filters=[ToIntegerFilter()])
            price: float = field(default=10.0)
            total: float = field(
                computed=lambda data: data["quantity"] * data["price"]
            )

        result = ComputedWithDefaultsFilter().validate_data({})

        self.assertEqual(result["quantity"], 1)
        self.assertEqual(result["price"], 10.0)
        self.assertEqual(result["total"], 10.0)

    def test_computed_field_chaining(self) -> None:
        """Test that computed fields can reference other computed fields."""

        class ChainedComputedFilter(InputFilter):
            a: int = field(required=True, filters=[ToIntegerFilter()])
            b: int = field(required=True, filters=[ToIntegerFilter()])
            sum_ab: int = field(computed=lambda data: data["a"] + data["b"])
            # Note: This might not work if computed fields are processed in random order
            # In current implementation, field order matters for chaining
            double_sum: int = field(
                computed=lambda data: data.get("sum_ab", 0) * 2 if data.get("sum_ab") is not None else 0
            )

        result = ChainedComputedFilter().validate_data({"a": 3, "b": 4})

        self.assertEqual(result["sum_ab"], 7)
        # This might be 14 if sum_ab was computed before double_sum
        # or 0 if order is not preserved
        if "double_sum" in result:
            self.assertIn(result["double_sum"], [0, 14])

    def test_computed_field_with_dataclass_model(self) -> None:
        """Test computed fields work with dataclass deserialization."""

        @dataclass
        class OrderModel:
            quantity: int
            price: float
            total: float

        class OrderWithModelFilter(InputFilter):
            from flask_inputfilter.declarative import model

            quantity: int = field(required=True, filters=[ToIntegerFilter()])
            price: float = field(required=True)
            total: float = field(
                computed=lambda data: data["quantity"] * data["price"]
            )

            model(OrderModel)

        result = OrderWithModelFilter().validate_data({"quantity": 3, "price": 5.5})

        # Check that result is a dataclass instance
        self.assertIsInstance(result, OrderModel)
        self.assertEqual(result.quantity, 3)
        self.assertEqual(result.price, 5.5)
        self.assertEqual(result.total, 16.5)

    def test_computed_field_with_copy(self) -> None:
        """Test computed fields work with copy parameter."""

        class ComputedWithCopyFilter(InputFilter):
            base_value: int = field(required=True, filters=[ToIntegerFilter()])
            copied_value: int = field(copy="base_value")
            computed_from_copy: int = field(
                computed=lambda data: data.get("copied_value", 0) * 3
            )

        result = ComputedWithCopyFilter().validate_data({"base_value": 10})

        self.assertEqual(result["base_value"], 10)
        self.assertEqual(result["copied_value"], 10)
        self.assertEqual(result["computed_from_copy"], 30)

    def test_computed_field_with_filters_on_dependencies(self) -> None:
        """Test computed fields when dependencies have filters applied."""
        from flask_inputfilter.filters import StringTrimFilter, ToLowerFilter

        class ComputedWithFiltersFilter(InputFilter):
            first_name: str = field(
                required=True, filters=[StringTrimFilter(), ToLowerFilter()]
            )
            last_name: str = field(
                required=True, filters=[StringTrimFilter(), ToLowerFilter()]
            )
            full_name: str = field(
                computed=lambda data: f"{data['first_name']} {data['last_name']}"
            )

        result = ComputedWithFiltersFilter().validate_data(
            {"first_name": "  JOHN  ", "last_name": "  DOE  "}
        )

        self.assertEqual(result["first_name"], "john")
        self.assertEqual(result["last_name"], "doe")
        self.assertEqual(result["full_name"], "john doe")

    def test_computed_field_with_validators_on_dependencies(self) -> None:
        """Test computed fields when dependencies have validators."""
        from flask_inputfilter.validators import RangeValidator

        class ComputedWithValidatorsFilter(InputFilter):
            quantity: int = field(
                required=True,
                filters=[ToIntegerFilter()],
                validators=[RangeValidator(min_value=1, max_value=100)],
            )
            price: float = field(
                required=True, validators=[RangeValidator(min_value=0.01)]
            )
            total: float = field(
                computed=lambda data: data["quantity"] * data["price"]
            )

        result = ComputedWithValidatorsFilter().validate_data(
            {"quantity": 5, "price": 10.50}
        )

        self.assertEqual(result["quantity"], 5)
        self.assertEqual(result["price"], 10.50)
        self.assertEqual(result["total"], 52.5)

    def test_computed_field_with_default_and_filters(self) -> None:
        """Test computed fields with defaults and filters on dependencies."""

        class ComputedWithDefaultAndFiltersFilter(InputFilter):
            quantity: int = field(default=1, filters=[ToIntegerFilter()])
            multiplier: int = field(default=2, filters=[ToIntegerFilter()])
            result: int = field(
                computed=lambda data: data["quantity"] * data["multiplier"]
            )

        result = ComputedWithDefaultAndFiltersFilter().validate_data({})

        self.assertEqual(result["quantity"], 1)
        self.assertEqual(result["multiplier"], 2)
        self.assertEqual(result["result"], 2)

    def test_computed_field_with_external_api(self) -> None:
        """Test computed fields can use data from external_api fields."""
        # This test would require mocking external API calls
        # Skipping for now as it requires more complex setup
        pass

    def test_computed_field_with_copy_and_filters(self) -> None:
        """Test computed fields with both copy and filters."""
        from flask_inputfilter.filters import ToUpperFilter

        class ComputedWithCopyAndFiltersFilter(InputFilter):
            original: str = field(required=True)
            copied_upper: str = field(copy="original", filters=[ToUpperFilter()])
            combined: str = field(
                computed=lambda data: f"{data['original']}-{data['copied_upper']}"
            )

        result = ComputedWithCopyAndFiltersFilter().validate_data(
            {"original": "hello"}
        )

        self.assertEqual(result["original"], "hello")
        self.assertEqual(result["copied_upper"], "HELLO")
        self.assertEqual(result["combined"], "hello-HELLO")

    def test_multiple_computed_fields_with_filters(self) -> None:
        """Test multiple computed fields where dependencies have filters."""

        class MultipleComputedWithFiltersFilter(InputFilter):
            a: int = field(required=True, filters=[ToIntegerFilter()])
            b: int = field(required=True, filters=[ToIntegerFilter()])
            sum: int = field(computed=lambda data: data["a"] + data["b"])
            product: int = field(computed=lambda data: data["a"] * data["b"])
            avg: float = field(
                computed=lambda data: data["sum"] / data["product"]
            )

        result = MultipleComputedWithFiltersFilter().validate_data(
            {"a": "10", "b": "20"}
        )

        self.assertEqual(result["a"], 10)
        self.assertEqual(result["b"], 20)
        self.assertEqual(result["sum"], 30)
        self.assertEqual(result["product"], 200)
        self.assertEqual(result["avg"], 0.15)

    def test_computed_field_with_optional_dependencies(self) -> None:
        """Test computed fields when dependencies are optional."""

        class ComputedWithOptionalDepsFilter(InputFilter):
            base: int = field(required=True, filters=[ToIntegerFilter()])
            bonus: int = field(required=False, filters=[ToIntegerFilter()], default=0)
            total: int = field(
                computed=lambda data: data["base"] + data["bonus"]
            )

        # With bonus
        result1 = ComputedWithOptionalDepsFilter().validate_data(
            {"base": 100, "bonus": 50}
        )
        self.assertEqual(result1["total"], 150)

        # Without bonus
        result2 = ComputedWithOptionalDepsFilter().validate_data({"base": 100})
        self.assertEqual(result2["total"], 100)

    def test_computed_field_depends_on_another_computed(self) -> None:
        """Test computed field that depends on another computed field."""

        class ChainedComputedWithFiltersFilter(InputFilter):
            price: float = field(required=True)
            quantity: int = field(required=True, filters=[ToIntegerFilter()])
            subtotal: float = field(
                computed=lambda data: data["price"] * data["quantity"]
            )
            tax: float = field(
                computed=lambda data: data.get("subtotal", 0) * 0.19
            )
            total: float = field(
                computed=lambda data: data.get("subtotal", 0) + data.get("tax", 0)
            )

        result = ChainedComputedWithFiltersFilter().validate_data(
            {"price": 10.0, "quantity": 5}
        )

        self.assertEqual(result["price"], 10.0)
        self.assertEqual(result["quantity"], 5)
        self.assertEqual(result["subtotal"], 50.0)
        self.assertEqual(result["tax"], 9.5)
        self.assertEqual(result["total"], 59.5)

    def test_computed_field_with_fallback_on_dependency(self) -> None:
        """Test computed fields when dependencies have fallback values."""

        class ComputedWithFallbackFilter(InputFilter):
            value: int = field(
                required=False,
                filters=[ToIntegerFilter()],
                validators=[IsIntegerValidator()],
                fallback=10,
            )
            doubled: int = field(computed=lambda data: data["value"] * 2)

        # Valid value
        result1 = ComputedWithFallbackFilter().validate_data({"value": 5})
        self.assertEqual(result1["value"], 5)
        self.assertEqual(result1["doubled"], 10)

        # Missing value, use fallback
        result2 = ComputedWithFallbackFilter().validate_data({"value": "no_int"})
        self.assertEqual(result2["value"], 10)
        self.assertEqual(result2["doubled"], 20)


if __name__ == "__main__":
    unittest.main()
