from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field
from flask_inputfilter.validators import RegexValidator, IsDateTimeValidator, IsStringValidator, RangeValidator, LengthValidator, IsIntegerValidator, IsFloatValidator, IsBooleanValidator, InArrayValidator, IsArrayValidator, ArrayLengthValidator
from flask_inputfilter.enums import RegexEnum


class TestInputFilter(InputFilter):
    """
    Complete Test Schema.

    Comprehensive test schema covering all supported JSON Schema types for CLI testing.
    """

    string_field = field(required=True, validators=[IsStringValidator(), LengthValidator(min_length=1, max_length=100)])

    email_field = field(required=True, validators=[RegexValidator(RegexEnum.EMAIL.value, 'Please enter a valid email address')])

    uri_field = field(required=False, validators=[RegexValidator(RegexEnum.URL.value, 'Invalid URL format.')])

    date_field = field(required=False, validators=[IsDateTimeValidator()])

    pattern_field = field(required=False, validators=[RegexValidator(r'^[A-Z]{2,3}-\d{4}$', 'Format must be like ABC-1234')])

    integer_field = field(required=True, validators=[IsIntegerValidator('Value must be between 0 and 1000'), RangeValidator(min_value=0, max_value=1000, 'Value must be between 0 and 1000')])

    number_field = field(required=False, validators=[IsFloatValidator(), RangeValidator(min_value=0.0, max_value=100.0)])

    boolean_field = field(required=True, validators=[IsBooleanValidator()])

    enum_field = field(required=True, validators=[InArrayValidator(["active", "inactive", "pending"])])

    array_strings = field(required=False, validators=[IsArrayValidator()])

    array_integers = field(required=False, validators=[IsArrayValidator(), ArrayLengthValidator(min_length=1, max_length=10)])

    nested_object = field(required=True, validators=[])

    optional_string = field(required=False, validators=[IsStringValidator()])

    default_value_field = field(required=False, default="default_value", validators=[IsStringValidator()])

    nullable_field = field(required=False, validators=[IsStringValidator()])
