flask-inputfilter
==================================

The `InputFilter` class is used to validate and filter input data in Flask applications.
It provides a modular way to clean and ensure that incoming data meets expected format
and type requirements before being processed.

:Test Status:

    .. image:: https://img.shields.io/github/actions/workflow/status/LeanderCS/flask-inputfilter/test.yaml?branch=main&style=flat-square&label=Github%20Actions
        :target: https://github.com/LeanderCS/flask-inputfilter/actions
    .. image:: https://img.shields.io/coveralls/LeanderCS/flask-inputfilter/main.svg?style=flat-square&label=Coverage
        :target: https://coveralls.io/r/LeanderCS/flask-inputfilter

:Version Info:

    .. image:: https://img.shields.io/pypi/v/flask-inputfilter?style=flat-square&label=PyPI
        :target: https://pypi.org/project/flask-inputfilter/

:Compatibility:

    .. image:: https://img.shields.io/pypi/pyversions/flask-inputfilter?style=flat-square&label=PyPI
        :target: https://pypi.org/project/flask-inputfilter/

:Downloads:

    .. image:: https://img.shields.io/pypi/dm/flask-inputfilter?style=flat-square&label=PyPI
        :target: https://pypi.org/project/flask-inputfilter/

Installation
============

.. code-block:: bash

    pip install flask-inputfilter

Quickstart
==========

To use the `InputFilter` class, create a new class that inherits from it and define the
fields you want to validate and filter.

There are numerous filters and validators available, but you can also create your `own <CREATE_OWN.md>`.

Definition
----------

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import ExactlyOneOfCondition
    from flask_inputfilter.Enum import RegexEnum
    from flask_inputfilter.Filter import StringTrimFilter, ToIntegerFilter, ToNullFilter
    from flask_inputfilter.Validator import IsIntegerValidator, IsStringValidator, RegexValidator

    class UpdateZipcodeInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add(
                'id',
                required=True,
                filters=[ToIntegerFilter(), ToNullFilter()],
                validators=[
                    IsIntegerValidator()
                ]
            )

            self.add(
                'zipcode',
                filters=[StringTrimFilter()],
                validators=[
                    RegexValidator(
                        RegexEnum.POSTAL_CODE.value,
                        'The zipcode is not in the correct format.'
                    )
                ]
            )

            self.add(
                'city',
                filters=[StringTrimFilter()],
                validators=[
                    IsStringValidator()
                ]
            )

            self.addCondition(
                ExactlyOneOfCondition(['zipcode', 'city'])
            )

Usage
-----

To use the `InputFilter` class, call the `validate` method on the class instance.
After calling `validate`, the validated data will be available in `g.validatedData`.
If the data is invalid, a 400 response with an error message will be returned.

.. code-block:: python

    from flask import Flask, g
    from your-path import UpdateZipcodeInputFilter

    app = Flask(__name__)

    @app.route('/update-zipcode', methods=['POST'])
    @UpdateZipcodeInputFilter.validate()
    def updateZipcode():
        data = g.validatedData

        # Do something with validated data
        id = data.get('id')
        zipcode = data.get('zipcode')

Options
=======

The `add` method supports several options:

- `Required`_
- `Filter <flask_inputfilter/Filter/README.md>`_
- `Validator <flask_inputfilter/Validator/README.md>`_
- `Default`_
- `Fallback`_
- `ExternalApi <EXTERNAL_API.md>`_

Required
--------

The `required` option specifies whether the field must be included in the input data.
If the field is missing, a `ValidationError` will be raised with an appropriate error message.

Default
-------

The `default` option allows you to specify a default value to use if the field is not
present in the input data.

Fallback
--------

The `fallback` option specifies a value to use if validation fails or required data
is missing. Note that if the field is optional and absent, `fallback` will not apply;
use `default` in such cases.
