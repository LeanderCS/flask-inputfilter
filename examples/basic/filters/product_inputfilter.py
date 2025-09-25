from enum import Enum

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.filters import ToFloatFilter
from flask_inputfilter.validators import (
    ArrayElementValidator,
    InEnumValidator,
    IsArrayValidator,
    IsFloatValidator,
    IsStringValidator,
)


class Tags(Enum):
    ELECTRONICS = "electronics"
    FASHION = "fashion"
    HOME = "home"
    BEAUTY = "beauty"
    SPORTS = "sports"
    TOYS = "toys"


class ProductInputFilter(InputFilter):
    name: str = field(required=True, validators=[IsStringValidator()])

    price: float = field(
        required=True,
        filters=[ToFloatFilter()],
        validators=[IsFloatValidator()],
    )

    tags: list = field(
        required=False,
        validators=[
            IsArrayValidator(),
            ArrayElementValidator(InEnumValidator(Tags)),
        ],
    )
