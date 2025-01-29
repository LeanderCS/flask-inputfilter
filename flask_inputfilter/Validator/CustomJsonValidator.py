import json
from typing import Any, Optional

from ..Exception import ValidationError
from .BaseValidator import BaseValidator


class CustomJsonValidator(BaseValidator):
    """
    Validiert den übergebenen Wert. Überprüft, ob der Wert ein gültiges
    JSON ist und ob alle erforderlichen Felder vorhanden sind.
    """

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

        if self.schema:
            for field, expected_type in self.schema.items():
                if field in value:
                    if not isinstance(value[field], expected_type):
                        raise ValidationError(
                            self.error_message
                            or f"Field '{field}' has to be of type "
                            f"'{expected_type.__name__}'."
                        )

        return True
