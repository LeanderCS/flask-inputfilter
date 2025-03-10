Condition
=========

``Conditions`` are used to validate the input data based on rules between fields.

Overview
--------

The `addCondition` method is used to add a condition between fields.

Example
-------

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import OneOfCondition
    from flask_inputfilter.Filter import StringTrimFilter
    from flask_inputfilter.Validator import IsStringValidator


    class TestInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add(
                'username',
                filters=[StringTrimFilter()],
                validators=[IsStringValidator()]
            )

            self.add(
                'name',
                filters=[StringTrimFilter()],
                validators=[IsStringValidator()]
            )

            self.addCondition(
                OneOfCondition(['id', 'name'])
            )

Available Conditions
--------------------

The following conditions are available in the `Condition` module:

1. `ArrayLengthEqualCondition` - Validates that the length of the array is equal to the given value.
2. `ArrayLongerThanCondition` - Validates that the length of the array is longer than the given value.
3. `CustomCondition` - A custom condition that can be used to validate the input data.
4. `EqualCondition` - Validates that the input is equal to the given value.
5. `ExactlyNOfCondition` - Validates that exactly `n` of the given conditions are true.
6. `ExactlyNOfMatchesCondition` - Validates that exactly `n` of the given matches are true.
7. `ExactlyOneOfCondition` - Validates that exactly one of the given conditions is true.
8. `ExactlyOneOfMatchesCondition` - Validates that exactly one of the given matches is true.
9. `IntegerBiggerThanCondition` - Validates that the integer is bigger than the given value.
10. `NOfCondition` - Validates that at least `n` of the given conditions are true.
11. `NOfMatchesCondition` - Validates that at least `n` of the given matches are true.
12. `NotEqualCondition` - Validates that the input is not equal to the given value.
13. `OneOfCondition` - Validates that at least one of the given conditions is true.
14. `OneOfMatchesCondition` - Validates that at least one of the given matches is true.
15. `RequiredIfCondition` - Validates that the input is required if the given field has a specific value.
16. `StringLongerThanCondition` - Validates that the string is longer than the given value.
17. `TemporalOrderCondition` - Validates that the input is in correct temporal order.
