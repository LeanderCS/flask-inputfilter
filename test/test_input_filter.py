import unittest
from unittest.mock import Mock, patch

from flask_inputfilter import InputFilter
from flask_inputfilter.Condition import BaseCondition
from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Filter import ToUpperFilter
from flask_inputfilter.Model import ExternalApiConfig
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

        # Default case triggert
        validated_data = self.inputFilter.validateData({})

        self.assertEqual(validated_data["available"], True)

        # Override default case
        validated_data = self.inputFilter.validateData({"available": False})

        self.assertEqual(validated_data["available"], False)

    def test_fallback(self) -> None:
        """
        Test that fallback field works.
        """

        self.inputFilter.add("available", required=True, fallback=True)
        self.inputFilter.add(
            "color",
            fallback="red",
            validators=[InArrayValidator(["red", "green", "blue"])],
        )

        # Fallback case triggert
        validated_data = self.inputFilter.validateData({"color": "yellow"})

        self.assertEqual(validated_data["available"], True)
        self.assertEqual(validated_data["color"], "red")

        # Override fallback case
        validated_data = self.inputFilter.validateData(
            {"available": False, "color": "green"}
        )

        self.assertEqual(validated_data["available"], False)
        self.assertEqual(validated_data["color"], "green")

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

        # Add fields where the external API receives its values
        self.inputFilter.add("name")

        self.inputFilter.add("hash")

        # Add a field with external API configuration
        self.inputFilter.add(
            "is_valid",
            required=True,
            external_api=ExternalApiConfig(
                url="https://api.example.com/validate_user/{{name}}",
                method="GET",
                params={"hash": "{{hash}}"},
                data_key="is_valid",
                headers={"custom_header": "value"},
                api_key="1234",
            ),
        )

        # API returns valid result
        validated_data = self.inputFilter.validateData(
            {"name": "test_user", "hash": "1234"}
        )

        self.assertEqual(validated_data["is_valid"], True)
        expected_url = "https://api.example.com/validate_user/test_user"
        mock_request.assert_called_with(
            headers={"Authorization": "Bearer 1234", "custom_header": "value"},
            method="GET",
            url=expected_url,
            params={"hash": "1234"},
        )

        # API returns invalid status code
        mock_response.status_code = 500
        mock_response.json.return_value = {"is_valid": False}
        with self.assertRaises(ValidationError):
            self.inputFilter.validateData(
                {"name": "invalid_user", "hash": "1234"}
            )

        # API returns invalid result
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

        # API call with fallback
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

    @patch("requests.request")
    def test_invalid_api_response(self, mock_request: Mock) -> None:
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


if __name__ == "__main__":
    unittest.main()
