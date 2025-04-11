from typing import Dict

from typing_extensions import final

from flask_inputfilter.Mixin import BaseMixin


class ErrorHandlingMixin(BaseMixin):
    @final
    def getErrorMessage(self, field_name: str) -> str:
        """
        Retrieves and returns a predefined error message.

        This method is intended to provide a consistent error message
        to be used across the application when an error occurs. The
        message is predefined and does not accept any parameters.
        The exact content of the error message may vary based on
        specific implementation, but it is designed to convey meaningful
        information about the nature of an error.

        Returns:
            str: A string representing the predefined error message.
        """
        return self._errors.get(field_name)

    @final
    def getErrorMessages(self) -> Dict[str, str]:
        """
        Retrieves all error messages associated with the fields in the
        input filter.

        This method aggregates and returns a dictionary of error messages
        where the keys represent field names, and the values are their
        respective error messages.

        Returns:
            Dict[str, str]: A dictionary containing field names as keys and
                            their corresponding error messages as values.
        """
        return self._errors
