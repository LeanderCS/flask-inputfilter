# Validator

The `Validator` class is used to validate the data after the filters have been applied.

## Available validators

The following validators are available in the `Validator` module:

1. [`ArrayElementValidator`](src/flask_inputfilter/Validator/ArrayElementValidator.py) - Validates each element of an array with its own defined InputFilter.
2. [`ArrayLengthValidator`](src/flask_inputfilter/Validator/ArrayLengthValidator.py) - Validates the length of an array.
3. [`InArrayValidator`](src/flask_inputfilter/Validator/InArrayValidator.py) - Validates that the value is in the given array.
4. [`InEnumValidator`](src/flask_inputfilter/Validator/InEnumValidator.py) - Validates that the value is in the given enum.
5. [`IsArrayValidator`](src/flask_inputfilter/Validator/IsArrayValidator.py) - Validates that the value is an array.
6. [`IsBase64ImageCorrectSizeValidator`](src/flask_inputfilter/Validator/IsBase64ImageCorrectSizeValidator.py) - Validates that the value is a base64 encoded string.
7. [`IsBase64ImageValidator`](src/flask_inputfilter/Validator/IsBase64ImageValidator.py) - Validates that the value is a base64 encoded string.
8. [`IsBooleanValidator`](src/flask_inputfilter/Validator/IsBooleanValidator.py) - Validates that the value is a boolean.
9. [`IsFloatValidator`](src/flask_inputfilter/Validator/IsFloatValidator.py) - Validates that the value is a float.
10. [`IsHexadecimalValidator`](src/flask_inputfilter/Validator/IsHexadecimalValidator.py) - Validates that the value is a hexadecimal string.
11. [`IsInstanceValidator`](src/flask_inputfilter/Validator/IsInstanceValidator.py) - Validates that the value is an instance of a class.
12. [`IsIntegerValidator`](src/flask_inputfilter/Validator/IsIntegerValidator.py) - Validates that the value is an integer.
13. [`IsJsonValidator`](src/flask_inputfilter/Validator/IsJsonValidator.py) - Validates that the value is a json string.
14. [`IsStringValidator`](src/flask_inputfilter/Validator/IsStringValidator.py) - Validates that the value is a string.
15. [`IsUUIDValidator`](src/flask_inputfilter/Validator/IsUUIDValidator.py) - Validates that the value is a UUID.
16. [`LengthValidator`](src/flask_inputfilter/Validator/LengthValidator.py) - Validates the length of the value.
17. [`RangeValidator`](src/flask_inputfilter/Validator/RangeValidator.py) - Validates that the value is within a specified range.
18. [`RegexValidator`](src/flask_inputfilter/Validator/RegexValidator.py) - Validates that the value matches a regex pattern.
