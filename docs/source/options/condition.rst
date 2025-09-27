Condition
=========

``Conditions`` are used to validate the input data based on rules between fields. They ensure that the relationships between multiple fields satisfy specific criteria before further processing.

Overview
--------

Conditions are added using the ``condition()`` declarative. They evaluate the combined input data, ensuring that inter-field dependencies and relationships (such as equality, ordering, or presence) meet predefined rules.

Example
-------

.. code-block:: python

    class TestInputFilter(InputFilter):
        username: str = field(
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        name: str = field(
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        condition(OneOfCondition(['id', 'name']))

Available Conditions
--------------------

- `ArrayLengthEqualCondition <#flask_inputfilter.conditions.ArrayLengthEqualCondition>`_
- `ArrayLongerThanCondition <#flask_inputfilter.conditions.ArrayLongerThanCondition>`_
- `CustomCondition <#flask_inputfilter.conditions.CustomCondition>`_
- `EqualCondition <#flask_inputfilter.conditions.EqualCondition>`_
- `ExactlyNOfCondition <#flask_inputfilter.conditions.ExactlyNOfCondition>`_
- `ExactlyNOfMatchesCondition <#flask_inputfilter.conditions.ExactlyNOfMatchesCondition>`_
- `ExactlyOneOfCondition <#flask_inputfilter.conditions.ExactlyOneOfCondition>`_
- `ExactlyOneOfMatchesCondition <#flask_inputfilter.conditions.ExactlyOneOfMatchesCondition>`_
- `IntegerBiggerThanCondition <#flask_inputfilter.conditions.IntegerBiggerThanCondition>`_
- `NOfCondition <#flask_inputfilter.conditions.NOfCondition>`_
- `NOfMatchesCondition <#flask_inputfilter.conditions.NOfMatchesCondition>`_
- `NotEqualCondition <#flask_inputfilter.conditions.NotEqualCondition>`_
- `OneOfCondition <#flask_inputfilter.conditions.OneOfCondition>`_
- `OneOfMatchesCondition <#flask_inputfilter.conditions.OneOfMatchesCondition>`_
- `RequiredIfCondition <#flask_inputfilter.conditions.RequiredIfCondition>`_
- `StringLongerThanCondition <#flask_inputfilter.conditions.StringLongerThanCondition>`_
- `TemporalOrderCondition <#flask_inputfilter.conditions.TemporalOrderCondition>`_

Base Condition
--------------

.. autoclass:: flask_inputfilter.conditions.BaseCondition
   :members:
   :undoc-members:
   :show-inheritance:

Detailed Description
--------------------

.. automodule:: flask_inputfilter.conditions
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: BaseCondition
