Condition
=========

``Conditions`` are used to validate the input data based on rules between fields. They ensure that the relationships between multiple fields satisfy specific criteria before further processing.

Overview
--------

Conditions are added using the ``addCondition`` method. They evaluate the combined input data, ensuring that inter-field dependencies and relationships (such as equality, ordering, or presence) meet predefined rules.

Example
-------

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import OneOfCondition
    from flask_inputfilter.Filter import StringTrimFilter
    from flask_inputfilter.Validator import IsStringValidator

    class TestInputFilter(InputFilter):
        def __init__(self):

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

The following conditions are available:

- `ArrayLengthEqualCondition`_
- `ArrayLongerThanCondition`_
- `CustomCondition`_
- `EqualCondition`_
- `ExactlyNOfCondition`_
- `ExactlyNOfMatchesCondition`_
- `ExactlyOneOfCondition`_
- `ExactlyOneOfMatchesCondition`_
- `IntegerBiggerThanCondition`_
- `NOfCondition`_
- `NOfMatchesCondition`_
- `NotEqualCondition`_
- `OneOfCondition`_
- `OneOfMatchesCondition`_
- `RequiredIfCondition`_
- `StringLongerThanCondition`_
- `TemporalOrderCondition`_

Detailed Description
--------------------

ArrayLengthEqualCondition
~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Checks if two array fields have equal length.

**Parameters:**

- **first_array_field** (*str*): The first field containing an array.
- **second_array_field** (*str*): The second field containing an array.

**Expected Behavior:**

Validates that the length of the array from ``first_array_field`` is equal to the length of the array from ``second_array_field``. If not, the condition fails.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import ArrayLengthEqualCondition
    from flask_inputfilter.Validator import IsArrayValidator

    class ArrayLengthFilter(InputFilter):
        def __init__(self):

            self.add(
                'list1',
                validators=[IsArrayValidator()]
            )

            self.add(
                'list2',
                validators=[IsArrayValidator()]
            )

            self.addCondition(ArrayLengthEqualCondition('list1', 'list2'))


ArrayLongerThanCondition
~~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Checks if the array in one field is longer than the array in another field.

**Parameters:**

- **longer_field** (*str*): The field expected to have a longer array.
- **shorter_field** (*str*): The field expected to have a shorter array.

**Expected Behavior:**

Validates that the array in ``longer_field`` has more elements than the array in ``shorter_field``.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import ArrayLongerThanCondition
    from flask_inputfilter.Validator import IsArrayValidator

    class ArrayComparisonFilter(InputFilter):
        def __init__(self):

            self.add(
                'list1',
                validators=[IsArrayValidator()]
            )

            self.add(
                'list2',
                validators=[IsArrayValidator()]
            )

            self.addCondition(ArrayLongerThanCondition('list1', 'list2'))


CustomCondition
~~~~~~~~~~~~~~~
**Description:**

Allows defining a custom condition using a user-provided callable.

**Parameters:**

- **condition** (*Callable[[Dict[str, Any]], bool]*): A function that takes the input data and returns a boolean indicating whether the condition is met.

**Expected Behavior:**

Executes the provided callable with the input data. The condition passes if the callable returns ``True``, and fails otherwise.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import CustomCondition
    from flask_inputfilter.Validator import IsIntegerValidator

    def my_custom_condition(data):
        return data.get('age', 0) >= 18

    class CustomFilter(InputFilter):
        def __init__(self):

            self.add(
                'age',
                validators=[IsIntegerValidator()]
            )

            self.addCondition(CustomCondition(my_custom_condition))


EqualCondition
~~~~~~~~~~~~~~
**Description:**

Checks if two specified fields are equal.

**Parameters:**

- **first_field** (*str*): The first field to compare.
- **second_field** (*str*): The second field to compare.

**Expected Behavior:**

Validates that the values of ``first_field`` and ``second_field`` are equal. Fails if they differ.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import EqualCondition

    class EqualFieldsFilter(InputFilter):
        def __init__(self):

            self.add(
                'password'
            )

            self.add(
                'confirm_password'
            )

            self.addCondition(EqualCondition('password', 'confirm_password'))


ExactlyNOfCondition
~~~~~~~~~~~~~~~~~~~
**Description:**

Checks that exactly ``n`` of the specified fields are present in the input data.

**Parameters:**

- **fields** (*List[str]*): A list of fields to check.
- **n** (*int*): The exact number of fields that must be present.

**Expected Behavior:**

Counts the number of specified fields present in the data and validates that the count equals ``n``.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import ExactlyNOfCondition

    class ExactFieldsFilter(InputFilter):
        def __init__(self):

            self.add(
                'field1'
            )

            self.add(
                'field2'
            )

            self.add(
                'field3'
            )

            self.addCondition(ExactlyNOfCondition(['field1', 'field2', 'field3'], 2))


ExactlyNOfMatchesCondition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Checks that exactly ``n`` of the specified fields match a given value.

**Parameters:**

- **fields** (*List[str]*): A list of fields to check.
- **n** (*int*): The exact number of fields that must match the value.
- **value** (*Any*): The value to match against.

**Expected Behavior:**

Validates that exactly ``n`` fields among the specified ones have the given value.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import ExactlyNOfMatchesCondition

    class MatchFieldsFilter(InputFilter):
        def __init__(self):

            self.add(
                'field1'
            )

            self.add(
                'field2'
            )

            self.addCondition(ExactlyNOfMatchesCondition(['field1', 'field2'], 1, 'expected_value'))


ExactlyOneOfCondition
~~~~~~~~~~~~~~~~~~~~~
**Description:**

Ensures that exactly one of the specified fields is present.

**Parameters:**

- **fields** (*List[str]*): A list of fields to check.

**Expected Behavior:**

Validates that only one field among the specified fields exists in the input data.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import ExactlyOneOfCondition

    class OneFieldFilter(InputFilter):
        def __init__(self):

            self.add(
                'email'
            )

            self.add(
                'phone'
            )

            self.addCondition(ExactlyOneOfCondition(['email', 'phone']))


ExactlyOneOfMatchesCondition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Ensures that exactly one of the specified fields matches a given value.

**Parameters:**

- **fields** (*List[str]*): A list of fields to check.
- **value** (*Any*): The value to match against.

**Expected Behavior:**

Validates that exactly one of the specified fields has the given value.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import ExactlyOneOfMatchesCondition

    class OneMatchFilter(InputFilter):
        def __init__(self):

            self.add(
                'option1'
            )

            self.add(
                'option2'
            )

            self.addCondition(ExactlyOneOfMatchesCondition(['option1', 'option2'], 'yes'))


IntegerBiggerThanCondition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Checks if the integer value in one field is greater than that in another field.

**Parameters:**

- **bigger_field** (*str*): The field expected to have a larger integer.
- **smaller_field** (*str*): The field expected to have a smaller integer.

**Expected Behavior:**

Validates that the integer value from ``bigger_field`` is greater than the value from ``smaller_field``.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import IntegerBiggerThanCondition
    from flask_inputfilter.Validator import IsIntegerValidator

    class NumberComparisonFilter(InputFilter):
        def __init__(self):

            self.add(
                'field_should_be_bigger',
                validators=[IsIntegerValidator()]
            )

            self.add(
                'field_should_be_smaller',
                validators=[IsIntegerValidator()]
            )

            self.addCondition(IntegerBiggerThanCondition('field_should_be_better', 'field_should_be_smaller'))


NOfCondition
~~~~~~~~~~~~
**Description:**

Checks that at least ``n`` of the specified fields are present in the input data.

**Parameters:**

- **fields** (*List[str]*): A list of fields to check.
- **n** (*int*): The minimum number of fields that must be present.

**Expected Behavior:**

Validates that the count of the specified fields present is greater than or equal to ``n``.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import NOfCondition

    class MinimumFieldsFilter(InputFilter):
        def __init__(self):

            self.add(
                'field1'
            )

            self.add(
                'field2'
            )

            self.add(
                'field3'
            )

            self.addCondition(NOfCondition(['field1', 'field2', 'field3'], 2))


NOfMatchesCondition
~~~~~~~~~~~~~~~~~~~~~
**Description:**

Checks that at least ``n`` of the specified fields match a given value.

**Parameters:**

- **fields** (*List[str]*): A list of fields to check.
- **n** (*int*): The minimum number of fields that must match the value.
- **value** (*Any*): The value to match against.

**Expected Behavior:**

Validates that the count of fields matching the given value is greater than or equal to ``n``.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import NOfMatchesCondition

    class MinimumMatchFilter(InputFilter):
        def __init__(self):

            self.add(
                'field1'
            )

            self.add(
                'field2'
            )

            self.addCondition(NOfMatchesCondition(['field1', 'field2'], 1, 'value'))


NotEqualCondition
~~~~~~~~~~~~~~~~~
**Description:**

Checks if two specified fields are not equal.

**Parameters:**

- **first_field** (*str*): The first field to compare.
- **second_field** (*str*): The second field to compare.

**Expected Behavior:**

Validates that the values of ``first_field`` and ``second_field`` are not equal.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import NotEqualCondition

    class DifferenceFilter(InputFilter):
        def __init__(self):

            self.add(
                'field1'
            )

            self.add(
                'field2'
            )

            self.addCondition(NotEqualCondition('field1', 'field2'))


OneOfCondition
~~~~~~~~~~~~~~
**Description:**

Ensures that at least one of the specified fields is present in the input data.

**Parameters:**

- **fields** (*List[str]*): A list of fields to check.

**Expected Behavior:**

Validates that at least one field from the specified list is present. Fails if none are present.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import OneOfCondition

    class OneFieldRequiredFilter(InputFilter):
        def __init__(self):

            self.add(
                'email'
            )

            self.add(
                'phone'
            )

            self.addCondition(OneOfCondition(['email', 'phone']))


OneOfMatchesCondition
~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Ensures that at least one of the specified fields matches a given value.

**Parameters:**

- **fields** (*List[str]*): A list of fields to check.
- **value** (*Any*): The value to match against.

**Expected Behavior:**

Validates that at least one field from the specified list has the given value.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import OneOfMatchesCondition

    class OneMatchRequiredFilter(InputFilter):
        def __init__(self):

            self.add(
                'option1'
            )

            self.add(
                'option2'
            )

            self.addCondition(OneOfMatchesCondition(['option1', 'option2'], 'yes'))


RequiredIfCondition
~~~~~~~~~~~~~~~~~~~
**Description:**

Ensures that a field is required if another field has a specific value.

**Parameters:**

- **condition_field** (*str*): The field whose value is checked.
- **value** (*Optional[Union[Any, List[Any]]]*): The value(s) that trigger the requirement.
- **required_field** (*str*): The field that becomes required if the condition is met.

**Expected Behavior:**

If the value of ``condition_field`` matches the specified value (or is in the specified list), then ``required_field`` must be present. Otherwise, the condition passes.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import RequiredIfCondition

    class ConditionalRequiredFilter(InputFilter):
        def __init__(self):

            self.add(
                'status'
            )

            self.add(
                'activation_date'
            )

            self.addCondition(
                RequiredIfCondition(
                    condition_field='status',
                    value='active',
                    required_field='activation_date'
                )
            )


StringLongerThanCondition
~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Checks if the length of the string in one field is longer than the string in another field.

**Parameters:**

- **longer_field** (*str*): The field expected to have a longer string.
- **shorter_field** (*str*): The field expected to have a shorter string.

**Expected Behavior:**

Validates that the string in ``longer_field`` has a greater length than the string in ``shorter_field``.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import StringLongerThanCondition

    class StringLengthFilter(InputFilter):
        def __init__(self):

            self.add(
                'description'
            )

            self.add(
                'summary'
            )

            self.addCondition(StringLongerThanCondition('description', 'summary'))


TemporalOrderCondition
~~~~~~~~~~~~~~~~~~~~~~
**Description:**

Checks if one date is before another, ensuring the correct temporal order. Supports datetime objects, date objects, and ISO 8601 formatted strings.

**Parameters:**

- **smaller_date_field** (*str*): The field containing the earlier date.
- **larger_date_field** (*str*): The field containing the later date.

**Expected Behavior:**

Validates that the date in ``smaller_date_field`` is earlier than the date in ``larger_date_field``. Raises a ``ValidationError`` if the dates are not in the correct order.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import TemporalOrderCondition

    class DateOrderFilter(InputFilter):
        def __init__(self):

            self.add(
                'start_date'
            )

            self.add(
                'end_date'
            )

            self.addCondition(TemporalOrderCondition('start_date', 'end_date'))
