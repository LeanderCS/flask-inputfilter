from __future__ import annotations

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.filters import StringTrimFilter, ToLowerFilter
from flask_inputfilter.validators import (
    IsStringValidator,
    LengthValidator,
    RegexValidator,
)


class ContactFormInputFilter(InputFilter):
    name = field(
        required=True,
        filters=[StringTrimFilter()],
        validators=[
            IsStringValidator(),
            LengthValidator(min_length=2, max_length=100),
        ],
    )

    email = field(
        required=True,
        filters=[StringTrimFilter(), ToLowerFilter()],
        validators=[
            IsStringValidator(),
            RegexValidator(RegexEnum.EMAIL.value),
        ],
    )

    subject = field(
        required=True,
        filters=[StringTrimFilter()],
        validators=[
            IsStringValidator(),
            LengthValidator(min_length=5, max_length=200),
        ],
    )

    message = field(
        required=True,
        filters=[StringTrimFilter()],
        validators=[
            IsStringValidator(),
            LengthValidator(min_length=10, max_length=1000),
        ],
    )
