Special Validator
=================

Special validators are validators that are used to combine or mutate the normal validators.
They are used to create complex validation logic by combining multiple validators or inverting the result of a validator.

Overview
--------


Example


.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import NotValidator, IsIntegerValidator

    class NotIntegerInputFilter(InputFilter):
        def __init__(self):
            super().__init__()
            self.add('value', validators=[
                NotValidator(validator=IsIntegerValidator())
            ])

Available Special Validators
----------------------------

The following special validators are available:

- `AndValidator`_
- `IfValidator`_
- `NotValidator`_
- `OrValidator`_
- `XorValidator`_

Detailed Description
--------------------

NotValidator
~~~~~~~~~~~~
**Description:**

Inverts the result of another validator. The validation passes if the inner validator fails, and vice versa.

**Parameters:**

- **validator** (*BaseValidator*): The validator whose outcome is to be inverted.
- **error_message** (*Optional[str]*): Custom error message if the inverted validation does not behave as expected.

**Expected Behavior:**

Executes the inner validator on the input. If the inner validator does not raise a ``ValidationError``, then the NotValidator raises one instead.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import NotValidator, IsIntegerValidator

    class NotIntegerInputFilter(InputFilter):
        def __init__(self):
            super().__init__()
            self.add('value', validators=[
                NotValidator(validator=IsIntegerValidator())
            ])
