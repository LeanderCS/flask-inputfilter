from __future__ import annotations

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.filters import (
    StringTrimFilter,
    ToIntegerFilter,
    ToLowerFilter,
)
from flask_inputfilter.validators import (
    InArrayValidator,
    IsIntegerValidator,
    IsStringValidator,
    RangeValidator,
)


class PaginationInputFilter(InputFilter):
    page = field(
        required=False,
        default=1,
        filters=[ToIntegerFilter()],
        validators=[IsIntegerValidator(), RangeValidator(min_value=1)],
    )

    per_page = field(
        required=False,
        default=20,
        filters=[ToIntegerFilter()],
        validators=[
            IsIntegerValidator(),
            RangeValidator(min_value=1, max_value=100),
        ],
    )

    sort_by = field(
        required=False,
        filters=[StringTrimFilter()],
        validators=[IsStringValidator()],
    )

    order = field(
        required=False,
        default="asc",
        filters=[StringTrimFilter(), ToLowerFilter()],
        validators=[IsStringValidator(), InArrayValidator(["asc", "desc"])],
    )
