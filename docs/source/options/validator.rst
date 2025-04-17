Validator
=========

``Validators`` are used to validate the data after filters have been applied. 
They ensure that the input data meets the required conditions before further processing.

Overview
--------

Validators can be added into the ``add`` method for a specific field or as a global validator for all fields in ``addGlobalValidator``.

The global validation will be executed before the specific field validation.

Example
-------

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsIntegerValidator, RangeValidator


    class UpdatePointsInputFilter(InputFilter):
        def __init__(self):

            self.add(
                'id',
                required=True
            )

            self.add(
                'points',
                required=True,
                validators=[RangeValidator(min_value=0, max_value=10)]
            )

            self.addGlobalValidator(IsIntegerValidator())

Available Validators
--------------------

The following validators are available:

- `ArrayElementValidator`_
- `ArrayLengthValidator`_
- `CustomJsonValidator`_
- `DateAfterValidator`_
- `DateBeforeValidator`_
- `DateRangeValidator`_
- `FloatPrecisionValidator`_
- `InArrayValidator`_
- `InEnumValidator`_
- `IsArrayValidator`_
- `IsBase64ImageCorrectSizeValidator`_
- `IsBase64ImageValidator`_
- `IsBooleanValidator`_
- `IsDataclassValidator`_
- `IsFloatValidator`_
- `IsFutureDateValidator`_
- `IsHexadecimalValidator`_
- `IsHorizontalImageValidator`_
- `IsHtmlValidator`_
- `IsInstanceValidator`_
- `IsIntegerValidator`_
- `IsJsonValidator`_
- `IsLowercaseValidator`_
- `IsMacAddressValidator`_
- `IsPastDateValidator`_
- `IsPortValidator`_
- `IsRgbColorValidator`_
- `IsSlugValidator`_
- `IsStringValidator`_
- `IsTypedDictValidator`_
- `IsUppercaseValidator`_
- `IsUrlValidator`_
- `IsUuidValidator`_
- `IsVerticalImageValidator`_
- `IsWeekdayValidator`_
- `IsWeekendValidator`_
- `LengthValidator`_
- `NotInArrayValidator`_
- `RangeValidator`_
- `RegexValidator`_


Special Validators
------------------

Following are the special validators that are used to combine or mutate the normal validators:

- :doc:`AndValidator <special_validator>`
- :doc:`NotValidator <special_validator>`
- :doc:`OrValidator <special_validator>`
- :doc:`XorValidator <special_validator>`

Detailed Description
--------------------

ArrayElementValidator
~~~~~~~~~~~~~~~~~~~~~
**Description:**

Validates each element within an array by applying an inner ``InputFilter`` to every element. It ensures that all array items conform to the expected structure.

**Parameters:**

- **elementFilter** (*InputFilter*): An instance used to validate each element.
- **error_message** (*Optional[str]*): Custom error message for validation failure.

**Expected Behavior:**

Verifies that the input is a list and then applies the provided filter to each element. If any element fails validation, a ``ValidationError`` is raised.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import ArrayElementValidator
    from my_filters import MyElementFilter

    class TagInputFilter(InputFilter):
        def __init__(self):

            self.add('tags', validators=[
                ArrayElementValidator(elementFilter=MyElementFilter())
            ])

ArrayLengthValidator
~~~~~~~~~~~~~~~~~~~~
**Description:**

Checks whether the length of an array falls within a specified range.

**Parameters:**

- **min_length** (*int*, default: 0): The minimum number of elements required.
- **max_length** (*int*, default: infinity): The maximum number of allowed elements.
- **error_message** (*Optional[str]*): Custom error message if the length check fails.

**Expected Behavior:**

Ensures that the input is a list and that its length is between the specified minimum and maximum. If not, a ``ValidationError`` is raised.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import ArrayLengthValidator

    class ListInputFilter(InputFilter):
        def __init__(self):

            self.add('items', validators=[
                ArrayLengthValidator(min_length=1, max_length=5)
            ])

CustomJsonValidator
~~~~~~~~~~~~~~~~~~~
**Description:**

Validates that the provided value is valid JSON. It also checks for the presence of required fields and optionally verifies field types against a provided schema.

**Parameters:**

- **required_fields** (*list*, default: []): Fields that must exist in the JSON.
- **schema** (*dict*, default: {}): A dictionary specifying expected types for certain fields.
- **error_message** (*Optional[str]*): Custom error message if validation fails.

**Expected Behavior:**

If the input is a string, it attempts to parse it as JSON. It then confirms that the result is a dictionary, contains all required fields, and that each field adheres to the defined type in the schema.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import CustomJsonValidator

    class JsonInputFilter(InputFilter):
        def __init__(self):

            self.add('data', validators=[
                CustomJsonValidator(
                    required_fields=['id', 'name'],
                    schema={'id': int, 'name': str}
                )
            ])

DateAfterValidator
~~~~~~~~~~~~~~~~~~
**Description:**

Ensures that a given date is after a specified reference date. It supports both datetime objects and ISO 8601 formatted strings.

**Parameters:**

- **reference_date** (*Union[str, date, datetime]*): The date that the input must be later than.
- **error_message** (*Optional[str]*): Custom error message if the validation fails.

**Expected Behavior:**

Converts both the input and the reference date to datetime objects and verifies that the input date is later. If the check fails, a ``ValidationError`` is raised.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import DateAfterValidator

    class EventInputFilter(InputFilter):
        def __init__(self):

            self.add('event_date', validators=[
                DateAfterValidator(reference_date="2023-01-01")
            ])

DateBeforeValidator
~~~~~~~~~~~~~~~~~~~
**Description:**

Validates that a given date is before a specified reference date. It supports datetime objects and ISO 8601 formatted strings.

**Parameters:**

- **reference_date** (*Union[str, date, datetime]*): The date that the input must be earlier than.
- **error_message** (*Optional[str]*): Custom error message if validation fails.

**Expected Behavior:**

Parses the input and reference date into datetime objects and checks that the input date is earlier. Raises a ``ValidationError`` on failure.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import DateBeforeValidator

    class RegistrationInputFilter(InputFilter):
        def __init__(self):

            self.add('birth_date', validators=[
                DateBeforeValidator(reference_date="2005-01-01")
            ])

DateRangeValidator
~~~~~~~~~~~~~~~~~~
**Description:**

Checks if a date falls within a specified range.

**Parameters:**

- **min_date** (*Optional[Union[str, date, datetime]]*): The lower bound of the date range.
- **max_date** (*Optional[Union[str, date, datetime]]*): The upper bound of the date range.
- **error_message** (*Optional[str]*): Custom error message if the date is outside the range.

**Expected Behavior:**

Ensures the input date is not earlier than ``min_date`` and not later than ``max_date``. A ``ValidationError`` is raised if the check fails.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import DateRangeValidator

    class BookingInputFilter(InputFilter):
        def __init__(self):

            self.add('booking_date', validators=[
                DateRangeValidator(min_date="2023-01-01", max_date="2023-12-31")
            ])

FloatPrecisionValidator
~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Ensures that a numeric value conforms to a specific precision and scale. This is useful for validating monetary values or measurements.

**Parameters:**

- **precision** (*int*): The maximum total number of digits allowed.
- **scale** (*int*): The maximum number of digits allowed after the decimal point.
- **error_message** (*Optional[str]*): Custom error message if validation fails.

**Expected Behavior:**

Converts the number to a string and checks the total number of digits and the digits after the decimal point. A ``ValidationError`` is raised if these limits are exceeded.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import FloatPrecisionValidator

    class PriceInputFilter(InputFilter):
        def __init__(self):

            self.add('price', validators=[
                FloatPrecisionValidator(precision=5, scale=2)
            ])

InArrayValidator
~~~~~~~~~~~~~~~~
**Description:**

Checks that the provided value exists within a predefined list of allowed values.

**Parameters:**

- **haystack** (*List[Any]*): The list of allowed values.
- **strict** (*bool*, default: False): When ``True``, also checks that the type of the value matches the types in the allowed list.
- **error_message** (*Optional[str]*): Custom error message if validation fails.

**Expected Behavior:**

Verifies that the value is present in the list. In strict mode, type compatibility is also enforced. If the check fails, a ``ValidationError`` is raised.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import InArrayValidator

    class StatusInputFilter(InputFilter):
        def __init__(self):

            self.add('status', validators=[
                InArrayValidator(haystack=["active", "inactive"])
            ])

InEnumValidator
~~~~~~~~~~~~~~~
**Description:**

Verifies that a given value is a valid member of a specified Enum class.

**Parameters:**

- **enumClass** (*Type[Enum]*): The Enum to validate against.
- **error_message** (*Optional[str]*): Custom error message if validation fails.

**Expected Behavior:**

Performs a case-insensitive comparison to ensure that the value matches one of the Enum's member names. Raises a ``ValidationError`` if the value is not a valid Enum member.

**Example Usage:**

.. code-block:: python

    from enum import Enum
    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import InEnumValidator

    class ColorEnum(Enum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    class ColorInputFilter(InputFilter):
        def __init__(self):

            self.add('color', validators=[
                InEnumValidator(enumClass=ColorEnum)
            ])

IsArrayValidator
~~~~~~~~~~~~~~~~
**Description:**

Checks if the provided value is an array (i.e. a list).

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if validation fails.

**Expected Behavior:**

Raises a ``ValidationError`` if the input is not a list.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsArrayValidator

    class ListInputFilter(InputFilter):
        def __init__(self):

            self.add('items', validators=[
                IsArrayValidator()
            ])

IsBase64ImageCorrectSizeValidator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Checks whether a Base64 encoded image has a size within the allowed range. By default, the image size must be between 1 and 4MB.

**Parameters:**

- **minSize** (*int*, default: 1): The minimum allowed size in bytes.
- **maxSize** (*int*, default: 4 * 1024 * 1024): The maximum allowed size in bytes.
- **error_message** (*Optional[str]*): Custom error message if validation fails.

**Expected Behavior:**

Decodes the Base64 string to determine the image size and raises a ``ValidationError`` if the image size is outside the permitted range.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsBase64ImageCorrectSizeValidator

    class ImageInputFilter(InputFilter):
        def __init__(self):

            self.add('image', validators=[
                IsBase64ImageCorrectSizeValidator(minSize=1024, maxSize=2 * 1024 * 1024)
            ])

IsBase64ImageValidator
~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Validates that a Base64 encoded string represents a valid image by decoding it and verifying its integrity.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if validation fails.

**Expected Behavior:**

Attempts to decode the Base64 string and open the image using the PIL library. If the image is invalid or corrupted, a ``ValidationError`` is raised.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsBase64ImageValidator

    class AvatarInputFilter(InputFilter):
        def __init__(self):

            self.add('avatar', validators=[
                IsBase64ImageValidator()
            ])

IsBooleanValidator
~~~~~~~~~~~~~~~~~~
**Description:**

Checks if the provided value is a boolean.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the input is not a bool.

**Expected Behavior:**

Raises a ``ValidationError`` if the input value is not of type bool.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsBooleanValidator

    class FlagInputFilter(InputFilter):
        def __init__(self):

            self.add('is_active', validators=[
                IsBooleanValidator()
            ])

IsDataclassValidator
~~~~~~~~~~~~~~~~~~~~
**Description:**

Validates that the provided value conforms to a specific dataclass type.

**Parameters:**

- **dataclass_type** (*Type[dict]*): The expected dataclass type.
- **error_message** (*Optional[str]*): Custom error message if validation fails.

**Expected Behavior:**

Ensures the input is a dictionary and, that all expected keys are present. Raises a ``ValidationError`` if the structure does not match.

**Example Usage:**

.. code-block:: python

    from dataclasses import dataclass
    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsDataclassValidator

    @dataclass
    class User:
        id: int
        name: str

    class UserInputFilter(InputFilter):
        def __init__(self):

            self.add('user', validators=[
                IsDataclassValidator(dataclass_type=User)
            ])

IsFloatValidator
~~~~~~~~~~~~~~~~
**Description:**

Checks if the provided value is a float.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not a float.

**Expected Behavior:**

Raises a ``ValidationError`` if the input value is not of type float.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsFloatValidator

    class MeasurementInputFilter(InputFilter):
        def __init__(self):

            self.add('temperature', validators=[
                IsFloatValidator()
            ])

IsFutureDateValidator
~~~~~~~~~~~~~~~~~~~~~
**Description:**

Ensures that a given date is in the future. Supports datetime objects and ISO 8601 formatted strings.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the date is not in the future.

**Expected Behavior:**

Parses the input date and compares it to the current date and time. If the input date is not later than the current time, a ``ValidationError`` is raised.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsFutureDateValidator

    class AppointmentInputFilter(InputFilter):
        def __init__(self):

            self.add('appointment_date', validators=[
                IsFutureDateValidator()
            ])

IsHexadecimalValidator
~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Checks if a given value is a valid hexadecimal string. The input must be a string that can be converted to an integer using base 16.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not a valid hexadecimal string.

**Expected Behavior:**

Verifies that the input is a string and attempts to convert it to an integer using base 16. Raises a ``ValidationError`` if the conversion fails.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsHexadecimalValidator

    class HexInputFilter(InputFilter):
        def __init__(self):
            self.add('hex_value', validators=[
                IsHexadecimalValidator()
            ])

IsHorizontalImageValidator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~          
**Description:**

Ensures that the provided image is horizontally oriented. This validator accepts either a Base64 encoded string or an image object.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the image is not horizontally oriented.

**Expected Behavior:**

Decodes the image (if provided as a string) and checks that its width is greater than or equal to its height. Raises a ``ValidationError`` if the image does not meet the horizontal orientation criteria.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsHorizontalImageValidator

    class HorizontalImageInputFilter(InputFilter):
        def __init__(self):
            self.add('image', validators=[
                IsHorizontalImageValidator()
            ])

IsHtmlValidator
~~~~~~~~~~~~~~~~

**Description:**

Checks if a value contains valid HTML. The validator looks for the presence of HTML tags in the input string.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value does not contain valid HTML.

**Expected Behavior:**

Verifies that the input is a string and checks for HTML tags using a regular expression. Raises a ``ValidationError`` if no HTML tags are found.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsHtmlValidator

    class HtmlInputFilter(InputFilter):
        def __init__(self):
            self.add('html_content', validators=[
                IsHtmlValidator()
            ])

IsInstanceValidator
~~~~~~~~~~~~~~~~~~~          
**Description:**

Validates that the provided value is an instance of a specified class.

**Parameters:**

- **classType** (*Type[Any]*): The class against which the value is validated.
- **error_message** (*Optional[str]*): Custom error message if the validation fails.

**Expected Behavior:**

Raises a ``ValidationError`` if the input is not an instance of the specified class.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsInstanceValidator

    class MyClass:
        pass

    class InstanceInputFilter(InputFilter):
        def __init__(self):
            self.add('object', validators=[
                IsInstanceValidator(classType=MyClass)
            ])

IsIntegerValidator
~~~~~~~~~~~~~~~~~~          
**Description:**

Checks whether the provided value is an integer.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not an integer.

**Expected Behavior:**

Raises a ``ValidationError`` if the input value is not of type int.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsIntegerValidator

    class NumberInputFilter(InputFilter):
        def __init__(self):
            self.add('number', validators=[
                IsIntegerValidator()
            ])

IsJsonValidator
~~~~~~~~~~~~~~~
**Description:**

Validates that the provided value is a valid JSON string.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the input is not a valid JSON string.

**Expected Behavior:**

Attempts to parse the input using JSON decoding. Raises a ``ValidationError`` if parsing fails.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsJsonValidator

    class JsonInputFilter(InputFilter):
        def __init__(self):
            self.add('json_data', validators=[
                IsJsonValidator()
            ])

IsLowercaseValidator
~~~~~~~~~~~~~~~~~~~~~

**Description:**

Checks if a value is entirely lowercase. The validator ensures that the input string has no uppercase characters.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not entirely lowercase.

**Expected Behavior:**

Confirms that the input is a string and verifies that all characters are lowercase using the string method ``islower()``. Raises a ``ValidationError`` if the check fails.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsLowercaseValidator

    class LowercaseInputFilter(InputFilter):
        def __init__(self):
            self.add('username', validators=[
                IsLowercaseValidator()
            ])


IsMacAddressValidator
~~~~~~~~~~~~~~~~~~~~~~

**Description:**

Checks if a value is a valid MAC address. It verifies common MAC address formats, such as colon-separated or hyphen-separated pairs of hexadecimal digits.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not a valid MAC address.

**Expected Behavior:**

Ensures the input is a string and matches a regular expression pattern for MAC addresses. Raises a ``ValidationError`` if the value does not conform to the expected MAC address format.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsMacAddressValidator

    class NetworkInputFilter(InputFilter):
        def __init__(self):
            self.add('mac_address', validators=[
                IsMacAddressValidator()
            ])

IsPastDateValidator
~~~~~~~~~~~~~~~~~~~
**Description:**

Checks whether a given date is in the past. Supports datetime objects, date objects, and ISO 8601 formatted strings.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the date is not in the past.

**Expected Behavior:**

Parses the input date and verifies that it is earlier than the current date and time. Raises a ``ValidationError`` if the input date is not in the past.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsPastDateValidator

    class HistoryInputFilter(InputFilter):
        def __init__(self):
            self.add('past_date', validators=[
                IsPastDateValidator()
            ])

IsPortValidator
~~~~~~~~~~~~~~~

**Description:**

Checks if a value is a valid network port. Valid port numbers range from 1 to 65535.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not a valid port number.

**Expected Behavior:**

Ensures that the input is an integer and that it lies within the valid range for port numbers. Raises a ``ValidationError`` if the value is outside this range.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsPortValidator

    class PortInputFilter(InputFilter):
        def __init__(self):
            self.add('port', validators=[
                IsPortValidator()
            ])


IsRgbColorValidator
~~~~~~~~~~~~~~~~~~~

**Description:**

Checks if a value is a valid RGB color string. The expected format is ``rgb(r, g, b)`` where *r*, *g*, and *b* are integers between 0 and 255.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not a valid RGB color.

**Expected Behavior:**

Verifies that the input is a string, matches the RGB color format using a regular expression, and that the extracted numeric values are within the range 0 to 255. Raises a ``ValidationError`` if the check fails.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsRgbColorValidator

    class ColorInputFilter(InputFilter):
        def __init__(self):
            self.add('color', validators=[
                IsRgbColorValidator()
            ])

IsSlugValidator
~~~~~~~~~~~~~~~

**Description:**

Checks if a value is a valid slug. A slug is typically a lowercase string that may contain numbers and hyphens, and does not include spaces or special characters.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not a valid slug.

**Expected Behavior:**

Ensures that the input is a string and matches the expected slug pattern (e.g., using a regular expression such as ``^[a-z0-9]+(?:-[a-z0-9]+)*$``). Raises a ``ValidationError`` if the input does not conform to this format.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsSlugValidator

    class SlugInputFilter(InputFilter):
        def __init__(self):
            self.add('slug', validators=[
                IsSlugValidator()
            ])

IsStringValidator
~~~~~~~~~~~~~~~~~
**Description:**

Validates that the provided value is a string.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not a string.

**Expected Behavior:**

Raises a ``ValidationError`` if the input is not of type str.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsStringValidator

    class TextInputFilter(InputFilter):
        def __init__(self):
            self.add('text', validators=[
                IsStringValidator()
            ])

IsTypedDictValidator
~~~~~~~~~~~~~~~~~~~~
**Description:**

Validates that the provided value conforms to a specified TypedDict structure.

**Parameters:**

- **typed_dict_type** (*Type[TypedDict]*): The TypedDict class that defines the expected structure.
- **error_message** (*Optional[str]*): Custom error message if the validation fails.

**Expected Behavior:**

Ensures the input is a dictionary and, that all expected keys are present. Raises a ``ValidationError`` if the structure does not match.

**Example Usage:**

.. code-block:: python

    from typing import TypedDict
    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsTypedDictValidator

    class PersonDict(TypedDict):
        name: str
        age: int

    class PersonInputFilter(InputFilter):
        def __init__(self):
            self.add('person', validators=[
                IsTypedDictValidator(typed_dict_type=PersonDict)
            ])

IsUppercaseValidator
~~~~~~~~~~~~~~~~~~~~

**Description:**

Checks if a value is entirely uppercase. It verifies that the input string has no lowercase characters.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not entirely uppercase.

**Expected Behavior:**

Ensures that the input is a string and that all characters are uppercase using the string method ``isupper()``. Raises a ``ValidationError`` if the check fails.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsUppercaseValidator

    class UppercaseInputFilter(InputFilter):
        def __init__(self):
            self.add('code', validators=[
                IsUppercaseValidator()
            ])


IsUrlValidator
~~~~~~~~~~~~~~

**Description:**

Checks if a value is a valid URL. The validator uses URL parsing to ensure that the input string contains a valid scheme and network location.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the value is not a valid URL.

**Expected Behavior:**

Verifies that the input is a string and uses URL parsing (via ``urllib.parse.urlparse``) to confirm that both the scheme and network location are present. Raises a ``ValidationError`` if the URL is invalid.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsUrlValidator

    class UrlInputFilter(InputFilter):
        def __init__(self):
            self.add('website', validators=[
                IsUrlValidator()
            ])

IsUUIDValidator
~~~~~~~~~~~~~~~
**Description:**

Checks if the provided value is a valid UUID string.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the input is not a valid UUID.

**Expected Behavior:**

Verifies that the input is a string and attempts to parse it as a UUID. Raises a ``ValidationError`` if parsing fails.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsUUIDValidator

    class UUIDInputFilter(InputFilter):
        def __init__(self):
            self.add('uuid', validators=[
                IsUUIDValidator()
            ])

IsVerticalImageValidator
~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Validates that the provided image is vertically oriented. Accepts either a Base64 encoded string or an image object.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the image is not vertically oriented.

**Expected Behavior:**

Decodes the image (if provided as a string) and checks that its height is greater than or equal to its width. Raises a ``ValidationError`` if the image is horizontally oriented.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsVerticalImageValidator

    class VerticalImageInputFilter(InputFilter):
        def __init__(self):
            self.add('image', validators=[
                IsVerticalImageValidator()
            ])

IsWeekdayValidator
~~~~~~~~~~~~~~~~~~
**Description:**

Checks whether a given date falls on a weekday (Monday to Friday). Supports datetime objects, date objects, and ISO 8601 formatted strings.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the date is not a weekday.

**Expected Behavior:**

Parses the input date and verifies that it corresponds to a weekday. Raises a ``ValidationError`` if the date falls on a weekend.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsWeekdayValidator

    class WorkdayInputFilter(InputFilter):
        def __init__(self):
            self.add('date', validators=[
                IsWeekdayValidator()
            ])

IsWeekendValidator
~~~~~~~~~~~~~~~~~~
**Description:**

Validates that a given date falls on a weekend (Saturday or Sunday). Supports datetime objects, date objects, and ISO 8601 formatted strings.

**Parameters:**

- **error_message** (*Optional[str]*): Custom error message if the date is not on a weekend.

**Expected Behavior:**

Parses the input date and confirms that it corresponds to a weekend day. Raises a ``ValidationError`` if the date is on a weekday.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsWeekendValidator

    class WeekendInputFilter(InputFilter):
        def __init__(self):
            self.add('date', validators=[
                IsWeekendValidator()
            ])

LengthValidator
~~~~~~~~~~~~~~~
**Description:**

Validates the length of a string, ensuring it falls within a specified range.

**Parameters:**

- **min_length** (*Optional[int]*): The minimum allowed length.
- **max_length** (*Optional[int]*): The maximum allowed length.
- **error_message** (*Optional[str]*): Custom error message if the validation fails.

**Expected Behavior:**

Checks the length of the input string and raises a ``ValidationError`` if it is shorter than ``min_length`` or longer than ``max_length``.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import LengthValidator

    class TextLengthInputFilter(InputFilter):
        def __init__(self):
            self.add('username', validators=[
                LengthValidator(min_length=3, max_length=15)
            ])


NotInArrayValidator
~~~~~~~~~~~~~~~~~~~
**Description:**

Ensures that the provided value is not present in a specified list of disallowed values.

**Parameters:**

- **haystack** (*List[Any]*): A list of disallowed values.
- **strict** (*bool*, default: False): If ``True``, the type of the value is also validated against the disallowed list.
- **error_message** (*Optional[str]*): Custom error message if the validation fails.

**Expected Behavior:**

Raises a ``ValidationError`` if the value is found in the disallowed list, or if strict type checking is enabled and the value's type does not match any allowed type.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import NotInArrayValidator

    class UsernameInputFilter(InputFilter):
        def __init__(self):
            self.add('username', validators=[
                NotInArrayValidator(haystack=["admin", "root"])
            ])

RangeValidator
~~~~~~~~~~~~~~
**Description:**

Checks whether a numeric value falls within a specified range.

**Parameters:**

- **min_value** (*Optional[float]*): The minimum allowed value.
- **max_value** (*Optional[float]*): The maximum allowed value.
- **error_message** (*Optional[str]*): Custom error message if the validation fails.

**Expected Behavior:**

Verifies that the numeric input is not less than ``min_value`` and not greater than ``max_value``. Raises a ``ValidationError`` if the value is outside this range.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import RangeValidator

    class ScoreInputFilter(InputFilter):
        def __init__(self):
            self.add('score', validators=[
                RangeValidator(min_value=0, max_value=100)
            ])

RegexValidator
~~~~~~~~~~~~~~
**Description:**

Validates that the input string matches a specified regular expression pattern.

**Parameters:**

- **pattern** (*str*): The regular expression pattern the input must match.
- **error_message** (*Optional[str]*): Custom error message if the input does not match the pattern.

**Expected Behavior:**

Uses the Python ``re`` module to compare the input string against the provided pattern. Raises a ``ValidationError`` if there is no match.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import RegexValidator

    class EmailInputFilter(InputFilter):
        def __init__(self):
            self.add('email', validators=[
                RegexValidator(pattern=r"[^@]+@[^@]+\.[^@]+")
            ])

