Create own components
=====================

Depending on what you want to build your own version from, there are different
parameters and return values required to work properly.

- `Condition`_
- `Filter`_
- `Validator`_

Inside each ``__init__`` method you can add everything as you wish,
due it not being called in the validation process.
Its definition is optional.

Condition
---------

First off with conditions.

Their validation method is called ``check``.
It expects a dict from the type ``Dict[str, Any]`` whereas the key (``str``) of the
dictionary represents the name of a field and the value (``Any``) the corresponding value.
The dict represents the entirety of all fields present in the InputFilter it is called.

The return value of the method should be ``bool``, representing if the condition is ``true`` or ``false``.
- ``true``: The condition is met and the validation can proceed
- ``false``: The validation is **not** met and the validation raises a ``ValidationError``

Example implementation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from typing import Any

    from flask_inputfilter.conditions import BaseCondition


    class EqualCondition(BaseCondition):
        """
        Condition that checks if two fields are equal.
        """

        def __init__(self, first_field: str, second_field: str) -> None:
            self.first_field = first_field
            self.second_field = second_field

        def check(self, data: dict[str, Any]) -> bool:
            return data.get(self.first_field) == data.get(self.second_field)


Filter
------

The next type we look at is filters.

Their method called in the validation process is ``apply``.
It expects ``Any``, representing the value of the specific field, it is applied to.

The return value should have the type ``Any``, representing either the successfully filtered value or
the value from the input.
The filter should **not** raise any ``ValidationError``, even if the value is not in the expected format
to be filtered properly. Instead, it should just return the unfiltered value from the parameters.
It is not a filers job to check weather a value meets the wanted format or not, that's what ``validators`` are for.

Example implementation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from datetime import date, datetime
    from typing import Any

    from flask_inputfilter.filters import BaseFilter


    class ToDateTimeFilter(BaseFilter):
        """
        Filter that converts a value to a datetime object.
        Supports ISO 8601 formatted strings.
        """

        def apply(self, value: Any) -> datetime|Any:
            if isinstance(value, datetime):
                return value

            elif isinstance(value, date):
                return datetime.combine(value, datetime.min.time())

            elif isinstance(value, str):
                try:
                    return datetime.fromisoformat(value)

                except ValueError:
                    return value

            return value


Validator
---------

The last type are the validators.

This type is the most important one, as it is the one that raises ensures the value meets the wanted format.

Their method called in the validation process is ``validate``.
It expects ``Any``, representing the value of the specific field, it is applied to.

The return value should be ``None`` if the value meets the wanted format, and
it should raise a ``ValidationError`` if the validation fails.

Example implementation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from typing import Any, Optional

    from flask_inputfilter.exceptions import ValidationError
    from flask_inputfilter.validators import BaseValidator


    class InArrayValidator(BaseValidator):
        """
        Validator that checks if a value is in a given list of allowed values.
        """

        def __init__(
            self,
            haystack: list[Any],
            strict: bool = False,
            error_message: Optional[str] = None,
        ) -> None:
            self.haystack = haystack
            self.strict = strict
            self.error_message = error_message

        def validate(self, value: Any) -> None:
            try:
                if self.strict:
                    if value not in self.haystack or not any(
                        isinstance(value, type(item)) for item in self.haystack
                    ):
                        raise ValidationError

                else:
                    if value not in self.haystack:
                        raise ValidationError

            except ValidationError:
                raise ValidationError(
                    self.error_message
                    or f"Value '{value}' is not in the allowed "
                    f"values '{self.haystack}'."
                )
