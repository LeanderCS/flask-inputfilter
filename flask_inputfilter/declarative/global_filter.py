from __future__ import annotations

from typing import TYPE_CHECKING

from ._utils import append_to_class_list

if TYPE_CHECKING:
    from flask_inputfilter.models import BaseFilter


def global_filter(*filter_instances: BaseFilter) -> None:
    """
    Register one or more global filters for declarative definition.

    This function registers global filters directly in the class definition
    without requiring variable assignment or __init__ methods.

    **Parameters:**

    - **filter_instances** (*BaseFilter*): One or more filter instances to
      register globally.

    **Examples:**

    .. code-block:: python

        class MyInputFilter(InputFilter):
            name: str = field(required=True, validators=[IsStringValidator()])
            email: str = field(required=True)

            # Single global filter
            global_filter(StringTrimFilter())

            # Multiple global filters at once
            global_filter(
                StringTrimFilter(),
                ToLowerFilter(),
                RemoveWhitespaceFilter()
            )
    """
    for filter_instance in filter_instances:
        append_to_class_list("_global_filters", filter_instance)
