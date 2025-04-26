from __future__ import annotations

import json
from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class CustomJsonValidator(BaseValidator):
    """
    CustomJsonValidator validates JSON data against specified requirements.

    The CustomJsonValidator class is designed to validate JSON input in
    string or dictionary format. It ensures the input adheres to specified
    required fields and schema constraints, and optionally raises tailored
    error messages on validation failures.
    """

    __slots__ = ("required_fields", "schema", "error_message")

    def __init__(
        self,
        required_fields: list = None,
        schema: dict = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.required_fields = required_fields or []
        self.schema = schema or {}
        self.error_message = error_message

    def validate(self, value: Any) -> bool:
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise ValidationError("Invalid json format.")

        if not isinstance(value, dict):
            raise ValidationError("The input should be a dictionary.")

        for field in self.required_fields:
            if field not in value:
                raise ValidationError(f"Missing required field '{field}'.")

        if not self.schema:
            return True

        for field, expected_type in self.schema.items():
            if field in value and not isinstance(value[field], expected_type):
                raise ValidationError(
                    self.error_message
                    or f"Field '{field}' has to be of type "
                    f"'{expected_type.__name__}'."
                )

        return True
