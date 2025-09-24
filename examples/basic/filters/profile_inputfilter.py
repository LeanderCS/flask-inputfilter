from dataclasses import dataclass

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.validators import (
    IsDataclassValidator,
    IsStringValidator,
)


@dataclass
class User:
    name: str
    age: int
    email: str


@dataclass
class Address:
    street: str
    city: str
    zip_code: int


class ProfileInputFilter(InputFilter):
    user: User = field(
        required=True, validators=[IsDataclassValidator(dataclass_type=User)]
    )

    address: Address = field(
        required=True,
        validators=[IsDataclassValidator(dataclass_type=Address)],
    )

    phone: str = field(required=False, validators=[IsStringValidator()])
