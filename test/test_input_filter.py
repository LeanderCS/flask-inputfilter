import unittest
from unittest.mock import Mock, patch

from flask import Flask, g, jsonify

from flask_inputfilter import InputFilter
from flask_inputfilter.Condition import BaseCondition
from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Filter import (
    SlugifyFilter,
    ToIntegerFilter,
    ToLowerFilter,
    ToUpperFilter,
)
from flask_inputfilter.Model import ExternalApiConfig, FieldModel
from flask_inputfilter.Validator import (
    InArrayValidator,
    IsIntegerValidator,
    IsStringValidator,
    LengthValidator,
    RegexValidator,
)


class TestInputFilter(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up a basic InputFilter instance for testing.
        """

        self.inputFilter = InputFilter()

    def test_validate_decorator(self) -> None:
        """
        Test that the validate decorator works.
        """

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
        """
        Test that route parameters are validated correctly.
        """

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

    def test_unsupported_method(self) -> None:
        """
        Test that a method not supported by the InputFilter instance raises
        a TypeError.
        """

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__(methods=["GET"])

        app = Flask(__name__)

        @app.route("/test-unsupported", methods=["POST"])
        @MyInputFilter.validate()
        def test_unsupported_route():
            validated_data = g.validated_data
            return jsonify(validated_data)

        with app.test_client() as client:
            response = client.post("/test-unsupported")
            self.assertEqual(response.status_code, 405)

    @patch.object(InputFilter, "validateData")
    def test_validation_error_response(self, mock_validateData):
        mock_validateData.side_effect = ValidationError("Invalid data")

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add(
                    name="age",
                    required=False,
                    default=18,
                    validators=[IsIntegerValidator()],
                )

        app = Flask(__name__)

        @app.route("/test", methods=["GET"])
        @MyInputFilter.validate()
        def test_route():
            return "Success"

        with app.test_client() as client:
            response = client.get("/test", query_string={"age": "not_an_int"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), "Invalid data")

    @patch.object(InputFilter, "validateData")
    def test_custom_supported_methods(self, mock_validateData):
        mock_validateData.return_value = {"username": "test_user", "age": 25}

        class MyInputFilter(InputFilter):
            def __init__(self):
                super().__init__(methods=["GET"])

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
                response.json, {"username": "test_user", "age": 25}
            )

            response = client.post("/test", json={"username": "test_user"})
            self.assertEqual(response.status_code, 405)

    def test_optional(self) -> None:
        """
        Test that optional field validation works.
        """
        self.inputFilter.add("name", required=True)

        self.inputFilter.validateData({"name": "Alice"})

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({})

    def test_default(self) -> None:
        """
        Test that default field works.
        """
        self.inputFilter.add("available", default=True)

        validated_data = self.inputFilter.validateData({})
        self.assertEqual(validated_data["available"], True)

        validated_data = self.inputFilter.validateData({"available": False})
        self.assertEqual(validated_data["available"], False)

    def test_fallback(self) -> None:
        """
        Test that fallback field works.
        """
        self.inputFilter.add("available", required=True, fallback=True)
        self.inputFilter.add(
            "color",
            required=True,
            fallback="red",
            validators=[InArrayValidator(["red", "green", "blue"])],
        )

        validated_data = self.inputFilter.validateData({"color": "yellow"})

        self.assertEqual(validated_data["available"], True)
        self.assertEqual(validated_data["color"], "red")

        validated_data = self.inputFilter.validateData(
            {"available": False, "color": "green"}
        )

        self.assertEqual(validated_data["available"], False)
        self.assertEqual(validated_data["color"], "green")

    def test_fallback_with_default(self) -> None:
        """
        Test that fallback field works.
        """

        self.inputFilter.add(
            "available", required=True, default=True, fallback=False
        )
        self.inputFilter.add(
            "color",
            default="red",
            fallback="blue",
            validators=[InArrayValidator(["red", "green", "blue"])],
        )

        validated_data = self.inputFilter.validateData({})

        self.assertEqual(validated_data["available"], False)
        self.assertEqual(validated_data["color"], "red")

        validated_data = self.inputFilter.validateData({"available": False})

        self.assertEqual(validated_data["available"], False)

        self.inputFilter.add("required_without_fallback", required=True)

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({})

    def test_count(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.assertEqual(self.inputFilter.count(), 2)

    def test_get_error_message(self) -> None:
        self.inputFilter.add("field", required=True)
        self.inputFilter.isValid()

        self.assertEqual(
            "Field 'field' is required.", self.inputFilter.getErrorMessage()
        )

    def test_get_input(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.setData({"field": "value"})

        self.assertEqual(
            self.inputFilter.getInput("field"),
            FieldModel(required=False, default=None),
        )

    def test_get_inputs(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")
        self.inputFilter.setData({"field1": "value1", "field2": "value2"})

        self.assertEqual(
            self.inputFilter.getInputs(),
            {
                "field1": FieldModel(required=False, default=None),
                "field2": FieldModel(required=False, default=None),
            },
        )

    def test_get_raw_value(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.setUnfilteredData(
            {"field": "raw_value", "unknown_field": "raw_value2"}
        )

        self.assertEqual(self.inputFilter.getRawValue("field"), "raw_value")

    def test_get_raw_values(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")
        self.inputFilter.setUnfilteredData(
            {"field1": "raw1", "field2": "raw2", "unknown_field": "raw3"}
        )

        self.assertEqual(
            self.inputFilter.getRawValues(),
            {"field1": "raw1", "field2": "raw2"},
        )

    def test_get_unfiltered_data(self) -> None:
        self.inputFilter.add("field", filters=[ToIntegerFilter()])
        self.inputFilter.setData({"field": "raw", "unknown_field": "raw2"})

        self.assertEqual(
            self.inputFilter.getUnfilteredData(),
            {"field": "raw", "unknown_field": "raw2"},
        )

    def test_get_value(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.setData({"field": "value"})

        self.inputFilter.isValid()
        self.assertEqual(self.inputFilter.getValue("field"), "value")

    def test_get_values(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")
        self.inputFilter.setData(
            {"field1": "value1", "field2": "value2", "field3": "value3"}
        )

        self.inputFilter.isValid()
        self.assertEqual(
            self.inputFilter.getValues(),
            {"field1": "value1", "field2": "value2"},
        )

    def test_has(self) -> None:
        self.inputFilter.add("field")

        self.assertTrue(self.inputFilter.has("field"))
        self.assertFalse(self.inputFilter.has("unknown_field"))

    def test_has_unknown(self) -> None:
        self.inputFilter.add("field1")

        self.inputFilter.setData(
            {"field1": "value1", "unknown_field": "value2"}
        )
        self.assertTrue(self.inputFilter.hasUnknown())

        self.inputFilter.setData({})
        self.assertTrue(self.inputFilter.hasUnknown())

        self.inputFilter.remove("field1")
        self.assertFalse(self.inputFilter.hasUnknown())

    def test_is_valid(self) -> None:
        self.inputFilter.add("field", required=True)

        self.inputFilter.setData({"field": "value"})
        self.assertTrue(self.inputFilter.isValid())

        self.inputFilter.setData({})
        self.assertFalse(self.inputFilter.isValid())

    def test_merge(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.setData({"field1": "value1"})

        input_filter = InputFilter()
        input_filter.add("field2")
        self.inputFilter.merge(input_filter)

        self.inputFilter.isValid()
        self.assertEqual(
            self.inputFilter.getValues(), {"field1": "value1", "field2": None}
        )

    def test_remove(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.setData({"field": "value"})

        self.inputFilter.remove("field")
        self.assertFalse(self.inputFilter.has("field"))

    def test_replace(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.setData({"field": "value"})

        self.inputFilter.replace("field", filters=[ToUpperFilter()])
        updated_data = self.inputFilter.validateData({"field": "value"})
        self.assertEqual(updated_data["field"], "VALUE")

    def test_set_data(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.setData({"field": "value"})

        self.inputFilter.isValid()
        self.assertEqual(self.inputFilter.getValue("field"), "value")

    def test_set_unfiltered_data(self) -> None:
        self.inputFilter.add("field")
        self.inputFilter.setUnfilteredData({"field": "raw_value"})
        self.assertEqual(self.inputFilter.getRawValue("field"), "raw_value")

    def test_steps(self) -> None:
        """
        Test that custom steps works.
        """
        self.inputFilter.add(
            "name_upper",
            steps=[
                ToUpperFilter(),
                InArrayValidator(["MAURICE"]),
                ToLowerFilter(),
            ],
        )

        validated_data = self.inputFilter.validateData(
            {"name_upper": "Maurice"}
        )
        self.assertEqual(validated_data["name_upper"], "maurice")

        with self.assertRaises(ValidationError):
            validated_data = self.inputFilter.validateData(
                {"name_upper": "Alice"}
            )
            self.assertEqual(validated_data["name_upper"], "ALICE")

        self.inputFilter.add(
            "fallback",
            fallback="fallback",
            steps=[
                ToUpperFilter(),
                InArrayValidator(["FALLBACK"]),
                ToLowerFilter(),
            ],
        )

        validated_data = self.inputFilter.validateData(
            {"fallback": "fallback"}
        )
        self.assertEqual(validated_data["fallback"], "fallback")

        self.inputFilter.add(
            "default",
            default="default",
            steps=[
                ToUpperFilter(),
                InArrayValidator(["DEFAULT"]),
                ToLowerFilter(),
            ],
        )

        validated_data = self.inputFilter.validateData({})
        self.assertEqual(validated_data["default"], "default")

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

        validated_data = self.inputFilter.validateData({})
        self.assertEqual(validated_data["fallback_with_default"], "default")

        validated_data = self.inputFilter.validateData(
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
            self.inputFilter.validateData({})

    @patch("requests.request")
    def test_external_api(self, mock_request: Mock) -> None:
        """
        Test that external API calls work.
        """
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
        validated_data = self.inputFilter.validateData({})

        self.assertEqual(validated_data["is_valid"], True)
        expected_url = "https://api.example.com/validate_user/test_user"
        mock_request.assert_called_with(
            headers={}, method="GET", url=expected_url, params={}
        )

        # API returns invalid result
        mock_response.status_code = 500
        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"name": "invalid_user"})

    @patch("requests.request")
    def test_external_api_params(self, mock_request: Mock) -> None:
        """
        Test that external API calls work.
        """

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

        validated_data = self.inputFilter.validateData(
            {"name": "test_user", "hash": "1234"}
        )

        self.assertEqual(validated_data["is_valid"], True)
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
            self.inputFilter.validateData(
                {"name": "invalid_user", "hash": "1234"}
            )

        mock_response.json.return_value = {}
        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
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

        validated_data = self.inputFilter.validateData(
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

        validated_data = self.inputFilter.validateData({})
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

        validated_data = self.inputFilter.validateData(
            {"username_with_fallback": None}
        )
        self.assertEqual(
            validated_data["username_with_fallback"], "fallback_user"
        )

    @patch("requests.request")
    def test_external_invalid_api_response(self, mock_request: Mock) -> None:
        """
        Test that a non-JSON API response raises a ValidationError.
        """
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
            self.inputFilter.validateData({})

    @patch("requests.request")
    def test_external_api_response_with_no_data_key(
        self, mock_request: Mock
    ) -> None:
        """
        Test that an API response with no data key raises a ValidationError.
        """
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
            self.inputFilter.validateData({})

    def test_multiple_validators(self) -> None:
        """
        Test that multiple validators are applied correctly.
        """
        self.inputFilter.add(
            "username",
            required=True,
            validators=[
                RegexValidator(r"^[a-zA-Z0-9_]+$"),
                LengthValidator(min_length=3, max_length=15),
            ],
        )

        validated_data = self.inputFilter.validateData(
            {"username": "valid_user"}
        )
        self.assertEqual(validated_data["username"], "valid_user")

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"username": "no"})

    def test_conditions(self) -> None:
        """
        Test that conditions are checked correctly.
        """

        class MockCondition(BaseCondition):
            def check(self, data: dict) -> bool:
                return data.get("age") > 18

        self.inputFilter.add("age", required=True)
        self.inputFilter.addCondition(MockCondition())

        validated_data = self.inputFilter.validateData({"age": 20})
        self.assertEqual(validated_data["age"], 20)

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"age": 17})

    def test_global_filter_applied_to_all_fields(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")

        self.inputFilter.addGlobalFilter(ToUpperFilter())

        validated_data = self.inputFilter.validateData(
            {"field1": "test", "field2": "example"}
        )

        self.assertEqual(validated_data["field1"], "TEST")
        self.assertEqual(validated_data["field2"], "EXAMPLE")

    def test_global_filter_with_no_fields(self) -> None:
        self.inputFilter.addGlobalFilter(ToUpperFilter())

        validated_data = self.inputFilter.validateData({})
        self.assertEqual(validated_data, {})

    def test_global_validator_applied_to_all_fields(self) -> None:
        self.inputFilter.add("field1")
        self.inputFilter.add("field2")
        self.inputFilter.addGlobalValidator(IsStringValidator())

        with self.assertRaises(ValidationError):
            self.inputFilter.validateData({"field1": 345, "field2": "example"})

        validated_data = self.inputFilter.validateData(
            {"field1": "test", "field2": "example"}
        )

        self.assertEqual(validated_data["field1"], "test")
        self.assertEqual(validated_data["field2"], "example")

    def test_global_validator_with_no_fields(self) -> None:
        self.inputFilter.addGlobalValidator(IsIntegerValidator())

        validated_data = self.inputFilter.validateData({})
        self.assertEqual(validated_data, {})

    def test_copy(self) -> None:
        """
        Test that InputFilter.copy() creates a deep copy
        of the InputFilter instance.
        """
        self.inputFilter.add("username")

        self.inputFilter.add(
            "escapedUsername", copy="username", filters=[SlugifyFilter()]
        )

        validated_data = self.inputFilter.validateData(
            {"username": "test user"}
        )
        self.assertEqual(validated_data["escapedUsername"], "test-user")

    def test_final_methods(self) -> None:
        def test_final_methods(self) -> None:
            final_methods = [
                "add",
                "addCondition",
                "addGlobalFilter",
                "addGlobalValidator",
                "count",
                "getErrorMessage",
                "getInput",
                "getInputs",
                "getRawValue",
                "getRawValues",
                "getUnfilteredData",
                "getValue",
                "getValues",
                "has",
                "hasUnknown",
                "isValid",
                "merge",
                "remove",
                "replace",
                "setData",
                "setUnfilteredData",
                "validateData",
            ]

            for method in final_methods:
                with self.assertRaises(TypeError), self.subTest(method=method):

                    class SubInputFilter(InputFilter):
                        def __getattr__(self, name):
                            if name == method:

                                def dummy_method(*args, **kwargs):
                                    pass

                                return dummy_method
                            return super().__getattr__(name)


if __name__ == "__main__":
    unittest.main()
