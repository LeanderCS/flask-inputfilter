# Validator

The `Validator` class is used to validate the data after the filters have been applied.

## Available validators

The following validators are available in the `Validator` module:

1. [`ArrayElementValidator`](ArrayElementValidator.py) - Validates each element of an array with its own defined InputFilter.
2. [`ArrayLengthValidator`](ArrayLengthValidator.py) - Validates the length of an array.
3. [`DateAfterValidator`](DateAfterValidator.py) - Validates that the date is after a specified date.
4. [`DateBeforeValidator`](DateBeforeValidator.py) - Validates that the date is before a specified date.
5. [`DateRangeValidator`](DateRangeValidator.py) - Validates that the date is within a specified range.
6. [`FloatPrecisionValidator`](FloatPrecisionValidator.py) - Validates the precision of a float.
7. [`InArrayValidator`](InArrayValidator.py) - Validates that the value is in the given array.
8. [`InEnumValidator`](InEnumValidator.py) - Validates that the value is in the given enum.
9. [`IsArrayValidator`](IsArrayValidator.py) - Validates that the value is an array.
10. [`IsBase64ImageCorrectSizeValidator`](IsBase64ImageCorrectSizeValidator.py) - Validates that the value is a base64 encoded string.
11. [`IsBase64ImageValidator`](IsBase64ImageValidator.py) - Validates that the value is a base64 encoded string.
12. [`IsBooleanValidator`](IsBooleanValidator.py) - Validates that the value is a boolean.
13. [`IsFloatValidator`](IsFloatValidator.py) - Validates that the value is a float.
14. [`IsFutureDateValidator`](IsFutureDateValidator.py) - Validates that the value is a future date.
15. [`IsHexadecimalValidator`](IsHexadecimalValidator.py) - Validates that the value is a hexadecimal string.
16. [`IsInstanceValidator`](IsInstanceValidator.py) - Validates that the value is an instance of a class.
17. [`IsIntegerValidator`](IsIntegerValidator.py) - Validates that the value is an integer.
18. [`IsJsonValidator`](IsJsonValidator.py) - Validates that the value is a json string.
19. [`IsPastDateValidator`](IsPastDateValidator.py) - Validates that the value is a past date.
20. [`IsStringValidator`](IsStringValidator.py) - Validates that the value is a string.
21. [`IsUUIDValidator`](IsUUIDValidator.py) - Validates that the value is a UUID.
22. [`IsWeekdayValidator`](IsWeekdayValidator.py) - Validates that the value is a weekday.
23. [`IsWeekendValidator`](IsWeekendValidator.py) - Validates that the value is a weekend.
24. [`LengthValidator`](LengthValidator.py) - Validates the length of the value.
25. [`NotInArrayValidator`](NotInArrayValidator.py) - Validates that the value is not in the given array.
26. [`NotValidator`](NotValidator.py) - Validates that inverts the result of another validator.
26. [`RangeValidator`](RangeValidator.py) - Validates that the value is within a specified range.
27. [`RegexValidator`](RegexValidator.py) - Validates that the value matches a regex pattern.
