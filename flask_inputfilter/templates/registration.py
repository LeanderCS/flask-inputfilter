from __future__ import annotations

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import EqualCondition
from flask_inputfilter.declarative import condition, field
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


class RegistrationInputFilter(InputFilter):
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
        validators=[
            IsStringValidator(),
            LengthValidator(min_length=8, max_length=128),
        ],
    )

    password_confirmation = field(
        required=True, validators=[IsStringValidator()]
    )

    terms_accepted = field(
        required=True,
        filters=[ToBooleanFilter()],
        validators=[IsBooleanValidator()],
    )

    condition(EqualCondition("password", "password_confirmation"))
