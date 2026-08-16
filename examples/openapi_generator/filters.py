from typing import Any

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.filters import (
    ToBooleanFilter,
    ToDateTimeFilter,
    ToFloatFilter,
    ToIntegerFilter,
)
from flask_inputfilter.validators import (
    ArrayElementValidator,
    ArrayLengthValidator,
    InArrayValidator,
    IsArrayValidator,
    IsBooleanValidator,
    IsDateTimeValidator,
    IsFloatValidator,
    IsIntegerValidator,
    IsStringValidator,
    LengthValidator,
    RangeValidator,
    RegexValidator,
)


class AddressInputFilter(InputFilter):
    street: str = field(
        required=True,
        validators=[
            IsStringValidator(),
            LengthValidator(min_length=1, max_length=100),
        ],
    )

    city: str = field(
        required=True,
        validators=[
            IsStringValidator(),
            LengthValidator(min_length=1, max_length=50),
        ],
    )

    zipcode: str = field(
        validators=[
            IsStringValidator(),
            RegexValidator(pattern="^\\d{5}(-\\d{4})?$"),
        ],
    )

    country: str = field(
        default="DE",
        validators=[IsStringValidator()],
    )


class UserInputFilter(InputFilter):
    name: str = field(
        required=True,
        validators=[
            IsStringValidator(),
            LengthValidator(min_length=2, max_length=50),
        ],
    )

    email: str = field(
        required=True,
        validators=[
            IsStringValidator(),
            RegexValidator(
                pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
            ),
        ],
    )

    age: int = field(
        filters=[ToIntegerFilter()],
        validators=[
            IsIntegerValidator(),
            RangeValidator(min_value=18, max_value=120),
        ],
    )

    active: bool = field(
        default=True,
        filters=[ToBooleanFilter()],
        validators=[IsBooleanValidator()],
    )

    tags: Any = field(
        validators=[
            IsArrayValidator(),
            ArrayElementValidator(element_filter=[IsStringValidator()]),
        ],
    )

    address: dict = field(
        input_filter=AddressInputFilter,
    )


class CategoryInputFilter(InputFilter):
    id: int = field(
        filters=[ToIntegerFilter()],
        validators=[IsIntegerValidator()],
    )

    name: str = field(
        validators=[IsStringValidator()],
    )


class ProductInputFilter(InputFilter):
    title: str = field(
        required=True,
        validators=[
            IsStringValidator(),
            LengthValidator(min_length=3, max_length=200),
        ],
    )

    description: str = field(
        validators=[
            IsStringValidator(),
            LengthValidator(max_length=1000),
        ],
    )

    price: float = field(
        required=True,
        filters=[ToFloatFilter()],
        validators=[
            IsFloatValidator(),
            RangeValidator(min_value=0),
        ],
    )

    status: str = field(
        required=True,
        validators=[
            IsStringValidator(),
            InArrayValidator(
                haystack=[
                    "available",
                    "unavailable",
                    "discontinued",
                ]
            ),
        ],
    )

    category: dict = field(
        input_filter=CategoryInputFilter,
    )

    images: Any = field(
        validators=[
            IsArrayValidator(),
            ArrayElementValidator(element_filter=[IsStringValidator()]),
            ArrayLengthValidator(min_length=1, max_length=10),
        ],
    )


class ItemsitemInputFilter(InputFilter):
    product_id: int = field(
        filters=[ToIntegerFilter()],
        validators=[IsIntegerValidator()],
    )

    quantity: int = field(
        filters=[ToIntegerFilter()],
        validators=[
            IsIntegerValidator(),
            RangeValidator(min_value=1),
        ],
    )

    price: float = field(
        filters=[ToFloatFilter()],
        validators=[
            IsFloatValidator(),
            RangeValidator(min_value=0),
        ],
    )


class OrderInputFilter(InputFilter):
    user_id: int = field(
        required=True,
        filters=[ToIntegerFilter()],
        validators=[IsIntegerValidator()],
    )

    user: dict = field(
        input_filter=UserInputFilter,
    )

    items: list[dict] = field(
        required=True,
        validators=[
            IsArrayValidator(),
            ArrayLengthValidator(min_length=1),
        ],
    )

    order_date: Any = field(
        filters=[ToDateTimeFilter()],
        validators=[IsDateTimeValidator()],
    )

    status: str = field(
        default="pending",
        validators=[
            IsStringValidator(),
            InArrayValidator(
                haystack=[
                    "pending",
                    "processing",
                    "shipped",
                    "delivered",
                    "cancelled",
                ]
            ),
        ],
    )
