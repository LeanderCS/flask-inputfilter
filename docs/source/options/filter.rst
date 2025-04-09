Filter
======

``Filters`` are used to filter the input data to a wanted format.

Overview
--------

Filters can be added into the ``add`` method for a specific field or as a global filter for all fields in ``addGlobalFilter``.

The global filters will be executed before the specific field filtering.

Example
-------

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import StringTrimFilter, ToLowerFilter

    class TestInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add(
                'username',
                required=True,
                filters=[StringTrimFilter()]
            )

            self.add(
                'name',
                required=True,
                filters=[StringTrimFilter()]
            )

            self.addGlobalFilter(ToLowerFilter())

Available Filters
-----------------

The following filters are available:

- `ArrayExplodeFilter`_
- `Base64ImageDownscaleFilter`_
- `Base64ImageResizeFilter`_
- `BlacklistFilter`_
- `StringRemoveEmojisFilter`_
- `StringSlugifyFilter`_
- `StringTrimFilter`_
- `ToAlphaNumericFilter`_
- `ToBooleanFilter`_
- `ToCamelCaseFilter`_
- `ToDateFilter`_
- `ToDateTimeFilter`_
- `ToDigitsFilter`_
- `ToEnumFilter`_
- `ToFloatFilter`_
- `ToIntegerFilter`_
- `ToIsoFilter`_
- `ToLowerFilter`_
- `ToNormalizedUnicodeFilter`_
- `ToNullFilter`_
- `ToPascalCaseFilter`_
- `ToSnakeCaseFilter`_
- `ToStringFilter`_
- `ToUpperFilter`_
- `TruncateFilter`_
- `WhitelistFilter`_
- `WhitespaceCollapseFilter`_

Detailed Description
--------------------

ArrayExplodeFilter
~~~~~~~~~~~~~~~~~~
**Description:**

Splits a string into an array based on a specified delimiter.

**Parameters:**

- **delimiter** (*str*, default: ``","``): The delimiter used to split the string.

**Expected Behavior:**

If the input value is a string, it returns a list of substrings. For non-string values, it returns the value unchanged.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import ArrayExplodeFilter

    class TagFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('tags', filters=[
                ArrayExplodeFilter(delimiter=";")
            ])

Base64ImageDownscaleFilter
~~~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Downscales a base64-encoded image to fit within a specified size. The filter can work with both base64 strings and PIL Image objects.

**Parameters:**

- **size** (*int*, default: ``1024 * 1024``): A rough pixel count used to compute default dimensions.
- **width** (*Optional[int]*): The target width. If not provided, it is calculated as ``sqrt(size)``.
- **height** (*Optional[int]*): The target height. If not provided, it is calculated as ``sqrt(size)``.
- **proportionally** (*bool*, default: ``True``): Determines if the image should be scaled proportionally. If ``False``, the image is forcefully resized to the specified width and height.

**Expected Behavior:**

If the image (or its base64 representation) exceeds the target dimensions, the filter downscales it. The result is a base64-encoded string. If the image is already within bounds or if the input is not a valid image, the original value is returned.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import Base64ImageDownscaleFilter

    class ImageFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('profile_pic', filters=[
                Base64ImageDownscaleFilter(size=1024*1024)
            ])

Base64ImageResizeFilter
~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Reduces the file size of a base64-encoded image by resizing and compressing it.

**Parameters:**

- **max_size** (*int*, default: ``4 * 1024 * 1024``): The maximum allowed file size in bytes.
- **format** (*ImageFormatEnum*, default: ``ImageFormatEnum.JPEG``): The output image format.
- **preserve_icc_profile** (*bool*, default: ``False``): If set to ``True``, the ICC profile is preserved.
- **preserve_metadata** (*bool*, default: ``False``): If set to ``True``, image metadata is preserved.

**Expected Behavior:**

The filter resizes and compresses the image iteratively until its size is below the specified maximum. The final output is a base64-encoded string of the resized image. If the input is invalid, the original value is returned.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import Base64ImageResizeFilter

    class AvatarFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('avatar', filters=[
                Base64ImageResizeFilter(max_size=4*1024*1024)
            ])

BlacklistFilter
~~~~~~~~~~~~~~~
**Description:**
Filters out unwanted substrings or keys based on a predefined blacklist.

**Parameters:**

- **blacklist** (*List[str]*): A list of substrings (for strings) or keys (for dictionaries) that should be removed.

**Expected Behavior:**

- For strings: Removes any occurrence of blacklisted items and trims whitespace.
- For lists: Filters out items present in the blacklist.
- For dictionaries: Removes key-value pairs where the key is blacklisted.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import BlacklistFilter

    class CommentFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('comment', filters=[
                BlacklistFilter(blacklist=["badword1", "badword2"])
            ])

StringRemoveEmojisFilter
~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Removes emojis from a string using regular expression matching.

**Expected Behavior:**

If the input is a string, all emoji characters are removed; non-string inputs are returned unchanged.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import StringRemoveEmojisFilter

    class CommentFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('comment', filters=[
                StringRemoveEmojisFilter()
            ])

StringSlugifyFilter
~~~~~~~~~~~~~~~~~~~
**Description:**

Converts a string into a slug format without deprecation warnings.

**Expected Behavior:**

Normalizes Unicode, converts to ASCII, lowercases the string, and replaces spaces with hyphens, producing a URL-friendly slug.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import StringSlugifyFilter

    class PostFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('title', filters=[
                StringSlugifyFilter()
            ])

StringTrimFilter
~~~~~~~~~~~~~~~~
**Description:**

Removes leading and trailing whitespace from a string.

**Expected Behavior:**

If the input is a string, it returns the trimmed version. Otherwise, the value remains unchanged.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import StringTrimFilter

    class UserFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('username', filters=[
                StringTrimFilter()
            ])

ToAlphaNumericFilter
~~~~~~~~~~~~~~~~~~~~
**Description:**

Ensures that a string contains only alphanumeric characters by removing all non-word characters.

**Expected Behavior:**

Strips out any character that is not a letter, digit, or underscore from the input string.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import ToAlphaNumericFilter

    class CodeFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('code', filters=[
                ToAlphaNumericFilter()
            ])

ToBooleanFilter
~~~~~~~~~~~~~~~
**Description:**

Converts the input value to a boolean.

**Expected Behavior:**

Uses Python’s built-in ``bool()`` conversion. Note that non-empty strings and non-zero numbers will return ``True``.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import ToBooleanFilter

    class ActiveFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('active', filters=[
                ToBooleanFilter()
            ])

ToCamelCaseFilter
~~~~~~~~~~~~~~~~~
**Description:**

Transforms a string into camelCase format.

**Expected Behavior:**

Normalizes delimiters such as spaces, underscores, or hyphens, capitalizes each word (except the first), and concatenates them so that the first letter is lowercase.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import ToCamelCaseFilter

    class IdentifierFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('identifier', filters=[
                ToCamelCaseFilter()
            ])

ToDataclassFilter
~~~~~~~~~~~~~~~~~
**Description:**

Converts a dictionary to a specified dataclass.

**Parameters:**

- **dataclass_type** (*Type[dict]*): The target dataclass type that the dictionary should be converted into.

**Expected Behavior:**
If the input is a dictionary, it instantiates the provided dataclass using the dictionary values. Otherwise, the input is returned unchanged.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import ToDataclassFilter
    from my_dataclasses import MyDataClass

    class DataFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('data', filters=[
                ToDataclassFilter(MyDataClass)
            ])

ToDateFilter
~~~~~~~~~~~~
**Description:**

Converts an input value to a ``date`` object. Supports ISO 8601 formatted strings and datetime objects.

**Expected Behavior:**

- If the input is a datetime, returns the date portion.
- If the input is a string, attempts to parse it as an ISO 8601 date.
- Returns the original value if conversion fails.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import ToDateFilter

    class BirthdateFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('birthdate', filters=[
                ToDateFilter()
            ])

ToDateTimeFilter
~~~~~~~~~~~~~~~~
**Description:**

Converts an input value to a ``datetime`` object. Supports ISO 8601 formatted strings.

**Expected Behavior:**

- If the input is a datetime, it is returned unchanged.
- If the input is a date, it is combined with a minimum time value.
- If the input is a string, the filter attempts to parse it as an ISO 8601 datetime.
- If conversion fails, the original value is returned.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import ToDateTimeFilter

    class TimestampFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('timestamp', filters=[
                ToDateTimeFilter()
            ])

ToDigitsFilter
~~~~~~~~~~~~~~
**Description:**

Converts a string to a numeric type (either an integer or a float).

**Expected Behavior:**

- If the input string matches an integer pattern, it returns an integer.
- If it matches a float pattern, it returns a float.
- Otherwise, the input is returned unchanged.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import ToDigitsFilter

    class QuantityFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('quantity', filters=[
                ToDigitsFilter()
            ])

ToEnumFilter
~~~~~~~~~~~~
**Description:**

Converts a value to an instance of a specified Enum.

**Parameters:**

- **enum_class** (*Type[Enum]*): The enum class to which the input should be converted.

**Expected Behavior:**

- If the input is a string or an integer, the filter attempts to convert it into the corresponding enum member.
- If the input is already an enum instance, it is returned as is.
- If conversion fails, the original input is returned.

**Example Usage:**

.. code:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import ToEnumFilter
    from my_enums import ColorEnum

    class ColorFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('color', filters=[
                ToEnumFilter(ColorEnum)
            ])

ToFloatFilter
~~~~~~~~~~~~~
**Description:**

Converts the input value to a float.

**Expected Behavior:**

- Attempts to cast the input using ``float()``.
- On a ValueError or TypeError, returns the original value.

**Example Usage:**

.. code:: python

    class PriceFilter(InputFilter):
        def __init__(self):
            super().__init__()

                self.add('price', filters=[
                    ToFloatFilter()
                ])

ToIntegerFilter
~~~~~~~~~~~~~~~
**Description:**


Converts the input value to an integer.

**Expected Behavior:**


- Attempts to cast the input using ``int()``.
- On failure, returns the original value.

**Example Usage:**

.. code:: python

    class AgeFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('age', filters=[
                ToIntegerFilter()
            ])

ToIsoFilter
~~~~~~~~~~~
**Description:**


Converts a date or datetime object to an ISO 8601 formatted string.

**Expected Behavior:**


- If the input is a date or datetime, returns its ISO 8601 string.
- Otherwise, returns the original value.

**Example Usage:**

.. code:: python

    class TimestampIsoFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('timestamp', filters=[
            ToIsoFilter()
            ])

ToLowerFilter
~~~~~~~~~~~~~
**Description:**


Converts a string to lowercase.

**Expected Behavior:**


- For string inputs, returns the lowercase version.
- Non-string inputs are returned unchanged.

**Example Usage:**

.. code:: python

    class UsernameFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('username', filters=[
                ToLowerFilter()
            ])

ToNormalizedUnicodeFilter
~~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Normalizes a Unicode string to a specified form.

**Parameters:**

- **form** (*Union[UnicodeFormEnum, Literal["NFC", "NFD", "NFKC", "NFKD"]]*, default: ``UnicodeFormEnum.NFC``): The target Unicode normalization form.

**Expected Behavior:**

- Removes accent characters and normalizes the string based on the specified form.
- Returns non-string inputs unchanged.

**Example Usage:**

.. code:: python

    class TextFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('text', filters=[
                ToNormalizedUnicodeFilter(form="NFKC")
            ])

ToNullFilter
~~~~~~~~~~~~
**Description:**

Transforms the input to ``None`` if it is an empty string or already ``None``.

**Expected Behavior:**

- If the input is ``""`` or ``None``, returns ``None``.
- Otherwise, returns the original value.

**Example Usage:**

.. code:: python

    class MiddleNameFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('middle_name', filters=[
                ToNullFilter()
            ])

ToPascalCaseFilter
~~~~~~~~~~~~~~~~~~~
**Description:**

Converts a string to PascalCase.

**Expected Behavior:**

- Capitalizes the first letter of each word and concatenates them without spaces.
- Returns non-string inputs unchanged.

**Example Usage:**

.. code:: python

    class ClassNameFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('class_name', filters=[
                ToPascalCaseFilter()
            ])

ToSnakeCaseFilter
~~~~~~~~~~~~~~~~~
**Description:**

Converts a string to snake_case.

**Expected Behavior:**

- Inserts underscores before uppercase letters (except the first), converts the string to lowercase, and replaces spaces or hyphens with underscores.
- Non-string inputs are returned unchanged.

**Example Usage:**

.. code:: python

    class VariableFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('variableName', filters=[
                ToSnakeCaseFilter()
            ])

ToStringFilter
~~~~~~~~~~~~~~
**Description:**

Converts any input value to its string representation.

**Expected Behavior:**

- Uses Python's built-in ``str()`` to convert the input to a string.

**Example Usage:**

.. code:: python

    class IdFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('id', filters=[
                ToStringFilter()
            ])

ToTypedDictFilter
~~~~~~~~~~~~~~~~~
**Description:**

Converts a dictionary into an instance of a specified TypedDict.

**Parameters:**

- **typed_dict** (*Type[TypedDict]*): The target TypedDict type.

**Expected Behavior:**

- If the input is a dictionary, returns an instance of the specified TypedDict.
- Otherwise, returns the original value.

**Example Usage:**

.. code:: python

    class ConfigFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('config', filters=[
                ToTypedDictFilter(MyTypedDict)
            ])

ToUpperFilter
~~~~~~~~~~~~~
**Description:**

Converts a string to uppercase.

**Expected Behavior:**

- For string inputs, returns the uppercase version.
- Non-string inputs are returned unchanged.

**Example Usage:**

.. code:: python

    class CodeFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('code', filters=[
                ToUpperFilter()
            ])

TruncateFilter
~~~~~~~~~~~~~~
**Description:**

Truncates a string to a specified maximum length.

**Parameters:**

- **max_length** (*int*): The maximum allowed length of the string.

**Expected Behavior:**

- If the string exceeds the specified length, it is truncated.
- Non-string inputs are returned unchanged.

**Example Usage:**

.. code:: python

    class DescriptionFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('description', filters=[
                TruncateFilter(max_length=100)
            ])

WhitelistFilter
~~~~~~~~~~~~~~~
**Description:**

Filters the input by only keeping elements that appear in a predefined whitelist.

**Parameters:**

- **whitelist** (*List[str]*, optional): A list of allowed words or keys. If not provided, no filtering is applied.

**Expected Behavior:**

- For strings: Splits the input by whitespace and returns only the words present in the whitelist.
- For lists: Returns a list of items that are in the whitelist.
- For dictionaries: Returns a dictionary containing only the whitelisted keys.

**Example Usage:**

.. code:: python

    class RolesFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('roles', filters=[
                WhitelistFilter(whitelist=["admin", "user"])
            ])

WhitespaceCollapseFilter
~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Collapses multiple consecutive whitespace characters into a single space.

**Expected Behavior:**

- Replaces sequences of whitespace with a single space and trims the result.
- Non-string inputs are returned unchanged.

**Example Usage:**

.. code:: python

    class AddressFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('address', filters=[
                WhitespaceCollapseFilter()
            ])
