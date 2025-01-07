# Filter

The `Filter` module contains the filters that can be used to filter the input data.

## Available filters

The following filters are available in the `Filter` module:

1. [`ArrayExplodeFilter`](src/flask_inputfilter/Filter/ArrayExplodeFilter.py) - Explodes the input string into an array.
2. [`StringTrimFilter`](src/flask_inputfilter/Filter/StringTrimFilter.py) - Trims the whitespace from the beginning and end of the string.
3. [`ToBooleanFilter`](src/flask_inputfilter/Filter/ToBooleanFilter.py) - Converts the string to a boolean value.
4. [`ToCamelCaseFilter`](src/flask_inputfilter/Filter/ToCamelCaseFilter.py) - Converts the string to camel case.
5. [`ToFloatFilter`](src/flask_inputfilter/Filter/ToFloatFilter.py) - Converts the string to a float value.
5. [`ToIntegerFilter`](src/flask_inputfilter/Filter/ToIntegerFilter.py) - Converts the string to an integer value.
6. [`ToLowerFilter`](src/flask_inputfilter/Filter/ToLowerFilter.py) - Converts the string to lowercase.
7. [`ToNullFilter`](src/flask_inputfilter/Filter/ToNullFilter.py) - Converts the string to `None` if it is already `None` or `''` (empty string).
8. [`ToPascaleCaseFilter`](src/flask_inputfilter/Filter/ToPascaleCaseFilter.py) - Converts the string to pascal case.
9. [`ToSnakeCaseFilter`](src/flask_inputfilter/Filter/ToSnakeCaseFilter.py) - Converts the string to snake case.
9. [`ToStringFilter`](src/flask_inputfilter/Filter/ToStringFilter.py) - Converts the input to a string value.
9. [`ToUpperFilter`](src/flask_inputfilter/Filter/ToUpperFilter.py) - Converts the string to uppercase.
10. [`WhitespaceCollapseFilter`](src/flask_inputfilter/Filter/WhitespaceCollapseFilter.py) - Collapses the whitespace in the string.
