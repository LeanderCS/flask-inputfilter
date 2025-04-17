Special Validator
=================

Overview
--------

Special validators are validators that are used to combine or mutate the normal validators.
They are used to create complex validation logic by combining multiple validators or inverting the result of a validator.

Example
-------

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
- `NotValidator`_
- `OrValidator`_
- `XorValidator`_

Detailed Description
--------------------

AndValidator
~~~~~~~~~~~~

**Description:**

Validates that the input passes all of the provided validators. This composite validator performs a logical AND over its constituent validators.

**Parameters:**

- **validators** (*List[BaseValidator]*): A list of validators that must all pass.
- **error_message** (*Optional[str]*): Custom error message if any of the validators fail.

**Expected Behavior:**

The validator sequentially applies each validator in the provided list to the input value. If any validator raises a ``ValidationError``, the AndValidator immediately raises a ``ValidationError``. If all validators pass, the input is considered valid.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import AndValidator, IsIntegerValidator, RangeValidator

    class AndInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('value', validators=[
                AndValidator([IsIntegerValidator(), RangeValidator(min_value=0, max_value=100)])
            ])

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

OrValidator
~~~~~~~~~~~

**Description:**

Validates that the input passes at least one of the provided validators. This composite validator performs a logical OR over its constituent validators.

**Parameters:**

- **validators** (*List[BaseValidator]*): A list of validators to apply.
- **error_message** (*Optional[str]*): Custom error message if none of the validators pass.

**Expected Behavior:**

The validator applies each validator in the provided list to the input value. If any one validator passes without raising a ``ValidationError``, the validation is considered successful. If all validators fail, it raises a ``ValidationError`` with the provided error message or a default message.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import OrValidator, IsIntegerValidator, IsStringValidator

    class OrInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('value', validators=[
                OrValidator([IsIntegerValidator(), IsStringValidator()])
            ])

XorValidator
~~~~~~~~~~~~

**Description:**

Validates that the input passes exactly one of the provided validators. This composite validator ensures that the input does not pass zero or more than one of the specified validators.

**Parameters:**

- **validators** (*List[BaseValidator]*): A list of validators, of which exactly one must pass.
- **error_message** (*Optional[str]*): Custom error message if the input does not satisfy exactly one validator.

**Expected Behavior:**

The validator applies each validator in the provided list to the input value and counts the number of validators that pass without raising a ``ValidationError``. If exactly one validator passes, the input is considered valid; otherwise, a ``ValidationError`` is raised with the provided or default error message.

**Example Usage:**

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Validator import XorValidator, IsIntegerValidator, IsStringValidator

    class XorInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add('value', validators=[
                XorValidator([IsIntegerValidator(), IsStringValidator()])
            ])
