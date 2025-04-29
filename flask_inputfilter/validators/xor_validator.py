from __future__ import annotations

from typing import Any, List, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import BaseValidator


class XorValidator(BaseValidator):
    """
    Validates that the input passes exactly one of the provided validators.
    This composite validator ensures that the input does not pass zero or more
    than one of the specified validators.

    **Parameters:**

    - **validators** (*List[BaseValidator]*): A list of validators,
        of which exactly one must pass.
    - **error_message** (*Optional[str]*): Custom error message if the
        input does not satisfy exactly one validator.

    **Expected Behavior:**

    The validator applies each validator in the provided list to the input
    value and counts the number of validators that pass without raising a
    ``ValidationError``. If exactly one validator passes, the input is
    considered valid; otherwise, a ``ValidationError`` is raised with the
    provided or default error message.

    **Example Usage:**

    .. code-block:: python

        class XorInputFilter(InputFilter):
            def __init__(self):
                super().__init__()

                self.add('value', validators=[
                    XorValidator([IsIntegerValidator(), IsStringValidator()])
                ])
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
        success_count = 0
        for validator in self.validators:
            try:
                validator.validate(value)
                success_count += 1
            except ValidationError:
                pass

        if success_count != 1:
            raise ValidationError(
                self.error_message or "No or multiple validators succeeded."
            )
