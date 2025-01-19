Validator
=========

The `Validator` class is used to validate the data after the filters have been applied.

Validators
----------

Validators can be added into the `add` method for a specific field or as a global validator for all fields in `addGlobalValidator`.

The global validation will be executed before the specific field validation.

Example
-------

Here is an example of how to use validators in an `InputFilter`:

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import IsIntegerValidator, RangeValidator


    class UpdatePointsInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

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

The following validators are available in the `Validator` module:

1. `ArrayElementValidator`
2. `ArrayLengthValidator`
3. `DateAfterValidator`
4. `DateBeforeValidator`
5. `DateRangeValidator`
6. `FloatPrecisionValidator`
7. `InArrayValidator`
8. `InEnumValidator`
9. `IsArrayValidator`
10. `IsBase64ImageCorrectSizeValidator`
11. `IsBase64ImageValidator`
12. `IsBooleanValidator`
13. `IsFloatValidator`
14. `IsFutureDateValidator`
15. `IsHexadecimalValidator`
16. `IsHorizontalImageValidator`
17. `IsInstanceValidator`
18. `IsIntegerValidator`
19. `IsJsonValidator`
20. `IsPastDateValidator`
21. `IsStringValidator`
22. `IsUUIDValidator`
23. `IsVerticalImageValidator`
24. `IsWeekdayValidator`
25. `IsWeekendValidator`
26. `LengthValidator`
27. `NotInArrayValidator`
28. `NotValidator`
29. `RangeValidator`
30. `RegexValidator`
