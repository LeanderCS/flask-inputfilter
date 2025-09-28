from dataclasses import dataclass

from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field, model
from flask_inputfilter.validators import IsIntegerValidator, IsStringValidator


@dataclass
class User:
    name: str
    age: int
    email: str


class UserInputFilter(InputFilter):
    model(User)

    name: str = field(required=True, validators=[IsStringValidator()])

    age: int = field(required=True, validators=[IsIntegerValidator()])

    email: str = field(required=True, validators=[IsStringValidator()])
