from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class NotValidator(BaseValidator):
    """
    Inverts the result of another validator. The validation passes if the inner
    validator fails, and vice versa.

    **Parameters:**

    - **validator** (*BaseValidator*): The validator whose outcome is to be
      inverted.
    - **error_message** (*Optional[str]*): Custom error message if the
      inverted validation does not behave as expected.

    **Expected Behavior:**

    Executes the inner validator on the input. If the inner validator does
    not raise a ``ValidationError``, then the NotValidator raises one
    instead.

    **Example Usage:**

    .. code-block:: python

        class NotIntegerInputFilter(InputFilter):
            value: Any = field(validators=[
                NotValidator(validator=IsIntegerValidator())
            ])
    """

    __slots__ = ("error_message", "validator")

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
