from __future__ import annotations

from typing import Any, List, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class OrValidator(BaseValidator):
    """
    Validator that succeeds if one of the given validators succeeds.
    """

    __slots__ = ("validators", "error_message")

    def __init__(
        self,
        validators: List[BaseValidator],
        error_message: Optional[str] = None,
    ) -> None:
        self.validators = validators
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        for validator in self.validators:
            try:
                validator.validate(value)
                return
            except ValidationError:
                pass

        raise ValidationError(self.error_message or "No validator succeeded.")
