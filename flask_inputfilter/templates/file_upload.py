from __future__ import annotations

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.filters import StringTrimFilter
from flask_inputfilter.validators import (
    IsBase64ImageValidator,
    IsStringValidator,
    LengthValidator,
    RegexValidator,
)


class FileUploadInputFilter(InputFilter):
    file = field(required=True, validators=[IsBase64ImageValidator()])

    filename = field(
        required=True,
        filters=[StringTrimFilter()],
        validators=[
            IsStringValidator(),
            LengthValidator(min_length=1, max_length=255),
            RegexValidator(r"^[a-zA-Z0-9._-]+$"),
        ],
    )

    description = field(
        required=False,
        default="",
        filters=[StringTrimFilter()],
        validators=[IsStringValidator(), LengthValidator(max_length=500)],
    )
