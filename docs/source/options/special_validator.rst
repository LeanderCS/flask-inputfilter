Special Validator
=================

Overview
--------

Special validators are validators that are used to combine or mutate the normal validators.
They are used to create complex validation logic by combining multiple validators or inverting the result of a validator.

Example
-------

.. code-block:: python

    class NotIntegerInputFilter(InputFilter):
        value: str = field(
            validators=[NotValidator(validator=IsIntegerValidator())]
        )

Available Special Validators
----------------------------

The following special validators are available:

- `AndValidator <#flask_inputfilter.validators.AndValidator>`_
- `NotValidator <#flask_inputfilter.validators.NotValidator>`_
- `OrValidator <#flask_inputfilter.validators.OrValidator>`_
- `XorValidator <#flask_inputfilter.validators.XorValidator>`_

Detailed Description
--------------------

.. autoclass:: flask_inputfilter.validators.AndValidator
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: flask_inputfilter.validators.NotValidator
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: flask_inputfilter.validators.OrValidator
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: flask_inputfilter.validators.XorValidator
   :members:
   :undoc-members:
   :show-inheritance:
