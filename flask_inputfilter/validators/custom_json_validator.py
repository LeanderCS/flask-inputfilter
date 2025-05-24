from __future__ import annotations

import json
from typing import Any, List, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class CustomJsonValidator(BaseValidator):
    """
    Validates that the provided value is valid JSON. It also checks for the
    presence of required fields and optionally verifies field types against a
    provided schema.

    **Parameters:**

    - **required_fields** (*list*, default: []): Fields that must exist
        in the JSON.
    - **schema** (*dict*, default: {}): A dictionary specifying expected
        types for certain fields.
    - **error_message** (*Optional[str]*): Custom error message if validation
        fails.

    **Expected Behavior:**

    If the input is a string, it attempts to parse it as JSON. It then
    confirms that the result is a dictionary, contains all required
    fields, and that each field adheres to the defined type in the schema.

    **Example Usage:**

    .. code-block:: python

        class JsonInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('data', validators=[
                    CustomJsonValidator(
                        required_fields=['id', 'name'],
                        schema={'id': int, 'name': str}
                    )
                ])
    """

    __slots__ = ("required_fields", "schema", "error_message")

    def __init__(
        self,
        required_fields: List[str] = None,
        schema: dict = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.required_fields = required_fields or []
        self.schema = schema or {}
        self.error_message = error_message

    def validate(self, value: Any) -> None:
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
            return

        for field, expected_type in self.schema.items():
            if field in value and not isinstance(value[field], expected_type):
                raise ValidationError(
                    self.error_message
                    or f"Field '{field}' has to be of type "
                    f"'{expected_type.__name__}'."
                )
