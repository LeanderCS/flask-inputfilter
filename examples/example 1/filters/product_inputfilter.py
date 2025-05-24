from enum import Enum

from flask_inputfilter import InputFilter
from flask_inputfilter.filters import ToFloatFilter
from flask_inputfilter.validators import IsStringValidator, IsIntegerValidator, InEnumValidator, IsArrayValidator, \
    ArrayElementValidator, IsFloatValidator


class Tags(Enum):
    ELECTRONICS = 'electronics'
    FASHION = 'fashion'
    HOME = 'home'
    BEAUTY = 'beauty'
    SPORTS = 'sports'
    TOYS = 'toys'

class ProductInputFilter(InputFilter):
    def __init__(self):
        super().__init__()

        self.add(
            'name',
            required=True,
            validators=[
                IsStringValidator(),
            ]
        )

        self.add(
            'price',
            required=True,
            filters=[
                ToFloatFilter()
            ],
            validators=[
                IsFloatValidator(),
            ]
        )

        self.add(
            'tags',
            required=False,
            validators=[
                IsArrayValidator(),
                ArrayElementValidator(
                    InEnumValidator(
                        Tags
                    )
                )
            ]
        )
