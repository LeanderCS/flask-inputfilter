# Validator

The `Validator` class is used to validate the data after the filters have been applied.

## Available validators

The following validators are available in the `Validator` module:

1. [`ArrayElementValidator`](ArrayElementValidator.py) - Validates each element of an array with its own defined InputFilter.
2. [`ArrayLengthValidator`](ArrayLengthValidator.py) - Validates the length of an array.
3. [`DateRangeValidator`](DateRangeValidator.py) - Validates that the date is within a specified range.
4. [`FloatPrecisionValidator`](FloatPrecisionValidator.py) - Validates the precision of a float.
5. [`InArrayValidator`](InArrayValidator.py) - Validates that the value is in the given array.
6. [`InEnumValidator`](InEnumValidator.py) - Validates that the value is in the given enum.
7. [`IsArrayValidator`](IsArrayValidator.py) - Validates that the value is an array.
8. [`IsBase64ImageCorrectSizeValidator`](IsBase64ImageCorrectSizeValidator.py) - Validates that the value is a base64 encoded string.
9. [`IsBase64ImageValidator`](IsBase64ImageValidator.py) - Validates that the value is a base64 encoded string.
10. [`IsBooleanValidator`](IsBooleanValidator.py) - Validates that the value is a boolean.
11. [`IsFloatValidator`](IsFloatValidator.py) - Validates that the value is a float.
12. [`IsFutureDateValidator`](IsFutureDateValidator.py) - Validates that the value is a future date.
13. [`IsHexadecimalValidator`](IsHexadecimalValidator.py) - Validates that the value is a hexadecimal string.
14. [`IsInstanceValidator`](IsInstanceValidator.py) - Validates that the value is an instance of a class.
15. [`IsIntegerValidator`](IsIntegerValidator.py) - Validates that the value is an integer.
16. [`IsJsonValidator`](IsJsonValidator.py) - Validates that the value is a json string.
17. [`IsPastDateValidator`](IsPastDateValidator.py) - Validates that the value is a past date.
18. [`IsStringValidator`](IsStringValidator.py) - Validates that the value is a string.
19. [`IsUUIDValidator`](IsUUIDValidator.py) - Validates that the value is a UUID.
20. [`IsWeekdayValidator`](IsWeekdayValidator.py) - Validates that the value is a weekday.
21. [`IsWeekendValidator`](IsWeekendValidator.py) - Validates that the value is a weekend.
22. [`LengthValidator`](LengthValidator.py) - Validates the length of the value.
23. [`RangeValidator`](RangeValidator.py) - Validates that the value is within a specified range.
24. [`RegexValidator`](RegexValidator.py) - Validates that the value matches a regex pattern.
