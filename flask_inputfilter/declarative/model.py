from __future__ import annotations

from ._utils import register_class_attribute


def model(model_class: type) -> None:
    """
    Set the model class for declarative definition.

    This function sets the model class directly in the class definition
    without requiring variable assignment or __init__ methods.

    **Parameters:**

    - **model_class** (*type*): The model class to use for serialization.

    **Example:**

    .. code-block:: python

        from dataclasses import dataclass

        @dataclass
        class UserModel:
            name: str
            email: str

        class UserInputFilter(InputFilter):
            name: str = field(required=True, validators=[IsStringValidator()])
            email: str = field(required=True, validators=[EmailValidator()])

            model(UserModel)
    """
    register_class_attribute("_model", model_class)
