# Validator

The `Validator` class is used to validate the data after the filters have been applied.

## Available validators

The following validators are available in the `Validator` module:

1. [`ArrayElementValidator`](ArrayElementValidator.py) - Validates each element of an array with its own defined InputFilter.
2. [`ArrayLengthValidator`](ArrayLengthValidator.py) - Validates the length of an array.
3. [`FloatPrecisionValidator`](FloatPrecisionValidator.py) - Validates the precision of a float.
4. [`InArrayValidator`](InArrayValidator.py) - Validates that the value is in the given array.
5. [`InEnumValidator`](InEnumValidator.py) - Validates that the value is in the given enum.
6. [`IsArrayValidator`](IsArrayValidator.py) - Validates that the value is an array.
7. [`IsBase64ImageCorrectSizeValidator`](IsBase64ImageCorrectSizeValidator.py) - Validates that the value is a base64 encoded string.
8. [`IsBase64ImageValidator`](IsBase64ImageValidator.py) - Validates that the value is a base64 encoded string.
9. [`IsBooleanValidator`](IsBooleanValidator.py) - Validates that the value is a boolean.
10. [`IsFloatValidator`](IsFloatValidator.py) - Validates that the value is a float.
11. [`IsHexadecimalValidator`](IsHexadecimalValidator.py) - Validates that the value is a hexadecimal string.
12. [`IsInstanceValidator`](IsInstanceValidator.py) - Validates that the value is an instance of a class.
13. [`IsIntegerValidator`](IsIntegerValidator.py) - Validates that the value is an integer.
14. [`IsJsonValidator`](IsJsonValidator.py) - Validates that the value is a json string.
15. [`IsStringValidator`](IsStringValidator.py) - Validates that the value is a string.
16. [`IsUUIDValidator`](IsUUIDValidator.py) - Validates that the value is a UUID.
17. [`LengthValidator`](LengthValidator.py) - Validates the length of the value.
18. [`RangeValidator`](RangeValidator.py) - Validates that the value is within a specified range.
19. [`RegexValidator`](RegexValidator.py) - Validates that the value matches a regex pattern.
