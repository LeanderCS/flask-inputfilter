Validator
=========

``Validators`` are used to validate the data after filters have been applied. 
They ensure that the input data meets the required conditions before further processing.

Overview
--------

Validators can be added into the ``add`` method for a specific field or as a global validator for all fields in ``add_global_validator``.

The global validation will be executed before the specific field validation.

Example
-------

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.validators import IsIntegerValidator, RangeValidator

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

            self.add_global_validator(IsIntegerValidator())

Available Validators
--------------------

- `ArrayElementValidator <#flask_inputfilter.validators.ArrayElementValidator>`_
- `ArrayLengthValidator <#flask_inputfilter.validators.ArrayLengthValidator>`_
- `CustomJsonValidator <#flask_inputfilter.validators.CustomJsonValidator>`_
- `DateAfterValidator <#flask_inputfilter.validators.DateAfterValidator>`_
- `DateBeforeValidator <#flask_inputfilter.validators.DateBeforeValidator>`_
- `DateRangeValidator <#flask_inputfilter.validators.DateRangeValidator>`_
- `FloatPrecisionValidator <#flask_inputfilter.validators.FloatPrecisionValidator>`_
- `InArrayValidator <#flask_inputfilter.validators.InArrayValidator>`_
- `InEnumValidator <#flask_inputfilter.validators.InEnumValidator>`_
- `IsArrayValidator <#flask_inputfilter.validators.IsArrayValidator>`_
- `IsBase64ImageCorrectSizeValidator <#flask_inputfilter.validators.IsBase64ImageCorrectSizeValidator>`_
- `IsBase64ImageValidator <#flask_inputfilter.validators.IsBase64ImageValidator>`_
- `IsBooleanValidator <#flask_inputfilter.validators.IsBooleanValidator>`_
- `IsDataclassValidator <#flask_inputfilter.validators.IsDataclassValidator>`_
- `IsDateTimeValidator <#flask_inputfilter.validators.IsDateTimeValidator>`_
- `IsDateValidator <#flask_inputfilter.validators.IsDateValidator>`_
- `IsFloatValidator <#flask_inputfilter.validators.IsFloatValidator>`_
- `IsFutureDateValidator <#flask_inputfilter.validators.IsFutureDateValidator>`_
- `IsHexadecimalValidator <#flask_inputfilter.validators.IsHexadecimalValidator>`_
- `IsHorizontalImageValidator <#flask_inputfilter.validators.IsHorizontalImageValidator>`_
- `IsHtmlValidator <#flask_inputfilter.validators.IsHtmlValidator>`_
- `IsInstanceValidator <#flask_inputfilter.validators.IsInstanceValidator>`_
- `IsIntegerValidator <#flask_inputfilter.validators.IsIntegerValidator>`_
- `IsJsonValidator <#flask_inputfilter.validators.IsJsonValidator>`_
- `IsLowercaseValidator <#flask_inputfilter.validators.IsLowercaseValidator>`_
- `IsMacAddressValidator <#flask_inputfilter.validators.IsMacAddressValidator>`_
- `IsPastDateValidator <#flask_inputfilter.validators.IsPastDateValidator>`_
- `IsPortValidator <#flask_inputfilter.validators.IsPortValidator>`_
- `IsRgbColorValidator <#flask_inputfilter.validators.IsRgbColorValidator>`_
- `IsStringValidator <#flask_inputfilter.validators.IsStringValidator>`_
- `IsTypedDictValidator <#flask_inputfilter.validators.IsTypedDictValidator>`_
- `IsUppercaseValidator <#flask_inputfilter.validators.IsUppercaseValidator>`_
- `IsUrlValidator <#flask_inputfilter.validators.IsUrlValidator>`_
- `IsUUIDValidator <#flask_inputfilter.validators.IsUUIDValidator>`_
- `IsVerticalImageValidator <#flask_inputfilter.validators.IsVerticalImageValidator>`_
- `IsWeekdayValidator <#flask_inputfilter.validators.IsWeekdayValidator>`_
- `IsWeekendValidator <#flask_inputfilter.validators.IsWeekendValidator>`_
- `LengthValidator <#flask_inputfilter.validators.LengthValidator>`_
- `NotInArrayValidator <#flask_inputfilter.validators.NotInArrayValidator>`_
- `RangeValidator <#flask_inputfilter.validators.RangeValidator>`_
- `RegexValidator <#flask_inputfilter.validators.RegexValidator>`_

Special Validators
------------------

Following are the special validators that are used to combine or mutate the normal validators:

- :doc:`AndValidator <special_validator>`
- :doc:`NotValidator <special_validator>`
- :doc:`OrValidator <special_validator>`
- :doc:`XorValidator <special_validator>`

Base Validator
--------------

.. autoclass:: flask_inputfilter.validators.BaseValidator
   :members:
   :undoc-members:
   :show-inheritance:

Detailed Description
--------------------

.. automodule:: flask_inputfilter.validators
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: BaseValidator, AndValidator, NotValidator, OrValidator, XorValidator
