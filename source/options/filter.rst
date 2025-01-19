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

1. `ArrayExplodeFilter <../flask_inputfilter/Filter/ArrayExplodeFilter.py>`_ - Explodes the input string into an array.
2. `Base64ImageDownscaleFilter <../flask_inputfilter/Filter/Base64ImageDownscaleFilter.py>`_ - Downscale the base64 image.
3. `Base64ImageResizeFilter <../flask_inputfilter/Filter/Base64ImageResizeFilter.py>`_ - Resize the base64 image.
4. `BlacklistFilter <../flask_inputfilter/Filter/BlacklistFilter.py>`_ - Filters the string based on the blacklist.
5. `RemoveEmojisFilter <../flask_inputfilter/Filter/RemoveEmojisFilter.py>`_ - Removes the emojis from the string.
6. `SlugifyFilter <../flask_inputfilter/Filter/SlugifyFilter.py>`_ - Converts the string to a slug.
7. `StringTrimFilter <../flask_inputfilter/Filter/StringTrimFilter.py>`_ - Trims the whitespace from the beginning and end of the string.
8. `ToAlphaNumericFilter <../flask_inputfilter/Filter/ToAlphaNumericFilter.py>`_ - Converts the string to an alphanumeric string.
9. `ToBooleanFilter <../flask_inputfilter/Filter/ToBooleanFilter.py>`_ - Converts the string to a boolean value.
10. `ToCamelCaseFilter <../flask_inputfilter/Filter/ToCamelCaseFilter.py>`_ - Converts the string to camel case.
11. `ToDateFilter <../flask_inputfilter/Filter/ToDateFilter.py>`_ - Converts a string to a date value.
12. `ToDateTimeFilter <../flask_inputfilter/Filter/ToDateTimeFilter.py>`_ - Converts a string to a datetime value.
13. `ToEnumFilter <../flask_inputfilter/Filter/ToEnumFilter.py>`_ - Converts a string or integer to an enum value.
14. `ToFloatFilter <../flask_inputfilter/Filter/ToFloatFilter.py>`_ - Converts a string to a float value.
15. `ToIntegerFilter <../flask_inputfilter/Filter/ToIntegerFilter.py>`_ - Converts a string to an integer value.
16. `ToIsoFilter <../flask_inputfilter/Filter/ToIsoFilter.py>`_ - Converts a string to an ISO8601 date time value.
17. `ToLowerFilter <../flask_inputfilter/Filter/ToLowerFilter.py>`_ - Converts a string to lowercase.
18. `ToNormalizedUnicodeFilter <../flask_inputfilter/Filter/ToNormalizedUnicodeFilter.py>`_ - Normalizes a unicode string.
19. `ToNullFilter <../flask_inputfilter/Filter/ToNullFilter.py>`_ - Converts the string to ``None`` if it is already ``None`` or ``''`` (empty string).
20. `ToPascaleCaseFilter <../flask_inputfilter/Filter/ToPascaleCaseFilter.py>`_ - Converts the string to pascal case.
21. `ToSnakeCaseFilter <../flask_inputfilter/Filter/ToSnakeCaseFilter.py>`_ - Converts the string to snake case.
22. `ToStringFilter <../flask_inputfilter/Filter/ToStringFilter.py>`_ - Converts the input to a string value.
23. `ToUpperFilter <../flask_inputfilter/Filter/ToUpperFilter.py>`_ - Converts the string to uppercase.
24. `TruncateFilter <../flask_inputfilter/Filter/TruncateFilter.py>`_ - Truncates the string to the specified length.
25. `WhitelistFilter <../flask_inputfilter/Filter/WhitelistFilter.py>`_ - Filters the string based on the whitelist.
26. `WhitespaceCollapseFilter <../flask_inputfilter/Filter/WhitespaceCollapseFilter.py>`_ - Collapses the whitespace in the string.
