import unittest
from unittest.mock import Mock, patch

from src.flask_inputfilter.Exception import ValidationError
from src.flask_inputfilter.InputFilter import InputFilter
from src.flask_inputfilter.Validator import InArrayValidator


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

        self.inputFilter.add("available", required=False, default=True)

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
            required=False,
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
        self.inputFilter.add("name", required=False, default="test_user")

        # Add a field with external API configuration
        self.inputFilter.add(
            "is_valid",
            external_api={
                "url": "https://api.example.com/validate_user/{{name}}",
                "method": "GET",
                "data_key": "is_valid",
            },
        )

        # API returns valid result
        validated_data = self.inputFilter.validateData({})

        self.assertEqual(validated_data["is_valid"], True)
        expected_url = "https://api.example.com/validate_user/test_user"
        mock_request.assert_called_with(
            method="GET",
            url=expected_url,
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
        self.inputFilter.add("name", required=False)

        self.inputFilter.add("hash", required=False)

        # Add a field with external API configuration
        self.inputFilter.add(
            "is_valid",
            required=True,
            external_api={
                "url": "https://api.example.com/validate_user/{{name}}",
                "method": "GET",
                "params": {"hash": "{{hash}}"},
                "data_key": "is_valid",
            },
        )

        # API returns valid result
        validated_data = self.inputFilter.validateData(
            {"name": "test_user", "hash": "1234"}
        )

        self.assertEqual(validated_data["is_valid"], True)
        expected_url = "https://api.example.com/validate_user/test_user"
        mock_request.assert_called_with(
            method="GET", url=expected_url, params={"hash": "1234"}
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
            external_api={
                "url": "https://api.example.com/validate_user",
                "method": "GET",
                "params": {"user": "{{value}}"},
                "data_key": "name",
            },
        )

        validated_data = self.inputFilter.validateData(
            {"username_with_fallback": None}
        )
        self.assertEqual(
            validated_data["username_with_fallback"], "fallback_user"
        )
