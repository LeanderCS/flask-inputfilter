from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import field


class TestInputFilter(InputFilter):
    """
    Complete Test Schema.

    Comprehensive test schema covering all supported JSON Schema types for CLI testing.
    """

    string_field: str = field(required=True, min_length=1, max_length=100)
    email_field: str = field(required=True, format="email")
    uri_field: str = field(required=False, format="uri")
    date_field: str = field(required=False, format="date-time")
    pattern_field: str = field(required=False, pattern="^[A-Z]{2,3}-\\d{4}$")
    integer_field: int = field(required=True, minimum=0, maximum=1000)
    number_field: float = field(required=False, minimum=0.0, maximum=100.0)
    boolean_field: bool = field(required=True)
    enum_field: str = field(required=True, choices=["active", "inactive", "pending"])
    array_strings: list = field(required=False)
    array_integers: list = field(required=False, min_items=1, max_items=10)
    nested_object: dict = field(required=True)
    optional_string: str = field(required=False)
    default_value_field: str = field(required=False, default="default_value")
    nullable_field: str = field(required=False, allow_null=True)
