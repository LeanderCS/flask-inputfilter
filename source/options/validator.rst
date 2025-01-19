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

1. :doc:`ArrayElementValidator <../flask_inputfilter/Validator/ArrayElementValidator>`
2. :doc:`ArrayLengthValidator <../flask_inputfilter/Validator/ArrayLengthValidator>`
3. :doc:`DateAfterValidator <../flask_inputfilter/Validator/DateAfterValidator>`
4. :doc:`DateBeforeValidator <../flask_inputfilter/Validator/DateBeforeValidator>`
5. :doc:`DateRangeValidator <../flask_inputfilter/Validator/DateRangeValidator>`
6. :doc:`FloatPrecisionValidator <../flask_inputfilter/Validator/FloatPrecisionValidator>`
7. :doc:`InArrayValidator <../flask_inputfilter/Validator/InArrayValidator>`
8. :doc:`InEnumValidator <../flask_inputfilter/Validator/InEnumValidator>`
9. :doc:`IsArrayValidator <../flask_inputfilter/Validator/IsArrayValidator>`
10. :doc:`IsBase64ImageCorrectSizeValidator <../flask_inputfilter/Validator/IsBase64ImageCorrectSizeValidator>`
11. :doc:`IsBase64ImageValidator <../flask_inputfilter/Validator/IsBase64ImageValidator>`
12. :doc:`IsBooleanValidator <../flask_inputfilter/Validator/IsBooleanValidator>`
13. :doc:`IsFloatValidator <../flask_inputfilter/Validator/IsFloatValidator>`
14. :doc:`IsFutureDateValidator <../flask_inputfilter/Validator/IsFutureDateValidator>`
15. :doc:`IsHexadecimalValidator <../flask_inputfilter/Validator/IsHexadecimalValidator>`
16. :doc:`IsHorizontalImageValidator <../flask_inputfilter/Validator/IsHorizontalImageValidator>`
17. :doc:`IsInstanceValidator <../flask_inputfilter/Validator/IsInstanceValidator>`
18. :doc:`IsIntegerValidator <../flask_inputfilter/Validator/IsIntegerValidator>`
19. :doc:`IsJsonValidator <../flask_inputfilter/Validator/IsJsonValidator>`
20. :doc:`IsPastDateValidator <../flask_inputfilter/Validator/IsPastDateValidator>`
21. :doc:`IsStringValidator <../flask_inputfilter/Validator/IsStringValidator>`
22. :doc:`IsUUIDValidator <../flask_inputfilter/Validator/IsUUIDValidator>`
23. :doc:`IsVerticalImageValidator <../flask_inputfilter/Validator/IsVerticalImageValidator>`
24. :doc:`IsWeekdayValidator <../flask_inputfilter/Validator/IsWeekdayValidator>`
25. :doc:`IsWeekendValidator <../flask_inputfilter/Validator/IsWeekendValidator>`
26. :doc:`LengthValidator <../flask_inputfilter/Validator/LengthValidator>`
27. :doc:`NotInArrayValidator <../flask_inputfilter/Validator/NotInArrayValidator>`
28. :doc:`NotValidator <../flask_inputfilter/Validator/NotValidator>`
29. :doc:`RangeValidator <../flask_inputfilter/Validator/RangeValidator>`
30. :doc:`RegexValidator <../flask_inputfilter/Validator/RegexValidator>`
