from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class NotValidator(BaseValidator):
    """
    Validator that inverts another validator.
    """

    __slots__ = ("validator", "error_message")

    def __init__(
        self,
        validator: BaseValidator,
        error_message: Optional[str] = None,
    ) -> None:
        self.validator = validator
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        try:
            self.validator.validate(value)
        except ValidationError:
            return

        raise ValidationError(
            self.error_message
            or f"Validation of '{value}' in "
            f"'{self.validator.__class__.__name__}' where "
            f"successful but should have failed."
        )
