import unittest
from dataclasses import dataclass
from unittest.mock import Mock, patch

from flask import Flask, g, jsonify, request
from flask_inputfilter import InputFilter
from flask_inputfilter.models import BaseCondition
from flask_inputfilter.conditions import ExactlyOneOfCondition
from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.filters import (
    StringSlugifyFilter,
    ToFloatFilter,
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
    RegexValidator,
)


class TestInputFilter(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a basic InputFilter instance for testing."""

        self.inputFilter = InputFilter()

    def test_validate_decorator(self) -> None:
        """Test that the validate decorator works."""

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add(
                    name="username",
                    required=True,
                )
                self.add(
                    name="age",
                    required=False,
                    default=18,
                    validators=[IsIntegerValidator()],
                )

        app = Flask(__name__)

        @app.route("/test", methods=["GET", "POST"])
        @MyInputFilter.validate()
        def test_route():
            validated_data = g.validated_data
            return jsonify(validated_data)

        with app.test_client() as client:
            response = client.get(
                "/test", query_string={"username": "test_user"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json, {"username": "test_user", "age": 18}
            )

            response = client.post(
                "/test", json={"username": "test_user", "age": 25}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json, {"username": "test_user", "age": 25}
            )

            response = client.post(
                "/test", json={"username": "test_user", "age": "not_an_int"}
            )
            self.assertEqual(response.status_code, 400)

    def test_route_params(self) -> None:
        """Test that route parameters are validated correctly."""

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add(
                    name="username",
                )

        app = Flask(__name__)

        @app.route("/test-delete/<username>", methods=["DELETE"])
        @MyInputFilter.validate()
        def test_route(username):
            self.assertEqual(g.validated_data, {"username": "test_user"})
            return jsonify(g.validated_data)

        with app.test_client() as client:
            response = client.delete("/test-delete/test_user")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"username": "test_user"})

    def test_custom_method(self) -> None:
        """Test that a method not supported by the InputFilter instance raises
        a TypeError."""

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__(methods=["GET"])

        app = Flask(__name__)

        @app.route("/test-custom", methods=["GET", "POST"])
        @MyInputFilter.validate()
        def test_custom_route():
            validated_data = g.validated_data
            return jsonify(validated_data)

        with app.test_client() as client:
            response = client.post("/test-custom")
            self.assertEqual(response.status_code, 405)

            response = client.get("/test-custom")
            self.assertEqual(response.status_code, 200)

    def test_validation_error_response(self):
        """Tests the behavior of the application when a validation error occurs
        due to invalid input data."""

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add(
                    name="age",
                    required=False,
                    default=18,
                    validators=[
                        IsIntegerValidator(error_message="Invalid data")
                    ],
                )

        app = Flask(__name__)

        @app.route("/test", methods=["GET"])
        @MyInputFilter.validate()
        def test_route():
            return "Success"

        with app.test_client() as client:
            response = client.get("/test", query_string={"age": "not_an_int"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json.get("age"), "Invalid data")

    def test_validate_decorator_non_dict_json(self) -> None:
        """Test that non-dictionary JSON data is handled correctly."""

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add("username", default="default_user")
                self.add("age", default=18)

        app = Flask(__name__)

        @app.route("/test", methods=["POST"])
        @MyInputFilter.validate()
        def test_route():
            return jsonify(g.validated_data)

        with app.test_client() as client:
            response = client.post(
                "/test",
                json=["item1", "item2", "item3"],
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json, {"username": "default_user", "age": 18}
            )

            response = client.post(
                "/test",
                data='"just a string"',
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json, {"username": "default_user", "age": 18}
            )

            response = client.post(
                "/test", data="42", content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json, {"username": "default_user", "age": 18}
            )

            response = client.post(
                "/test", data="true", content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json, {"username": "default_user", "age": 18}
            )

            response = client.post(
                "/test", json="null", content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json, {"username": "default_user", "age": 18}
            )

    def test_validate_decorator_invalid_json(self) -> None:
        """Test that invalid JSON is handled correctly."""

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add("field", default="default")

        app = Flask(__name__)

        @app.route("/test", methods=["POST"])
        @MyInputFilter.validate()
        def test_route():
            return jsonify(g.validated_data)

        with app.test_client() as client:
            response = client.post(
                "/test", data="{invalid json}", content_type="application/json"
            )
            self.assertEqual(response.status_code, 400)

    def test_validate_decorator_mixed_json_types(self) -> None:
        """Test various JSON types that should be converted to empty dict."""

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add("name", required=False)
                self.add("value", required=False)

        app = Flask(__name__)

        @app.route("/test", methods=["POST"])
        @MyInputFilter.validate()
        def test_route():
            return jsonify(
                {
                    "validated": g.validated_data,
                    "original_type": type(request.get_json()).__name__,
                }
            )

        with app.test_client() as client:
            response = client.post(
                "/test",
                json=[{"key": "value"}, ["nested", "array"]],
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json["validated"], {"name": None, "value": None}
            )
            self.assertEqual(response.json["original_type"], "list")

            response = client.post(
                "/test", json=3.14, content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json["validated"], {"name": None, "value": None}
            )
            self.assertEqual(response.json["original_type"], "float")

    def test_validate_decorator_required_fields_with_non_dict(self) -> None:
        """Test that required fields raise errors when non-dict JSON is
        sent."""

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add("username", required=True)
                self.add("email", required=True)

        app = Flask(__name__)

        @app.route("/test", methods=["POST"])
        @MyInputFilter.validate()
        def test_route():
            return jsonify(g.validated_data)

        with app.test_client() as client:
            response = client.post(
                "/test",
                json=["user1", "user2"],
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 400)
            response_data = response.get_json()
            self.assertIn("username", response_data)
            self.assertIn("email", response_data)

            # Test mit String
            response = client.post(
                "/test", data='"some string"', content_type="application/json"
            )
            self.assertEqual(response.status_code, 400)
            response_data = response.get_json()
            self.assertIn("username", response_data)
            self.assertIn("email", response_data)

    def test_validate_decorator_with_fallback_and_non_dict(self) -> None:
        """Test that fallback values work correctly with non-dict JSON."""

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add("status", required=True, fallback="active")
                self.add(
                    "count",
                    required=True,
                    fallback=0,
                    validators=[IsIntegerValidator()],
                )

        app = Flask(__name__)

        @app.route("/test", methods=["POST"])
        @MyInputFilter.validate()
        def test_route():
            return jsonify(g.validated_data)

        with app.test_client() as client:
            response = client.post(
                "/test", json=False, content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"status": "active", "count": 0})

            response = client.post(
                "/test", json=[], content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"status": "active", "count": 0})

    def test_optional(self) -> None:
        """Test that optional field validation works."""

        self.inputFilter.add("name", required=True)

        self.inputFilter.validate_data({"name": "Alice"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data({})

    def test_default(self) -> None:
        """Test that default field works."""

        self.inputFilter.add("available", default=True)

        validated_data = self.inputFilter.validate_data({})
        self.assertTrue(validated_data["available"])

        validated_data = self.inputFilter.validate_data({"available": False})
        self.assertFalse(validated_data["available"])

    def test_fallback(self) -> None:
        """Test that fallback field works."""
        self.inputFilter.add("available", required=True, fallback=True)
        self.inputFilter.add(
            "color",
            required=True,
            fallback="red",
            validators=[InArrayValidator(["red", "green", "blue"])],
        )

        validated_data = self.inputFilter.validate_data({"color": "yellow"})

        self.assertTrue(validated_data["available"])
        self.assertEqual(validated_data["color"], "red")

        validated_data = self.inputFilter.validate_data(
            {"available": False, "color": "green"}
        )

        self.assertFalse(validated_data["available"])
        self.assertEqual(validated_data["color"], "green")

    def test_fallback_with_default(self) -> None:
        """Test that fallback field works."""

        self.inputFilter.add(
            "available", required=True, default=True, fallback=False
        )
        self.inputFilter.add(
            "color",
            default="red",
            fallback="blue",
            validators=[InArrayValidator(["red", "green", "blue"])],
        )

        validated_data = self.inputFilter.validate_data({})

        self.assertFalse(validated_data["available"])
        self.assertEqual(validated_data["color"], "red")

        validated_data = self.inputFilter.validate_data({"available": False})

        self.assertFalse(validated_data["available"])

        self.inputFilter.add("required_without_fallback", required=True)

        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data({})

    def test_count(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.assertEqual(self.inputFilter.count(), 2)

    def test_get_error_message(self) -> None:
        self.inputFilter.add("field", required=True)
        self.inputFilter.is_valid()

        self.assertEqual(
            self.inputFilter.get_error_message("field"),
            "Field 'field' is required.",
        )

    def test_get_error_messages(self) -> None:
        self.inputFilter.add(
            "field", required=True, validators=[IsIntegerValidator()]
        )
        self.inputFilter.add(
            "field2", required=True, validators=[IsIntegerValidator()]
        )
        self.inputFilter.set_data({"field2": "value2"})
        self.inputFilter.is_valid()

        self.assertEqual(
            self.inputFilter.get_error_messages().get("field"),
            "Field 'field' is required.",
        )
        self.assertEqual(
            self.inputFilter.get_error_messages().get("field2"),
            "Value 'value2' is not an integer.",
        )

    def test_global_error_messages(self) -> None:
        self.inputFilter.add("field", required=True)
        self.inputFilter.add("field2", required=True)
        self.inputFilter.set_data({"field2": "value2"})
        self.inputFilter.add_global_validator(IsIntegerValidator())

        self.inputFilter.is_valid()

        self.assertEqual(
            self.inputFilter.get_error_messages().get("field"),
            "Field 'field' is required.",
        )
        self.assertEqual(
            self.inputFilter.get_error_messages().get("field2"),
            "Value 'value2' is not an integer.",
        )

    def test_condition_error_messages(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.add("field2")
        self.inputFilter.add_condition(
            ExactlyOneOfCondition(["field", "field2"])
        )
        self.inputFilter.set_data({"field2": "value2"})
        self.inputFilter.is_valid()

        self.assertEqual(self.inputFilter.get_error_messages(), {})

        self.inputFilter.set_data({"field": "value", "field2": "value2"})
        self.inputFilter.is_valid()

        self.assertEqual(
            self.inputFilter.get_error_messages().get("_condition"),
            "Condition 'ExactlyOneOfCondition' not met.",
        )

    def test_get_input(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.set_data({"field": "value"})

        self.assertFalse(self.inputFilter.get_input("field").required)

        self.inputFilter.add("field2", required=True)
        self.assertTrue(self.inputFilter.get_input("field2").required)

    def test_get_inputs(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2", required=True, default=True)
        self.inputFilter.set_data({"field1": "value1", "field2": "value2"})

        field1 = self.inputFilter.get_inputs().get("field1")
        field2 = self.inputFilter.get_inputs().get("field2")

        self.assertFalse(field1.required)
        self.assertTrue(field2.required)

        self.assertIsNone(field1.default)
        self.assertTrue(field2.default)

    def test_get_raw_value(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.set_unfiltered_data(
            {"field": "raw_value", "unknown_field": "raw_value2"}
        )

        self.assertEqual(self.inputFilter.get_raw_value("field"), "raw_value")

    def test_get_raw_values(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")
        self.inputFilter.set_unfiltered_data(
            {"field1": "raw1", "field2": "raw2", "unknown_field": "raw3"}
        )

        self.assertEqual(
            self.inputFilter.get_raw_values(),
            {"field1": "raw1", "field2": "raw2"},
        )

        self.inputFilter.clear()

        self.assertEqual(
            self.inputFilter.get_raw_values(),
            {},
        )

    def test_get_unfiltered_data(self) -> None:
        self.inputFilter.add("field", filters=[ToIntegerFilter()])
        self.inputFilter.set_data({"field": "raw", "unknown_field": "raw2"})

        self.assertEqual(
            self.inputFilter.get_unfiltered_data(),
            {"field": "raw", "unknown_field": "raw2"},
        )

    def test_get_value(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.set_data({"field": "value"})

        self.inputFilter.is_valid()
        self.assertEqual(self.inputFilter.get_value("field"), "value")

    def test_get_values(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")
        self.inputFilter.set_data(
            {"field1": "value1", "field2": "value2", "field3": "value3"}
        )

        self.inputFilter.is_valid()
        self.assertEqual(
            self.inputFilter.get_values(),
            {"field1": "value1", "field2": "value2"},
        )

    def test_has(self) -> None:
        self.inputFilter.add("field")

        self.assertTrue(self.inputFilter.has("field"))
        self.assertFalse(self.inputFilter.has("unknown_field"))

    def test_get_conditions(self) -> None:
        condition1 = ExactlyOneOfCondition(["test"])
        self.inputFilter.add_condition(condition1)

        self.assertEqual(self.inputFilter.get_conditions(), [condition1])

    def test_get_global_filters(self) -> None:
        filter1 = ToIntegerFilter()
        self.inputFilter.add_global_filter(filter1)

        self.assertEqual(self.inputFilter.get_global_filters(), [filter1])

    def test_get_global_validators(self) -> None:
        validator1 = InArrayValidator(["test"])
        self.inputFilter.add_global_validator(validator1)

        self.assertEqual(
            self.inputFilter.get_global_validators(), [validator1]
        )

    def test_has_unknown(self) -> None:
        self.inputFilter.add("field1")

        self.inputFilter.set_data(
            {"field1": "value1", "unknown_field": "value2"}
        )
        self.assertTrue(self.inputFilter.has_unknown())

        self.inputFilter.set_data({})
        self.assertTrue(self.inputFilter.has_unknown())

        self.inputFilter.remove("field1")
        self.assertFalse(self.inputFilter.has_unknown())

    def test_is_valid(self) -> None:
        self.inputFilter.add("field", required=True)

        self.inputFilter.set_data({"field": "value"})
        self.assertTrue(self.inputFilter.is_valid())

        self.inputFilter.set_data({})
        self.assertFalse(self.inputFilter.is_valid())

    def test_merge(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.set_data({"field1": "value1"})

        input_filter = InputFilter()
        input_filter.add("field2")
        self.inputFilter.merge(input_filter)

        self.inputFilter.is_valid()
        self.assertEqual(
            self.inputFilter.get_values(), {"field1": "value1", "field2": None}
        )

        with self.assertRaises(TypeError):
            self.inputFilter.merge("no input filter")

    def test_merge_overrides_field(self) -> None:
        self.inputFilter.add("field1")

        input_filter = InputFilter()
        filter_ = ToIntegerFilter()
        input_filter.add("field1", filters=[filter_])
        self.inputFilter.merge(input_filter)

        self.inputFilter.is_valid()
        self.assertEqual(
            self.inputFilter.get_input("field1").filters, [filter_]
        )

    def test_merge_combined_conditions(self) -> None:
        condition1 = ExactlyOneOfCondition(["test"])
        self.inputFilter.add_condition(condition1)

        condition2 = ExactlyOneOfCondition(["test2"])
        input_filter = InputFilter()
        input_filter.add_condition(condition2)

        self.inputFilter.merge(input_filter)

        self.assertEqual(
            self.inputFilter.get_conditions(), [condition1, condition2]
        )

    def test_merge_combines_global_filters(self) -> None:
        filter1 = ToIntegerFilter()
        self.inputFilter.add_global_filter(filter1)

        filter2 = ToFloatFilter()
        input_filter = InputFilter()
        input_filter.add_global_filter(filter2)

        self.inputFilter.merge(input_filter)

        self.assertEqual(
            self.inputFilter.get_global_filters(), [filter1, filter2]
        )

    def test_merge_replace_global_filters(self) -> None:
        filter1 = ToIntegerFilter()
        self.inputFilter.add_global_filter(filter1)

        filter2 = ToIntegerFilter()
        input_filter = InputFilter()
        input_filter.add_global_filter(filter2)

        self.inputFilter.merge(input_filter)

        self.assertEqual(self.inputFilter.get_global_filters(), [filter2])

    def test_merge_combines_global_validators(self) -> None:
        validator1 = InArrayValidator(["test"])
        self.inputFilter.add_global_validator(validator1)

        validator2 = IsIntegerValidator()
        input_filter = InputFilter()
        input_filter.add_global_validator(validator2)

        self.inputFilter.merge(input_filter)

        self.assertEqual(
            self.inputFilter.get_global_validators(), [validator1, validator2]
        )

    def test_merge_replace_global_validators(self) -> None:
        self.inputFilter.add_global_validator(InArrayValidator(["test"]))

        validator2 = InArrayValidator(["test2"])
        input_filter = InputFilter()
        input_filter.add_global_validator(validator2)

        self.inputFilter.merge(input_filter)

        self.assertEqual(
            self.inputFilter.get_global_validators(), [validator2]
        )

    def test_remove(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.set_data({"field": "value"})

        self.assertTrue(self.inputFilter.has("field"))

        self.inputFilter.remove("field")
        self.assertFalse(self.inputFilter.has("field"))

    def test_replace(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.set_data({"field": "value"})

        with self.assertRaises(ValueError):
            self.inputFilter.add("field")

        self.inputFilter.replace("field", filters=[ToUpperFilter()])
        updated_data = self.inputFilter.validate_data({"field": "value"})
        self.assertEqual(updated_data["field"], "VALUE")

    def test_clear(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.set_data({"field": "value"})

        self.inputFilter.is_valid()
        self.assertEqual(self.inputFilter.get_value("field"), "value")

        self.inputFilter.clear()
        self.assertIsNone(self.inputFilter.get_value("field"))

    def test_set_unfiltered_data(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.set_unfiltered_data({"field": "raw_value"})
        self.assertEqual(self.inputFilter.get_raw_value("field"), "raw_value")

    def test_steps(self) -> None:
        """Test that custom steps works."""
        self.inputFilter.add(
            "name_upper",
            steps=[
                ToUpperFilter(),
                InArrayValidator(["MAURICE"]),
                ToLowerFilter(),
            ],
        )

        validated_data = self.inputFilter.validate_data(
            {"name_upper": "Maurice"}
        )
        self.assertEqual(validated_data["name_upper"], "maurice")

        validated_data = None
        with self.assertRaises(ValidationError):
            validated_data = self.inputFilter.validate_data(
                {"name_upper": "Alice"}
            )
        self.assertIsNone(validated_data)

        self.inputFilter.add(
            "fallback",
            fallback="FALLBACK",
            steps=[
                ToUpperFilter(),
                InArrayValidator(["FALLBACK"]),
                ToLowerFilter(),
            ],
        )

        validated_data = self.inputFilter.validate_data(
            {"fallback": "fallback"}
        )
        self.assertEqual(validated_data["fallback"], "fallback")

        self.inputFilter.add(
            "default",
            default="DEFAULT",
            steps=[
                ToUpperFilter(),
                InArrayValidator(["DEFAULT"]),
                ToLowerFilter(),
            ],
        )

        validated_data = self.inputFilter.validate_data({})
        self.assertEqual(validated_data["default"], "DEFAULT")

        self.inputFilter.add(
            "fallback_with_default",
            default="default",
            fallback="fallback",
            steps=[
                ToUpperFilter(),
                InArrayValidator(["DEFAULT"]),
                ToLowerFilter(),
            ],
        )

        validated_data = self.inputFilter.validate_data({})
        self.assertEqual(validated_data["fallback_with_default"], "default")

        validated_data = self.inputFilter.validate_data(
            {"fallback_with_default": "fallback"}
        )
        self.assertEqual(validated_data["fallback_with_default"], "fallback")

        self.inputFilter.add(
            "required_without_fallback",
            required=True,
            steps=[
                ToUpperFilter(),
                InArrayValidator(["REQUIRED"]),
                ToLowerFilter(),
            ],
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data({})

    @patch("requests.request")
    def test_external_api(self, mock_request: Mock) -> None:
        """Test that external API calls work."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"is_valid": True}
        mock_request.return_value = mock_response

        # Add a field where the external API receives its value
        self.inputFilter.add("name", default="test_user")

        # Add a field with external API configuration
        self.inputFilter.add(
            "is_valid",
            external_api=ExternalApiConfig(
                url="https://api.example.com/validate_user/{{name}}",
                method="GET",
                data_key="is_valid",
            ),
        )

        # API returns valid result
        validated_data = self.inputFilter.validate_data({})

        self.assertTrue(validated_data["is_valid"])
        expected_url = "https://api.example.com/validate_user/test_user"
        mock_request.assert_called_with(
            headers={}, method="GET", url=expected_url, params={}
        )

        # API returns invalid result
        mock_response.status_code = 500
        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data({"name": "invalid_user"})

    @patch("requests.request")
    def test_external_api_params(self, mock_request: Mock) -> None:
        """Test that external API calls work."""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"is_valid": True}
        mock_request.return_value = mock_response

        self.inputFilter.add("name")

        self.inputFilter.add("hash")

        self.inputFilter.add(
            "is_valid",
            required=True,
            external_api=ExternalApiConfig(
                url="https://api.example.com/validate_user/{{name}}",
                method="GET",
                params={"hash": "{{hash}}", "id": 123},
                data_key="is_valid",
                headers={"custom_header": "value"},
                api_key="1234",
            ),
        )

        validated_data = self.inputFilter.validate_data(
            {"name": "test_user", "hash": "1234"}
        )

        self.assertTrue(validated_data["is_valid"])
        expected_url = "https://api.example.com/validate_user/test_user"
        mock_request.assert_called_with(
            headers={"Authorization": "Bearer 1234", "custom_header": "value"},
            method="GET",
            url=expected_url,
            params={"hash": "1234", "id": 123},
        )

        mock_response.status_code = 500
        mock_response.json.return_value = {"is_valid": False}
        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data(
                {"name": "invalid_user", "hash": "1234"}
            )

        mock_response.json.return_value = {}
        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data(
                {"name": "invalid_user", "hash": "1234"}
            )

    @patch("requests.request")
    def test_external_api_fallback(self, mock_request: Mock) -> None:
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"name": True}
        mock_request.return_value = mock_response

        self.inputFilter.add(
            "username_with_fallback",
            required=True,
            fallback="fallback_user",
            external_api=ExternalApiConfig(
                url="https://api.example.com/validate_user",
                method="GET",
                params={"user": "{{value}}"},
                data_key="name",
            ),
        )

        validated_data = self.inputFilter.validate_data(
            {"username_with_fallback": None}
        )
        self.assertEqual(
            validated_data["username_with_fallback"], "fallback_user"
        )

    @patch("requests.request")
    def test_external_api_default(self, mock_request: Mock) -> None:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        # API call with fallback
        self.inputFilter.add(
            "username_with_default",
            default="default_user",
            external_api=ExternalApiConfig(
                url="https://api.example.com/validate_user",
                method="GET",
                params={"user": "{{value}}"},
                data_key="name",
            ),
        )

        validated_data = self.inputFilter.validate_data({})
        self.assertEqual(
            validated_data["username_with_default"], "default_user"
        )

    @patch("requests.request")
    def test_external_api_fallback_with_default(
        self, mock_request: Mock
    ) -> None:
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"name": True}
        mock_request.return_value = mock_response

        self.inputFilter.add(
            "username_with_fallback",
            required=True,
            default="default_user",
            fallback="fallback_user",
            external_api=ExternalApiConfig(
                url="https://api.example.com/validate_user",
                method="GET",
                params={"user": "{{value}}"},
                data_key="name",
            ),
        )

        validated_data = self.inputFilter.validate_data(
            {"username_with_fallback": None}
        )
        self.assertEqual(
            validated_data["username_with_fallback"], "fallback_user"
        )

    @patch("requests.request")
    def test_external_invalid_api_response(self, mock_request: Mock) -> None:
        """Test that a non-JSON API response raises a ValidationError."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_request.return_value = mock_response

        self.inputFilter.add(
            "is_valid",
            external_api=ExternalApiConfig(
                url="https://api.example.com/validate",
                method="GET",
            ),
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data({})

    @patch("requests.request")
    def test_external_api_response_with_no_data_key(
        self, mock_request: Mock
    ) -> None:
        """Test that an API response with no data key raises a
        ValidationError."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        self.inputFilter.add(
            "is_valid",
            external_api=ExternalApiConfig(
                url="https://api.example.com/validate",
                method="GET",
            ),
        )

        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data({})

    def test_multiple_validators(self) -> None:
        """Test that multiple validators are applied correctly."""
        self.inputFilter.add(
            "username",
            required=True,
            validators=[
                RegexValidator(r"^[a-zA-Z0-9_]+$"),
                LengthValidator(min_length=3, max_length=15),
            ],
        )

        validated_data = self.inputFilter.validate_data(
            {"username": "valid_user"}
        )
        self.assertEqual(validated_data["username"], "valid_user")

        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data({"username": "no"})

    def test_conditions(self) -> None:
        """Test that conditions are checked correctly."""

        class MockCondition(BaseCondition):
            def check(self, data: dict) -> bool:
                return data.get("age") > 18

        self.inputFilter.add("age", required=True)
        self.inputFilter.add_condition(MockCondition())

        validated_data = self.inputFilter.validate_data({"age": 20})
        self.assertEqual(validated_data["age"], 20)

        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data({"age": 17})

    def test_global_filter_applied_to_all_fields(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.add_global_filter(ToUpperFilter())

        validated_data = self.inputFilter.validate_data(
            {"field1": "test", "field2": "example"}
        )

        self.assertEqual(validated_data["field1"], "TEST")
        self.assertEqual(validated_data["field2"], "EXAMPLE")

    def test_global_filter_with_no_fields(self) -> None:
        self.inputFilter.add_global_filter(ToUpperFilter())

        validated_data = self.inputFilter.validate_data({})
        self.assertEqual(validated_data, {})

    def test_global_validator_applied_to_all_fields(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")
        self.inputFilter.add_global_validator(IsStringValidator())

        with self.assertRaises(ValidationError):
            self.inputFilter.validate_data(
                {"field1": 345, "field2": "example"}
            )

        validated_data = self.inputFilter.validate_data(
            {"field1": "test", "field2": "example"}
        )

        self.assertEqual(validated_data["field1"], "test")
        self.assertEqual(validated_data["field2"], "example")

    def test_global_validator_with_no_fields(self) -> None:
        self.inputFilter.add_global_validator(IsIntegerValidator())

        validated_data = self.inputFilter.validate_data({})
        self.assertEqual(validated_data, {})

    def test_copy(self) -> None:
        """Test that copy copies the value of the field to the current
        field."""
        self.inputFilter.add("username")

        self.inputFilter.add(
            "escapedUsername", copy="username", filters=[StringSlugifyFilter()]
        )

        validated_data = self.inputFilter.validate_data(
            {"username": "test user"}
        )
        self.assertEqual(validated_data["escapedUsername"], "test-user")

    def test_serialize_and_set_model(self) -> None:
        """Test that InputFilter.serialize() serializes the validated data."""

        class User:
            def __init__(self, username: str):
                self.username = username

        @dataclass
        class User2:
            username: str

        self.inputFilter.add("username")
        self.inputFilter.set_data({"username": "test user"})

        self.inputFilter.is_valid()

        self.inputFilter.set_model(User)
        self.assertEqual(self.inputFilter.serialize().username, "test user")

        self.inputFilter.set_model(None)
        self.assertEqual(
            self.inputFilter.serialize(), {"username": "test user"}
        )

        self.inputFilter.set_model(User2)
        self.assertEqual(self.inputFilter.serialize().username, "test user")

    def test_model_class_serialisation(self) -> None:
        """Test that the model class is serialized correctly."""

        class User:
            def __init__(self, username: str):
                self.username = username

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add("username")
                self.set_model(User)

        app = Flask(__name__)

        @app.route("/test-custom", methods=["GET"])
        @MyInputFilter.validate()
        def test_custom_route():
            validated_data = g.validated_data

            return jsonify(validated_data.username)

        with app.test_client() as client:
            response = client.get(
                "/test-custom", query_string={"username": "test user"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, "test user")

            response = client.get(
                "/test-custom",
                query_string={"username": "test user2", "age": 20},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, "test user2")

            response = client.get("/test-custom", query_string={"age": 20})
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(response.json)


if __name__ == "__main__":
    unittest.main()
