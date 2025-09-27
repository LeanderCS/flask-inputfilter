from __future__ import annotations

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.filters import (
    StringTrimFilter,
    ToBooleanFilter,
    ToLowerFilter,
)
from flask_inputfilter.validators import (
    IsBooleanValidator,
    IsStringValidator,
    LengthValidator,
    RegexValidator,
)


class AuthenticationInputFilter(InputFilter):
    email = field(
        required=True,
        filters=[StringTrimFilter(), ToLowerFilter()],
        validators=[
            IsStringValidator(),
            RegexValidator(RegexEnum.EMAIL.value),
        ],
    )

    password = field(
        required=True,
        validators=[IsStringValidator(), LengthValidator(min_length=8)],
    )

    remember_me = field(
        required=False,
        default=False,
        filters=[ToBooleanFilter()],
        validators=[IsBooleanValidator()],
    )
