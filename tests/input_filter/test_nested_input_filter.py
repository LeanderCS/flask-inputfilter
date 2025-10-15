"""Tests for nested InputFilter feature."""

from __future__ import annotations

import pytest

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import ToIntegerFilter, StringTrimFilter
from flask_inputfilter.validators import IsIntegerValidator, IsStringValidator


class TestNestedInputFilter:
    """Test nested InputFilter validation."""

    def test_basic_nested_validation(self) -> None:
        """Test basic nested InputFilter validation."""

        class UserFilter(InputFilter):
            id = field(
                required=True,
                filters=[ToIntegerFilter()],
                validators=[IsIntegerValidator()],
            )
            name = field(
                required=True,
                filters=[StringTrimFilter()],
                validators=[IsStringValidator()],
            )

        class OrderFilter(InputFilter):
            quantity = field(
                required=True,
                filters=[ToIntegerFilter()],
                validators=[IsIntegerValidator()],
            )
            user = field(required=True, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({
            "quantity": "5",
            "user": {"id": "123", "name": "  John Doe  "},
        })

        assert validated_data["quantity"] == 5
        assert validated_data["user"]["id"] == 123
        assert validated_data["user"]["name"] == "John Doe"

    def test_nested_validation_missing_required_field(self) -> None:
        """Test nested validation with missing required field."""

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])
            name = field(required=True, validators=[IsStringValidator()])

        class OrderFilter(InputFilter):
            quantity = field(required=True, validators=[IsIntegerValidator()])
            user = field(required=True, input_filter=UserFilter)

        with pytest.raises(ValidationError) as exc_info:
            OrderFilter().validate_data({"quantity": 5, "user": {"id": 123}})

        errors = exc_info.value.args[0]
        assert "user" in errors
        assert "name" in str(errors["user"])

    def test_nested_validation_invalid_type(self) -> None:
        """Test nested validation with invalid type (not a dict)."""

        class UserFilter(InputFilter):
            id = field(required=True)

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        with pytest.raises(ValidationError) as exc_info:
            OrderFilter().validate_data({"user": "invalid_string"})

        errors = exc_info.value.args[0]
        assert "user" in errors
        assert "must be a dict" in errors["user"]

    def test_nested_validation_optional_field(self) -> None:
        """Test nested validation with optional nested field."""

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])

        class OrderFilter(InputFilter):
            quantity = field(required=True, validators=[IsIntegerValidator()])
            user = field(required=False, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({"quantity": 5})

        assert validated_data["quantity"] == 5
        assert validated_data["user"] is None

    def test_nested_validation_with_none_value(self) -> None:
        """Test nested validation when value is None."""

        class UserFilter(InputFilter):
            id = field(required=True)

        class OrderFilter(InputFilter):
            user = field(required=False, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({"user": None})

        # None should bypass nested validation
        assert validated_data["user"] is None

    def test_multiple_levels_of_nesting(self) -> None:
        """Test multiple levels of nested InputFilters."""

        class AddressFilter(InputFilter):
            city = field(required=True, validators=[IsStringValidator()])
            zipcode = field(required=True, validators=[IsStringValidator()])

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])
            name = field(required=True, validators=[IsStringValidator()])
            address = field(required=True, input_filter=AddressFilter)

        class OrderFilter(InputFilter):
            quantity = field(required=True, validators=[IsIntegerValidator()])
            user = field(required=True, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({
            "quantity": 10,
            "user": {
                "id": 123,
                "name": "John Doe",
                "address": {"city": "New York", "zipcode": "10001"},
            },
        })

        assert validated_data["quantity"] == 10
        assert validated_data["user"]["id"] == 123
        assert validated_data["user"]["name"] == "John Doe"
        assert validated_data["user"]["address"]["city"] == "New York"
        assert validated_data["user"]["address"]["zipcode"] == "10001"

    def test_nested_validation_with_filters_and_validators(self) -> None:
        """Test nested validation with both filters and validators."""

        class UserFilter(InputFilter):
            id = field(
                required=True,
                filters=[ToIntegerFilter()],
                validators=[IsIntegerValidator()],
            )
            email = field(
                required=True,
                filters=[StringTrimFilter()],
                validators=[IsStringValidator()],
            )

        class OrderFilter(InputFilter):
            quantity = field(
                required=True,
                filters=[ToIntegerFilter()],
                validators=[IsIntegerValidator()],
            )
            user = field(required=True, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({
            "quantity": "15",
            "user": {"id": "456", "email": "  test@example.com  "},
        })

        assert validated_data["quantity"] == 15
        assert validated_data["user"]["id"] == 456
        assert validated_data["user"]["email"] == "test@example.com"

    def test_nested_validation_field_descriptor_access(self) -> None:
        """Test accessing nested fields via field descriptor."""

        class UserFilter(InputFilter):
            id: int = field(required=True, validators=[IsIntegerValidator()])
            name: str = field(required=True, validators=[IsStringValidator()])

        class OrderFilter(InputFilter):
            quantity: int = field(
                required=True, validators=[IsIntegerValidator()]
            )
            user: dict = field(required=True, input_filter=UserFilter)

        order_filter = OrderFilter()
        order_filter.validate_data({
            "quantity": 5,
            "user": {"id": 123, "name": "John Doe"},
        })

        assert order_filter.quantity == 5
        assert order_filter.user["id"] == 123
        assert order_filter.user["name"] == "John Doe"

    def test_nested_validation_with_default_values(self) -> None:
        """Test nested validation with default values."""

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])
            role = field(required=False, default="user")

        class OrderFilter(InputFilter):
            quantity = field(required=True, validators=[IsIntegerValidator()])
            user = field(required=True, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({
            "quantity": 3,
            "user": {"id": 789},
        })

        assert validated_data["quantity"] == 3
        assert validated_data["user"]["id"] == 789
        assert validated_data["user"]["role"] == "user"

    def test_nested_validation_error_message_context(self) -> None:
        """Test that nested validation errors include field context."""

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        with pytest.raises(ValidationError) as exc_info:
            OrderFilter().validate_data({"user": {"id": "not_an_integer"}})

        errors = exc_info.value.args[0]
        assert "user" in errors
        # Error message should indicate nested validation failed
        assert "Nested validation failed" in errors["user"]

    def test_is_valid_with_nested_filters(self) -> None:
        """Test is_valid method with nested InputFilters."""

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])

        class OrderFilter(InputFilter):
            quantity = field(required=True, validators=[IsIntegerValidator()])
            user = field(required=True, input_filter=UserFilter)

        order_filter = OrderFilter()
        order_filter.validate_data({"quantity": 5, "user": {"id": 123}})

        assert order_filter.errors == {}

        order_filter2 = OrderFilter()
        assert order_filter2.is_valid() is False

        try:
            OrderFilter().validate_data({"quantity": 5, "user": {"id": "invalid"}})
            assert False, "Should have raised ValidationError"
        except ValidationError as e:
            errors = e.args[0]
            assert "user" in errors

    def test_nested_validation_with_list_instead_of_dict(self) -> None:
        """Test nested validation fails when list is provided instead of
        dict."""

        class UserFilter(InputFilter):
            id = field(required=True)

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        with pytest.raises(ValidationError) as exc_info:
            OrderFilter().validate_data({"user": [1, 2, 3]})

        errors = exc_info.value.args[0]
        assert "user" in errors
        assert "must be a dict" in errors["user"]
        assert "list" in errors["user"]

    def test_nested_validation_with_integer_instead_of_dict(self) -> None:
        """Test nested validation fails when integer is provided."""

        class UserFilter(InputFilter):
            id = field(required=True)

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        with pytest.raises(ValidationError) as exc_info:
            OrderFilter().validate_data({"user": 123})

        errors = exc_info.value.args[0]
        assert "user" in errors
        assert "must be a dict" in errors["user"]
        assert "int" in errors["user"]

    def test_nested_validation_empty_dict(self) -> None:
        """Test nested validation with empty dict."""

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])
            name = field(required=True, validators=[IsStringValidator()])

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        with pytest.raises(ValidationError) as exc_info:
            OrderFilter().validate_data({"user": {}})

        errors = exc_info.value.args[0]
        assert "user" in errors
        assert "Nested validation failed" in errors["user"]

    def test_nested_validation_with_fallback_values(self) -> None:
        """Test nested validation with fallback values in nested filter."""

        class UserFilter(InputFilter):
            id = field(
                required=True,
                validators=[IsIntegerValidator()],
                fallback=999,
            )
            name = field(required=True, validators=[IsStringValidator()])

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({
            "user": {"id": "invalid_int", "name": "John"},
        })

        assert validated_data["user"]["id"] == 999
        assert validated_data["user"]["name"] == "John"

    def test_multiple_nested_fields_in_same_filter(self) -> None:
        """Test multiple nested fields at the same level."""

        class AddressFilter(InputFilter):
            city = field(required=True, validators=[IsStringValidator()])
            zipcode = field(required=True, validators=[IsStringValidator()])

        class ContactFilter(InputFilter):
            email = field(required=True, validators=[IsStringValidator()])
            phone = field(required=True, validators=[IsStringValidator()])

        class UserFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])
            address = field(required=True, input_filter=AddressFilter)
            contact = field(required=True, input_filter=ContactFilter)

        validated_data = UserFilter().validate_data({
            "name": "John Doe",
            "address": {"city": "NYC", "zipcode": "10001"},
            "contact": {"email": "john@example.com", "phone": "555-1234"},
        })

        assert validated_data["name"] == "John Doe"
        assert validated_data["address"]["city"] == "NYC"
        assert validated_data["address"]["zipcode"] == "10001"
        assert validated_data["contact"]["email"] == "john@example.com"
        assert validated_data["contact"]["phone"] == "555-1234"

    def test_nested_validation_with_optional_nested_fields(self) -> None:
        """Test nested filter with optional fields inside."""

        class MetadataFilter(InputFilter):
            created_by = field(required=False, validators=[IsStringValidator()])
            updated_by = field(required=False, validators=[IsStringValidator()])

        class OrderFilter(InputFilter):
            quantity = field(required=True, validators=[IsIntegerValidator()])
            metadata = field(required=True, input_filter=MetadataFilter)

        validated_data = OrderFilter().validate_data({
            "quantity": 5,
            "metadata": {},
        })

        assert validated_data["quantity"] == 5
        assert validated_data["metadata"]["created_by"] is None
        assert validated_data["metadata"]["updated_by"] is None

    def test_deeply_nested_validation_error_propagation(self) -> None:
        """Test error propagation through multiple nesting levels."""

        class AddressFilter(InputFilter):
            city = field(required=True, validators=[IsStringValidator()])
            zipcode = field(required=True, validators=[IsIntegerValidator()])

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])
            address = field(required=True, input_filter=AddressFilter)

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        with pytest.raises(ValidationError) as exc_info:
            OrderFilter().validate_data({
                "user": {"id": 123, "address": {"city": "NYC", "zipcode": "invalid"}},
            })

        errors = exc_info.value.args[0]
        assert "user" in errors
        assert "Nested validation failed" in errors["user"]

    def test_nested_validation_with_extra_fields(self) -> None:
        """Test nested validation ignores extra fields not defined in
        filter."""

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])
            name = field(required=True, validators=[IsStringValidator()])

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({
            "user": {
                "id": 123,
                "name": "John",
                "extra_field": "should be ignored",
                "another_extra": 999,
            },
        })

        assert validated_data["user"]["id"] == 123
        assert validated_data["user"]["name"] == "John"
        # Extra fields should not be in validated data
        assert "extra_field" not in validated_data["user"]
        assert "another_extra" not in validated_data["user"]

    def test_nested_validation_with_boolean_false_value(self) -> None:
        """Test that False boolean value doesn't get treated as None."""

        class SettingsFilter(InputFilter):
            enabled = field(required=True)

        class ConfigFilter(InputFilter):
            settings = field(required=True, input_filter=SettingsFilter)

        validated_data = ConfigFilter().validate_data({
            "settings": {"enabled": False},
        })

        assert validated_data["settings"]["enabled"] is False

    def test_nested_validation_with_zero_value(self) -> None:
        """Test that zero value doesn't get treated as None."""

        class PriceFilter(InputFilter):
            amount = field(required=True, validators=[IsIntegerValidator()])

        class ProductFilter(InputFilter):
            price = field(required=True, input_filter=PriceFilter)

        validated_data = ProductFilter().validate_data({
            "price": {"amount": 0},
        })

        assert validated_data["price"]["amount"] == 0

    def test_nested_validation_with_empty_string_value(self) -> None:
        """Test nested validation with empty string value."""

        class UserFilter(InputFilter):
            name = field(required=True, validators=[IsStringValidator()])

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({
            "user": {"name": ""},
        })

        assert validated_data["user"]["name"] == ""

    def test_nested_filter_reusability(self) -> None:
        """Test that the same nested filter class can be reused."""

        class AddressFilter(InputFilter):
            city = field(required=True, validators=[IsStringValidator()])

        class UserFilter(InputFilter):
            home_address = field(required=True, input_filter=AddressFilter)
            work_address = field(required=True, input_filter=AddressFilter)

        validated_data = UserFilter().validate_data({
            "home_address": {"city": "NYC"},
            "work_address": {"city": "LA"},
        })

        assert validated_data["home_address"]["city"] == "NYC"
        assert validated_data["work_address"]["city"] == "LA"

    def test_nested_validation_with_computed_fields_in_parent(self) -> None:
        """Test nested validation works with computed fields in parent."""

        class UserFilter(InputFilter):
            first_name = field(required=True, validators=[IsStringValidator()])
            last_name = field(required=True, validators=[IsStringValidator()])

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)
            total = field(required=True, validators=[IsIntegerValidator()])
            total_with_tax = field(
                computed=lambda data: data.get("total", 0) * 1.1
            )

        validated_data = OrderFilter().validate_data({
            "user": {"first_name": "John", "last_name": "Doe"},
            "total": 100,
        })

        assert validated_data["user"]["first_name"] == "John"
        assert validated_data["user"]["last_name"] == "Doe"
        assert validated_data["total"] == 100
        assert abs(validated_data["total_with_tax"] - 110.0) < 0.0001

    def test_nested_validation_preserves_field_order(self) -> None:
        """Test that nested validation preserves field order."""

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])
            name = field(required=True, validators=[IsStringValidator()])
            email = field(required=True, validators=[IsStringValidator()])

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({
            "user": {"id": 123, "name": "John", "email": "john@example.com"},
        })

        # All fields should be present
        assert "id" in validated_data["user"]
        assert "name" in validated_data["user"]
        assert "email" in validated_data["user"]

    def test_nested_validation_with_copy_field_in_nested_filter(self) -> None:
        """Test nested validation with copy field inside nested filter."""

        class UserFilter(InputFilter):
            id = field(required=True, validators=[IsIntegerValidator()])
            user_id_copy = field(copy="id")

        class OrderFilter(InputFilter):
            user = field(required=True, input_filter=UserFilter)

        validated_data = OrderFilter().validate_data({
            "user": {"id": 123},
        })

        assert validated_data["user"]["id"] == 123
        assert validated_data["user"]["user_id_copy"] == 123
