from typing import Any, List, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class OrValidator(BaseValidator):
    """
    Validator that succeeds if one of the given validators succeeds.
    """

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
