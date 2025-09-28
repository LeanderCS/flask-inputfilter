from __future__ import annotations

from typing import TYPE_CHECKING

from ._utils import append_to_class_list

if TYPE_CHECKING:
    from flask_inputfilter.models import BaseCondition


def condition(*condition_instances: BaseCondition) -> None:
    """
    Register one or more conditions for declarative condition definition.

    This function registers conditions directly in the class definition
    without requiring variable assignment or __init__ methods.

    **Parameters:**

    - **condition_instances** (*BaseCondition*): One or more condition
      instances to register.

    **Examples:**

    .. code-block:: python

        class RegistrationInputFilter(InputFilter):
            password: str = field(
                required=True, validators=[IsStringValidator()]
            )
            password_confirmation: str = field(
                required=True, validators=[IsStringValidator()]
            )

            # Single condition
            condition(EqualCondition('password', 'password_confirmation'))

            # Multiple conditions at once
            condition(
                RequiredCondition('password'),
                LengthCondition('password', min_length=8)
            )
    """
    for condition_instance in condition_instances:
        append_to_class_list("_conditions", condition_instance)
