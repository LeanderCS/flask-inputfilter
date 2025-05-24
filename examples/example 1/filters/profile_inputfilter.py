from dataclasses import dataclass

from flask_inputfilter import InputFilter
from flask_inputfilter.validators import IsStringValidator, IsDataclassValidator


@dataclass
class User:
    name: int
    age: int
    email: str


@dataclass
class Address:
    street: str
    city: str
    zip_code: int


class ProfileInputFilter(InputFilter):
    def __init__(self):
        super().__init__()

        self.add(
            'user',
             required=True,
             validators=[
                 IsDataclassValidator(
                    dataclass_type=User
                 )
             ]
         )

        self.add(
            'address',
             required=True,
             validators=[
                 IsDataclassValidator(
                    dataclass_type=Address
                 )
             ]
         )

        self.add(
            'phone',
             required=False,
             validators=[
                 IsStringValidator()
             ]
         )
