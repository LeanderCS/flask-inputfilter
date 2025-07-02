from flask_inputfilter import InputFilter
from flask_inputfilter.validators import IsIntegerValidator, IsStringValidator


class UserInputFilter(InputFilter):
    def __init__(self):
        super().__init__()

        self.add("name", required=True, validators=[IsStringValidator()])

        self.add("age", required=True, validators=[IsIntegerValidator()])

        self.add("email", required=True, validators=[IsStringValidator()])
