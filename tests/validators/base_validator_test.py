import unittest
from typing import Any, Optional

from flask_inputfilter import InputFilter
from flask_inputfilter.exceptions import ValidationError


class BaseValidatorTest(unittest.TestCase):
    """
    Base class for all validator tests.

    Provides common setup logic and helper methods that can be used
    in all validator test classes.
    """

    def setUp(self) -> None:
        """Initialize an InputFilter for each test."""
        self.input_filter = InputFilter()

    def assertValidationError(
        self,
        field_name: str,
        invalid_value: Any,
        expected_message: Optional[str] = None,
    ) -> None:
        """
        Helper method to check if an invalid value raises a ValidationError.

        Args:
            field_name (str): Name of the field to validate
            invalid_value (Any): The invalid value that should trigger a
                ValidationError
            expected_message (Optional[str]): Optional expected error message
        """
        with self.assertRaises(ValidationError) as context:
            self.input_filter.validate_data({field_name: invalid_value})

        errors = context.exception.args[0]

        self.assertIn(field_name, errors, expected_message)

        if expected_message:
            self.assertEqual(errors[field_name], expected_message)
