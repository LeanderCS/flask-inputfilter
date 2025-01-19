Filter
======

The ``Filter`` module contains the filters that can be used to filter the input data.

Filters
-------

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

The following filters are available in the ``Filter`` module:

1. `ArrayExplodeFilter` - Explodes the input string into an array.
2. `Base64ImageDownscaleFilter` - Downscale the base64 image.
3. `Base64ImageResizeFilter` - Resize the base64 image.
4. `BlacklistFilter` - Filters the string based on the blacklist.
5. `RemoveEmojisFilter` - Removes the emojis from the string.
6. `SlugifyFilter` - Converts the string to a slug.
7. `StringTrimFilter` - Trims the whitespace from the beginning and end of the string.
8. `ToAlphaNumericFilter` - Converts the string to an alphanumeric string.
9. `ToBooleanFilter` - Converts the string to a boolean value.
10. `ToCamelCaseFilter` - Converts the string to camel case.
11. `ToDateFilter` - Converts a string to a date value.
12. `ToDateTimeFilter` - Converts a string to a datetime value.
13. `ToEnumFilter` - Converts a string or integer to an enum value.
14. `ToFloatFilter` - Converts a string to a float value.
15. `ToIntegerFilter` - Converts a string to an integer value.
16. `ToIsoFilter` - Converts a string to an ISO8601 date time value.
17. `ToLowerFilter` - Converts a string to lowercase.
18. `ToNormalizedUnicodeFilter` - Normalizes a unicode string.
19. `ToNullFilter` - Converts the string to ``None`` if it is already ``None`` or ``''`` (empty string).
20. `ToPascaleCaseFilter` - Converts the string to pascal case.
21. `ToSnakeCaseFilter` - Converts the string to snake case.
22. `ToStringFilter` - Converts the input to a string value.
23. `ToUpperFilter` - Converts the string to uppercase.
24. `TruncateFilter` - Truncates the string to the specified length.
25. `WhitelistFilter` - Filters the string based on the whitelist.
26. `WhitespaceCollapseFilter` - Collapses the whitespace in the string.
