from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class OrValidator(BaseValidator):
    """
    Validates that the input passes at least one of the provided validators.
    This composite validator performs a logical OR over its constituent
    validators.

    **Parameters:**

    - **validators** (*list[BaseValidator]*): A list of validators
      to apply.
    - **error_message** (*Optional[str]*): Custom error message if none
      of the validators pass.

    **Expected Behavior:**

    The validator applies each validator in the provided list to the input
    value. If any one validator passes without raising a ``ValidationError``,
    the validation is considered successful. If all validators fail, it
    raises a ``ValidationError`` with the provided error message or a default
    message.

    **Example Usage:**

    .. code-block:: python

        class OrInputFilter(InputFilter):
            value: str = field(
                validators=[
                    OrValidator([
                        IsIntegerValidator(),
                        IsStringValidator()
                    ])
                ]
            )
    """

    __slots__ = ("error_message", "validators")

    def __init__(
        self,
        validators: list[BaseValidator],
        error_message: Optional[str] = None,
    ) -> None:
        self.validators = validators
        self.error_message = error_message or "No validator succeeded."

    def validate(self, value: Any) -> None:
        for validator in self.validators:
            try:
                validator.validate(value)
                return
            except ValidationError:
                pass

        raise ValidationError(self.error_message)
